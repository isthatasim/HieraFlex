from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class EventClock:
    step: int = 0
    speed: float = 60.0
    running: bool = False

    def tick(self) -> int:
        self.step += 1
        return self.step

    def reset(self) -> None:
        self.step = 0

    def set_speed(self, speed: float) -> None:
        self.speed = max(0.1, speed)
