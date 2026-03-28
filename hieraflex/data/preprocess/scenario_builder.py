from __future__ import annotations

import pandas as pd


def build_scenario_window(df: pd.DataFrame, start_index: int, end_index: int) -> pd.DataFrame:
    ts = sorted(df["timestamp"].unique())
    if not ts:
        return df.head(0).copy()
    start = max(0, start_index)
    end = min(len(ts), max(start + 1, end_index))
    selected = set(ts[start:end])
    return df[df["timestamp"].isin(selected)].reset_index(drop=True)
