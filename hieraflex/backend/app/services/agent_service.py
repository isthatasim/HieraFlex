from __future__ import annotations

from dataclasses import dataclass, field

from core.agents.community_agent import CommunityAgent


@dataclass
class AgentService:
    community_agent: CommunityAgent = field(default_factory=CommunityAgent)
    latest_house_states: dict[str, dict] = field(default_factory=dict)

    def update_house_state(self, state: dict) -> None:
        self.latest_house_states[str(state["house_id"])] = state

    def community_state(self) -> dict:
        houses = []
        for hid, state in self.latest_house_states.items():
            houses.append(
                {
                    "house_id": hid,
                    "load_kw": float(state.get("load_kw", 0.0)),
                    "flexible_kw": float(state.get("flexible_kw", 0.0)),
                }
            )
        return self.community_agent.coordinate(houses)


agent_service = AgentService()
