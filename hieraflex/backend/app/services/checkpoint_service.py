from __future__ import annotations

from pathlib import Path
from typing import Any

from backend.app.services.io_utils import append_jsonl, read_jsonl
from backend.app.services.run_registry import run_registry


class CheckpointService:
    def checkpoints_dir(self, run_id: str) -> Path:
        return run_registry.run_dir(run_id) / "checkpoints"

    def checkpoints_file(self, run_id: str) -> Path:
        return run_registry.run_dir(run_id) / "checkpoints.jsonl"

    def register(self, run_id: str, checkpoint_path: str, episode: int, score: float, is_best: bool) -> dict[str, Any]:
        event = {
            "run_id": run_id,
            "checkpoint_path": checkpoint_path,
            "episode": int(episode),
            "score": float(score),
            "is_best": bool(is_best),
        }
        append_jsonl(self.checkpoints_file(run_id), event)
        return event

    def list_checkpoints(self, run_id: str) -> list[dict[str, Any]]:
        return read_jsonl(self.checkpoints_file(run_id))

    def latest(self, run_id: str) -> dict[str, Any] | None:
        rows = self.list_checkpoints(run_id)
        return rows[-1] if rows else None

    def best(self, run_id: str) -> dict[str, Any] | None:
        rows = self.list_checkpoints(run_id)
        if not rows:
            return None
        return max(rows, key=lambda x: float(x.get("score", 0.0)))

    def validate_artifact(self, path: str | Path) -> bool:
        p = Path(path)
        return p.exists() and p.is_file() and p.stat().st_size > 0


checkpoint_service = CheckpointService()
