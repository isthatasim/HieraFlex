from __future__ import annotations

from pathlib import Path

import pandas as pd


class LocalAdapter:
    """Loads preprocessed local scenario files when available."""

    def __init__(self, root: str | Path = "experiments/outputs/parquet") -> None:
        self.root = Path(root)

    def load_scenario(self, scenario_id: str) -> pd.DataFrame | None:
        parquet_path = self.root / f"{scenario_id}.parquet"
        csv_path = self.root / f"{scenario_id}.csv"
        if parquet_path.exists():
            return pd.read_parquet(parquet_path)
        if csv_path.exists():
            return pd.read_csv(csv_path)
        return None
