# C6 — Hermes-Native UI Status Semantics Correction (13 Aug 2026)

> Correction pass C6 per Founder directive — executed under project-workflow v3.8
> (governed engineering path), browser-smoked BOTH /kanban and /org-office.

## 1. Runtime status vocabulary (source of truth)

`hermes_cli/kanban_db.py:102` — **VALID_STATUSES = {triage, todo, scheduled, ready,
running, blocked, review, done, archived}** (9 statuses; NO `cancelled`).

## 2. Adapter correction (`backend/hermes_kanban_store.py`)

Before (Stage 7.5): `todo→Ready`, `archived→Done`, phantom `cancelled→Cancelled`,
no triage/scheduled/review — a hidden replacement state machine.

After (C6): direct 1:1 mapping of all 9 runtime statuses —
`Triage, Todo, Scheduled, Ready, Running, Blocked, Review, Done, Archived`.
No collapse, no invented status. `list_holds()` docstring updated (historical
records at evidence/organization/holds/).

## 3. Frontend

- `KanbanBoardPage.tsx` — renders columns dynamically from the API (unchanged
  architecture, FD #59); comments updated to the native vocabulary.
- `OrgOfficePage.tsx` — INFLIGHT/AWAITING buckets remapped to native statuses
  (inflight = Todo/Scheduled/Ready/Running; awaiting = Blocked/Review/Triage);
  "Published" filter → Done; metric notes updated ("blocked · review · triage",
  "todo → running"). Legacy 11-column names removed.

## 4. Locked tests (Acceptance Lock — FD #106 reference)

`tests/locked/test_org_workflow_api.py` updated to the Stage 7.5 contract:
- data_source = `hermes_kanban_board`; board slug/name asserted
- columns = the 9 native statuses; every card's workflow_column ∈ native set;
  legacy-only labels must NOT leak (no replacement state machine)
- C1 repair asserted: [GATE][ORG-2026-0004] = Blocked (needs_input), never Done;
  [MIGRATED:ORG-2026-0004] = Done (migration executed ≠ Founder approval)
- /org-queue holds = [] (board has no holds concept; historical holds on
  /org-holds from evidence/organization/holds/ per C4)
- `tests/locked/test_audit_api.py` — register date assertion bumped 11→13 Aug
  (FD #106 + harness backfill; same pattern as the earlier 10→11 Aug bump)

## 5. Verification

| Check | Result |
|---|---|
| pytest full suite | **206/206 passed** (was 203/206; 3 stale org-workflow + audit date) |
| frontend build (`npm run build`) | exit 0 (tsc -b + vite) |
| browser smoke /kanban (Playwright chromium, real render) | ✅ 9/9 native columns render (Triage/Todo/Scheduled/Ready/Running/Blocked/Review/Done/Archived); GATE + MIGRATED + RADAR cards visible; blocked cards show `blocked: needs_input`; console errors 0 |
| browser smoke /org-office | ✅ 11 desks render (10/11 active), "No active holds" (honest — both holds cleared/historical), metric labels native; console errors 0 |
| screenshots | `evidence/ui/c6-browser-smoke/kanban.png` + `org-office.png` (vision-verified) |

## 6. Residual / notes

- Long GATE titles truncate in the 192px kanban columns (pre-existing design trait
  of the narrow-column read-only board, FD #59 horizontal scroll) — cosmetic, not
  a regression. No overflow of the board container.
- `/org-holds` endpoint continues to serve the two HISTORICAL hold records
  (provenance `org_workflow_holds`) — live work-state comes only from the Hermes
  board; no legacy live-work mixing.

<!-- 2026-08-13 17:00 UTC+7 -->
