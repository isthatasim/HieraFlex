from __future__ import annotations

import asyncio
from collections import defaultdict

from fastapi import WebSocket


class LiveStreamHub:
    def __init__(self) -> None:
        self.channels: dict[str, set[WebSocket]] = defaultdict(set)

    async def connect(self, channel: str, ws: WebSocket) -> None:
        await ws.accept()
        self.channels[channel].add(ws)

    def disconnect(self, channel: str, ws: WebSocket) -> None:
        if channel in self.channels:
            self.channels[channel].discard(ws)

    async def broadcast(self, channel: str, payload: dict) -> None:
        dead: list[WebSocket] = []
        for ws in self.channels.get(channel, set()):
            try:
                await ws.send_json(payload)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(channel, ws)

    async def fanout(self, payloads: dict[str, dict]) -> None:
        await asyncio.gather(*(self.broadcast(ch, data) for ch, data in payloads.items()))


live_stream_hub = LiveStreamHub()
