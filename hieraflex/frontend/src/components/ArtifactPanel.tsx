import React from "react";

export function ArtifactPanel({
  models,
  csv,
  parquet,
}: {
  models: Array<{ name: string; size_bytes: number }>;
  csv: Array<{ name: string; size_bytes: number }>;
  parquet: Array<{ name: string; size_bytes: number }>;
}) {
  return (
    <section className="panel">
      <h2>Artifacts</h2>
      <p className="muted">Models: {models.length} | CSV: {csv.length} | Parquet: {parquet.length}</p>
      <ul className="trace-list">
        {models.length === 0 ? (
          <li><span>No model artifacts yet</span><strong>--</strong></li>
        ) : (
          models.slice(0, 5).map((m) => (
            <li key={m.name}><span>{m.name}</span><strong>{Math.round(m.size_bytes / 1024)} KB</strong></li>
          ))
        )}
      </ul>
    </section>
  );
}
