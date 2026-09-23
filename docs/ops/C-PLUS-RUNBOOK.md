# C+ Cron Operations Runbook — POST-M5.3 O3 R0 (FD #142)

Status: **R0 IMPLEMENTED** — operational authority: FD #142 (Final Founder Ruling,
23 Sep 2026). M5.3 permanently `FOUNDER ACCEPTED / CLOSED / FROZEN` (FD #141).
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
sync = python scripts/ops/sync_main_to_ops.py   # fast-forward, persists OPS_SYNC_BASE_SHA
<job executes its pipeline; writes ONLY its allowlisted artifact>
v = python scripts/ops/validate_delta.py --job <id>   # EXIT 0 else FAIL CLOSED
c = python scripts/ops/commit_push_ops.py --job <id>  # explicit-path commit + push + verify
```

Never skip a step; never bypass validation to "make the run pass".

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

1. Interactive review: `python scripts/ops/generate_promotion_manifest.py --job <id> --from <base> --to <head>`
   → `ops/manifests/<id>.json` (SHA-256 mechanical; allowlist/denylist re-checked).
2. Founder approves the manifest (one approval = whole batch; `disposition` → APPROVED).
3. `python scripts/ops/promote_batch.py --manifest <path> --target-branch <b> [--push]`
   — TOCTOU: current origin/main must equal `manifest_main_sha` else HOLD (revalidate).
   R0 canary uses a temporary branch; real P1 uses `main` + `--into-primary` after approval.
4. Promotion record = normal governed main commit (files + receipt). Ops merge history
   never imported; no broad cherry-pick. Newer ops artifacts are never implicit.

## 8. Maintenance mode (P2 design)

Promotion refused when `OPS_MAINTENANCE_MODE=ON` (env) or IIP profile config
`ops.maintenance_mode` = on. Lock lives OUTSIDE governed main (profile/runtime state)
so entering/exiting maintenance never requires a main commit. Artifact jobs continue
on ops; no promotion; no artifact loss; state remains auditable.

## 9. Verification

- Ops tooling: `python -m pytest tests/ops/test_ops_tooling.py -q --basetemp <scratch>`
  (23 tests; temp git repos only — never the real worktree/remote).
- Full suite: `python -m pytest` (must stay green; no M5.3 semantic changes). R0 gate: 795 passed.
- Pre-resume dry/canary: see SESSION_CLOSEOUT.md R0 record (G0 states, allowlist
  fixture, denylist refusal, push-failure preserve, manifest freeze, TOCTOU HOLD,
  exact-content promotion on a TEMPORARY canary branch — not governed main).

## 10. P1 hash semantics (Windows CRLF note)

- Manifest `sha256` is computed from the **git blob** (`git show <commit>:<path>`),
  NOT from the working-tree file. On Windows `core.autocrlf`/`.gitattributes` can
  convert LF→CRLF on checkout, so the on-disk bytes may differ from the blob — that
  is expected and irrelevant to promotion integrity.
- Promotion transfers the exact blob bytes and re-verifies post-commit hashes via
  `git show HEAD:<path>`; a mismatch (altered artifact) fails closed. Blob-level
  identity is the invariant; never compare disk-encoded bytes for verification.

<!-- 2026-09-23 16:30 UTC+7 -->