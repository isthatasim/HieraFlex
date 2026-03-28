from __future__ import annotations

import pandas as pd


def align_timeseries(df: pd.DataFrame, freq: str = "5min") -> pd.DataFrame:
    out = df.copy()
    out["timestamp"] = pd.to_datetime(out["timestamp"], errors="coerce")
    out = out.dropna(subset=["timestamp"]).copy()
    out["timestamp"] = out["timestamp"].dt.floor(freq)
    grouped = (
        out.groupby(["timestamp", "house_id", "appliance_id"], as_index=False)["power_kw"]
        .mean()
        .sort_values(["timestamp", "house_id", "appliance_id"])
    )
    grouped["state"] = grouped["power_kw"].gt(0.02).map({True: "on", False: "off"})
    grouped["source"] = out.get("source", "deddiag")
    grouped["timestamp"] = grouped["timestamp"].dt.tz_localize(None).dt.strftime("%Y-%m-%dT%H:%M:%S")
    return grouped
