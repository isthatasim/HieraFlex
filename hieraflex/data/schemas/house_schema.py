from __future__ import annotations

from pydantic import BaseModel, Field


class HouseMeta(BaseModel):
    house_id: str
    power_cap_kw: float = Field(default=8.0, gt=0.0)
    has_pv: bool = True
    has_battery: bool = True
    has_ev: bool = True
