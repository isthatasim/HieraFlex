import React from "react";

type Item = { appliance_id: string; nominal_power_kw: number; interruptible: boolean; flexibility_flag?: boolean };

export function ApplianceExplorer({ appliances }: { appliances: Item[] }) {
  return (
    <section className="panel">
      <h2>Appliance Explorer</h2>
      <table className="table">
        <thead><tr><th>Appliance</th><th>Power (kW)</th><th>Interruptible</th></tr></thead>
        <tbody>
          {appliances.map((a) => (
            <tr key={a.appliance_id}><td>{a.appliance_id}</td><td>{a.nominal_power_kw.toFixed(2)}</td><td>{a.interruptible ? "Yes" : "No"}</td></tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
