import React from "react";

export function TrainingDashboard({ status }: { status: Record<string, unknown> }) {
  return (
    <section className="panel">
      <h2>Training Dashboard</h2>
      <pre>{JSON.stringify(status, null, 2)}</pre>
    </section>
  );
}
