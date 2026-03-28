import React from "react";

type Props = {
  traces: Array<{ label: string; value: number }>;
};

export function ResourceLayer({ traces }: Props) {
  return (
    <section className="panel">
      <h2>Resource Layer</h2>
      <ul className="trace-list">
        {traces.map((t) => (
          <li key={t.label}><span>{t.label}</span><strong>{t.value.toFixed(2)}</strong></li>
        ))}
      </ul>
    </section>
  );
}
