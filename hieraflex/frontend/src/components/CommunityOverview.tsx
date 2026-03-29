import React from "react";

import type { CommunitySnapshot } from "../types/domain";

type Props = {
  snapshot: CommunitySnapshot | null;
};

export function CommunityOverview({ snapshot }: Props) {
  return (
    <section className="panel">
      <h2>Community Overview</h2>
      <div className="metric-grid">
        <div><span>Total Demand</span><strong>{snapshot?.community?.total_kw?.toFixed(2) ?? "--"} kW</strong></div>
        <div><span>Flexible Demand</span><strong>{snapshot?.community?.flexible_kw?.toFixed(2) ?? "--"} kW</strong></div>
        <div><span>Local Trade</span><strong>{snapshot?.market?.matched_kwh?.toFixed(3) ?? "--"} kWh</strong></div>
        <div><span>Clearing Price</span><strong>{snapshot?.market?.local_clearing_price?.toFixed(3) ?? "--"}</strong></div>
        <div><span>Fairness Penalty</span><strong>{snapshot?.market?.fairness_penalty?.toFixed(4) ?? "--"}</strong></div>
        <div><span>Coordination Signal</span><strong>{snapshot?.community?.coordination_signal?.toFixed(2) ?? "--"}</strong></div>
      </div>
    </section>
  );
}
