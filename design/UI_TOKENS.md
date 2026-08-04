# UI Tokens — Research Desk (v3.0)

> **Phase H.2 — ui-dashboard-workflow v4.0.0 · 2026-08-04 · FD #51 direction A**
> Semantic tokens only (Tailwind v4 `@theme inline` mapping required — audit C1: prior build had no `--color-*` bridge).

## Color

| Token | Value | Usage |
|---|---|---|
| `--bg-page` | `#FAFAF7` | Page canvas (paper) |
| `--bg-panel` | `#F1F1EA` | Tonal secondary panel (no outline) |
| `--bg-input` | `#FFFFFF` | Input surface |
| `--ink` | `#1A1C1E` | Primary text (near-black) |
| `--ink-2` | `#5A5E63` | Secondary text |
| `--ink-3` | `#8A8E93` | Tertiary/meta text |
| `--rule` | `#DDDED6` | Hairline separators |
| `--accent` | `#1F4E79` | Steel blue — links, kickers, active nav, HYBRID provenance |
| `--positive` | `#2E7D5B` | Positive / REAL provenance (sage) |
| `--negative` | `#A34A4A` | Negative / loss (muted rose) |
| `--warning` | `#8A6D1F` | Warning / SYNTHETIC provenance (amber) |
| `--focus` | `#1F4E79` | Focus ring (accent, 2px) |

**Semantic pairs (Tailwind bridge — MUST map):** `--color-bg-page`, `--color-bg-panel`, `--color-bg-input`, `--color-ink`, `--color-ink-2`, `--color-ink-3`, `--color-rule`, `--color-accent`, `--color-positive`, `--color-negative`, `--color-warning`, `--color-focus`, plus foreground pairs where used (`--color-accent-foreground` etc.).

## Typography

| Token | Value |
|---|---|
| `--font-display` | Georgia, 'Times New Roman', serif |
| `--font-sans` | 'Inter', system-ui, -apple-system, sans-serif |
| `--font-mono` | 'JetBrains Mono', 'Consolas', monospace |
| `--text-hero` | 40px / 1.12 / 700 (display) |
| `--text-h2` | 22px / 700 (display) |
| `--text-lede` | 16px / 1.6 |
| `--text-body` | 14px / 1.5 |
| `--text-meta` | 11px / uppercase / 0.12em |
| `--text-num` | 13px mono |

## Spacing / radius / elevation

| Token | Value |
|---|---|
| `--space-1..8` | 4/8/12/16/24/32/44/56 px |
| `--radius` | 4px (inputs/panels), 2px (chips) |
| `--shadow` | none (flat paper) |

## Status mapping

| Semantic | Color | Badge example |
|---|---|---|
| Positive / REAL | sage `#2E7D5B` | "REAL EOD" |
| Hybrid | steel blue `#1F4E79` | "HYBRID evidence" |
| Synthetic / demo | amber `#8A6D1F` | "SYNTHETIC DEMO" |
| Negative / loss | rose `#A34A4A` | "−8.8%" |
| Info / neutral | ink-2 | meta text |

## Migration note

Replaces MASTER.md v2.1 light-editorial tokens (dark #0f1117 sidebar, mint/pink neon-adjacent accents, rounded-2xl hero). MASTER.md → v3.0 Research Desk on implementation. Tailwind v4 `@theme inline` bridge is MANDATORY (audit C1 — this was the broken token bridge).
<!-- 2026-08-04 17:36 UTC+7 -->
