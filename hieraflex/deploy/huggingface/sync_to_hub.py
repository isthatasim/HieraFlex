from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-dir", default="experiments/outputs/parquet")
    parser.add_argument("--model-dir", default="experiments/outputs/models")
    parser.add_argument("--space-dir", default="deploy/huggingface")
    args = parser.parse_args()

    token = require_env("HF_TOKEN")
    dataset_repo = require_env("HF_DATASET_REPO_ID")
    model_repo = require_env("HF_MODEL_REPO_ID")
    space_repo = require_env("HF_SPACE_REPO_ID")

    run(["hf", "auth", "login", "--token", token])
    run(["python", "deploy/huggingface/publish_dataset.py", "--source", args.dataset_dir, "--repo", dataset_repo])
    run(["python", "deploy/huggingface/publish_model.py", "--source", args.model_dir, "--repo", model_repo])
    run(["python", "deploy/huggingface/publish_space.py", "--source", args.space_dir, "--repo", space_repo])


if __name__ == "__main__":
    main()
