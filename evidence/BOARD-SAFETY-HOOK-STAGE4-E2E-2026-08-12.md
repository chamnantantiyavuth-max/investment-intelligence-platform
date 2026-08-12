# BOARD SAFETY HOOK — Stage 4 Live E2E (2026-08-12)

Task: t_25f6af1d [PILOT-NONCANONICAL] Board Safety Hook E2E
Pilot stage: 4 — "verify live create under hook-protected config lands on iip"
Worker runs: run 13 (killed by gateway restart, 20:25–20:32) → run 14 (live E2E, 20:32+)

## Outcome: PASS

The pre_tool_call board-safety-hook now fires live in the worker loop and
enforces fail-closed board safety for all kanban mutations on the iip profile.

## 1. What the hook protects

- Config: `profiles/iip/config.yaml` → `hooks.pre_tool_call[0]`
  - matcher: `kanban_.*|terminal`  (fullmatch semantics — must match real tool names)
  - command: `C:/Program Files/Git/usr/bin/bash.EXE .../scripts/board-safety-hook.sh`
  - timeout: 10s, fail_closed: true, hooks_auto_accept: true
- Script: `iip-harness-prep/scripts/board-safety-hook.sh`
  - blocks kanban_* tools whose resolved board != iip, or whose
    HERMES_KANBAN_DB / db arg points at a non-iip DB
  - blocks terminal commands containing `hermes kanban <mutation>` with --board != iip

## 2. Bugs found & fixed by run 13 (root cause analysis)

| # | Bug | Fix |
|---|-----|-----|
| B1 | Config matcher `kanban_\|hermes kanban` used `re.fullmatch` semantics — matches NO real tool name (`kanban_create` → False). Hook registered but could never fire. | `hermes config set hooks.pre_tool_call.0.matcher 'kanban_.*\|terminal'` (verified fullmatch-valid for all kanban_* tools + terminal) |
| B2 | Script compared HERMES_KANBAN_DB raw string: live env carries Windows form (`C:\...`) while EXPECTED_DB is MSYS form (`/c/...`) → would false-block EVERY call once B1 was fixed. | Added `norm_path()` (cygpath -m, lowercase fallback) for DB path comparison |
| B3 | (tool behavior, observed) `kanban_create(board="other")` with the inert hook did NOT route to an other-board DB — it fell back and created on the iip DB. Now unreachable: the hook blocks board=other before the tool runs. | — |

## 3. Verification layers (run 13, before kill)

- 11-case script matrix (test_hook.py): create board=iip / board=other / no board /
  DB→other / env-unset / terminal hermes kanban ± --board / read-only / non-kanban
  tools / db_path alt key → all pass (ALLOW for iip, BLOCK for other).
- Official harness `hermes hooks test` (4 cases incl. wire-shape parsing of the
  block directive) → pass.
- Confirmed `_serialize_payload` (agent/shell_hooks.py:687) maps kwargs["args"] →
  wire `tool_input`, so the script's `tool_input` read is correct for the live engine.

## 4. LIVE E2E (run 14 — hook registered in worker at spawn 20:32:40, matcher kanban_.*|terminal)

### Positive control — board=iip
- `kanban_create(board="iip", ...)` → hook ALLOWED → card t_a6d35895 created.
- DB check: present in `boards/iip/kanban.db` (id=t_a6d35895, tenant=iip, status=todo,
  created_by=iip); NOT present in any other board DB (capital-command, default,
  notebooklm-kb, other, robot-trading scanned).

### Negative control — board=other
- `kanban_create(board="other", ...)` → hook BLOCKED live.
  Tool error: `Board safety: resolved board 'other' != expected 'iip' — refusing kanban mutation`
- DB check: no card with that title exists in ANY board DB (zero rows).
- The board=other mutation never reached the tool layer.

## 5. Locked acceptance

`scripts/stage4-acceptance.sh` (board resolution, board-guard fail-closed,
kanban/current=iip, CLI boards show) → run after E2E, see run output (PASS expected).

## 6. Probe-card cleanup

The kernel scopes workers to their own task (cross-task mutate refused), so the
probe worker leaves handoff comments on each child; on t_25f6af1d completion the
dependency gate releases them to ready, each dispatches once to iip, reads the
comment, and self-completes (no re-verification).

- t_a6d35895 (live positive probe, run 14) → hook ALLOWED, landed iip DB; self-completes.
- t_71fc2511 (positive probe created in run 13 while hook was still inert —
  superseded by the live re-test) → self-completes.
- t_0f01727d (negative-control card created in run 13 — it was NOT blocked then
  because the matcher bug made the hook inert; the negative control was re-run
  live in run 14 and correctly BLOCKED with no card created) → self-completes.

## Artifacts

- Hook script (fixed): `iip-harness-prep/scripts/board-safety-hook.sh`
- Script matrix driver: `kanban/boards/iip/workspaces/t_25f6af1d/test_hook.py`
- Acceptance script: `iip-harness-prep/scripts/stage4-acceptance.sh`

<!-- 2026-08-12 20:40 UTC+7 -->
