from __future__ import annotations


def battery_step(
    soc: float,
    p_ch: float,
    p_dis: float,
    dt_h: float,
    eta_ch: float,
    eta_dis: float,
    soc_min: float,
    soc_max: float,
) -> float:
    next_soc = soc + eta_ch * p_ch * dt_h - (p_dis * dt_h) / max(eta_dis, 1e-6)
    return float(min(max(next_soc, soc_min), soc_max))
