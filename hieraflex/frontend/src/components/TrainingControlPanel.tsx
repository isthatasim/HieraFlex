import React from "react";

import { apiPost } from "../lib/api";

type Props = {
  selectedRunId?: string;
  onStarted: () => void;
};

export function TrainingControlPanel({ selectedRunId, onStarted }: Props) {
  const [algorithm, setAlgorithm] = React.useState("ppo_single");
  const [configPath, setConfigPath] = React.useState("experiments/configs/single_house.yaml");
  const [scenario, setScenario] = React.useState("demo_week");
  const [episodes, setEpisodes] = React.useState(120);
  const [seed, setSeed] = React.useState(42);
  const [priceMode, setPriceMode] = React.useState("real_time");
  const [housesCsv, setHousesCsv] = React.useState("H1,H2");
  const [checkpointInterval, setCheckpointInterval] = React.useState(5);
  const [evalInterval, setEvalInterval] = React.useState(10);
  const [message, setMessage] = React.useState<string>("");

  async function start() {
    try {
      await apiPost("/training/start", {
        algorithm,
        config_path: configPath,
        scenario_id: scenario,
        episodes,
        seed,
        checkpoint_interval: checkpointInterval,
        eval_interval: evalInterval,
        price_mode: priceMode,
        houses: housesCsv.split(",").map((x) => x.trim()).filter(Boolean),
      });
      setMessage("Training started.");
      onStarted();
    } catch (err) {
      setMessage(String(err));
    }
  }

  async function stop() {
    if (!selectedRunId) return;
    try {
      await apiPost("/training/stop", { run_id: selectedRunId });
      setMessage(`Stop requested for ${selectedRunId}.`);
      onStarted();
    } catch (err) {
      setMessage(String(err));
    }
  }

  async function resume() {
    if (!selectedRunId) return;
    try {
      await apiPost("/training/resume", { run_id: selectedRunId, extra_episodes: 80 });
      setMessage(`Resumed ${selectedRunId}.`);
      onStarted();
    } catch (err) {
      setMessage(String(err));
    }
  }

  return (
    <section className="panel">
      <h2>Training Control</h2>
      <div className="form-grid">
        <label>Algorithm<input value={algorithm} onChange={(e) => setAlgorithm(e.target.value)} /></label>
        <label>Config<input value={configPath} onChange={(e) => setConfigPath(e.target.value)} /></label>
        <label>Scenario<input value={scenario} onChange={(e) => setScenario(e.target.value)} /></label>
        <label>Episodes<input type="number" value={episodes} onChange={(e) => setEpisodes(Number(e.target.value))} /></label>
        <label>Seed<input type="number" value={seed} onChange={(e) => setSeed(Number(e.target.value))} /></label>
        <label>Price Mode<input value={priceMode} onChange={(e) => setPriceMode(e.target.value)} /></label>
        <label>Houses (CSV)<input value={housesCsv} onChange={(e) => setHousesCsv(e.target.value)} /></label>
        <label>Checkpoint Interval<input type="number" value={checkpointInterval} onChange={(e) => setCheckpointInterval(Number(e.target.value))} /></label>
        <label>Eval Interval<input type="number" value={evalInterval} onChange={(e) => setEvalInterval(Number(e.target.value))} /></label>
      </div>
      <div className="button-row">
        <button onClick={start}>Start</button>
        <button onClick={resume} disabled={!selectedRunId}>Resume</button>
        <button onClick={stop} disabled={!selectedRunId}>Stop</button>
      </div>
      {message && <p className="muted">{message}</p>}
    </section>
  );
}
