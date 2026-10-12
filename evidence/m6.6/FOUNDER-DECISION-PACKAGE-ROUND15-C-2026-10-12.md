# FOUNDER DECISION PACKAGE — M6.6 ROUND-15 VERDICT = C (OPTION A STOP RULE ENGAGED)

**Cluster:** QAD M6.6 — Noncanonical Source Discovery + Admission Bridge (FD #151)
**Branch:** `impl/m6-gemini-notebook` · **Correction commit reviewed:** `18531e5`
`main` unchanged (`5bf107774b29e5a5fe4dcec5846800b9b48361ba`) · 5/5 cron PAUSED · M6.7 NOT started
**Date:** 2026-10-12

---

## 0. What happened

Founder **Option A** authorized ONE minimal correction (the reconciliation-entry allowlist) +
focused tests + ONE family-independent Round-15 review, with the same stop rule: closeout only on
**A or B**; on **C → STOP, reproduce, return a minimal decision package; do NOT run Round 16
automatically, do NOT freeze, do NOT claim M6.6 GREEN**.

**Round 15 returned `C` — 1 material finding, 0 non-blocking findings.**

Per that stop rule, this package is returned and **nothing further was done**:

- ❌ M6.6 is **NOT closed** and **NOT** claimed GREEN.
- ❌ The finding is **NOT** frozen or accepted as risk.
- ❌ Round 16 was **NOT** run.
- ❌ Nothing was carried into M6.7 (still NOT STARTED).
- ✅ The Round-14 finding **IS fixed and independently verified** in this commit (Round-15 probe 2
  VERIFIED: an unrecognized `RuntimeError` with an exact pair now propagates with no read-back, no
  disposition, pending candidate, unchanged hashes).
- ✅ Round-15 probe 10 CONFIRMED the probe-11 test-strength gap is closed: removing the
  `SourceBridgeError` guard now turns `test_54` RED.
- ℹ️ `M6_RAW_SUCCESS_API_GATE` remains **OPEN** and blocking.

This is the **seventh consecutive C** on this cluster (r9–r15).

## 1. The finding (verbatim from the reviewer)

> **1. Unlisted subclasses enter reconciliation.**
> (a) `source_bridge.py:1231` uses `isinstance(error, _RECONCILABLE_ENTRY_FAILURES)`. I raised
> `UnrecognizedIntegritySubclass(IntegrityConflict)` during re-entry with an exact existing pair; it
> is not an exact tuple member, but current production code reconciled it, returned IMPORTED with
> `('EV-A',)` / `('EAR-A',)`, and wrote one disposition.
> (b) An exception whose reconciliation semantics were never approved can be converted into a
> settled, lineage-claiming success—the same failure mode this round was meant to close.
> (c) Keep the preceding `SourceBridgeError` guard, then use exact-type membership
> (`type(error) in _RECONCILABLE_ENTRY_FAILURES`) or another explicitly closed class policy.
> (d) Add direct and end-to-end tests for a non-SourceBridgeError subclass of each allowlisted base.
> Require original exception propagation, zero read-back, no disposition/linkage, pending candidate,
> and unchanged hashes; retain tests proving the exact base classes reconcile.

Also reported (probe 10, test-strength, not a separate material finding): *"a copied-code mutation
that additionally admitted `NotImplementedError` passed all 71 M6.6 tests and reconciled an
identical pair."*

## 2. Parent re-verification — the finding is VALID and was REPRODUCED

`evidence/m6.6/PARENT-REVERIFY-ROUND15-2026-10-12.txt` (raw):

```
_RECONCILABLE_ENTRY_FAILURES = (IntegrityConflict, TransactionFailure)
  IntegrityConflict                  isinstance=True  exact_type=True
  TransactionFailure                 isinstance=True  exact_type=True
  *subclass of IntegrityConflict*    isinstance=True  exact_type=False
  *subclass of TransactionFailure*   isinstance=True  exact_type=False

=== END-TO-END: exact canonical pair + subclass of IntegrityConflict ===
  RETURNED: disposition=IMPORTED evidence_ids=('EV-A',) ear_ids=('EAR-A',) pending=()
  dispositions written = 1
=== END-TO-END: exact canonical pair + subclass of TransactionFailure ===
  RETURNED: disposition=IMPORTED evidence_ids=('EV-A',) ear_ids=('EAR-A',) pending=()
  dispositions written = 1
=== CONTROL: the exact BASE classes must still reconcile ===
  IntegrityConflict    -> IMPORTED ('EV-A',) ('EAR-A',)
  TransactionFailure   -> IMPORTED ('EV-A',) ('EAR-A',)
```

Both unlisted subclasses are admitted to reconciliation and settle a lineage-claiming success, while
the exact base classes continue to reconcile correctly (that behaviour must be preserved).

**Reachability, stated honestly:** the ACCEPTED persistence layer defines **no subclass** of
`IntegrityConflict` / `TransactionFailure` — every raise site in `qad/persistence/reference.py` raises
the exact classes. The defect is therefore reached today only by a subclass produced by something
other than the accepted stores (a future/alternative registry, a wrapper store, an injected test
double). It is a **latent closure gap in the entry predicate**, not an immediately reachable
production path.

## 3. Classification: residual of the Round-14 class — **not** a regression

- The Round-15 correction closed the Round-14 escape route (unrecognized class → reconciled success).
  The reviewer VERIFIED that (probe 2) and VERIFIED the base-class reconciliation still works.
- The remaining gap is the **predicate's membership semantics**: `isinstance` is an *open* test
  (subclasses pass); the Founder's mandated policy is a *closed* one —
  *"Only recognized exception classes … For any other exception class, propagate the ORIGINAL
  exception unchanged."* Under that wording, an unlisted subclass is "another exception class".
- **This is NOT a regression introduced by the Round-15 correction, and not by the Round-14
  refactor**: the original accepted entry condition was an `except (IntegrityConflict,
  TransactionFailure):` clause, and Python `except` clauses match subclasses too. A subclass would
  equally have been admitted before the refactor. It is a **pre-existing latent property of the
  original allowlist semantics**, surfaced now because the policy requires an exactly closed class
  set.

**Affected boundary (precise):** the entry predicate in `classify_evidence_admission_failure`
(`qad/m6/source_bridge.py:1231`) — the *membership test*, not the classification logic, not the
reconciliation comparison, and not the `SourceBridgeError` precedence guard (which is correct).

## 4. Minimal correction (analysed, NOT applied — stop rule)

Change the predicate from open membership to exact-type membership:

```python
    if type(error) not in _RECONCILABLE_ENTRY_FAILURES:      # was: if not isinstance(error, ...)
```

Expected to preserve every accepted behaviour: exact `IntegrityConflict` / `TransactionFailure`
still reconcile (rows 05/13, tests 38, 50, 51); the `SourceBridgeError` guard still wins first
(test_54, including the collision-shaped governance case); incomplete/divergent/read-back-failure/
unrecognized paths unchanged (rows 03/04/06–12, tests 39–41, 48, 49, 52, 53).

Required new tests (per the reviewer's (d)): a non-`SourceBridgeError` **subclass of each**
allowlisted base must propagate with **zero read-back**, no disposition, no linkage, pending
candidate, unchanged hashes (direct + end-to-end); plus a **non-allowlisted class** (e.g.
`NotImplementedError`) to close the predicate-mutation detection gap; and the existing base-class
reconciliation tests are retained unchanged.

**Every statement in this section is UNEXECUTED analysis. Nothing was implemented, so nothing here
is verified.** The finding remains open.

## 5. Options (one decision)

### Option A — apply the exact-type-membership closure, then ONE Round-16 confirmation review *(recommended)*
A **single-predicate** change (`isinstance` → `type(...) in`), the required subclass/non-allowlisted
tests, a mutation demonstration, the full regression matrix, then ONE family-independent Round-16
review of that commit.
- 🔎 Why: it is the smallest possible change, it is the exact discipline the Founder already
  mandated ("only recognized exception classes"), it needs no design work, and it simultaneously
  closes the described test-strength gap. Exact-type membership also removes the *shape* of escape
  route that rounds 14 and 15 both used (an unexpected class reaching reconciliation that was not
  enumerated).
- ⚠️ Cost/risk: one more fix + one more review (an eighth round on this cluster). I do **not** claim
  it works; it is unexecuted.

### Option B — FREEZE M6.6 at `18531e5` as **review-unconfirmed**, carrying the open finding forward
Close M6.6 with its final head explicitly labelled **no independent A/B verdict**, the Round-15
finding recorded **OPEN (not accepted as risk)**, and a **blocking** item added to the pre-M6.7
gate-resolution package.
- 🔎 Honest and stops spending now; the residual is latent (no subclass exists in the accepted
  persistence layer today), so the practical exposure is low.
- ⚠️ It contradicts the brief's own closeout gate (independent A/B) — I would label it
  review-unconfirmed, **not** a pass — and it leaves a known closure gap on the admission boundary
  M6.7 would build on.

### Option C — revert the round-15 correction
Not recommended: it re-opens the Round-14 finding (an unrecognized error reconciled into a
lineage-claiming success), which is strictly worse than the current head.

### Option D — change the review treatment instead of the code
Stop the per-round cycle and ask for **ONE bounded closure sweep**: a single family-independent
review whose scope is *only* to prove that the entry predicate is closed (every exception class
either reconciles by exact type or propagates), including adversarial subclass/dynamic-class
probes — rather than re-reviewing the whole module each round.
- Reasonable if the Founder's concern is now "seven C's means the review scope, not the code, is the
  cost driver". It could be combined with A (fix first, then one closure-scoped review).

## 6. Exact approval requested

Select **A**, **B**, **C**, or **D**. My recommendation is **A** — a one-predicate closure plus the
subclass/non-allowlisted tests, because it is the smallest possible correction, it is the discipline
already mandated, and it closes both the finding and the reported test-strength gap. If the Founder's
priority is now to stop spending on this cluster, **B** is defensible provided the open finding is
recorded as **review-unconfirmed + blocking carry-forward**, never as accepted risk, and never as a
pass.

## 7. Current status (unchanged by this package)

| Item | Status |
|---|---|
| M6.6 | `IMPLEMENTED / NOT CLOSED / ROUND-15 = C ON THE CORRECTION COMMIT` |
| Round-14 finding | **FIXED AND INDEPENDENTLY VERIFIED** in `18531e5` |
| Round-15 finding | **OPEN — not frozen, not accepted as risk** |
| M6.6 labelled GREEN or a pass? | **NO** |
| Round 16 | **NOT RUN** |
| `M6_RAW_SUCCESS_API_GATE` | **OPEN / BLOCKING** before M6.7 SUCCESS execution |
| M6.7 | **NOT STARTED** |
| cron | **5/5 PAUSED** |
| `main` | `5bf107774b29e5a5fe4dcec5846800b9b48361ba` — unchanged |

## 8. Evidence

- `evidence/m6.6/REVIEW-ROUND15-2026-10-12.txt` — reviewer output, **verbatim**
- `evidence/m6.6/REVIEW-ROUND15-2026-10-12-PROMPT.txt` — the exact prompt used (includes the
  explicit instruction not to steer the reviewer toward a PASS)
- `evidence/m6.6/REVIEW-ROUND15-2026-10-12-ROUTING.txt` — family-independence provenance
  (`family_independent: true`, guard exit 0)
- `evidence/m6.6/PARENT-REVERIFY-ROUND15-2026-10-12.txt` — Parent reproduction, raw
- `evidence/m6.6/CORRECTION-RECONCILIATION-ENTRY-ALLOWLIST-2026-10-12.md` — the round-15 correction
  record (entry condition, tests A–G, mutation demonstration, regression totals) + round-15 addendum
- `evidence/m6.6/RED-DEMO-ROUND15-2026-10-12.txt` — executed mutation demonstration
- Commit lineage: `38dcd9f` (round-14 refactor, r14 = C) → `166b986` (docs) → **`18531e5`**
  (round-15 correction, r15 = C, the reviewed commit)

<!-- 2026-10-12 14:35 UTC+7 -->
