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
