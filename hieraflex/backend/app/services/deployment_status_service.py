from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from backend.app.services.io_utils import project_root


@dataclass
class DeploymentStatusService:
    def status(self) -> dict:
        keys = [
            "HF_TOKEN",
            "HF_DATASET_REPO_ID",
            "HF_MODEL_REPO_ID",
            "HF_SPACE_REPO_ID",
            "HF_USERNAME",
        ]
        flags = {k: bool(os.getenv(k)) for k in keys}
        hf_ready = all(flags.values())
        root = project_root()
        mode = os.getenv("HIERAFLEX_MODE", "local-dev")
        frontend_dist = (root / "frontend" / "dist").exists()
        serve_frontend = os.getenv("HIERAFLEX_SERVE_FRONTEND", "0") == "1"
        worker_available = True

        return {
            "mode": mode,
            "frontend_dist_available": frontend_dist,
            "serve_frontend": serve_frontend,
            "worker_available": worker_available,
            "huggingface_ready": hf_ready,
            "variables_present": flags,
            "message": "Deployment stack healthy" if worker_available else "Training worker unavailable",
        }


deployment_status_service = DeploymentStatusService()
