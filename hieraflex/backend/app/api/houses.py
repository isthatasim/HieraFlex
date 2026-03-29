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


@router.get("/{house_id}/resources")
def get_house_resources(house_id: str, limit: int = 288) -> dict:
    bundle = dataset_service.load_bundle()
    trace = bundle.trace[bundle.trace["house_id"].astype(str) == str(house_id)].copy()
    if trace.empty:
        return {"house_id": house_id, "timeline": [], "appliances": []}

    timeline = (
        trace.groupby("timestamp", as_index=False)["power_kw"]
        .sum()
        .rename(columns={"power_kw": "house_total_kw"})
        .sort_values("timestamp")
    )
    prices = bundle.prices.rename(columns={"grid_buy_price": "price"})[["timestamp", "price"]]
    timeline = timeline.merge(prices, on="timestamp", how="left").tail(max(1, min(limit, 2000)))

    appliance_rows = []
    for appliance_id, group in trace.groupby("appliance_id"):
        rows = (
            group.sort_values("timestamp")[["timestamp", "power_kw", "state"]]
            .tail(max(1, min(limit, 2000)))
            .to_dict(orient="records")
        )
        appliance_rows.append(
            {
                "appliance_id": appliance_id,
                "nominal_kw": float(group["power_kw"].quantile(0.9)),
                "series": rows,
            }
        )

    return {
        "house_id": house_id,
        "timeline": timeline.to_dict(orient="records"),
        "appliances": sorted(appliance_rows, key=lambda x: x["appliance_id"]),
    }
