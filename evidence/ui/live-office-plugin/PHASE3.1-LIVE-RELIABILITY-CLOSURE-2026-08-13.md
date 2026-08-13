# PHASE 3.1 — LIVE RELIABILITY CLOSURE (R1–R3)

> Live Office v1 · Phase 3 Visual = **PASS** (Founder) ·
> Production Readiness = **PASS WITH CONDITIONS** (R1–R3, Founder source review)
> Scope: three bounded reliability/security closures ONLY. No redesign, no
> S1–S4 reopen. Phase 3.1 = the final gate before `V1 FINAL = PASS`.

## R1 — WebSocket reconnect gap (LIVE observability defect)

**Finding:** frontend never preserved/sent its last processed cursor on
reconnect; backend only emitted `cursor` when events existed — a silent
connection never handed the client a baseline, so a reconnect fell back to
live-tail and skipped events that occurred while disconnected.

**Fix (both sides):**
- Backend `/events`: always send `{"events", "cursor"}` every 2s poll (even
  empty) — the cursor is the client's reconnect baseline and the poll doubles
  as a lightweight heartbeat (also prevents idle-close of silent sockets).
- Frontend: track `lastCursorRef` from every message; reconnect with
  `?since=<last_cursor>`; `onopen` now also runs a read-only `refresh()` as a
  state-reconciliation safety net on every (re)connect. First load stays
  live-tail (no history replay).

**Bounded acceptance (live, in-browser):**
```
first ws url            : .../events?token=…            (no since — live tail) ✓
reconnect ws url        : ...&since=965                 (cursor preserved)     ✓
gap event catch-up      : sub "…· created 11:46 PM"     (lastEvent advanced)   ✓
state reconcile         : tasks 71 → 72 + DIAG ready 2  (B visible, no future
                          event needed)                                        ✓
console                 : 0 errors                                              ✓
```

## R2 — WebSocket auth FAIL-CLOSED (security boundary)

**Finding:** `except Exception: authorized = True` converted auth-helper
failure into authorization.

**Fix:** extracted `_ws_authorized(ws)` — helper unavailable/error/exception
⇒ `False` ⇒ connection closed (1008). Auth failure is NEVER authorization;
raw task-event data is never exposed when authentication cannot be
established. No separate auth system invented (installed Hermes auth
contract preserved).

**Deterministic verification:**
- Unit (4 cases, monkeypatched helper): accept-on-ok ✓ reject-on-deny ✓
  reject-on-raise ✓ reject-on-module-missing ✓
- E2E (live, raw WebSocket): missing credential → rejected ✓
  invalid credential → rejected ✓
- The dashboard's own token-carrying connection remains accepted (office live
  through every smoke).

## R3 — Profile activity filter BEFORE LIMIT (drawer accuracy)

**Finding:** `/activity?profile=&limit=N` applied global LIMIT N then filtered
by profile → desks with older events could return `[]` under noise.

**Fix:** adapter `recent_events(conn, limit, profile)` — the profile filter
now runs inside the SQL JOIN (`tasks.assignee = ?` … `LIMIT ?`) before the
limit. Decision documented + tested: **archived-task events ARE included** in
the drawer's recent history (audit trail, consistent with handoffs'
include-archived classification).

**Bounded verification:**
- Unit (in-memory DB): target event survives 20 newer noise events ✓; global
  path unchanged ✓; archived-task rule ✓
- E2E (live): `/activity?profile=org-cro&limit=8` returns the OLDER target
  event despite a newer org-cos noise event ✓

## Regression & preservation

- Suite: **235/235 passed** (229 + 6 new R2/R3 tests).
- Browser smoke (final build): 11 desks · 0 handoff lines (zero-active quiet
  office unchanged) · 2 Founder GATEs (0004 + 0012) · drawer opens · **0
  console errors** · 1440/1920 clean.
- Frozen invariants intact: Native Kanban authoritative · read-only
  projection · zero write routes · no Office DB/state · S1–S4 semantics ·
  all Phase-3 visual behavior. Stage 7 = PASS WITH CONDITIONS · Stage 8 =
  HOLD. Luna not required/not invoked (no Hermes-core/auth-contract change
  needed — auth helper contract untouched).

## Notes

- First-load live-tail behavior preserved (no history replay) — probe events
  created before page load are intentionally NOT replayed (verified: probe A
  silent, baseline cursor still provided by the empty-poll message).
- `[TEST]` probes archived after each phase (bounded, zero residue — board
  returned to baseline: 39 task_links, 0 running runs).

<!-- 2026-08-13 23:47 UTC+7 (system clock) -->
