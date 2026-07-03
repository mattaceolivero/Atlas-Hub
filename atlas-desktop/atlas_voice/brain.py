"""The brain: run the Atlas Hub project as a persistent agent via the Claude Agent SDK.

This loads the repo's CLAUDE.md (Atlas's charter), the specialists in
`.claude/agents/`, the skills, and `.claude/settings.json` — so the voice you talk
to *is* Atlas, with the whole collective behind it. Conversation state persists
across turns for the life of the app (one continuous session).

SDK: `pip install claude-agent-sdk` (Python 3.10+).
Docs: https://code.claude.com/docs/en/agent-sdk/python
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import AsyncIterator

from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AssistantMessage,
    TextBlock,
    ResultMessage,
)

# Tool-use blocks carry a `.name`; TextBlock does not. We detect them structurally.
_SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


class Brain:
    def __init__(self, hub_path: str, model: str = "claude-opus-4-8",
                 permission_mode: str = "bypassPermissions") -> None:
        self.hub_path = str(Path(hub_path).resolve())
        self.options = ClaudeAgentOptions(
            model=model,
            cwd=self.hub_path,
            # Load CLAUDE.md, .claude/agents/, skills, settings.json, and .mcp.json:
            setting_sources=["project", "user"],
            allowed_tools=[
                "Read", "Write", "Edit", "Glob", "Grep", "Bash", "Agent", "Skill",
                # the specialists (subagents) and their MCP tools are auto-approved:
                "mcp__*",
            ],
            permission_mode=permission_mode,   # headless: no interactive prompts
            max_turns=20,
        )
        self._client: ClaudeSDKClient | None = None

    async def __aenter__(self) -> "Brain":
        self._client = ClaudeSDKClient(options=self.options)
        await self._client.connect()
        return self

    async def __aexit__(self, *exc) -> None:
        if self._client:
            await self._client.disconnect()
            self._client = None

    async def ask(self, prompt: str) -> AsyncIterator[tuple[str, str]]:
        """Send a turn; yield ('speak', sentence) and ('action', tool_name) events.

        Text is chunked into sentences so TTS can start speaking the first sentence
        while Atlas is still generating the rest (low perceived latency).
        """
        assert self._client is not None, "Brain not connected"
        # Nudge Atlas to answer in a spoken register (short, no markdown) for voice.
        framed = (
            "[Spoken conversation — reply the way you'd say it out loud: concise, "
            "natural, no markdown, no lists unless asked. If you need to act, do it.]\n\n"
            + prompt
        )
        await self._client.query(framed)

        buffer = ""
        async for message in self._client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        buffer += block.text
                        # Emit complete sentences as they form.
                        while True:
                            m = _SENTENCE_END.search(buffer)
                            if not m:
                                break
                            sentence, buffer = buffer[: m.start()], buffer[m.end():]
                            sentence = sentence.strip()
                            if sentence:
                                yield ("speak", sentence)
                    elif getattr(block, "name", None):  # ToolUseBlock
                        yield ("action", block.name)
            elif isinstance(message, ResultMessage):
                break

        tail = buffer.strip()
        if tail:
            yield ("speak", tail)
