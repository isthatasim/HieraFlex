import React from "react";

export function PriceOverlayChart({
  load,
  price,
}: {
  load: Array<{ timestamp: string; value: number }>;
  price: Array<{ timestamp: string; value: number }>;
}) {
  const width = 340;
  const height = 120;
  const maxLoad = Math.max(1, ...load.map((p) => p.value));
  const maxPrice = Math.max(1, ...price.map((p) => p.value));

  const toPath = (arr: Array<{ value: number }>, max: number) =>
    arr
      .map((p, i) => {
        const x = (i / Math.max(1, arr.length - 1)) * width;
        const y = height - (p.value / max) * height;
        return `${i === 0 ? "M" : "L"}${x},${y}`;
      })
      .join(" ");

  return (
    <section className="panel">
      <h2>Load/Price Overlay</h2>
      <svg viewBox={`0 0 ${width} ${height}`} className="chart-svg">
        <path d={toPath(load, maxLoad)} fill="none" stroke="var(--brand)" strokeWidth="2" />
        <path d={toPath(price, maxPrice)} fill="none" stroke="var(--accent)" strokeWidth="2" strokeDasharray="4 3" />
      </svg>
    </section>
  );
}
