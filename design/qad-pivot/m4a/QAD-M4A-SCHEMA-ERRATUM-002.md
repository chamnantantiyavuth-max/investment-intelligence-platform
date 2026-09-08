# QAD-M4A-SCHEMA-ERRATUM-002

> **Status:** APPROVED / APPLIED
> **Authority:** FD #137 (7 Sep 2026)
> **Classification:** M4A_CONTRACT_DEFECT_REPAIR — field additions + one conditional-immutability lifecycle materialization + one FK
>
> **Supersession:** M4A remains FINAL / FROZEN. Two contract defects corrected by this
> erratum: (1) RRM-01 lifecycle contradiction (required-field + PIT-immutable blocking
> honest partial manifests), (2) EAR-01 missing LIVE_CASE_UPDATE provenance carrier.
> No methodology, schema count, or state machine logic changes. One new enum
> (`run_state`) and one new FK (`update_pit_context_id → PITC-01`) added.

---

## Background

The M5.3 Verify-First pre-authorization analysis (SESSION_CLOSEOUT.md, 7 Sep 2026)
identified two contract defects in the frozen M4A canonical schemas that block M5.3
implementation (S7 PIT Runtime Enforcement + S8 Retry Kernel):

| Defect | Schema | Nature |
|--------|--------|--------|
| ER-005 | RRM-01 (I-1) | Required-field contradiction: `completion_time` required + PIT-immutable, yet partial manifest requires `completion_time = None` at run start |
| ER-006 | EAR-01 (B-9) | SM-12 / PITC-01 validation_rules require "explicitly tagged UPDATE with provenance" for LIVE_CASE_UPDATE mode, but no frozen schema exposes `is_update`, `update_provenance`, or `update_pit_context_id` |

Both are classified **M4A_CONTRACT_DEFECT_REPAIR**: the frozen contract contains a
semantic contradiction (ER-005) or a missing carrier for an M3-required invariant
(ER-006). No existing enum value set was altered, but one new enum (`run_state`)
and one new FK (`update_pit_context_id → PITC-01`) were added. Schema count stays 68.

---

## Changes

### ER-005: RRM-01 (ResearchRunManifest) — Lifecycle Finalization

**Problem:** `completion_time` was in `required_fields` and `PIT fields`, but
`validation_rules` require a partial manifest at run start — before `completion_time`
can be known. PIT immutability then blocks the honest `None → timestamp` transition
at run completion.

**Action:**
1. Move `completion_time` from `required_fields` → `optional_fields`.
2. Add `run_state: RUNNING / COMPLETED / FAILED` to `required_fields` + `enums`.
3. Update `immutability_rules` to reference lifecycle states.
4. Add lifecycle validation rules:
   - `completion_time` MUST be absent if `run_state = RUNNING`
   - `completion_time` REQUIRED if `run_state = COMPLETED` or `FAILED`
5. Classify `completion_time` as `CONDITIONAL_IMMUTABLE` (PIT field that may
   transition absent→present exactly once during RUNNING→COMPLETED/FAILED finalization).
6. Classify `run_state` as `APPEND_ONLY_STATE` (lifecycle transitions validated
   by persistence/state layer).
7. Identity anchors (`manifest_id`, `case_id`, `case_version`, `as_of_date`,
   `start_time`) remain `FIELD_IMMUTABLE` at all times.

**Before (RRM-01):**
```text
required_fields:  manifest_id, case_id, case_version, as_of_date, universe_version,
                  selection_policy_version, models_used[], providers{}, start_time,
                  completion_time
optional_fields:  model_versions{}, prompts_contracts[], notebook_runs[],
                  deep_research_runs[], sources_added, calculation_version,
                  token_usage{}, cost{}, retries, failures[], output_version
immutability_rules:  Manifest immutable after run completion.
```

**After (RRM-01):**
```text
required_fields:  manifest_id, case_id, case_version, as_of_date, universe_version,
                  selection_policy_version, models_used[], providers{}, start_time,
                  run_state
optional_fields:  completion_time, model_versions{}, prompts_contracts[],
                  notebook_runs[], deep_research_runs[], sources_added,
                  calculation_version, token_usage{}, cost{}, retries, failures[],
                  output_version
enums:            run_state: RUNNING / COMPLETED / FAILED
immutability_rules:  Manifest immutable after COMPLETED or FAILED.
validation_rules:  Run start record created even if run fails (partial manifest).
                   completion_time MUST be absent if run_state = RUNNING;
                   REQUIRED if run_state = COMPLETED or FAILED.
PIT fields:        as_of_date, start_time, completion_time  (unchanged —
                   completion_time is CONDITIONAL_IMMUTABLE: absent→present
                   one-time transition during finalization)
```

---

### ER-006: EAR-01 (EvidenceAdmissionRecord) — UPDATE Provenance Carrier

**Problem:** SM-12 (PIT Context State Machine) requires post-AS_OF evidence in
LIVE_CASE_UPDATE mode to be "explicitly tagged UPDATE with provenance." PITC-01
validation_rules repeat: "LIVE mode requires explicit UPDATE tag." No frozen
schema exposes a deterministic machine-readable carrier (`is_update`,
`update_provenance`, `update_pit_context_id`).

**Action:**
1. Add `is_update: bool` and `update_provenance: text` to `EAR-01.optional_fields`.
2. Add `update_pit_context_id: str` to `EAR-01.optional_fields` with FK
   `update_pit_context_id → PITC-01.pit_context_id`.
3. Add cross-field validation rules:
   - If `is_update = true`: `update_provenance` REQUIRED, `update_pit_context_id` REQUIRED
   - Referenced PITC must exist with `mode = LIVE_CASE_UPDATE`
   - PITC `created_by` must represent Research Director authority (per SM-12)

**Rationale for EAR-01 placement:** The update tag is an **admission concern**, not
an evidence-content concern. EAR-01 already records `admission_method`,
`admitting_role`, `validation_method` — `is_update` is a natural addition. EV-01
stays clean (evidence content is immutable — update tag is not content). PITC-01
stays clean (context mode controls the *gate*, not the *evidence audit trail*).
The `update_pit_context_id` FK provides deterministic machine-readable linkage
to the PIT context that authorized the update.

**Before (EAR-01):**
```text
optional_fields:  validation_notes, original_source_verified, pit_verified,
                  contradiction_check
IDs / foreign keys:  admission_id, evidence_id → EV-01.evidence_id
validation_rules:  AI/NotebookLM synthesis must be validated against original source.
                   L10 cannot be admitted as sole material support.
```

**After (EAR-01):**
```text
optional_fields:  validation_notes, original_source_verified, pit_verified,
                  contradiction_check, is_update, update_provenance,
                  update_pit_context_id
IDs / foreign keys:  admission_id, evidence_id → EV-01.evidence_id,
                     update_pit_context_id → PITC-01.pit_context_id
validation_rules:  AI/NotebookLM synthesis must be validated against original source.
                   L10 cannot be admitted as sole material support.
                   If is_update = true, update_provenance REQUIRED and
                   update_pit_context_id REQUIRED; referenced PITC must have
                   mode = LIVE_CASE_UPDATE and created_by must represent
                   Research Director authority.
```

---

## Scope Exclusions

This erratum explicitly does NOT change:

- Investment methodology
- M4B evaluation methodology
- State machine logic (SM-12 unaffected — UPDATE semantics remain as frozen; carriers are added)
- Schema count (remains 68 — no new schema, no deletion)
- Production stack, cost calibration, fixture sealing, routing (all remain post-M5.3 per FD #135)
- Any existing enum value set (one NEW enum `run_state` added: RUNNING/COMPLETED/FAILED)
- `completion_time` PIT field status (remains in PIT fields — CONDITIONAL_IMMUTABLE absent→present one-time transition during finalization)

**New additions:**
- One new FK: `EAR-01.update_pit_context_id → PITC-01.pit_context_id` (FK count 87→88)
- One new enum: `RRM-01.run_state: RUNNING / COMPLETED / FAILED`

---

## Historical Traceability

Original M4A freeze at M4A closeout baseline, modified by Erratum-001 (FD #136),
now modified by Erratum-002.

```text
pre-erratum-002 canonical source baseline =
  (M4A-FROZEN + ERRATUM-001)

Erratum-002 authority =
  FD #137 (7 Sep 2026)
```

---

## Verification

After application (regenerated from source of truth):

```text
CONTRACT_AMBIGUITY = 0
unused enum classes = 0
schemas = 68
FK references = 88
FIELD_ENUM = 73
TYPE_ALIAS_ENUM = 8
Total enum declarations = 81  (+1: run_state added)
```

Cross-field invariants:
- INV-RRM-01: `completion_time` REQUIRED if `run_state = COMPLETED` or `FAILED`; MUST be absent if `run_state = RUNNING`
- INV-EAR-01: `update_provenance` REQUIRED if `is_update = true`
- INV-EAR-02: `update_pit_context_id` REQUIRED if `is_update = true`; referenced PITC must have `mode = LIVE_CASE_UPDATE`

**Verification truth (2026-09-08 — Erratum-002 independent-audit correction cycle, Commit C + Commit D):**

| Check | Result | Class |
|---|---|---|
| Full pytest suite | **630/630 PASS** (LOCAL, hermes-agent venv) | LOCAL — real run, 5.35s |
| QAD contract conformance | 105/105 PASS | LOCAL |
| M4A validator (`validate-m4a-contracts.py`) | 173/173 PASS | LOCAL |
| M4B validator (`validate-m4b-pack.py`) | 93/93 PASS | LOCAL |
| Item-13 cross-contract (`test_cross_contract_validation.py`) | 7/7 PASS | LOCAL |
| RRM lifecycle targeted (`TestRrmLifecycle`) | 11/11 PASS | LOCAL |
| LIVE carrier targeted (`TestLiveUpdateCarrier`) | 7/7 PASS | LOCAL |
| Five-anchor live-update integration (`test_erratum002_diagnostic_five_anchor.py`) | 16/16 PASS | LOCAL |

All counts are LOCAL pytest results on the corrected implementation. GitHub/Vercel
deploy status is NOT Python CI and proves nothing about the test suite.

> **Change note vs the 596/596 claim:** this erratum's verification section
> originally recorded the pre-Erratum-002-era full suite count "596/596". The
> post-Erratum suite is larger (630 = 596 - 0 + 18 Erratum-002 defect-closure
> + 16 five-anchor integration). The 596/596 claim is superseded by the exact
> LOCAL counts above.

<!-- 2026-09-07 16:20 UTC+7 (updated 2026-09-08: verification truth corrected to exact post-correction LOCAL counts) -->