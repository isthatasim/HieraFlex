from __future__ import annotations

import subprocess

from backend.app.services.metrics_stream_service import metrics_stream_service
from backend.app.services.checkpoint_service import checkpoint_service
from backend.app.services.experiment_tracker import experiment_tracker
from backend.app.services.run_registry import run_registry
from backend.app.services.training_manager import training_manager


def test_run_registry_and_tracking_roundtrip() -> None:
    run_id = "test_run_registry_roundtrip"
    # idempotent cleanup of previous leftovers by overwriting status when exists
    try:
        run = run_registry.create_run(
            {
                "run_id": run_id,
                "algorithm": "ppo_single",
                "config_path": "experiments/configs/single_house.yaml",
                "scenario_id": "demo_week",
                "episodes_target": 3,
                "seed": 123,
            }
        )
    except ValueError:
        run = run_registry.update_run(run_id, status="queued", current_episode=0, current_step=0)

    assert run["run_id"] == run_id

    experiment_tracker.append_metric(run_id, {"episode": 1, "episode_return": 1.2, "energy_cost": 0.8})
    experiment_tracker.append_metric(run_id, {"episode": 2, "episode_return": 1.6, "energy_cost": 0.7})
    checkpoint_service.register(run_id, "fake/path/checkpoint_ep_0002.pt", episode=2, score=1.6, is_best=True)

    summary = experiment_tracker.summarize(run_id)
    assert summary["episodes"] >= 2
    assert summary["best_return"] >= summary["latest_return"] or summary["latest_return"] >= 0

    checkpoints = checkpoint_service.list_checkpoints(run_id)
    assert checkpoints
    assert checkpoints[-1]["episode"] == 2


def test_metrics_stream_poll_cursor_behavior() -> None:
    run_id = "test_metrics_stream_poll"
    try:
        run_registry.create_run({"run_id": run_id, "algorithm": "ppo_single", "episodes_target": 2})
    except ValueError:
        run_registry.update_run(run_id, status="queued", current_episode=0, current_step=0)

    experiment_tracker.append_metric(run_id, {"episode": 1, "episode_return": 0.5, "energy_cost": 1.1})
    checkpoint_service.register(run_id, "fake/path/ep1.pt", episode=1, score=0.5, is_best=True)

    first = metrics_stream_service.poll(run_id)
    assert len(first["new_metrics"]) >= 1
    assert len(first["new_checkpoints"]) >= 1

    second = metrics_stream_service.poll(run_id)
    assert second["new_metrics"] == []
    assert second["new_checkpoints"] == []


def test_duplicate_run_id_is_rejected() -> None:
    run_id = "test_duplicate_run_id"
    try:
        run_registry.create_run({"run_id": run_id, "algorithm": "ppo_single"})
    except ValueError:
        pass

    raised = False
    try:
        run_registry.create_run({"run_id": run_id, "algorithm": "ppo_single"})
    except ValueError:
        raised = True
    assert raised


def test_resume_clears_stop_marker(monkeypatch) -> None:
    run_id = "test_resume_clears_stop_marker"
    try:
        run_registry.create_run({"run_id": run_id, "algorithm": "ppo_single", "status": "stopped"})
    except ValueError:
        run_registry.update_run(run_id, status="stopped", latest_checkpoint=None)

    stop_file = run_registry.run_dir(run_id) / "STOP"
    stop_file.write_text("stop requested", encoding="utf-8")

    class _DummyProc:
        pid = 99999

        def poll(self):
            return None

    monkeypatch.setattr(subprocess, "Popen", lambda *args, **kwargs: _DummyProc())
    resumed = training_manager.resume_run(run_id=run_id, extra_episodes=1)
    assert resumed["status"] == "running"
    assert not stop_file.exists()
