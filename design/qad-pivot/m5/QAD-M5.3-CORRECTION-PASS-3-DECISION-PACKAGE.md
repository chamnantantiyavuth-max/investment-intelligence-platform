# QAD-M5.3 — CORRECTION PASS 3 DECISION PACKAGE (READ-ONLY, 9 Sep 2026)

> **Audit target:** `main @ 283a7aa` (chain `3341dce → 23101ba → fac8ab3 → 283a7aa`)
> **Verdict:** M5.3 = **INDEPENDENT RE-AUDIT FAIL / CORRECTION REQUIRED — NOT CLOSED / NOT FROZEN**
> **Governing authority:** FD #138 (NO FD #139)
> **Nature:** READ-ONLY analysis delivered after the 2nd Founder independent re-audit.
> No code/test/doc was modified by this package; F1 was confirmed by a direct
> read-only runtime probe against the reference persistence layer.
> **Awaiting Founder rulings on:** F3 (SI-01 lifecycle), F5 (UUIDv7 strictness),
> F6 (RRM retries semantics) — before any Correction Pass 3 GO.

---

## 1. CURRENT STATE

| Item | Value |
|---|---|
| HEAD / origin/main | `283a7aa` (clean) |
| M5.3 | INDEPENDENT RE-AUDIT FAIL / CORRECTION REQUIRED — NOT CLOSED / NOT FROZEN |
| Suites (claimed) | pass-2 diag 14/14 · M5.3 55/55 · ids 11/11 · QAD 470/470 · full 706/706 · M4A 173/173 · M4B 93/93 |
| M6 branch | `docs/m6-gemini-notebook-dr @ a37e92d` — PARKED, OUT OF SCOPE |
| M6 / M7 / Production / Live QAD | NOT AUTHORIZED |
| AGENTS.md checkpoint | untouched |

**Reviewer note (independent execution):** the 2nd re-audit was a **source-level
contract audit** against GitHub HEAD (sandbox could not resolve github.com for
an independent clone), so it did NOT claim an independent run of the 706-test
suite. Findings F1–F6 are code-path + frozen-authority verifiable directly.

## 2. FINDINGS F1–F6 — CONFIRMED

### F1 — APPEND_ONLY_STATE not actually enforced (CRITICAL) — Class A
- Frozen: M5.2 §5.4 (line 357) *"Validate state transitions for APPEND_ONLY_STATE
  fields — only forward enum transitions are accepted"*; §2.4 line 308.
- Defect: `qad/persistence/immutability.py` `check_immutability()` ends with
  *"APPEND_ONLY / APPEND_ONLY_STATE — noted for M5.3 enforcement (Currently
  treated as mutable at M5.1 scope.)"* — no transition table.
- **Runtime probe (read-only, 9 Sep):** direct `store()` of RSR-01, same stage_id:
  - `FAILED → COMPLETE` → **ACCEPTED** (SM-3-illegal; store returns COMPLETE)
  - `COMPLETE → FAILED` → **ACCEPTED** (also illegal)
  - `IN_PROGRESS → COMPLETE` → accepted (legal)
  - version preservation occurs (`v0001`) but that is NOT transition enforcement.
- Root cause: `_load_versioned_schemas()` preserves prior versions (store
  concern); nothing validates transition legality (validation concern). The
  "treated as mutable" comment is a deferred obligation never completed.
- Same gap affects all APPEND_ONLY_STATE schemas (CASE-01, CR-01, RU-01, QU-01,
  RSR-01, RB-01 — M5.2 §12 line 914).

### F2 — Cross-anchor terminal/provenance recovery not implemented (CRITICAL) — Class A (+B doc overclaim)
- Path: `retry_kernel.py` writes RSR terminal (COMPLETE/FAILED) to `stage_store`
  FIRST, then RR-01 + RRM-01 `store_batch` to RunManifestStore. Two anchors.
- If the batch fails after the RSR write: RSR terminal survives, RR/RRM
  provenance does not land, and the next `execute()` sees terminal RSR and
  replays immediately (no reconcile).
- Module docstring claims *"resume reconciles via RSR.retry_count and rewrites
  the missing RR"* — **no such code path exists** (verified: no reconcile /
  repair / rewrite logic in the file).
- Frozen basis: M5.2 §7.2 assigns cross-store coordination to the application
  layer; ordering exists, compensating recovery does not.

### F3 — SI-01 status lifecycle not honest (CRITICAL / lifecycle design) — Class C
- SI-01.status ∈ {SUCCESS, FAILURE, PARTIAL}; every field RECORD_IMMUTABLE;
  RR-01 FK requires SI-01 to pre-exist (kernel fail-closed).
- Test helper `_make_invocation()` seeds `status=FAILURE` BEFORE execution; the
  clean-first-run-success test stores that FAILURE SI-01 and completes; kernel
  never updates SI-01 (immutable).
- Conflict: "SI-01 must pre-exist" + "SI-01 immutable" + "outcome unknown until
  execution finishes" cannot all hold. FD #138's sequence
  (`initial success → SI-01=SUCCESS`) is not implementable as written.
- **Requires Founder ruling before code.**

### F4 — SM-3 FAILED side-effect RFR-01 missing (HIGH) — Class A
- Frozen SM-3: `FAILED → (escalation to Research Director) → side effects:
  ResearchFailureRecord created`. RFR-01 is a frozen M4A schema.
- No RFR-01 construction exists in `retry_kernel.py` or its dependency path;
  no test references it.
- Root cause: SM-3 side-effect obligation dropped during pass-1/2 without a
  deferral note.

### F5 — deterministic_uuid7 not RFC-9562 time-conformant (HIGH) — Class A (semantic ruling needed)
- RFC 9562 §5.7: first 48 bits MUST be unix epoch ms timestamp.
- `qad/ids.py::deterministic_uuid7` derives the 48-bit field from
  SHA-256(seed) — arbitrary hash bits, NOT a unix-ms timestamp.
- `is_uuid7()` checks only version==7 + variant==RFC4122 → cannot detect.
- Docstring claim *"DETERMINISTIC RFC-9562 UUID v7"* is false as written.
- Constraint to preserve: FD #138's mechanically stable retried-write identity
  (same seed → same id, no duplicate writes, no hard-coded IDs).
- **Requires a semantic ruling** (acceptable "stable ID with UUIDv7 shape" vs
  strict time semantics), not a silent deletion.

### F6 — RRM retry-success lineage ambiguous (MEDIUM) — Class C
- `_write_attempt_and_manifest()`: RETRYING → append rr_id to `manifest.retries`
  (comma-join string); FAILED → append to `manifest.failures`; **SUCCEEDED →
  manifest unchanged**. So a successful retry's RR-01 SUCCEEDED record is not
  referenced by RRM-01.
- Frozen text inconsistency: M4A RRM-01 lists `retries` (no type) + `failures[]`
  optional; operating model shows `retries: N` (integer count). Ambiguous
  whether `retries` = count, reference list, or both.
- RR-01 ledger itself retains the authoritative per-retry lineage
  (invocation_id + attempt_number + status).
- **Requires Founder ruling** on the authoritative semantics; do not decide
  silently.

## 3. CLASSIFICATION SUMMARY

| Finding | Class | Needs Founder ruling? | Erratum? |
|---|---|---|---|
| F1 | A — IMPLEMENTATION BUG (M5.2 §5.4 conformance) | No (mandated) | No |
| F2 | A (implementation) + B (doc overclaim) | No (M5.2 §7.2 assigns to app layer) | No |
| F3 | C — CONTRACT AMBIGUITY / lifecycle design | **YES** | Possibly doc clarification; likely no schema change |
| F4 | A — IMPLEMENTATION BUG (SM-3 side-effect) | No (mandated) | No |
| F5 | A (implementation) + semantic ruling | **YES** (strictness ruling) | No schema change |
| F6 | C — EXISTING FROZEN CONTRACT AMBIGUITY | **YES** | Possibly doc clarification; no schema change |

No FD number invented. No erratum created. No frozen M3/M4A/M4B text modified.

## 4. MINIMUM CORRECTION OPTIONS (NOT YET AUTHORIZED)

| Finding | Option | Authority |
|---|---|---|
| F1 | (a) RSR-01-only SM-3 transition enforcement in `check_immutability()` (recommended now); (b) generic engine for all 6 APPEND_ONLY_STATE schemas (separate bounded item) | No new FD — M5.2 §5.4 conformance |
| F2 | Application-layer reconcile on `execute()` resume: if RSR terminal && RR ledger incomplete for terminal attempt → write missing RR + RRM batch (idempotent, attempt-number keyed) | No new FD — M5.2 §7.2 |
| F3 | (a) SI-01 = invocation REQUEST record (status=PARTIAL=accepted; outcome lives in RSR/RR); (b) SI-01.status = outcome of the whole retry lifecycle (recorded terminal — conflicts with pre-existing); (c) two-record split (request + outcome) | **Founder ruling** |
| F4 | Create RFR-01 on terminal FAILED (deterministic failure_id via existing surface; idempotent — no duplicates on restart) | No new FD — SM-3 mandates |
| F5 | (a) Relabel: stable deterministic ID with UUIDv7 *shape* (restrict the "RFC-9562" claim); (b) redesign: hash-derived rand bits + deterministic floor of real first-seen time in the 48-bit field (still needs ruling on strictness) | **Founder ruling** |
| F6 | (a) `retries` = count (operating-model reading); RR ledger = lineage source; (b) `retries` also records SUCCEEDED rr_ids; (c) doc clarification | **Founder ruling** |

## 5. RED TESTS REQUIRED (before any correction)

1. **F1:** direct canonical-store test — RSR FAILED→COMPLETE same stage_id must
   be REJECTED deterministically (already proven RED by probe); IN_PROGRESS→
   COMPLETE stays legal. Do NOT substitute a kernel-path test.
2. **F2:** fault-injection — (a) retry succeeds, RSR COMPLETE persists, RR/RRM
   batch fails, restart → provenance reconciled; (b) terminal-fail, RSR FAILED
   persists, batch fails, restart → reconciled; assert completeness + no dup RR.
3. **F3:** lifecycle test per the Founder-chosen semantics.
4. **F4:** RFR-01 created exactly once on terminal FAILED; not on intermediate
   retry; no duplicates after restart.
5. **F5:** timestamp-semantics test (top 48 bits per chosen ruling);
   strengthen `is_uuid7` as needed; keep seed-string contract unchanged so
   pass-2 idempotency tests remain valid.
6. **F6:** lineage test per the chosen `retries` semantics.

## 6. REGRESSION BLAST RADIUS

- F1(a) RSR-only: moderate — all 55 m53 tests that write same-stage_id RSR
  transitions (stable stage_id, output accumulation, resume) must still pass
  legal transitions. F1(b) generic: high — five-anchor 16, Item-13 7,
  authority-isolation 10 touch other APPEND_ONLY_STATE schemas; separate item.
- F2: resume/replay tests (`test_checkpoint_replay_returns_without_reexecution`,
  staged-resume tests) may change terminal-replay behavior.
- F4: new RFR-01 writes hit stage_store; FK assumptions across the 55 tests.
- F5: `deterministic_uuid7` feeds pass-2 EG-01 idempotency tests; keeping the
  seed-string contract identical limits churn to the derivation internals.
- F3/F6: pending ruling; no immediate runtime impact.

## 7. EXACT FILES THAT WOULD CHANGE (IF AUTHORIZED)

| Finding | Files |
|---|---|
| F1 | `qad/persistence/immutability.py` (+ transition hook in `reference.py` if needed), `tests/qad/persistence/` |
| F2 | `qad/m53/retry_kernel.py`, `tests/qad/m53/` |
| F3 | per ruling — `qad/m53/retry_kernel.py` + test helpers; NO schema change unless ruling demands |
| F4 | `qad/m53/retry_kernel.py` (+ RFR-01 import), `tests/qad/m53/test_correction_pass3.py` |
| F5 | `qad/ids.py`, `tests/qad/test_ids.py` |
| F6 | per ruling — `qad/m53/retry_kernel.py` semantics only |

## 8. STOP-CONDITION ASSESSMENT

- This package is READ-ONLY. Nothing was modified during analysis. The session
  end-of-session docs commit (this package file + state docs) is a docs-only
  commit — it does not alter the audited functional baseline `283a7aa`.
- **M5.3 = INDEPENDENT RE-AUDIT FAIL / CORRECTION REQUIRED — NOT CLOSED / NOT
  FROZEN.** Correction Pass 3 is NOT authorized until Founder rules on F3/F5/F6
  and issues GO. No FD #139. Erratum-002 remains FROZEN. M6/M7 remain NOT
  AUTHORIZED.

<!-- 2026-09-09 16:30 UTC+7 -->