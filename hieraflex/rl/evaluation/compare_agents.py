from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
import yaml

from rl.agents.cheapest_slot_agent import CheapestSlotAgent
from rl.agents.fixed_schedule_agent import FixedScheduleAgent
from rl.agents.ppo_agent import PPOAgent
from rl.agents.rule_based_agent import RuleBasedAgent
from rl.envs.single_house_env import SingleHouseEnv


def rollout(agent, episodes: int = 5) -> dict:
    env = SingleHouseEnv()
    totals = []
    peak_list = []
    for _ in range(episodes):
        obs = env.reset()
        done = False
        ep_reward = 0.0
        loads = []
        costs = []
        while not done:
            action = agent.act(obs)
            obs, reward, done, info = env.step(action)
            ep_reward += reward
            loads.append(info["energy_cost"])
            costs.append(info["energy_cost"])
        totals.append(ep_reward)
        peak = max(loads) if loads else 0.0
        mean = sum(loads) / len(loads) if loads else 1.0
        peak_list.append(peak / mean if mean > 0 else 0.0)
    return {
        "avg_return": float(sum(totals) / len(totals)),
        "par": float(sum(peak_list) / len(peak_list)),
        "cost_proxy": float(-sum(totals) / len(totals)),
    }


def compare(config_path: str) -> dict:
    _ = yaml.safe_load(Path(config_path).read_text(encoding="utf-8"))
    baseline = FixedScheduleAgent()
    rule = RuleBasedAgent()
    cheapest = CheapestSlotAgent()
    ppo = PPOAgent.load("experiments/outputs/models/ppo_single_house.pt")

    rows = []
    for name, agent in [
        ("no_control", baseline),
        ("rule_based", rule),
        ("cheapest_slot", cheapest),
        ("ppo", ppo),
    ]:
        metrics = rollout(agent)
        rows.append({"agent": name, **metrics})

    df = pd.DataFrame(rows)
    out_csv = Path("experiments/outputs/csv/evaluation_comparison.csv")
    out_json = Path("experiments/outputs/logs/evaluation_comparison.json")
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)
    out_json.write_text(df.to_json(orient="records", indent=2), encoding="utf-8")

    return {
        "rows": rows,
        "csv": str(out_csv),
        "json": str(out_json),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="experiments/configs/community.yaml")
    args = parser.parse_args()
    print(json.dumps(compare(args.config), indent=2))
