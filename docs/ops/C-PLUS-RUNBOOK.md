# C+ Cron Operations Runbook — POST-M5.3 O3 R0.3 (FD #142)

Status: **R0.3 P1 GOVERNANCE/ATOMICITY HARDENING COMPLETE** — bounded
implementation corrections (24
Sep 2026, Founder independent source review): R0.1/R0.2 retained PASS; R0.3 adds
Founder-approval gate bound to the exact immutable manifest digest, two-phase
validate-then-mutate (zero primary mutation on late failure), fail-closed atomic
ops-state, owner re-derivation at consumption, post-commit exactness before push,
and exact-delta recovery with a recorded pending identity.
R0.1 sync lifecycle PASS, R0.1-B
multi-job manifest/raw-blob PASS, R0.2 real-P1 promotion path hardened (exact
canonical-main start, into_primary⇒push+main, exact success order, per-artifact
+ delta revalidation, promotion-pending lock, P1_LOCAL_COMMIT_PENDING_REMOTE_
RECOVERY + deterministic --recover). No FD reopened: FD #142 architecture /
M5.3 / D-0 / C0 / P1 Founder-approval policy / Learning Loop authority / P2
prohibition all intact — R0.1/R0.2 are implementation conformance, NO new FD.
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

1. Interactive review: `python scripts/ops/generate_promotion_manifest.py [--job <id> ...]`
   → `ops/manifests/<id>.json`.
   - **Canonical authority model (R0.2 §7/§8):** the batch range is derived
     MECHANICALLY from the fetched origin refs — `MANIFEST_MAIN_SHA = origin/main`,
     `MANIFEST_OPS_HEAD_SHA = origin/ops/automation`; `batch_base_sha = main`.
     `main..ops` is the authoritative pending-promotion delta. No caller `--from/
     --to` (production never trusts arbitrary SHAs). HOLD unless main is an
     ancestor of (or equal to) ops — run the main→ops sync first.
   - `last_promoted_ops_sha` is provenance ONLY (R0.2 §9): must resolve to a
     commit and be in the current ops lineage, else HOLD; it never overrides the
     canonical current-main → current-ops delta.
   - Two or more job classes may share one batch (e.g. Radar + AM); every
     artifact's owning job is DERIVED mechanically from the anchored allowlists
     (0 matches = FAIL, >1 = FAIL ambiguous; `--job` is an optional expected-owner
     validation constraint only). Per-artifact `source_commit` = the actual latest
     commit in `main..ops` touching that path; `sha256` = SHA-256 over the exact
     RAW `git show <source_commit>:<path>` blob bytes (binary — no text decode,
     no newline conversion, no errors=replace); `run_timestamp` = source commit
     committer time (mechanical provenance); PIT only when provided. Denylist/
     allowlist re-checked per artifact (fail-closed).
   - **Promotion-pending lock (R0.2 §14):** writing the manifest sets
     `promotion_pending_manifest_id` in external ops-state (NOT a repo write).
     While set, artifact-cron preflight / G0 FAILS CLOSED (case PENDING) — the
     "jobs paused during Founder P1 review" pause is mechanical.
2. Founder approves the manifest (one approval = whole batch). **Approval is
   DIGEST-BOUND (R0.3 §2/§3):** the manifest carries `immutable_digest` — a
   SHA-256 over the deterministic canonical serialization of the immutable
   payload (manifest_id, batch_base_sha, manifest_main_sha, manifest_ops_head_sha,
   the exact ordered artifact entries path/job_id/source_commit/sha256, and
   changed_jobs). Mutable review metadata (disposition, generated_at, notes) is
   EXCLUDED. Set `disposition = APPROVED` in the manifest, then bind the receipt:
   `python scripts/ops/generate_promotion_manifest.py --approve --manifest <path>`
   → records `approved_manifest_id + approved_manifest_sha256` in ops-state. A
   real P1 requires ALL FOUR: `promotion_pending_manifest_id == manifest_id` AND
   `approved_manifest_id == manifest_id` AND
   `approved_manifest_sha256 == recomputed immutable_digest` AND
   `disposition == APPROVED`. Any mismatch = FAIL CLOSED `approval`/`pending`.
   A different/edited manifest requires NEW approval; one pending manifest never
   promotes/clears another. Cancellation:
   `... --cancel --manifest <path>` (exact id + digest only).
3. Real P1: `python scripts/ops/promote_batch.py --manifest <path> --target-branch main
   --push --into-primary` — TWO-PHASE (R0.3 §4), exact order (R0.2 §4/R0.3 §17):
   1. invocation contract (into_primary ⇒ target==main + do_push; into_primary +
      verify_only invalid) → 2. fetch → 3. primary main CLEAN → 4. local HEAD ==
      origin/main == manifest_main_sha (ahead/behind/diverged = HOLD "baseline",
      NO merge/rebase/reset) → 5. revalidate frozen ops snapshot (manifest ops
      head still in current origin/ops lineage, else "frozen_lineage" HOLD) →
      6. APPROVAL GATE (pending identity, then receipt id, then receipt digest,
      then disposition — R0.3 §2/§3/§13) → 7. manifest consistency
      (batch_base_sha == manifest_main_sha; duplicate artifact paths = FAIL
      CLOSED) → **PHASE V — PURE READ-ONLY VALIDATION OF THE ENTIRE BATCH (no
      file writes/staging/commits/state changes):** canonical-delta revalidation
      (recomputed `main..ops` artifact set must EQUAL the manifest set exactly)
      then per-artifact: denylist under CURRENT config, owner MECHANICALLY
      RE-DERIVED at consumption via owning_jobs (0 = "owner", >1 =
      "owner_ambiguous", unique ≠ manifest claim = "owner_mismatch"), source_commit
      is a commit, is the LATEST path-touch within the frozen batch, path exists
      there, raw sha256 matches — validated bytes held in memory ONLY → 8. IF
      EVERY artifact passed: PHASE M — write exact bytes, explicit-path stage,
      staged-set verify, commit → 9. POST-COMMIT EXACTNESS before push (parent ==
      manifest_main_sha; `diff --name-status main..HEAD` == manifest path set; all
      committed raw-blob hashes == manifest — protects against hooks/index
      mutation; failure = "post_commit", DO NOT PUSH) → 10. push → 11. fetch →
      12. verify origin/main == promotion commit → **ONLY THEN** 13-15. advance
      `last_promoted_ops_sha`, clear the exact pending + approval + recovery
      state, persist → 16. remove manifest residue → success.
      Any PHASE-V failure leaves primary main byte-for-byte clean.
   - R0 canary: `--target-branch <temp>` (optionally `--push`) — may rehearse an
     AWAITING manifest; NEVER advances last_promoted, NEVER touches promotion
     state, NEVER implies Founder approval, NEVER removes the review manifest.
     `--verify-only` rehearses a temp branch; it is invalid with into_primary.
4. **Push/remote-verify failure (R0.2 §13 + R0.3 §9):** state =
   `P1_LOCAL_COMMIT_PENDING_REMOTE_RECOVERY`. Local promotion commit PRESERVED,
   origin/main unchanged, last_promoted unchanged, manifest preserved, no new P1,
   no unrelated governed-main work. The failure RECORDS the exact recovery
   identity in ops-state (`pending_p1_manifest_id`, `pending_p1_manifest_sha256`,
   `pending_p1_local_commit_sha`). Recovery:
   `python scripts/ops/promote_batch.py --recover --manifest <path> --target-branch main`
   — requires the recorded identity to MATCH exactly (never inferred from HEAD),
   re-runs the approval gate (--recover never bypasses approval), verifies parent
   == manifest_main_sha and the EXACT commit delta (path set + A/M only + raw
   hashes), then retries the EXACT push; on success advances state + clears the
   exact locks + removes residue. No reset. If origin/main advanced past the
   reviewed base (`main_moved`), Founder disposition only.
5. Promotion record = normal governed main commit (files + receipt). Ops merge
   history never imported; no broad cherry-pick. Newer ops artifacts are never
   implicit.
6. `last_promoted_ops_sha` (external ops state) advances ONLY after a
   Founder-approved, remote-VERIFIED REAL P1 promotion into main succeeds — never
   on canary, manifest generation, cron artifact commits, or push failure. It
   defines the next batch range as provenance.
7. On REAL P1 success the interactive manifest is removed from the automation
   working tree (residue); `ops/manifests/` is gitignored and is NEVER a cron
   allowlist. G0 must return clean before scheduled cron resumes. The
   promotion-pending lock is cleared ONLY by verified success or explicit
   cancellation/disposition of that manifest.
8. **Ops-state is FAIL-CLOSED + ATOMIC (R0.3 §6/§7):** ops-state (external
   profile dir, never a repo write) carries the promotion-pending lock, approval
   receipt, last_promoted_ops_sha and recovery identity. `load_state()` returns
   {} ONLY when the file does not exist (explicit bootstrap); an EXISTING file
   that is malformed/truncated/unreadable/wrong-type/structurally-invalid raises
   StateError — G0 returns `STATE_CORRUPT`, manifest generation HOLDS, real P1
   HOLDS, recovery HOLDS. Corrupt state is NEVER treated as 'no lock'. Writes
   are atomic: deterministic same-directory temp file → flush → fsync →
   `os.replace` — the previous valid state survives until replacement succeeds;
   no partial/truncated authoritative state.

## 8. Maintenance mode (P2 design)

Promotion refused when `OPS_MAINTENANCE_MODE=ON` (env) or IIP profile config
`ops.maintenance_mode` = on. Lock lives OUTSIDE governed main (profile/runtime state)
so entering/exiting maintenance never requires a main commit. Artifact jobs continue
on ops; no promotion; no artifact loss; state remains auditable.

## 9. Verification

- Ops tooling: `python -m pytest tests/ops/test_ops_tooling.py -q --basetemp <scratch>`
  (76 tests; temp git repos + per-test temp state dir only — never the real
  worktree, remote OR ops-state). Matrix:
  G0 A–E + PENDING + STATE_CORRUPT (promotion-pending lock with fail-closed
  corrupt state), S0–S3 sync lifecycle (T1/T2
  sequential ops-ahead acceptance, T3 remote-first, T4 durable S1 push, T5 clean-
  divergence merge, T6 conflict abort, T7 push-failure preserve+block), M1/M2
  multi-job manifests, M3 unknown path FAIL, M4 ambiguous ownership FAIL, M5
  deletion FAIL, M6 rename FAIL, M7 raw CRLF/latin-1 blob hash, M8 frozen head,
  canary-vs-real last-promoted semantics, owner-scope, real-source-commit blob,
  residue removal, **R0.2 P1-A..P1-G + recovery** (baseline/dirty/contract/target/
  verify-only refusal, push-failure pending-state preservation, remote-first
  state advance, deterministic --recover), **M9–M18** (mechanical canonical
  range, caller-range equality, frozen-lineage HOLD, out-of-batch/stale
  source_commit HOLD, delta omission/foreign-artifact HOLD, governance-between-
  batches delta, promotion-pending lock block + clear),
  **R0.3 R3-A..R3-O + A1–A4** (AWAITING/REJECTED/approved-string-without-receipt/
  digest-mismatch refusals, foreign-pending refusal, late bad-hash/invalid-owner/
  invalid-source/denylisted atomic zero-mutation, corrupt-state G0+generate+
  promote HOLD, interrupted-write state preservation, owner-ambiguity
  re-derivation, recovery extra-path refusal + exact recovery, post-commit
  extra-path push refusal, duplicate-path FAIL, batch-base mismatch FAIL).
- Full suite: `python -m pytest` (must stay green; no M5.3 semantic changes).
  R0.3 gate: 848 passed (813 R0.1 + 18 R0.2 + 17 net new ops tests).
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