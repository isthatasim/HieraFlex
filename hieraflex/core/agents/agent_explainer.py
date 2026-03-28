from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class DecisionExplanation:
    title: str
    summary: str
    dominant_driver: str
    reward_terms: dict[str, float]


class AgentExplainer:
    def explain(
        self,
        action: str,
        driver: str,
        price: float,
        deadline_slack: float,
        flexibility: float,
        comfort_risk: float,
    ) -> DecisionExplanation:
        reward_terms = {
            "energy": -price,
            "deadline": -max(0.0, 1.0 - deadline_slack),
            "flexibility": flexibility,
            "comfort": -comfort_risk,
        }
        summary = (
            f"Action '{action}' selected because {driver} dominated this step; "
            f"price={price:.3f}, deadline_slack={deadline_slack:.2f}, flexibility={flexibility:.2f}."
        )
        return DecisionExplanation(
            title=f"Decision: {action}",
            summary=summary,
            dominant_driver=driver,
            reward_terms=reward_terms,
        )
