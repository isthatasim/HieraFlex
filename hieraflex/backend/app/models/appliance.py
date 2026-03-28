from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ApplianceModel(BaseModel):
    appliance_id: str
    house_id: str
    nominal_power_kw: float = Field(ge=0.0)
    interruptible: bool = True
    flexible: bool = True
    cycle_duration_steps: int = Field(default=1, ge=1)
    earliest_start_step: int = 0
    latest_finish_step: int = 288
