from __future__ import annotations

from fastapi import APIRouter

from backend.app.services.market_service import market_service

router = APIRouter(prefix="/market", tags=["market"])


@router.get("/state")
def market_state() -> dict:
    return market_service.latest_state
