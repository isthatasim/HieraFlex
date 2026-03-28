from __future__ import annotations

import time
import uuid

from fastapi import APIRouter

from backend.app.core.db import db

router = APIRouter(prefix="/training", tags=["training"])


@router.post("/start")
def start_training(config_path: str = "experiments/configs/single_house.yaml") -> dict:
    job_id = str(uuid.uuid4())
    db.training_jobs[job_id] = {
        "job_id": job_id,
        "status": "running",
        "config_path": config_path,
        "started_at": time.time(),
        "progress": 0.05,
        "message": "Training launched (mock pipeline ready for replacement with full PPO trainer).",
    }
    return db.training_jobs[job_id]


@router.get("/status")
def training_status() -> dict:
    if not db.training_jobs:
        return {"jobs": []}
    jobs = []
    for jid, st in db.training_jobs.items():
        elapsed = max(0.0, time.time() - st["started_at"])
        progress = min(1.0, 0.05 + elapsed / 60.0)
        status = "completed" if progress >= 1.0 else "running"
        st["progress"] = progress
        st["status"] = status
        jobs.append(st)
    return {"jobs": jobs}
