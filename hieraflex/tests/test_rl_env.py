from __future__ import annotations

from rl.agents.rule_based_agent import RuleBasedAgent
from rl.envs.single_house_env import SingleHouseEnv


def test_rl_env_rollout() -> None:
    env = SingleHouseEnv()
    agent = RuleBasedAgent()
    obs = env.reset()
    done = False
    total = 0.0
    while not done:
        action = agent.act(obs)
        obs, reward, done, _ = env.step(action)
        total += reward
    assert total != 0.0
