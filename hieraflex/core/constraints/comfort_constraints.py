from __future__ import annotations


def comfort_penalty(delay_steps: int, slack_steps: int) -> float:
    if delay_steps <= slack_steps:
        return 0.0
    return float(delay_steps - slack_steps)
