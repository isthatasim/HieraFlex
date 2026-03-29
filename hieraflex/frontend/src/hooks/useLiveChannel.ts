import { useEffect, useRef, useState } from "react";

import { wsUrl } from "../lib/api";

export function useLiveChannel<T>(channel: string) {
  const [latest, setLatest] = useState<T | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const retryRef = useRef<number | null>(null);

  useEffect(() => {
    let closed = false;

    const connect = () => {
      if (closed) return;
      const ws = new WebSocket(wsUrl(channel));
      wsRef.current = ws;

      ws.onopen = () => {
        ws.send("subscribe");
      };

      ws.onmessage = (ev) => {
        try {
          setLatest(JSON.parse(ev.data) as T);
        } catch {
          // ignore malformed payload
        }
      };

      ws.onclose = () => {
        wsRef.current = null;
        if (!closed) {
          retryRef.current = window.setTimeout(connect, 1500);
        }
      };

      ws.onerror = () => {
        ws.close();
      };
    };

    connect();

    return () => {
      closed = true;
      if (retryRef.current) {
        window.clearTimeout(retryRef.current);
      }
      wsRef.current?.close();
      wsRef.current = null;
    };
  }, [channel]);

  return latest;
}
