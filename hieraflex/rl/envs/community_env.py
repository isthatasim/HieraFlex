from __future__ import annotations

import numpy as np

from rl.envs.single_house_env import SingleHouseEnv


class CommunityEnv:
    def __init__(self, houses: int = 4, horizon: int = 288) -> None:
        self.house_envs = [SingleHouseEnv() for _ in range(houses)]
        self.horizon = horizon
        self.t = 0

    def reset(self) -> dict[str, np.ndarray]:
        self.t = 0
        return {f"H{i+1}": env.reset() for i, env in enumerate(self.house_envs)}

    def step(self, actions: dict[str, int]) -> tuple[dict[str, np.ndarray], dict[str, float], bool, dict]:
        obs, rewards = {}, {}
        costs = []
        done = False
        for i, env in enumerate(self.house_envs):
            hid = f"H{i+1}"
            o, r, d, info = env.step(actions.get(hid, 2))
            obs[hid] = o
            rewards[hid] = r
            costs.append(info["energy_cost"])
            done = done or d
        fairness = float(np.var(costs)) if costs else 0.0
        for hid in rewards:
            rewards[hid] -= 0.1 * fairness
        self.t += 1
        return obs, rewards, done, {"fairness_var": fairness}
