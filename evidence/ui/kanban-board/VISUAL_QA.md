# Visual QA — Kanban Visual Board (FD #59)

- **Task:** Read-only kanban VISUAL board view — 11 canonical columns (KANBAN-CONTRACT §2) rendered as column stacks from GET /org-queue (D1 endpoints, FD #55). Closes the 5 Aug 2026 closeout open question.
- **Commit:** (pending — commit after Founder acceptance)
- **Approved objective (FD #59):** read-only board with columns + cards + holds, honest empty states, borderless 0–2, Research Desk pattern. Presentation-layer only — no backend/API/schema changes, no write routes.
- **Mode:** FEATURE (established design system — Research Desk v3.0 / FD #51)

## Pages / states reviewed

| Page | States | Result |
|---|---|---|
| /kanban | populated (5 pilot cards), empty columns (6), loading (skeleton), error (scoped retry) | ✅ browser-verified |
| /research/org-pilot/IC-DECISION-PACK.md | artifact detail reached from board card link | ✅ browser-verified |
| nav | Kanban Board item active state, Research Desk + Briefing regression | ✅ browser-verified |

## Viewports

- Desktop 1258×622 (browser tool lock — matches previous tasks' desktop evidence) ✅ screenshot
- Mobile 390×844 — **EXTERNAL_NOT_TESTED** (browser tool locks viewport at 1258px, same as UI-1/2 task); code-level responsive audit below

**Code-level responsive audit (mobile 390):** board container `overflow-x-auto` + `min-w-max` + fixed 192px columns = standard kanban horizontal scroll (columns never compress below usable width); masthead nav already `flex-wrap` (existing behavior); cards stack vertically inside columns with no fixed heights. No media queries needed for the board itself.

## Functional verification (browser)

- Console: 0 errors, 0 JS exceptions (post-refinement HMR reload)
- All 11 columns render in canonical order with counts derived from `workflow_column` (never hardcoded): INBOX 0 · TRIAGE 1 · SCOPED 0 · DATA READY 0 · IN RESEARCH 2 · CROSS-REVIEW 1 · VALIDATION 0 · FOUNDER REVIEW 1 · MONITORING 0 · BLOCKED 0 · CLOSED 0
- 5 pilot cards in their YAML columns (contract source — UI follows card YAML, not board.md display table)
- Empty columns: honest "No cards / intake: CoS / IC Secretary"
- Card → artifact links: all 5 hrefs resolve via `linkArtifact` (e.g. ORG-2026-0004 → /research/org-pilot/IC-DECISION-PACK.md); detail page renders (provenance stamp, 7 tabs, identity table, related artifacts)
- No active holds in pilot data (holds were cleared in the dry-run) — hold-line rendering path present in code (card.active_holds map)
- No drag/move/write affordances anywhere (KANBAN-CONTRACT §6 — read-only)

## Bible-to-UI coverage

| Contract | UI representation |
|---|---|
| KANBAN-CONTRACT §1 (operational ≠ domain state) | header label: "Operational tracking only — card state never equals domain state (§1)" |
| KANBAN-CONTRACT §2 (11 canonical columns) | columns rendered from API `columns` field, never hardcoded |
| KANBAN-CONTRACT §6 (movement rights) | read-only — no drag/move/write affordances |
| KANBAN-CONTRACT §7 (blocked standard) | blocked_reason warning line on card |
| Constitution §10 (no composite scores) | counts only; no progress bars, no readiness scores |
| Constitution §8 / §23.4 (provenance) | data_source stamp + latest-card-update label |

## First-pass findings → corrections made (refinement pass)

1. Card padding `py-2.5` → `py-2`; column gap `gap-4` → `gap-3`; column width 200 → 192px — density pass toward the paper-desk character (vision review: "too airy")
2. Column header `whitespace-nowrap` added — long names (CROSS-REVIEW) can never wrap
- No other findings. Vision review of final pass: 11 columns, hairline separators, tonal chips, no clipping, dense paper aesthetic confirmed.

## Border / containment audit

- Full-perimeter bordered content surfaces: **0** (within 0–2 budget)
- Tonal surfaces (no outline): card chips `bg-bg-panel rounded-md` (independent objects — justified) + error/empty states
- Single-axis separators only: `border-l border-rule` hairlines between columns (scanning justification — 11 parallel stacks need boundary cues), `border-b border-rule` under page header (app-wide pattern)
- No decorative borders, no parent+child outlines, no shadows

## Accessibility (static check)

- Card links keyboard-focusable with `focus-visible:outline-2 outline-primary`
- Column headers + counts read as text (no color-only meaning); warning statuses carry text ("HOLD…", "blocked: …")
- Color contrast: ink-2/ink-3 on background = existing design-system tokens (app-wide baseline)
- Read-only semantics: no interactive affordances that imply write

## Remaining deviations

- Mobile 390 viewport not browser-tested (tool lock) — code-level audit only (same convention as UI-1/2, per iip-ui-design)
- Empty-column note "intake: CoS / IC Secretary" is a display hint, not a write affordance

## Screenshot inventory

| File | Content |
|---|---|
| 01-first-pass-desktop.png | first browser pass (wider spacing) |
| 02-final-desktop.png | after refinement pass (density, nowrap headers) |

## Evidence tags

`BROWSER_VERIFIED` · `SCREENSHOT_VERIFIED` (02-final-desktop) · `FUNCTION_TEST_VERIFIED` (console 0 errors, card→artifact chain) · `ACCESSIBILITY_STATIC_CHECK` · mobile 390 `EXTERNAL_NOT_TESTED` (tool lock; code-level audit done) · `STATIC_OBSERVATION` (hold-line path code-reviewed, no active holds in current data)

## Final verdict

**PASS — ready for Founder acceptance.** Non-material presentation-layer change (AGENTS.md UI rule); no backend/API/schema change → Python suite unaffected (311/311 baseline). No visual council required per v3.7.1 materiality rule (routine single-view feature in established design system); Founder may request one.

<!-- 2026-08-06 12:30 UTC+7 -->
