# FOUNDER DECISION PACKAGE — M6.6 review-loop disposition (after Round 13)

Date: 2026-10-09 · Cluster: QAD M6.6 (Noncanonical Source Discovery + Admission Bridge,
FD #151) · Branch: `impl/m6-gemini-notebook` · Head: **`88e61ce`**
`main` unchanged (`5bf107774b29e5a5fe4dcec5846800b9b48361ba`) · 5/5 cron PAUSED · M6.7 not started.

## 1. Where the loop stands

Five consecutive family-independent rounds have each returned **C** with real, bounded
implementation findings. Every one has been fixed, RED-proven and regression-tested.

| Round | Verdict | Findings | Nature |
|---|---|---|---|
| 9 | C | 1 material + 3 non-blocking | forged verification (direct verdict construction); builder signature; index bound; duplicate outcomes |
| 10 | C | 3 material | caller-authored verified EAR; verdict replay across runs; unauthenticated REPLAY_EXCEPTION |
| 11 | C | 2 material | binding not mandatory on every admission; cross-store lineage lost on re-entry |
| 12 | C | 1 material | reconciliation accepted a same-id/different-payload record |
| 13 | C | 1 material | reconciliation settled an INCOMPLETE (EV-only / EAR-only) same-id pair |

**Rounds 12 and 13 were defects introduced by the fix chain itself**, not new design gaps.

## 2. The technical pattern (this matters for the choice)

Rounds 11–13 all live in ONE small block: the evidence/disposition error handling inside
`process_discovered_sources` (a nested `try` whose broad `except Exception` downgrades
anything it catches into a "transient partial admission" outcome). Each round the reviewer
has found a different escape route into that handler:

- r11: a disposition failure after an evidence commit → lost lineage;
- r12: a same-id/different-payload record → reconciled as success;
- r13: a same-id but INCOMPLETE pair → settled as a partial outcome.

Each fix was correct in isolation, but the *structure* — a broad catch-all with several
bespoke conditions layered on top — keeps generating the next escape route. This is a
structural smell, not a series of independent bugs.

Current verified state: `tests/qad/m6` **365 passed** (M6.6 targeted **41**), M5.2+M5.3+M6.3
**460 passed**, `tests/qad` **900 passed / 1 inherited** (`test_schema_build_identity`,
unchanged attribution), `tests/ops` **94 passed**, `gate-check.sh` exit 0,
`isolation-scan.sh` exit 0, no `.sqlite3` residue, schema 68, RRM-01 unchanged.

## 3. Options (one decision)

### Option A — ONE final round, preceded by a structural simplification *(recommended)*
Before the last review, replace the broad `except Exception` in the evidence/disposition
block with an explicit, closed decision structure: classify each failure into a named
outcome (`TRANSIENT_PARTIAL`, `RECONCILED_IDENTICAL`, `CONFLICT_INCOMPLETE`,
`CONFLICT_DIVERGENT`) and let nothing else be silently absorbed — so the class of
"escapes into the transient handler" disappears instead of being patched again.
Then run ONE confirmation review (Round 14) covering that region plus a full regression sweep.
- If A/B → close M6.6 immediately with the required success status.
- If C **again inside that same region** → freeze M6.6 at the then-current fixed head with a
  documented accepted-risk note (no further fix cycles).
- Cost: one refactor + one review. Benefit: likely ends the class, and gives M6.6 a proper
  independent A/B verdict on its final head.

### Option B — FREEZE NOW at `88e61ce` (no further cycles)
Close M6.6 as **implemented with all r9–r13 findings fixed**, explicitly recording that its
final head has **no independent A/B verdict**, and carry a bounded gated item into the
pre-M6.7 gate-resolution package.
- Cost: lowest; stops spending now.
- Risk: violates the brief's own closeout gate ("independent review A or B"); the cluster
  would close on self-report for its final head. I would have to label it that way, not as a pass.

### Option C — keep iterating fix + re-review until A/B
Mechanically allowed, but on 5 rounds of evidence the marginal signal is low and I do not
recommend it.

### Option D — change the review treatment
Escalate to a different reviewer configuration (e.g. a hostile/whole-module review of the
entire `source_bridge.py` rather than the r9–r13 region, or a second independent reviewer) to
test whether the residual risk is confined to this block or broader.

## 4. Exact approval requested

Select **A**, **B**, **C**, or **D**. My recommendation is **A**.

If the Founder wants to stop spending on this cluster now, **B** is defensible provided we
record it as review-unconfirmed rather than as a pass — I will not label it an independent
pass.

## 5. Evidence

- `evidence/m6.6/REVIEW-ROUND9..13-2026-10-09.txt` (verbatim reviewer outputs) + prompts +
  routing-provenance files (all `family_independent: true`, verdict `INDEPENDENT`).
- Commit lineage: `2de4cb8` (M6.6) → `911836d` (r9) → `58ff8dc` (r10) → `a9f0370` (r11) →
  `28c1ac4` (r12) → **`88e61ce` (r13)**.
- `M6_RAW_SUCCESS_API_GATE` (FD #154) remains **OPEN** and untouched throughout.

<!-- 2026-10-09 18:05 UTC+7 -->
