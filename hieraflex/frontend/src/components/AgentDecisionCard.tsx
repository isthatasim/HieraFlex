import React from "react";

export function AgentDecisionCard({ title, action, reason }: { title: string; action: string; reason: string }) {
  return (
    <article className="card decision">
      <h3>{title}</h3>
      <strong>{action}</strong>
      <p>{reason}</p>
    </article>
  );
}
