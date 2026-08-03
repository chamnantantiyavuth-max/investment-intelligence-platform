// Login page (FD #46 — single-user session auth gate; FD #49 dark redesign)
import { useState } from "react"
import { login } from "@/api/authClient"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { TrendingUp, Shield, Building2 } from "lucide-react"

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
      {/* Product intro — answers "what is this app" at first sight (FD #49) */}
      <div className="hidden flex-1 flex-col justify-center gap-6 border-r border-border p-12 lg:flex">
        <div>
          <div className="flex items-center gap-2">
            <div className="flex size-9 items-center justify-center rounded-md bg-primary text-primary-foreground">
              <TrendingUp className="size-5" />
            </div>
            <span className="font-mono text-lg font-semibold text-foreground">IIP</span>
          </div>
          <p className="mt-1 text-sm text-muted-foreground">
            Investment Intelligence Platform
          </p>
        </div>
        <div className="max-w-md space-y-3 text-sm leading-relaxed text-muted-foreground">
          <p className="text-foreground">
            A decision-desk for opportunity discovery — it reduces the global investment search
            space while preserving evidence, uncertainty, and dissent.
          </p>
          <p>It answers one question: <span className="text-foreground">what deserves further investigation?</span></p>
          <div className="space-y-2 pt-1">
            <div className="flex items-center gap-2">
              <Shield className="size-4 text-info" />
              <span>Advisory only — no buy/sell/allocate. No broker connectivity.</span>
            </div>
            <div className="flex items-center gap-2">
              <Building2 className="size-4 text-info" />
              <span>Portfolio-blind: the system never sees your holdings (§23.8.1).</span>
            </div>
            <div className="flex items-center gap-2">
              <TrendingUp className="size-4 text-info" />
              <span>Evidence-first: every surface carries a real/synthetic provenance label.</span>
            </div>
          </div>
        </div>
        <p className="font-mono text-[11px] text-muted-foreground/70">
          Alpha Momentum · Close System · Fundamental &amp; Opportunity — one shared intelligence core
        </p>
      </div>

      {/* Sign-in */}
      <div className="flex flex-1 items-center justify-center p-6">
        <form onSubmit={submit} className="w-full max-w-sm space-y-4 rounded-md border border-border bg-card p-6">
          <div>
            <h1 className="font-mono text-lg font-semibold text-foreground">IIP — Sign in</h1>
            <p className="text-xs text-muted-foreground">Single-user loopback session (FD #47)</p>
          </div>
          <div className="space-y-1.5">
            <label htmlFor="username" className="text-xs font-medium text-muted-foreground">
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
            <label htmlFor="password" className="text-xs font-medium text-muted-foreground">
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
          {error && <p className="text-sm text-negative">Invalid credentials</p>}
          <Button type="submit" disabled={busy} className="w-full">
            {busy ? "Signing in…" : "Sign in"}
          </Button>
        </form>
      </div>
    </div>
  )
}
