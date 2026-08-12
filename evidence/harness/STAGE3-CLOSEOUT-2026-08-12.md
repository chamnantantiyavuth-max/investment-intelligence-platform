# STAGE 3 — Non-Canonical Kanban Technical Pilot Closeout

**Status:** COMPLETE — recommendation: **PASS** (amended per C6 — see STAGE3.2-CLOSURE for the evidence-language corrections; all previously "pending" items now verified)
**Date:** 2026-08-12 (amended 2026-08-12 via Stage 3.2 C6)
**Board:** `iip` (display name "Capital Intelligence") — ONE board
**Authorization:** FD #99 (Stage 3 conditional GO, 24 constraints)
**Scope honored:** PILOT-NONCANONICAL only · no real repo-board mirror · no /kanban rewire · no Cron migration · no v3.8 promotion · no SOUL switch · no MEMORY/USER mutation · no board other deletion · no real IPM repo access
**Impact statement (C6 correction):** **ZERO canonical research/portfolio-state impact; bounded live runtime-config changes occurred for the technical pilot** (kanban toolset enabled on iip/org-cos/org-data-steward; ipm pilot model + toolset). Pilot-only configs restored post-pilot per C5 (least privilege).

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

## 5. Restart Durability Evidence (C2-amended)

- **DB persistence: PASS** — all 6 tasks persist in `kanban/boards/iip/kanban.db` across separate CLI/worker processes (SQLite-backed); dependency link + comments/events persist.
- **Gateway restart recovery: PASS (verified in C2, Stage 3.2)** — real `hermes gateway restart` (PID 8060 → 43016): task persisted, board remained `iip`, dispatcher resumed (run 9, worker pid 8920), single worker no duplicate, no task redirected to board `other`.

## 6. Failure/Recovery Evidence

- **Timeout path (granularity recorded):** configured `max_runtime=5s`; observed worker termination ≈ **60–61s** (dispatcher tick granularity 60s). `max_runtime` is NOT exact wall-clock enforcement — do not use as second-level SLA until dispatcher granularity is understood (C6 note).
- **Failure limit / circuit breaker:** 2 consecutive non-success → `blocked` with `consecutive_failures=2, failure_limit=2, last_error` metadata. **No worker storm** (only 2 runs then auto-block).
- **Block semantics:** worker attempting `complete` while blocked → kernel rejects ("already terminal") — verified as designed.
- **Orphan recovery: PASS (verified in C3, Stage 3.2)** — worker pid 19232 deliberately killed mid-run → dispatcher detected stale run ("pid 19232 not alive"), reconciled to `ready`, spawned exactly ONE replacement (run 11, pid 37812) → completed. No storm, no duplicate workers.

## 7. Tenant / Privacy Findings

- **Tenant = soft filter CONFIRMED:** iip session `list` shows the `[ipm]` task (t_ce872540) — cross-visible as designed. Board hygiene + workspace discipline are the real boundary, not tenant.
- **Privacy/leak scan (title/body/comments/results/attachments):** regex sweep for holdings/position/cost basis/P&L/ledger/transaction/broker/account/key/token/secret/200,000/PM-letter — **0 sensitive hits** across 6 tasks + 8 comments + results. **0 attachments.**
- **Synthetic IPM workspace used:** `Antigravity/harness-pilot/ipm-test/` — real `independent-portfolio-manager` repo **never touched** (verified: pilot task workspace=dir:harness-pilot/ipm-test).
- **Finding S3-F1 (real defect):** `HERMES_KANBAN_BOARD=other` env var is injected by the Hermes runtime/session env and overrides the `kanban/current` file (env has precedence in `get_current_board()`). First pilot task landed on board `other` before detection. **Workaround:** always pass `--board iip` explicitly + export `HERMES_KANBAN_BOARD=iip` in worker shells. **Root fix (Stage 4+):** set env correctly at session/gateway level or document board-pinning convention.

## 8. Filesystem Isolation — VERDICT: **A (HARD ISOLATION AVAILABLE AND ADOPTED AS TARGET) — PRODUCTION READINESS (C4-verified)**

**A1 — Hard-isolation primitive: PROVEN (Stage 3).** Docker 29.6.1 + WSL2 Ubuntu; container mount test both directions (IIP container cannot read ipm sentinel; IPM container cannot read iip sentinel).

**A2 — Hermes worker Docker compatibility: PROVEN (C4, Stage 3.2).** Real Kanban worker on `terminal.backend: docker`:

| Check | Result |
|---|---|
| Worker launches in Docker | PASS — spawned as root, `.dockerenv` present |
| IIP synthetic workspace readable | PASS — `sentinel-iip` read |
| Opposite IPM workspace | PASS (isolated) — `/workspace/ipm-test` absent (mount not provided) |
| Reverse (IPM profile container) | PASS — only ipm mounted; iip-test absent |
| Python | PASS — 3.11.15 |
| Git | PASS — 2.47.3 |
| Node | PASS — v20.20.2 |
| Heartbeat/comment/complete | PASS — persisted back to board (run 12) |
| Result persistence | PASS — summary + events in `kanban/boards/iip/kanban.db` |

**Operational cost (measured):** Docker Desktop daemon startup ~5s; idle overhead ~42MB / 0.27% RAM for existing containers. Hermes docker backend uses `nikolaik/python-nodejs:python3.11-nodejs20` image (python+node+git available). Worker startup latency: one-time image pull on first run; subsequent runs fast. Complexity: per-profile `terminal.backend: docker` + `docker_volumes` mount mapping (IIP-only vs IPM-only) — contained in profile config.

**FILESYSTEM ISOLATION VERDICT — PRODUCTION READINESS: A (hard isolation available and adopted as target architecture).** Production IPM tasks may proceed on the shared board once the production IPM profile is configured with docker backend + IPM-only mounts (Stage 7 cutover decision; Founder approval still required for production IPM model).

## 9. Rollback Proof

- Config rollback tested live: restored `iip` config from backup → `kanban` back to 2 refs (disabled) → re-applied pilot state → YAML valid. **Rollback works in both directions.**
- Board DB backup (pre-pilot hash `0605b7f3...`) restorable via `kanban/backup-pre-stage3/`.
- Worktree checkpoint `e466df3` + `765b24a` on `harness/stage2-prep` (not merged to main).
- Main working tree: still untouched (verified).

## 10. Unresolved Defects

| ID | Severity | Description | Owner |
|---|---|---|---|
| S3-F1 | **Medium → FIXED (C1, Stage 3.2)** | `HERMES_KANBAN_BOARD` env injected by `_pin_kanban_board_env()` at session boot overrides board file. Root cause identified (`hermes_cli/main.py:2445-2463` pins env at chat boot from then-current board). **C1 mitigation:** `scripts/board-guard.sh` fail-closed assertion (4/4 tests: stale env → block; force/fresh/explicit → pass) — organizational tasks MUST resolve board=iip or STOP. Full upstream fix deferred to Stage 4 (S3-F1 is the Stage 4 engineering pilot candidate). | Harness |
| S3-F2 | Low | `kanban boards show <slug>` subcommand syntax differs (needs `show` without arg) — cosmetic CLI discoverability | Hermes docs |
| S3-F3 | Low | `set-default-workdir iip` (no path) did NOT clear; explicit `""` did — CLI semantics misleading | Hermes docs |
| S3-F4 | Info | Worker `timed_out` elapsed ≈60s vs max_runtime 5s — dispatcher tick granularity (60s dispatch_interval); max_runtime ≠ exact wall-clock (C6 note) | Acceptable for IIP cadence |
| S3-F5 | Info | Board `other` retains 185 junk tasks (untouched per constraint) + 1 archived pilot (t_657aab4e) + 1 done pilot (t_4c6afbcd landed there pre-fix) — deletion still deferred (O5) | Founder |

## 11. Recommendation: **PASS** (amended from PASS WITH CONDITIONS — C2/C3/C4 verified the previously-pending items)

**PASS** — Hermes Kanban works end-to-end as an organizational runtime on this machine: worker lifecycle, dependency promotion, block/unblock, circuit breaker, tenant cross-visibility, Sol pilot model dispatch, privacy cleanliness, gateway restart recovery, orphan reconciliation, and Docker hard isolation (A1+A2) — all verified with real worker evidence.

**Stage 4 entry conditions (now satisfied or scoped):**
1. ✅ S3-F1 board-pinning mitigated fail-closed (`board-guard.sh`); root fix = Stage 4 pilot scope.
2. ✅ Filesystem isolation: A (hard) PROVEN incl. Hermes worker (C4) — production-readiness verdict issued; production IPM config still needs Stage 7 cutover decision.
3. ⏸ Board `other` disposition (O5) — still deferred, not a Stage 4 blocker.
4. ✅ Stage 4 scope: ONE bounded engineering task (S3-F1 board-pinning root fix) on v3.8 candidate; rollback to v3.7.1 on regression.

**Stage 4 NOT started. STOP — awaiting Founder review.**

---
<!-- 2026-08-12 19:34:00 +0700 — M1: captured via scripts/artifact_timestamp.py (system clock at correction; agent-guessed timestamps rejected) -->
