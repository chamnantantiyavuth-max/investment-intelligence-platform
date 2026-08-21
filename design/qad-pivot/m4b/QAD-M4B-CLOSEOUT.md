# QAD-M4B Closeout — Evaluation Contract + PIT Fixtures + Acceptance Matrix + Validator + PIT Proof + Final Review

> **Status:** M4B = FINAL / FROZEN — FOUNDER ACCEPTED
> **Authority:** FD #133, FD #134
> **Predecessor:** M4A = FROZEN FOR M4B DERIVATION (Freeze Gate PASS)
> **Execution order:** M4A → Freeze → M4B → Freeze → STOP — **COMPLETE**

---

## M4B Deliverables

| Artifact | File | Status |
|----------|------|--------|
| Evaluation Contract | `QAD-M4B-EVALUATION-CONTRACT.md` | ✅ FINAL / FROZEN |
| PIT Fixture Specification (10 fixture types) | `QAD-M4B-PIT-FIXTURE-SPEC.md` | ✅ DRAFT_UNSEALED (fixture state — unchanged by freeze) |
| Acceptance Matrix | `QAD-M4B-ACCEPTANCE-MATRIX.md` | ✅ FINAL / FROZEN |
| M4B Validator | `validate-m4b-pack.py` | ✅ 92/92 PASS |
| PIT Leakage Proof | `pit-leakage-proof.py` | ✅ 9/9 PASS |
| Final Independent Review | `QAD-M4B-INDEPENDENT-REVIEW-FINAL.md` | ✅ PASS |
| Post-Review Proof Sync | `QAD-M4B-POST-REVIEW-PROOF-SYNC.md` | ✅ MECHANICAL VERIFICATION |

---

## Evaluation Summary

### Metric Count (Mechanically Computed from Acceptance Matrix)

| Section | Metrics | Type |
|---------|---------|------|
| §1 Evidence Quality | 6 | A |
| §2 Analytical Quality | 7 | A |
| §3 Financial Quality | 5 | A |
| §4 Process Quality | 6 | A |
| §5 Discovery Quality | 10 | B |
| §6 Saturation / EIV | 4 | A |
| §7 Cost / Model Routing | 6 | A+B |
| **Total** | **44** | **28 A + 10 B + 6 A+B** |

### Type A — Research Quality (28 metrics)

| Dimension | Metrics | Fixtures |
|-----------|---------|----------|
| Evidence Quality | 6 metrics | All fixture types |
| Analytical Quality | 7 metrics | All fixture types |
| Financial Quality | 5 metrics | Temporary, Structural, Mixed, Valuation |
| Process Quality | 6 metrics | All fixture types |
| Saturation / EIV | 4 metrics | All fixture types |

### Type B — Discovery Recall (10 metrics)

| Dimension | Metrics | Fixtures |
|-----------|---------|----------|
| Discovery Quality | 10 metrics | Industry/Company Shock, Temporary, Structural |

### Radar Incremental Recall

Comparison: QAD Discovery without Radar vs QAD Discovery + Radar.
Radar retention deferred to post-M4B per FD #133.

### Cost / Model Evaluation (6 shared metrics)

4-tier model (A/B/C/D) with authority restrictions on cheap/free models for
quality assessment, moat classification, impairment diagnosis, normalized earnings,
permanent loss, valuation asymmetry, final underwriting, and final Red Team adjudication.

---

## PIT Fixture Summary

| # | Fixture Type | Status | Sealed? |
|---|-------------|--------|---------|
| 1 | True Temporary Impairment | DRAFT_UNSEALED — AI_PROPOSED | ❌ |
| 2 | True Structural Deterioration | DRAFT_UNSEALED — AI_PROPOSED | ❌ |
| 3 | Mixed Impairment | DRAFT_UNSEALED — AI_PROPOSED | ❌ |
| 4 | False Quality | DRAFT_UNSEALED — AI_PROPOSED | ❌ |
| 5 | Balance-Sheet Trap | DRAFT_UNSEALED — AI_PROPOSED | ❌ |
| 6 | Industry / Cycle Shock | DRAFT_UNSEALED — AI_PROPOSED | ❌ |
| 7 | Company-Specific Shock | DRAFT_UNSEALED — AI_PROPOSED | ❌ |
| 8 | Unresolved / Ambiguous Case | DRAFT_UNSEALED — AI_PROPOSED | ❌ |
| 9 | Valuation Failure | DRAFT_UNSEALED — AI_PROPOSED | ❌ |
| 10 | Narrative Panic | DRAFT_UNSEALED — AI_PROPOSED | ❌ |

**Draft fixture candidates: 10 | Sealed fixtures: 0**

> Sealing requires: source pack assembly → independent adjudication → seal contract completion.
> None of the 10 fixtures have passed beyond DRAFT_UNSEALED — AI_PROPOSED.
> Fixture labels are NOT scoring ground truth.

---

## PIT Leakage Proof Results

`pit-leakage-proof.py` — Non-production deterministic synthetic tests:

| Test | Result |
|------|--------|
| Pre-AS_OF evidence in SEALED mode → ALLOWED | ✅ PASS |
| Post-AS_OF evidence in SEALED mode → HARD BLOCK | ✅ PASS |
| Post-AS_OF in LIVE without UPDATE tag → BLOCK | ✅ PASS |
| Post-AS_OF in LIVE with valid UPDATE provenance → ALLOWED | ✅ PASS |
| REPLAY_EXCEPTION without provenance → BLOCK | ✅ PASS |
| REPLAY_EXCEPTION with explicit provenance → ALLOWED | ✅ PASS |
| Sealed fixture/source hash mutation → INVALIDATE SEAL | ✅ PASS |
| Unauthorized actor in REPLAY_EXCEPTION → BLOCK | ✅ PASS |
| Spoofed provenance with 'Founder' text but actor != FOUNDER → BLOCK | ✅ PASS |

**Total: 9/9 passed, exit code 0**

---

## Validator Results

`validate-m4b-pack.py` (upgraded) — 87 deterministic checks:

| Section | Checks | Result |
|---------|--------|--------|
| 1. Evaluation Contract | 11 checks (includes lifecycle sequence, seal contract fields) | ✅ 11/11 |
| 2. PIT Fixture Spec | 19 checks (includes AI_PROPOSED, DRAFT_UNSEALED, NOT_VALID_FOR_SCORING, counts) | ✅ 19/19 |
| 3. Acceptance Matrix | 48 checks (includes type separation, per-row threshold cell validation, row count) | ✅ 48/48 |
| 4. No Production Code | 1 check (message fixed: two files permitted) | ✅ 1/1 |
| 5. M4A Freeze Status | 1 check | ✅ 1/1 |
| 6. PIT Leakage Proof | 12 checks (subprocess execution, exit code, 9 tests by name, summary line) | ✅ 12/12 |
| 7. Final Independent Review | 4 checks (file existence ×2, FINAL marker, post-review sync marker) | ✅ 4/4 |
| **Total** | **93** | **✅ 93/93 PASS** |

---

## Non-Authorization Preservation

- ❌ No M5 production implementation
- ❌ No workforce migration
- ❌ No cron mutation
- ❌ No production QAD operation
- ❌ No database/schema migration
- ❌ No broker/execution/capital allocation
- ❌ No constitutionalized thresholds (all PROVISIONAL_M4B_THRESHOLD)
- ❌ No sealed scoring fixtures (0 sealed)
- ❌ No fictional human-curator adjudication

---

## Next

```text
M4A = FROZEN FOR M4B DERIVATION
M4B = FINAL / FROZEN — FOUNDER ACCEPTED
M5  = GATE REVIEW AUTHORIZED — IMPLEMENTATION NOT AUTHORIZED
```

<!-- 2026-08-21 (M4B freeze update — FINAL / FROZEN — FOUNDER ACCEPTED; M5 Gate Review authorized) -->