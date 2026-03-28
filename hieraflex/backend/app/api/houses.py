from __future__ import annotations

from fastapi import APIRouter

from backend.app.services.dataset_service import dataset_service
from backend.app.services.policy_service import policy_service
from backend.app.services.simulation_runtime import simulation_runtime

router = APIRouter(prefix="/houses", tags=["houses"])


@router.get("")
def list_houses() -> list[dict]:
    bundle = dataset_service.load_bundle()
    houses = sorted(bundle.trace["house_id"].astype(str).unique().tolist())
    return [{"house_id": hid} for hid in houses]


@router.get("/{house_id}")
def get_house(house_id: str) -> dict:
    bundle = dataset_service.load_bundle()
    view = bundle.trace[bundle.trace["house_id"].astype(str) == str(house_id)]
    return {
        "house_id": house_id,
        "rows": int(len(view)),
        "appliances": sorted(view["appliance_id"].astype(str).unique().tolist()),
    }


@router.get("/{house_id}/agent-state")
def get_house_agent_state(house_id: str) -> dict:
    if house_id in policy_service.house_agents:
        agent = policy_service.house_agents[house_id]
        return {
            "house_id": house_id,
            "latest_action": agent.memory.actions[-1] if agent.memory.actions else "none",
            "price_trend": agent.memory.price_trend(),
            "last_reward": agent.memory.rewards[-1] if agent.memory.rewards else 0.0,
        }
    recent = [e for e in simulation_runtime.latest_events if any(h["house_id"] == house_id for h in e.get("houses", []))]
    if not recent:
        return {"house_id": house_id, "latest_action": "none", "price_trend": 0.0, "last_reward": 0.0}
    house = [h for h in recent[-1]["houses"] if h["house_id"] == house_id][0]
    return house.get("decision", {})
