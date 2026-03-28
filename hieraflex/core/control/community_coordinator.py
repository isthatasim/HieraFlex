from __future__ import annotations


def community_peak_signal(total_kw: float, cap_kw: float) -> dict:
    excess = max(0.0, total_kw - cap_kw)
    return {"total_kw": total_kw, "cap_kw": cap_kw, "peak_excess_kw": excess, "is_peak": excess > 0}
