from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field

from backend.app.services.agent_service import agent_service
from backend.app.services.market_service import market_service
from backend.app.services.policy_service import policy_service
from backend.app.services.replay_service import replay_service
from backend.app.sockets.live_stream import live_stream_hub


@dataclass
class SimulationRuntime:
    task: asyncio.Task | None = None
    latest_events: list[dict] = field(default_factory=list)
    action_log: list[dict] = field(default_factory=list)
    trade_log: list[dict] = field(default_factory=list)
    summary: dict = field(default_factory=dict)

    async def ensure_running(self, scenario_id: str = "demo_week") -> None:
        engine = replay_service.ensure(scenario_id=scenario_id)
        if self.task and not self.task.done():
            return
        engine.start()
        self.task = asyncio.create_task(self._loop())

    async def _loop(self) -> None:
        engine = replay_service.ensure()
        while engine.state.running:
            event = engine.next_event()
            if not event:
                await asyncio.sleep(0.02)
                continue

            now = time.perf_counter()
            rows = event["house_rows"]
            grouped: dict[str, list[dict]] = {}
            for row in rows:
                grouped.setdefault(str(row["house_id"]), []).append(row)

            house_states: list[dict] = []
            for house_id, house_rows in grouped.items():
                load_kw = float(sum(float(r["power_kw"]) for r in house_rows))
                flexible_kw = float(sum(float(r["power_kw"]) for r in house_rows if r.get("appliance_id") != "fridge"))
                obs = {
                    "price": float(event["price"]["grid_buy_price"]),
                    "comfort_slack": 0.6,
                    "deadline_slack": max(0.1, 1.0 - (engine.state.current_step / max(engine.state.end_index, 1))),
                    "flexible_ratio": 0.0 if load_kw <= 0 else min(1.0, flexible_kw / load_kw),
                    "community_signal": agent_service.community_agent.latest_signal,
                }
                decision = policy_service.step_house(house_id=house_id, obs=obs)
                state = {
                    "house_id": house_id,
                    "load_kw": load_kw,
                    "flexible_kw": flexible_kw,
                    "decision": decision,
                    "net_kw": load_kw,
                }
                agent_service.update_house_state(state)
                house_states.append(state)
                self.action_log.append(
                    {
                        "timestamp": event["timestamp"],
                        "house_id": house_id,
                        "action": decision["action"],
                        "reason": decision["reason"],
                        "inference_latency_ms": (time.perf_counter() - now) * 1000,
                    }
                )

            community = agent_service.community_state()
            market = market_service.step(house_states=house_states, price=event["price"])
            self.trade_log.extend(market["trades"])

            payloads = {
                "community": {
                    "timestamp": event["timestamp"],
                    "community": community,
                    "market": market,
                },
                "price": {"timestamp": event["timestamp"], "price": event["price"]},
                "actions": {"timestamp": event["timestamp"], "actions": self.action_log[-len(house_states) :]},
                "trades": {"timestamp": event["timestamp"], "trades": market["trades"]},
                "houses": {
                    "timestamp": event["timestamp"],
                    "house_states": house_states,
                },
            }
            await live_stream_hub.fanout(payloads)
            self.latest_events.append({"event": event, "community": community, "market": market, "houses": house_states})
            self.latest_events = self.latest_events[-500:]

        self.summary = self.compute_summary()

    def compute_summary(self) -> dict:
        if not self.latest_events:
            return {}
        community_load = [
            float(x["community"].get("total_kw", 0.0))
            for x in self.latest_events
            if "community" in x and isinstance(x["community"], dict)
        ]
        peak = max(community_load) if community_load else 0.0
        avg = sum(community_load) / len(community_load) if community_load else 0.0
        par = peak / avg if avg > 0 else 0.0
        total_cost = 0.0
        per_house: dict[str, float] = {}
        for e in self.latest_events:
            price = float(e["event"]["price"].get("grid_buy_price", 0.2))
            for hs in e["houses"]:
                c = float(hs.get("load_kw", 0.0)) * price / 12.0
                per_house[hs["house_id"]] = per_house.get(hs["house_id"], 0.0) + c
                total_cost += c
        fairness = 0.0
        vals = list(per_house.values())
        if vals:
            denom = len(vals) * sum(v * v for v in vals)
            fairness = ((sum(vals) ** 2) / denom) if denom > 1e-9 else 0.0

        return {
            "total_cost": total_cost,
            "community_cost": total_cost,
            "peak_demand_kw": peak,
            "par": par,
            "trade_volume_kwh": float(sum(float(t.get("energy_kwh", 0.0)) for t in self.trade_log)),
            "fairness_jain": fairness,
            "per_house": [{"house_id": k, "cost": v} for k, v in sorted(per_house.items())],
            "decision_update_frequency": len(self.action_log),
            "inference_latency_ms_avg": (
                sum(float(a.get("inference_latency_ms", 0.0)) for a in self.action_log) / len(self.action_log)
                if self.action_log
                else 0.0
            ),
        }


simulation_runtime = SimulationRuntime()
