import React from "react";

import type { TrainingRun } from "../types/domain";
import { AgentStatusBadge } from "./AgentStatusBadge";

export function TrainingRunTable({ runs, selectedRunId, onSelect }: { runs: TrainingRun[]; selectedRunId?: string; onSelect: (id: string) => void }) {
  return (
    <section className="panel">
      <h2>Training Runs</h2>
      <table className="table">
        <thead>
          <tr><th>Run</th><th>Status</th><th>Algorithm</th><th>Episode</th><th>Best</th></tr>
        </thead>
        <tbody>
          {runs.length === 0 ? (
            <tr>
              <td colSpan={5}>No training runs yet. Start one from Training Control.</td>
            </tr>
          ) : (
            runs.map((run) => (
              <tr key={run.run_id} className={selectedRunId === run.run_id ? "selected-row" : ""} onClick={() => onSelect(run.run_id)}>
                <td>{run.run_id}</td>
                <td><AgentStatusBadge status={run.status} /></td>
                <td>{run.algorithm}</td>
                <td>{run.current_episode}/{run.episodes_target}</td>
                <td>{run.summary?.best_return?.toFixed?.(2) ?? "--"}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </section>
  );
}
