from __future__ import annotations

import numpy as np
import pandas as pd


def build_price_series(timestamps: list[str], seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    ts = pd.to_datetime(pd.Series(timestamps)).drop_duplicates().sort_values().reset_index(drop=True)
    hour = ts.dt.hour
    base = np.where((hour >= 17) & (hour <= 21), 0.38, 0.19)
    shoulder = np.where((hour >= 6) & (hour < 10), 0.26, 0.0)
    noise = rng.normal(0.0, 0.02, len(ts))
    buy = np.clip(base + shoulder + noise, 0.08, 0.55)
    sell = np.clip(buy * 0.55, 0.03, 0.35)
    incentive = np.where((hour >= 18) & (hour <= 21), 0.04, 0.0)
    return pd.DataFrame(
        {
            "timestamp": ts.dt.strftime("%Y-%m-%dT%H:%M:%S"),
            "grid_buy_price": buy,
            "grid_sell_price": sell,
            "incentive_price": incentive,
        }
    )
