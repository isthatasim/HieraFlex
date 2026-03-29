const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) {
    throw new Error(`API error ${res.status}`);
  }
  return (await res.json()) as T;
}

export async function apiPost<T>(path: string, body?: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) {
    const message = await res.text();
    throw new Error(message || `API error ${res.status}`);
  }
  return (await res.json()) as T;
}

export function wsUrl(channel: string): string {
  const host = API_BASE.replace("http", "ws");
  return `${host}/ws/${channel}`;
}

export { API_BASE };
