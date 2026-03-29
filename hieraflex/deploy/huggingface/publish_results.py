from __future__ import annotations

import argparse
import os
from pathlib import Path

from huggingface_hub import HfApi


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="experiments/outputs/json")
    parser.add_argument("--repo", default=os.getenv("HF_DATASET_REPO_ID", ""))
    args = parser.parse_args()

    token = os.getenv("HF_TOKEN")
    if not token:
        raise SystemExit("HF_TOKEN not set.")
    if not args.repo:
        raise SystemExit("HF_DATASET_REPO_ID not set.")

    api = HfApi(token=token)
    api.create_repo(repo_id=args.repo, repo_type="dataset", private=False, exist_ok=True)
    src = Path(args.source)
    for file in src.rglob("*.json"):
        rel = file.relative_to(src).as_posix()
        api.upload_file(path_or_fileobj=str(file), path_in_repo=f"results/{rel}", repo_id=args.repo, repo_type="dataset")
    for file in src.rglob("*.jsonl"):
        rel = file.relative_to(src).as_posix()
        api.upload_file(path_or_fileobj=str(file), path_in_repo=f"results/{rel}", repo_id=args.repo, repo_type="dataset")
    print(f"Published result artifacts from {src} to {args.repo}")


if __name__ == "__main__":
    main()
