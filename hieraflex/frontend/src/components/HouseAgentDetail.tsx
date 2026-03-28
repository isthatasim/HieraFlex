import React from "react";

import type { HouseDecision } from "../types/domain";

type Props = {
  decisions: HouseDecision[];
};

export function HouseAgentDetail({ decisions }: Props) {
  return (
    <section className="panel">
      <h2>House Agent Detail</h2>
      <div className="card-list">
        {decisions.map((d) => (
          <article key={d.house_id} className="card">
            <header>
              <h3>{d.house_id}</h3>
              <span>{d.action}</span>
            </header>
            <p>{d.explanation?.summary ?? "No explanation available."}</p>
            <small>Driver: {d.reason}</small>
          </article>
        ))}
      </div>
    </section>
  );
}
