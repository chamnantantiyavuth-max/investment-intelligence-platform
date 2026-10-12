# M6.6 ROUND-15 CORRECTION — EXPLICIT RECONCILIATION-ENTRY ALLOWLIST

**Cluster:** QAD M6.6 (Noncanonical Source Discovery + Admission Bridge, FD #151)
**Authorization:** Founder **OPTION A** (bounded correction) from
`evidence/m6.6/FOUNDER-DECISION-PACKAGE-ROUND14-C-2026-10-12.md` — ONE minimal correction of the
Round-14 reconciliation-entry defect + focused regression tests + ONE independent Round-15
confirmation review. **No further architectural refactor.**
**Correction commit:** `18531e5` (branch `impl/m6-gemini-notebook`) · parent `166b986`
**`main`:** `5bf107774b29e5a5fe4dcec5846800b9b48361ba` (unchanged) · **Date:** 2026-10-12

---

## 1. The defect being corrected (Round 14, material finding 1)

`classify_evidence_admission_failure` entered `reconcile_canonical_evidence_pair` for **any**
failure that was not a `SourceBridgeError`, and then decided purely on authoritative read-back.
Consequently an **unrecognized** exception raised by the canonical gate while an **exact** canonical
EV-01/EAR-01 pair already existed was reconciled into a settled `IMPORTED` outcome that claimed the
evidence lineage, instead of failing closed.

The pre-refactor code entered reconciliation only from the accepted
`except (IntegrityConflict, TransactionFailure)` allowlist, so the round-14 refactor had **widened
the entry condition** — a regression introduced by that refactor (proven by the pre/post comparison
in `evidence/m6.6/PARENT-REVERIFY-ROUND14-2026-10-12.txt`).

## 2. The precise correction — the reconciliation-entry condition

New module constant (qad/m6/source_bridge.py):

```python
_RECONCILABLE_ENTRY_FAILURES: tuple[type[BaseException], ...] = (
    IntegrityConflict,
    TransactionFailure,
)
```

And in `classify_evidence_admission_failure`, in this exact order:

```python
    if isinstance(error, SourceBridgeError):
        # proof / binding / verification / governance failure: pre-boundary, fail closed.
        # This guard is checked FIRST and takes PRECEDENCE over the entry allowlist below: a
        # governance failure never enters reconciliation even if it also carries a
        # collision-shaped type.
        raise error
    if not isinstance(error, _RECONCILABLE_ENTRY_FAILURES):
        # RECONCILIATION-ENTRY ALLOWLIST (round-14 correction). A failure whose class has NO
        # established reconciliation semantics must not reach the read-back at all: nothing is
        # read, nothing is guessed, and the ORIGINAL exception propagates unchanged. This is
        # what stops an unrecognized failure from being turned into a settled success merely
        # because an identical canonical pair happens to exist.
        raise error
    state = reconcile_canonical_evidence_pair(...)
```

**Reconciliation-entry condition, stated exactly:** authoritative read-back is attempted **if and
only if** the triggering failure is an instance of `IntegrityConflict` **or** `TransactionFailure`,
**and** it is not a `SourceBridgeError` (checked first, takes precedence). Every other exception
class propagates unchanged **before** any read-back.

The rest of the classifier is unchanged: neither-record + recognized-retryable (`TransactionFailure`)
→ `TRANSIENT_PARTIAL`; neither-record + otherwise → propagate; exactly one record → `CONFLICT_INCOMPLETE`;
both identical → `RECONCILED_IDENTICAL`; both differing → `CONFLICT_DIVERGENT`; read-back failure →
propagate.

## 3. What was deliberately NOT changed

- `_RETRYABLE_OPERATIONAL_FAILURES` is still exactly `(TransactionFailure,)` — the transient-partial
  allowlist was **not** broadened (asserted by `test_42b` and `test_54`).
- The closed classification structure, the five outcome names, and the three separated operations
  (A attempt / B read-back reconciliation / C settled-only disposition) are unchanged.
- Canonical hash semantics, source binding, PIT authority, verification/proof binding, and
  disposition semantics are unchanged.
- No new canonical schema (still 68 — no #69). RRM-01 unchanged. FD #152/#153/#154 untouched.
- No Gemini Notebook / provider execution / browser / network / cron activation.

## 4. Files changed (commit `18531e5`)

| File | Change |
|---|---|
| `qad/m6/source_bridge.py` | **+31 / −3** — the new entry-allowlist constant, the entry guard, and 3 docstring lines reworded (documentation only; **no logic removed**) |
| `tests/qad/m6/test_m66_source_bridge.py` | **+347 / −0** — 7 new tests appended; **zero** lines removed, so all 64 previously accepted tests are retained byte-identically |

## 5. Focused tests (Founder-mandated cases A–G), 71 tests total

| Case | Test | What it proves |
|---|---|---|
| **A** | `test_48_A_...` | Unknown `RuntimeError` + **exact** pair → original exception propagates (identity-preserved), candidate **pending**, **no disposition**, **no new lineage**, canonical hashes unchanged; a read-back **spy** proves NO authoritative read-back is attempted. Direct + end-to-end. |
| **B** | `test_49_B_...` | Unknown `RuntimeError` + **no** pair → propagates, no disposition, no canonical write. Direct (spy) + end-to-end. |
| **C** | `test_50_C_...` | Recognized `IntegrityConflict` + exact pair → `RECONCILED_IDENTICAL`, existing ids linked correctly, **no duplicate** canonical records. Direct + end-to-end with the registry's own natural collision (no fault injection). |
| **D** | `test_51_D_...` | Recognized `TransactionFailure` + exact pair → read-back reconciliation with exact identity checks; ids linked; no duplicates. Direct + end-to-end. |
| **E** | `test_52_E_...` | Unknown exception + **incomplete** (EV-only) pair → propagate, never reconcile/settle; + **divergent** pair → propagate; + end-to-end candidate stays undisposed. |
| **F** | `test_53_F_...` | Read-back failure (`load`/`contains` raising) under an otherwise recognized exception → fails closed, no disposition, no fabricated lineage. Direct + end-to-end. |
| **G** | executed mutation demonstration (below) | Removing the entry allowlist turns the new tests RED; restoring the file byte-identically turns them GREEN. |
| probe-11 gap | `test_54_...` | A governance failure that is **also** collision-shaped (`SourceBridgeError` + `IntegrityConflict`) must propagate with **no** read-back. Removing the `SourceBridgeError` guard now turns this test **RED** — the Round-14 test-strength gap is closed. |

## 6. Mutation demonstration (executed) — `evidence/m6.6/RED-DEMO-ROUND15-2026-10-12.txt`

| Mutation | Expected | Actual |
|---|---|---|
| **1** — remove the reconciliation-entry allowlist | new focused tests RED | **3 failed** (`test_48_A`, `test_49_B`, `test_52_E`), exit 1 |
| **2** — remove the `SourceBridgeError` fast-fail guard | `test_54` RED | **1 failed** (`test_54`), exit 1 (the plain-`SourceBridgeError` row still passes, as expected) |
| restore byte-identical | GREEN | **7 passed**, exit 0 |

`qad/m6/source_bridge.py` sha256 `c85ce508…` before and after both mutations (verified).
The mutation is caught, so the new tests prove the entry-allowlist property itself.

## 7. Regression — actual counts

| Suite | Interpreter | Result |
|---|---|---|
| `tests/qad/m6/test_m66_source_bridge.py` | Python 3.11.15 (hermes venv) | **71 passed** (64 retained + 7 new) |
| `tests/qad/m6` | Python 3.11.15 | **395 passed** |
| `tests/qad/persistence` (M5.2) | Python 3.14.6 | **292 passed** |
| `tests/qad/m53` (M5.3 PIT) | Python 3.14.6 | **116 passed** |
| `tests/qad` | Python 3.14.6 | **930 passed / 1 failed** |
| `tests/ops` | Python 3.14.6 | **94 passed** |
| `tests/locked` | Python 3.11.15 | **17 failed / 144 passed / 1 error** |
| `.sqlite3` runtime residue | — | **0 files** |

**Inherited failures — attributed, not caused by this correction:**
- `tests/qad` → 1 failure `test_contract_conformance.py::test_schema_build_identity`
  (`spec_source_sha256` `7bf250a0…` expected vs `3b513829…` actual) — unchanged before/after, and
  identical to the value the Round-13/Round-14 reviewers reported.
- `tests/locked` → 17 failed / 144 passed / 1 error, all inside `tests/locked/test_real_data_api.py`
  (legacy AM/FO/II/CS real-data API surface; zero `qad` imports anywhere under `tests/locked`) —
  proven inherited by identical counts at the pre-correction commits.

Environment note (reported honestly): an earlier matrix run reported 172 collection errors because
`$TMPDIR` resolved to `/tmp` in that shell and pytest could not create the basetemp under the native
interpreter. Re-running with an explicit existing `--basetemp` gave the counts above. This is a
runner-path artifact, not a product defect.

## 8. Round-15 independent review — VERDICT = **C** (1 material finding)

Reviewer: GPT-6 Luna high, family-independent from the DeepSeek producer (routing provenance
`family_independent: true`, guard exit 0); disposable no-`.git` copy + explicit external basetemp;
read-only — the reviewer modified no reviewed file (LF-normalized hashes re-verified after the run).
Output preserved verbatim: `evidence/m6.6/REVIEW-ROUND15-2026-10-12.txt`.

**VERIFIED by the reviewer:** probe 2 (an unrecognized `RuntimeError` + exact pair propagates, no
read-back, no disposition, pending, unchanged hashes) · probe 3 (exact `IntegrityConflict` /
`TransactionFailure` still reconcile end-to-end with reused ids and no duplicates) · probe 4
(incomplete/divergent pairs stay undisposed, stored records not rewritten) · probe 5 (read-back
failures propagate) · probe 6 (ordinary-caller verification/binding refusals) · probe 7 (PIT /
REPLAY_EXCEPTION) · probe 8 (disposition + repeated re-entry integrity) · probe 9 (no canonical
bypass) · probe 11 (no SUCCESS-writing path / gate bypass) · probe 10 partially: the producer's
claim that removing the `SourceBridgeError` guard is now detected was **confirmed** (`test_54` RED).

**MATERIAL FINDING (open):** `source_bridge.py:1231` uses `isinstance(error,
_RECONCILABLE_ENTRY_FAILURES)`, which is an OPEN membership test — an **unlisted subclass** of
`IntegrityConflict` or `TransactionFailure` is admitted to reconciliation and settles a
lineage-claiming `IMPORTED` success. Reproduced independently by the Parent for **both** bases
(`evidence/m6.6/PARENT-REVERIFY-ROUND15-2026-10-12.txt`), with the exact base classes still
reconciling correctly (control). Latent rather than immediately reachable: the accepted persistence
layer defines no subclass of either class. **Classification: residual of the Round-14 defect class,
NOT a regression** — the original accepted `except (IntegrityConflict, TransactionFailure)` clause
also matched subclasses.

**Also reported (test-strength):** a copied-code mutation that additionally admitted
`NotImplementedError` to the entry predicate passed all 71 tests.

**Action taken: NONE.** Per the Founder's Option-A stop rule (C → STOP, reproduce, return a decision
package, do NOT run Round 16, do NOT freeze, do NOT claim GREEN):
`evidence/m6.6/FOUNDER-DECISION-PACKAGE-ROUND15-C-2026-10-12.md`.
M6.6 remains **NOT CLOSED**; the finding remains **OPEN** and is **not** accepted risk.

<!-- 2026-10-12 14:35 UTC+7 -->

