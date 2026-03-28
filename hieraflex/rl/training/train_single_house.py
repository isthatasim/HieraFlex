from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from rl.agents.ppo_agent import PPOAgent
from rl.envs.single_house_env import SingleHouseEnv, SingleHouseEnvConfig


def run_training(config_path: str) -> dict:
    config = yaml.safe_load(Path(config_path).read_text(encoding="utf-8"))
    episodes = int(config.get("training", {}).get("episodes", 20))
    horizon = int(config.get("environment", {}).get("horizon", 288))

    env = SingleHouseEnv(SingleHouseEnvConfig(horizon=horizon))
    agent = PPOAgent()

    logs: list[dict] = []
    for ep in range(episodes):
        obs = env.reset()
        done = False
        ep_return = 0.0
        batch = []
        while not done:
            action = agent.act(obs)
            next_obs, reward, done, info = env.step(action)
            batch.append({"obs": obs, "action": action, "reward": reward, "info": info})
            ep_return += reward
            obs = next_obs
        update = agent.update(batch)
        logs.append({"episode": ep, "return": ep_return, **update})

    out_model = Path("experiments/outputs/models/ppo_single_house.pt")
    out_log = Path("experiments/outputs/logs/train_single_house.json")
    agent.save(out_model)
    out_log.parent.mkdir(parents=True, exist_ok=True)
    out_log.write_text(json.dumps(logs, indent=2), encoding="utf-8")
    return {"model_path": str(out_model), "log_path": str(out_log), "episodes": episodes}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="experiments/configs/single_house.yaml")
    args = parser.parse_args()
    result = run_training(args.config)
    print(json.dumps(result, indent=2))
