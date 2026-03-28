from __future__ import annotations

from pydantic import BaseModel, Field


class SimulationControlRequest(BaseModel):
    scenario_id: str = "demo_week"
    start_index: int = 0
    end_index: int = 288
    replay_speed: float = Field(default=60.0, gt=0)


class SimulationSeekRequest(BaseModel):
    step: int = Field(ge=0)


class SimulationStateModel(BaseModel):
    running: bool
    current_step: int
    start_index: int
    end_index: int
    speed: float
    scenario_id: str
    timeline_size: int
