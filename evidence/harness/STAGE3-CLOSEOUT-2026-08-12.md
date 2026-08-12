# STAGE 3 — Non-Canonical Kanban Technical Pilot Closeout

**Status:** COMPLETE — recommendation: **PASS WITH CONDITIONS** (see §11)
**Date:** 2026-08-12
**Board:** `iip` (display name "Capital Intelligence") — ONE board, ZERO production impact
**Authorization:** FD #99 (Stage 3 conditional GO, 24 constraints)
**Scope honored:** PILOT-NONCANONICAL only · no real repo-board mirror · no /kanban rewire · no Cron migration · no v3.8 promotion · no SOUL switch · no MEMORY/USER mutation · no board other deletion · no real IPM repo access

---

## 1. Exact Config Diffs

| Profile | Change | Backup |
|---|---|---|
| `iip` | disabled_toolsets: removed `kanban`; platform_toolsets.cli: added `kanban`; plugins.disabled: `[kanban]` → `[]` | `config.yaml.bak-2026-08-12-stage3` |
| `org-cos` | same 3 changes | `config.yaml.bak-2026-08-12-stage3` |
| `org-data-steward` | same 3 changes | `config.yaml.bak-2026-08-12-stage3` |
| `ipm` | added `model: gpt-5.6-sol/openai-codex/high` + `delegation` + `fallback` + platform_toolsets.cli incl. `kanban` (was: skills-only config) | `config.yaml.bak-2026-08-12-stage3` |
| Board `iip` | `default_workdir` → `null` (cleared); display name → "Capital Intelligence" | `kanban/backup-pre-stage3/` |

**Global config:** unchanged in Stage 3 (2A already fixed `gpt-5.6-sol`). v3.7.1, SOULs, MEMORY/USER, cron, frontend: **untouched**.

## 2. Backup Hashes (pre-pilot zero-state)

```
board iip kanban.db (pre)  : 0605b7f3186dee3d86a0... (backup: kanban/backup-pre-stage3/kanban.db.20260812-191319.bak)
board iip kanban.db (post) : 166cbccfc65c8d216c07...
board.json + config backups: kanban/backup-pre-stage3/ + profiles/*/config.yaml.bak-2026-08-12-stage3
```

## 3. Pilot Task Graph (all on board iip)

```
t_efb0c5cf  [iip]     PILOT 1 — worker lifecycle          → done
t_e793a387  [iip]     PILOT 2 parent                       → done
  └─ t_4511a056 [org-cos] child (task_links: parent→child) → done
t_828dc13b  [org-data-steward] PILOT 3 block/unblock       → done
t_1ecfaaef  [org-data-steward] PILOT 4 intentional failure → blocked (expected — failure_limit)
t_ce872540  [ipm]     PILOT 5 tenant (gpt-5.6-sol pilot)   → done
```
6 tasks · 1 dependency link · all PILOT-NONCANONICAL labeled.

## 4. Worker/Run Evidence

| Pilot | Runs | Outcome |
|---|---|---|
| 1 | 1 run, iip, 21s | completed — full lifecycle |
| 2 | parent 1 run (iip, 17s) + child 1 run (org-cos, 18s) | completed — dependency gate held child in todo, auto-promoted on parent done |
| 3 | run 4 (blocked) + run 5 (completed), org-data-steward | block → kernel rejected worker self-complete → unblock → re-claim → done |
| 4 | run 1 timed_out (60s>5s) + run 2 timed_out (61s>5s) | consecutive_failures=2 → failure_limit=2 → **auto-blocked** (circuit breaker) |
| 5 | 1 run, ipm, 1m, model_override=gpt-5.6-sol/openai-codex | completed — Sol pilot model confirmed in event record |

Worker spawn evidence: pid 41116 (P1), pid 27656 (P4 run 6), etc. Heartbeat + comment persistence verified in every run.

## 5. Restart Durability Evidence

- All 6 tasks persist in `kanban/boards/iip/kanban.db` across separate CLI/worker processes (SQLite-backed — durable by design; verified by independent DB read after worker processes exited).
- Dependency link persists in `task_links` table.
- Comments/events persist per task (verified counts).

## 6. Failure/Recovery Evidence

- **Timeout path:** worker exceeding `max_runtime` → dispatcher records `timed_out` with elapsed/limit → re-queued `ready` with retry.
- **Failure limit / circuit breaker:** 2 consecutive non-success → `blocked` with `consecutive_failures=2, failure_limit=2, last_error` metadata. **No worker storm** (only 2 runs then auto-block).
- **Block semantics:** worker attempting `complete` while blocked → kernel rejects ("already terminal") — verified as designed.
- **Orphan recovery:** no orphans observed in pilot window (dispatcher `reconcile_orphans` default on).

## 7. Tenant / Privacy Findings

- **Tenant = soft filter CONFIRMED:** iip session `list` shows the `[ipm]` task (t_ce872540) — cross-visible as designed. Board hygiene + workspace discipline are the real boundary, not tenant.
- **Privacy/leak scan (title/body/comments/results/attachments):** regex sweep for holdings/position/cost basis/P&L/ledger/transaction/broker/account/key/token/secret/200,000/PM-letter — **0 sensitive hits** across 6 tasks + 8 comments + results. **0 attachments.**
- **Synthetic IPM workspace used:** `Antigravity/harness-pilot/ipm-test/` — real `independent-portfolio-manager` repo **never touched** (verified: pilot task workspace=dir:harness-pilot/ipm-test).
- **Finding S3-F1 (real defect):** `HERMES_KANBAN_BOARD=other` env var is injected by the Hermes runtime/session env and overrides the `kanban/current` file (env has precedence in `get_current_board()`). First pilot task landed on board `other` before detection. **Workaround:** always pass `--board iip` explicitly + export `HERMES_KANBAN_BOARD=iip` in worker shells. **Root fix (Stage 4+):** set env correctly at session/gateway level or document board-pinning convention.

## 8. Filesystem Isolation — VERDICT: **A (HARD ISOLATION AVAILABLE) — Docker adopted as feasible**

Feasibility test executed (real containers, real sentinels):

```
Docker 29.6.1 + Docker Desktop (daemon starts in ~5s) — AVAILABLE
WSL2 Ubuntu default distro — AVAILABLE

IIP container (mounts ONLY iip-test):
  read iip sentinel        → sentinel-iip          ✓
  read ipm sentinel (rel)  → BLOCKED (not mounted) ✓
  read host ipm path       → BLOCKED (not mounted) ✓

IPM container (mounts ONLY ipm-test):
  read ipm sentinel        → sentinel-ipm-private  ✓
  read iip sentinel        → BLOCKED (not mounted) ✓
```

**Operational cost assessment:**
- Docker Desktop daemon startup ~5s; idle RAM overhead for existing containers ~42MB / 0.27% (measured `docker stats`); one existing unrelated container (`capital-circuit-research-lab-db-1`) untouched.
- **But:** Hermes terminal backend is currently `local` (all profiles). Workers run on host with full FS access today. Adopting Docker as the worker runtime requires a **terminal backend switch + per-profile mount mapping** — this is a Stage 4+ engineering change, NOT a Stage 3 pilot outcome.
- **Verdict:** Hard isolation via Docker is **feasible and demonstrated**. Residual risk TODAY (logical-only workers) remains; the path to hard isolation is concrete and tested. Founder acceptance of the transition plan is a Stage 4 decision.

## 9. Rollback Proof

- Config rollback tested live: restored `iip` config from backup → `kanban` back to 2 refs (disabled) → re-applied pilot state → YAML valid. **Rollback works in both directions.**
- Board DB backup (pre-pilot hash `0605b7f3...`) restorable via `kanban/backup-pre-stage3/`.
- Worktree checkpoint `e466df3` + `765b24a` on `harness/stage2-prep` (not merged to main).
- Main working tree: still untouched (verified).

## 10. Unresolved Defects

| ID | Severity | Description | Owner |
|---|---|---|---|
| S3-F1 | Medium | `HERMES_KANBAN_BOARD=other` env overrides board file — wrong-board task placement risk | Harness (Stage 4+) |
| S3-F2 | Low | `kanban boards show <slug>` subcommand syntax differs (needs `show` without arg) — cosmetic CLI discoverability | Hermes docs |
| S3-F3 | Low | `set-default-workdir iip` (no path) did NOT clear; explicit `""` did — CLI semantics misleading | Hermes docs |
| S3-F4 | Info | Worker `timed_out` elapsed ≈60s vs max_runtime 5s — dispatcher tick granularity (60s dispatch_interval) means sub-60s runtime caps round up | Acceptable for IIP cadence |
| S3-F5 | Info | Board `other` retains 185 junk tasks (untouched per constraint) + 1 archived pilot (t_657aab4e) — deletion still deferred (O5) | Founder |

## 11. Recommendation: **PASS WITH CONDITIONS**

**PASS** — Hermes Kanban works end-to-end as an organizational runtime on this machine: worker lifecycle, dependency promotion, block/unblock, circuit breaker, tenant cross-visibility, Sol pilot model dispatch, privacy cleanliness, rollback — all verified with real worker evidence.

**Conditions for Stage 4 (v3.8 engineering pilot):**
1. Resolve S3-F1 board-pinning (env var) before multi-board production traffic.
2. Decide filesystem isolation transition: adopt Docker worker backend (hard isolation proven) or Founder-accept logical-only with documented residual risk.
3. Review board `other` disposition (O5) — still deferred.
4. Apply Stage 4 scope: ONE bounded engineering task on v3.8 candidate; rollback to v3.7.1 on regression.

**Stage 4 NOT started. STOP — awaiting Founder review.**

---
<!-- 2026-08-12 19:34:00 +0700 — M1: captured via scripts/artifact_timestamp.py (system clock at correction; agent-guessed timestamps rejected) -->
