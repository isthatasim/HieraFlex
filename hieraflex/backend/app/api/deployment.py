from __future__ import annotations

from fastapi import APIRouter

from backend.app.services.deployment_status_service import deployment_status_service

router = APIRouter(prefix="/deployment", tags=["deployment"])


@router.get("/status")
def deployment_status() -> dict:
    return deployment_status_service.status()
