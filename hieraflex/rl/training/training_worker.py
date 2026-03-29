from __future__ import annotations

import argparse
import json
import os
import random
import time
from pathlib import Path
from typing import Any

import numpy as np
import yaml

from rl.agents.ppo_agent import PPOAgent
from rl.envs.community_env import CommunityEnv
from rl.envs.single_house_env import SingleHouseEnv, SingleHouseEnvConfig


def utc_now() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)


def rollout_single(agent: PPOAgent, env: SingleHouseEnv) -> tuple[list[dict], dict[str, float]]:
    obs = env.reset()
    done = False
    batch: list[dict] = []
    total_reward = 0.0
    total_energy_cost = 0.0
    peak_proxy = 0.0
    comfort_penalty = 0.0
    while not done:
        action = agent.act(obs)
        next_obs, reward, done, info = env.step(action)
        batch.append({"obs": obs, "action": action, "reward": reward, "info": info})
        obs = next_obs
        total_reward += float(reward)
        total_energy_cost += float(info.get("energy_cost", 0.0))
        peak_proxy = max(peak_proxy, float(info.get("peak_cost", 0.0)))
        comfort_penalty += float(info.get("comfort_pen", 0.0))

    metrics = {
        "episode_return": total_reward,
        "episode_energy_cost": total_energy_cost,
        "episode_peak_proxy": peak_proxy,
        "episode_comfort_penalty": comfort_penalty,
        "steps": len(batch),
    }
    return batch, metrics


def rollout_shared(agent: PPOAgent, env: CommunityEnv) -> tuple[list[dict], dict[str, float]]:
    obs_map = env.reset()
    done = False
    batch: list[dict] = []
    total_return = 0.0
    fairness_penalty = 0.0
    steps = 0

    while not done:
        actions = {hid: agent.act(obs) for hid, obs in obs_map.items()}
        next_obs, rewards, done, info = env.step(actions)
        for hid, obs in obs_map.items():
            batch.append({"obs": obs, "action": actions[hid], "reward": rewards[hid], "info": info})
            total_return += float(rewards[hid])
        obs_map = next_obs
        fairness_penalty += float(info.get("fairness_var", 0.0))
        steps += 1

    metrics = {
        "episode_return": total_return,
        "episode_energy_cost": max(0.0, -total_return),
        "episode_peak_proxy": 0.0,
        "episode_comfort_penalty": 0.0,
        "episode_fairness_penalty": fairness_penalty / max(1, steps),
        "steps": steps,
    }
    return batch, metrics


def evaluate(agent: PPOAgent, algorithm: str) -> dict[str, float]:
    if algorithm == "ppo_shared":
        env = CommunityEnv(houses=4)
        _, metrics = rollout_shared(agent, env)
    else:
        env = SingleHouseEnv(SingleHouseEnvConfig(horizon=288, seed=1234))
        _, metrics = rollout_single(agent, env)
    return {"eval_return": float(metrics["episode_return"]), "eval_energy_cost": float(metrics["episode_energy_cost"])}


def run(args: argparse.Namespace) -> int:
    project_root = Path(__file__).resolve().parents[2]
    run_dir = project_root / "experiments" / "outputs" / "json" / "runs" / args.run_id
    run_file = run_dir / "run.json"
    metrics_file = run_dir / "metrics.jsonl"
    checkpoints_file = run_dir / "checkpoints.jsonl"
    evaluations_file = run_dir / "evaluations.jsonl"
    stop_file = run_dir / "STOP"
    ckpt_dir = run_dir / "checkpoints"
    ckpt_dir.mkdir(parents=True, exist_ok=True)

    run_meta = read_json(run_file)
    if not run_meta:
        run_meta = {
            "run_id": args.run_id,
            "algorithm": args.algorithm,
            "config_path": args.config,
            "scenario_id": args.scenario,
            "status": "running",
            "episodes_target": args.episodes,
            "current_episode": 0,
            "current_step": 0,
            "seed": args.seed,
            "started_at": utc_now(),
            "updated_at": utc_now(),
        }

    config = {}
    cfg_path = project_root / args.config
    if cfg_path.exists():
        config = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}

    set_seed(args.seed)
    resume_ckpt = args.resume_from or run_meta.get("latest_checkpoint")
    agent = PPOAgent.load(resume_ckpt) if resume_ckpt else PPOAgent()

    start_episode = int(run_meta.get("current_episode", 0)) + 1
    end_episode = start_episode + args.episodes - 1

    best_score = float(run_meta.get("best_score", -1e9))

    for episode in range(start_episode, end_episode + 1):
        if stop_file.exists():
            run_meta.update({"status": "stopped", "ended_at": utc_now(), "updated_at": utc_now()})
            write_json(run_file, run_meta)
            return 0

        if args.algorithm == "ppo_shared":
            batch, episode_metrics = rollout_shared(agent, CommunityEnv(houses=int(config.get("environment", {}).get("houses", 4))))
        else:
            horizon = int(config.get("environment", {}).get("horizon", 288))
            batch, episode_metrics = rollout_single(agent, SingleHouseEnv(SingleHouseEnvConfig(horizon=horizon, seed=args.seed + episode)))

        update = agent.update(batch)

        metric_row = {
            "timestamp": utc_now(),
            "run_id": args.run_id,
            "episode": episode,
            "episode_return": float(episode_metrics.get("episode_return", 0.0)),
            "energy_cost": float(episode_metrics.get("episode_energy_cost", 0.0)),
            "peak_proxy": float(episode_metrics.get("episode_peak_proxy", 0.0)),
            "comfort_penalty": float(episode_metrics.get("episode_comfort_penalty", 0.0)),
            "fairness_penalty": float(episode_metrics.get("episode_fairness_penalty", 0.0)),
            "loss": float(update.get("loss", 0.0)),
            "steps": int(episode_metrics.get("steps", len(batch))),
        }
        append_jsonl(metrics_file, metric_row)

        run_meta["current_episode"] = episode
        run_meta["current_step"] = int(run_meta.get("current_step", 0)) + int(metric_row["steps"])
        run_meta["status"] = "running"
        run_meta["updated_at"] = utc_now()

        if episode % max(1, args.checkpoint_interval) == 0 or episode == end_episode:
            ckpt_path = ckpt_dir / f"checkpoint_ep_{episode:05d}.pt"
            agent.save(ckpt_path)
            is_best = metric_row["episode_return"] >= best_score
            if is_best:
                best_score = metric_row["episode_return"]
                run_meta["best_checkpoint"] = str(ckpt_path)
                run_meta["best_score"] = float(best_score)
            run_meta["latest_checkpoint"] = str(ckpt_path)
            append_jsonl(
                checkpoints_file,
                {
                    "timestamp": utc_now(),
                    "run_id": args.run_id,
                    "episode": episode,
                    "checkpoint_path": str(ckpt_path),
                    "score": float(metric_row["episode_return"]),
                    "is_best": bool(is_best),
                },
            )

        if episode % max(1, args.eval_interval) == 0:
            eval_row = {"timestamp": utc_now(), "run_id": args.run_id, "episode": episode, **evaluate(agent, args.algorithm)}
            append_jsonl(evaluations_file, eval_row)

        write_json(run_file, run_meta)
        time.sleep(0.05)

    run_meta.update({"status": "completed", "ended_at": utc_now(), "updated_at": utc_now()})
    write_json(run_file, run_meta)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--algorithm", default="ppo_single")
    parser.add_argument("--config", default="experiments/configs/single_house.yaml")
    parser.add_argument("--scenario", default="demo_week")
    parser.add_argument("--episodes", type=int, default=100)
    parser.add_argument("--checkpoint-interval", type=int, default=5)
    parser.add_argument("--eval-interval", type=int, default=10)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--resume-from", default="")
    return parser.parse_args()


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
