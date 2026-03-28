from __future__ import annotations

import numpy as np


class RuleBasedAgent:
    """Price threshold policy for responsive load shifting baseline."""

    def __init__(self, high: float = 0.3, low: float = 0.14) -> None:
        self.high = high
        self.low = low

    def act(self, obs: np.ndarray) -> int:
        price = float(obs[1])
        slack = float(obs[4])
        if price > self.high and slack > 0.25:
            return 1  # defer
        if price < self.low:
            return 0  # start
        return 2  # keep
