# Visual QA — P2 Institutional Presentation Rollout (FD #60)

- **Task:** P2 rollout — apply the approved institutional research-note standard (Ray Dalio requirement #7) across all pages, following the accepted reference page (Fundamental detail).
- **Reference:** `evidence/ui/p2-reference/02-aapl-note-final.png` (Founder-approved standard, commit 1336d33)
- **Commits:** e861931 (queue+cheap&quality) · a95707d (CS radar+SLV note) · b32c98a (13F ledger+weak signals) · bda25fa (AM polish)
- **Mode:** FEATURE rollout within the established Research Desk v3.0 system; presentation-layer only.

## Standard (applied everywhere)

1. Question-led: every page opens with the investment question + a one-paragraph answer
2. Dense aligned number tables (tabular-nums, hairline rows) — no shadcn Card/Badge/Tabs shells
3. States as compact colored text (mint/rose/amber), never pill-everything
4. Honest depth: missing data framed as "Analysis limits" / known limits — never pseudo-complete
5. Zero internal jargon (Bible §/FD#/CONTRACT/spec refs) — provenance as discreet chips, IDs as tooltips/background
6. Synthetic/hybrid/real labels preserved (discreet but honest)

## Pages converted (browser-verified)

| Page | Result | Evidence |
|---|---|---|
| /fundamental (queue) | question-led ledger "Which companies deserve a closer look?" + honest moat-limitation note | browser + console |
| /fundamental/:id (reference) | accepted standard (AAPL note) | 02-aapl-note-final.png |
| /cheap-quality | honest empty state with real reason (no 5y volatility data) | browser |
| /cs-radar | dense ledger + lead judgment, discreet synthetic label | browser |
| /cs-radar/:id (SLV) | one-scroll note — buried discount/demand substance surfaced (gold/silver ratio 88 vs 65 median, solar +20%, physical premiums); macro depth-limit honest | 03-slv-note.png |
| /institutional | 13F ledger — plain-language actions (Held/Added/Reduced), CUSIPs to tooltips, pagination | 07-institutional-ledger.png |
| /weak-signals | ledger, no dead buttons, honest demo framing | browser |
| /am-queue · /am-theme · /am-screener | already v3.0 + P1 hygiene — verified consistent | 06-am-screener.png |
| / (Briefing) · /research · /kanban | v3.0 + P1 hygiene — consistent | (P1 pass) |

## Independent review (vision model, bounded question)

- AAPL note: "would pass as a high-quality internal First Look at a professional fund"
- SLV note: honest depth-limit framing "highly professional... protects the credibility of the overall conviction rating"
- AM screener: "institutional-grade... dense enough for professional analysis but aligned and styled to avoid visual fatigue"
- 13F ledger: "clean, dense institutional data display... perfectly aligned"

## Border / containment audit

- Full-perimeter bordered surfaces: 0 across converted pages (hairline row separators + tonal panels only)
- No decorative outlines, no parent+child containment, no shadows

## Verification

- npm run lint: 0 errors (7 pre-existing warnings) per batch
- npm run build (tsc -b + vite): exit 0 per batch
- Browser: every page walked after conversion; console 0 errors
- Python suite untouched (frontend-only) — 311/311 baseline

## Remaining phases (unchanged)

- P3: research-artifact pages render CIW research as designed notes, not raw markdown
- P4: content depth (CS macro enrichment / FO moat-valuation-narrative — material, named FDs)
- P5: full re-audit + visual council + Founder acceptance

## Evidence tags

`BROWSER_VERIFIED` · `SCREENSHOT_VERIFIED` (02-aapl-note, 03-slv-note, 06-am-screener, 07-institutional-ledger) · `FUNCTION_TEST_VERIFIED` · `ACCESSIBILITY_STATIC_CHECK` (focus-visible links, text+color states) · mobile `EXTERNAL_NOT_TESTED` (browser tool viewport lock — code-level responsive: tables use min-width grids + overflow-x-auto)

<!-- 2026-08-06 14:10 UTC+7 -->
