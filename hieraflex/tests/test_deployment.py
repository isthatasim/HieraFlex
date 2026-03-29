from __future__ import annotations

from backend.app.services.deployment_service import deployment_service


def test_deployment_status_shape() -> None:
    st = deployment_service.status()
    assert "huggingface_ready" in st
    assert "variables_present" in st
    assert "HF_TOKEN" in st["variables_present"]


def test_deployment_mode_from_env(monkeypatch) -> None:
    monkeypatch.setenv("HIERAFLEX_MODE", "public-demo")
    monkeypatch.setenv("HF_TOKEN", "x")
    monkeypatch.setenv("HF_DATASET_REPO_ID", "x/y")
    monkeypatch.setenv("HF_MODEL_REPO_ID", "x/y")
    monkeypatch.setenv("HF_SPACE_REPO_ID", "x/y")
    monkeypatch.setenv("HF_USERNAME", "x")

    st = deployment_service.status()
    assert st["mode"] == "public-demo"
    assert st["huggingface_ready"] is True
