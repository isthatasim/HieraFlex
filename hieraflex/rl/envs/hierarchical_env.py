from __future__ import annotations

from rl.envs.community_env import CommunityEnv


class HierarchicalEnv:
    def __init__(self, houses: int = 4, horizon: int = 288) -> None:
        self.community = CommunityEnv(houses=houses, horizon=horizon)

    def reset(self) -> dict:
        return self.community.reset()

    def step(self, actions: dict[str, int]) -> tuple[dict, dict, bool, dict]:
        return self.community.step(actions)
