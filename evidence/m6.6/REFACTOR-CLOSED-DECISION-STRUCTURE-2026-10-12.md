# M6.6 STRUCTURAL REFACTOR — CLOSED FAILURE CLASSIFICATION AT THE
# EVIDENCE-ADMISSION / RECONCILIATION / DISPOSITION BOUNDARY

**Cluster:** QAD M6.6 (Noncanonical Source Discovery + Admission Bridge, FD #151) — Founder
direction **OPTION A+** (see `DECISION-OPTION-A-PLUS-2026-10-12.md`)
**Branch:** `impl/m6-gemini-notebook` · **Refactor commit:** `38dcd9f`
**Parent:** `1a5002e` · **`main`:** `5bf1077` (unchanged) · **Date:** 2026-10-12

---

## 1. Structural root cause (what was actually wrong)

The repeated Rounds 11/12/13 defects all lived in ONE nested block inside
`process_discovered_sources` (`qad/m6/source_bridge.py`), which had this shape:

```
try:
    built = evidence_builder(...)                 # construction
    if built is not None:
        ev, ear = built
        try:
            admit_candidate_evidence(...)         # canonical admission
        except (IntegrityConflict, TransactionFailure):
            ev_exists  = registry.contains(...)   # READ-BACK inside the handler
            ear_exists = registry.contains(...)
            if not (ev_exists or ear_exists):
                raise                             # re-raise -> caught one level up
            if not (ev_exists and ear_exists):
                raise SourceEvidenceConflict(...)
            stored_ev  = registry.load(...)
            stored_ear = registry.load(...)
            if <any mismatch>:
                raise SourceEvidenceConflict(...)
        evidence_ids = (...); ear_ids = (...)
except SourceBridgeError:
    raise
except Exception as exc:                          # <-- THE DEFECT
    evidence_error = f"{type(exc).__name__}: {exc}"   # -> ordinary partial outcome
```

Three distinct structural defects, one class:

1. **`except Exception` was the classifier.** Any unknown integrity/governance failure
   (a boundary violation, a missing FK, an immutability/hash violation, a PIT block, malformed
   state, an unexpected runtime error) was downgraded into an ordinary partial
   evidence-admission outcome and the candidate was **disposed**.
2. **"Neither record exists" was treated as automatically transient** — the bare `raise`
   re-raised *any* error (including an unexplained collision) back into the same broad handler,
   which then recorded the partial outcome. Absence of canonical records proves nothing.
3. **The authoritative read-back ran INSIDE the catastrophic handler.** A failure while reading
   the stored state (`contains` / `load`) propagated out of the `except` clause into the broad
   handler and was swallowed: the bridge could not tell "the pair is absent" from "I could not
   read the pair", and settled the candidate anyway.

Each round-11/12/13 finding was a different escape route into this one handler. Round 13's own
reviewer conclusion: the incomplete pair *"is downgraded to an IMPORTED partial outcome and the
candidate is disposed"*.

## 2. The closed decision structure (structure, not another escape route)

`EvidenceAdmissionClassification` — exhaustive for the recognized operational cases, with **no
implicit/default mapping**:

| Classification | Condition (decided by AUTHORITATIVE read-back) | Effect |
|---|---|---|
| `ADMITTED_NEW` | this attempt wrote the canonical pair | candidate settled (evidence ids recorded) |
| `RECONCILED_IDENTICAL` | pair already committed by an earlier attempt AND matches EXACTLY | candidate settled, **existing ids reused**, canonical state untouched |
| `TRANSIENT_PARTIAL` | **no** canonical trace **and** the error is a recognized retryable operational failure | candidate settled: SOURCE IMPORTED / CANONICAL EVIDENCE NOT ADMITTED |
| `CONFLICT_INCOMPLETE` | exactly one of EV-01 / EAR-01 exists | raised `SourceEvidenceIncomplete`; candidate **undisposed** |
| `CONFLICT_DIVERGENT` | both exist but identity / source binding / payload differs | raised `SourceEvidenceConflict`; candidate **undisposed** |

**FAIL-CLOSED (not a classification — the ORIGINAL error propagates with its provenance, and NO
disposition is written):**

| Case | Behaviour |
|---|---|
| pre-boundary proof / binding / verification / governance failure (`SourceBridgeError`) | re-raised immediately, without read-back |
| neither record exists **and** the error is NOT a recognized retryable operational failure | re-raised (absence alone is never "transient") |
| a failure while reading the authoritative stored state (`contains` / `load`) | propagates untouched — never guessed |
| `BaseException` | never caught |

**The transient allowlist is explicit and narrow:**
`_RETRYABLE_OPERATIONAL_FAILURES = (TransactionFailure,)` — a `TransactionFailure` is raised only
when a batch transaction failed before commit and *guarantees zero committed records*, so an
honest retry is the truthful reading of "the pair was not written". Canonical conflicts,
boundary violations, missing foreign keys, hash/immutability violations, PIT blocks,
proof/binding failures, identity collisions and malformed state are all excluded.

**Explicit distinction preserved** between a successfully admitted ORIGINAL SOURCE
(`SourceAdmissionOutcome.admitted` / `.reused` / `.src01_id`) and successfully admitted EV-01 /
EAR-01 canonical EVIDENCE (`evidence_ids` / `ear_ids`).

## 3. Three separated operations (were one nested catch-all)

| Op | Function | Responsibility |
|---|---|---|
| A | `attempt_canonical_evidence_admission(...)` | attempt the pair through the **existing** `EvidenceRegistry.admit_evidence` gate only; on failure it **routes** (never classifies) to the classifier |
| B | `reconcile_canonical_evidence_pair(...)` | authoritative read-back + EXACT-record comparison; returns `CanonicalPairState` |
| C | `dispose_settled_candidate(...)` | write the ONE durable disposition — **only** for a settled classification; an unsettled one propagates as a typed conflict |
| — | `construct_candidate_evidence(...)` | documented **PRE-BOUNDARY**, mutation-free stage (builds the in-memory DTOs) |
| — | `classify_evidence_admission_failure(...)` | the exhaustive classifier over A/B |

**No cross-store atomicity was invented.** A committed SRC-01 / EV-01 / EAR-01 is never deleted,
never rewritten, and never used to simulate a rollback. An unsettled candidate simply stays
pending (the accepted M6.0 §7.5 "no source vanishes without a disposition" rule is satisfied by
the candidate remaining explicitly pending, which the existing completeness check surfaces).

**Reconciliation requires FULL canonical record identity** — not merely matching ids:
stored `EV.evidence_id`, stored `EAR.admission_id`, stored `EAR.evidence_id == EV.evidence_id`,
stored `EV.source_id == the verified source`, **and** both `compute_canonical_hash` values equal.

**The pre-boundary construction stage** (the caller-supplied `evidence_builder`) is the ONE
place where a non-`SourceBridgeError` failure yields `TRANSIENT_PARTIAL`. Its allowlist is
*stage-scoped*, not exception-type-scoped, and it is justified structurally: the stage performs
**zero canonical mutation**, so a failure there cannot conceal, or downgrade, a canonical
integrity/governance failure. A `SourceBridgeError` raised by the builder still propagates.
(This preserves the accepted Rounds 12–13 semantics that "a builder/transient error still yields
the truthful partial outcome".) The stage is proven mutation-free by test 43.

## 4. Exception policy (as mandated)

- `except Exception` is **never** a classifier anywhere in the refactored region.
- The two remaining broad handlers are (a) **routing-only** — `attempt_canonical_evidence_admission`
  returns a classified decision or re-raises — and (b) the **mutation-free-stage** handler above.
- `BaseException` is never caught.
- Error provenance is preserved: fail-closed cases re-raise the **same exception object**
  (`excinfo.value is case["error"]`, asserted in the table test), and diagnostics keep
  `"{TypeName}: {message}"`.
- Enforced mechanically by `test_42c_...`: an AST scan proves that no broad handler inside
  `process_discovered_sources`, `construct_candidate_evidence`,
  `attempt_canonical_evidence_admission`, `classify_evidence_admission_failure`,
  `reconcile_canonical_evidence_pair` or `dispose_settled_candidate` contains any statement
  other than `return` / `raise` (i.e. nothing there can record or downgrade a failure class).

## 5. Accepted invariants — preserved, not regressed

Round-9 trusted-verdict minting · Round-10 proof-bound canonical admission + REPLAY_EXCEPTION
authorization · Round-11 mandatory run/candidate/source verification binding + cross-store
lineage · Round-12 exact canonical payload comparison · Round-13 incomplete-pair collision
protection · `RawSourceArchive.admit_source` semantics · `EvidenceRegistry.admit_evidence`
semantics · M5.3 PIT · M6.3 ledger immutability · FD #152 proof boundary · FD #153 atomic
SUCCESS finalization · FD #154 raw-SUCCESS hard gate.
**No canonical schema addition or modification (68 schemas, no #69); no RRM-01 change.**

## 6. Exact code / tests changed

| File | Change |
|---|---|
| `qad/m6/source_bridge.py` | +435 / −66 (`git diff --numstat HEAD~1 HEAD`) — new `SourceEvidenceIncomplete`, `EvidenceAdmissionClassification`, `EvidenceAdmissionDecision`, `CanonicalPairState`, `_SETTLED_EVIDENCE_CLASSIFICATIONS`, `_RETRYABLE_OPERATIONAL_FAILURES`; new operations A/B/C + `construct_candidate_evidence` + the classifier; `process_discovered_sources`' evidence block rewritten to use them (the nested `try` is **gone**); docstring + `__all__` updated |
| `tests/qad/m6/test_m66_source_bridge.py` | +645 / **−0** — 23 new tests appended; the diff removes **no** line, so all 41 existing M6.6 tests are retained byte-identically (verified: only the `--- a/…` header line matches `^-`) |

## 7. RED→GREEN proof (executed, not asserted)

One deliberate mutation of the mandated FAIL-CLOSED behaviour — the neither-record /
non-retryable branch of `classify_evidence_admission_failure` replaced `raise error` with a
fabricated `TRANSIENT_PARTIAL` return:

| Run | Targeted tests | Result |
|---|---|---|
| RED (mutated, sha256 `a302b087…`) | `row02_neither_exists_unexpected`, `row10_unknown_integrity_exception`, `row12_pit_validation_exception`, `test_45_no_candidate_settlement_on_an_unresolved_governance_error` | **4 failed** (all `DID NOT RAISE`), exit 1 |
| GREEN (restored, sha256 `704a23c4…` — byte-identical to the committed blob) | same 4 | **4 passed**, exit 0 |

Raw output: `evidence/m6.6/RED-DEMO-2026-10-12.txt`. The mutation is caught, so the tests prove
the classifier's FAIL-CLOSED property rather than the public happy path.

## 8. Mandated classification table — row coverage

| # | Row | Where proven |
|---|---|---|
| 1 | neither exists + explicitly retryable operational error | `row01` → `TRANSIENT_PARTIAL` |
| 2 | neither exists + unexpected exception | `row02` → propagates (same object) |
| 3 | EV exists, EAR absent | `row03` → `CONFLICT_INCOMPLETE` |
| 4 | EAR exists, EV absent | `row04` → `CONFLICT_INCOMPLETE` |
| 5 | both exist, identical payload/hash | `row05` → `RECONCILED_IDENTICAL` |
| 6 | both exist, EV payload mismatch | `row06` → `CONFLICT_DIVERGENT` |
| 7 | both exist, EAR payload mismatch | `row07` → `CONFLICT_DIVERGENT` |
| 8 | both exist, source mismatch | `row08` → `CONFLICT_DIVERGENT` |
| 9 | canonical record load / read-back fails | `row09_load`, `row09_contains` → propagates |
| 10 | unknown integrity exception | `row10` → propagates (same object) |
| 11 | proof-verification exception | `row11` → `SourceBridgeError` propagates |
| 12 | PIT-validation exception | `row12` → `PITBlockError` propagates |
| 13 | evidence-builder exception | `test_43` (pre-boundary `TRANSIENT_PARTIAL`, zero canonical mutation) + `test_43b` (builder `SourceBridgeError` fails closed) |
| 14 | disposition write fails after canonical admission | `test_44` (+ existing `test_38`) |
| 15 | re-entry after identical evidence commit | `row13` (+ existing `test_38`, `test_46`) |
| 16 | re-entry after conflicting evidence commit | `row14` (+ existing `test_39/40/41`, `test_46`) |
| 17 | no candidate settlement on unresolved governance error | `test_45` + `test_47` (operation C refuses) |
| 18 | no duplicate canonical records during replay | `test_46` |

Deterministic fault injection only: monkeypatched `contains`/`load`/`admit_evidence`, injected
typed persistence errors, a load-bomb and a contains-bomb registry double, and a one-shot ledger
disposition failure. All probes write into an external basetemp.

## 9. Verification — actual counts

| Suite | Interpreter | Result |
|---|---|---|
| `tests/qad/m6/test_m66_source_bridge.py` | Python 3.11.15 (hermes venv) | **64 passed** (41 retained + 23 new) |
| `tests/qad/m6` | Python 3.11.15 | **388 passed** |
| `tests/qad/m53` (M5.3 PIT) | Python 3.14.6 | **116 passed** |
| `tests/qad/persistence` (M5.2) | Python 3.14.6 | **292 passed** |
| `tests/qad` | Python 3.14.6 | **923 passed / 1 failed** |
| `tests/ops` | Python 3.14.6 | **94 passed** |
| `tests/locked` | Python 3.11.15 | **17 failed / 144 passed / 1 error** |
| `scripts/gate-check.sh` | — | **exit 0** (all gates pass) |
| `scripts/isolation-scan.sh` | — | **exit 0** (no forbidden-path violations) |
| `.sqlite3` runtime residue in the repo | — | **0 files** |

### Inherited failures — reported accurately, NOT caused by this refactor

- **`tests/qad` → 1 failure:** `test_contract_conformance.py::test_schema_build_identity`
  (`spec_source_sha256` `7bf250a0…` vs current artifact `3b513829…`). **Identical hashes to those
  the Round-13 reviewer reported at `28c1ac4`** — present before this commit, unchanged by it.
- **`tests/locked` → 17 failed / 144 passed / 1 error:** every failure is inside
  `tests/locked/test_real_data_api.py` (the legacy AM/FO/II/CS real-data API surface). Proven
  **inherited** by running the same suite against the **parent commit `1a5002e`** in a throwaway
  worktree: **identical 17 failed / 144 passed / 1 error**. Zero files under `tests/locked`
  import `qad` at all, so a change confined to `qad/m6/source_bridge.py` cannot affect them.
  (`tests/locked` also needs `fastapi`; the canonical rounds-9–13 interpreter has it.)
- `scripts/gate-check.sh` **Gate 6** reads the *last commit message*; it reports a failure on the
  pre-refactor HEAD `1a5002e` (a docs-only `[NO CODE CHANGE]` commit) and passes at `38dcd9f`.

## 10. Claim-to-Code check

Every claim above was re-read against the staged diff before commit (`git diff` inspected after
all edits). No `pass`/placeholder/`TODO` blocks were introduced; no dead code; no unused new
symbols (`__all__` updated); no pre-existing test was modified or weakened; no assertion removed.
The only behaviour deliberately changed is the one the Founder mandated.

## Addendum — Round-14 outcome (added 2026-10-12 AFTER this record was written)

Round 14 (the ONE family-independent confirmation review of commit `38dcd9f`, GPT-6 Luna high,
disposable no-`.git` copy, external basetemp) returned **C — 1 material finding**, 0 non-blocking,
0 evidence gaps. The finding is real and was reproduced by the Parent independently: an
**unrecognized** exception raised by the canonical gate while an EXACT canonical pair already exists
is reconciled into a settled `IMPORTED` outcome that claims the EV-01/EAR-01 lineage, instead of
failing closed. The same probe against the pre-refactor bridge shows the pre-refactor code settled
that case with `evidence_ids=()` (no lineage claim), so the refactor **widened the reconciliation
entry condition** — a regression introduced by the refactor, inside the boundary A+ was
commissioned to close. Per the Founder's A+ STOP rule, **nothing was fixed**, the finding was
**not** frozen as accepted risk, and a decision package was returned:
`evidence/m6.6/FOUNDER-DECISION-PACKAGE-ROUND14-C-2026-10-12.md`.
M6.6 remains **NOT CLOSED**.

The two numbers below were re-measured by the reviewer in its no-`.git` copy and differ slightly
from the Parent's run for an environmental reason, reported honestly: `tests/locked` gave
**18 failed / 143 passed / 1 error** there versus **17 failed / 144 passed / 1 error** in the
Parent's worktree, because one locked test asserts on git history and cannot pass without `.git`
metadata. `tests/qad/m6` (388), `tests/qad/m6/test_m66_source_bridge.py` (64), `tests/qad`
(923 passed / 1 failed — same `test_schema_build_identity` spec-hash mismatch, expected
`7bf250…` vs actual `3b5138…`) and `tests/ops` (94) matched exactly.

<!-- 2026-10-12 13:30 UTC+7 -->


## 11. Scope exclusions honoured

No Gemini Notebook · no browser automation or repair · no provider transport · no network
execution · no Deep Research SUCCESS writer · no new runtime orchestration · no cron restart ·
no merge to main.
`M6_RAW_SUCCESS_API_GATE` remains **OPEN** and BLOCKING before M6.7 SUCCESS execution integration.
M6.7 = **NOT STARTED**.

<!-- 2026-10-12 13:10 UTC+7 -->
