from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CommunityAgent:
    fairness_weight: float = 1.0
    latest_signal: float = 0.0
    history: list[dict] = field(default_factory=list)

    def coordinate(self, houses: list[dict]) -> dict:
        total_kw = float(sum(float(h.get("load_kw", 0.0)) for h in houses))
        flexible_kw = float(sum(float(h.get("flexible_kw", 0.0)) for h in houses))
        peak_ratio = flexible_kw / (total_kw + 1e-6)
        signal = min(1.0, max(0.0, peak_ratio))
        self.latest_signal = signal
        state = {
            "total_kw": total_kw,
            "flexible_kw": flexible_kw,
            "coordination_signal": signal,
            "congestion": total_kw > 0 and peak_ratio < 0.25,
        }
        self.history.append(state)
        return state
