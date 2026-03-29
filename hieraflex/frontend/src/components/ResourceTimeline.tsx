import React from "react";

export function ResourceTimeline({ points, title }: { points: Array<{ timestamp: string; value: number }>; title: string }) {
  const max = Math.max(1, ...points.map((p) => p.value));
  const width = 340;
  const height = 120;
  const path = points
    .map((p, i) => {
      const x = (i / Math.max(1, points.length - 1)) * width;
      const y = height - (p.value / max) * height;
      return `${i === 0 ? "M" : "L"}${x},${y}`;
    })
    .join(" ");

  return (
    <section className="panel">
      <h2>{title}</h2>
      <svg viewBox={`0 0 ${width} ${height}`} className="chart-svg">
        <path d={path} fill="none" stroke="var(--accent)" strokeWidth="2" />
      </svg>
    </section>
  );
}
