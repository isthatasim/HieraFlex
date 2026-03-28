from __future__ import annotations

import pandas as pd


class TariffEngine:
    def __init__(self, mode: str = "real_time") -> None:
        self.mode = mode

    def price(self, buy_price: float, sell_price: float, incentive: float = 0.0) -> dict[str, float]:
        if self.mode == "fixed":
            return {"grid_buy": 0.22, "grid_sell": 0.10, "incentive": 0.0, "mode": "fixed"}
        if self.mode == "hybrid":
            return {
                "grid_buy": float(0.6 * buy_price + 0.4 * 0.22),
                "grid_sell": float(0.6 * sell_price + 0.4 * 0.10),
                "incentive": float(incentive),
                "mode": "hybrid",
            }
        return {
            "grid_buy": float(buy_price),
            "grid_sell": float(sell_price),
            "incentive": float(incentive),
            "mode": "real_time",
        }

    def inject(self, frame: pd.DataFrame, price_frame: pd.DataFrame) -> pd.DataFrame:
        merged = frame.merge(price_frame, on="timestamp", how="left")
        merged[["grid_buy_price", "grid_sell_price", "incentive_price"]] = merged[
            ["grid_buy_price", "grid_sell_price", "incentive_price"]
        ].fillna(method="ffill")
        return merged
