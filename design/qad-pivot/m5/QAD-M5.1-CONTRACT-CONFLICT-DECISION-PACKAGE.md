# QAD-M5.1 Contract Conflict Decision Package

> **Status:** CONTRACT_CONFLICT — FOUNDER DECISION REQUIRED
> **Authority:** FD #135; M4A Canonical Schema Registry (FROZEN)
> **Baseline:** `618b33965a9448e0e9b64f86f917e7b18fdb58a5`
>
> **Gate condition violated:** CONTRACT_AMBIGUITY must equal 0 before
> M5.1 can be declared FINAL. Current value: 4.
>
> This package traces each frozen-contract contradiction to its M3 authority
> and proposes minimal errata. No M4A modification is made here.
> No runtime code changes are included.
> No M5.2 work proceeds until this package is resolved.

---

## Phase Truth Correction

Current status must be updated:

```text
M5.1 = CONTRACT_CONFLICT — FOUNDER DECISION REQUIRED
M5.2 = HOLD
```

The four conflicts blocking FINAL:

```text
EAR-01.admission_method     — M4A_SCHEMA_OMISSION
RC-01.charter_state         — M4A_SCHEMA_OMISSION
RB-01.budget_state          — M4A_SCHEMA_OMISSION
CCV-01.validation_result    — M4A_SCHEMA_OMISSION
```

---

## 1. EAR-01: `admission_method`

### M4A Schema (FROZEN)

```text
schema_id:            EAR-01
purpose:              Audit trail for every evidence admission to canonical registry.
authority_source:     M3-04 §2 (Layer 2), M3-09 §3 (Audit Checklist)
required_fields:      admission_id, evidence_id, admitting_role, admission_timestamp,
                      validation_method, source_tier_check
optional_fields:      validation_notes, original_source_verified, pit_verified,
                      contradiction_check
enums:                admission_method: DIRECT_SOURCE / AI_EXTRACTION / AI_SYNTHESIS /
                      HUMAN_ANALYSIS / SCUTTLEBUTT
```

### Conflict

The `enums` row declares `admission_method` with 5 values, but **no field named `admission_method` appears in either required_fields or optional_fields**. The closest field name is `validation_method`.

### Does `admission_method` = `validation_method`?

**No — these are distinct concepts:**

| Dimension | `admission_method` | `validation_method` |
|---|---|---|
| What it records | How evidence entered the registry | How it was checked for quality |
| Semantic range | DIRECT_SOURCE / AI_EXTRACTION / AI_SYNTHESIS / HUMAN_ANALYSIS / SCUTTLEBUTT | (unspecified in M4A — likely tier check, PIT check, contradiction check) |
| M3 evidence | INV-005 explicitly writes `EvidenceAdmissionRecord.admission_method` | M4A provenance fields row lists `validation_method` as provenance |

**M3 evidence (M4A Invariants INV-005):**

```
Enforcement: If EvidenceAdmissionRecord.admission_method = AI_SYNTHESIS
and no original_source_verified flag → VIOLATION.
```

This proves `admission_method` is a required runtime field — a contract invariant depends on it. The syntax `EvidenceAdmissionRecord.admission_method` in the invariant document is the authoritative source identifier.

### Classification: **M4A_SCHEMA_OMISSION**

`admission_method` is a genuinely missing field. It was declared in the enums row and referenced in the invariants but **accidentally omitted from the required_fields/optional_fields row**.

### Recommended Erratum

Add `admission_method` to **required_fields** (every admission needs to record how the evidence entered the registry):

```diff
- required_fields:  admission_id, evidence_id, admitting_role, admission_timestamp,
-                   validation_method, source_tier_check
+ required_fields:  admission_id, evidence_id, admitting_role, admission_timestamp,
+                   admission_method, validation_method, source_tier_check
```

**Authority:** M3-04 §2 (Layer 2 admission evidence), M3-04 §4 (AI/NotebookLM requires source validation — differentiates by admission_method). INV-005 depends on this field.

---

## 2. RC-01: `charter_state`

### M4A Schema (FROZEN)

```text
schema_id:            RC-01
purpose:              Binding research contract for a case.
authority_source:     M3-03 §3 (Stage 2: Research Charter), M3-09 §4 (Research Charter governance)
required_fields:      charter_id, case_id, hypothesis_ids[], key_questions[], evidence_scope,
                      budget_estimate, director, evidence_lead_validation
optional_fields:      timeline, budget_approved, budget_controller, source_plan,
                      material_blind_spots[]
enums:                charter_state: DRAFT / VALIDATED / BUDGET_APPROVED / ACTIVE / COMPLETED
```

### Conflict

`charter_state` is declared as an enum with 5 lifecycle states but **no field named `charter_state` appears in required or optional fields**.

### Does another field represent the same concept?

- `budget_approved` (optional, boolean) is a binary flag — whether budget was approved. This is one transition among 5 charter states.
- No other field captures the full DRAFT → VALIDATED → BUDGET_APPROVED → ACTIVE → COMPLETED lifecycle.

**M3 evidence (validation_rules + immutability_rules):**

```
validation_rules:    Charter must contain H1–H5. Evidence Lead validates evidence scope
                      completeness. Budget Controller authorizes budget.
immutability_rules:  Charter immutable after BUDGET_APPROVED.
failure_semantics:   Budget not approved → charter cannot proceed.
```

The phrase "Charter immutable after BUDGET_APPROVED" directly references `charter_state = BUDGET_APPROVED` as a lifecycle transition gate. The charter's lifecycle is a core requirement of M3-03 §3 (Stage 2: the charter must transition through defined states before research begins).

### Classification: **M4A_SCHEMA_OMISSION**

`charter_state` is a genuinely missing field. The charter lifecycle is explicit in M3. The 5-state enum matches the natural charter lifecycle.

### Recommended Erratum

Add `charter_state` to **required_fields** (every charter must have a state):

```diff
- required_fields:  charter_id, case_id, hypothesis_ids[], key_questions[], evidence_scope,
-                   budget_estimate, director, evidence_lead_validation
+ required_fields:  charter_id, case_id, hypothesis_ids[], key_questions[], evidence_scope,
+                   budget_estimate, charter_state, director, evidence_lead_validation
```

**Authority:** M3-03 §3 (Stage 2: Research Charter lifecycle), M3-09 §4 (charter governance). The 5-state lifecycle is directly implied by "Charter immutable after BUDGET_APPROVED" (M4A immutability_rules).

---

## 3. RB-01: `budget_state`

### M4A Schema (FROZEN)

```text
schema_id:            RB-01
purpose:              Per-case budget allocation and spend tracking.
authority_source:     M3-01 §9 (Budget Discipline), M3-03 §3 (Stage 2)
required_fields:      budget_id, case_id, allocated_amount, approved_by, policy_version
optional_fields:      cumulative_spend, remaining_budget, spend_breakdown[], budget_exhausted
enums:                budget_state: APPROVED / ACTIVE / EXHAUSTED / CLOSED
```

### Conflict

`budget_state` is declared as an enum with 4 lifecycle states but **no field named `budget_state` appears in required or optional fields**. The field `budget_exhausted` (boolean) exists in optional fields.

### Is `budget_state` equivalent to `budget_exhausted`?

**No.**

| Dimension | `budget_state` | `budget_exhausted` |
|---|---|---|
| What it records | 4-state lifecycle | Boolean — is budget consumed? |
| Values | APPROVED / ACTIVE / EXHAUSTED / CLOSED | true / false |
| M3 evidence | INV-003: `budget_state = EXHAUSTED` | — |

**M3 evidence (M4A Invariants INV-003):**

```
Rule: Budget exhaustion must produce INCOMPLETE, never a weakened quality gate.
Enforcement: If budget_state = EXHAUSTED and stage_state ≠ INCOMPLETE → VIOLATION.
```

The invariant is written against `budget_state = EXHAUSTED`, not `budget_exhausted = True`. The state machine needs the full 4-state field. `budget_exhausted` is a narrower concept (binary flag for one specific transition point).

### Classification: **M4A_SCHEMA_OMISSION**

`budget_state` is a genuinely missing field. The 4-state lifecycle (APPROVED → ACTIVE → EXHAUSED → CLOSED) is directly governed by M3-01 §9 (Budget Discipline) and enforced in INV-003. After inclusion, `budget_exhausted` may be redundant and could be removed from optional_fields.

### Recommended Erratum

Add `budget_state` to **required_fields** (every budget record must have a state):
Optionally remove `budget_exhausted` if superseded.

```diff
- required_fields:  budget_id, case_id, allocated_amount, approved_by, policy_version
+ required_fields:  budget_id, case_id, allocated_amount, approved_by, budget_state,
+                   policy_version
```

If `budget_exhausted` is determined to be fully superseded:

```diff
- optional_fields:  cumulative_spend, remaining_budget, spend_breakdown[], budget_exhausted
+ optional_fields:  cumulative_spend, remaining_budget, spend_breakdown[]
```

**Authority:** M3-01 §9 Budget Discipline (state machine for budget lifecycle). INV-003/M4A invariants directly dependent.

---

## 4. CCV-01: `validation_result`

### M4A Schema (FROZEN)

```text
schema_id:            CCV-01
purpose:              Record of cross-case validation for a candidate lesson.
authority_source:     M3-09 §7 (Knowledge Compounding), M3-09 §7.1 (Cross-Case Validation)
required_fields:      validation_id, lesson_id, validating_case_ids[], pattern_consistent,
                      validator, validation_date
optional_fields:      inconsistent_case_ids[], notes, industry_playbook_id
enums:                validation_result: CONFIRMED / PARTIALLY_CONFIRMED / INCONCLUSIVE /
                      REJECTED
```

### Conflict

`validation_result` is declared as an enum with 4 outcomes but **no field named `validation_result` appears**. The field `pattern_consistent` (boolean) exists in required fields.

### Are `validation_result` and `pattern_consistent` the same?

**No — distinct concepts:**

| Dimension | `pattern_consistent` | `validation_result` |
|---|---|---|
| What it records | Whether the pattern held across validating cases (binary) | Overall cross-case validation conclusion (4 states) |
| Values | true / false (boolean) | CONFIRMED / PARTIALLY_CONFIRMED / INCONCLUSIVE / REJECTED |
| Semantic nuance | Input data — factual check | Output — expert judgment incorporating nuance |

A boolean cannot express PARTIALLY_CONFIRMED or INCONCLUSIVE. These are qualitatively different outcomes — e.g., a pattern may be CONFIRMED in 3 of 5 cases and contradicted in 2 (PARTIALLY_CONFIRMED), or the evidence may be insufficient to judge (INCONCLUSIVE). Reducing this to a boolean loses the entire validation resolution spectrum.

### Classification: **M4A_SCHEMA_OMISSION**

`validation_result` is a genuinely missing field. `pattern_consistent` is the input evidence; `validation_result` is the overall judgment. Both belong in the schema.

### Recommended Erratum

Add `validation_result` to **required_fields**:

```diff
- required_fields:  validation_id, lesson_id, validating_case_ids[], pattern_consistent,
-                   validator, validation_date
+ required_fields:  validation_id, lesson_id, validating_case_ids[], pattern_consistent,
+                   validation_result, validator, validation_date
```

**Authority:** M3-09 §7.1 (Cross-Case Validation — requires 3+ independent cases, produces a validation judgment). The 4-state outcome spectrum is directly from M3-09 §7.1.

---

## Summary of Recommended Errata

| # | Schema | Change | Classification | M3 Authority |
|---|--------|--------|----------------|-------------|
| ER-001 | EAR-01 | Add `admission_method` to required_fields | M4A_SCHEMA_OMISSION | M3-04 §2/§4, INV-005 |
| ER-002 | RC-01 | Add `charter_state` to required_fields | M4A_SCHEMA_OMISSION | M3-03 §3, M3-09 §4 |
| ER-003 | RB-01 | Add `budget_state` to required_fields; remove `budget_exhausted` (optional) | M4A_SCHEMA_OMISSION | M3-01 §9, INV-003 |
| ER-004 | CCV-01 | Add `validation_result` to required_fields | M4A_SCHEMA_OMISSION | M3-09 §7.1 |

**None of these changes:**
- change investment methodology
- change enum values
- add new research concepts
- change state-machine logic
- change M4B evaluation design

All four are purely mechanical field omissions in the frozen schema row.
Apply erratum → regenerate → `CONTRACT_AMBIGUITY = 0` → `unused enums = 0` → M5.1 can close.

---

## Proof Residues (post-erratum closure patch items)

These are non-governance implementation gaps recorded for the post-erratum fix pass:

### A. `qad/validator.py` — Docstring scope gap

`validate_contract()` docstring claims to validate "FK descriptor source/target validity, canonical boundary, family, scalar type binding" but the actual implementation only checks:
- `extra=forbid` ✅
- `schema_id` present + frozen ✅
- PIT field frozen (by name heuristic) ✅

It does NOT check: field surface match, FK integrity, canonical boundary, scalar binding, collection shapes. The `validate_all_contracts()` global pass does detect unused enums and calls per-schema validate_contract, but the per-schema function's scope is narrower than claimed.

**Fix:** Either expand validate_contract() to match its docstring, or narrow the docstring to match actual scope. Recommend narrowing docstring for M5.1 (post-erratum, pre-M5.2).

### B. `SCHEMA_BUILD_IDENTITY` — `generated_artifact_hashes` missing

The generator computes `artifact_hashes` inside `main()` but does not embed them into `SCHEMA_BUILD_IDENTITY`. The dict currently has a placeholder comment:

```python
SCHEMA_BUILD_IDENTITY = {
    ...
    # generated_artifact_hashes populated post-generation via regeneration test
}
```

**Fix:** Populate `generated_artifact_hashes` before writing `__init__.py`. The generator already computes these hashes — it just needs to inject them. (Matter of ~5 lines.)

### C. Type Binding Policy stale

`QAD-M5.1-TYPE-BINDING-POLICY.md` §2 still lists only 1 TYPE_ALIAS_ENUM (`plausibility`). Current runtime has 8. §7 describes build identity as inline comments but current runtime has machine-readable `SCHEMA_BUILD_IDENTITY` dict. §6 "Unresolved Scalar Bindings" no longer matches current `SCALAR_BINDING_MAP`.

**Fix:** Update policy document to match current runtime. (Pure documentation — no methodology change.)

### D. Full regression suite proof

Last visible report was `103/103 qad conformance tests`. The full suite (`pytest tests/ -q`) was not run during this delta. The closeout does not report full suite count.

**Fix:** Run full `python -m pytest tests/ -q --tb=short` and record result in closeout.

---

## Commitment

This pass produced **zero runtime changes** and **zero M4A edits**. Only two files were created/updated:

1. `design/qad-pivot/m5/QAD-M5.1-CONTRACT-CONFLICT-DECISION-PACKAGE.md` (this file)
2. Phase-truth correction if Founder approves `M5.1 = CONTRACT_CONFLICT` status in closeout

No compiler patches. No schema regenerations. No new FD.

---

## Return Payload

```
Status:             CONTRACT_CONFLICT — FOUNDER DECISION REQUIRED
Baseline SHA:       618b33965a9448e0e9b64f86f917e7b18fdb58a5

EAR-01 classification:   M4A_SCHEMA_OMISSION — admission_method missing from field row
RC-01 classification:    M4A_SCHEMA_OMISSION — charter_state missing from field row
RB-01 classification:    M4A_SCHEMA_OMISSION — budget_state missing from field row
CCV-01 classification:   M4A_SCHEMA_OMISSION — validation_result missing from field row

Recommended action:     Approve minimal 4-row erratum QAD-M4A-SCHEMA-ERRATUM-001
                         (field additions only, no semantic changes)
                        Then: apply erratum → regenerate → fix 3 proof residues →
                         verify CONTRACT_AMBIGUITY = 0 → M5.1 = FINAL → M5.2 PROCEED
```

<!-- 2026-08-24 -->