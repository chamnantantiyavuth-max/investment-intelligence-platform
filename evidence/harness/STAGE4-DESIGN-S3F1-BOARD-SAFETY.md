# STAGE 4 — S3-F1 Board Safety Root Fix: Design & Alternatives

**Stage:** 4 (Project Workflow v3.8 Engineering Pilot — ONE bounded task)
**Date:** 2026-08-12
**Status:** Design for Independent Engineering Review (material engineering gate — approved independent-review routing)
**v3.8 status:** CANDIDATE — not promoted. v3.7.1 production unchanged.

---

## 1. Problem (S3-F1) — reproduced

**Root cause (verified):** `hermes_cli/main.py:2445-2463` `_pin_kanban_board_env()` pins `HERMES_KANBAN_BOARD=<current board>` into the env at **chat-session boot**. `get_current_board()` precedence is env → board file → default. A session started while the board file said `other` keeps `HERMES_KANBAN_BOARD=other` for its whole life; `hermes kanban boards switch iip` fixes the file but NOT the inherited env. Every shell/CLI/agent-tool call from that session then resolves board `other`.

**Reproduction (2026-08-12):** `HERMES_KANBAN_BOARD=other hermes kanban create ...` → task `t_029e72a0` landed on board `other` (verified: iip DB 0 rows, other DB 1 row with the repro idempotency key). Archived as evidence.

**Upstream intent:** session pinning is deliberate (issue #20074 — prevents mid-turn board flips when another session switches the file). Treat as intentional upstream behavior. **Do NOT patch Hermes core `main.py` in this pilot.**

## 2. Requirements (from FD #100 locked acceptance)

| # | Acceptance | Meaning |
|---|---|---|
| 1 | Fresh shell → iip | new shell resolves board iip for IIP org work |
| 2 | Fresh iip session → iip | new `hermes -p iip` session pins iip |
| 3 | Fresh gateway → iip | gateway board resolution = iip |
| 4 | CLI task create → iip | `hermes kanban create` in IIP context lands iip |
| 5 | Agent kanban tool mutation → iip | in-agent `kanban_*` tool calls resolve iip |
| 6 | Dispatcher → iip | dispatch claims/workers on iip |
| 7 | Spawned worker → iip | worker env resolves iip |
| 8 | Gateway restart → iip | survives restart |
| 9 | Stale/wrong board state → fail closed | never silently write elsewhere; resolve iip or BLOCK |
| 10 | Unrelated projects unaffected | capital-command / notebooklm / robot-trading boards NOT forced to iip |

## 3. Architecture Alternatives

### A — Shell hook `pre_tool_call` + `fail_closed: true` (RECOMMENDED)
- Hermes v0.20.0 shell hooks (`config.yaml hooks:` block) fire on `pre_tool_call` with JSON stdin, can **block** the tool call; `fail_closed: true` makes a hook failure block by default.
- Add to IIP/org profiles: a `board-guard-hook` that inspects `tool_name` (kanban_*) + resolved board; if board ≠ iip → `{"decision":"block","reason":"..."}`.
- **Automatic** — fires on every agent tool mutation, no operator memory required (satisfies FD #100 directive 4).
- Local harness only (script in harness workspace + config hook), zero Hermes-core change.
- Works CLI + Gateway (shell hooks registered in both — hooks.md:1350).
- Caveat: hooks require consent/first-use approval (`hooks_auto_accept` or stored allowlist); gateway/non-interactive runs need `HERMES_ACCEPT_HOOKS=1` or pre-approved allowlist. Must verify on this install.

### B — `on_session_start` hook (context injection + env sanity)
- Shell hook on `on_session_start` injects a context note ("resolved board = X; expected iip") into the session.
- **Cannot set parent-process env** (subprocess), so it cannot re-pin `HERMES_KANBAN_BOARD`. Advisory only.
- Usable as a companion to A (visibility), not a fix alone.

### C — Profile-startup contract (SOUL/AGENTS/PRINCIPAL rule)
- Encode in IIP AGENTS + capital-kanban skill: "every org task must pass `board-guard.sh` / resolve iip before create".
- Zero runtime change; pure policy. **Not automatic enforcement** — depends on agent compliance. Insufficient alone (founder: "not merely a script the operator must remember").

### D — CLI wrapper (alias/wrapper script `hermes-kanban-iip`)
- Wrap `hermes kanban create/assign/...` to export `HERMES_KANBAN_BOARD=iip` + assert.
- Covers shell/CLI paths only; **agent in-process `kanban_*` tools bypass it**. Partial.

### E — Upstream fix to `_pin_kanban_board_env()` (REJECTED for this pilot)
- E.g. re-pin on every board-sensitive call, or make env pin relative to task context.
- Touches Hermes core; FD #100 says do NOT rush patching core; treat pinning as intentional. Defer to Hermes upstream discussion.

## 4. Recommended Composition (smallest safe fix)

```
A (pre_tool_call fail-closed hook)  → automatic enforcement for agent tool mutations
+ C (AGENTS/capital-kanban rule)    → policy for CLI/shell paths (board-guard.sh already exists)
+ B (on_session_start context)      → visibility
```

- Hook script: reuse `scripts/board-guard.sh` logic as a hook handler (stdin JSON → tool_name check → board resolve → block/allow).
- Config change: `hooks:` block in iip profile (and later org profiles when re-enabled). Unrelated profiles get NO hook → requirement 10 preserved.
- Dispatcher/worker (6,7,8): already verified iip in Stage 3 (dispatch sets env per task — kanban_watchers.py:1416); no change needed.

## 5. Locked Acceptance Test Plan (mapped to §2)

1. fresh shell: `env -u HERMES_KANBAN_BOARD bash scripts/board-guard.sh` → PASS(iip)
2. fresh session: `hermes --profile iip ... config get kanban` resolves iip board file
3. fresh gateway: `hermes gateway restart` → board stays iip (re-run C2 pattern)
4. CLI create (no stale env): lands iip
5. agent kanban tool with stale env: hook BLOCKS (fail-closed) — negative test
6. dispatcher claim → iip (run evidence)
7. worker spawn → iip (run evidence)
8. restart → iip
9. negative: `HERMES_KANBAN_BOARD=other` + agent tool → BLOCKED, nothing written to other
10. unrelated profile (capcmd) creates task → lands on its own board, not iip

## 6. Engineering Review Request

Review this design against: (a) completeness of the 10 acceptance criteria, (b) hook fail-closed semantics on v0.20.0 (verify schema/behavior claims), (c) whether composition A+C+B is minimal and safe, (d) any missing negative/regression case, (e) rollback sufficiency. Verdict: PASS / PASS WITH FIXES / REWORK.

<!-- 2026-08-12 20:38:20 +0700 — captured via scripts/artifact_timestamp.py (system clock at write) -->
