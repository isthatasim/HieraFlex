from __future__ import annotations

from dataclasses import dataclass, field

from core.agents.house_agent import HouseAgent


@dataclass
class PolicyService:
    house_agents: dict[str, HouseAgent] = field(default_factory=dict)

    def get_or_create(self, house_id: str) -> HouseAgent:
        if house_id not in self.house_agents:
            self.house_agents[house_id] = HouseAgent(house_id=house_id)
        return self.house_agents[house_id]

    def step_house(self, house_id: str, obs: dict) -> dict:
        agent = self.get_or_create(house_id)
        return agent.observe_reason_plan_act(obs)


policy_service = PolicyService()
