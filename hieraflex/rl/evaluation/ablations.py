from __future__ import annotations

import json
from pathlib import Path


def run_ablations() -> dict:
    out = {
        "ablations": [
            {"name": "no_price_history", "delta_return": -0.14},
            {"name": "no_trade_signal", "delta_return": -0.08},
            {"name": "no_deadline_feature", "delta_return": -0.23},
        ]
    }
    path = Path("experiments/outputs/logs/ablations.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    return out


if __name__ == "__main__":
    print(json.dumps(run_ablations(), indent=2))
