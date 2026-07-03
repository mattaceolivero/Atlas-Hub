"""Text-to-speech via the Gemini API — key-only, no project or service account.

Works with just a Gemini API key (GEMINI_API_KEY). Gemini TTS returns raw 24 kHz
mono 16-bit PCM, which the Speaker plays directly. Synthesizes one sentence at a
time (the brain streams sentences) so Atlas starts talking almost immediately.

Voice: a Gemini prebuilt voice name (config `tts.gemini_voice`), e.g. "Charon",
"Kore", "Puck", "Aoede". Pick the one you want as "Atlas's voice".
"""

from __future__ import annotations

import asyncio
import os

from google import genai
from google.genai import types


class GeminiTTS:
    def __init__(self, voice_name: str = "Charon",
                 model: str = "gemini-2.5-flash-preview-tts",
                 sample_rate: int = 24000, chunk_ms: int = 40) -> None:
        self._client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        self._model = model
        self._voice = voice_name
        self.sample_rate = sample_rate                       # Gemini TTS = 24 kHz PCM
        self._chunk_bytes = int(sample_rate * chunk_ms / 1000) * 2

    def _synth_sync(self, text: str) -> bytes:
        resp = self._client.models.generate_content(
            model=self._model,
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=self._voice
                        )
                    )
                ),
            ),
        )
        return resp.candidates[0].content.parts[0].inline_data.data  # raw int16 PCM

    async def stream(self, text: str):
        """Async-yield int16 PCM byte chunks for one sentence."""
        loop = asyncio.get_running_loop()
        pcm = await loop.run_in_executor(None, self._synth_sync, text)
        for i in range(0, len(pcm), self._chunk_bytes):
            yield pcm[i : i + self._chunk_bytes]
