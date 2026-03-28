from __future__ import annotations


def non_interruptible_feasible(running: bool, command: str, interruptible: bool) -> bool:
    return not (running and command == "defer" and not interruptible)
