from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field


@dataclass
class AgentMemory:
    horizon: int = 24
    prices: deque[float] = field(default_factory=lambda: deque(maxlen=24))
    actions: deque[str] = field(default_factory=lambda: deque(maxlen=24))
    rewards: deque[float] = field(default_factory=lambda: deque(maxlen=24))

    def push_price(self, price: float) -> None:
        self.prices.append(float(price))

    def push_action(self, action: str) -> None:
        self.actions.append(action)

    def push_reward(self, reward: float) -> None:
        self.rewards.append(float(reward))

    def price_trend(self) -> float:
        if len(self.prices) < 2:
            return 0.0
        return float(self.prices[-1] - self.prices[0])
