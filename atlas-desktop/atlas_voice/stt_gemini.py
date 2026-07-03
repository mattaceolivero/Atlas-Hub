"""Speech-to-text via the Gemini API — key-only, no project or service account.

The local Silero VAD already tells us when you've finished a thought, so we wrap
the captured utterance as a WAV and ask Gemini to transcribe it verbatim. Works
with just a Gemini API key (GEMINI_API_KEY).
"""

from __future__ import annotations

import asyncio
import io
import os
import struct

from google import genai
from google.genai import types


def _wav(pcm: bytes, sample_rate: int) -> bytes:
    """Wrap raw mono int16 PCM in a minimal WAV container."""
    n = len(pcm)
    buf = io.BytesIO()
    buf.write(b"RIFF")
    buf.write(struct.pack("<I", 36 + n))
    buf.write(b"WAVEfmt ")
    buf.write(struct.pack("<IHHIIHH", 16, 1, 1, sample_rate, sample_rate * 2, 2, 16))
    buf.write(b"data")
    buf.write(struct.pack("<I", n))
    buf.write(pcm)
    return buf.getvalue()


_PROMPT = (
    "Transcribe this audio verbatim. Output ONLY the transcript text with no "
    "preamble, quotes, or commentary. If there is no speech, output nothing."
)


class GeminiSTT:
    def __init__(self, model: str = "gemini-2.5-flash", sample_rate: int = 16000) -> None:
        self._client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        self._model = model
        self.sample_rate = sample_rate

    def _recognize_sync(self, pcm: bytes) -> str:
        audio = types.Part.from_bytes(
            data=_wav(pcm, self.sample_rate), mime_type="audio/wav"
        )
        resp = self._client.models.generate_content(
            model=self._model, contents=[audio, _PROMPT]
        )
        return (resp.text or "").strip()

    async def transcribe(self, pcm: bytes) -> str:
        if not pcm:
            return ""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._recognize_sync, pcm)
