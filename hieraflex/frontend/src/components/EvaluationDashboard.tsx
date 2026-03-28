import React from "react";

export function EvaluationDashboard({ summary }: { summary: Record<string, unknown> }) {
  return (
    <section className="panel">
      <h2>Evaluation Dashboard</h2>
      <div className="metric-grid">
        <div><span>Community Cost</span><strong>{Number(summary.community_cost ?? 0).toFixed(2)}</strong></div>
        <div><span>Peak</span><strong>{Number(summary.peak_demand_kw ?? 0).toFixed(2)} kW</strong></div>
        <div><span>PAR</span><strong>{Number(summary.par ?? 0).toFixed(3)}</strong></div>
        <div><span>Trade Volume</span><strong>{Number(summary.trade_volume_kwh ?? 0).toFixed(3)} kWh</strong></div>
      </div>
    </section>
  );
}
