# Stage 4b — Live Hook Re-Verify (Fresh Process) — PASS

- Date: 2026-08-12 20:38 UTC+7
- Worker: iip (kanban task t_b1382bfc, run 16)
- Session: 20260812_203743_6a377e (fresh process spawned AFTER config fix)
- Hook: pre_tool_call -> C:/Program Files/Git/usr/bin/bash.EXE C:/Users/Admin/Desktop/Antigravity/iip-harness-prep/scripts/board-safety-hook.sh
- Matcher: `kanban_.*|terminal` (fixed from fullmatch bug in Stage 4)
- fail_closed: true, hooks_auto_accept: true, timeout: 10s

## Checks

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `hermes hooks list` | PASS — "✓ allowed" (auto re-approval on fresh boot) | hooks list output; agent.log line 28308 (auto-approved 20:37:43) |
| 2 | Negative control: kanban_create(title="[PILOT-4B] must-block", board="other") | PASS — BLOCKED, fail-closed | Tool error: "Board safety: resolved board 'other' != expected 'iip' — refusing kanban mutation"; 0 matches for title in all 6 board DBs |
| 3 | Positive control: kanban_create(title="[PILOT-4B] iip-probe", board="iip") | PASS — allowed, card t_35fe9e83 | Landed in boards/iip/kanban.db only; absent from all other board DBs |
| 4 | Firing evidence in agent.log (session 20260812_203743_6a377e) | PASS | 20:37:43 hook registered (matcher kanban_.*|terminal); 20:37:57 block WARNING; 20:38:14 kanban_create completed (allowed); ~0.46s latency/call consistent with hook firing |
| 5 | Cleanup | DONE | t_35fe9e83 set status='done' + task_events 'completed' row inserted directly in iip/kanban.db |
| 6 | Verdict | **PASS** | Hook blocked in step 2 → PASS per protocol |

## Board DBs scanned (6)

- capital-command/kanban.db — no [PILOT-4B] cards
- default/kanban.db — empty (no tables)
- iip/kanban.db — probe card t_35fe9e83 only (cleaned)
- notebooklm-kb/kanban.db — none
- other/kanban.db — none
- robot-trading/kanban.db — none

## Agent.log evidence (session 20260812_203743_6a377e)

```
20:37:43,564 INFO  agent.shell_hooks: shell hook auto-approved via --accept-hooks / env / config: pre_tool_call -> .../board-safety-hook.sh
20:37:43,564 INFO  agent.shell_hooks: shell hook registered: pre_tool_call -> .../board-safety-hook.sh (matcher=kanban_.*|terminal, timeout=10s, fail_closed=True)
20:37:57,055 WARNING agent.tool_executor: Tool kanban_create returned error (0.46s): {"error": "Board safety: resolved board 'other' != expected 'iip' — refusing kanban mutation"}
20:38:14,721 INFO  agent.tool_executor: tool kanban_create completed (0.49s, 149 chars)
```

## Conclusion

The board-safety hook is ACTIVE in a fresh worker process: fixed matcher registers at boot, auto-approval works, cross-board mutation is fail-closed (negative blocked, no card anywhere), and legitimate iip-board mutation is allowed. Stage 4's "inert hook" defect is confirmed fixed in a clean process.
