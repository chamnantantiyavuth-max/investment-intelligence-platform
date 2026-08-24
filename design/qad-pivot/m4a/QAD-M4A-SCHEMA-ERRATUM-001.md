# QAD-M4A-SCHEMA-ERRATUM-001

> **Status:** APPROVED / APPLIED
> **Authority:** FD #136 (24 Aug 2026)
> **Classification:** M4A_SCHEMA_OMISSION — bounded field additions only
>
> **Supersession:** M4A remains FINAL / FROZEN. Four schema-field omissions
> corrected by this erratum per FD #136. No methodology, enum value, state
> machine, invariant, or schema count changes.

---

## Background

M5.1 implementation exposed four frozen M4A contracts where an enum declaration
existed in the `enums` row but the corresponding field was absent from both
`required_fields` and `optional_fields`. These were confirmed by M3 authority
cross-reference and M4A invariant dependency (INV-003, INV-005).

All four are classified **M4A_SCHEMA_OMISSION**: the field was semantically
intended and declared in the enums row, but accidentally omitted from the
field-surface row.

---

## Changes

### ER-001: EAR-01 (EvidenceAdmissionRecord)

**Field:** `admission_method`

**Enum values:** `DIRECT_SOURCE / AI_EXTRACTION / AI_SYNTHESIS / HUMAN_ANALYSIS / SCUTTLEBUTT`

**Action:** Add to required_fields

**Evidence:** INV-005 explicitly references `EvidenceAdmissionRecord.admission_method`.
Distinct from `validation_method` (provenance field).

**Before:**
```text
required_fields:  admission_id, evidence_id, admitting_role, admission_timestamp,
                  validation_method, source_tier_check
```

**After:**
```text
required_fields:  admission_id, evidence_id, admitting_role, admission_timestamp,
                  admission_method, validation_method, source_tier_check
```

---

### ER-002: RC-01 (ResearchCharter)

**Field:** `charter_state`

**Enum values:** `DRAFT / VALIDATED / BUDGET_APPROVED / ACTIVE / COMPLETED`

**Action:** Add to required_fields

**Evidence:** M3-03 §3 (Stage 2: Research Charter lifecycle). M4A immutability_rules
states "Charter immutable after BUDGET_APPROVED" — directly references charter_state.

**Before:**
```text
required_fields:  charter_id, case_id, hypothesis_ids[], key_questions[], evidence_scope,
                  budget_estimate, director, evidence_lead_validation
```

**After:**
```text
required_fields:  charter_id, case_id, hypothesis_ids[], key_questions[], evidence_scope,
                  budget_estimate, charter_state, director, evidence_lead_validation
```

---

### ER-003: RB-01 (ResearchBudgetRecord)

**Field:** `budget_state`

**Enum values:** `APPROVED / ACTIVE / EXHAUSTED / CLOSED`

**Action:** Add to required_fields

**Note:** `budget_exhausted` (optional, boolean) is **RETAINED** as a convenience
flag. The two fields represent distinct concepts: `budget_state` is the 4-state
lifecycle truth; `budget_exhausted` is a derived/convenience boolean.

**Evidence:** INV-003 enforces `If budget_state = EXHAUSTED`. M3-01 §9 (Budget
Discipline) defines the lifecycle.

**Before:**
```text
required_fields:  budget_id, case_id, allocated_amount, approved_by, policy_version
```

**After:**
```text
required_fields:  budget_id, case_id, allocated_amount, approved_by, budget_state,
                  policy_version
```

`budget_exhausted` remains in optional_fields unchanged.

---

### ER-004: CCV-01 (CrossCaseValidation)

**Field:** `validation_result`

**Enum values:** `CONFIRMED / PARTIALLY_CONFIRMED / INCONCLUSIVE / REJECTED`

**Action:** Add to required_fields

**Note:** `pattern_consistent` (boolean) is **RETAINED**. It represents the
input evidence (did the pattern hold?), while `validation_result` is the overall
expert judgment. A boolean cannot express PARTIALLY_CONFIRMED or INCONCLUSIVE.

**Evidence:** M3-09 §7.1 (Cross-Case Validation requires 3+ independent cases
and produces a structured validation judgment with 4 outcomes).

**Before:**
```text
required_fields:  validation_id, lesson_id, validating_case_ids[], pattern_consistent,
                  validator, validation_date
```

**After:**
```text
required_fields:  validation_id, lesson_id, validating_case_ids[], pattern_consistent,
                  validation_result, validator, validation_date
```

---

## Scope Exclusions

This erratum explicitly does NOT change:

- Investment methodology
- Enum values (all 4 enums remain exactly as frozen)
- M4B evaluation methodology
- State machine logic (SM-2, SM-4, SM-11 unaffected)
- Invariants (INV-003, INV-005 continue to use the same field names —
  the fields now exist in the machine-bindable surface)
- Schema count (remains 68)
- FK references (no FK changes)
- `budget_exhausted` (RETAINED in RB-01 optional_fields)

---

## Historical Traceability

Original M4A freeze at M4A closeout baseline (see QAD-M4A-CLOSEOUT.md) contained these
field omissions. The frozen M4A closeout document and the original M4A source hash
remain valid as historical snapshots. This erratum is an amendment, not a rewrite.

```text
pre-erratum canonical source baseline =
232e84d2e963cb455cbfa11cd7b79d56133577f8

pre-erratum source SHA256 =
d4b27d82e72fa856c334709abbcc808eb14c3a7d2c4b710b29ffdb847b2a49ba

post-erratum source SHA256 =
6755cff07cbb240a8bab8eb49ab39894f5673c73322e51c4e2ead932f706dfa6

Erratum application commit =
440d3323810d377073088b7a4ecaba46918a3499

Erratum authority =
FD #136 (24 Aug 2026)
```

---

## Verification

After application and regeneration:

```text
CONTRACT_AMBIGUITY = 0
unused enum classes = 0
FIELD_ENUM = 72
TYPE_ALIAS_ENUM = 8
Total enum declarations = 80
schemas = 68
```

Cross-checked by runtime validator (68/68 PASS, 0 global violations) and
`test_contract_conformance.py` (103/103 PASS).

<!-- 2026-08-24 -->