# QAD-ERRATUM-002-DECISION-PACKAGE

> **Status:** DECISION PACKAGE — NOT YET AUTHORIZED
> **Authority:** Pending Founder decision
> **Classification:** CONTRACT DEFECT REPAIR (2 defects)
> **Precedent:** QAD-M4A-SCHEMA-ERRATUM-001 (FD #136)
>
> **Prerequisite:** M5.3 implementation authorization blocked until this package is resolved.

---

## Background

Two contract defects were identified in the frozen M4A canonical schemas that prevent M5.3 implementation (S7 PIT Runtime Enforcement + S8 Retry Kernel) from proceeding:

| Defect | Schema | Nature | Impact |
|--------|--------|--------|--------|
| A — RRM-01 lifecycle | RRM-01 (I-1) | Required-field contradiction blocks partial-manifest creation | S8 Retry Kernel cannot create honest partial manifests |
| B — LIVE_CASE_UPDATE carrier | PITC-01 (I-2) + EV-01 (B-2) | UPDATE tag requirement has no machine-readable surface | S7 PIT Lock cannot enforce "explicitly tagged UPDATE" |

Both defects are **schema-level omissions** — the M3 authority contract requires the semantics, but the M4A frozen surface does not expose the machine-readable carrier.

---

## Defect A: RRM-01 Lifecycle / Finalization

### Frozen Schema (RRM-01, I-1)

| Field | Value |
|-------|-------|
| `required_fields` | `manifest_id, case_id, case_version, as_of_date, universe_version, selection_policy_version, models_used[], providers{}, start_time, completion_time` |
| `PIT fields` | `as_of_date, start_time, completion_time` |
| `validation_rules` | Run start record created even if run fails (partial manifest). |
| `immutability_rules` | Manifest immutable after run completion. |
| `failure_semantics` | Partial manifest if run fails. |

### Contradiction

1. `completion_time` is **REQUIRED** — must be present at record creation.
2. A partial manifest (created at run start, before completion) **cannot honestly supply** `completion_time` — it is `None` by definition.
3. `completion_time` is a **PIT field** — treated as immutable point-in-time once written.
4. Therefore: runtime cannot create a partial manifest (required by validation_rules) without violating the required_fields constraint, AND cannot mutate `completion_time` from `None` → real timestamp at run completion because PIT fields are immutable.

### Repair Options

**Option A — Add `run_state` + `completion_time`→optional**
- Move `completion_time` from `required_fields` → `optional_fields`.
- Add `run_state: RUNNING / COMPLETED / FAILED` to `required_fields`.
- `immutability_rules`: "Manifest immutable after COMPLETED or FAILED" (replaces "after run completion").
- `completion_time` becomes conditionally required: MUST be present if `run_state = COMPLETED`, MUST be absent if `run_state = RUNNING`.
- **Pro:** Clean lifecycle semantics. Partial manifest is honest (no completion_time, no sentinel value). PIT enforcement on `completion_time` naturally defers to only when it exists.
- **Con:** Adds a new field. Requires runtime generator update (set `run_state: RUNNING` at start, transition to `COMPLETED`/`FAILED` at end). Conditional validation rule is not expressible in the current flat-field table format — needs a cross-field invariant (INV-RRM-01).

**Option B — Sentinel value for `completion_time`**
- Keep `completion_time` as required but allow a sentinel value (e.g., `0001-01-01T00:00:00Z` or `PLACEHOLDER`) for partial manifests.
- At run completion, mutate the sentinel → real timestamp, with PIT exception for this specific field.
- **Pro:** No new field. Minimal schema change.
- **Con:** Sentinel values are semantically dishonest. PIT exception for one field creates a special-case loophole. Future readers see `completion_time = sentinel` and cannot distinguish "run still running" from "data corruption" without checking provenance.

**Option C — Separate finalization record (RRM-01_FINAL)**
- Keep RRM-01 as-is (partial manifest = `completion_time = PLACEHOLDER`).
- Add a new schema `RRM-02` (RunFinalization) with `manifest_id, completed_at, run_state, finalization_provenance`.
- **Pro:** Does not touch frozen RRM-01 surface. Append-only.
- **Con:** A partial manifest and its finalization are now in two records, breaking atomicity. Adds schema count (68 → 69). Extra join required for every manifest read.

### Recommended Option: **A**

The lifecycle-state field is the honest approach. A two-field pattern (`run_state` + conditional `completion_time`) is standard in run-manifest design and avoids sentinel values or split-record atomicity. The cross-field invariant (`completion_time` required iff `run_state = COMPLETED`) is a one-line addition to the M4A invariant set.

---

## Defect B: LIVE_CASE_UPDATE Provenance Carrier

### Frozen Source

**PITC-01 (I-2) `validation_rules`:**
> LIVE mode requires explicit UPDATE tag.

**SM-12 (PIT Context State Machine):**
> LIVE_CASE_UPDATE → post-AS_OF evidence ALLOWED only as explicitly tagged UPDATE
> side effects: evidence tagged with UPDATE provenance

**EV-01 (B-2) current relevant fields:**
| Field | Value |
|-------|-------|
| `required_fields` | `evidence_id, source_id, evidence_type, content, extractor, validation_status, as_of, admitting_role, source_tier` |
| `optional_fields` | `contradicts_ids[], superseded_by_id, confidence, context, extraction_method` |
| `validation_status` | `RAW / VALIDATED / CONTRADICTED / SUPERSEDED / RETRACTED / DISPUTED` |

**EAR-01 (B-9) current relevant fields:**
| Field | Value |
|-------|-------|
| `required_fields` | `admission_id, evidence_id, admitting_role, admission_timestamp, admission_method, validation_method, source_tier_check` |
| `optional_fields` | `validation_notes, original_source_verified, pit_verified, contradiction_check` |

### Gap

SM-12 requires "explicitly tagged UPDATE with provenance" for post-AS_OF evidence in LIVE mode. No frozen schema exposes a deterministic machine-readable carrier equivalent to:

- `is_update: bool` — is this evidence item a post-AS_OF update?
- `update_provenance` — who authorized the update? (e.g., research_director, pit_context_id, or a free-text justification)

The closest existing carriers are:
- `EV-01.validation_status = SUPERSEDED` — but this is for evidence replacement, not post-AS_OF update admission.
- `EAR-01.admission_method` — but this is about *how* evidence was admitted, not *whether* it is a post-AS_OF update.

### Repair Options

**Option A — Add fields to EV-01 optional_fields**
- Add `is_update: bool` and `update_provenance: text` to `EV-01.optional_fields`.
- When `is_update = true`, `update_provenance` MUST be present (conditional invariant: INV-EV-01).
- **Pro:** Single schema change. The evidence object itself carries the tag. Minimal surface impact.
- **Con:** Adds semantic weight to EV-01. The update tag is PIT-context-specific, not evidence-inherent — a piece of evidence might be an update in one context and original in another.

**Option B — Add fields to PITC-01 optional_fields**
- Add `evidence_ids[]` and `update_provenance` to `PITC-01.optional_fields`.
- The PIT context record explicitly lists which evidence items were admitted as updates.
- **Pro:** The UPDATE tag lives at the PIT context level, where the mode is defined. Natural ownership by S7 (PIT Lock Service).
- **Con:** Requires a FK relationship from PITC-01 → EV-01 for each update evidence item. PITC-01 currently has no FK to evidence. Evidence still carries no self-tag.

**Option C — Reuse/extend EAR-01**
- Add `is_update: bool` and `update_provenance: text` to `EAR-01.optional_fields`.
- EAR-01 is already the admission audit trail — adding an update flag makes it the natural carrier for "this admission was a post-AS_OF update."
- **Pro:** EAR-01 is the audit layer for evidence admission. Separates update provenance from evidence content (EV-01 stays clean). Consistent with Erratum-001 pattern (EAR-01 was already corrected once).
- **Con:** EAR-01 is a B-family (EvidenceRegistry) schema, not an I-family (Operations) schema. PIT context is an I-family concern. The provenance carrier is one hop removed from the evidence itself.

### Recommended Option: **C** (EAR-01 extension)

The update tag is an **admission concern**, not an evidence-content concern. EAR-01 exists precisely for admission provenance. Adding `is_update` + `update_provenance` to EAR-01 is the most coherent placement:

- EV-01 stays clean (evidence content is immutable — update tag is not content).
- PITC-01 stays clean (context mode controls the *gate*, not the *evidence audit trail*).
- EAR-01 already records `admission_method`, `admitting_role`, `validation_method` — `is_update` is a natural addition.
- Cross-field invariant: `if is_update = true, update_provenance MUST be present`.

---

## Scope Exclusions

This Decision Package explicitly does **NOT** propose changes to:

- Investment methodology
- M4B evaluation methodology
- State machine logic (SM-12 unaffected — the UPDATE semantics remain as frozen; only the carrier is added)
- Schema count (currently 68; Option C = 68 unchanged, Option A = 68, Option B = 68)
- FK references (no FK changes under any option)
- Retry logic (RR-01, S8 service contracts — these are M5.3 implementation, not schema repair)
- PIT enforcement logic (S7 — this is M5.3 implementation, not schema repair)
- Production stack, cost calibration, fixture sealing, routing (all remain post-M5.3 per FD #135)

---

## Implementation Sequence (if approved)

```
1. Founder decision → which option per defect (or alternative)
2. Apply targeted contract repair to QAD-M4A-CANONICAL-SCHEMAS.md
3. Regenerate type binding (QAD-M5.1-TYPE-BINDING-POLICY) if affected
4. Record QAD-ERRATUM-002.md (following Erratum-001 format)
5. Run independent contract/conformance re-check (68/68 schemas, invariants)
6. Return to M5.3 implementation authorization gate
7. Only after gate: S7 + S8 implementation begins
```

---

## Risk / Trade-off Summary

| Factor | Defect A (Opt A) | Defect B (Opt C) |
|--------|------------------|------------------|
| **Schema count change** | 68 → 68 (no change) | 68 → 68 (no change) |
| **New fields** | 1 (`run_state`) + 1 conditional invariant | 2 (`is_update`, `update_provenance`) |
| **Frozen table rows changed** | RRM-01 required_fields, immutability_rules, PIT fields | EAR-01 optional_fields |
| **Backward compatibility** | Partial manifests without `run_state` would be invalid — migration needed | New optional fields — no backward break |
| **Generator impact** | S6 must set `run_state` at creation, transition at completion | S7 must populate `is_update` + `update_provenance` on LIVE_CASE_UPDATE admissions |
| **Independent review needed** | Yes — cross-field invariant | Yes — cross-field invariant |

---

**Decision required from Founder:**
1. Defect A repair option: A / B / C / custom
2. Defect B repair option: A / B / C / custom
3. Confirm scope exclusions
4. Authorize Erratum-002 Decision Package → proceed to M5.3 implementation gate

<!-- 2026-09-07 16:08 UTC+7 -->