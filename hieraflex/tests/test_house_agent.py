from __future__ import annotations

from core.agents.house_agent import HouseAgent


def test_house_agent_loop() -> None:
    agent = HouseAgent(house_id="H1")
    out = agent.observe_reason_plan_act(
        {
            "price": 0.35,
            "comfort_slack": 0.7,
            "deadline_slack": 0.6,
            "flexible_ratio": 0.4,
            "community_signal": 0.2,
        }
    )
    assert out["house_id"] == "H1"
    assert "explanation" in out
    assert out["action"] in {"start_flexible", "defer_flexible", "keep", "offer_flex"}
