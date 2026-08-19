# QAD-M4A Independent Schema Consistency Review — FINAL

> **Review date:** 2026-08-19  
> **Scope:** M4A Schema Registry + State Machines + Invariants + Traceability + Validator  
> **Method:** Independent read-only verification against frozen M3 domain contracts  
> **Status:** **PASS — All 11 checklist items verified.** Minor cosmetic issues noted.

---

## Executive Summary

The M4A artifact suite has been comprehensively corrected from earlier defects. The semantic contract validator (`validate-m4a-contracts.py`) passes **183/183 checks with 0 failures**:

```
Results: 183 passed, 0 failed, 0 warnings
```

All 11 independent review checkpoints are satisfied. Two **minor non-blocking** issues were found — stale section-header count annotations in the schemas document — that do not affect correctness.

---

## Checklist Verification

### 1. ✅ 68 Expected Canonical Schemas (All Present)

**Evidence:** Exact regex match for `| **schema_id** | <ID> |` produced **68 unique schema IDs**. The validator confirms `Schema count: 68 (expected ≥68)`.

**Distribution by family:**

| Family | Count | Schema IDs |
|--------|-------|------------|
| A — Identity & Coverage | 6 | SM-01, RU-01, SR-01, CR-01, QU-01, CASE-01 |
| B — Source & Evidence | 10 | SRC-01, EV-01, FACT-01, CLM-01, INF-01, HYP-01, CTR-01, EG-01, EAR-01, SRCV-01 |
| C — Research Governance | 8 | RC-01, RSR-01, IC-01, RB-01, RFR-01, HS-01, IR-01, RSR-02 |
| D — Business/Industry/Mgmt | 7 | QA-01, MA-01, IE-01, MC-01, CAE-01, MDL-01, MO-02 |
| E — Impairment & Recovery | 6 | DR-01, IA-01, CE-01, RM-01, TK-01, FE-01 |
| F — Financial & Economic | 8 | FF-01, NFF-01, CALC-01, SCEN-01, PLA-01, RDCF-01, VA-01, PIE-01 |
| G — Challenge/Audit/Pub | 7 | RTC-01, AF-01, AG-01, UV-01, PUB-01, FDR-01, CRESP-01 |
| H — Monitoring & Knowledge | 7 | MI-01, MO-01, MASS-01, CL-01, IKR-01, IPR-01, CCV-01 |
| I — Reproducibility & Ops | 9 | RRM-01, PITC-01, SI-01, RR-01, CLK-01, BU-01, MOD-01, PROV-01, EHR-01 |
| **Total** | **68** | |

**Minor issue (cosmetic — does not affect correctness):**
Section header annotations in the schemas file include stale counts:
- **Section B** header says "(11 schemas)" but actual count is 10 (B-1 through B-10). Should say "(10 schemas)".
- **Section C** header says "(9 schemas)" but actual count is 8 (C-1 through C-8). Should say "(8 schemas)".

The total sum of header annotations (6+11+9+7+6+8+7+7+9 = 70) does not match the actual schema count of 68 due to these two stale headers. The closeout summary table correctly lists family counts, and the closeout text correctly states **"Total: 68 schemas"**. The validator checks the actual count (68) and passes.

**Recommendation:** Update section headers B and C to read "(10 schemas)" and "(8 schemas)" respectively on next edit.

---

### 2. ✅ All 14 Correct M3 Roles (Role 13/14 Verified)

**Source:** `QAD-M3-PRODUCTION-ROLE-CONTRACTS.md` — Role 13 (p. 338) and Role 14 (p. 363).

| # | Role | Verified |
|---|------|----------|
| 1 | Research Director / Case Orchestrator | ✅ |
| 2 | Evidence Intelligence Lead | ✅ |
| 3 | Core Desk Researcher | ✅ |
| 4 | Business & Industry Analyst | ✅ |
| 5 | Financial & Management Analyst | ✅ |
| 6 | Impairment Diagnosis Specialist | ✅ |
| 7 | Valuation & Expectations Specialist | ✅ |
| 8 | Chief Underwriter | ✅ |
| 9 | Structural Red Team | ✅ |
| 10 | Independent Research Auditor | ✅ |
| 11 | Thai Long-Form Research Editor | ✅ |
| 12 | Thesis / Knowledge Steward | ✅ |
| **13** | **Discovery & Dislocation Scout** | ✅ Correct name, no longer "Radar Scout" |
| **14** | **Elastic Investigator** | ✅ Correct name |

Validator confirms all 14 role names present in the schemas document (check 6 passes for all roles).

---

### 3. ✅ Role 14 Output = InvestigationReport (IR-01) — Exists

**Evidence:**
- Schema `IR-01` exists as **C-8: InvestigationReport** at line 500 of the schemas file.
- Schema purpose: *"Output of Role 14 (Elastic Investigator)."*
- Owner: Elastic Investigator (Role 14).
- Required fields include `investigation_id`, `investigator_charter_id`, `evidence_gap_id`, `falsifiable_question`, `disposition` with enum `ANSWERED / NOT_ANSWERED / PARTIALLY_ANSWERED`.
- Matches M3 Role 14 output schema: `{investigation_id, evidence_gap_id, falsifiable_question, findings, sources[], sampling_limitations, disposition, proposed_evidence_ids[], stop_rule_triggered, investigator}`.
- Validator check 14 passes: `InvestigationReport schema ID: IR-01` and `Role 14: Elastic Investigator referenced`.

---

### 4. ✅ S1–S12 Service I/O Mapping

**Evidence:** Validator check 7 confirms all 12 service concepts appear in the schemas document:

| Service | Concept | Schema Ownership / Key Reference |
|---------|---------|----------------------------------|
| S1 | Autonomous Selection Engine | Policy service (not an owner); validates CR-01 selection state transitions |
| S2 | Research Budget Controller | **Owner** of RB-01 (ResearchBudgetRecord), BU-01 (BudgetUsage) |
| S3 | Security / Entity Resolution | **Owner** of SM-01 (SecurityMaster) |
| S4 | Canonical Evidence Registry | Data layer; EV-01 and related evidence schemas reference it |
| S5 | Raw Source Archive | Data layer; SRC-01, SRCV-01 reference it |
| S6 | Run Manifest Service | **Owner** of RRM-01, SI-01, MOD-01, PROV-01 |
| S7 | Point-in-Time Lock | **Owner** of PITC-01 (PITContext) |
| S8 | Retry / Research Execution Controller | **Owner** of RR-01 (RetryRecord) |
| S9 | Case Locking / Idempotency | **Owner** of CLK-01 (CaseLock) |
| S10 | Notebook / Deep Research Interface | Interface service; validation rules reference NotebookLM across evidence schemas |
| S11 | Publication Renderer | PUB-01 owner is Thai Editor (Role 11); S11 is the rendering service |
| S12 | Evaluation Harness | **Owner** of EHR-01 (EvaluationHarnessRun) |

**Conclusion:** Every service maps unambiguously to at least one canonical schema or is explicitly referenced in validation rules. No guessing required.

---

### 5. ✅ Zero Dangling Foreign Keys

**Evidence:** Systematic verification of all FK targets:

- **25 unique FK target schemas** extracted from all `→ <SCHEMA-ID>.<field>` references in the schemas file.
- **All 25 FK targets exist** in the 68-schema set.
- No FK references to `ER-01` (an old predecessor ID for evidence records) — validator confirms: `No dangling FK ER-01 (should be EV-01)`.
- No FK references to `SR-02` (the old ScenarioRecord ID, now `SCEN-01`) — validator confirms: `No SR-02 schema ID (should be SCEN-01)`.
- No FK references to non-existent schemas.

**FK targets verified (all present):** AF-01, AG-01, CASE-01, CL-01, CR-01, EG-01, EV-01, FF-01, HYP-01, IA-01, IC-01, IKR-01, MC-01, MI-01, MOD-01, PLA-01, PUB-01, RB-01, RDCF-01, RTC-01, SI-01, SM-01, SR-01, SRC-01, UV-01.

---

### 6. ✅ No Unauthorized Candidate Scoring (No `priority_score` in CandidateRecord)

**Evidence:**
- Regex search over the CandidateRecord section (A-4) confirms `priority_score` is **not present**.
- The CR-01 validation rule explicitly states: *"Selection Engine must NOT score or rank candidates (M3 S1)."*
- `FORBIDDEN_FIELDS = {"priority_score"}` is enforced by validator check 9: `Forbidden field not present: priority_score` ✅.

---

### 7. ✅ Technical Detector Failure ≠ `NO_SIGNAL` (`DETECTION_ERROR` Exists)

**Evidence:**
- SignalRecord (SR-01) `failure_semantics` field explicitly distinguishes:
  - *"Successful scan with no material signal → `NO_SIGNAL`."*
  - *"Technical/data/detector failure → `DETECTION_ERROR` (candidate retryable; never silent Type-B miss)."*
- Both enum values exist distinctly in the schemas file.
- Validator check 10 confirms both: `✅ DETECTION_ERROR exists` and `✅ NO_SIGNAL exists`.

---

### 8. ✅ PIT Modes Traced to M3 (Not `NEW_M4A_DERIVATION`)

**Evidence:**
- PITContext schema `authority_source` = `M3-01 §8 (PIT Lock), M3-SERVICES S7 (PIT Lock)`.
- The three PIT modes (`LIVE_CASE_UPDATE`, `SEALED_HISTORICAL_EVALUATION`, `REPLAY_EXCEPTION`) are explicitly defined by M3-SERVICES S7.
- Traceability document **NEW_M4A_DERIVATION Item 7** states: *"The 3-mode taxonomy is NOT NEW_M4A_DERIVATION — it is frozen in M3."*
- Only the field-level data model (ID scheme, representation) is NEW_M4A_DERIVATION — this is correctly documented.
- Validator check 15 confirms all 3 PIT modes present: `✅ PIT mode: REPLAY_EXCEPTION`, `✅ LIVE_CASE_UPDATE`, `✅ SEALED_HISTORICAL_EVALUATION`.

---

### 9. ✅ PIT Fail-Closed (Not Fail-Open)

**Evidence:**
- PITContext schema `failure_semantics` = *"PIT service unavailable → queries blocked (fail closed)."*
- SM-12 (PIT Context State Machine) contains **3 explicit `FAIL CLOSED`** annotations:
  - `LIVE_CASE_UPDATE` → *"PIT service failure: FAIL CLOSED (no PIT-unchecked access)"*
  - `SEALED_HISTORICAL_EVALUATION` → *"PIT service failure: FAIL CLOSED"*
  - `REPLAY_EXCEPTION` → *"PIT service failure: FAIL CLOSED"*
- SM-12 illegal transitions explicitly prohibit *"Any PIT-unchecked query (fail closed on service failure)."*
- Validator check 11 confirms: `✅ PIT fail-closed behavior`.
- INV-004 and INV-015 in the invariants document reinforce hard-block semantics for SEALED mode.

---

### 10. ✅ NEW_M4A_DERIVATION Reconciliation (9 Items, Not 0)

**Evidence:** The traceability document's `NEW_M4A_DERIVATION Items` section lists exactly **9 items** across 4 categories:

| # | Category | Item | Details |
|---|----------|------|---------|
| 1 | Operational Telemetry | I-3: ServiceInvocation (SI-01) | Invocation status enum, duration_ms, I/O summary |
| 2 | Operational Telemetry | I-4: RetryRecord (RR-01) | Invocation_id link, attempt_number, ESCALATED status |
| 3 | Operational Telemetry | I-6: BudgetUsage (BU-01) | resource_type enum (TOKEN/API_CALL/etc.) |
| 4 | Operational Telemetry | I-7: ModelInvocation (MOD-01) | Token/cost telemetry, prompt_hash, latency |
| 5 | Operational Telemetry | I-8: ProviderInvocation (PROV-01) | Provider wrapper, fallback tracking |
| 6 | Evidence Gap → IC Link | EG-01.investigator_charter_id | FK linkage between EG-01 and IC-01 |
| 7 | PIT Enumeration | PITC-01 field-level model | Data model representation (modes themselves are M3) |
| 8 | Naming Convention | Schema ID format (XX-NN) | M4A design convention |
| 9 | Naming Convention | UUID v7 as primary ID | M4A implementation choice |

Validator check 12 confirms: `✅ NEW_M4A_DERIVATION in traceability (10 references)` — the 10th reference is the section header or summary table.

Validator check 18 confirms closeout consistency: `✅ Closeout reports 9 NEW_M4A_DERIVATION`.

---

### 11. ✅ Semantic Validator Coverage

The `validate-m4a-contracts.py` (340 lines) implements **19 semantic check groups** covering all verification dimensions:

| Check | Focus | Checks | 
|-------|-------|--------|
| 1 | Schema count | ≥68 |
| 2 | Required schema IDs | 68 specific IDs |
| 3 | No forbidden IDs | SR-02 absent |
| 4 | No duplicate IDs | All unique |
| 5 | Canonical enums (8 categories, 39 values) | Moat, Impairment, Selection, Evidence, Verdict, Quality, Monitoring, PIT modes |
| 6 | M3 role mapping | All 14 roles |
| 7 | S1-S12 service I/O | All 12 service concepts |
| 8 | No dangling FKs | ER-01, SR-02 checks |
| 9 | No forbidden fields | priority_score absent |
| 10 | Signal failure semantics | DETECTION_ERROR + NO_SIGNAL |
| 11 | PIT fail-closed | FAIL_CLOSED present |
| 12 | NEW_M4A_DERIVATION | Traceability references |
| 13 | EvidenceGap resolvability | 3 resolvability classes |
| 14 | InvestigationReport | IR-01 + Elastic Investigator |
| 15 | PIT modes traced to M3 | All 3 modes present |
| 16 | State machine checks | 12 machines + fail-closed + hard-block |
| 17 | Invariant checks | 15 invariants (INV-001 through INV-015) |
| 18 | Closeout consistency | 68 schemas + 9 derivations |
| 19 | No production code | Only validator .py present |

**Total: 183 passes, 0 failures, 0 warnings.** Every review checkpoint is covered by at least one automated check.

---

## Summary of Findings

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | 68 canonical schemas | ✅ PASS | 68 found. Minor: section B header says 11 (actual 10), section C says 9 (actual 8) — stale annotations. |
| 2 | 14 M3 roles (13/14 correct) | ✅ PASS | Role 13 = Discovery & Dislocation Scout, Role 14 = Elastic Investigator |
| 3 | Role 14 output = IR-01 | ✅ PASS | InvestigationReport (C-8) exists with correct schema |
| 4 | S1-S12 service I/O | ✅ PASS | All 12 services map to schema ownership or explicit references |
| 5 | Zero dangling foreign keys | ✅ PASS | All 25 FK targets verified as existing schemas |
| 6 | No priority_score in CR-01 | ✅ PASS | Scoring prohibition enshrined in validation rules |
| 7 | DETECTION_ERROR != NO_SIGNAL | ✅ PASS | Both distinct failure semantics documented in SR-01 |
| 8 | PIT modes traced to M3 | ✅ PASS | Authority = M3-SERVICES S7; not NEW_M4A_DERIVATION |
| 9 | PIT fail-closed | ✅ PASS | 3 explicit FAIL CLOSED annotations in SM-12 |
| 10 | NEW_M4A_DERIVATION = 9 items | ✅ PASS | 9 items across 4 categories in traceability |
| 11 | Validator coverage | ✅ PASS | 19 check groups, 183/183 pass |

---

## Recommendations

1. **Optional (cosmetic):** Fix section B header from "(11 schemas)" to "(10 schemas)" and section C from "(9 schemas)" to "(8 schemas)" in `QAD-M4A-CANONICAL-SCHEMAS.md` to match actual counts. The total of 68 is correct.

2. **Ready for freeze gate.** No blocking issues found. All 11 independent review criteria are satisfied.

---

## Verification Method

- All 7 source files read in full.
- Systematic regex extraction of all 68 schema IDs, 25 FK targets, 14 role names, 12 service names.
- Validator executed: `python validate-m4a-contracts.py` → **183/183 PASS**.
- Zero modifications made to any artifact.
- Review file written to: `QAD-M4A-INDEPENDENT-REVIEW-FINAL.md`.

<!-- 2026-08-19 17:30 UTC+7 -->