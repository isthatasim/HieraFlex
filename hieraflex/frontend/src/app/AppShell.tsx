import React from "react";

import { AgentDecisionCard } from "../components/AgentDecisionCard";
import { ApplianceExplorer } from "../components/ApplianceExplorer";
import { CommunityOverview } from "../components/CommunityOverview";
import { EvaluationDashboard } from "../components/EvaluationDashboard";
import { ExplainabilityPanel } from "../components/ExplainabilityPanel";
import { HouseAgentDetail } from "../components/HouseAgentDetail";
import { PlaybackControls } from "../components/PlaybackControls";
import { ResourceLayer } from "../components/ResourceLayer";
import { ScenarioBuilder } from "../components/ScenarioBuilder";
import { TrainingDashboard } from "../components/TrainingDashboard";
import { useLiveChannel } from "../hooks/useLiveChannel";
import { apiGet } from "../lib/api";
import { useAppState } from "../store/useAppState";
import type { CommunitySnapshot, HouseDecision } from "../types/domain";

export function AppShell() {
  const { summary } = useAppState();
  const community = useLiveChannel<CommunitySnapshot>("community");
  const actions = useLiveChannel<{ actions: Array<{ house_id: string; action: string; reason: string; explanation?: { summary?: string; dominant_driver?: string } }> }>("actions");

  const [appliances, setAppliances] = React.useState<Array<{ appliance_id: string; nominal_power_kw: number; interruptible: boolean }>>([]);
  const [training, setTraining] = React.useState<Record<string, unknown>>({});

  React.useEffect(() => {
    apiGet<Array<{ appliance_id: string; nominal_power_kw: number; interruptible: boolean }>>("/appliances")
      .then(setAppliances)
      .catch(() => setAppliances([]));
    apiGet<Record<string, unknown>>("/training/status").then(setTraining).catch(() => setTraining({}));
  }, []);

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

  return (
    <main className="layout">
      <header className="hero">
        <h1>HieraFlex</h1>
        <p>Hierarchical Flexibility Intelligence for Community Energy Trading</p>
      </header>

      <PlaybackControls />
      <ScenarioBuilder />
      <CommunityOverview snapshot={community} />
      <EvaluationDashboard summary={summary} />
      <HouseAgentDetail decisions={decisions} />
      <ResourceLayer traces={[
        { label: "Mains", value: community?.community.total_kw ?? 0 },
        { label: "Flexible", value: community?.community.flexible_kw ?? 0 },
        { label: "Grid Exchange", value: community?.market.matched_kwh ?? 0 },
      ]} />
      <ApplianceExplorer appliances={appliances} />
      <TrainingDashboard status={training} />
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
