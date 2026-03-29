import React from "react";

export function RunComparisonView({ rows }: { rows: Array<{ run_id: string; episodes: number; best_return: number; latest_return: number; avg_last_10: number }> }) {
  return (
    <section className="panel">
      <h2>Run Comparison</h2>
      <table className="table">
        <thead><tr><th>Run</th><th>Episodes</th><th>Best Return</th><th>Latest</th><th>Avg Last 10</th></tr></thead>
        <tbody>
          {rows.length === 0 ? (
            <tr>
              <td colSpan={5}>Comparison is empty. Start or select runs first.</td>
            </tr>
          ) : (
            rows.map((r) => (
              <tr key={r.run_id}>
                <td>{r.run_id}</td>
                <td>{r.episodes}</td>
                <td>{r.best_return?.toFixed?.(2) ?? "--"}</td>
                <td>{r.latest_return?.toFixed?.(2) ?? "--"}</td>
                <td>{r.avg_last_10?.toFixed?.(2) ?? "--"}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </section>
  );
}
