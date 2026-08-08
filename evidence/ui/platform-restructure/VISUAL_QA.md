# VISUAL_QA — Platform Restructure + Blog Filter/Sort (FD #86, WS-1 + WS-2)

**Date:** 2026-08-09 · **Skill:** ui-dashboard-workflow v4.0.0 · **Status:** WS-1 + WS-2 COMPLETE (WS-3 UI-4 + WS-4 deep-analysis pending)

## Task / commits

- FD #86 — Platform Restructure (Option A): blog = primary surface; old platform trimmed to Org Office + Kanban Board; routes DELETED.
- WS-1: blog full filter + sort system (search · status · type · series · sort: newest/oldest/title/series).
- WS-2: App.tsx — `/` → `/library` redirect; 13 legacy page files + 8 dead helper files deleted; Masthead 10-item → 3-item (Library · Kanban Board · Org Office).

## Pages / states reviewed (browser, localhost:8000)

| Page | State | Result |
|---|---|---|
| `/` | redirect | → /library (magazine) ✓ |
| `/library` | populated | hero + 01/02/03 grid + latest stream + chips + Ft1 footer ✓ |
| `/library` + search "gold" | filtered | 2 rows (both gold) ✓ |
| `/library` + sort title A–Z | sorted | "Gold vs Real Rates" < "The Channel…" ✓ |
| `/library` + series Apple + search "moat" | combined | 3 rows (all Apple, title contains moat) ✓ |
| `/library` + filters → no match | empty state | "No reports match your filters" + Clear filters button ✓ |
| `/kanban` | populated | 11 columns render, 3-item nav ✓ |
| `/org-office` | populated | 11 role sprites render, 3-item nav ✓ |
| `/am-queue` (deleted route) | 404 | NotFoundPage ✓ |
| console | all pages | 0 errors ✓ |

## Viewports

Desktop 1440 verified. Mobile not re-captured this pass (no responsive changes — existing breakpoints unchanged).

## Bible-to-UI coverage

- FD #86 (this decision) · FD #62 (reports = product — blog primary) · FD #65 (legacy freeze — backend untouched) · FD #84 (standalone magazine shell) · FD #58 (point-in-time footer). Presentation-layer only: no backend/API/schema change; no new domain semantics.

## Functional verification

- Search matches title + subject + author + date (case-insensitive).
- Sort: date_desc (default) / date_asc / title A–Z / series (series-name then date desc).
- Series chips + status/type selects compose with search and sort (all filters AND together).
- Empty state offers single "Clear filters" action that resets all four controls.

## Border & containment audit

- Blog (library): 0 full-perimeter outlines — hairlines (border-rule/ink rules) as separators only. Inputs/selects have functional editable-boundary outlines (excluded by policy). Filter toolbar = open region.
- Kanban/Org Office: unchanged (0 bordered surfaces from prior audits).

## Screenshot inventory

- `evidence/ui/platform-restructure/01-library-filter-sort-final.png` — library with search+sort toolbar, chips, magazine footer.
- `evidence/ui/platform-restructure/02-library-before-filters.png` — full library populated state.

## Evidence tags

`BROWSER_VERIFIED` · `FUNCTION_TEST_VERIFIED` · `SCREENSHOT_VERIFIED` · `STATIC_OBSERVATION`

## Verdict

WS-1 + WS-2 accepted evidence: gates tsc 0 / lint 0 / build exit 0 / pytest 141/141; browser 9 scenarios 0 errors. Remaining: WS-3 UI-4 (Decision Register/Audit Center — needs git-history endpoint) + WS-4 deep-analysis mandate.
<!-- 2026-08-09 03:40 UTC+7 -->
