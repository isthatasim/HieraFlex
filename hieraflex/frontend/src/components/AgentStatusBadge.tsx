import React from "react";

export function AgentStatusBadge({ status }: { status: string }) {
  const normalized = status.toLowerCase();
  const cls =
    normalized.includes("running")
      ? "badge running"
      : normalized.includes("completed")
        ? "badge completed"
        : normalized.includes("failed")
          ? "badge failed"
          : "badge";
  return <span className={cls}>{status}</span>;
}
