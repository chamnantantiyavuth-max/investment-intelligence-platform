// Login page (FD #46 — single-user session auth gate; Research Desk v3.0, FD #51)
import { useState } from "react"
import { login } from "@/api/authClient"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { LangToggle } from "@/components/LangToggle"
import { useLang } from "@/i18n/LanguageContext"
import { translate } from "@/i18n/translations"

export default function LoginPage({ onSuccess }: { onSuccess: () => void }) {
  const { lang } = useLang()
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
      {/* Language toggle — top-right, available before auth */}
      <div className="absolute right-4 top-4">
        <LangToggle />
      </div>

      {/* Product intro — answers "what is this app" at first sight */}
      <div className="hidden flex-1 flex-col justify-center gap-8 border-r border-rule p-12 lg:flex">
        <div>
          <p className="text-[11px] font-bold uppercase tracking-[0.18em] text-primary">
            {translate("login.momentum", lang)}
          </p>
          <h1 className="mt-3 max-w-md font-display text-4xl font-bold leading-[1.12] tracking-[-0.01em] text-foreground">
            {translate("login.platform", lang)}
          </h1>
        </div>
        <div className="max-w-md space-y-4 text-sm leading-relaxed text-ink-2">
          <p className="text-foreground">
            {translate("login.decisiondesk", lang)}
          </p>
          <p>
            {translate("login.question", lang).split(":")[0]}:{" "}
            <span className="font-semibold text-foreground">{translate("login.question", lang).split(": ")[1] ?? ""}</span>
          </p>
          <div className="space-y-2 border-t border-rule pt-4">
            <p className="flex items-center gap-2">
              <span className="text-ink-3">—</span> {translate("login.advisory", lang)}
            </p>
            <p className="flex items-center gap-2">
              <span className="text-ink-3">—</span> {translate("login.portfolioBlind", lang)}
            </p>
            <p className="flex items-center gap-2">
              <span className="text-ink-3">—</span> {translate("login.dataLabeled", lang)}
            </p>
          </div>
        </div>
        <p className="font-mono text-[11px] text-ink-3">
          {translate("login.pillars", lang)}
        </p>
      </div>

      {/* Sign-in — one independent action = the page's single allowed outline */}
      <div className="flex flex-1 items-center justify-center p-6">
        <form onSubmit={submit} className="w-full max-w-sm space-y-4 rounded-md border border-rule bg-card p-6">
          <div>
            <h2 className="font-display text-xl font-bold text-foreground">{translate("login.title", lang)}</h2>
            <p className="mt-1 text-xs text-ink-2">{translate("login.subtitle", lang)}</p>
          </div>
          <div className="space-y-1.5">
            <label htmlFor="username" className="text-xs font-medium text-ink-2">
              {translate("login.username", lang)}
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
              {translate("login.password", lang)}
            </label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
            />
          </div>
          {error && <p className="text-sm text-negative">{translate("login.error", lang)}</p>}
          <Button type="submit" disabled={busy} className="w-full">
            {busy ? (lang === "th" ? "กำลังเข้าสู่ระบบ…" : "Signing in…") : translate("login.button", lang)}
          </Button>
        </form>
      </div>
    </div>
  )
}
