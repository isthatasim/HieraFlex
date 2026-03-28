from __future__ import annotations

from fastapi.testclient import TestClient

from backend.app.main import app


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
