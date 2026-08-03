// Auth API client (FD #46 — single-user session login)
const BASE = "/api";

export async function login(username: string, password: string): Promise<boolean> {
  const res = await fetch(`${BASE}/auth/login`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  return res.ok;
}

export async function logout(): Promise<void> {
  await fetch(`${BASE}/auth/logout`, { method: "POST", credentials: "include" });
}

export async function authStatus(): Promise<boolean> {
  try {
    const res = await fetch(`${BASE}/auth/status`, { credentials: "include" });
    if (!res.ok) return false;
    const body = await res.json();
    return body.authenticated === true;
  } catch {
    return false;
  }
}
