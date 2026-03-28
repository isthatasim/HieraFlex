from __future__ import annotations

from dataclasses import dataclass

from core.replay.replay_engine import ReplayEngine

from backend.app.services.dataset_service import dataset_service


@dataclass
class ReplayService:
    engine: ReplayEngine | None = None

    def ensure(self, scenario_id: str = "demo_week") -> ReplayEngine:
        if self.engine is None:
            bundle = dataset_service.load_bundle(scenario_id=scenario_id)
            self.engine = ReplayEngine(trace=bundle.trace, prices=bundle.prices)
        return self.engine

    def reset_engine(self, scenario_id: str = "demo_week") -> ReplayEngine:
        bundle = dataset_service.load_bundle(scenario_id=scenario_id)
        self.engine = ReplayEngine(trace=bundle.trace, prices=bundle.prices)
        return self.engine


replay_service = ReplayService()
