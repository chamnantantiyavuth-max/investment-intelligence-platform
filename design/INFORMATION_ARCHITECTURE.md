# Information Architecture — Investment Intelligence Platform

> **Phase E — ui-dashboard-workflow v4.0.0 · 2026-08-04 · FD #51 (A — Research Desk)**

## Principle

Smallest architecture that supports every approved decision (page-count discipline). No page per Bible §; no tabs per entity without a workflow; no settings page (nothing user-editable in V0).

## Navigation hierarchy

```
DASHBOARD                     — overview: attention + boundaries + change + next
ALPHA MOMENTUM                — momentum-first discovery
  ├─ Queue                    — theme-first research queue (ordered)
  ├─ Theme Card               — single-theme deep read (thesis/evidence/falsification)
  └─ Screener                 — approved criteria matrix
CLOSE SYSTEM                  — product radar (SYNTHETIC DEMO)
  └─ Radar                    — P1–P3 eligibility + 5-layer synthesis + conviction
FUNDAMENTAL                   — fundamental & opportunity intelligence (real data)
  ├─ Queue                    — company packages
  ├─ Company                  — moat / earnings quality / valuation context
  └─ Cheap & Quality          — cheap-quality vs trap
INSTITUTIONAL                 — 13F signals (real data)
  └─ Signals                  — conviction/action table + pagination
WEAK SIGNALS                  — anomalies + hypotheses (Experimental)
```

## Rules

- **Names describe user destinations, not internal modules** — no "api", "adapter", "pipeline" in nav.
- **Primary nav stable + compact:** 6 top-level items (Dashboard + 5 groups); secondary detail lives in drill-downs/panels, not new nav entries.
- **No tabs-as-process-steps:** Theme Card uses sections/tabs for dimensions/evidence/falsification — these are reading modes, not a workflow stepper.
- **Cross-page relationships:** Dashboard hero → Theme Card (evidence drill); Queue row → Theme Card; FO verdicts → Company detail; Screener row → candidate detail.
- **Progressive disclosure:** hero/lede (claim) → findings ledger (evidence summary) → deep-dive tier (evidence register, methodology) → methodology/footer (authority, advisory).
- **Mobile strategy:** single column; nav collapses to a compact bar; tables become stacked rows; border budget holds at 0–2.
- **Experimental separation:** Weak Signal surfaces carry EXPERIMENTAL label; never alter official filters/rankings (FD #27).

## Page-count justification (11 pages — no additions, no removals)

| Page | Justified by decision |
|---|---|
| Login | Auth boundary (FD #46) |
| Dashboard | Attention triage (overview rule) |
| AM Queue / Theme Card / Screener | AM spec §5.1–5.3 + screener objective (FD #49) |
| CS Radar | CS spec §2–5 |
| FO Queue / Company / Cheap & Quality | FO spec §3 (6 sub-domains) + FD #40 |
| Institutional | FD #42 + II follow-up |
| Weak Signal | FD #27 |

## Global vs local controls

- Global: nav, provenance legend, advisory footer, as-of/run stamp.
- Local: filters on Screener/II (server-side pagination II), sort on Queue, tab switch on Theme Card.
<!-- 2026-08-04 17:22 UTC+7 -->
