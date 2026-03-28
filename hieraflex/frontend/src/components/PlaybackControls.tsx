import React from "react";

import { API_BASE } from "../lib/api";

async function post(path: string, body?: unknown) {
  await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
}

export function PlaybackControls() {
  return (
    <section className="panel controls">
      <h2>Playback Controls</h2>
      <div className="button-row">
        <button onClick={() => post("/simulation/start", { scenario_id: "demo_week", start_index: 0, end_index: 288, replay_speed: 60 })}>Start</button>
        <button onClick={() => post("/simulation/pause")}>Pause</button>
        <button onClick={() => post("/simulation/reset")}>Reset</button>
      </div>
    </section>
  );
}
