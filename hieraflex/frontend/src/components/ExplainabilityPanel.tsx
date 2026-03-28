import React from "react";

export function ExplainabilityPanel({ items }: { items: Array<{ house_id: string; summary: string; driver: string }> }) {
  return (
    <section className="panel">
      <h2>Explainability</h2>
      {items.length === 0 && <p>No decisions yet. Start replay to inspect action reasons.</p>}
      {items.map((i) => (
        <article key={i.house_id} className="card">
          <h3>{i.house_id}</h3>
          <p>{i.summary}</p>
          <small>Triggered by: {i.driver}</small>
        </article>
      ))}
    </section>
  );
}
