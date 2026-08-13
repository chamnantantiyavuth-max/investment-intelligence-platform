# Capital Intelligence Live Office v1 — FIRST VISUAL CHECKPOINT (13 Aug 2026)

> Charter v1.1 checkpoint. Read-only Hermes Dashboard plugin
> `capital-intelligence-office`. STOP for Founder visual review after this.
> Clock basis: artifact_timestamp.py (2026-08-13 17:33 +0700).

## Deliverables (charter §7)

| # | Deliverable | Evidence |
|---|---|---|
| 1 | Dashboard navigation shows **Kanban + Capital Office** | `nav-kanban-capital-office.png` (vision-confirmed: KANBAN → CAPITAL OFFICE → ACHIEVEMENTS, no clipping) |
| 2 | Capital Office 11-desk floor | `capital-office-floor.png` (vision-confirmed: header LIVE·Capital Intelligence, Founder Desk ×2 GATEs, 11 desks with states/tasks/meta, activity + workers strips, no layout breaks) |
| 3 | LIVE-OFFICE-SOURCE-MAP.md | `hermes-plugins/capital-intelligence-office/LIVE-OFFICE-SOURCE-MAP.md` |
| 4 | Presentation-state mapping | source map §presentation-state contract + verified below |
| 5 | Sampled Office ↔ Native Kanban ↔ CLI comparison | see §Agreement |
| 6 | WebSocket live-event proof | see §Live events |
| 7 | Zero-write verification | see §Zero-write |
| 8 | No Office-specific persistent state | see §No persistent state |

## Plugin (installed via supported user/dashboard plugin mechanism)

- Source (versioned): `hermes-plugins/capital-intelligence-office/` (manifest v1.0.0,
  tab `/capital-office` after:kanban, plain-IIFE frontend via
  `window.__HERMES_PLUGIN_SDK__`, read-only backend `plugin_api.py`).
- Installed: `$LOCALAPPDATA/hermes/plugins/capital-intelligence-office/` +
  `plugins.enabled: [capital-intelligence-office]` in global config.
- NO Hermes core modification; NO version mismatch; bundled runtime v0.20.0.

## Acceptance

- Nav: Kanban + Capital Office both visible ✅ (DOM + vision).
- Tab opens without console error: 0 console/page errors ✅.
- Board: header `LIVE · Capital Intelligence` (slug iip resolved via
  `kanban/current`), data_source `hermes_kanban_board`, tasks 68 (native board
  shows the same 68; 4 archived excluded both sides) ✅.
- 11 desks render: CoS(Blocked), IC Secretary(Awaiting Founder),
  Commodity(Idle), Macro(Awaiting Founder), Equity(Idle), Options(Idle),
  CRO(Idle), Quant(Idle), Data Steward(Blocked), Auditor(Idle), Radar(Idle) ✅.
- Founder Desk: 2 GATE rows = t_51e3be79 ([GATE] 0004, needs_input) +
  t_2342aa1d ([GATE] 0012, needs_input) — identical to native Kanban + CLI ✅.

## Agreement (Office ↔ Native Kanban ↔ Hermes CLI ↔ DB oracle)

Method: office `/desks` states vs (a) native dashboard columns Blocked5/Done63
(verified Phase -1, same task IDs), (b) `hermes kanban list` blocked = same 5
IDs, (c) direct-SQLite TEST ORACLE (permitted for verification only) with the
same priority derivation → **11/11 desks match**:

| Desk | Office state | Oracle-expected | Sample current task |
|---|---|---|---|
| org-cos | blocked | blocked | t_8411623f (0016) |
| org-ic-secretary | awaiting_founder | awaiting_founder | t_51e3be79 (GATE 0004) |
| org-commodity-analyst | idle | idle | — |
| org-macro-strategist | awaiting_founder | awaiting_founder | t_2342aa1d (GATE 0012) |
| org-equity-analyst | idle | idle | — |
| org-options-strategist | idle | idle | — (role registered, no tasks — honest) |
| org-cro | idle | idle | — |
| org-quant-validator | idle | idle | — |
| org-data-steward | blocked | blocked | t_1ecfaaef (pilot fail) |
| org-auditor | idle | idle | — |
| org-radar-scout | idle | idle | — |

## Live events (charter D)

WebSocket `/events` (task_events tail, 2s poll, same stream as native Kanban).
**Proof:** with the office page open and NO manual refresh, a bounded synthetic
task was created (`[PILOT-NONCANONICAL] Live Office WS proof`, t_2f8c732d) →
the UI changed by itself: `tasks 68 → 69` + `last event: spawned` appeared
within the 2s poll window. Task archived immediately after verification
(`Archived t_2f8c732d`) — harmless bounded test per charter E. ✅

## Failure behavior (charter F)

Playwright route-block of all office API calls → **DEGRADED — data source
unavailable** banner + Founder area "Unavailable" + 0 desk cards; NO
fabricated Working/Idle states (verified: fabricatedWorking=false,
fabricatedIdle=false). `failure-degraded.png` ✅

## Zero-write (charter forbidden list)

- `plugin_api.py`: **0** POST/PUT/PATCH/DELETE routes; **0** INSERT/UPDATE/DELETE
  statements (grep-verified). GET + WS only.
- Frontend: fetch + WebSocket only; never reads SQLite directly.
- The only board mutation this session = the sanctioned bounded synthetic test
  (created via the supported CLI, archived after) — not an Office write path.

## No persistent state

The plugin creates no tables, no files, no caches — every response is derived
per request from `hermes_cli.kanban_db`. No Office-specific organizational
state exists (charter §5 presentation states never persisted).

## Constraints respected

Stage 7 = PASS WITH CONDITIONS (untouched) · Stage 8 = HOLD · old repo board
frozen/ACL (untouched) · board `other` untouched · no core modification ·
no portfolio-sensitive data · no IPM room · no write controls in v1.

## Deferred (Phase 2+ — per charter §8)

Pixel-art office, animations, handoff graph, approvals, IPM room, sound,
core changes. NOT implemented.

<!-- 2026-08-13 17:34 UTC+7 (artifact_timestamp.py) -->
