from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from rl.agents.ppo_agent import PPOAgent
from rl.envs.community_env import CommunityEnv


def run_shared_training(config_path: str) -> dict:
    cfg = yaml.safe_load(Path(config_path).read_text(encoding="utf-8"))
    houses = int(cfg.get("environment", {}).get("houses", 4))
    episodes = int(cfg.get("training", {}).get("episodes", 10))

    env = CommunityEnv(houses=houses)
    agent = PPOAgent()
    logs = []

    for ep in range(episodes):
        obs_map = env.reset()
        done = False
        ep_return = 0.0
        batch = []
        while not done:
            actions = {hid: agent.act(obs) for hid, obs in obs_map.items()}
            next_obs, rewards, done, info = env.step(actions)
            for hid, obs in obs_map.items():
                batch.append({"obs": obs, "action": actions[hid], "reward": rewards[hid], "info": info})
                ep_return += rewards[hid]
            obs_map = next_obs
        upd = agent.update(batch)
        logs.append({"episode": ep, "return": ep_return, **upd})

    model_path = Path("experiments/outputs/models/ppo_shared.pt")
    log_path = Path("experiments/outputs/logs/train_shared_ppo.json")
    agent.save(model_path)
    log_path.write_text(json.dumps(logs, indent=2), encoding="utf-8")
    return {"model_path": str(model_path), "log_path": str(log_path), "episodes": episodes}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="experiments/configs/community.yaml")
    args = parser.parse_args()
    print(json.dumps(run_shared_training(args.config), indent=2))
