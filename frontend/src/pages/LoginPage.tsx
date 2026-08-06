// Login page (FD #46 — single-user session auth gate; Research Desk v3.0, FD #51)
import { useState } from "react"
import { login } from "@/api/authClient"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

export default function LoginPage({ onSuccess }: { onSuccess: () => void }) {
  const [username, setUsername] = useState("founder")
  const [password, setPassword] = useState("")
  const [error, setError] = useState(false)
  const [busy, setBusy] = useState(false)

  async function submit(e: React.FormEvent) {
    e.preventDefault()
    setBusy(true)
    setError(false)
    const ok = await login(username, password)
    setBusy(false)
    if (ok) onSuccess()
    else setError(true)
  }

  return (
    <div className="flex min-h-screen bg-background">
      {/* Product intro — answers "what is this app" at first sight */}
      <div className="hidden flex-1 flex-col justify-center gap-8 border-r border-rule p-12 lg:flex">
        <div>
          <p className="text-[11px] font-bold uppercase tracking-[0.18em] text-primary">
            Momentum-first opportunity discovery
          </p>
          <h1 className="mt-3 max-w-md font-display text-4xl font-bold leading-[1.12] tracking-[-0.01em] text-foreground">
            The Investment Intelligence Platform
          </h1>
        </div>
        <div className="max-w-md space-y-4 text-sm leading-relaxed text-ink-2">
          <p className="text-foreground">
            A decision-desk that reduces the global investment search space while preserving
            evidence, uncertainty, and dissent.
          </p>
          <p>
            It answers one question:{" "}
            <span className="font-semibold text-foreground">what deserves further investigation?</span>
          </p>
          <div className="space-y-2 border-t border-rule pt-4">
            <p className="flex items-center gap-2">
              <span className="text-ink-3">—</span> Advisory only — no buy/sell/allocate. No broker connectivity.
            </p>
            <p className="flex items-center gap-2">
              <span className="text-ink-3">—</span> Portfolio-blind: the system never sees your holdings.
            </p>
            <p className="flex items-center gap-2">
              <span className="text-ink-3">—</span> Data is labeled real, hybrid, or synthetic on every page.
            </p>
          </div>
        </div>
        <p className="font-mono text-[11px] text-ink-3">
          Alpha Momentum · Close System · Fundamental &amp; Opportunity — one shared intelligence core
        </p>
      </div>

      {/* Sign-in — one independent action = the page's single allowed outline */}
      <div className="flex flex-1 items-center justify-center p-6">
        <form onSubmit={submit} className="w-full max-w-sm space-y-4 rounded-md border border-rule bg-card p-6">
          <div>
            <h2 className="font-display text-xl font-bold text-foreground">Sign in</h2>
            <p className="mt-1 text-xs text-ink-2">Private research workspace — advisory intelligence, not advice.</p>
          </div>
          <div className="space-y-1.5">
            <label htmlFor="username" className="text-xs font-medium text-ink-2">
              Username
            </label>
            <Input
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              autoComplete="username"
            />
          </div>
          <div className="space-y-1.5">
            <label htmlFor="password" className="text-xs font-medium text-ink-2">
              Password
            </label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
            />
          </div>
          {error && <p className="text-sm text-negative">Invalid credentials — try again.</p>}
          <Button type="submit" disabled={busy} className="w-full">
            {busy ? "Signing in…" : "Sign in"}
          </Button>
        </form>
      </div>
    </div>
  )
}
