from __future__ import annotations


def ev_charge_step(soc: float, p_ev: float, dt_h: float, eta_ev: float, soc_max: float) -> float:
    return float(min(soc_max, soc + eta_ev * p_ev * dt_h))
