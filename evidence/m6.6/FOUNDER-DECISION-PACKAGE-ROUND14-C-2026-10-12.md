# FOUNDER DECISION PACKAGE — M6.6 ROUND-14 VERDICT = C (OPTION A+ STOP RULE ENGAGED)

**Cluster:** QAD M6.6 — Noncanonical Source Discovery + Admission Bridge (FD #151)
**Branch:** `impl/m6-gemini-notebook` · **Refactor commit reviewed:** `38dcd9f`
`main` unchanged (`5bf107774b29e5a5fe4dcec5846800b9b48361ba`) · 5/5 cron PAUSED · M6.7 NOT started
**Date:** 2026-10-12

---

## 0. What happened

The Founder's **Option A+** direction authorized ONE bounded structural refactor of the M6.6
evidence-admission / reconciliation / disposition boundary, focused tests, then **ONE**
family-independent confirmation review, **with a stricter closeout condition**: closeout only on
**A or B**; on **C → STOP, do not freeze the finding as accepted risk, return a decision package**.

**Round 14 returned `C` with 1 material finding, 0 non-blocking findings, 0 evidence gaps.**

Per the A+ STOP rule, this package is returned and **nothing was fixed, frozen, re-reviewed or
closed**:

- ❌ M6.6 is **NOT closed**.
- ❌ The finding is **NOT** frozen as accepted risk.
- ❌ No independent PASS is claimed (Round 14 was **C**).
- ❌ No further fix and no further review cycle was started.
- ❌ Nothing was carried into M6.7 (M6.7 remains NOT STARTED).
- ✅ The raw refactor **did fix the defect it was commissioned to fix** (proven — see §3).
- ℹ️ `M6_RAW_SUCCESS_API_GATE` remains **OPEN** and blocking.

Round 14 (GPT-6 Luna high, family-independent from the DeepSeek producer; disposable no-`.git`
copy; external basetemp; read-only — the reviewer modified no reviewed file) is the **sixth
consecutive C** on this cluster.

## 1. The finding (verbatim from the reviewer)

> **1. Unknown admission errors are reconciled as successful evidence when read-back finds an exact pair.**
> (a) `source_bridge.py:1208-1238` only fast-fails `SourceBridgeError`; otherwise an exact pair
> returns `RECONCILED_IDENTICAL` regardless of the original exception. In an end-to-end probe, a
> pre-seeded exact pair was unchanged (same EV/EAR hashes before and after), `admit_evidence`
> raised `RuntimeError` without writing, yet `process_discovered_sources` returned `IMPORTED`,
> linked EV-A/EAR-A, cleared pending, and wrote one disposition.
> (b) This converts an unexpected canonical-boundary failure into a successful durable candidate
> outcome, contrary to the required fail-closed behavior.
> (c) Before reconciling, propagate unrecognized exception classes unchanged; retain read-back
> reconciliation only for explicitly recognized failure classes.
> (d) Add direct-classifier and end-to-end cases for unknown errors with exact canonical traces;
> assert original-error propagation, pending candidate, no disposition, and unchanged canonical hashes.

Also recorded by the reviewer as a **DEFECT at probe 11** (reported, not listed as a separate
material finding): *"deleting its `SourceBridgeError` fail-fast guard still leaves all 64 target
tests passing"* — a **test-strength gap** on the same boundary.

## 2. Parent re-verification — the finding is VALID and MATERIAL

The Parent reproduced it independently (never accepting a reviewer self-report) against `38dcd9f`,
using a scenario where the exact canonical pair is genuine — it was committed by an **earlier
attempt of the same candidate** whose disposition write failed:

```
SCENARIO A: exact canonical pair (from an earlier attempt) + UNKNOWN error
  attempt-1 raised: LedgerValidationError (expected)
  canonical pair committed: EV=True EAR=True
  candidate still pending : True
  RETRY RETURNED (no exception): disposition=IMPORTED evidence_ids=('EV-A',) ear_ids=('EAR-A',) err=None
  dispositions after retry: [('SC-00924423d0fee0943b0fc715', 'IMPORTED', ('EV-A',), ('EAR-A',))]
  pending after retry     : ()
  canonical hashes unchanged: True
  SCENARIO A VERDICT: FINDING REPRODUCED (settled as reconciled success)
```

An **unrecognized** exception was converted into a durable, lineage-claiming successful candidate
outcome. That is exactly what the Founder's direction forbids
(§3 "An unknown exception must propagate or return an explicit FAIL-CLOSED outcome, without a
fabricated disposition"; §5 "Keep … out of transient handling").

Raw evidence: `evidence/m6.6/PARENT-REVERIFY-ROUND14-2026-10-12.txt`.

## 3. Classification: **REGRESSION INTRODUCED BY THE REFACTOR** (not a new design gap)

Same probe, run against the **pre-refactor** bridge (parent commit `1a5002e`, bridge sha256
`99eb4099…`) in a throwaway worktree:

| Scenario | PRE-refactor (`1a5002e`) | POST-refactor (`38dcd9f`) |
|---|---|---|
| **A** unknown error + EXACT canonical pair | settled `IMPORTED` with `evidence_ids=()` / `ear_ids=()` — **no lineage claim**, reason honestly said "canonical evidence admission FAILED … no canonical evidence was admitted" | settled `IMPORTED` **claiming EV-A / EAR-A** ← **the finding** |
| **B** unknown error + NO canonical trace | **RETURNED with no exception** — settled `IMPORTED`, nothing recorded as a failure → **FAIL CLOSED BROKEN** | **propagates `RuntimeError`**, candidate pending, no disposition, no canonical write ← **fixed** |

**Reading.**
- The refactor **achieved its primary objective**: the "unknown error → ordinary partial outcome"
  downgrade that Rounds 11–13 were about is **gone** for the no-trace case (Scenario B now fails
  closed).
- But the refactor **widened** the guard that gets you *into* reconciliation. Before the refactor
  reconciliation was entered only from an explicit allowlist —
  `except (IntegrityConflict, TransactionFailure):` — so an unrecognized failure **could never**
  enter it. After the refactor the classifier enters reconciliation for **any** non-`SourceBridgeError`
  failure and then decides purely on read-back. That is a **broadened entry condition = a
  regression introduced by the refactor**, inside exactly the boundary A+ was commissioned to close.

**Affected boundary (precise):** the *reconciliation ENTRY* decision in
`classify_evidence_admission_failure` — **not** the reconciliation comparison itself. The reviewer
VERIFIED (probe 4) that identity / source-binding / payload / hash comparison correctly yields
`CONFLICT_DIVERGENT`; probe 2/3/5 VERIFIED the divergent, incomplete and read-back-failure paths.

**Same root cause as the probe-11 defect.** Removing the `SourceBridgeError` early-raise guard is
behaviourally equivalent *except* in the exact-pair case — which is precisely the case no test
covers today. So probe 11 is not an independent defect: it is the same unhandled case, seen from
the test-strength side.

## 4. Minimal correction (analysed, NOT applied — STOP rule)

Restore an explicit **reconciliation-entry allowlist**: only *recognized* collision classes may
enter read-back reconciliation (`IntegrityConflict`, `TransactionFailure`); every other exception
class propagates unchanged **before** read-back. ~10 lines in
`classify_evidence_admission_failure`.

Why it is the smallest sufficient correction: it restores a condition that **already existed in
the pre-refactor code and was accepted through Rounds 11–13**, rather than inventing new policy.
It is expected to preserve every accepted behaviour — `test_38` re-entry
(`IntegrityConflict`), rows 05/13 (`IntegrityConflict` / `TransactionFailure` reconcile), `test_39`
and rows 06–08 (divergent), tests 40/41 and rows 03/04 (incomplete) — and to close the probe-11
gap (an unknown error with an exact pair would then propagate, which the new cases assert).

**All statements in this section are UNEXECUTED analysis. Nothing was implemented, so nothing here
is verified.** The finding remains open.

## 5. Options (one decision)

### Option A — apply the minimal bounded correction, then ONE Round-15 confirmation review *(recommended)*
Apply §4 + the reviewer's requested cases (direct-classifier + end-to-end, unknown error with an
exact trace: assert original-error propagation, pending candidate, no disposition, unchanged
canonical hashes) + a RED demonstration + the full regression matrix, then **ONE** family-independent
Round-15 review of that commit.
- 🔎 Why: the finding is a **single, precisely located, previously-narrowed guard** with a known
  minimal edit, and §3 proves *empirically* what the correct entry condition was. This is a bounded
  correction, not a re-design.
- ⚠️ Cost/risk: one more fix + one more review on a cluster that has now had six C rounds. I do
  **not** claim the correction works; it is unexecuted.

### Option B — FREEZE M6.6 at `38dcd9f` as **review-unconfirmed**, carrying the open finding forward
Close M6.6 with its final head explicitly labelled **no independent A/B verdict**, the C finding
recorded **open (not accepted as risk)**, and a blocking item added to the pre-M6.7
gate-resolution package.
- 🔎 Honest and cheap; stops spending now.
- ⚠️ It contradicts the brief's own closeout gate ("independent review A or B") — I would have to
  label it review-unconfirmed, **not** a pass. And the open finding sits on the admission boundary,
  i.e. on the path M6.7 SUCCESS integration would depend on.

### Option C — revert the refactor to the pre-refactor behaviour
Not recommended: the pre-refactor comparison proves that revert re-opens Scenario B (unknown error
silently settled, fail-closed broken) — strictly worse than the current head.

### Option D — change the review treatment instead of the code
Escalate to a different independent treatment (e.g. GPT-6 Sol high hostile review of the whole
`source_bridge.py` rather than the refactored region, or a second independent reviewer) to test
whether the residual risk is confined to this boundary or broader.
- Reasonable if the Founder's concern is now "is 6× C a symptom of something wider?" rather than
  "fix this one guard".

## 6. Exact approval requested

Select **A**, **B**, **C**, or **D**. My recommendation is **A** — one bounded correction plus one
confirmation review, because the correction restores an entry condition that was already accepted
before the refactor, and because closing on B would leave the cluster without any independent A/B
verdict on a boundary that has failed six consecutive reviews.

If the Founder wants to stop spending on this cluster now, **B** is defensible **provided it is
recorded as review-unconfirmed, not as a pass** — I will not label it a pass.

## 7. Current status (unchanged by this package)

| Item | Status |
|---|---|
| M6.6 | `IMPLEMENTED / NOT CLOSED / ROUND-14 = C ON THE REFACTOR COMMIT` |
| Round-14 verdict | **C** — 1 material finding (open), 0 non-blocking, 0 evidence gaps |
| Fix applied for the finding | **NONE** (STOP rule) |
| M6.6 labelled a pass? | **NO** |
| Finding frozen as accepted risk? | **NO** |
| `M6_RAW_SUCCESS_API_GATE` | **OPEN / BLOCKING** before M6.7 SUCCESS execution |
| M6.7 | **NOT STARTED** |
| cron | **5/5 PAUSED** |
| `main` | `5bf107774b29e5a5fe4dcec5846800b9b48361ba` — unchanged |

## 8. Evidence

- `evidence/m6.6/REVIEW-ROUND14-2026-10-12.txt` — reviewer output, **verbatim**
- `evidence/m6.6/REVIEW-ROUND14-2026-10-12-PROMPT.txt` — the exact prompt used
- `evidence/m6.6/REVIEW-ROUND14-2026-10-12-ROUTING.txt` — family-independence provenance
  (`family_independent: true`, guard exit 0, reviewer self-ID probe)
- `evidence/m6.6/PARENT-REVERIFY-ROUND14-2026-10-12.txt` — Parent reproduction + pre-refactor
  comparison, raw
- `evidence/m6.6/DECISION-OPTION-A-PLUS-2026-10-12.md` — the A+ choice, recorded accurately
- `evidence/m6.6/REFACTOR-CLOSED-DECISION-STRUCTURE-2026-10-12.md` — root cause, closed decision
  structure, classification table, code/tests changed, RED→GREEN proof, actual test counts
- `evidence/m6.6/RED-DEMO-2026-10-12.txt` — the executed RED→GREEN demonstration
- Commit lineage: `88e61ce` (r13) → `1a5002e` (docs) → **`38dcd9f` (the refactor, reviewed)**

<!-- 2026-10-12 13:25 UTC+7 -->
