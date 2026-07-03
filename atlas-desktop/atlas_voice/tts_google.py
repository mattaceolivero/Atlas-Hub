"""Text-to-speech via Google Cloud Text-to-Speech — Chirp 3: HD voices.

Synthesizes a sentence at a time (the brain streams sentences) so Atlas starts
speaking almost immediately. Returns raw 24 kHz mono int16 PCM chunks the Speaker
can play, with barge-in able to cut playback at any chunk boundary.

Voice: any `en-US-Chirp3-HD-*` name (config `tts.voice_name`). Pick the one you
like as "Atlas's voice".
"""

from __future__ import annotations

import asyncio

from google.cloud import texttospeech


# LINEAR16 responses are a WAV container; strip the 44-byte header to get raw PCM.
_WAV_HEADER_BYTES = 44


class GoogleChirpTTS:
    def __init__(self, voice_name: str = "en-US-Chirp3-HD-Charon",
                 language_code: str = "en-US", sample_rate: int = 24000,
                 speaking_rate: float = 1.0, chunk_ms: int = 40) -> None:
        self._client = texttospeech.TextToSpeechClient()
        self._voice = texttospeech.VoiceSelectionParams(
            language_code=language_code, name=voice_name
        )
        self._audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate,
            speaking_rate=speaking_rate,
        )
        self.sample_rate = sample_rate
        # bytes per playback chunk (int16 = 2 bytes/sample)
        self._chunk_bytes = int(sample_rate * chunk_ms / 1000) * 2

    def _synth_sync(self, text: str) -> bytes:
        resp = self._client.synthesize_speech(
            input=texttospeech.SynthesisInput(text=text),
            voice=self._voice,
            audio_config=self._audio_config,
        )
        pcm = resp.audio_content
        return pcm[_WAV_HEADER_BYTES:] if len(pcm) > _WAV_HEADER_BYTES else pcm

    async def stream(self, text: str):
        """Async-yield int16 PCM byte chunks for one sentence."""
        loop = asyncio.get_running_loop()
        pcm = await loop.run_in_executor(None, self._synth_sync, text)
        for i in range(0, len(pcm), self._chunk_bytes):
            yield pcm[i : i + self._chunk_bytes]
