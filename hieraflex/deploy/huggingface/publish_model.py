from __future__ import annotations

import argparse
import os
from pathlib import Path

from huggingface_hub import HfApi


CARD = """---
library_name: pytorch
license: mit
---

# HieraFlex PPO Policy

Checkpoint and metadata for HieraFlex price-responsive house-agent policy.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="experiments/outputs/models")
    parser.add_argument("--repo", default=os.getenv("HF_MODEL_REPO_ID", ""))
    args = parser.parse_args()

    token = os.getenv("HF_TOKEN")
    if not token:
        raise SystemExit("HF_TOKEN not set.")
    if not args.repo:
        raise SystemExit("HF_MODEL_REPO_ID not set.")

    source = Path(args.source)
    api = HfApi(token=token)
    api.create_repo(repo_id=args.repo, repo_type="model", private=False, exist_ok=True)
    for file in source.glob("*"):
        if file.is_file():
            api.upload_file(path_or_fileobj=str(file), path_in_repo=file.name, repo_id=args.repo, repo_type="model")
    readme_path = source / "README.model.md"
    readme_path.write_text(CARD, encoding="utf-8")
    api.upload_file(path_or_fileobj=str(readme_path), path_in_repo="README.md", repo_id=args.repo, repo_type="model")
    print(f"Published model artifacts from {source} to {args.repo}")


if __name__ == "__main__":
    main()
