from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.app.models.experiment import RunCompareRequest, RunEvaluateRequest, TrainingResumeRequest, TrainingStartRequest, TrainingStopRequest
from backend.app.services.checkpoint_service import checkpoint_service
from backend.app.services.experiment_tracker import experiment_tracker
from backend.app.services.training_manager import training_manager
from backend.app.services.run_registry import run_registry

router = APIRouter(prefix="/training", tags=["training"])


@router.post("/start")
def start_training(req: TrainingStartRequest) -> dict:
    try:
        run = training_manager.start_run(req.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"status": "started", "run": run}


@router.post("/stop")
def stop_training(req: TrainingStopRequest) -> dict:
    try:
        run = training_manager.stop_run(req.run_id)
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"status": "stop_requested", "run": run}


@router.post("/resume")
def resume_training(req: TrainingResumeRequest) -> dict:
    try:
        run = training_manager.resume_run(run_id=req.run_id, checkpoint_path=req.checkpoint_path, extra_episodes=req.extra_episodes)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"status": "resumed", "run": run}


@router.get("/status")
def training_status() -> dict:
    training_manager.sync_processes()
    runs = run_registry.list_runs()
    active = [r for r in runs if r.get("status") in {"running", "starting", "stop_requested"}]
    return {"active_runs": len(active), "runs": runs[:20]}


@router.get("/runs")
def list_runs() -> dict:
    training_manager.sync_processes()
    return {"runs": run_registry.list_runs()}


@router.get("/runs/{run_id}")
def run_details(run_id: str) -> dict:
    try:
        return training_manager.run_details(run_id)
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/runs/{run_id}/metrics")
def run_metrics(run_id: str, limit: int = 300) -> dict:
    rows = experiment_tracker.metrics(run_id, limit=max(1, min(limit, 2000)))
    return {"run_id": run_id, "metrics": rows}


@router.get("/runs/{run_id}/checkpoints")
def run_checkpoints(run_id: str) -> dict:
    return {"run_id": run_id, "checkpoints": checkpoint_service.list_checkpoints(run_id)}


@router.post("/runs/{run_id}/evaluate")
def run_evaluate(run_id: str, req: RunEvaluateRequest) -> dict:
    # Lightweight API-side evaluation summary over tracked metrics.
    summary = experiment_tracker.summarize(run_id)
    return {"run_id": run_id, "scenario_id": req.scenario_id, "summary": summary}


@router.post("/compare")
def compare_runs(req: RunCompareRequest) -> dict:
    run_ids = req.run_ids or [r["run_id"] for r in run_registry.list_runs()[:5]]
    return {"comparisons": experiment_tracker.compare(run_ids)}


@router.get("/runs/{run_id}/logs")
def run_logs(run_id: str, tail: int = 200) -> dict:
    run = run_registry.load_run(run_id)
    path = run_registry.run_dir(run_id) / "worker.log"
    if not path.exists():
        return {"run_id": run_id, "logs": []}
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    return {"run_id": run_id, "logs": lines[-max(1, min(tail, 5000)) :]}
