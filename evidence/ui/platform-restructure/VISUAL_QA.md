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

## WS-3 UI-4 COMPLETE (2026-08-09, same session — FD #86 Option A approved)

`/audit` page (Decision Register + Audit Center + Model Registry) + 3 read-only endpoints.

- Backend: `audit_store.py` (FD register parser — 102 items contiguous, git log bounded 40, §23.9 correction records, adapter registry) + `audit_routes.py` (GET /api/decisions, /api/audit/git-log, /api/audit/model-registry) + main.py router registered.
- Locked tests: `tests/locked/test_audit_api.py` (4 tests: auth boundary 401; register contiguous 1..102 + FD #86 date stamp; git-log commits + corrections; model-registry == ADAPTER_VERSION v5). Suite 141 → **145**.
- Frontend: `auditClient.ts` (credentials include) + `AuditPage.tsx` (3 sections, borderless, ledger rows, register search, loading/error/empty states) + route `/audit` + Masthead nav (Library · Kanban Board · Org Office · Audit).
- Browser verified (localhost:8000): /audit renders 102 items · 40 commits · 6 corrections · v1–v5 registry; register search "Hallmark" → FD #85; console 0 errors. Screenshot: `03-audit-page-final.png`.
- Gates: tsc 0 / lint 0 / build exit 0 / pytest 145/145.

**WS-4 (deep-analysis coverage gap) — pending Founder mandate (research pipeline, not UI).**

## Verdict

WS-1 + WS-2 + WS-3 accepted evidence: gates tsc 0 / lint 0 / build exit 0 / pytest 145/145; browser 10+ scenarios 0 errors (library filter/sort, platform trim 404s, /audit 3 sections + search). Remaining: WS-4 deep-analysis mandate.
<!-- 2026-08-09 03:40 UTC+7 -->
