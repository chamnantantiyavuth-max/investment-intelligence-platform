// Insight derivation helpers — display-layer only. Every value maps to a real
// pipeline field; ranking is presentation ordering, never an investment rule.
import type { ThemeWithCandidates } from "@/types/am"

export interface RankedCandidate {
  ticker: string
  themeId: string
  themeName: string
  lifecycle: string
  conviction: string
  researchState: string
  rs: string
  trend: string
  breakout: string
  base: string
  whyNow: string
}

const CONVICTION: Record<string, number> = { Maximum: 0, High: 1, Moderate: 2, Low: 3, Minimal: 4 }
const BREAKOUT: Record<string, number> = { "In Progress": 0, Near: 1, Far: 2, None: 3 }
const RS: Record<string, number> = { Leading: 0, Neutral: 1, Lagging: 2 }

/** Rank candidates: conviction → breakout proximity → relative strength. */
export function rankCandidates(themes: ThemeWithCandidates[]): RankedCandidate[] {
  return themes
    .flatMap((t) =>
      (t.candidates ?? []).map((c) => ({
        ticker: c.ticker,
        themeId: t.theme.id,
        themeName: t.theme.name,
        lifecycle: t.theme.lifecycle,
        conviction: c.conviction_level,
        researchState: c.research_state,
        rs: c.candidate_quality.relative_strength,
        trend: c.candidate_quality.trend_quality,
        breakout: c.entry_readiness.breakout_proximity,
        base: c.entry_readiness.base_quality,
        whyNow: t.theme.why_now,
      }))
    )
    .sort(
      (a, b) =>
        (CONVICTION[a.conviction] ?? 5) - (CONVICTION[b.conviction] ?? 5) ||
        (BREAKOUT[a.breakout] ?? 9) - (BREAKOUT[b.breakout] ?? 9) ||
        (RS[a.rs] ?? 9) - (RS[b.rs] ?? 9)
    )
}

export function lifecycleCounts(themes: ThemeWithCandidates[]): [string, number][] {
  const m = new Map<string, number>()
  for (const t of themes) m.set(t.theme.lifecycle, (m.get(t.theme.lifecycle) ?? 0) + 1)
  return [...m.entries()].sort((a, b) => b[1] - a[1])
}

export function leadershipCount(themes: ThemeWithCandidates[]): number {
  return themes.filter((t) => /emerging|expansion/i.test(t.theme.lifecycle)).length
}
