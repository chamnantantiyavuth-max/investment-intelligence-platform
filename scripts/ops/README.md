# C+ Ops Tooling — scripts/ops/

Deterministic, fail-closed operational tooling for the `ops/automation` cron write
architecture (FD #142 — POST-M5.3 O3 Final Founder Ruling, 23 Sep 2026).

Hard invariants (FD #142):
- Background cron NEVER mutates governed `main`.
- Never `git reset --hard` over an ahead/diverged ops worktree; never discard
  unresolved local artifacts.
- Never `git add -A`; never push main from cron; arrow main -> ops only.
- Denylist hit = FAIL CLOSED; an allowlist PASS never overrides a denylist hit.
- All hashes/manifest values mechanical (SHA-256), no LLM-authored values.

## Components

| Script | Role |
|---|---|
| `ops_config.py` | Single authority: anchored job allowlists + absolute denylist + state file |
| `ops_git.py` | Fail-closed git subprocess wrapper |
| `g0_check.py` | G0 preservation gate — cases A (equal/clean), B (behind ff-ready), C (ahead = push-fail BLOCK), D (diverged FAIL), E (dirty FAIL+preserve) |
| `sync_main_to_ops.py` | origin/main -> ops/automation fast-forward only; captures `OPS_SYNC_BASE_SHA` |
| `validate_delta.py` | Cron-delta authority: validates only `OPS_SYNC_BASE_SHA -> job-produced state` |
| `commit_push_ops.py` | Explicit-path stage -> commit -> push ops -> fetch -> verify remote SHA |
| `generate_promotion_manifest.py` | Deterministic P1 manifest (interactive only) |
| `promote_batch.py` | Exact-content promotion w/ TOCTOU HOLD; R0 = temp/canary branch only |

## Per-job anchored artifact allowlists (fullmatch, POSIX-rel)

- Weekly Radar `8ba233e88015`: `^evidence/radar/digests/\d{4}-\d{2}-\d{2}-radar-digest\.md$`
- Mid-Week Radar `cda817d17236`: `^evidence/radar/digests/\d{4}-\d{2}-\d{2}-radar-midweek\.md$`
- CIW MSFT `8b1cd19aba7d`: `^docs/ciw-pilot-msft/monitoring/\d{4}-\d{2}-\d{2}-monitoring-draft\.md$`
- AM SRL `73e611584447`: `^operational/self-reflection-logs/\d{4}-\d{2}-\d{2}-run-AM-V0-\d{8}-\d{6}\.md$`
- Learning Loop `1f5f03f9236d`: NO REPOSITORY OUTPUT (observer/reconciler only)

Do NOT widen a pattern to make a run pass — a new artifact class requires explicit
Founder authorization (HOLD).

## Cron run sequence (per scheduled job, in the ops worktree)

1. `python scripts/ops/g0_check.py` — must exit 0 (case A/B) else DO NOT RUN.
2. `python scripts/ops/sync_main_to_ops.py` — fast-forward, persists OPS_SYNC_BASE_SHA.
3. Job executes; writes ONLY its allowlisted artifact(s).
4. `python scripts/ops/validate_delta.py --job <id>` — must exit 0.
5. `python scripts/ops/commit_push_ops.py --job <id>` — explicit-path commit + push + verify.
6. Next run starts again at G0.

Push failure → the script preserves the local commit and exits non-zero; the next
G0 sees case C and refuses a new job until the exact commit is pushed. NEVER reset.

## P1 promotion (interactive, Founder-approved batch)

1. Interactive review session: `generate_promotion_manifest.py --job <id> --from <base> --to <head>`
   → writes `ops/manifests/<id>.json` on ops.
2. Founder approves the manifest batch (one approval = whole batch).
3. Exact content promotion: `promote_batch.py --manifest <path> --target-branch <branch> [--push]`
   (R0 canary uses a temporary branch; real P1 uses `main` with `--into-primary` after approval).
   TOCTOU: current main must equal `manifest_main_sha`, else HOLD exit 2.
4. Promotion record = normal governed main commit (artifacts + receipt); ops merge
   history is never imported.

## State

Persistent scheduler state lives OUTSIDE the repo (never breaks G0 cleanliness):
`<HERMES_HOME>/ops-state/ops-state.json` (`OPS_STATE_DIR` overrides; tests use tmp).

## Tests

`pytest tests/ops/test_ops_tooling.py -q` — full-matrix on temp git repos;
never touches the real worktree/remote.

## Maintenance mode (P2, design-only)

Promotion is refused when env `OPS_MAINTENANCE_MODE=ON` or the IIP profile config
key `ops.maintenance_mode` is set — lock lives outside governed main.

<!-- 2026-09-23 15:00 UTC+7 -->