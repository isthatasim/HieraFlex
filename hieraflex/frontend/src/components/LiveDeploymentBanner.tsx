import React from "react";

export function LiveDeploymentBanner({ mode, message }: { mode: string; message: string }) {
  return (
    <section className="panel banner">
      <h2>Live Website Mode</h2>
      <p><strong>{mode}</strong> - {message}</p>
      <small>Public viewers can stay in replay/demo mode while training runs in backend workers.</small>
    </section>
  );
}
