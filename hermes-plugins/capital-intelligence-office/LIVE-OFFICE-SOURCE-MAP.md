# LIVE-OFFICE-SOURCE-MAP — Capital Intelligence Live Office v1

> Charter §3 deliverable. Every piece of UI information maps to a Hermes
> runtime source, a derived presentation rule, and a degraded/failure behavior.
> Runtime: Hermes v0.20.0. Clock basis: artifact_timestamp.py.

## Data-flow invariant

```
Hermes Kanban (Capital Intelligence board, kanban/boards/iip)
      │  kanban_db (supported interface — same path as CLI/gateway)
      ▼
Capital Office plugin backend (READ-ONLY, per-request derivation, no state)
      │  /api/plugins/capital-intelligence-office/*  +  /events WS
      ▼
Capital Office frontend (plain IIFE via window.__HERMES_PLUGIN_SDK__)
```

The frontend NEVER reads SQLite directly. Direct SQLite reads are TEST-ORACLE
only (agreement verification). The plugin writes NOTHING (no POST/PUT/PATCH/
DELETE routes exist; no tables/files created).

## Source map

| UI information | Hermes source | Derived presentation rule | Degraded / failure behavior |
|---|---|---|---|
| Board identity + task totals | `kanban_db.list_tasks` (board iip) | count per native status (`VALID_STATUSES`), active runs from `list_runs` | health fetch fails → header DEGRADED badge, counts hidden |
| 11 desks (role/profile) | static ROLE-REGISTRY v0.1 rows 1–11 (`org-cos`…`org-radar-scout`) | fixed desk set; per-desk aggregation by `assignee` | always render (static); task data per-desk = Unknown when API down |
| Desk presentation state | task status + `block_kind` + active run | priority: blocked+needs_input → Awaiting Founder; active run → Working; blocked → Blocked; review → Reviewing; open (triage/todo/scheduled/ready) → Queued; only done/archived → Idle; no data → Unknown | no data → Unknown + DEGRADED banner; never fabricate Working/Idle |
| Current task title per desk | top-priority open task of the desk | first task matching the desk state (same priority order) | “—” when unavailable |
| Open/queued task count | tasks with status ∈ {triage,todo,scheduled,ready,running,blocked,review} | count per desk | “—” when API down |
| Active worker status | `task_runs` — run.status running / claimed+unexpired claim | desk active if any task has an active run | “idle” only when data present; Unknown otherwise |
| Last meaningful activity | `task_events.MAX(created_at)` per task (GROUP BY task_id) | max across desk tasks → epoch → time | “—” when none |
| Founder Desk items | tasks blocked + `block_kind ∈ {needs_input}` OR status=review | gate label founder_decision (needs_input) vs review | “Unavailable” when API down |
| Recent activity strip | `task_events` tail (last N by id) | join task title via task id | “No recent events” / “Unavailable” |
| Workers/runs strip | `task_runs` (recent, by id desc) | profile · task title · status · started_at | “No recent runs” / “Unavailable” |
| Live updates | `/events` WebSocket tailing `task_events` (id cursor, 2s poll) | on event → refetch desks/health → UI updates without manual refresh | WS close → reconnect 3s; WS error → DEGRADED until next successful fetch |
| DEGRADED / UNKNOWN | — | any API fetch failure → banner + per-surface Unknown; no stale-state fabrication | banner persists until a fetch succeeds |

## Presentation-state contract (charter §5 — UI-only, never persisted)

| State | Semantics (exact) | Source fields |
|---|---|---|
| Awaiting Founder | ≥1 task blocked with block_kind=needs_input | status, block_kind |
| Working | ≥1 task with an active run (running, or claimed with unexpired lock) | task_runs.status/claim_expires |
| Blocked | ≥1 task blocked (non-gate) | status=blocked, block_kind≠needs_input |
| Reviewing | ≥1 task in review | status=review |
| Queued | open tasks exist, no active run, no higher state | status ∈ {triage,todo,scheduled,ready} |
| Idle | no open tasks (all done/archived) | status |
| Unknown | no data (API/WS unavailable) | — |

Desk-state precedence: Awaiting Founder > Working > Blocked > Reviewing > Queued > Idle.

## Why no Options Strategist tasks on the board (honest note)

Desk 6 (Options Strategist, profile `org-options-strategist`) is registered in
ROLE-REGISTRY v0.1 but has no tasks and no installed profile in the current
org — it renders Idle (and will show a state only when real work is assigned).
No synthetic desk data is invented.

<!-- 2026-08-13 17:20 UTC+7 (artifact_timestamp.py) -->
