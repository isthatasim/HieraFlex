from __future__ import annotations

from fastapi import APIRouter

from backend.app.models.simulation import SimulationControlRequest, SimulationSeekRequest
from backend.app.services.replay_service import replay_service
from backend.app.services.simulation_runtime import simulation_runtime

router = APIRouter(prefix="/simulation", tags=["simulation"])


@router.post("/start")
async def start_simulation(req: SimulationControlRequest) -> dict:
    engine = replay_service.reset_engine(scenario_id=req.scenario_id)
    engine.configure(scenario_id=req.scenario_id, start=req.start_index, end=req.end_index, speed=req.replay_speed)
    await simulation_runtime.ensure_running(scenario_id=req.scenario_id)
    return {"status": "started", "state": engine.snapshot()}


@router.post("/pause")
def pause_simulation() -> dict:
    engine = replay_service.ensure()
    engine.pause()
    return {"status": "paused", "state": engine.snapshot()}


@router.post("/reset")
def reset_simulation() -> dict:
    engine = replay_service.ensure()
    engine.reset()
    return {"status": "reset", "state": engine.snapshot()}


@router.post("/seek")
def seek_simulation(req: SimulationSeekRequest) -> dict:
    engine = replay_service.ensure()
    engine.seek(req.step)
    return {"status": "seeked", "state": engine.snapshot()}
