from __future__ import annotations

from pydantic import BaseModel, Field


class ExperimentRequest(BaseModel):
    config_path: str
    scenario_id: str = "demo_week"


class ExperimentStatus(BaseModel):
    job_id: str
    status: str
    message: str


class TrainingStartRequest(BaseModel):
    algorithm: str = "ppo_single"
    config_path: str = "experiments/configs/single_house.yaml"
    scenario_id: str = "demo_week"
    episodes: int = Field(default=120, ge=1, le=50000)
    seed: int = 42
    checkpoint_interval: int = Field(default=5, ge=1)
    eval_interval: int = Field(default=10, ge=1)
    price_mode: str = "real_time"
    houses: list[str] = Field(default_factory=lambda: ["H1"])
    notes: str = ""


class TrainingStopRequest(BaseModel):
    run_id: str


class TrainingResumeRequest(BaseModel):
    run_id: str
    checkpoint_path: str | None = None
    extra_episodes: int = Field(default=60, ge=1, le=50000)


class RunCompareRequest(BaseModel):
    run_ids: list[str] = Field(default_factory=list)


class RunEvaluateRequest(BaseModel):
    scenario_id: str = "demo_week"
