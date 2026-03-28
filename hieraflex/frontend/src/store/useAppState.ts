import { useEffect, useMemo, useState } from "react";

import { apiGet } from "../lib/api";
import type { CommunitySnapshot } from "../types/domain";

export function useAppState() {
  const [houses, setHouses] = useState<Array<{ house_id: string }>>([]);
  const [summary, setSummary] = useState<Record<string, unknown>>({});

  useEffect(() => {
    apiGet<Array<{ house_id: string }>>("/houses").then(setHouses).catch(() => setHouses([]));
    apiGet<Record<string, unknown>>("/results/summary").then(setSummary).catch(() => setSummary({}));
  }, []);

  const houseIds = useMemo(() => houses.map((x) => x.house_id), [houses]);
  return { houses, houseIds, summary };
}

export type { CommunitySnapshot };
