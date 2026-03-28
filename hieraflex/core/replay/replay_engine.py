from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

import pandas as pd

from core.replay.event_clock import EventClock


@dataclass(slots=True)
class ReplayState:
    running: bool = False
    current_step: int = 0
    start_index: int = 0
    end_index: int = 0
    speed: float = 60.0
    scenario_id: str = "demo_week"


@dataclass
class ReplayEngine:
    trace: pd.DataFrame
    prices: pd.DataFrame
    clock: EventClock = field(default_factory=EventClock)
    state: ReplayState = field(default_factory=ReplayState)

    def __post_init__(self) -> None:
        self.timeline = sorted(self.trace["timestamp"].unique().tolist())
        self.state.end_index = len(self.timeline)
        self.price_by_ts = {r["timestamp"]: r for _, r in self.prices.iterrows()}

    def configure(self, scenario_id: str, start: int, end: int, speed: float) -> None:
        self.state.scenario_id = scenario_id
        self.state.start_index = max(0, start)
        self.state.end_index = min(len(self.timeline), max(start + 1, end))
        self.state.current_step = self.state.start_index
        self.state.speed = speed
        self.clock.set_speed(speed)

    def start(self) -> None:
        self.state.running = True

    def pause(self) -> None:
        self.state.running = False

    def reset(self) -> None:
        self.state.current_step = self.state.start_index
        self.clock.reset()

    def seek(self, step: int) -> None:
        self.state.current_step = min(max(self.state.start_index, step), self.state.end_index - 1)

    def next_event(self) -> dict[str, Any] | None:
        if not self.state.running:
            return None
        if self.state.current_step >= self.state.end_index:
            self.state.running = False
            return None

        ts = self.timeline[self.state.current_step]
        house_slice = self.trace[self.trace["timestamp"] == ts].copy()
        price = self.price_by_ts.get(ts, {})
        event = {
            "timestamp": ts,
            "step": self.state.current_step,
            "price": {
                "grid_buy_price": float(price.get("grid_buy_price", 0.2)),
                "grid_sell_price": float(price.get("grid_sell_price", 0.1)),
                "incentive_price": float(price.get("incentive_price", 0.0)),
            },
            "house_rows": house_slice.to_dict(orient="records"),
        }
        self.state.current_step += 1
        sleep_s = max(0.0, 1.0 / self.clock.speed)
        if sleep_s > 0.0:
            time.sleep(min(sleep_s, 0.05))
        return event

    def snapshot(self) -> dict[str, Any]:
        return {
            "running": self.state.running,
            "current_step": self.state.current_step,
            "start_index": self.state.start_index,
            "end_index": self.state.end_index,
            "speed": self.state.speed,
            "scenario_id": self.state.scenario_id,
            "timeline_size": len(self.timeline),
        }
