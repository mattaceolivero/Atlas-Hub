"""'Hey Atlas' wake-word spotter (Picovoice Porcupine, on-device).

Only the wake word is matched locally — no audio leaves the machine until Atlas
is awake. Generate a custom "Hey Atlas" keyword (.ppn) free at
https://console.picovoice.ai (see scripts/get_wakeword.md). Until you do, this
falls back to a built-in keyword (default "jarvis") so you can test immediately.
"""

from __future__ import annotations

import os
import struct
from pathlib import Path

import pvporcupine


class WakeWord:
    def __init__(self, keyword_path: str | None, sensitivity: float = 0.6,
                 builtin_fallback: str | None = "jarvis") -> None:
        access_key = os.environ["PICOVOICE_ACCESS_KEY"]

        kw = Path(keyword_path) if keyword_path else None
        if kw and kw.exists():
            self._porcupine = pvporcupine.create(
                access_key=access_key,
                keyword_paths=[str(kw)],
                sensitivities=[sensitivity],
            )
            self.name = f"custom:{kw.stem}"
        elif builtin_fallback:
            self._porcupine = pvporcupine.create(
                access_key=access_key,
                keywords=[builtin_fallback],
                sensitivities=[sensitivity],
            )
            self.name = f"builtin:{builtin_fallback}"
        else:
            raise FileNotFoundError(
                f"Wake-word file not found ({keyword_path}) and no builtin_fallback set. "
                "Create 'Hey Atlas' at https://console.picovoice.ai — see scripts/get_wakeword.md."
            )

    @property
    def frame_length(self) -> int:
        return self._porcupine.frame_length

    @property
    def sample_rate(self) -> int:
        return self._porcupine.sample_rate  # 16000

    def process(self, frame_bytes: bytes) -> bool:
        """Return True when the wake word is detected in this frame."""
        pcm = struct.unpack_from("h" * self._porcupine.frame_length, frame_bytes)
        return self._porcupine.process(pcm) >= 0

    def close(self) -> None:
        self._porcupine.delete()
