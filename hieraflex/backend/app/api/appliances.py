from __future__ import annotations

from fastapi import APIRouter

from backend.app.services.dataset_service import dataset_service

router = APIRouter(prefix="/appliances", tags=["appliances"])


@router.get("")
def list_appliances(house_id: str | None = None) -> list[dict]:
    bundle = dataset_service.load_bundle()
    meta = bundle.appliance_meta.copy()
    if house_id:
        meta = meta[meta["house_id"].astype(str) == str(house_id)]
    return meta.to_dict(orient="records")
