from __future__ import annotations

import os
from dataclasses import dataclass

import pandas as pd


@dataclass(slots=True)
class HFStreamAdapter:
    dataset_repo_id: str | None = None
    token: str | None = None

    @classmethod
    def from_env(cls) -> "HFStreamAdapter":
        return cls(
            dataset_repo_id=os.getenv("HF_DATASET_REPO_ID"),
            token=os.getenv("HF_TOKEN"),
        )

    def available(self) -> bool:
        return bool(self.dataset_repo_id and self.token)

    def stream(self, split: str = "train") -> pd.DataFrame:
        if not self.available():
            raise RuntimeError("HF streaming unavailable: missing HF_TOKEN or HF_DATASET_REPO_ID")
        # Placeholder for datasets.load_dataset streaming path to preserve offline compatibility.
        return pd.DataFrame()
