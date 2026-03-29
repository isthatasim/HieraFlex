from __future__ import annotations

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.services.run_registry import run_registry
from backend.app.services.training_manager import training_manager


client = TestClient(app)


def test_api_root_and_houses() -> None:
    root = client.get("/")
    assert root.status_code == 200
    houses = client.get("/houses")
    assert houses.status_code == 200
    assert isinstance(houses.json(), list)


def test_api_simulation_controls() -> None:
    start = client.post("/simulation/start", json={"scenario_id": "demo_week", "start_index": 0, "end_index": 24, "replay_speed": 20})
    assert start.status_code == 200
    pause = client.post("/simulation/pause")
    assert pause.status_code == 200
    reset = client.post("/simulation/reset")
    assert reset.status_code == 200


def test_api_training_routes(monkeypatch) -> None:
    fake_run = {
        "run_id": "api_fake_run",
        "status": "running",
        "algorithm": "ppo_single",
        "scenario_id": "demo_week",
        "config_path": "experiments/configs/single_house.yaml",
        "current_episode": 0,
        "episodes_target": 10,
    }

    monkeypatch.setattr(training_manager, "start_run", lambda payload: fake_run)
    monkeypatch.setattr(training_manager, "stop_run", lambda run_id: {**fake_run, "run_id": run_id, "status": "stop_requested"})
    monkeypatch.setattr(training_manager, "resume_run", lambda run_id, checkpoint_path=None, extra_episodes=50: {**fake_run, "run_id": run_id, "status": "running"})
    monkeypatch.setattr(training_manager, "sync_processes", lambda: None)

    monkeypatch.setattr(run_registry, "list_runs", lambda: [fake_run])
    monkeypatch.setattr(run_registry, "load_run", lambda run_id: {**fake_run, "run_id": run_id})

    start = client.post(
        "/training/start",
        json={
            "algorithm": "ppo_single",
            "config_path": "experiments/configs/single_house.yaml",
            "scenario_id": "demo_week",
            "episodes": 10,
            "seed": 42,
            "checkpoint_interval": 2,
            "eval_interval": 2,
            "houses": ["H1"],
        },
    )
    assert start.status_code == 200

    stop = client.post("/training/stop", json={"run_id": "api_fake_run"})
    assert stop.status_code == 200

    resume = client.post("/training/resume", json={"run_id": "api_fake_run", "extra_episodes": 5})
    assert resume.status_code == 200

    runs = client.get("/training/runs")
    assert runs.status_code == 200
    assert runs.json()["runs"]

    details = client.get("/training/runs/api_fake_run")
    assert details.status_code == 200

    compare = client.post("/training/compare", json={"run_ids": ["api_fake_run"]})
    assert compare.status_code == 200
    assert compare.json()["comparisons"]


def test_resource_visualization_endpoint() -> None:
    res = client.get("/houses/H1/resources?limit=24")
    assert res.status_code == 200
    payload = res.json()
    assert "timeline" in payload
    assert "appliances" in payload


def test_artifacts_endpoints() -> None:
    models = client.get("/artifacts/models")
    results = client.get("/artifacts/results")
    assert models.status_code == 200
    assert results.status_code == 200
