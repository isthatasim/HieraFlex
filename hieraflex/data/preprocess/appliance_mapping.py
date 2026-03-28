from __future__ import annotations

APPLIANCE_MAPPING: dict[str, dict[str, object]] = {
    "hvac": {"interruptible": True, "flexible": True, "priority": 0.9},
    "washer": {"interruptible": False, "flexible": True, "priority": 0.5},
    "dishwasher": {"interruptible": False, "flexible": True, "priority": 0.6},
    "water_heater": {"interruptible": True, "flexible": True, "priority": 0.8},
    "fridge": {"interruptible": True, "flexible": False, "priority": 1.0},
}


def classify_appliance(appliance_id: str) -> dict[str, object]:
    return APPLIANCE_MAPPING.get(appliance_id, {"interruptible": True, "flexible": True, "priority": 0.7})
