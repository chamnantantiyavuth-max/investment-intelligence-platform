# Design System: Investment Intelligence Platform

**Version:** 3.0 — Research Desk (FD #51 direction A, 4 August 2026)
**Stack:** React + Vite + TypeScript + Tailwind CSS v4 (frontend/); design tokens below apply across all surfaces
**Pattern:** Research Desk — quiet institutional research workspace: paper canvas, ink text, serif display headlines (FT-style), dense ledgers, hairline separators, one muted steel-blue accent. Typography establishes hierarchy before containers; borderless-by-default (0–2 full-perimeter outlines per viewport).
**Canonical tokens:** `frontend/src/index.css` (`@theme` — Tailwind v4 semantic `--color-*` set; audit C1 fix) + `design/UI_TOKENS.md` + `design/UI_DIRECTION.md`. Supersedes v2.1 Light Editorial (retired by FD #51).

## Color Tokens (HSL — mapped in frontend/src/index.css :root)

| Token | HSL | Hex | Usage |
|---|---|---|---|
| `--bg-page` | `220 23% 97%` | `#F7F8FA` | Page background |
| `--bg-card` | `0 0% 100%` | `#FFFFFF` | Card/panel surface |
| `--bg-elevated` | `220 23% 95%` | `#EFF1F5` | Tonal panel / hover surface |
| `--bg-sidebar` | `0 0% 100%` | `#FFFFFF` | Sidebar (border-right separates) |
| `--text-primary` | `221 27% 12%` | `#161B26` | Ink text |
| `--text-secondary` | `217 13% 40%` | `#5A6474` | Secondary/muted text |
| `--positive` | `160 71% 32%` | `#178A63` | Positive / gain (deep sage) |
| `--negative` | `338 48% 54%` | `#C2527B` | Negative / loss (deep muted pink) |
| `--warning` | `38 71% 40%` | `#B07A1E` | Warning / caution (deep amber) |
| `--info` | `213 42% 50%` | `#4A7BB5` | Info / neutral (steel blue) |
| `--border` | `220 19% 91%` | `#E3E6EC` | Hairline borders (deep tier only) |
| `--radius` | — | `6px` | Base radius (dense); hero/findings use `rounded-2xl` |

## Typography

| Token | Font | Usage |
|---|---|---|
| `--font-body` | `'Inter', system-ui, -apple-system, sans-serif` | All text |
| `--font-mono` | `'JetBrains Mono', 'Consolas', monospace` | Tickers, numbers, page titles |
| Base size | `14px` | Body |
| Display scale | `2.75rem` hero / `2rem` finding value / `1.25rem` finding headline | Editorial hierarchy |
| Kickers | `11px` uppercase, `0.16em` tracking | Section/finding labels |

## Status Colors (display-only mapping — never a rule)

| Status | Tone |
|---|---|
| Emerging / Expansion / Approved / Active Monitoring / Maximum / High / Confirmed / NEW / ADD / Wide / Deep / Stable | `positive` |
| Deteriorating / Crowded / Late Stage / Rejected / EXIT / COSMETIC / Trap / Narrowing / Shallow / None | `negative` |
| Under Human Review / Moderate / Dormant / REDUCE / Watch / Medium | `warning` |
| Experimental / Formation / Detected / MAINTAIN / Unknown | `info` |
| Everything else | `muted` |

## Components

- **HeroInsight:** the single most interesting thing on the page — kicker + headline + big mono display + sub + provenance chips. Tonal fill (6–7% accent), no border.
- **FindingCard:** discovery panels — kicker dot + kicker + headline + display value + why-it-matters. Featured variant spans 2 columns. Tonal fill, no border.
- **Reference tier:** engine provenance, matrices, tables — quieter: `bg-elevated/50`, small caps labels; hairline borders allowed here only.
- **Provenance chips:** mandatory on every surface — `REAL · source · as_of` (positive) vs `SYNTHETIC` (warning).
- **StatusBadge:** pill, 11px, accent-tinted fill, no invented semantics (display-only tone mapping).
- **ExplainPanel:** collapsible methodology with spec references. **AdvisoryFooter:** every page ends advisory-only + portfolio-blind. **StalenessBanner:** AM ≤7d / FO ≤30d / II ≤120d (FD #47 D3).

## Anti-Patterns (Avoid)

- Neon/bright accents (FD #49) — all accents muted institutional, light-contrast values
- Dark-mode default — light editorial is the only theme (v2.1)
- Uniform bordered card grids — tonal panels + typographic hierarchy instead
- Emoji as icons — lucide-react SVG only
- Raw hex in components — use tokens/theme colors
- Faux composite scores — the four quality dimensions stay separate (Constitution §10, §13)
- Invented thresholds in the screener — criteria come from the approved spec only

## Page Overrides

| Page | Override File |
|---|---|
| Alpha Momentum Queue | `pages/am-queue.md` |
| Alpha Momentum Theme Card | `pages/am-theme-card.md` |
| Close System Radar | `pages/cs-radar.md` |
<!-- 2026-08-04 02:10 UTC+7 -->
