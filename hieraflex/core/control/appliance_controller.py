from __future__ import annotations


def enforce_appliance_safety(command: str, interruptible: bool, running: bool) -> tuple[bool, str]:
    if command == "defer" and running and not interruptible:
        return False, "non_interruptible_cycle"
    return True, "ok"
