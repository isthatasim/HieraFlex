from __future__ import annotations

import statistics
from dataclasses import dataclass

from core.market.peer_matching import MatchedTrade


@dataclass(slots=True)
class ClearingResult:
    local_clearing_price: float
    matched_kwh: float
    trades: list[dict]
    fairness_penalty: float


class ClearingEngine:
    def clear(
        self,
        trades: list[MatchedTrade],
        grid_buy_price: float,
        grid_sell_price: float,
        savings_by_house: dict[str, float] | None = None,
    ) -> ClearingResult:
        matched_kwh = float(sum(t.energy_kwh for t in trades))
        local_price = float((grid_buy_price + grid_sell_price) / 2.0)
        fairness_penalty = 0.0
        if savings_by_house:
            vals = list(savings_by_house.values())
            if len(vals) > 1:
                fairness_penalty = float(statistics.pvariance(vals))
        return ClearingResult(
            local_clearing_price=local_price,
            matched_kwh=matched_kwh,
            trades=[t.__dict__ for t in trades],
            fairness_penalty=fairness_penalty,
        )
