export type CommunitySnapshot = {
  timestamp: string;
  community: {
    total_kw: number;
    flexible_kw: number;
    coordination_signal: number;
    congestion: boolean;
  };
  market: {
    local_clearing_price: number;
    matched_kwh: number;
    fairness_penalty: number;
    trades: Array<Record<string, unknown>>;
  };
};

export type HouseDecision = {
  house_id: string;
  action: string;
  reason: string;
  utility_score: number;
  explanation: {
    summary: string;
    dominant_driver: string;
    reward_terms: Record<string, number>;
  };
};

export type TrainingRun = {
  run_id: string;
  algorithm: string;
  status: string;
  scenario_id: string;
  config_path: string;
  created_at?: string;
  started_at?: string;
  ended_at?: string;
  current_episode: number;
  episodes_target: number;
  latest_checkpoint?: string;
  best_checkpoint?: string;
  summary?: {
    latest_return?: number;
    best_return?: number;
    avg_last_10?: number;
  };
};

export type RunMetric = {
  timestamp: string;
  episode: number;
  episode_return: number;
  energy_cost: number;
  peak_proxy: number;
  comfort_penalty: number;
  fairness_penalty?: number;
  loss?: number;
  steps?: number;
};

export type CheckpointEvent = {
  timestamp?: string;
  run_id: string;
  episode: number;
  checkpoint_path: string;
  score: number;
  is_best: boolean;
};

export type HouseResourceResponse = {
  house_id: string;
  timeline: Array<{ timestamp: string; house_total_kw: number; price: number }>;
  appliances: Array<{
    appliance_id: string;
    nominal_kw: number;
    series: Array<{ timestamp: string; power_kw: number; state: string }>;
  }>;
};
