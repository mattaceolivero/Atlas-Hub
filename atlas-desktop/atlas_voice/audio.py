"""Microphone capture and speaker playback.

A single always-open input stream feeds both the wake-word spotter and the STT
recognizer via an asyncio queue of 16 kHz mono int16 frames. Playback is a
separate output stream that can be cut instantly for barge-in.
"""

from __future__ import annotations

import asyncio
import queue
import numpy as np
import sounddevice as sd


class MicStream:
    """Continuous mic capture → async frames of int16 PCM at `sample_rate`."""

    def __init__(self, sample_rate: int = 16000, frame_ms: int = 20,
                 device: int | None = None) -> None:
        self.sample_rate = sample_rate
        self.frame_samples = int(sample_rate * frame_ms / 1000)
        self.device = device
        self._q: "queue.Queue[bytes]" = queue.Queue()
        self._stream: sd.RawInputStream | None = None

    def _callback(self, indata, frames, time_info, status) -> None:  # sd thread
        if status:
            # Overflows are non-fatal; drop and continue.
            pass
        self._q.put(bytes(indata))

    def start(self) -> None:
        self._stream = sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=self.frame_samples,
            dtype="int16",
            channels=1,
            device=self.device,
            callback=self._callback,
        )
        self._stream.start()

    def stop(self) -> None:
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None

    async def frames(self):
        """Yield int16 PCM frames (bytes) as they arrive, without blocking the loop."""
        loop = asyncio.get_running_loop()
        while True:
            frame = await loop.run_in_executor(None, self._q.get)
            yield frame


class Speaker:
    """Streaming playback with instant interrupt for barge-in."""

    def __init__(self, sample_rate: int = 24000, device: int | None = None) -> None:
        self.sample_rate = sample_rate
        self.device = device
        self._stream: sd.OutputStream | None = None
        self._interrupt = False

    def _ensure(self) -> None:
        if self._stream is None:
            self._stream = sd.OutputStream(
                samplerate=self.sample_rate, channels=1, dtype="int16",
                device=self.device,
            )
            self._stream.start()

    def interrupt(self) -> None:
        """Called on barge-in: the next write() will bail and playback stops."""
        self._interrupt = True

    async def play(self, pcm_chunks) -> bool:
        """Play an async iterator of int16 PCM byte chunks.

        Returns True if it finished, False if interrupted (barge-in).
        """
        self._interrupt = False
        self._ensure()
        loop = asyncio.get_running_loop()
        async for chunk in pcm_chunks:
            if self._interrupt:
                return False
            audio = np.frombuffer(chunk, dtype=np.int16)
            await loop.run_in_executor(None, self._stream.write, audio)
        return not self._interrupt

    def close(self) -> None:
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None
