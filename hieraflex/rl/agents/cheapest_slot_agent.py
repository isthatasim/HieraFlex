from __future__ import annotations

import numpy as np


class CheapestSlotAgent:
    """Heuristic baseline: pick start when current price in lower quantile of recent horizon."""

    def __init__(self, window: int = 24, quantile: float = 0.35) -> None:
        self.window = window
        self.quantile = quantile
        self.prices: list[float] = []

    def act(self, obs: np.ndarray) -> int:
        price = float(obs[1])
        slack = float(obs[4])
        self.prices.append(price)
        recent = self.prices[-self.window :]
        threshold = float(np.quantile(recent, self.quantile))
        if price <= threshold:
            return 0
        if slack > 0.2:
            return 1
        return 2
