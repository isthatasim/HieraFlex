from __future__ import annotations

from fastapi import APIRouter

from backend.app.core.db import db
from backend.app.services.experiment_service import experiment_service
from backend.app.services.simulation_runtime import simulation_runtime

router = APIRouter(prefix="/results", tags=["results"])


@router.get("/summary")
def summary() -> dict:
    if "latest" in db.results:
        return db.results["latest"]
    return simulation_runtime.compute_summary()


@router.get("/export")
def export_results() -> dict:
    summary_data = summary()
    exported = experiment_service.export_summary(summary_data if summary_data else {"per_house": []})
    return {"status": "ok", "files": exported}
