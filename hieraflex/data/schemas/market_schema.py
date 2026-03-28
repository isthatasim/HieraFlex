from __future__ import annotations

from pydantic import BaseModel, Field


class PriceSample(BaseModel):
    timestamp: str
    grid_buy_price: float = Field(ge=0.0)
    grid_sell_price: float = Field(ge=0.0)
    incentive_price: float = Field(default=0.0)


class TradeEvent(BaseModel):
    timestamp: str
    seller_house_id: str
    buyer_house_id: str
    energy_kwh: float = Field(ge=0.0)
    clearing_price: float = Field(ge=0.0)
