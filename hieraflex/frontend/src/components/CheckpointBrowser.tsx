import React from "react";

import type { CheckpointEvent } from "../types/domain";

export function CheckpointBrowser({ checkpoints }: { checkpoints: CheckpointEvent[] }) {
  return (
    <section className="panel">
      <h2>Checkpoint Browser</h2>
      <ul className="trace-list">
        {checkpoints.length === 0 ? (
          <li><span>No checkpoints yet</span><strong>--</strong></li>
        ) : (
          checkpoints.map((cp) => (
            <li key={`${cp.checkpoint_path}-${cp.episode}`}>
              <span>Ep {cp.episode} {cp.is_best ? "(Best)" : ""}</span>
              <strong>{cp.score.toFixed(2)}</strong>
            </li>
          ))
        )}
      </ul>
    </section>
  );
}
