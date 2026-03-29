import React from "react";

import { AgentDecisionCard } from "../components/AgentDecisionCard";
import { AgentStatusBadge } from "../components/AgentStatusBadge";
import { ApplianceExplorer } from "../components/ApplianceExplorer";
import { ArtifactPanel } from "../components/ArtifactPanel";
import { CheckpointBrowser } from "../components/CheckpointBrowser";
import { CommunityOverview } from "../components/CommunityOverview";
import { EvaluationDashboard } from "../components/EvaluationDashboard";
import { ExplainabilityPanel } from "../components/ExplainabilityPanel";
import { HouseAgentDetail } from "../components/HouseAgentDetail";
import { LiveDeploymentBanner } from "../components/LiveDeploymentBanner";
import { PlaybackControls } from "../components/PlaybackControls";
import { PriceOverlayChart } from "../components/PriceOverlayChart";
import { ResourceLayer } from "../components/ResourceLayer";
import { ResourceTimeline } from "../components/ResourceTimeline";
import { RunComparisonView } from "../components/RunComparisonView";
import { RunResumeDialog } from "../components/RunResumeDialog";
import { ScenarioBuilder } from "../components/ScenarioBuilder";
import { TrainingControlPanel } from "../components/TrainingControlPanel";
import { TrainingDashboard } from "../components/TrainingDashboard";
import { TrainingRunTable } from "../components/TrainingRunTable";
import { useLiveChannel } from "../hooks/useLiveChannel";
import { apiGet, apiPost } from "../lib/api";
import { useAppState } from "../store/useAppState";
import type { CheckpointEvent, CommunitySnapshot, HouseDecision, HouseResourceResponse, RunMetric, TrainingRun } from "../types/domain";

export function AppShell() {
  const { houses, summary } = useAppState();
  const community = useLiveChannel<CommunitySnapshot>("community");
  const actions = useLiveChannel<{ actions: Array<{ house_id: string; action: string; reason: string; explanation?: { summary?: string; dominant_driver?: string } }> }>("actions");
  const trainingWs = useLiveChannel<{ run: TrainingRun }>("training_status");
  const metricWs = useLiveChannel<{ run_id: string; latest_metric?: RunMetric }>("training_metrics");

  const [appliances, setAppliances] = React.useState<Array<{ appliance_id: string; nominal_power_kw: number; interruptible: boolean }>>([]);
  const [trainingStatus, setTrainingStatus] = React.useState<Record<string, unknown>>({});
  const [runs, setRuns] = React.useState<TrainingRun[]>([]);
  const [selectedRunId, setSelectedRunId] = React.useState<string | undefined>(undefined);
  const [selectedRun, setSelectedRun] = React.useState<TrainingRun | undefined>(undefined);
  const [metrics, setMetrics] = React.useState<RunMetric[]>([]);
  const [checkpoints, setCheckpoints] = React.useState<CheckpointEvent[]>([]);
  const [comparison, setComparison] = React.useState<Array<{ run_id: string; episodes: number; best_return: number; latest_return: number; avg_last_10: number }>>([]);
  const [deployment, setDeployment] = React.useState<{ mode: string; message: string }>({ mode: "local-dev", message: "loading..." });
  const [artifacts, setArtifacts] = React.useState<{ models: Array<{ name: string; size_bytes: number }>; csv: Array<{ name: string; size_bytes: number }>; parquet: Array<{ name: string; size_bytes: number }> }>({ models: [], csv: [], parquet: [] });
  const [resourceData, setResourceData] = React.useState<HouseResourceResponse | null>(null);
  const [selectedHouse, setSelectedHouse] = React.useState<string>("H1");

  const refreshRuns = React.useCallback(() => {
    apiGet<{ runs: TrainingRun[] }>("/training/runs")
      .then((res) => {
        setRuns(res.runs);
        if (!selectedRunId && res.runs.length > 0) {
          setSelectedRunId(res.runs[0].run_id);
        }
      })
      .catch(() => setRuns([]));
  }, [selectedRunId]);

  React.useEffect(() => {
    apiGet<Array<{ appliance_id: string; nominal_power_kw: number; interruptible: boolean }>>("/appliances")
      .then(setAppliances)
      .catch(() => setAppliances([]));

    apiGet<Record<string, unknown>>("/training/status").then(setTrainingStatus).catch(() => setTrainingStatus({}));
    apiGet<{ mode: string; message: string }>("/deployment/status").then(setDeployment).catch(() => setDeployment({ mode: "unknown", message: "unavailable" }));

    apiGet<{ models: Array<{ name: string; size_bytes: number }> }>("/artifacts/models")
      .then((res) => setArtifacts((prev) => ({ ...prev, models: res.models })))
      .catch(() => undefined);

    apiGet<{ csv: Array<{ name: string; size_bytes: number }>; parquet: Array<{ name: string; size_bytes: number }> }>("/artifacts/results")
      .then((res) => setArtifacts((prev) => ({ ...prev, csv: res.csv, parquet: res.parquet })))
      .catch(() => undefined);

    refreshRuns();
    const timer = setInterval(refreshRuns, 4000);
    return () => clearInterval(timer);
  }, [refreshRuns]);

  React.useEffect(() => {
    if (!selectedRunId) return;
    apiGet<TrainingRun>(`/training/runs/${selectedRunId}`).then(setSelectedRun).catch(() => setSelectedRun(undefined));
    apiGet<{ metrics: RunMetric[] }>(`/training/runs/${selectedRunId}/metrics?limit=240`).then((x) => setMetrics(x.metrics)).catch(() => setMetrics([]));
    apiGet<{ checkpoints: CheckpointEvent[] }>(`/training/runs/${selectedRunId}/checkpoints`).then((x) => setCheckpoints(x.checkpoints)).catch(() => setCheckpoints([]));
  }, [selectedRunId, runs, metricWs, trainingWs]);

  React.useEffect(() => {
    const house = houses[0]?.house_id ?? "H1";
    setSelectedHouse((prev) => (houses.some((h) => h.house_id === prev) ? prev : house));
  }, [houses]);

  React.useEffect(() => {
    if (!selectedHouse) return;
    apiGet<HouseResourceResponse>(`/houses/${selectedHouse}/resources?limit=240`).then(setResourceData).catch(() => setResourceData(null));
  }, [selectedHouse, community]);

  React.useEffect(() => {
    if (runs.length === 0) {
      setComparison([]);
      return;
    }
    const runIds = runs.slice(0, 4).map((r) => r.run_id);
    apiPost<{ comparisons: Array<{ run_id: string; episodes: number; best_return: number; latest_return: number; avg_last_10: number }> }>("/training/compare", { run_ids: runIds })
      .then((x) => setComparison(x.comparisons))
      .catch(() => setComparison([]));
  }, [runs, metricWs]);

  const decisions: HouseDecision[] =
    actions?.actions?.map((x) => ({
      house_id: x.house_id,
      action: x.action,
      reason: x.reason,
      utility_score: 0,
      explanation: {
        summary: x.explanation?.summary ?? "Action selected by current policy",
        dominant_driver: x.explanation?.dominant_driver ?? x.reason,
        reward_terms: {},
      },
    })) ?? [];

  const loadPoints = (resourceData?.timeline ?? []).map((p) => ({ timestamp: p.timestamp, value: p.house_total_kw }));
  const pricePoints = (resourceData?.timeline ?? []).map((p) => ({ timestamp: p.timestamp, value: p.price ?? 0 }));

  return (
    <main className="layout">
      <header className="hero">
        <h1>HieraFlex</h1>
        <p>Hierarchical Flexibility Intelligence for Community Energy Trading</p>
        {trainingWs?.run && <p className="muted">Live worker: <AgentStatusBadge status={trainingWs.run.status} /></p>}
      </header>

      <LiveDeploymentBanner mode={deployment.mode} message={deployment.message} />
      <PlaybackControls />
      <ScenarioBuilder />

      <CommunityOverview snapshot={community} />
      <EvaluationDashboard summary={summary} />
      <TrainingControlPanel selectedRunId={selectedRunId} onStarted={refreshRuns} />
      <TrainingRunTable runs={runs} selectedRunId={selectedRunId} onSelect={setSelectedRunId} />
      <RunResumeDialog
        run={selectedRun}
        onResume={({ checkpointPath, extraEpisodes }) =>
          selectedRunId &&
          apiPost("/training/resume", { run_id: selectedRunId, checkpoint_path: checkpointPath, extra_episodes: extraEpisodes }).then(refreshRuns)
        }
      />
      <TrainingDashboard
        status={trainingStatus}
        run={selectedRun}
        metrics={metrics}
        latestMetric={metricWs?.latest_metric ?? metrics[metrics.length - 1]}
      />
      <RunComparisonView rows={comparison} />
      <CheckpointBrowser checkpoints={checkpoints} />

      <HouseAgentDetail decisions={decisions} />
      <ResourceLayer traces={[
        { label: "Mains", value: community?.community?.total_kw ?? 0 },
        { label: "Flexible", value: community?.community?.flexible_kw ?? 0 },
        { label: "Grid Exchange", value: community?.market?.matched_kwh ?? 0 },
      ]} />
      <section className="panel">
        <h2>House Selector</h2>
        <label>
          Active House
          <select value={selectedHouse} onChange={(e) => setSelectedHouse(e.target.value)}>
            {(houses.length ? houses : [{ house_id: "H1" }]).map((house) => (
              <option value={house.house_id} key={house.house_id}>
                {house.house_id}
              </option>
            ))}
          </select>
        </label>
      </section>

      <ResourceTimeline title={`House ${selectedHouse} Total Load`} points={loadPoints} />
      <PriceOverlayChart load={loadPoints} price={pricePoints} />
      <ApplianceExplorer appliances={appliances} />

      <ArtifactPanel models={artifacts.models} csv={artifacts.csv} parquet={artifacts.parquet} />
      <ExplainabilityPanel
        items={decisions.map((d) => ({
          house_id: d.house_id,
          summary: d.explanation.summary,
          driver: d.explanation.dominant_driver,
        }))}
      />
      <section className="panel">
        <h2>Decision Cards</h2>
        <div className="card-list">
          {decisions.map((d) => (
            <AgentDecisionCard key={d.house_id} title={d.house_id} action={d.action} reason={d.reason} />
          ))}
        </div>
      </section>
    </main>
  );
}
