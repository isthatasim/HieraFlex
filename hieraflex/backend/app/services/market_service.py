from __future__ import annotations

from dataclasses import dataclass, field

from core.market.bid_offer_engine import BidOfferEngine
from core.market.clearing_engine import ClearingEngine, ClearingResult
from core.market.peer_matching import PeerMatchingEngine
from core.market.tariff_engine import TariffEngine


@dataclass
class MarketService:
    tariff: TariffEngine = field(default_factory=TariffEngine)
    bid_offer: BidOfferEngine = field(default_factory=BidOfferEngine)
    matching: PeerMatchingEngine = field(default_factory=PeerMatchingEngine)
    clearing: ClearingEngine = field(default_factory=ClearingEngine)
    latest_state: dict = field(default_factory=dict)

    def step(self, house_states: list[dict], price: dict, savings_by_house: dict[str, float] | None = None) -> dict:
        tariff_values = self.tariff.price(
            buy_price=float(price.get("grid_buy_price", 0.2)),
            sell_price=float(price.get("grid_sell_price", 0.1)),
            incentive=float(price.get("incentive_price", 0.0)),
        )
        books = self.bid_offer.build(house_states)
        trades = self.matching.match(books)
        cleared: ClearingResult = self.clearing.clear(
            trades=trades,
            grid_buy_price=tariff_values["grid_buy"],
            grid_sell_price=tariff_values["grid_sell"],
            savings_by_house=savings_by_house,
        )
        self.latest_state = {
            "tariff": tariff_values,
            "matched_kwh": cleared.matched_kwh,
            "local_clearing_price": cleared.local_clearing_price,
            "trades": cleared.trades,
            "fairness_penalty": cleared.fairness_penalty,
        }
        return self.latest_state


market_service = MarketService()
