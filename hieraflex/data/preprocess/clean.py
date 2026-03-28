from __future__ import annotations

import pandas as pd


def clean_trace(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out = out.dropna(subset=["timestamp", "house_id", "appliance_id"]).reset_index(drop=True)
    out["power_kw"] = out["power_kw"].fillna(0.0).clip(lower=0.0)
    out = out.sort_values(["timestamp", "house_id", "appliance_id"]).reset_index(drop=True)
    return out
