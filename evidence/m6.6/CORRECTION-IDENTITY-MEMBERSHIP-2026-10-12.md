# M6.6 ROUND-17 CORRECTION — RECONCILIATION-ENTRY CONTRACT CLOSED BY EXACT OBJECT IDENTITY

**Cluster:** QAD M6.6 (Noncanonical Source Discovery + Admission Bridge, FD #151)
**Authorization:** Founder ruling, 12 Oct 2026 — **Option A**: ONE minimal identity-closed correction
+ focused adversarial regression testing + ONE family-independent Round-17 confirmation review.
Not an architectural redesign; not an open-ended fix/review cycle.
**Correction commit:** `d67f2a6` (branch `impl/m6-gemini-notebook`) · parent `1b533f0`
**`main`:** `5bf107774b29e5a5fe4dcec5846800b9b48361ba` (unchanged) · **Date:** 2026-10-12
**Round 15 and Round 16 remain `C` and are NOT erased or relabelled. M6.6 remains NOT CLOSED.**

---

## 1. The defect being corrected (Round 16, material finding 1)

`type(error) not in _RECONCILABLE_ENTRY_FAILURES` is an **EQUality** test: Python tuple containment can
invoke a metaclass `__eq__`, so an unlisted subclass whose metaclass compares equal to
`IntegrityConflict` passed the predicate, entered the authoritative read-back, and settled a
lineage-claiming `IMPORTED` success. Parent reproduction:
`evidence/m6.6/PARENT-REVERIFY-ROUND16-2026-10-12.txt`. Reachability recorded then: **not reachable
through the accepted production boundary** (no custom metaclass and no exception `__eq__` anywhere
under `qad/`), but it violated the literal form of the Founder's exact-type ruling because the
prescribed predicate (`in`) was equality-based.

## 2. The exact correction — IDENTITY, not equality

```python
    if isinstance(error, SourceBridgeError):            # guard FIRST — precedence preserved
        raise error
    if not any(
        type(error) is allowed
        for allowed in _RECONCILABLE_ENTRY_FAILURES
    ):
        raise error                                     # propagate BEFORE any read-back
    state = reconcile_canonical_evidence_pair(...)       # comparison logic UNCHANGED
```

**Contract, stated exactly:** authoritative read-back is attempted **if and only if** the triggering
failure's class is the **actual object** `IntegrityConflict` **or** the **actual object**
`TransactionFailure` (identity, `is`), **and** it is not a `SourceBridgeError` (checked first, takes
precedence). No subclass, no dynamically created same-name class, and no equality-compatible class may
enter reconciliation. Every other failure propagates UNCHANGED before any read-back and no disposition
is written.

## 3. What was deliberately NOT changed

Reconciliation identity comparisons · canonical hashing · source binding · PIT · admission ·
dispositions · retry policy · `_RETRYABLE_OPERATIONAL_FAILURES` (still `(TransactionFailure,)`) ·
the closed classification structure · no schema change (68) · FD #149–#154 untouched · no
provider/Gemini/browser/network/cron/M6.7 work.

## 4. Files changed (commit `d67f2a6`)

| File | Change |
|---|---|
| `qad/m6/source_bridge.py` | **+29 / −18** — the only functional removed line is the previous predicate itself; all other removals are comment/docstring text. New: identity predicate + identity-contract documentation. |
| `tests/qad/m6/test_m66_source_bridge.py` | **+106 / −0** — 2 new tests; **zero** lines removed, so all 78 previously accepted tests are retained byte-identically |

## 5. Tests (Founder-mandated), 80 total

**`test_62_identity_predicate_rejects_an_equality_compatible_class`** — a test-only subclass whose
metaclass `__eq__` compares equal to `IntegrityConflict`, proving all ten mandated points:

| # | Required proof | Assertion in the test |
|---|---|---|
| 1 | `type(error) is IntegrityConflict` is FALSE | `assert (type(spoof) is IntegrityConflict) is False` |
| 2 | equality membership would be TRUE against the previous predicate | `assert (type(spoof) in sb._RECONCILABLE_ENTRY_FAILURES) is True` |
| 3 | the new identity predicate rejects it | `assert any(type(spoof) is a for a in ...) is False` (+ `isinstance` is True, showing isinstance is unsuitable) |
| 4 | the ORIGINAL exception propagates unchanged | `excinfo.value is spoof` |
| 5 | ZERO authoritative read-back calls | `spy.calls == 0` (a double that raises if touched) |
| 6 | ZERO candidate dispositions | `_dispositions(...) == {}` |
| 7 | candidate remains pending | `pending_candidates(...) == (cid,)` |
| 8 | canonical EV-01/EAR-01 hashes unchanged | `_canonical_hashes(registry) == before` |
| 9 | no evidence lineage newly claimed | outcome has no evidence/ear ids before recovery |
| 10 | the SAME candidate recovers legitimately later | final run reconciles via the actual approved type; ids linked; exactly one EV and one EAR |

**`test_63_a_dynamically_created_same_name_class_cannot_enter_reconciliation`** — a runtime-forged
class named `"IntegrityConflict"` is not the allowed class object; it propagates with zero read-back.

**Positive controls retained unchanged** (not re-implemented): exact `IntegrityConflict` reconciles
(`test_55`) · exact `TransactionFailure` reconciles (`test_56`) · ordinary subclasses rejected
(`test_57`/`test_58`) · `NotImplementedError` rejected (`test_59`) · `SourceBridgeError` precedence
(`test_54`/`test_60`) · allowlist composition exactly two classes (`test_61`) · unknown errors
fail-closed (`test_49`).

## 6. Required mutation proof A/B (executed) — `evidence/m6.6/RED-DEMO-ROUND17-2026-10-12.txt`

| Step | Expected | Actual |
|---|---|---|
| **A** — previous equality-based predicate restored | the new metaclass regression turns RED | **test_62 FAILED** (1 failed / 5 passed), exit 1 |
| **B** — identity predicate restored byte-identically (`sha256 320c70be…`) | GREEN | **6 passed**, exit 0 |

## 7. Regression — actual counts

| Suite | Interpreter | Result | Reference |
|---|---|---|---|
| `tests/qad/m6/test_m66_source_bridge.py` | Python 3.11.15 | **80 passed** | 78 + 2 new |
| `tests/qad/m6` | Python 3.11.15 | **404 passed** | 402 + 2 |
| `tests/qad/persistence` (M5.2) | Python 3.14.6 | **292 passed** | matches |
| `tests/qad/m53` (M5.3 PIT) | Python 3.14.6 | **116 passed** | matches |
| `tests/qad` | Python 3.14.6 | **939 passed / 1 failed** | 937 + 2 |
| `tests/ops` | Python 3.14.6 | **94 passed** | matches |
| `tests/locked` | Python 3.11.15 | **17 failed / 144 passed / 1 error** | matches (inherited) |
| `scripts/gate-check.sh` | — | **exit 0** (all gates) | — |
| `scripts/isolation-scan.sh` | — | **exit 0** | — |
| `.sqlite3` runtime residue | — | **0 files** | — |

**Inherited failures, reported separately:** `tests/qad` → 1 failure
`test_contract_conformance.py::test_schema_build_identity` (`spec_source_sha256` `7bf250a0…` expected
vs `3b513829…` actual — unchanged before/after, same as reported by the Round-13/14/15/16 reviewers).
`tests/locked` → 17 failed / 144 passed / 1 error, all inside `tests/locked/test_real_data_api.py`
(legacy AM/FO/II/CS surface; zero `qad` imports under `tests/locked`), identical at the prior commits.
**No new regression.**

## 8. Round-17 independent review — VERDICT = **B** (PASS WITH ONE BOUNDED NON-BLOCKING FINDING)

Focused confirmation reviewer: GPT-6 Luna high, family-independent from the DeepSeek producer
(routing provenance `family_independent: true`, guard exit 0); disposable no-`.git` copy of `d67f2a6`
+ explicit external basetemp; read-only — the reviewed files in the copy re-hash to the committed
blobs (`320c70be…` / `702e4729…` LF-normalised) after the run, i.e. the reviewer modified neither the
bridge nor its test file. Output verbatim: `evidence/m6.6/REVIEW-ROUND17-2026-10-12.txt`.

**PRINCIPAL QUESTION — answered YES** (verbatim): *"The current reconciliation-entry boundary enforces
exact class-object identity for only `IntegrityConflict` and `TransactionFailure`. The metaclass-equality
spoof is rejected before authoritative read-back; the existing exact-base reconciliation paths still
reuse matching EV-01/EAR-01 records and fail closed on unauthorized errors. I found no material
regression in the reviewed behavior."*

**Probe results:** 1 identity predicate (`type(error) is allowed`) VERIFIED · 2 end-to-end metaclass
spoof rejection VERIFIED (same exception object, zero registry reads, no disposition, pending, hashes
preserved) · 3 ordinary + nested + runtime-forged same-name class rejection VERIFIED · 4 exact-base
reconciliation still returns `RECONCILED_IDENTICAL`, reuses ids, one disposition, no duplicates ·
5 `SourceBridgeError` precedence VERIFIED (pure + multiple inheritance) · 6 no false lineage/disposition
VERIFIED · 7 no read-back **attempted** VERIFIED (raising double recorded zero calls) · 8 comparator
checks identity/source/both hashes, six independent mismatch probes → `CONFLICT_DIVERGENT` ·
9 counts reproduced (80 / 404) · 10 no SUCCESS writer or gate bypass, schema 68, no
provider/network/browser/Gemini/Notebook imports, PITC-01 authority intact.

**MATERIAL FINDINGS: NONE.**

**NON-BLOCKING FINDING 1** — the reviewer could not confirm the *historical* "comparator untouched"
claim because the disposable copy carries no prior snapshot and git use was prohibited; it noted this
limits only the ATTRIBUTION of changes, not the verification of current comparator behaviour (which it
confirmed with six mismatch probes). **Closed by the Parent in this round** by supplying the exact
authorised delta: `evidence/m6.6/CORRECTION-IDENTITY-MEMBERSHIP-DIFF-2026-10-12.txt` — 14 non-blank
changed lines, of which the ONLY functional statement is the predicate (1 removed → 4 added); the
comparator's own text hashes identically in the parent and the reviewed commit
(`sha256 91179368…`); zero changed lines mention the comparator.

## 9. M6.6 CLOSEOUT (facts-only, authorised on A/B)

All prior verdicts are recorded **truthfully and unchanged**:

| Round | Verdict | Finding | Status of that finding |
|---|---|---|---|
| 9 | accepted | trusted-verdict minting | closed, retained |
| 10 | accepted | proof-bound canonical admission / REPLAY_EXCEPTION | closed, retained |
| 11 | C | run/candidate/source verification | fixed |
| 12 | C | exact canonical payload comparison | fixed |
| 13 | C | incomplete EV-only / EAR-only collision protection | fixed |
| 14 | C | reconciliation ENTRY widened by the structural refactor | fixed in `18531e5` |
| 15 | C | `isinstance` admitted unlisted subclasses | fixed in `6565227` |
| 16 | C | `in` is an equality test (metaclass `__eq__` spoof) | **fixed in `d67f2a6`** |
| 17 | **B** | none material; 1 bounded non-blocking (attribution gap) | closed by the delta evidence above |

**Corrected contract (recorded as THE contract):** authoritative read-back is attempted **iff** the
triggering failure's class is the **actual object** `IntegrityConflict` **or** the **actual object**
`TransactionFailure` (identity via `is`), and it is not a `SourceBridgeError` (checked first,
precedence preserved). No subclass, dynamically created same-name class, or equality-compatible class
may enter. Every other failure propagates UNCHANGED before any read-back, with no disposition.

**M6.6 STATUS:**
`M6.6 SOURCE DISCOVERY + ADMISSION BRIDGE GREEN / CANONICAL RECONCILIATION FAIL-CLOSED /
ORIGINAL-SOURCE BOUNDARY VERIFIED / READY FOR PRE-M6.7 RAW SUCCESS API GATE RESOLUTION`
(closed on Round 17 = B — pass with ONE bounded non-blocking finding, no material blocker; the
finding's attribution gap is closed by the delta evidence in this document's round-17 section).

**NOT changed by the closeout:** `M6_RAW_SUCCESS_API_GATE` remains **OPEN** (blocking before M6.7
SUCCESS execution integration) · **M6.7 NOT STARTED** · 5/5 cron PAUSED · `main` unchanged
`5bf1077…` · inherited failures preserved unmodified (`test_schema_build_identity`; the 17/144/1
`tests/locked` set).

<!-- 2026-10-12 17:35 UTC+7 -->
