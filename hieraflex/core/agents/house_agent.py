from __future__ import annotations

from dataclasses import dataclass, field

from core.agents.agent_explainer import AgentExplainer, DecisionExplanation
from core.agents.agent_memory import AgentMemory
from core.agents.agent_planner import AgentPlanner


@dataclass
class HouseAgent:
    house_id: str
    memory: AgentMemory = field(default_factory=AgentMemory)
    planner: AgentPlanner = field(default_factory=AgentPlanner)
    explainer: AgentExplainer = field(default_factory=AgentExplainer)

    def observe_reason_plan_act(self, obs: dict) -> dict:
        price = float(obs.get("price", 0.2))
        comfort_slack = float(obs.get("comfort_slack", 0.5))
        deadline_slack = float(obs.get("deadline_slack", 0.5))
        flexible_ratio = float(obs.get("flexible_ratio", 0.4))
        community_signal = float(obs.get("community_signal", 0.0))

        self.memory.push_price(price)
        decision = self.planner.plan(
            price=price,
            comfort_slack=comfort_slack,
            deadline_slack=deadline_slack,
            flexible_ratio=flexible_ratio,
            community_signal=community_signal,
        )
        self.memory.push_action(decision.action)

        reward = (
            -price
            - 0.5 * max(0.0, 1.0 - deadline_slack)
            - 0.2 * max(0.0, 0.3 - comfort_slack)
            + 0.4 * flexible_ratio
        )
        self.memory.push_reward(reward)

        explanation: DecisionExplanation = self.explainer.explain(
            action=decision.action,
            driver=decision.reason_tag,
            price=price,
            deadline_slack=deadline_slack,
            flexibility=flexible_ratio,
            comfort_risk=max(0.0, 0.3 - comfort_slack),
        )

        return {
            "house_id": self.house_id,
            "action": decision.action,
            "utility_score": decision.utility_score,
            "reason": decision.reason_tag,
            "reward": reward,
            "explanation": explanation.__dict__,
            "trend": self.memory.price_trend(),
        }
