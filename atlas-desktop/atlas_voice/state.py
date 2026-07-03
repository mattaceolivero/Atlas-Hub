"""Conversation states and events for Atlas Desktop.

The whole app is a state machine:

    IDLE --"Hey Atlas"--> LISTENING --(you stop talking)--> THINKING --> SPEAKING
      ^                        ^                                            |
      |                        |------------- barge-in ---------------------|
      |                                                                     |
      +--- window timeout / end-phrase <--- ACTING (tools/apps) <-----------+

The HUD subscribes to these states to drive the orb's visuals, and the audio
layer uses them to decide whether the mic is hot and whether TTS may play.
"""

from __future__ import annotations

import asyncio
from enum import Enum
from typing import Callable, Awaitable


class State(str, Enum):
    IDLE = "idle"            # asleep, only the wake-word spotter is listening
    LISTENING = "listening"  # capturing your speech, streaming to STT
    THINKING = "thinking"    # Atlas is reasoning / calling tools
    SPEAKING = "speaking"    # TTS is playing (mic still hot for barge-in)
    ACTING = "acting"        # running a tool / opening an app

    # sub-signal, not a lifecycle state — used only for the HUD transcript
    def label(self) -> str:
        return {
            State.IDLE: "asleep",
            State.LISTENING: "listening",
            State.THINKING: "thinking",
            State.SPEAKING: "speaking",
            State.ACTING: "working",
        }[self]


StateListener = Callable[[State], Awaitable[None]]
TranscriptListener = Callable[[str, str], Awaitable[None]]  # (role, text)


class Bus:
    """Tiny async pub/sub so the loop, the HUD, and the audio layer stay decoupled."""

    def __init__(self) -> None:
        self._state = State.IDLE
        self._state_listeners: list[StateListener] = []
        self._transcript_listeners: list[TranscriptListener] = []
        # Set when the user barges in while Atlas is speaking; TTS watches this.
        self.interrupt = asyncio.Event()

    @property
    def state(self) -> State:
        return self._state

    def on_state(self, fn: StateListener) -> None:
        self._state_listeners.append(fn)

    def on_transcript(self, fn: TranscriptListener) -> None:
        self._transcript_listeners.append(fn)

    async def set_state(self, state: State) -> None:
        self._state = state
        for fn in self._state_listeners:
            await fn(state)

    async def say_transcript(self, role: str, text: str) -> None:
        """role: 'you' | 'atlas' | 'action'"""
        for fn in self._transcript_listeners:
            await fn(role, text)
