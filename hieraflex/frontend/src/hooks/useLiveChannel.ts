import { useEffect, useRef, useState } from "react";

import { wsUrl } from "../lib/api";

export function useLiveChannel<T>(channel: string) {
  const [latest, setLatest] = useState<T | null>(null);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const ws = new WebSocket(wsUrl(channel));
    wsRef.current = ws;
    ws.onopen = () => ws.send("subscribe");
    ws.onmessage = (ev) => {
      try {
        setLatest(JSON.parse(ev.data) as T);
      } catch {
        // ignore malformed payload
      }
    };
    return () => {
      ws.close();
      wsRef.current = null;
    };
  }, [channel]);

  return latest;
}
