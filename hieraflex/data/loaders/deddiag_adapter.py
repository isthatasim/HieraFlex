from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


DEFAULT_APPLIANCES = ["hvac", "washer", "dishwasher", "water_heater", "fridge"]


class DEDDIAGAdapter:
    """Loads DEDDIAG-like appliance traces from CSV/Parquet while preserving measured signals."""

    def __init__(self, root: str | Path = "data/raw/deddiag") -> None:
        self.root = Path(root)

    def list_files(self) -> list[Path]:
        if not self.root.exists():
            return []
        return sorted([*self.root.rglob("*.csv"), *self.root.rglob("*.parquet")])

    def load(self, houses: int = 4, steps: int = 288) -> pd.DataFrame:
        files = self.list_files()
        if files:
            frames: list[pd.DataFrame] = []
            for file in files:
                if file.suffix.lower() == ".csv":
                    df = pd.read_csv(file)
                else:
                    df = pd.read_parquet(file)
                frames.append(df)
            df_all = pd.concat(frames, ignore_index=True)
            return self._normalize(df_all)
        return self._build_synthetic_backbone(houses=houses, steps=steps)

    def detect_houses(self, df: pd.DataFrame) -> list[str]:
        return sorted(df["house_id"].astype(str).unique().tolist())

    def detect_appliances(self, df: pd.DataFrame, house_id: str) -> list[str]:
        view = df[df["house_id"].astype(str) == str(house_id)]
        return sorted(view["appliance_id"].astype(str).unique().tolist())

    def _normalize(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        rename_map = {
            "time": "timestamp",
            "datetime": "timestamp",
            "house": "house_id",
            "home_id": "house_id",
            "appliance": "appliance_id",
            "device": "appliance_id",
            "power": "power_kw",
            "power_w": "power_w",
        }
        out = out.rename(columns={k: v for k, v in rename_map.items() if k in out.columns})

        if "power_kw" not in out.columns and "power_w" in out.columns:
            out["power_kw"] = out["power_w"] / 1000.0
        if "timestamp" not in out.columns:
            out["timestamp"] = pd.RangeIndex(len(out)).astype(str)
        if "house_id" not in out.columns:
            out["house_id"] = "H1"
        if "appliance_id" not in out.columns:
            out["appliance_id"] = "unknown"
        out["power_kw"] = out.get("power_kw", 0.0).fillna(0.0).astype(float).clip(lower=0.0)
        out["state"] = np.where(out["power_kw"] > 0.02, "on", "off")
        out["source"] = "deddiag"
        return out[["timestamp", "house_id", "appliance_id", "power_kw", "state", "source"]]

    def _build_synthetic_backbone(self, houses: int, steps: int) -> pd.DataFrame:
        rng = np.random.default_rng(42)
        timestamps = pd.date_range("2025-01-01", periods=steps, freq="5min")
        rows: list[dict[str, object]] = []
        for h in range(1, houses + 1):
            for app in DEFAULT_APPLIANCES:
                base = 0.05 if app == "fridge" else 0.0
                profile = base + rng.uniform(0.0, 2.0, size=steps)
                active = rng.uniform(size=steps) > 0.6
                power = np.where(active, profile, base)
                for ts, p in zip(timestamps, power):
                    rows.append(
                        {
                            "timestamp": ts.isoformat(),
                            "house_id": f"H{h}",
                            "appliance_id": app,
                            "power_kw": float(max(0.0, p)),
                            "state": "on" if p > 0.05 else "off",
                            "source": "synthetic",
                        }
                    )
        return pd.DataFrame(rows)


def summarize_appliance_stats(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby(["house_id", "appliance_id"], as_index=False).agg(
        nominal_power_kw=("power_kw", "quantile"),
        avg_power_kw=("power_kw", "mean"),
        max_power_kw=("power_kw", "max"),
        active_ratio=("state", lambda x: float((x == "on").mean())),
    )
    grouped["nominal_power_kw"] = grouped["nominal_power_kw"].clip(lower=0.05)
    grouped["cycle_duration_steps"] = np.maximum((grouped["active_ratio"] * 8).round().astype(int), 1)
    grouped["interruptible"] = grouped["appliance_id"].isin(["hvac", "fridge"])
    grouped["flexibility_flag"] = ~grouped["appliance_id"].isin(["fridge"])
    return grouped
