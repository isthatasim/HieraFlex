from __future__ import annotations

from data.loaders.deddiag_adapter import DEDDIAGAdapter


def test_deddiag_loader_fallback() -> None:
    adapter = DEDDIAGAdapter(root="nonexistent/path")
    df = adapter.load(houses=2, steps=48)
    assert not df.empty
    assert {"timestamp", "house_id", "appliance_id", "power_kw"}.issubset(df.columns)
    assert len(adapter.detect_houses(df)) == 2
