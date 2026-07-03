"""Endpointing with Silero VAD — decides when you've *finished* a thought.

Tuned generously (config: silence_end_ms) because Matt pauses mid-sentence and
should never be cut off. Fed 16 kHz int16 frames; emits a boolean "speech now"
and tracks trailing silence so the loop knows when to stop capturing.
"""

from __future__ import annotations

import numpy as np

try:
    # silero-vad>=5 ships a small ONNX model + helper.
    from silero_vad import load_silero_vad
    _HAVE_SILERO = True
except Exception:  # pragma: no cover - import guard for setup clarity
    _HAVE_SILERO = False


class Endpointer:
    """Streaming utterance endpointer.

    Usage per turn:
        ep.reset()
        for frame in frames:            # 16 kHz int16, 30 ms recommended
            state = ep.update(frame)
            if state == "done": break
    """

    def __init__(self, sample_rate: int = 16000, frame_ms: int = 32,
                 speech_start_ms: int = 200, silence_end_ms: int = 1200,
                 threshold: float = 0.5) -> None:
        if not _HAVE_SILERO:
            raise RuntimeError(
                "silero-vad not installed. `pip install silero-vad onnxruntime`."
            )
        self.sample_rate = sample_rate
        self.threshold = threshold
        self.speech_start_frames = max(1, speech_start_ms // frame_ms)
        self.silence_end_frames = max(1, silence_end_ms // frame_ms)
        self._model = load_silero_vad(onnx=True)
        self.reset()

    def reset(self) -> None:
        self._speech_run = 0
        self._silence_run = 0
        self.started = False
        self._model.reset_states()

    def _prob(self, frame_bytes: bytes) -> float:
        import torch
        audio = np.frombuffer(frame_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        # Silero expects 512-sample (32ms) chunks at 16k; pad/truncate as needed.
        if len(audio) < 512:
            audio = np.pad(audio, (0, 512 - len(audio)))
        else:
            audio = audio[:512]
        return float(self._model(torch.from_numpy(audio), self.sample_rate).item())

    def update(self, frame_bytes: bytes) -> str:
        """Return 'silence' | 'speaking' | 'started' | 'done'."""
        speech = self._prob(frame_bytes) >= self.threshold
        if speech:
            self._speech_run += 1
            self._silence_run = 0
            if not self.started and self._speech_run >= self.speech_start_frames:
                self.started = True
                return "started"
            return "speaking" if self.started else "silence"
        else:
            self._silence_run += 1
            self._speech_run = 0
            if self.started and self._silence_run >= self.silence_end_frames:
                return "done"
            return "silence"
