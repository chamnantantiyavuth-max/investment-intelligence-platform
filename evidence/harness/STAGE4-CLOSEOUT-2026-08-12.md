# STAGE 4 — Project Workflow v3.8 Engineering Pilot: S3-F1 Board Safety Root Fix — CLOSEOUT

**Status:** COMPLETE — awaiting Founder review. v3.8 NOT promoted. v3.7.1 production unchanged.
**Date:** 2026-08-12
**Authorization:** FD #100 (Stage 4 = ONE bounded engineering pilot, 12 Aug 2026)
**Workflow used:** project-workflow v3.8 CANDIDATE (engineering/change-control scope)

---

## 1. Root-Cause Reproduction

- **Reproduced 2026-08-12:** `HERMES_KANBAN_BOARD=other hermes kanban create` → task `t_029e72a0` landed on board **other** (verified: iip DB 0 rows, other DB 1 row with the repro idempotency key). Archived as evidence.
- **Root cause (confirmed):** `hermes_cli/main.py:2445-2463` `_pin_kanban_board_env()` pins `HERMES_KANBAN_BOARD=<current board>` into env at **chat-session boot**. `get_current_board()` precedence: env → board file → default. A session started while board file said `other` keeps env=other for its whole life; `boards switch iip` fixes the file, not the inherited env. **Session pinning is intentional upstream behavior (issue #20074)** — per FD #100, Hermes core was NOT patched.

## 2. Alternatives Considered

| Alt | Mechanism | Verdict |
|---|---|---|
| A | `pre_tool_call` shell hook (fail_closed) | **ADOPTED (core of fix)** — automatic, agent-tool + terminal paths |
| B | `on_session_start` context injection | Rejected — v0.20.0 does not inject context on this event; advisory only |
| C | AGENTS/capital-kanban policy rule | **ADOPTED as companion** — covers operator CLI/shell paths (board-guard.sh) |
| D | CLI wrapper | Rejected — agent in-process tools bypass |
| E | Patch Hermes core `main.py` | **REJECTED per FD #100** (intentional upstream behavior) |

## 3. Engineering Review (independent, approved routing)

- **Reviewer:** Sol Medium via delegate_task (Engineering Council / Phase 2R equivalent) — **VERDICT: REWORK**
- **Material findings adopted:**
  - **F4 (High):** in-agent kanban tools expose explicit `board` input overriding env pin (`kanban_tools.py:215-227, 1674-1690`); `HERMES_KANBAN_DB` pins DB path directly and precedes board selection (`kanban_db.py:565-587`). Guard now derives the **actual effective DB destination** (tool board arg → env board → board file, plus HERMES_KANBAN_DB override check).
  - **F5 (High):** hook matcher/absence behavior — matcher covers `kanban_*` + terminal `hermes kanban` mutations; `fail_closed: true` blocks when hook missing/fails.
  - **F1:** terminal/CLI path guarded (terminal tool command inspection in hook).
  - **F3:** registration/consent — `hooks_auto_accept: true` + allowlist approved + `hermes hooks doctor` healthy (verified after gateway restart).
  - **F2:** on_session_start visibility dropped (doesn't inject context in v0.20.0).
  - **F6:** rollback section + test (below).

## 4. Exact Implementation Diff

**New files (harness worktree `iip-harness-prep`):**
```
scripts/board-safety-hook.sh      (3.0KB — pre_tool_call fail-closed guard)
scripts/stage4-acceptance.sh      (1.8KB — locked acceptance runner)
evidence/harness/STAGE4-DESIGN-S3F1-BOARD-SAFETY.md
evidence/harness/STAGE4-REWORK-RESPONSE-S3F1-v2.md
evidence/harness/STAGE4-DOCKER-PRODUCTION-PATTERN.md
evidence/harness/STAGE4-COMPARISON-V37-V38.md
```

**Config change (`profiles/iip/config.yaml`):**
```yaml
hooks:
  pre_tool_call:
  - matcher: kanban_|hermes kanban
    command: "C:/Program Files/Git/usr/bin/bash.EXE C:/Users/Admin/Desktop/Antigravity/iip-harness-prep/scripts/board-safety-hook.sh"
    timeout: 10
    fail_closed: true
hooks_auto_accept: true
```
- **Hook runtime fix discovered:** hook runner uses `subprocess.run(shell=False)` → bare `bash` resolves to WSL bash (can't read Windows paths); must use full git-bash path `C:/Program Files/Git/usr/bin/bash.EXE`. (WinError 193 / exit 127 during testing → fixed.)
- Backup: `profiles/iip/config.yaml.bak-2026-08-12-stage4`

## 5. Locked Acceptance Evidence

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | Fresh shell → iip | ✅ | `stage4-acceptance.sh` 5/5 PASS (baseline) |
| 2 | Fresh iip session → iip | ✅ | hermes run resolves iip |
| 3 | Fresh gateway → iip | ✅ | boards show = Capital Intelligence after restart |
| 4 | CLI create → iip | ✅ | live create t_25f6af1d landed iip (DB verified) |
| 5 | Agent kanban tool → iip | ✅ | hook allows board=iip / omitted board (T1, ACCEPT-1) |
| 6 | Dispatcher → iip | ✅ | runs on iip board throughout |
| 7 | Spawned worker → iip | ✅ | run 13/14 on iip (claim lock LAPTOP:45172) |
| 8 | Gateway restart → iip | ✅ | restart PID 15320/30424; board + hooks healthy |
| 9 | Stale/wrong board → fail closed | ✅ | NEG-1 board=other BLOCK; NEG-2 HERMES_KANBAN_DB BLOCK; NEG-3 terminal create stale BLOCK — zero DB delta |
| 10 | Unrelated projects unaffected | ✅ | no hook on capcmd/notebooklm/robot-trading; boards intact (verified list) |

**Extra review-required cases:** explicit `board=iip` allowed ✓ · `board=other` blocked zero delta ✓ · `HERMES_KANBAN_DB→other` blocked ✓ · terminal-tool CLI guarded ✓ · hooks-disabled safe-mode = `fail_closed` (block) ✓ · post-restart `hermes hooks doctor` healthy ✓

## 6. Regression / Security / Secret Scan

- **Regression:** unrelated boards untouched; iip board tasks intact (10 tasks); main repo tree untouched (9967459); worktree branch only.
- **Secret scan:** Docker test profiles (`harness-docker-test`, `harness-docker-ipm`) stripped of `.env` + `auth.json` (verified absent); no secret material in Stage 3/3.2/4 artifacts or git-tracked files (only `.env.example` template); production `iip/.env` intact (25,262 bytes).
- **Docker cleanup:** creds removed; profiles retained as reusable A2 test fixtures (no secrets, synthetic mounts only).

## 7. Rollback Evidence

- **Config:** restore `config.yaml.bak-2026-08-12-stage4` → remove `hooks:` block + `hooks_auto_accept` → hook gone.
- **Verified:** `hermes hooks list` shows 0 hooks after removal (rollback test done in C1 pattern; config backup restore proven Stage 3.2).
- **Board DB:** `kanban/backup-pre-stage3/` restorable; pilot tasks PILOT-NONCANONICAL only.
- **Worktree:** branch `harness/stage2-prep` — delete worktree + branch = full rollback.

## 8. New Findings

| ID | Severity | Description | Disposition |
|---|---|---|---|
| S4-F1 | Info | `HERMES_DELEGATED_CHILD_CONTEXT=1` in this session env blocks kanban mutation unless unset — a session-context quirk for harness operators | Documented; not a defect |
| S4-F2 | Medium (accepted) | Gateway restart kills in-flight worker; task claim held until `claim_expires` (~15 min) before dispatcher reconciles; operator can force re-dispatch via block/unblock (proven) | Operational-latency note for cutover; NOT board-safety related |

## 9. v3.7.1 vs v3.8 Comparison — see `STAGE4-COMPARISON-V37-V38.md`

**Summary:** 6 dimensions EQUAL (root-cause, scope, architecture, review, test strength, evidence, regression), 2 dimensions BETTER (context overhead, bureaucracy removed), overall confidence EQUAL. The pilot proves v3.8 removes targeted bureaucracy without degrading engineering quality.

## 10. Recommendation

**REVISE v3.8 — CONDITIONAL (promote after ≥1 more bounded engineering task).**
- v3.8 shape validated on this pilot; promotion needs one more engineering data point (consistent with v3.7.1's own evidence rule — no further governance change before 2–3 project evidence).
- S4-F2 accepted as operational latency, not defect.
- v3.7.1 remains production. Board safety now enforced automatically via hook (fail-closed).

**Stage 5 NOT started. STOP — awaiting Founder review.**

---
<!-- 2026-08-12 20:38:00 +0700 — captured at write time via scripts/artifact_timestamp.py -->
