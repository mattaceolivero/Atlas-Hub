"""Atlas Desktop — hands-free voice loop.

Single-consumer state machine over the mic:

  IDLE  ── wake word "Hey Atlas" ──►  LISTENING ── you stop (VAD) ──►  THINKING
    ▲                                     ▲                              │
    │ window elapsed                      │  barge-in (you talk)         ▼
    └──────────────────────────  SPEAKING/ACTING ◄──── stream answer ────┘

One coroutine ("ears") owns the microphone and dispatches frames by state, so the
mic is never double-read. Speaking happens in a separate task, letting the ears
keep listening for barge-in while Atlas talks.
"""

from __future__ import annotations

import asyncio
import os
import time
from pathlib import Path

import yaml
from dotenv import load_dotenv

from .state import Bus, State
from .audio import MicStream, Speaker
from .wakeword import WakeWord
from .vad import Endpointer
from .brain import Brain
from .hud.server import HudServer

FRAME_MS = 32  # 512 samples @ 16 kHz — matches Porcupine + Silero frame sizes
SAMPLE_RATE = 16000


def _build_stt(cfg: dict):
    provider = cfg["stt"].get("provider", "gemini")
    if provider == "gemini":
        from .stt_gemini import GeminiSTT
        return GeminiSTT(cfg["stt"].get("gemini_model", "gemini-2.5-flash"), SAMPLE_RATE)
    if provider == "google-chirp":
        from .stt_google import GoogleChirpSTT
        return GoogleChirpSTT(cfg["stt"]["language_codes"], cfg["stt"]["chirp_model"],
                              cfg["stt"]["location"], SAMPLE_RATE)
    raise SystemExit(f"Unknown stt.provider: {provider}")


def _build_tts(cfg: dict):
    provider = cfg["tts"].get("provider", "gemini")
    if provider == "gemini":
        from .tts_gemini import GeminiTTS
        return GeminiTTS(cfg["tts"].get("gemini_voice", "Charon"),
                         cfg["tts"].get("gemini_model", "gemini-2.5-flash-preview-tts"),
                         cfg["tts"]["sample_rate_hz"])
    if provider == "google-chirp":
        from .tts_google import GoogleChirpTTS
        return GoogleChirpTTS(cfg["tts"]["chirp_voice_name"], cfg["tts"]["language_code"],
                              cfg["tts"]["sample_rate_hz"], cfg["tts"]["speaking_rate"])
    raise SystemExit(f"Unknown tts.provider: {provider}")


def load_config() -> dict:
    here = Path(__file__).resolve().parent.parent
    load_dotenv(here / ".env")
    with open(here / "config.yaml") as f:
        return yaml.safe_load(f)


class AtlasVoice:
    def __init__(self, cfg: dict) -> None:
        self.cfg = cfg
        self.bus = Bus()
        self.mic = MicStream(sample_rate=SAMPLE_RATE, frame_ms=FRAME_MS,
                             device=cfg["audio"].get("input_device"))
        self.wake = WakeWord(
            cfg["wake_word"].get("keyword_path"),
            cfg["wake_word"].get("sensitivity", 0.6),
            cfg["wake_word"].get("builtin_fallback"),
        )
        self.ep = Endpointer(
            SAMPLE_RATE, FRAME_MS,
            cfg["vad"]["speech_start_ms"], cfg["vad"]["silence_end_ms"],
        )
        self.bargein_ep = Endpointer(
            SAMPLE_RATE, FRAME_MS,
            cfg["vad"]["speech_start_ms"], cfg["vad"]["silence_end_ms"],
        )
        self.stt = _build_stt(cfg)
        self.tts = _build_tts(cfg)
        self.speaker = Speaker(sample_rate=cfg["tts"]["sample_rate_hz"],
                               device=cfg["audio"].get("output_device"))
        self.hud = HudServer(cfg["hud"]) if cfg["hud"]["enabled"] else None

        self.window_s = cfg["conversation"]["continuous_window_seconds"]
        self.end_phrases = [p.lower() for p in cfg["conversation"]["end_phrases"]]
        self.max_utt = cfg["vad"]["max_utterance_seconds"]

        self._utter = bytearray()
        self._awake_until = 0.0
        self._respond_task: asyncio.Task | None = None
        self._brain: Brain | None = None

    # ---- helpers ---------------------------------------------------------
    def _is_end_phrase(self, text: str) -> bool:
        t = text.lower().strip(" .!?")
        return any(p in t for p in self.end_phrases)

    async def _speak_text(self, text: str) -> bool:
        """Speak one string; returns False if barged-in."""
        await self.bus.say_transcript("atlas", text)
        return await self.speaker.play(self.tts.stream(text))

    # ---- the speaking task (runs concurrently with the ears) -------------
    async def _respond(self, text: str) -> None:
        self.bus.interrupt.clear()
        try:
            await self.bus.set_state(State.THINKING)
            spoke_anything = False
            async for kind, payload in self._brain.ask(text):
                if self.bus.interrupt.is_set():
                    break
                if kind == "action":
                    await self.bus.set_state(State.ACTING)
                    await self.bus.say_transcript("action", payload)
                elif kind == "speak":
                    await self.bus.set_state(State.SPEAKING)
                    self.bargein_ep.reset()
                    spoke_anything = True
                    if not await self._speak_text(payload):
                        break  # barged in
            if not spoke_anything and not self.bus.interrupt.is_set():
                await self._speak_text("Done.")
        finally:
            # Hand control back to the ears in LISTENING, extending the window.
            if self.bus.state in (State.SPEAKING, State.THINKING, State.ACTING):
                self._awake_until = time.monotonic() + self.window_s
                self.ep.reset()
                self._utter = bytearray()
                await self.bus.set_state(State.LISTENING)

    async def _handle_utterance(self) -> None:
        pcm = bytes(self._utter)
        self._utter = bytearray()
        await self.bus.set_state(State.THINKING)
        text = (await self.stt.transcribe(pcm)).strip()
        if not text:
            await self.bus.set_state(State.LISTENING)
            return
        await self.bus.say_transcript("you", text)
        if self._is_end_phrase(text):
            await self._speak_text("Talk soon.")
            await self.bus.set_state(State.IDLE)
            return
        self._respond_task = asyncio.create_task(self._respond(text))

    # ---- the ears: single mic consumer -----------------------------------
    async def run(self) -> None:
        if self.hud:
            self.bus.on_state(self.hud.push_state)
            self.bus.on_transcript(self.hud.push_transcript)
            await self.hud.start()

        self.mic.start()
        async with Brain(
            self.cfg["brain"]["hub_path"],
            self.cfg["brain"]["model"],
            self.cfg["brain"]["permission_mode"],
        ) as brain:
            self._brain = brain
            await self.bus.set_state(State.IDLE)
            greeting = self.cfg["brain"].get("greeting")
            if greeting:
                await self.speaker.play(self.tts.stream(greeting))
            print(f'Atlas is listening. Say "{self._wake_phrase()}".')

            async for frame in self.mic.frames():
                st = self.bus.state
                if st is State.IDLE:
                    if self.wake.process(frame):
                        self._awake_until = time.monotonic() + self.window_s
                        self.ep.reset()
                        self._utter = bytearray()
                        await self.bus.set_state(State.LISTENING)

                elif st is State.LISTENING:
                    ev = self.ep.update(frame)
                    if self.ep.started:
                        self._utter.extend(frame)
                    if ev == "done":
                        await self._handle_utterance()
                    elif not self.ep.started and time.monotonic() > self._awake_until:
                        await self.bus.set_state(State.IDLE)

                elif st is State.SPEAKING:
                    # Watch for barge-in while Atlas talks.
                    if self.cfg["conversation"]["barge_in"]:
                        ev = self.bargein_ep.update(frame)
                        if ev == "started":
                            self.bus.interrupt.set()
                            self.speaker.interrupt()
                            self._awake_until = time.monotonic() + self.window_s
                            self.ep.reset()
                            self._utter = bytearray(frame)
                            await self.bus.set_state(State.LISTENING)

                # THINKING / ACTING: ignore mic; the respond task drives us onward.

    def _wake_phrase(self) -> str:
        return "Hey Atlas" if "custom" in self.wake.name else self.wake.name.split(":")[-1]

    async def aclose(self) -> None:
        self.mic.stop()
        self.speaker.close()
        self.wake.close()
        if self.hud:
            await self.hud.stop()


def main() -> None:
    cfg = load_config()
    # The brain uses your Claude Code login (no ANTHROPIC_API_KEY needed).
    required = ["PICOVOICE_ACCESS_KEY"]
    uses_gemini = "gemini" in (cfg["stt"].get("provider"), cfg["tts"].get("provider"))
    uses_chirp = "google-chirp" in (cfg["stt"].get("provider"), cfg["tts"].get("provider"))
    if uses_gemini:
        required.append("GEMINI_API_KEY")
    if uses_chirp:
        required.append("GOOGLE_APPLICATION_CREDENTIALS")
    for var in required:
        if not os.environ.get(var):
            raise SystemExit(f"Missing {var}. Copy .env.example to .env and fill it in.")
    app = AtlasVoice(cfg)
    try:
        asyncio.run(app.run())
    except KeyboardInterrupt:
        print("\nAtlas going to sleep.")
    finally:
        asyncio.run(app.aclose())


if __name__ == "__main__":
    main()
