from __future__ import annotations

import numpy as np
import pandas as pd


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    ts = pd.to_datetime(out["timestamp"])
    out["hour"] = ts.dt.hour
    out["dow"] = ts.dt.dayofweek
    out["is_peak_hour"] = out["hour"].isin([7, 8, 9, 18, 19, 20]).astype(int)
    out["rolling_power_kw"] = out.groupby(["house_id", "appliance_id"]) ["power_kw"].transform(
        lambda s: s.rolling(6, min_periods=1).mean()
    )
    out["flexibility_slack"] = np.maximum(0.0, 1.0 - out["rolling_power_kw"] / (out["power_kw"].max() + 1e-6))
    return out
