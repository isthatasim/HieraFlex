const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) {
    throw new Error(`API error ${res.status}`);
  }
  return (await res.json()) as T;
}

export function wsUrl(channel: string): string {
  const host = API_BASE.replace("http", "ws");
  return `${host}/ws/${channel}`;
}

export { API_BASE };
