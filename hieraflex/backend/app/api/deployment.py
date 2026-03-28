from __future__ import annotations

from fastapi import APIRouter

from backend.app.services.deployment_service import deployment_service

router = APIRouter(prefix="/deployment", tags=["deployment"])


@router.get("/status")
def deployment_status() -> dict:
    return deployment_service.status()
