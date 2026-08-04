# UI Direction — Research Desk (v3.0)

> **Phase H.2 — ui-dashboard-workflow v4.0.0 · 2026-08-04 · FD #51 direction A**

## Direction statement (concrete, not vague)

```text
Quiet institutional research desk. A financial newspaper of record for one reader.
Paper-white canvas, ink text, serif display headlines (FT-style), dense but airy ledgers,
hairline separators. Typography establishes hierarchy BEFORE containers.
Borderless-by-default across primary and secondary surfaces — no decorative full-perimeter borders.
Separators appear only where scanning requires them (table rows, masthead rules).
Maximum panel radius 4px. No uniform grid of contained metric cards. No hero banners,
no gradients, no glass, no glow. One muted accent (steel blue) + semantic sage/rose/amber.
Operational content appears immediately; the lead story is the attention triage, not a welcome mat.
Mono numerals (JetBrains Mono) for tickers, numbers, run stamps.
Every claim carries an evidence link; every number carries provenance (REAL/HYBRID/SYNTHETIC).
```

## Key composition rules

1. **One dominant focal region per page** — the lead story (hero) on Dashboard; the ledger on Queue/Screener; the judgment surface on Theme Card.
2. **Hierarchy order before outlines:** spacing → typography → alignment → position/proportion → grouping → restrained background tint → single-axis separator → full-perimeter outline as last resort.
3. **Ledger tables are the workhorse:** findings, queue, screener matrix, II signals, FO verdicts — aligned columns, mono numbers, hairline row separators, header rules.
4. **Tonal zones instead of cards:** subtle paper-2 tint (#F1F1EA) for secondary panels (CS summary, provenance rail) — no outline.
5. **Masthead:** double rule under brand (newspaper of record); small-caps nav; right-aligned mono run stamp.
6. **Provenance chips:** REAL (sage) / HYBRID (steel blue) / SYNTHETIC (amber) — text + color, never color alone (audit C3 fix: full state set).
7. **Advisory footer on every page** — no buy/sell/allocate, portfolio-blind, Constitution §23.8.1.
8. **Failure honesty:** error states say what failed + what's affected + retry; never coerce API failure to zero (C5).

## Anti-patterns (reject by default)

KPI card grids · icon-in-colored-square tiles · welcome heroes in operational pages · decorative gradients/glass/glow · pills on every label · equal-weight four-column layouts · charts to fill space · hidden tooltip-only context · green/red without meaning · fake "AI insights" panels without evidence · outlined Cards inside outlined panels · parent+child double outlines.

## Type system

| Role | Face | Size/weight |
|---|---|---|
| Display headline | Georgia / Source Serif 4 | 36–44px / 700 |
| Section headline | Georgia | 22px / 700 |
| Page title | Inter | 20px / 650 |
| Kicker / small-caps label | Inter | 10–11px / 700, letter-spacing 0.12em, uppercase |
| Body / supporting | Inter | 13–15px / 400 |
| Numeric data / tickers / stamps | JetBrains Mono | 11–14px |
| Table header | Inter | 10px uppercase |
| Lede | Inter | 16–17px / 400, ink-2 |

## Spacing rhythm

8px base. Control-internal 6–8 · related items 8–12 · components 16–24 · sections 32–44 · page 28–36. Hierarchy by spacing first, never by adding gaps arbitrarily.

## Border/radius/shadows

- Radius: 4px max (inputs 4px, panels 4px, chips 2px).
- Shadows: none (flat paper). Elevation via tint only.
- Borders: masthead double rule (2px ink), section rules (1px ink under h2), hairline row separators (1px rule). Full-perimeter outlines: only functional (login form; semantic error/synthetic banners are excluded by policy).
<!-- 2026-08-04 17:34 UTC+7 -->
