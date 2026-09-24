# C+ Cron Operations Runbook — POST-M5.3 O3 R0.1 (FD #142)

Status: **R0.1 CORRECTION COMPLETE** — bounded implementation correction (24 Sep
2026, Founder independent source review: `R0 NOT YET ACCEPTED`; R0.1 does NOT
reopen FD #142 architecture / M5.3 / D-0 / C0 / P1 policy / Learning Loop
authority). M5.3 permanently `FOUNDER ACCEPTED / CLOSED / FROZEN` (FD #141).
M6 remains PARKED until clean-cycle gate G is satisfied.

## 1. Hard invariants

- BACKGROUND CRON NEVER MUTATES GOVERNED `main` (origin/main writable only through
  explicit interactive/governed work).
- Hard rule: no `git reset --hard` over an ahead/diverged ops worktree; never
  discard unresolved local artifacts; never `git add -A`; never push main from cron;
  sync arrow main -> ops only.
- Denylist hit = FAIL CLOSED; allowlist PASS never overrides; unknown path = FAIL.
- Learning Loop has ZERO repository write authority (any repo delta = FAIL).
- No Hermes scheduler patch (D-0); no `hermes update` in O3; gateway left untouched (C0).

## 2. Layout

| Role | Location |
|---|---|
| Governed repo | `C:\Users\Admin\Desktop\Antigravity\investment-intelligence-platform` (main) |
| Automation worktree | `C:\Users\Admin\Desktop\Antigravity\investment-intelligence-platform-ops` (branch `ops/automation`) |
| Scheduler state | `<HERMES_HOME>/ops-state/ops-state.json` (outside repo — never breaks G0 cleanliness) |
| Ops tooling | `scripts/ops/` (deterministic, fail-closed; see `scripts/ops/README.md`) |

## 3. Cron jobs (IIP profile; all PAUSED during R0 implementation)

| Job | Class | Schedule | Artifact allowlist (anchored) | Write surface |
|---|---|---|---|---|
| `8ba233e88015` Weekly Radar | scanner | Mon 08:00 UTC+7 | `evidence/radar/digests/\d{4}-\d{2}-\d{2}-radar-digest\.md` | ops worktree only |
| `cda817d17236` Radar Mid-Week | scanner | Thu 08:00 UTC+7 | `evidence/radar/digests/\d{4}-\d{2}-\d{2}-radar-midweek\.md` | ops worktree only |
| `8b1cd19aba7d` CIW MSFT monitor | artifact | Mon 09:00 UTC+7 | `docs/ciw-pilot-msft/monitoring/\d{4}-\d{2}-\d{2}-monitoring-draft\.md` | ops worktree only |
| `73e611584447` Nick-Weekly AM SRL | artifact | Sat 09:00 UTC+7 | `operational/self-reflection-logs/\d{4}-\d{2}-\d{2}-run-AM-V0-\d{8}-\d{6}\.md` | ops worktree only |
| `1f5f03f9236d` Daily Learning Loop | observer | 19:00 UTC+7 | NONE — no repository output | read-only; delivery `local` |

External side effects (recorded separately, NOT governed by the repo allowlist):
- Radar jobs: kanban Task Idea Cards (external kanban writes allowed; digest is the
  repo artifact). Weekly Radar also produces `kanban/digests/` digest copies (kanban
  output path, outside repo allowlist).
- CIW: none beyond the monitoring-draft.
- AM: none beyond the SRL.
- Learning Loop: nothing — observer only (cron runs/incidents/stuck claims/delivery
  truth observations reported via delivery=local).

## 4. Per-run sequence (in the automation worktree)

```
g0 = python scripts/ops/g0_check.py        # EXIT 0 (case A/B) else DO NOT RUN
sync = python scripts/ops/sync_main_to_ops.py   # S0/S1/S2/S3 lifecycle, persists OPS_SYNC_BASE_SHA
<job executes its pipeline; writes ONLY its allowlisted artifact>
v = python scripts/ops/validate_delta.py --job <id>   # EXIT 0 else FAIL CLOSED
c = python scripts/ops/commit_push_ops.py --job <id>  # explicit-path commit + push + verify
```

Never skip a step; never bypass validation to "make the run pass".

### 4.1 Sync lifecycle S0/S1/S2/S3 (R0.1, 24 Sep 2026)

OPS_AHEAD is the NORMAL state after any cron artifact commit, not an error.

| Case | Condition | Behavior | Base |
|---|---|---|---|
| S0 SAME | `ops == main` | no-op | ops HEAD |
| S1 MAIN AHEAD | `ops` ancestor of `main` | fast-forward ops to main, **push + remote-verify** | resulting ops HEAD |
| S2 OPS AHEAD | `main` ancestor of `ops` | NO merge, NO reset — artifact history preserved | current ops HEAD |
| S3 DIVERGED | neither ancestor | normal `main -> ops` merge in the OPS worktree ONLY; clean → **push + remote-verify**; conflict → abort, verify clean, preserve pre-merge ops HEAD, FAIL CLOSED | merged ops HEAD |

- **Remote-first:** before evaluating main vs ops, local ops is `--ff-only`'d to
  `origin/ops/automation` and verified equal (G0 case B is performed here).
  Diverged local/remote ops = G0 case D block; sync never resolves it silently.
- **Durable baseline:** when S1/S3 changes ops HEAD, sync PUSHES and remote-verifies
  the new baseline BEFORE storing OPS_SYNC_BASE_SHA. An unpushed sync commit never
  creates an unexplained G0 case C after a mid-run job failure.
- Arrow is ALWAYS main -> ops. Never reverse, never rebase, never rewrite history.

## 5. Incident responses

- Push failure: artifact commit PRESERVED. Next G0 = case C → refuses new runs.
  Recovery: `git push origin ops/automation` (exact existing commit) → verify remote
  == local → only then may the next run begin. NEVER reset.
- Dirty/untracked residue after a run: G0 case E → preserve, surface, do not clean
  automatically.
- Stuck `fire_claim` / "running" execution: recovery is native (pending_slot +
  stale in-flight sweep, min 30 min); verify via `hermes cron status` /
  `hermes cron doctor` / `hermes cron runs`. Do NOT hand-edit jobs.json.
- Gateway down / late catch-up: native keep-alive + catch_up_missed; late-but-
  exactly-once with truthful lateness is operationally CLEAN (C0; power-off cycles
  are exceptions recorded as such).

## 6. Resume order (after R0 dry/canary verification)

1. nearest scheduled artifact job (e.g. Mid-Week Radar Thu)
2. second artifact job, different class (e.g. Nick-Weekly Sat)
3. observe both executions; only then
4. remaining artifact jobs (Weekly Radar Mon, CIW Mon)
5. Learning Loop LAST (observer; never counts toward the two clean artifact cycles)

Clean-cycle gate G: 2 CONSECUTIVE CLEAN SCHEDULED EXECUTIONS from >= TWO distinct
artifact-producing job classes; main SHA unchanged throughout both; each artifact
lands on ops + pushed + allowlist/denylist pass + no orphan/untracked + truthful
lateness; plus >= ONE successful end-to-end P1 batch promotion (canary-verified).

## 7. P1 promotion (interactive; Founder-approved batch; P2 NOT authorized)

1. Interactive review: `python scripts/ops/generate_promotion_manifest.py --from <base> --to <head> [--job <id> ...]`
   → `ops/manifests/<id>.json`. TWO or more job classes may share one batch (e.g.
   Radar + AM); every artifact's owning job is DERIVED mechanically from the
   anchored allowlists (0 matches = FAIL, >1 = FAIL ambiguous; `--job` is an
   optional expected-owner validation constraint only). Per-artifact
   `source_commit` = the actual latest commit in `base..head` touching that path;
   `sha256` = SHA-256 over the exact RAW `git show <source_commit>:<path>` blob
   bytes (binary — no text decode, no newline conversion, no errors=replace);
   `run_timestamp` = source commit committer time (mechanical provenance); PIT
   only when provided. Denylist/allowlist re-checked per artifact (fail-closed).
2. Founder approves the manifest (one approval = whole batch; `disposition` → APPROVED).
3. `python scripts/ops/promote_batch.py --manifest <path> --target-branch <b> [--push]`
   — TOCTOU: current origin/main must equal `manifest_main_sha` else HOLD (revalidate).
   R0 canary uses a temporary branch; real P1 uses `main` + `--into-primary` after approval.
   Per artifact: frozen blob verified at its REAL source_commit, hash recomputed on
   the same raw-blob definition, target path re-validated against THAT artifact's
   owning job (authority never widened by a multi-job batch), exact bytes transfer,
   post-commit hash re-verify.
4. Promotion record = normal governed main commit (files + receipt). Ops merge history
   never imported; no broad cherry-pick. Newer ops artifacts are never implicit.
5. `last_promoted_ops_sha` (external ops state) advances ONLY after a Founder-approved
   REAL P1 promotion into main succeeds — never on canary, manifest generation, or
   cron artifact commits. It defines the next batch range.
6. On success the interactive manifest is removed from the automation working tree
   (residue); `ops/manifests/` is gitignored and is NEVER a cron allowlist. G0 must
   return clean before scheduled cron resumes.

## 8. Maintenance mode (P2 design)

Promotion refused when `OPS_MAINTENANCE_MODE=ON` (env) or IIP profile config
`ops.maintenance_mode` = on. Lock lives OUTSIDE governed main (profile/runtime state)
so entering/exiting maintenance never requires a main commit. Artifact jobs continue
on ops; no promotion; no artifact loss; state remains auditable.

## 9. Verification

- Ops tooling: `python -m pytest tests/ops/test_ops_tooling.py -q --basetemp <scratch>`
  (41 tests; temp git repos only — never the real worktree/remote). R0.1 matrix:
  T1/T2 sequential ops-ahead lifecycle (the previously-missing acceptance
  scenario), T3 remote-ops-first, T4 durable S1 push, T5 clean-divergence merge,
  T6 conflict abort, T7 sync push-failure preserve+block, M1/M2 multi-job
  manifests, M3 unknown path FAIL, M4 ambiguous ownership FAIL, M5 deletion FAIL,
  M6 rename FAIL, M7 raw CRLF/latin-1 blob hash, M8 frozen head, canary-vs-real
  last-promoted semantics, owner-scope, real-source-commit blob, residue removal.
- Full suite: `python -m pytest` (must stay green; no M5.3 semantic changes).
  R0.1 gate: 813 passed (795 R0 + 18 net new ops tests).
- Gate: `bash scripts/gate-check.sh` (all gates incl. verification-tag on the
  closeout commit) + `bash scripts/isolation-scan.sh` (clean tree).

## 10. P1 hash semantics (Windows CRLF note)

- Manifest `sha256` is computed from the **raw git blob** (`git show <commit>:<path>`
  in BINARY mode — `run_git_bytes`, no text decode, no newline conversion, no
  `errors=replace`), NOT from the working-tree file and NOT from a text-mode
  re-encode. On Windows `core.autocrlf`/`.gitattributes` can convert LF→CRLF on
  checkout, so the on-disk bytes may differ from the blob — that is expected and
  irrelevant to promotion integrity. Blob bytes are authoritative (R0.1 §9).
- Promotion recomputes the same raw-blob hash at each artifact's REAL `source_commit`,
  transfers the exact bytes, and re-verifies post-commit hashes via the same binary
  read; a mismatch (altered artifact) fails closed.

<!-- 2026-09-24 12:50 UTC+7 (R0.1 correction closeout) -->