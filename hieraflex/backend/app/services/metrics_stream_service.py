from __future__ import annotations

from typing import Any

from backend.app.services.checkpoint_service import checkpoint_service
from backend.app.services.experiment_tracker import experiment_tracker


class MetricsStreamService:
    def __init__(self) -> None:
        self.metric_cursors: dict[str, int] = {}
        self.checkpoint_cursors: dict[str, int] = {}

    def latest_metrics(self, run_id: str, limit: int = 100) -> list[dict[str, Any]]:
        return experiment_tracker.metrics(run_id, limit=limit)

    def latest_checkpoints(self, run_id: str, limit: int = 50) -> list[dict[str, Any]]:
        rows = checkpoint_service.list_checkpoints(run_id)
        return rows[-limit:]

    def poll(self, run_id: str) -> dict[str, Any]:
        metrics = experiment_tracker.metrics(run_id)
        checkpoints = checkpoint_service.list_checkpoints(run_id)

        m_start = self.metric_cursors.get(run_id, 0)
        c_start = self.checkpoint_cursors.get(run_id, 0)

        new_metrics = metrics[m_start:]
        new_checkpoints = checkpoints[c_start:]

        self.metric_cursors[run_id] = len(metrics)
        self.checkpoint_cursors[run_id] = len(checkpoints)

        return {
            "run_id": run_id,
            "new_metrics": new_metrics,
            "new_checkpoints": new_checkpoints,
            "latest_metric": metrics[-1] if metrics else None,
            "latest_checkpoint": checkpoints[-1] if checkpoints else None,
        }


metrics_stream_service = MetricsStreamService()
