# Visual QA — Org Office / War Room (`/org-office`)

- **Task:** Org Office War Room page (role-centric org monitor) — Founder pick A (mockup `design/mockups/org-office-war-room.html`), 2026-08-07
- **Commits:** (pending — this QA is written before the feature commit; see git log for `org-office` commit after)
- **Approved objective (Founder):** monitor that work is actually divided across roles — "who is working on what, where each item stands, what needs your attention" — read-only, real data only, presentation layer.
- **Pages/states reviewed:** `/org-office` populated (desktop 1440); empty/standby desks (Options, Quant, CoS, Radar cards-owned) verified in same view; error/loading handled by existing pattern (Skeleton + scoped error with Retry).
- **Viewports:** desktop 1440 verified in browser. Mobile 390 = code-level audit only (browser tool locks viewport): grid `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`, pulse `grid-cols-2 md:grid-cols-6`, flex-wrap on desk meta — collapses to single column; masthead nav wraps; no horizontal overflow introduced by this page (desk rows wrap, tables absent).
- **Data contract (all real, read-only):** `GET /org-queue` (cards + columns + holds), `GET /research-artifacts` (artifact registry for card→artifact links), `GET /reports` (published notes per role via author match). No backend/API/schema change; git stays single writer (KANBAN-CONTRACT §6 — read-only by design, no drag/move/writes).
- **Role desks:** 11 principals from ROLE-REGISTRY-v0.1 (display names in user language; profile codes as discreet mono meta). Cards grouped by `principal_owner` (normalized: profile code OR display name, e.g. "Equity Alpha Analyst (simulated)" → equity desk).
- **Radar Scout desk:** cards owned = 0 (radar hands cards to analysts); desk shows "PRODUCED" + the 6 RADAR-001 cards (cards carrying `radar_observation`) under Recent output — honest representation of scout output without inventing ownership.
- **Org pulse:** display derivations only (Constitution §10 — no composite scores): cards in flight (Inbox→Validation), awaiting you (Founder Review + Blocked), published notes (reports `status: published`), active holds (non-CLEARED), desks active (n/11), org pulse (Healthy when 0 holds + 0 blocked).
- **IC Secretary author match:** anchored `^IC Secretary` — reports authored "… — IC Secretary synthesis" stay with their analyst desks; secretary desk shows only its own letters. (First pass over-matched; corrected in refinement pass.)

## Functional verification (browser, 2026-08-07)

- Login → `/org-office` renders: masthead nav includes **Org Office**; 11 desks; pulse strip (Cards in flight 4 · Awaiting you 1 · Published notes 18 · Active holds 0 · Desks active 7/11 · Org pulse Healthy); holds section "No active holds".
- Card→artifact links: 5 links to `/research/*` (pilot cards resolving via `linkArtifact`); 19 links to `/library/*` (published reports per desk).
- Console: **0 errors / 0 warnings** on the route (verified via `browser_console`).
- `npm run build` exit 0 (tsc -b + vite) · `npm run lint` 0 errors (7 pre-existing warnings).

## Border & containment audit

- Full-perimeter bordered content surfaces per viewport: **0** (target 0, budget ≤2).
- Desk grid uses hairline single-axis separators (`border-r`/`border-b`/`border-l`/`border-t` on grid cells — grid lines, not box outlines); pulse strip hairline `border-l` separators; desk headers `border-b`; rows `border-b` separators. No `ring`, no `border` box wraps, no shadow, no card containers.
- Tonal chips for status only (STANDBY/ACTIVE/WIP OK/PRODUCED + holds) — semantic state chips, excluded from border budget.
- Justification for every outline: scanning/state communication only (grid + hairline separators); no decorative outlines.

## Browser-first refinement pass (≥1 required — done)

1. First pass: IC Secretary desk over-matched reports (every report's author ends "— IC Secretary synthesis") → anchored regex to `^IC Secretary` (secretary desk now shows only weekly letters).
2. First pass: Radar Scout desk showed STANDBY + empty despite producing 6 cards → added `radar_observation`/`radar_source` to `OrgCard` type + "PRODUCED" load state + radar-produced cards under Recent output.
3. Removed unused `DONE_COLUMNS` (tsc TS6133) → build clean.

## Remaining deviations / notes

- **Known data drift (pre-existing, not introduced by this page):** cards ORG-2026-0006..0011 carry `workflow_column: Published`, which is NOT in `org_store.COLUMNS` (11 canonical columns) — the existing `/kanban` board therefore does not render published cards; this page renders cards by their own `workflow_column` so published cards appear correctly. Flagged for org-workflow (CoS/IC Secretary) — not a UI fix.
- Pilot cards (ORG-2026-0001..0005) remain in In Research/Cross-Review/Triage/Founder Review per card YAML (board.md shows Closed) — known board/card drift (2026-08-05) recorded in skill; page shows card truth, not the mirror.
- Mobile 390 = **EXTERNAL_NOT_TESTED** (browser viewport lock); code-level audit passed (single-column collapse, wraps, no horizontal scroll introduced).
- No new locked tests: presentation-layer page over existing read-only endpoints (same class as /kanban FD #59 — non-material, no backend change).

## Screenshot inventory

| File | State | Viewport |
|---|---|---|
| `03-final-desktop.png` | populated — 11 desks + pulse + holds | 1440 |

## Evidence tags

`BROWSER_VERIFIED` · `SCREENSHOT_VERIFIED` · `FUNCTION_TEST_VERIFIED` · `ACCESSIBILITY_STATIC_CHECK` (contrast tokens from MASTER.md v3.0) · `EXTERNAL_NOT_TESTED` (mobile viewport)

## Verdict

**PASS** — renders with real org data, role-centric monitoring objective met, borderless 0, institutional dense presentation per mockup pick A, console clean, build/lint green. Presentation-layer only; no backend/schema/API change.

<!-- 2026-08-07 14:35 UTC+7 -->
