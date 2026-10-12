# FOUNDER DECISION PACKAGE — M6.6 ROUND-16 VERDICT = C (OPTION-A STOP RULE ENGAGED)

**Cluster:** QAD M6.6 (Noncanonical Source Discovery + Admission Bridge, FD #151)
**Branch:** `impl/m6-gemini-notebook` · **Correction commit reviewed:** `6565227`
`main` unchanged (`5bf107774b29e5a5fe4dcec5846800b9b48361ba`) · 5/5 cron PAUSED · M6.7 NOT started
**Round-15 remains `C`; it is not erased or relabelled.** **Date:** 2026-10-12

## 0. What happened

Your ruling (Option A + bounded closure-focused review) was executed exactly as scoped: one
predicate change, the mandated tests A–J, the mandated mutation demonstrations H/I/J, the full
regression matrix, and ONE closure-focused independent Round-16 review.

**Round 16 returned `C` — 1 material finding, 0 non-blocking, repro confirmed by the Parent.**

Per your §7 stop rule, I did **not**: launch Round 17, freeze the finding as accepted risk, claim
M6.6 GREEN, or move anything into M6.7. M6.6 remains **NOT CLOSED**.

What Round 16 **did** verify (probes 3–6, 9, 11): ordinary subclasses of both bases rejected;
`NotImplementedError`, `CanonicalBoundaryViolation`, `MissingForeignKey`, `PITBlockError`, a
subclass-of-subclass and a dynamically-created same-name subclass all rejected with **zero** read-back;
`SourceBridgeError` precedence intact (pure and multiple-inheritance forms); exact bases still
reconcile end-to-end with ids reused, one disposition and no duplicates; all identity/divergence
comparisons correct; no SUCCESS path or gate bypass.

## 1. The finding (verbatim, condensed) + Parent reproduction

> `type(error) not in _RECONCILABLE_ENTRY_FAILURES` uses **equality-based tuple membership, not
> identity**. An unlisted `IntegrityConflict` subclass whose metaclass defines `__eq__` had
> `type(error) is IntegrityConflict == False` but membership `True`, and was reconciled.
> Smallest correction: `any(type(error) is allowed for allowed in _RECONCILABLE_ENTRY_FAILURES)`.

Parent reproduction against `6565227`
(`evidence/m6.6/PARENT-REVERIFY-ROUND16-2026-10-12.txt`):

```
type(error) is IntegrityConflict          = False
type(error) in allowlist (equality `in`)  = True       <-- the gap
(a) direct classifier: READ-BACK ATTEMPTED             <-- read-back IS entered
(b) end-to-end: RETURNED disposition=IMPORTED evidence_ids=('EV-A',) ear_ids=('EAR-A',)
    dispositions written = 1   pending cleared         <-- settled WITH lineage
control: exact IntegrityConflict  -> IMPORTED ('EV-A',) ('EAR-A',)   (correct, must be preserved)
control: exact TransactionFailure -> IMPORTED ('EV-A',) ('EAR-A',)   (correct, must be preserved)
control: ordinary (non-spoofing) subclass -> excluded by both tests  (correct)
```

## 2. Is it reachable through the accepted production boundary? — **NO**

- No class anywhere under `qad/` defines a custom metaclass (zero `metaclass=` usages) and no
  exception class defines `__eq__`. Every raise site in `qad/persistence/reference.py` raises the
  EXACT classes.
- Reaching this defect requires in-process code that **defines a metaclass-spoofing exception class**
  — an adversarial same-process construct. There is no ordinary-caller path to it: an ordinary caller
  cannot make `IntegrityConflict` be raised with a spoofing metaclass.

## 3. Does it violate a settled policy? — **YES, in its literal form**

The Founder ruling of 12 Oct 2026 says the allowlist is "CLOSED BY EXACT TYPE" and prescribes the
predicate `type(error) not in _RECONCILABLE_ENTRY_FAILURES`. `in` is an **equality** test (it can
invoke a metaclass `__eq__`), so the prescribed predicate is not **identity**-closed. The current
code implements the Founder's literal instruction; the reviewer shows that the literal form is not
sufficient to make the contract airtight. **This is a policy-precision question, not an implementation
deviation from your instruction.**

Related honest note: the reviewer also reported that a mutation replacing the predicate with pairwise
`!=` checks escaped all 78 tests. That is expected — it is a behaviourally *equivalent* mutant under
the current equality semantics. An identity-closed predicate plus a metaclass regression would close
both.

## 4. Minimum correction (analysed, NOT applied — stop rule)

```python
    if not any(type(error) is allowed for allowed in _RECONCILABLE_ENTRY_FAILURES):
        raise error          # identity-closed; equality spoofing cannot satisfy it
```
One line + one metaclass-equality regression test (which must FAIL against the current predicate and
PASS after) + the existing exact-base reconciliation tests retained unchanged. The comparison logic,
the guards and the transient allowlist are untouched. **Unexecuted analysis — nothing implemented.**

## 5. Options (one decision)

### Option A — apply the identity-closed one-liner, then ONE Round-17 review *(recommended)*
Cheapest possible closure of a settled policy: change `in` to an identity test. Cost: one line, two
tests, one review.
- 🔎 Rationale: it makes your "CLOSED BY EXACT TYPE" ruling literally true; no design work; no other
  semantics move; and it also closes the reported equivalent-mutant gap.

### Option B — FREEZE M6.6 at `6565227` as **review-unconfirmed**, with a bounded carry-forward
Record the deepening contract as review-unconfirmed (**no A/B**), the Round-16 finding as **open and
NOT accepted as risk**, and the identity-closure as a **documented, blocking-before-M6.7 item**.
- 🔎 Rationale: the residual requires an adversarial in-process metaclass spoof, which has no path
  through the accepted code, and FD #152 already places hostile same-process constructs outside the
  accepted trust boundary for the adjacent concern (verification authority). This is the point at
  which "is the threat in scope?" is a Founder policy question rather than an engineering one.
- ⚠️ It contradicts the brief's own closeout gate ("independent A/B") — I would label it
  review-unconfirmed, **never** a pass.

### Option C — revert the round-16 correction
Not recommended: re-opens the Round-15 finding (ordinary subclasses entering reconciliation), which
is strictly worse.

### Option D — rule the threat model explicitly instead of changing code
Rule that adversarial in-process metaclass/class-identity spoofing is **outside the accepted M6.6
trust boundary** (mirroring FD #152's exclusion), record that ruling, and then close on B with the
identity-closure noted as a non-blocking future hardening. If you take this path, the closure becomes
a documented policy boundary rather than an open defect.

## 6. Exact approval requested

Select **A**, **B**, **C**, or **D**. My recommendation is **A**: the correction is one line, it makes
your exact-type ruling literally true, and it costs one review. If you judge the adversarial
in-process spoof to be outside the accepted trust model, **D-then-B** is legitimate — but it must be
recorded as an explicit policy ruling and the finding must not be called a pass.

## 7. Status (unchanged by this package)

| Item | Status |
|---|---|
| M6.6 | `IMPLEMENTED / NOT CLOSED / ROUND-16 = C ON 6565227` |
| Round-15 finding | **FIXED** in `6565227` and independently VERIFIED (probe 2 = ordinary subclasses rejected; probe 3) |
| Round-16 finding | **OPEN** — not frozen, not accepted as risk |
| Round 17 | **NOT RUN** |
| M6.6 GREEN? | **NO** |
| `M6_RAW_SUCCESS_API_GATE` | **OPEN** |
| M6.7 | **NOT STARTED** |
| cron | **5/5 PAUSED** |
| `main` | `5bf1077…` — unchanged |

## 8. Evidence

`evidence/m6.6/REVIEW-ROUND16-2026-10-12.txt` (verbatim) ·
`…-PROMPT.txt` · `…-ROUTING.txt` (family_independent true, guard exit 0) ·
`PARENT-REVERIFY-ROUND16-2026-10-12.txt` · `CORRECTION-EXACT-TYPE-MEMBERSHIP-2026-10-12.md` ·
`RED-DEMO-ROUND16-2026-10-12.txt`

<!-- 2026-10-12 15:55 UTC+7 -->
