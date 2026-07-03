"""Local HUD server — serves the reactive orb and pushes live state to it.

A tiny aiohttp app on localhost with a websocket. The voice loop calls
`push_state` / `push_transcript`; the browser orb reacts. Self-contained, no
external assets, so it works offline.
"""

from __future__ import annotations

import asyncio
import json
import webbrowser
from pathlib import Path

from aiohttp import web

from ..state import State

_INDEX = Path(__file__).resolve().parent / "index.html"


class HudServer:
    def __init__(self, cfg: dict) -> None:
        self.port = cfg.get("port", 4173)
        self.open_browser = cfg.get("open_browser_on_start", True)
        self.theme = cfg.get("theme", "reactor")
        self.reduced_motion = cfg.get("reduced_motion", False)
        self._app = web.Application()
        self._app.add_routes([
            web.get("/", self._index),
            web.get("/ws", self._ws),
        ])
        self._runner: web.AppRunner | None = None
        self._sockets: set[web.WebSocketResponse] = set()

    async def _index(self, request: web.Request) -> web.Response:
        html = _INDEX.read_text()
        html = html.replace("__THEME__", self.theme)
        html = html.replace("__REDUCED_MOTION__", "true" if self.reduced_motion else "false")
        return web.Response(text=html, content_type="text/html")

    async def _ws(self, request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        self._sockets.add(ws)
        try:
            async for _ in ws:  # we only push; ignore inbound
                pass
        finally:
            self._sockets.discard(ws)
        return ws

    async def _broadcast(self, payload: dict) -> None:
        dead = []
        for ws in self._sockets:
            try:
                await ws.send_str(json.dumps(payload))
            except ConnectionResetError:
                dead.append(ws)
        for ws in dead:
            self._sockets.discard(ws)

    # ---- called by the voice loop ----
    async def push_state(self, state: State) -> None:
        await self._broadcast({"type": "state", "state": state.value})

    async def push_transcript(self, role: str, text: str) -> None:
        await self._broadcast({"type": "transcript", "role": role, "text": text})

    async def start(self) -> None:
        self._runner = web.AppRunner(self._app)
        await self._runner.setup()
        site = web.TCPSite(self._runner, "127.0.0.1", self.port)
        await site.start()
        url = f"http://127.0.0.1:{self.port}"
        print(f"HUD: {url}")
        if self.open_browser:
            try:
                webbrowser.open(url)
            except Exception:
                pass

    async def stop(self) -> None:
        for ws in list(self._sockets):
            await ws.close()
        if self._runner:
            await self._runner.cleanup()
