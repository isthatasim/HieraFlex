from __future__ import annotations

from backend.app.services.deployment_service import deployment_service


def test_deployment_status_shape() -> None:
    st = deployment_service.status()
    assert "huggingface_ready" in st
    assert "variables_present" in st
    assert "HF_TOKEN" in st["variables_present"]
