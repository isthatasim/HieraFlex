from __future__ import annotations

from backend.app.services.market_service import market_service


def test_market_step() -> None:
    house_states = [
        {"house_id": "H1", "net_kw": 2.0},
        {"house_id": "H2", "net_kw": -1.5},
        {"house_id": "H3", "net_kw": 0.4},
    ]
    out = market_service.step(house_states, {"grid_buy_price": 0.3, "grid_sell_price": 0.1, "incentive_price": 0.0})
    assert "local_clearing_price" in out
    assert out["local_clearing_price"] > 0
