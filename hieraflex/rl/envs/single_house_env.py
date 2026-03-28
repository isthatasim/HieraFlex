from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class SingleHouseEnvConfig:
    horizon: int = 288
    seed: int = 42


class SingleHouseEnv:
    """Price-responsive single-house environment for quick PPO/rule baseline evaluation."""

    ACTIONS = ["start", "defer", "keep", "charge", "discharge", "bid", "offer", "noop"]

    def __init__(self, config: SingleHouseEnvConfig | None = None) -> None:
        self.config = config or SingleHouseEnvConfig()
        self.rng = np.random.default_rng(self.config.seed)
        self.t = 0
        self.price = None
        self.load = None
        self.flex = None
        self.deadline = None

    def reset(self) -> np.ndarray:
        self.t = 0
        self.price = np.clip(self.rng.normal(0.22, 0.06, size=self.config.horizon), 0.08, 0.55)
        self.load = np.clip(self.rng.normal(2.5, 0.9, size=self.config.horizon), 0.4, 7.5)
        self.flex = np.clip(self.rng.normal(0.4, 0.15, size=self.config.horizon), 0.05, 0.95)
        self.deadline = np.linspace(1.0, 0.0, self.config.horizon)
        return self._obs()

    def _obs(self) -> np.ndarray:
        return np.array(
            [
                self.t / max(1, self.config.horizon - 1),
                float(self.price[self.t]),
                float(self.load[self.t]),
                float(self.flex[self.t]),
                float(self.deadline[self.t]),
            ],
            dtype=np.float32,
        )

    def step(self, action_idx: int) -> tuple[np.ndarray, float, bool, dict]:
        action = self.ACTIONS[int(action_idx)]
        p = float(self.price[self.t])
        l = float(self.load[self.t])
        f = float(self.flex[self.t])
        d = float(self.deadline[self.t])

        energy_cost = p * l
        peak_cost = max(0.0, l - 4.5)
        comfort_pen = max(0.0, 0.5 - d) if action == "defer" else 0.0
        switch_pen = 0.05 if action in {"start", "defer"} else 0.0
        trade_rev = 0.08 * f if action == "offer" else 0.0
        flex_reward = 0.05 * f if action in {"defer", "offer", "bid"} else 0.0
        resp_reward = 0.06 if (p > 0.3 and action == "defer") or (p < 0.15 and action == "start") else 0.0

        reward = (
            -1.0 * energy_cost
            - 0.4 * peak_cost
            - 0.5 * comfort_pen
            - 0.2 * switch_pen
            + 0.5 * trade_rev
            + flex_reward
            + resp_reward
        )

        info = {
            "energy_cost": energy_cost,
            "peak_cost": peak_cost,
            "comfort_pen": comfort_pen,
            "switch_pen": switch_pen,
            "trade_rev": trade_rev,
            "flex_reward": flex_reward,
            "resp_reward": resp_reward,
            "action": action,
        }

        self.t += 1
        done = self.t >= self.config.horizon
        obs = self._obs() if not done else np.zeros(5, dtype=np.float32)
        return obs, float(reward), done, info
