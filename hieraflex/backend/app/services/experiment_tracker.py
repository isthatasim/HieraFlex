from __future__ import annotations

from pathlib import Path
from typing import Any

from backend.app.services.io_utils import append_jsonl, read_jsonl
from backend.app.services.run_registry import run_registry


class ExperimentTracker:
    def metrics_file(self, run_id: str) -> Path:
        return run_registry.run_dir(run_id) / "metrics.jsonl"

    def evaluations_file(self, run_id: str) -> Path:
        return run_registry.run_dir(run_id) / "evaluations.jsonl"

    def append_metric(self, run_id: str, metric: dict[str, Any]) -> None:
        append_jsonl(self.metrics_file(run_id), metric)

    def append_evaluation(self, run_id: str, metric: dict[str, Any]) -> None:
        append_jsonl(self.evaluations_file(run_id), metric)

    def metrics(self, run_id: str, limit: int | None = None) -> list[dict[str, Any]]:
        rows = read_jsonl(self.metrics_file(run_id))
        return rows[-limit:] if limit else rows

    def evaluations(self, run_id: str, limit: int | None = None) -> list[dict[str, Any]]:
        rows = read_jsonl(self.evaluations_file(run_id))
        return rows[-limit:] if limit else rows

    def summarize(self, run_id: str) -> dict[str, Any]:
        rows = self.metrics(run_id)
        if not rows:
            return {"run_id": run_id, "episodes": 0}
        best = max(rows, key=lambda r: float(r.get("episode_return", -1e9)))
        latest = rows[-1]
        avg_last = sum(float(r.get("episode_return", 0.0)) for r in rows[-10:]) / min(len(rows), 10)
        return {
            "run_id": run_id,
            "episodes": len(rows),
            "latest_return": float(latest.get("episode_return", 0.0)),
            "best_return": float(best.get("episode_return", 0.0)),
            "avg_last_10": float(avg_last),
        }

    def compare(self, run_ids: list[str]) -> list[dict[str, Any]]:
        return [self.summarize(run_id) for run_id in run_ids]


experiment_tracker = ExperimentTracker()
