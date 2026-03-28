from __future__ import annotations

from fastapi import APIRouter

from backend.app.core.db import db
from backend.app.services.simulation_runtime import simulation_runtime

router = APIRouter(prefix="/evaluation", tags=["evaluation"])


@router.post("/run")
def run_evaluation() -> dict:
    summary = simulation_runtime.compute_summary()
    db.results["latest"] = summary
    return {"status": "ok", "summary": summary}
