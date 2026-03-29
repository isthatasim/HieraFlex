import React from "react";

import type { RunMetric, TrainingRun } from "../types/domain";

type Props = {
  status: Record<string, unknown>;
  run?: TrainingRun;
  metrics: RunMetric[];
  latestMetric?: RunMetric | null;
};

function metricPath(values: number[], width: number, height: number): string {
  if (values.length === 0) return "";
  const min = Math.min(...values);
  const max = Math.max(...values);
  const span = Math.max(1e-6, max - min);
  return values
    .map((value, idx) => {
      const x = (idx / Math.max(1, values.length - 1)) * width;
      const y = height - ((value - min) / span) * height;
      return `${idx === 0 ? "M" : "L"}${x},${y}`;
    })
    .join(" ");
}

export function TrainingDashboard({ status, run, metrics, latestMetric }: Props) {
  const returns = metrics.map((m) => m.episode_return);
  const costs = metrics.map((m) => m.energy_cost);
  const width = 340;
  const height = 100;

  return (
    <section className="panel">
      <h2>Training Dashboard</h2>
      <div className="metric-grid">
        <div>
          <small>Status</small>
          <p><strong>{run?.status ?? "idle"}</strong></p>
        </div>
        <div>
          <small>Episode</small>
          <p><strong>{run ? `${run.current_episode}/${run.episodes_target}` : "--"}</strong></p>
        </div>
        <div>
          <small>Latest Return</small>
          <p><strong>{latestMetric?.episode_return?.toFixed?.(3) ?? "--"}</strong></p>
        </div>
        <div>
          <small>Latest Cost</small>
          <p><strong>{latestMetric?.energy_cost?.toFixed?.(3) ?? "--"}</strong></p>
        </div>
      </div>

      <div className="split-grid">
        <div>
          <h3>Reward Trend</h3>
          <svg viewBox={`0 0 ${width} ${height}`} className="chart-svg">
            <path d={metricPath(returns, width, height)} fill="none" stroke="var(--brand)" strokeWidth="2" />
          </svg>
        </div>
        <div>
          <h3>Cost Trend</h3>
          <svg viewBox={`0 0 ${width} ${height}`} className="chart-svg">
            <path d={metricPath(costs, width, height)} fill="none" stroke="var(--accent)" strokeWidth="2" />
          </svg>
        </div>
      </div>

      <details>
        <summary>Raw Status Payload</summary>
        <pre>{JSON.stringify(status, null, 2)}</pre>
      </details>
    </section>
  );
}
