from __future__ import annotations


def enforce_house_cap(total_load_kw: float, cap_kw: float) -> tuple[float, bool]:
    if total_load_kw <= cap_kw:
        return total_load_kw, False
    return cap_kw, True
