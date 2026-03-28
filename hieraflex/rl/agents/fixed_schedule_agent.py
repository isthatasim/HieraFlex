from __future__ import annotations

import numpy as np


class FixedScheduleAgent:
    def __init__(self, schedule: list[int] | None = None) -> None:
        self.schedule = schedule or [2] * 288
        self.t = 0

    def act(self, obs: np.ndarray) -> int:
        action = self.schedule[min(self.t, len(self.schedule) - 1)]
        self.t += 1
        return int(action)
