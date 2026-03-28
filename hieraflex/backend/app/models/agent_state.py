from __future__ import annotations

from pydantic import BaseModel


class AgentStateModel(BaseModel):
    house_id: str
    action: str
    utility_score: float
    reason: str
    reward: float
    trend: float
    explanation: dict
