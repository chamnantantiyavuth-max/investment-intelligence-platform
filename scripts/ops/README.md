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
| `sync_main_to_ops.py` | S0/S1/S2/S3 main->ops lifecycle (remote-ops-first; durable baseline push; clean-merge / conflict-abort); captures `OPS_SYNC_BASE_SHA` |
| `validate_delta.py` | Cron-delta authority: validates only `OPS_SYNC_BASE_SHA -> job-produced state` |
| `commit_push_ops.py` | Explicit-path stage -> commit -> push ops -> fetch -> verify remote SHA |
| `generate_promotion_manifest.py` | Deterministic MULTI-JOB P1 manifest over the CANONICAL range (origin/main → origin/ops/automation, mechanical — R0.2 §7/§8); mechanical ownership, per-artifact source_commit, raw-blob SHA-256, immutable payload digest (R0.3 §3); `--approve`/`--cancel` digest-bound receipt — approve requires the exact pending id+digest, cancel is exact-disposition + recovery-refusal (R0.4 §3); corrupt-state HOLD (R0.3 §6); interactive only; write sets the pending pair (id+digest) LOCK-FIRST — manifest-write failure keeps the conservative lock (R0.4 §9) |
| `promote_batch.py` | TWO-PHASE P1 promotion (R0.3 §4; R0.4 crash-consistency): Phase V pure read-only validation of the ENTIRE batch (approval gate + owner re-derived at consumption + exact delta + hashes — zero primary mutation), Phase M write/stage/commit; exact-canonical-main contract (into_primary ⇒ main + push, clean local, local==origin==manifest), post-commit exactness before push (R0.3 §10), MANDATORY digest-bound pending identity (R0.4 §2), recovery identity recorded BEFORE the uncertain push (R0.4 §6), remote-success/ack-loss reconciliation CASE A/B/C (R0.4 §5), remote-verified-first, ONE atomic final state transition (R0.4 §7), P1_LOCAL_COMMIT_PENDING_REMOTE_RECOVERY + `--recover` with recorded pending identity (R0.3 §9); R0 = temp/canary branch only |

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
2. `python scripts/ops/sync_main_to_ops.py` — S0/S1/S2/S3 lifecycle; persists OPS_SYNC_BASE_SHA.
3. Job executes; writes ONLY its allowlisted artifact(s).
4. `python scripts/ops/validate_delta.py --job <id>` — must exit 0.
5. `python scripts/ops/commit_push_ops.py --job <id>` — explicit-path commit + push + verify.
6. Next run starts again at G0.

Sync lifecycle (R0.1, 24 Sep 2026): OPS_AHEAD is the NORMAL state after any
artifact commit. S0 (ops==main) no-op; S1 (main ahead) ff + push/verify;
S2 (ops ahead) NO merge/NO reset, base = ops HEAD; S3 (diverged) normal main->ops
merge in the ops worktree only (clean -> push/verify; conflict -> abort +
preserve + FAIL CLOSED). Remote-first: local ops is --ff-only'd to
origin/ops/automation before the main-vs-ops evaluation; a baseline changed by
S1/S3 is pushed and remote-verified BEFORE OPS_SYNC_BASE_SHA is stored.

Push failure → the script preserves the local commit and exits non-zero; the next
G0 sees case C and refuses a new job until the exact commit is pushed. NEVER reset.

## P1 promotion (interactive, Founder-approved batch)

1. Interactive review session:
   `generate_promotion_manifest.py [--job <id> ...]`
   → writes `ops/manifests/<id>.json` on ops (gitignored; interactive-only residue).
2. Founder approval is DIGEST-BOUND (R0.3 §2/§3): set `disposition = APPROVED` in
   the manifest, then `generate_promotion_manifest.py --approve --manifest <path>`
   records `approved_manifest_id + approved_manifest_sha256` into ops-state. A
   real P1 requires pending id == manifest id AND receipt id == manifest id AND
   receipt digest == recomputed immutable digest AND disposition == APPROVED.
   A different/edited manifest requires NEW approval; one pending manifest never
   clears/promotes another. `--cancel --manifest <path>` for exact disposition.
   **Canonical authority (R0.2):** the batch range is MECHANICAL —
   `MANIFEST_MAIN_SHA = origin/main`, `MANIFEST_OPS_HEAD_SHA =
   origin/ops/automation` (no `--from/--to`; HOLD unless main is ancestor of ops —
   sync first). Writing the manifest sets `promotion_pending_manifest_id` in
   external ops-state → G0 FAILS CLOSED (case PENDING) until verified REAL P1 or
   cancellation (R0.2 §14).
   One manifest may span MULTIPLE job classes (Radar + AM / Radar + CIW): each
   artifact's owning job is DERIVED mechanically from the anchored allowlists
   (0 matches / >1 matches = FAIL CLOSED; `--job` = optional expected-owner
   constraint only; Learning Loop's empty allowlist never owns a repo artifact).
   Per-artifact: `source_commit` = actual latest commit in `main..ops` touching
   the path; `sha256` = SHA-256 over the exact RAW `git show <c>:<path>` blob
   bytes (binary `run_git_bytes` — no text decode / no newline conversion / no
   errors=replace); `run_timestamp` = source committer time; PIT only when given.
2. Founder approves the manifest batch (one approval = whole batch).
3. Exact content promotion — real P1:
   `promote_batch.py --manifest <path> --target-branch main --push --into-primary`
   (R0 canary uses a temporary branch; canary NEVER advances state/removes the
   review manifest; `--verify-only` is canary-only, invalid with `--into-primary`).
   Exact order (R0.2 §4): contract (into_primary ⇒ main + push) → fetch → primary
   main clean → local == origin == manifest_main_sha → frozen-lineage check →
   canonical-delta revalidation (recomputed set == manifest set exactly) →
   per-artifact revalidation (commit, latest path-touch, exists, owner, raw hash)
   → transfer → explicit stage → commit → post-commit hash verify → record the
     exact recovery identity BEFORE the push (R0.4 §6) → push → fetch → remote
     verify (post-push fetch failure = UNKNOWN outcome, reconcile later) →
     **ONLY THEN** ONE atomic final state transition (R0.4 §7: last_promoted +
     exact pending/approval/recovery keys in a single authoritative write) →
     remove residue.
4. Push failure / acknowledgement loss → `P1_LOCAL_COMMIT_PENDING_REMOTE_RECOVERY`:
   local commit preserved, last_promoted unchanged, manifest preserved.
   `promote_batch.py --recover --manifest <path> --target-branch main` verifies
   the recorded identity (id+digest+commit, persisted BEFORE the push) +
   parent + hashes, then RECONCILES (R0.4 §5): remote == base → retry the EXACT
   push; remote == exact promotion commit → finalize state ONLY
   (`reconciled_remote_success`, no duplicate push); remote == other →
   `main_moved` FAIL CLOSED, Founder disposition only. No reset.
   `last_promoted_ops_sha`
   advances ONLY after a REAL remote-VERIFIED approved P1 into main — the
   code ENFORCES the Founder-approval gate (R0.3 §2/§3; R0.4 §2 pending pair
   MANDATORY), so "Founder-approved"
   is a mechanical fact, not an aspiration
   (mechanical; canary / generation / cron commits / push failure never advance
   it). On success the manifest residue is removed; G0 returns clean.

## State

Persistent scheduler state lives OUTSIDE the repo (never breaks G0 cleanliness):
`<HERMES_HOME>/ops-state/ops-state.json` (`OPS_STATE_DIR` overrides; tests use tmp).

## Tests

`pytest tests/ops/test_ops_tooling.py -q --basetemp <scratch>` — full-matrix on
temp git repos + a
per-test temp state dir; never touches the real worktree/remote/ops-state.
91 tests: G0 A–E + PENDING + STATE_CORRUPT (promotion-
pending pair), S0–S3 sync lifecycle (T1–T7), multi-job manifests M1–M8
(mechanical ownership, ambiguity FAIL, deletion/rename FAIL, raw CRLF/latin-1
blob, frozen head), canary-vs-real last-promoted, owner-scope, real-source-commit
blob, residue removal, P1-A..P1-G + recovery (exact-canonical-main baseline/
dirty/contract/target/verify-only refusals, push-failure
P1_LOCAL_COMMIT_PENDING_REMOTE_RECOVERY preservation, remote-verified-first
state advance, deterministic --recover), M9–M18 (mechanical canonical range,
  caller-range equality, frozen-lineage HOLD, out-of-batch/stale source_commit
  HOLD, delta omission/foreign-artifact HOLD, governance-between-batches delta,
  promotion-pending lock block + clear), R0.3 R3-A..R3-O + A1–A4 (approval-gate
  refusals incl. digest/receipt binding, late-artifact atomic zero-mutation,
  corrupt-state FAIL CLOSED, interrupted-write preservation, owner re-derivation,
  recovery exact-delta refusal + success, post-commit extra-path push refusal,
  duplicate-path + batch-base HOLDs), R0.4 R4-A..R4-J (mandatory pending
  identity, exact-disposition cancellation incl. recovery-refusal, short-write
  safety, remote-success/ack-loss reconciliation A/B/C, pre-push recovery
  identity, one atomic final transition, partial-tuple STATE_CORRUPT,
  lock-first manifest write).

## Maintenance mode (P2, design-only)

Promotion is refused when env `OPS_MAINTENANCE_MODE=ON` or the IIP profile config
key `ops.maintenance_mode` is set — lock lives outside governed main.

<!-- 2026-09-24 15:30 UTC+7 (R0.3 P1 governance/atomicity hardening closeout) -->