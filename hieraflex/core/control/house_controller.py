from __future__ import annotations


def apply_house_policy_to_appliances(rows: list[dict], action: str) -> list[dict]:
    out: list[dict] = []
    for row in rows:
        r = dict(row)
        if action == "defer_flexible" and row.get("appliance_id") not in {"fridge"}:
            r["command"] = "defer"
        elif action == "start_flexible":
            r["command"] = "start"
        elif action == "offer_flex":
            r["command"] = "offer"
        else:
            r["command"] = "hold"
        out.append(r)
    return out
