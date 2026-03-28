from __future__ import annotations

from dataclasses import dataclass

from core.market.bid_offer_engine import BidOffer


@dataclass(slots=True)
class MatchedTrade:
    seller_house_id: str
    buyer_house_id: str
    energy_kwh: float


class PeerMatchingEngine:
    def match(self, books: list[BidOffer]) -> list[MatchedTrade]:
        sellers = [{"house_id": b.house_id, "qty": b.offer_kwh} for b in books if b.offer_kwh > 0]
        buyers = [{"house_id": b.house_id, "qty": b.bid_kwh} for b in books if b.bid_kwh > 0]

        trades: list[MatchedTrade] = []
        i = j = 0
        while i < len(sellers) and j < len(buyers):
            qty = min(sellers[i]["qty"], buyers[j]["qty"])
            if qty <= 0:
                break
            trades.append(
                MatchedTrade(
                    seller_house_id=sellers[i]["house_id"],
                    buyer_house_id=buyers[j]["house_id"],
                    energy_kwh=float(qty),
                )
            )
            sellers[i]["qty"] -= qty
            buyers[j]["qty"] -= qty
            if sellers[i]["qty"] <= 1e-9:
                i += 1
            if buyers[j]["qty"] <= 1e-9:
                j += 1
        return trades
