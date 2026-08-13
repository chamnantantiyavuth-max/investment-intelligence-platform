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

## H1 — profile truth (Phase 2)

All 11 organizational profiles ARE installed in the runtime (verified
2026-08-13: `profiles/` contains org-cos … org-options-strategist … org-radar-scout).
`org-options-strategist` exists → its Idle is genuine (profile exists, no work).
The adapter still distinguishes (H1): `available: false` → presentation state
`unavailable`/Not Installed (never Idle) if a profile is ever missing.

## H2 — operational vs diagnostics (Phase 2)

Presentation-only classification: PILOT-NONCANONICAL / harness-canary / test /
synthetic tasks (assignee in {harness-canary-ipm, harness-docker-test,
harness-test} OR title markers) are exposed in a `diagnostics` layer per desk
(e.g. Data Steward `DIAG done:4 blocked:1` — the pilot failure-test residue)
but do NOT drive the main desk state. Main state derives from Operational work
only. Hermes truth is never filtered (tasks remain on the board).

## H3 — adapter isolation (Phase 2)

All kanban-DB access lives behind ONE `LiveOfficeDataAdapter` in
`plugin_api.py` (kanban_db helpers preferred; the read-only SELECTs on
task_runs/task_events/task_links are isolated there). The frontend is
completely schema-independent (consumes only the JSON API).

## Phase 2.1 — Semantic Hardening (S1–S4, Founder PASS WITH CONDITIONS)

### S1 — handoff classification: ACTIVE / RECENT / HISTORICAL

A recorded `task_links` relationship is NOT proof of live coordination.
`/handoffs` classifies every desk-to-desk edge per request:

| Class | Definition | Presentation |
|---|---|---|
| ACTIVE | parent or child is currently open (status ∈ open set) OR has a live worker (active run) | normal visible line + packet animation |
| RECENT | both sides closed, but either side saw an event or a finished run within the 30-minute window (`_HANDOFF_RECENT_WINDOW = 1800`) | subdued dashed fading line |
| HISTORICAL | both sides completed/archived and no activity in the window | NOT shown by default; exposed via `scope=all` (History toggle) |

- Edge class = worst class across its links (any open link keeps the edge ACTIVE).
- `load_board(include_archived=True)` is used ONLY by `/handoffs` so archived
  tasks stay in the classification universe (spec: "both sides completed/archived").
- Packet animation fires ONLY when a real WS event maps to a rendered
  ACTIVE/RECENT edge (`task_ids` contains the event's task; historical edges
  never pulse).
- Verified live 2026-08-13: the 39 recorded links collapse into 15 desk edges
  — ALL historical (DR/PILOT/DISC chains, all done, no recent activity).
  Default office honestly draws 0 lines; History toggle reports 15.

### S2 — Error precedence + crash detection

Desk-state precedence (updated): Awaiting Founder > Working > Blocked >
Reviewing > Queued > **Error** > Recently Completed > Idle. A recent failure
can NEVER be masked by a recent success.

Failure/success detection follows the actual `task_runs` schema (verified in
kanban_db.py): `status ∈ {crashed, timed_out, failed}` OR
`outcome ∈ {crashed, timed_out, spawn_failed, gave_up}` ⇒ failure; success
when `status ∈ {done, completed}` OR `outcome == completed`. Both fields are
checked (old code checked outcome only).

### S3 — structured diagnostics classification

Replaces broad free-text substring matching ("synthetic", "test residue") with
a strict order:
1. explicit structured task metadata — the `tasks` table exposes NO
   type/kind/tags column (verified against schema 2026-08-13) → tier currently
   unavailable, kept as the documented hook;
2. exact standardized title PREFIXES: `[PILOT-NONCANONICAL]`, `[TEST]`,
   `[SYNTHETIC]` (case-insensitive, startswith);
3. known harness/test profiles: {harness-canary-ipm, harness-docker-test,
   harness-test}.

An operational task titled "Analyze synthetic data exposure" stays Operational
(locked negative test). Verified: no live-board title contains the old markers,
so zero reclassification side-effects.

### S4 — Hermes-home profile resolution

`_profiles_dir()` resolves through the Hermes runtime
(`hermes_cli.config.get_hermes_home()` → profiles root when HERMES_HOME is
profile-shaped; else `<HERMES_HOME>/profiles`). The Windows AppData absolute
path remains only as a last-resort fallback. Verified: resolves to
`…\AppData\Local\hermes\profiles` with all 11 org-* profiles present.

### Locked acceptance tests

`tests/test_capital_office_semantics.py` — 23 bounded tests (S1 classification
+ archived inclusion, S2 precedence + dual-field run semantics, S3 positive +
negative classification, S4 resolution). Suite: **229/229 passed**.
Bounded live probes (2 task pairs, [TEST] prefix) created → verified
active/recent/historical classification + desk-state isolation → archived +
unlinked (zero residue). Browser smoke: 11 desks, 2 Founder GATEs, 0 handoff
lines (honest), History toggle (15), 0 console errors, 1440×900 clean.

## Phase 3 — Visual Polish / Living Office (v1.2.0, LOGIC FREEZE)

Presentation-layer only (per Founder freeze 2026-08-13): pod-zone floor
(Founder Office focal → TRANSITION → ORCHESTRATION → RESEARCH/INTELLIGENCE
pods → REVIEW/CONTROL → EXTERNAL SENSING), role-motif pixel workstations
(monitors/rack/radar/shield/docs/chart…), truthful per-state visuals,
`▲ FOUNDER` chip on awaiting desks, desk-edge handoff lines, enlarged glowing
packet, read-only agent detail drawer, top summary strip, compact rail.
Semantics unchanged (S1–S4 frozen).

Two backend touches (both read-only / genuine-defect fixes exposed by visual
work):
1. `/activity?profile=<p>` — additive per-desk event filter for the drawer.
2. `/events` WS live-tail — cursor now starts at `MAX(id)` at connect instead
   of 0 (which replayed the full history at 200 events/2s and delayed real
   events by minutes). Packet pulse now fires ≤1s after a real event.

Evidence: `evidence/ui/live-office-plugin/PHASE3-VISUAL-POLISH-2026-08-13.md`
+ `VISUAL_QA.md` + screenshots (1440/1920 clean, drawer, working, active
handoff packet, full-page). Suite 229/229. 0 console errors.

## Phase 3.1 — Live Reliability Closure (R1–R3, v1.2.1)

Bounded reliability/security closure (no visual change, no S1–S4 reopen):

- **R1 WS reconnect contract** — backend now always sends `{events, cursor}`
  every 2s poll (cursor = client reconnect baseline + heartbeat); frontend
  tracks the cursor, reconnects with `?since=<last_cursor>`, and runs a
  read-only `refresh()` on every (re)connect. First load stays live-tail (no
  history replay). Live proof: reconnect URL `&since=965`, gap event caught
  up (sub advanced to `created 11:46 PM`), state reconciled without a future
  event.
- **R2 WS auth FAIL-CLOSED** — `_ws_authorized(ws)`: helper
  unavailable/error/exception ⇒ unauthorized ⇒ close 1008. Unit ×4
  (ok/deny/raise/module-missing) + E2E (missing + invalid credential
  rejected; office's own token connection still accepted).
- **R3 profile filter BEFORE LIMIT** — `recent_events(conn, limit, profile)`
  filters inside the SQL (JOIN tasks.assignee) before LIMIT; archived-task
  events included in drawer history (documented rule + test). E2E: target
  profile's older event returned despite newer noise.

Suite **235/235** (229 + 6 new). Browser smoke: 11 desks, 2 GATEs, 0 lines,
drawer, 0 console errors. Evidence:
`evidence/ui/live-office-plugin/PHASE3.1-LIVE-RELIABILITY-CLOSURE-2026-08-13.md`.

<!-- 2026-08-13 23:47 UTC+7 (system clock) -->
