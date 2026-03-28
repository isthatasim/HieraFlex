from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class BidOffer:
    house_id: str
    bid_kwh: float = 0.0
    offer_kwh: float = 0.0


class BidOfferEngine:
    def build(self, house_states: list[dict]) -> list[BidOffer]:
        out: list[BidOffer] = []
        for state in house_states:
            net = float(state.get("net_kw", 0.0))
            hid = str(state["house_id"])
            if net > 0:
                out.append(BidOffer(house_id=hid, bid_kwh=max(net, 0.0) / 12.0, offer_kwh=0.0))
            else:
                out.append(BidOffer(house_id=hid, bid_kwh=0.0, offer_kwh=max(-net, 0.0) / 12.0))
        return out
