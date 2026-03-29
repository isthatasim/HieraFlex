from __future__ import annotations

import subprocess
import uuid
from pathlib import Path
from typing import Any

from backend.app.services.io_utils import ensure_dir, project_root, read_json, utc_now_iso, write_json


class RunRegistry:
    """Persistent run metadata registry stored as one JSON per run."""

    def __init__(self) -> None:
        self.root = project_root() / "experiments" / "outputs" / "json" / "runs"
        ensure_dir(self.root)

    def run_dir(self, run_id: str) -> Path:
        return ensure_dir(self.root / run_id)

    def run_file(self, run_id: str) -> Path:
        return self.run_dir(run_id) / "run.json"

    def _git_commit(self) -> str | None:
        try:
            out = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=str(project_root()), text=True)
            return out.strip()
        except Exception:
            return None

    def create_run(self, payload: dict[str, Any]) -> dict[str, Any]:
        run_id = payload.get("run_id") or uuid.uuid4().hex[:12]
        path = self.run_file(run_id)
        if path.exists():
            raise ValueError(f"Run id already exists: {run_id}")

        now = utc_now_iso()
        run = {
            "run_id": run_id,
            "algorithm": payload.get("algorithm", "ppo_single"),
            "config_path": payload.get("config_path", "experiments/configs/single_house.yaml"),
            "scenario_id": payload.get("scenario_id", "demo_week"),
            "status": payload.get("status", "queued"),
            "created_at": now,
            "started_at": payload.get("started_at"),
            "ended_at": payload.get("ended_at"),
            "updated_at": now,
            "episodes_target": int(payload.get("episodes_target", 100)),
            "current_episode": int(payload.get("current_episode", 0)),
            "current_step": int(payload.get("current_step", 0)),
            "latest_checkpoint": payload.get("latest_checkpoint"),
            "best_checkpoint": payload.get("best_checkpoint"),
            "metrics_path": str(self.run_dir(run_id) / "metrics.jsonl"),
            "checkpoints_path": str(self.run_dir(run_id) / "checkpoints.jsonl"),
            "worker_log": str(self.run_dir(run_id) / "worker.log"),
            "git_commit": payload.get("git_commit") or self._git_commit(),
            "seed": int(payload.get("seed", 42)),
            "price_mode": payload.get("price_mode", "real_time"),
            "houses": payload.get("houses", ["H1"]),
            "notes": payload.get("notes", ""),
        }
        write_json(path, run)
        return run

    def load_run(self, run_id: str) -> dict[str, Any]:
        run = read_json(self.run_file(run_id), default={})
        if not run:
            raise FileNotFoundError(f"Run not found: {run_id}")
        return run

    def update_run(self, run_id: str, **updates: Any) -> dict[str, Any]:
        run = self.load_run(run_id)
        run.update(updates)
        run["updated_at"] = utc_now_iso()
        write_json(self.run_file(run_id), run)
        return run

    def list_runs(self) -> list[dict[str, Any]]:
        runs: list[dict[str, Any]] = []
        for run_dir in sorted(self.root.glob("*")):
            if not run_dir.is_dir():
                continue
            payload = read_json(run_dir / "run.json", default={})
            if payload:
                runs.append(payload)
        runs.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return runs

    def mark_recovered_states(self) -> None:
        for run in self.list_runs():
            if run.get("status") in {"running", "starting", "stop_requested", "stopping"}:
                self.update_run(run["run_id"], status="interrupted", ended_at=utc_now_iso())


run_registry = RunRegistry()
