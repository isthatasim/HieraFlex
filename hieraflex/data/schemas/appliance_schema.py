from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ApplianceSample(BaseModel):
    timestamp: str
    house_id: str
    appliance_id: str
    power_kw: float = Field(ge=0.0)
    state: Literal["on", "off"]
    source: Literal["deddiag", "synthetic"] = "deddiag"


class ApplianceMeta(BaseModel):
    house_id: str
    appliance_id: str
    nominal_power_kw: float
    cycle_duration_steps: int = Field(default=1, ge=1)
    interruptible: bool = False
    earliest_start_step: int = 0
    latest_finish_step: int = 96
    priority_weight: float = 1.0
    discomfort_weight: float = 1.0
    flexibility_flag: bool = True
