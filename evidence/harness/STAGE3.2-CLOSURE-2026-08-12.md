# STAGE 3.2 — Closure Report (C1–C7)

**Status:** COMPLETE — Final Stage 3 verdict: **PASS** (upgraded from PASS WITH CONDITIONS)
**Date:** 2026-08-12
**Branch:** `harness/stage2-prep`
**Authorization:** Founder Stage 3.2 direction (C1–C7) — Stage 4 NOT authorized yet

---

## C1 — S3-F1 Root Cause + Fail-Closed Board Assertion ✅

**Root cause (exact source):** `hermes_cli/main.py:2445-2463` `_pin_kanban_board_env()` — at chat-session boot, if `HERMES_KANBAN_BOARD` is unset, Hermes pins the **then-current** board into the env var for the whole session. The Stage 3 session started (18:47) while the board file still said `other`, so every shell/CLI spawned from that session inherited `HERMES_KANBAN_BOARD=other`. `get_current_board()` precedence: env > `kanban/current` file → board switch later did NOT override the stale env. This is by-design session pinning (prevents mid-turn board flips, issue #20074), not a simple bug — the defect is a STALE pin when the board is switched after session start.

**Fail-closed guard (implemented):** `scripts/board-guard.sh`
- Rule: `expected_board=iip`; resolved from env → board file; if mismatch → EXIT 1, DO NOT create/dispatch.
- Test results: stale `other` env → **BLOCK** (exit 1) ✓ · `--force` → PASS ✓ · fresh shell (no env) → PASS (resolves board file=iip) ✓ · explicit `iip` env → PASS ✓ — **4/4**.
- Acceptance coverage (fresh shell/session/gateway/CLI/dispatcher/worker resolve board=iip) satisfied: C2 verified fresh gateway + dispatcher + worker all resolved iip; guard covers shell/CLI paths.

**Upstream fix:** deferred to Stage 4 (S3-F1 = proposed Stage 4 engineering pilot candidate). Mitigation is fail-closed, so no wrong-board task can be created silently.

## C2 — Real Gateway Restart Durability Test ✅ PASS

- Created benign blocked→ready task `t_86aa9e33` pre-restart; `hermes gateway restart` (PID 8060 → 43016, clean drain + respawn).
- **Verified:** board remained `Capital Intelligence`/iip · task persisted (status running→done, all fields intact) · dispatcher resumed (run 9, worker pid 8920, post-restart instance) · exactly ONE worker, no duplicate · no task redirected to board `other` (other DB count unchanged by the restart; the +1 was the pre-fix t_4c6afbcd from 19:16, not restart-related).
- **Evidence:** `boards/iip/kanban.db` read post-restart + run trail (run 9 completed 19:44).

## C3 — Intentional Orphan-Recovery Test ✅ PASS

- Created benign long-running task `t_3f678024` (max-runtime 300s) → worker run 10 (pid 19232) started.
- **Killed worker deliberately** (Stop-Process -Force) → orphan state (status=running, claim lock held, process dead).
- **Recovery observed:** dispatcher detected stale run → run 10 recorded `crashed` ("pid 19232 not alive") → task reconciled to `ready` → exactly ONE replacement worker (run 11, pid 37812) → verified marker file → **completed**. No storm, no duplicate workers.
- **Evidence:** runs trail: `1 crashed` + `2 completed`.

## C4 — Hermes Worker Docker Compatibility (A2) ✅ PASS → PRODUCTION READINESS

**Distinction recorded:**
- A1 Hard-isolation primitive = **PROVEN** (Stage 3 — mount isolation both directions).
- A2 Hermes worker Docker compatibility = **PROVEN (this closure)**.

**A2 test (real Kanban worker, `terminal.backend: docker`):**
- Created docker-test profiles (`harness-docker-test` mounts iip-test ONLY; `harness-docker-ipm` mounts ipm-test ONLY) — synthetic workspaces only, real IPM repo untouched.
- IIP worker container: sentinel-iip readable ✓ · `/workspace/ipm-test` absent (mount not provided) ✓ · python 3.11.15 ✓ · git 2.47.3 ✓ · node v20.20.2 ✓.
- IPM worker container (reverse): sentinel-ipm-readable ✓ · iip-test absent ✓.
- **Kanban worker e2e (task t_2835a77b, run 12):** spawned in docker (root, .dockerenv) → read iip sentinel → ipm isolated → python+git functional → heartbeat/comment/complete persisted back to `boards/iip/kanban.db` → **done**.
- **Operational cost:** daemon ~5s start; ~42MB/0.27% idle; image `nikolaik/python-nodejs:python3.11-nodejs20` (one-time pull); per-profile mount config contained.

**FILESYSTEM ISOLATION VERDICT — PRODUCTION READINESS: A (hard isolation available and adopted as target architecture).**

## C5 — Restore Pilot-Only Runtime Config ✅

| Profile | Stage 3 pilot state | Restored to | Kanban refs now |
|---|---|---|---|
| `org-cos` | kanban enabled | pre-Stage-3 backup | 2 (disabled) ✓ |
| `org-data-steward` | kanban enabled | pre-Stage-3 backup | 2 (disabled) ✓ |
| `ipm` | pilot model gpt-5.6-sol + kanban | pre-Stage-3 backup | 0 (clean) ✓ |
| `iip` | kanban enabled | **KEPT** (Stage 4 needs iip only) | 1 (enabled) ✓ |

- All YAML valid. `gpt-5.6-sol/openai-codex/high` remains PILOT model only — NOT production IPM decision (per Founder).
- Global FD #93 routing untouched (delegation = gpt-5.6-sol/high everywhere).
- Least privilege: only `iip` remains kanban-enabled for Stage 4.

## C6 — Stage 3 Evidence Language Amended ✅

`STAGE3-CLOSEOUT-2026-08-12.md` amended:
- **Impact:** "ZERO production impact" → **"ZERO canonical research/portfolio-state impact; bounded live runtime-config changes occurred for the technical pilot."**
- **Restart:** split into `DB persistence = PASS` + `Gateway restart recovery = PASS (C2-verified)`.
- **Orphan:** `no orphans observed` → `Orphan recovery = PASS (C3-verified)` with state transitions.
- **Docker:** `A1 = PROVEN` + `A2 = PROVEN (C4)` — verdict upgraded to PRODUCTION READINESS.
- **Timeout granularity recorded:** `configured max_runtime=5s; observed termination ≈60–61s` (dispatcher tick 60s) — max_runtime is NOT exact wall-clock; noted as S3-F4.
- Recommendation: **PASS WITH CONDITIONS → PASS**.

## C7 — Timestamp Safety Rule ✅

**Rule adopted (binding):**
1. `scripts/artifact_timestamp.py` may GENERATE or VERIFY timestamps only.
2. **PROHIBITED:** generic regex bulk replacement over historical provenance comments.
3. Historical timestamps may be corrected ONLY via targeted artifact/location changes with preserved correction evidence.

**M1 damage verification (git/backup comparison):**
- `operational/FOUNDERS-DECISIONS.md`: 21 historical footers intact + 1 M1 footer (FD-99 only) ✓ — restored from commit 765b24a, no unintended rewrite remains.
- Vault FD register: 2 footers (historical 2026-07-30 + M1 FD-99) ✓ — mid-file footer restored to original 2026-07-30.
- Stage 1–3 harness artifacts: each has exactly 1 M1 footer, `footer <= now` VERIFY=PASS (7/7) ✓.
- **Root cause of the earlier bulk damage:** the M1 correction script used `re.M|re.S` regex over whole files and rewrote every footer comment; fixed by restoring from git and re-applying targeted corrections. The new rule prevents recurrence.

---

## Final Stage 3 Verdict: **PASS**

All previously-pending evidence items (C2 restart recovery, C3 orphan recovery, C4 Docker worker A2) are now verified with real runtime evidence. S3-F1 mitigated fail-closed. Pilot-only configs restored. Stage 3 evidence language corrected.

**Stage 4 NOT started. STOP — awaiting Founder review.**

---
<!-- 2026-08-12 20:05:00 +0700 — M1: captured via scripts/artifact_timestamp.py (system clock at correction; agent-guessed timestamps rejected) -->
