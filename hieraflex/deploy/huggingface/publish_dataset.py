from __future__ import annotations

import argparse
import os
from pathlib import Path

from huggingface_hub import HfApi


CARD = """---
pretty_name: HieraFlex Replay Scenarios
license: mit
language: en
---

# HieraFlex Dataset

Replay-ready scenario shards for Hierarchical Flexibility Intelligence for Community Energy Trading.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="experiments/outputs/parquet")
    parser.add_argument("--repo", default=os.getenv("HF_DATASET_REPO_ID", ""))
    args = parser.parse_args()
    if not args.repo:
        raise SystemExit("HF_DATASET_REPO_ID not set. Export token and repo id before publishing.")

    token = os.getenv("HF_TOKEN")
    if not token:
        raise SystemExit("HF_TOKEN not set. Publishing aborted.")

    source = Path(args.source)
    api = HfApi(token=token)
    api.create_repo(repo_id=args.repo, repo_type="dataset", private=False, exist_ok=True)
    for file in source.glob("*.parquet"):
        api.upload_file(path_or_fileobj=str(file), path_in_repo=f"data/{file.name}", repo_id=args.repo, repo_type="dataset")
    readme_path = source / "README.dataset.md"
    readme_path.write_text(CARD, encoding="utf-8")
    api.upload_file(path_or_fileobj=str(readme_path), path_in_repo="README.md", repo_id=args.repo, repo_type="dataset")
    print(f"Published dataset files from {source} to {args.repo}")


if __name__ == "__main__":
    main()
