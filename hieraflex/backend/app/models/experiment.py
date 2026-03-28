from __future__ import annotations

from pydantic import BaseModel


class ExperimentRequest(BaseModel):
    config_path: str
    scenario_id: str = "demo_week"


class ExperimentStatus(BaseModel):
    job_id: str
    status: str
    message: str
