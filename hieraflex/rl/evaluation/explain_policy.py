from __future__ import annotations

import json
from pathlib import Path


def explain() -> dict:
    explanation = {
        "reward_decomposition": {
            "energy": "penalizes high-price consumption",
            "peak": "discourages synchronized peaks",
            "comfort": "penalizes missed service windows",
            "trade": "rewards useful local exchange",
            "responsiveness": "rewards adapting to price changes",
        },
        "dominant_drivers": ["price", "deadline", "community_signal"],
    }
    path = Path("experiments/outputs/logs/policy_explain.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(explanation, indent=2), encoding="utf-8")
    return explanation


if __name__ == "__main__":
    print(json.dumps(explain(), indent=2))
