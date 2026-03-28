from __future__ import annotations

from backend.app.services.dataset_service import dataset_service
from core.replay.replay_engine import ReplayEngine


def test_replay_engine_step_flow() -> None:
    bundle = dataset_service.load_bundle()
    engine = ReplayEngine(trace=bundle.trace, prices=bundle.prices)
    engine.configure("demo", 0, 20, 120.0)
    engine.start()
    event = engine.next_event()
    assert event is not None
    assert "price" in event
    assert "house_rows" in event
    engine.pause()
    assert engine.snapshot()["running"] is False
