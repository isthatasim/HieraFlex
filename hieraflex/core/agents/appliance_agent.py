from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ApplianceDecision:
    appliance_id: str
    command: str
    feasible: bool
    message: str


class ApplianceAgent:
    def decide(self, appliance_id: str, command: str, interruptible: bool, running: bool) -> ApplianceDecision:
        if command == "defer" and (running and not interruptible):
            return ApplianceDecision(appliance_id, command, False, "Blocked: non-interruptible cycle in progress")
        return ApplianceDecision(appliance_id, command, True, "Accepted")
