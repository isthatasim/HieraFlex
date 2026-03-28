from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class PlanDecision:
    action: str
    utility_score: float
    reason_tag: str


class AgentPlanner:
    def plan(
        self,
        price: float,
        comfort_slack: float,
        deadline_slack: float,
        flexible_ratio: float,
        community_signal: float,
    ) -> PlanDecision:
        urgency = max(0.0, 1.0 - deadline_slack)
        price_pressure = min(1.0, max(0.0, (price - 0.2) / 0.25))

        if urgency > 0.7:
            return PlanDecision("start_flexible", 0.9 - 0.2 * price_pressure, "deadline")
        if price_pressure > 0.6 and comfort_slack > 0.2:
            return PlanDecision("defer_flexible", 0.8 + 0.2 * flexible_ratio, "price")
        if community_signal > 0.5 and flexible_ratio > 0.3:
            return PlanDecision("offer_flex", 0.75, "community")
        return PlanDecision("keep", 0.6, "stability")
