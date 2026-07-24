# Design System: Investment Intelligence Platform

**Version:** 1.0 (Standardized — FD #39, 25 July 2026)
**Stack:** HTML/CSS + Jinja2
**Pattern:** Data-Dense Dashboard

## Color Tokens

| Token | Hex | Usage |
|---|---|---|
| `--bg-page` | `#f5f6f8` | Page background |
| `--bg-card` | `#ffffff` | Card/surface background |
| `--bg-sidebar` | `#0f1117` | Sidebar / dark header |
| `--text-primary` | `#1a1a2e` | Primary text |
| `--text-secondary` | `#6b7280` | Secondary/muted text |
| `--text-inverse` | `#ffffff` | Text on dark backgrounds |
| `--positive` | `#10b981` | Positive / gain (mint green) |
| `--negative` | `#ec4899` | Negative / loss (pink) |
| `--warning` | `#f59e0b` | Warning / caution (amber) |
| `--info` | `#3b82f6` | Info / neutral (blue) |
| `--border` | `#e5e7eb` | Card/table borders |
| `--border-strong` | `#d1d5db` | Strong borders |
| `--radius-sm` | `8px` | Small radius |
| `--radius-md` | `12px` | Card radius |
| `--radius-lg` | `16px` | Large radius |
| `--shadow-card` | `0 1px 3px rgba(0,0,0,0.06)` | Card shadow |

## Typography

| Token | Font | Usage |
|---|---|---|
| `--font-body` | `'Inter', system-ui, -apple-system, sans-serif` | All text |
| `--font-mono` | `'JetBrains Mono', 'Consolas', monospace` | Tickers, data |
| Base size | `14px` | Body |
| Line height | `1.6` | Body |

## Status Colors

| Status | Color | CSS Class |
|---|---|---|
| Positive / High / Confirmed | `#10b981` | `.positive`, `.badge-high` |
| Negative / Low / Invalidated | `#ec4899` | `.negative`, `.badge-low` |
| Warning / Moderate | `#f59e0b` | `.warning`, `.badge-moderate` |
| Info / Neutral | `#3b82f6` | `.info` |

## Components

- **Cards:** white bg, 12px radius, 1px `--border`, subtle shadow
- **Tables:** clean, zebra optional, hover highlight on rows
- **Badges:** pill-shaped (border-radius 20px), 11px font, semi-bold
- **Metric cards:** centered numbers, uppercase labels, min-width 110px
- **Headers:** dark sidebar (#0f1117) with white text
- **Buttons:** none in V0 — this is a display platform, not interactive

## Anti-Patterns (Avoid)

- Beige/warm/Claude-inspired palette — use grey-white system above
- Playfair Display / serif headlines — use Inter only
- Emoji as icons — use text labels or SVG
- Ornate design — data comes first
- Raw hex in components — use CSS variables

## Page Overrides

| Page | Override File |
|---|---|
| Alpha Momentum Queue | `pages/am-queue.md` |
| Alpha Momentum Theme Card | `pages/am-theme-card.md` |
| Close System Radar | `pages/cs-radar.md` |
