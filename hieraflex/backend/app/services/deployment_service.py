from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class DeploymentService:
    def status(self) -> dict:
        keys = [
            "HF_TOKEN",
            "HF_DATASET_REPO_ID",
            "HF_MODEL_REPO_ID",
            "HF_SPACE_REPO_ID",
            "HF_USERNAME",
        ]
        flags = {k: bool(os.getenv(k)) for k in keys}
        ready = all(flags.values())
        return {
            "huggingface_ready": ready,
            "variables_present": flags,
            "message": "Ready for Hugging Face publishing" if ready else "Missing Hugging Face environment variables",
        }


deployment_service = DeploymentService()
