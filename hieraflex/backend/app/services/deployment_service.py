from __future__ import annotations

from backend.app.services.deployment_status_service import DeploymentStatusService


class DeploymentService(DeploymentStatusService):
    pass


deployment_service = DeploymentService()
