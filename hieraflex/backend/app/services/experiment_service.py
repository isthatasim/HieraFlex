from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


class ExperimentService:
    def export_summary(self, summary: dict, root: str = "experiments/outputs") -> dict:
        out = Path(root)
        out.mkdir(parents=True, exist_ok=True)
        csv_dir = out / "csv"
        parquet_dir = out / "parquet"
        csv_dir.mkdir(parents=True, exist_ok=True)
        parquet_dir.mkdir(parents=True, exist_ok=True)

        frame = pd.DataFrame(summary.get("per_house", []))
        csv_path = csv_dir / "results_summary.csv"
        pq_path = parquet_dir / "results_summary.parquet"
        json_path = out / "summary.json"

        frame.to_csv(csv_path, index=False)
        frame.to_parquet(pq_path, index=False)
        json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        return {"csv": str(csv_path), "parquet": str(pq_path), "json": str(json_path)}


experiment_service = ExperimentService()
