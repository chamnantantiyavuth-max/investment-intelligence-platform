# M6.6 ROUND-16 CORRECTION — RECONCILIATION-ENTRY CONTRACT CLOSED BY EXACT TYPE

**Cluster:** QAD M6.6 (Noncanonical Source Discovery + Admission Bridge, FD #151)
**Authorization:** Founder ruling, 12 Oct 2026 — **Option A combined with the bounded
closure-focused review treatment (Option D)**: ONE narrowly scoped correction + test strengthening +
ONE independent Round-16 review. No redesign, no structural refactor.
**Correction commit:** `6565227` (branch `impl/m6-gemini-notebook`) · parent `e084ea5`
**`main`:** `5bf107774b29e5a5fe4dcec5846800b9b48361ba` (unchanged) · **Date:** 2026-10-12
**Round 15 remains `C` and is NOT erased or relabelled. M6.6 is NOT closed.**

---

## 1. The defect being corrected (Round 15, material finding 1)

`classify_evidence_admission_failure` used `isinstance(error, _RECONCILABLE_ENTRY_FAILURES)` — an
**open** membership test — so an **unlisted SUBCLASS** of `IntegrityConflict` or `TransactionFailure`
entered authoritative read-back reconciliation and settled a lineage-claiming `IMPORTED` success.
Parent reproduced it for BOTH bases:
`evidence/m6.6/PARENT-REVERIFY-ROUND15-2026-10-12.txt`. Classification recorded then: residual of the
Round-14 defect class, **not** a regression (the original accepted
`except (IntegrityConflict, TransactionFailure)` clause also matched subclasses), and **latent** —
the accepted persistence layer defines no subclass of either class.

## 2. The exact code change (one predicate)

```python
    if isinstance(error, SourceBridgeError):                      # guard FIRST — precedence preserved
        raise error
    if type(error) not in _RECONCILABLE_ENTRY_FAILURES:            # was: not isinstance(...)
        raise error                                               # propagate BEFORE any read-back
    state = reconcile_canonical_evidence_pair(...)                 # comparison logic UNCHANGED
```

**Reconciliation-entry contract, stated exactly:** authoritative read-back is attempted **if and only
if** the triggering failure is **exactly** `IntegrityConflict` or **exactly** `TransactionFailure`
(exact-type membership), **and** it is not a `SourceBridgeError` (checked first, takes precedence).
Every other failure — an unlisted subclass, any other class, a governance failure — propagates
UNCHANGED **before** any read-back, and no candidate disposition is written.

## 3. What was deliberately NOT changed

- Reconciliation comparison logic (full canonical identity) — unchanged.
- `_RETRYABLE_OPERATIONAL_FAILURES` — unchanged, still `(TransactionFailure,)`; NOT broadened.
- The closed classification structure, the five outcome names, the three separated operations.
- Canonical hash semantics, source binding, PIT authority, verification/proof binding, disposition
  semantics.
- No M6.3 ledger change · no M6.4 proof-seam change · no M6.5 retry change · no canonical schema change
  (still 68) · FD #152/#153/#154 untouched · no provider/Gemini/browser/network work · no cron
  activation · no M6.7 work.

## 4. Files changed (commit `6565227`)

| File | Change |
|---|---|
| `qad/m6/source_bridge.py` | **+18 / −13** — one predicate line changed; every other changed line is a comment/docstring rewording (**no logic removed**) |
| `tests/qad/m6/test_m66_source_bridge.py` | **+199 / −0** — 7 new tests appended; **zero** lines removed, so all 71 previously accepted tests are retained byte-identically |

## 5. Tests — Founder-mandated cases A–J (78 tests total)

| Case | Test | What it proves |
|---|---|---|
| **A** | `test_55_A_...` | EXACT `IntegrityConflict` + exact pair → legitimate `RECONCILED_IDENTICAL`; direct classifier **and** a complete end-to-end lifecycle |
| **B** | `test_56_B_...` | EXACT `TransactionFailure` + exact pair → legitimate reconciliation, ids reused, no duplicates (full lifecycle) |
| **C** | `test_57_C_...` | UNLISTED subclass of `IntegrityConflict` → propagates unchanged (same object), **ZERO** read-back (spy), no disposition, pending, hashes unchanged; **then the SAME candidate recovers and reconciles** through the exact allowlist |
| **D** | `test_58_D_...` | UNLISTED subclass of `TransactionFailure` → same fail-closed outcome + full lifecycle |
| **E** | `test_59_E_...` | `NotImplementedError` (unlisted plain class) → same fail-closed outcome + full lifecycle |
| **F** | `test_60_F_...` | multiple inheritance `SourceBridgeError` + `IntegrityConflict` → governance guard retains precedence, zero read-back, fails closed + full lifecycle; plus a pure governance failure |
| **G** | `test_61_G_...` | allowlist composition is closed and exact: exactly the two approved classes, no third, no duplicates, subclasses excluded, transient allowlist not broadened |
| **H, I, J** | executed mutation demonstrations (§6) | the new tests detect both the reopened-door mutation and the added-third-class mutation; byte-identical restore → GREEN |

Each fail-closed case proves a **complete candidate lifecycle** (nothing settled → the same candidate
still recoverable → reconciliation completes), not just a predicate assertion.

## 6. Mutation demonstrations (executed) — `evidence/m6.6/RED-DEMO-ROUND16-2026-10-12.txt`

| Mutation | Expected | Actual |
|---|---|---|
| **H** — exact-type membership replaced with `isinstance` | subclass tests RED | **2 failed** (`test_57_C`, `test_58_D`), exit 1 |
| **I** — `NotImplementedError` inserted into the allowlist | composition + behavioural tests RED | **2 failed** (`test_59_E`, `test_61_G`), exit 1 |
| **J** — restore byte-identical | GREEN | **7 passed**, exit 0 |

`qad/m6/source_bridge.py` sha256 `cc8192ae…` before and after both mutations (verified).

## 7. Regression — actual counts

| Suite | Interpreter | Result |
|---|---|---|
| `tests/qad/m6/test_m66_source_bridge.py` | Python 3.11.15 (hermes venv) | **78 passed** (71 retained + 7 new) |
| `tests/qad/m6` | Python 3.11.15 | **402 passed** |
| `tests/qad/persistence` (M5.2) | Python 3.14.6 | **292 passed** |
| `tests/qad/m53` (M5.3 PIT) | Python 3.14.6 | **116 passed** |
| `tests/qad` | Python 3.14.6 | **937 passed / 1 failed** |
| `tests/ops` | Python 3.14.6 | **94 passed** |
| `tests/locked` | Python 3.11.15 | **17 failed / 144 passed / 1 error** |
| `.sqlite3` runtime residue | — | **0 files** |

**Inherited failures (separated from any new regression):** `tests/qad` → 1 failure
`test_contract_conformance.py::test_schema_build_identity` (`spec_source_sha256` `7bf250a0…` expected
vs `3b513829…` actual — unchanged before/after, same value reported by the Round-13/14/15 reviewers).
`tests/locked` → 17 failed / 144 passed / 1 error, all inside `tests/locked/test_real_data_api.py`
(legacy AM/FO/II/CS real-data API surface; zero `qad` imports under `tests/locked`), proven inherited
by identical counts at the pre-correction commits. **No new regression.**

## 8. Round-16 independent review — VERDICT = **C** (1 material finding)

Closure-focused reviewer: GPT-6 Luna high, family-independent from the DeepSeek producer (routing
provenance `family_independent: true`, guard exit 0); disposable no-`.git` copy + explicit external
basetemp; read-only — reviewed-file hashes re-verified unchanged after the run. Output verbatim:
`evidence/m6.6/REVIEW-ROUND16-2026-10-12.txt`.

**VERIFIED by the reviewer:** ordinary subclasses of both bases rejected (probe 2); `NotImplementedError`,
`CanonicalBoundaryViolation`, `MissingForeignKey`, `PITBlockError`, a subclass-of-subclass and a
dynamically-created same-name subclass all propagate the same object with **zero** read-back (probe 3);
`SourceBridgeError` precedence intact for pure and multiple-inheritance forms (probe 4); exact
`IntegrityConflict` and exact `TransactionFailure` each reconcile an exact pair end-to-end, reuse
`EV-A`/`EAR-A`, write one disposition, leave one EV and one EAR and no pending candidate (probe 5);
all identity/divergence comparisons correct — stored evidence id, admission id, EAR evidence id,
source binding, EV hash, EAR hash (probe 6); no SUCCESS-writing path or gate bypass (probe 11).
Counts reproduced exactly: `tests/qad/m6` 402 passed, `tests/qad` 937 passed / 1 failed.

**MATERIAL FINDING (open):** `type(error) not in _RECONCILABLE_ENTRY_FAILURES` is an **equality**
test, not an identity test — Python tuple containment can invoke a metaclass `__eq__`. An unlisted
`IntegrityConflict` subclass whose metaclass compares equal to the allowlisted class therefore passes
the predicate, **enters the authoritative read-back**, and settles a lineage-claiming `IMPORTED`
success. Reproduced independently by the Parent
(`evidence/m6.6/PARENT-REVERIFY-ROUND16-2026-10-12.txt`): `type(error) is IntegrityConflict` False
while `type(error) in allowlist` True, read-back attempted, `IMPORTED ('EV-A',) ('EAR-A',)` with one
disposition and pending cleared; controls (exact bases) still reconcile correctly.

**Reachability:** NOT reachable through the accepted production boundary — no custom metaclass and no
exception `__eq__` exists anywhere under `qad/`; reaching it requires in-process code that defines a
metaclass-spoofing exception class. **Settled policy:** it does violate the literal form of the
Founder's "CLOSED BY EXACT TYPE" ruling, because the prescribed predicate (`in`) is equality-based.

**Action taken: NONE.** Per the §7 stop rule (C → STOP, no Round 17, no freeze, no GREEN claim):
`evidence/m6.6/FOUNDER-DECISION-PACKAGE-ROUND16-C-2026-10-12.md`.
M6.6 remains **NOT CLOSED**; the finding remains **OPEN** and is **not** accepted risk.

<!-- 2026-10-12 15:55 UTC+7 -->

