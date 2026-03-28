from __future__ import annotations

from pydantic import BaseModel, Field


class ReplayConfig(BaseModel):
    scenario_id: str = "demo_week"
    start_index: int = 0
    end_index: int = 288
    replay_speed: float = Field(default=60.0, gt=0.0)
    loop: bool = False
