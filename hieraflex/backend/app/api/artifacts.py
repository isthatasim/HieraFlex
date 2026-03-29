from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter

from backend.app.services.io_utils import project_root

router = APIRouter(prefix="/artifacts", tags=["artifacts"])


def _list_files(path: Path, patterns: list[str]) -> list[dict]:
    rows: list[dict] = []
    for pattern in patterns:
        for p in sorted(path.glob(pattern)):
            if p.is_file():
                rows.append({"name": p.name, "path": str(p), "size_bytes": p.stat().st_size})
    rows.sort(key=lambda x: x["name"])
    return rows


@router.get("/models")
def list_models() -> dict:
    root = project_root() / "experiments" / "outputs" / "models"
    root.mkdir(parents=True, exist_ok=True)
    return {"models": _list_files(root, ["*.pt", "*.pth", "*.json"]) }


@router.get("/results")
def list_results() -> dict:
    base = project_root() / "experiments" / "outputs"
    return {
        "csv": _list_files(base / "csv", ["*.csv"]),
        "parquet": _list_files(base / "parquet", ["*.parquet"]),
        "figures": _list_files(base / "figures", ["*.png", "*.jpg", "*.svg"]),
        "json": _list_files(base / "json", ["*.json", "*.jsonl"]),
    }
