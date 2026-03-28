from __future__ import annotations

import argparse
import os
from pathlib import Path

from huggingface_hub import HfApi


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="deploy/huggingface")
    parser.add_argument("--repo", default=os.getenv("HF_SPACE_REPO_ID", ""))
    args = parser.parse_args()

    token = os.getenv("HF_TOKEN")
    if not token:
        raise SystemExit("HF_TOKEN not set.")
    if not args.repo:
        raise SystemExit("HF_SPACE_REPO_ID not set.")

    api = HfApi(token=token)
    api.create_repo(repo_id=args.repo, repo_type="space", private=False, exist_ok=True, space_sdk="docker")

    src = Path(args.source)
    for file in src.glob("*"):
        if file.is_file():
            api.upload_file(path_or_fileobj=str(file), path_in_repo=file.name, repo_id=args.repo, repo_type="space")
    print(f"Published space package from {src} to {args.repo}")


if __name__ == "__main__":
    main()
