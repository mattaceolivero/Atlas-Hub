"""Speech-to-text via Google Cloud Speech-to-Text v2 — Chirp 2.

The local Silero VAD already tells us when you've finished a thought, so we
capture the whole utterance and transcribe it in one v2 `recognize` call against
the Chirp 2 model. Simple and reliable; streaming interim results are a later
enhancement (the HUD shows a listening pulse in the meantime).

Chirp requires a *regional* endpoint (e.g. us-central1), not the global one.
"""

from __future__ import annotations

import asyncio
import os

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech


class GoogleChirpSTT:
    def __init__(self, language_codes: list[str], model: str = "chirp_2",
                 location: str = "us-central1", sample_rate: int = 16000) -> None:
        self.project = os.environ["GOOGLE_CLOUD_PROJECT"]
        self.location = location
        self.sample_rate = sample_rate
        self._client = SpeechClient(
            client_options={"api_endpoint": f"{location}-speech.googleapis.com"}
        )
        self._config = cloud_speech.RecognitionConfig(
            explicit_decoding_config=cloud_speech.ExplicitDecodingConfig(
                encoding=cloud_speech.ExplicitDecodingConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=sample_rate,
                audio_channel_count=1,
            ),
            language_codes=language_codes,
            model=model,
        )
        self._recognizer = (
            f"projects/{self.project}/locations/{location}/recognizers/_"
        )

    def _recognize_sync(self, pcm: bytes) -> str:
        request = cloud_speech.RecognizeRequest(
            recognizer=self._recognizer,
            config=self._config,
            content=pcm,
        )
        response = self._client.recognize(request=request)
        parts = [
            r.alternatives[0].transcript
            for r in response.results
            if r.alternatives
        ]
        return " ".join(p.strip() for p in parts).strip()

    async def transcribe(self, pcm: bytes) -> str:
        """Transcribe a full utterance of 16 kHz mono int16 PCM."""
        if not pcm:
            return ""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._recognize_sync, pcm)
