from __future__ import annotations

import asyncio
import contextlib

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.appliances import router as appliances_router
from backend.app.api.deployment import router as deployment_router
from backend.app.api.evaluation import router as evaluation_router
from backend.app.api.houses import router as houses_router
from backend.app.api.market import router as market_router
from backend.app.api.results import router as results_router
from backend.app.api.simulation import router as simulation_router
from backend.app.api.training import router as training_router
from backend.app.core.config import get_settings
from backend.app.core.logging import setup_logging
from backend.app.services.replay_service import replay_service
from backend.app.services.simulation_runtime import simulation_runtime
from backend.app.sockets.live_stream import live_stream_hub

settings = get_settings()
setup_logging(settings.log_level)

app = FastAPI(title="HieraFlex", description="Hierarchical Flexibility Intelligence for Community Energy Trading", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in [
    houses_router,
    appliances_router,
    market_router,
    simulation_router,
    training_router,
    evaluation_router,
    results_router,
    deployment_router,
]:
    app.include_router(router)


@app.get("/")
def root() -> dict:
    return {
        "name": "HieraFlex",
        "description": "Hierarchical Flexibility Intelligence for Community Energy Trading",
        "state": replay_service.ensure().snapshot(),
    }


@app.websocket("/ws/{channel}")
async def ws_channel(websocket: WebSocket, channel: str) -> None:
    await live_stream_hub.connect(channel, websocket)
    try:
        while True:
            await websocket.receive_text()
            await websocket.send_json({"ok": True, "channel": channel})
    except WebSocketDisconnect:
        live_stream_hub.disconnect(channel, websocket)


@app.on_event("startup")
async def startup() -> None:
    replay_service.ensure()


@app.on_event("shutdown")
async def shutdown() -> None:
    if simulation_runtime.task and not simulation_runtime.task.done():
        simulation_runtime.task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await simulation_runtime.task


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.app.main:app", host=settings.api_host, port=settings.api_port, reload=False)

