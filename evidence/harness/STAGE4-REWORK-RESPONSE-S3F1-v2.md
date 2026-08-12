# Stage 4 — Engineering Review REWORK Response (S3-F1 Board Safety v2)

**Date:** 2026-08-12
**Reviewer:** Independent Engineering Council (Sol Medium, approved routing) — Verdict: **REWORK**
**Status:** Design v2 — incorporating all review findings. Awaiting full review text; findings extracted from review transcript.

---

## Review Findings (from transcript)

- **F1 (High):** Terminal/CLI path remains policy-only in A+C+B — `board-guard.sh` is manual; CLI mutations from within the agent (terminal tool) or operator shells bypass the hook. Need automatic enforcement on the CLI/terminal surface too.
- **F2 (High):** `on_session_start` hook does NOT inject context in this install (no context-injection support for that event as designed) — visibility mechanism as proposed won't work; replace with a different mechanism or drop.
- **F3 (High):** Hook registration/consent failure modes unhandled: non-TTY (gateway/worker) skips non-allowlisted hooks unless `HERMES_ACCEPT_HOOKS=1` / `hooks_auto_accept: true`; a silently-skipped hook = no protection. Need explicit registration + health verification (`hermes hooks list` / `hermes hooks doctor`).
- **F4 (High):** Guard derives board from env/file only — but in-agent kanban tools expose an explicit `board` input that overrides the env pin (`kanban_tools.py:215-227, 1674-1690`), and `HERMES_KANBAN_DB` directly pins the DB path and takes precedence over board selection (`kanban_db.py:565-587`). Bypasses: env=iip + `tool_input.board="other"` → allowed by env-only hook; env=iip + `HERMES_KANBAN_DB=<other db>` → wrong DB mutated. **Guard must derive the ACTUAL EFFECTIVE DB DESTINATION**, not merely `HERMES_KANBAN_BOARD`.
- **F5 (High):** Hook matcher and hook-absence behavior: matcher must cover all kanban_* tool names AND terminal-tool CLI invocations; if hook is absent/disabled, Kanban mutation must be prohibited or startup-pin-safe (safe-mode).
- **F6 (Med):** Missing explicit rollback section + rollback test.

## Required changes (from review)

1. Automatic enforcement on ALL mutation surfaces (agent tool + terminal/CLI + dispatcher + worker), not policy-only for CLI.
2. Replace `on_session_start` visibility with a mechanism that actually works on v0.20.0 (or drop — visibility is secondary).
3. Explicit hook registration/consent: set `hooks_auto_accept: true` (or pre-seed allowlist) + verify with `hermes hooks list` + `hermes hooks doctor` after gateway restart.
4. Guard must compute effective DB destination: resolve `HERMES_KANBAN_DB` → board file → env pin → tool_input.board override → assert DB path == iip board DB.
5. Safe-mode: when hooks are disabled/absent → Kanban mutation blocked (fail-closed), or startup pin guarantees iip.
6. Rollback section + test.

## Missing acceptance cases (add, don't replace the 10)

- in-agent mutation, board omitted → lands iip
- explicit `board=iip` → allowed
- explicit `board=other` → BLOCKED, zero DB delta
- `HERMES_KANBAN_DB` pointing to other → BLOCKED
- terminal-tool CLI `hermes kanban create` with stale env → BLOCKED (hook on terminal tool or guard wrapper)
- hooks disabled → mutation blocked (safe-mode)
- gateway restart → `hermes hooks list` shows hook registered + healthy

---

## Design v2 (REWORK response)

### Mechanism change: hook on BOTH tool surfaces + deterministic startup pin

**v2 architecture:**

```
1. Deterministic startup pin (profile-level, no core patch):
   iip/org profiles: config `hooks` on_session_start → a small script that
   RE-PINS HERMES_KANBAN_BOARD=iip in the session env? 
   → F2 says on_session_start doesn't inject context; but it CAN run a command.
   Verify: can a shell hook modify parent env? NO (subprocess). So startup pin
   must come from: (a) board file = iip (already true), (b) explicit
   `export HERMES_KANBAN_BOARD=iip` in profile startup contract (AGENTS/capital-kanban),
   (c) hook that BLOCKS kanban mutations unless effective DB == iip.

2. pre_tool_call hook (fail_closed) on iip profile — matcher covers:
   - kanban_* in-agent tools (kanban_create, kanban_assign, kanban_complete, ...)
   - terminal tool invocations containing "hermes kanban" (create/assign/complete/...)
   Handler: parse stdin JSON → determine effective DB destination:
     - if tool is kanban_*: check tool_input.board (explicit override) + HERMES_KANBAN_DB env + HERMES_KANBAN_BOARD env + board file
     - if tool is terminal: check command string for "--board X" / "boards switch" / env
     - assert effective destination == iip board DB (kanban/boards/iip/kanban.db)
     - else {"decision":"block","reason":"Board safety: ..."}

3. hooks_auto_accept: true on iip profile (gateway/worker non-TTY needs it) + verify via hermes hooks list/doctor.

4. Safe-mode: if hook missing/failed → fail_closed:true means hook failure blocks;
   PLUS capital-kanban/AGENTS rule: "if hooks not registered (hermes hooks list shows none),
   do not create tasks — report to Founder".

5. Dispatcher/worker: already proven iip (Stage 3.2 C2 — dispatcher sets env per task; worker resolves iip). No change; add regression check.

6. Unrelated profiles: no hooks added → unaffected (req 10).
```

### Hook handler (bash, stdin JSON)

```bash
#!/usr/bin/env bash
# board-safety-hook.sh — pre_tool_call fail-closed guard
# stdin: {"hook_event_name":"pre_tool_call","tool_name":"...","tool_input":{...},...}
set -u
EXPECTED_DB="/c/Users/Admin/AppData/Local/hermes/kanban/boards/iip/kanban.db"
EXPECTED_BOARD="iip"
INPUT=$(cat)
TOOL=$(echo "$INPUT" | python -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null)
# only guard kanban mutations + terminal kanban CLI
case "$TOOL" in
  kanban_create|kanban_assign|kanban_complete|kanban_block|kanban_unblock|kanban_comment|kanban_link|kanban_archive|kanban_move|kanban_*)
    BOARD_ARG=$(echo "$INPUT" | python -c "import sys,json; d=json.load(sys.stdin); ti=d.get('tool_input') or {}; print(ti.get('board',''))" 2>/dev/null)
    DB_ARG=$(echo "$INPUT" | python -c "import sys,json; d=json.load(sys.stdin); ti=d.get('tool_input') or {}; print(ti.get('db',''))" 2>/dev/null)
    ;;
  terminal)
    CMD=$(echo "$INPUT" | python -c "import sys,json; d=json.load(sys.stdin); ti=d.get('tool_input') or {}; print(ti.get('command',''))" 2>/dev/null)
    case "$CMD" in
      *"hermes kanban"*create*|*"hermes kanban"*assign*|*"hermes kanban"*complete*|*"hermes kanban"*block*|*"hermes kanban"*unblock*|*"hermes kanban"*comment*|*"hermes kanban"*link*|*"hermes kanban"*archive*)
        BOARD_ARG=$(echo "$CMD" | grep -oE '\-\-board [a-z-]+' | awk '{print $2}')
        ;;
      *) exit 0 ;;  # non-kanban terminal command
    esac
    ;;
  *) exit 0 ;;  # non-kanban tool
esac
# resolve effective destination
RESOLVED_BOARD="${BOARD_ARG:-${HERMES_KANBAN_BOARD:-$(tr -d '[:space:]' < /c/Users/Admin/AppData/Local/hermes/kanban/current 2>/dev/null)}}"
DB_ENV="${HERMES_KANBAN_DB:-}"
if [ -n "$DB_ENV" ] && [ "$DB_ENV" != "$EXPECTED_DB" ]; then
  echo '{"action":"block","message":"Board safety: HERMES_KANBAN_DB points outside iip board DB"}'
  exit 0
fi
if [ "$RESOLVED_BOARD" != "$EXPECTED_BOARD" ]; then
  echo "{\"action\":\"block\",\"message\":\"Board safety: resolved board '$RESOLVED_BOARD' != '$EXPECTED_BOARD' — refusing kanban mutation\"}"
  exit 0
fi
exit 0  # allow (empty output = no-op)
```

### Config (iip profile)

```yaml
hooks:
  pre_tool_call:
    - matcher: "kanban_|hermes kanban"
      command: "C:/Users/Admin/Desktop/Antigravity/iip-harness-prep/scripts/board-safety-hook.sh"
      timeout: 10
      fail_closed: true
hooks_auto_accept: true
```

### Rollback

- Remove `hooks:` block + `hooks_auto_accept` from iip config → restore backup → hooks gone, board-guard.sh still available manually.
- Verify rollback: `hermes hooks list` shows zero hooks; kanban mutations revert to pre-guard behavior (with board file = iip still correct).

<!-- 2026-08-12 20:38:20 +0700 — captured via scripts/artifact_timestamp.py (system clock at write) -->
