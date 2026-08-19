# QAD Logical Organization — Role & Service Registry

> **Status:** M3 FINAL — FROZEN FOR M4 DERIVATION
> **Authority:** FD #130; Frozen Architecture (Separation of Duties); Constitution §2 (QAD Capabilities)
> **Traceability:** M3-01 §6 (Separation of Duties) · M3-02 (Discovery & Selection) · M3-03 (Research Protocol) · M3-04 (Evidence) · M3-05 (Scuttlebutt) · M3-06 (Business/Industry/Management) · M3-07 (Impairment/Recovery) · M3-08 (Economic Underwriting) · M3-09 (Challenge/Audit/Publication) · FD #130 · NEW_M3_DERIVATION (classification, compatibility matrices)

---

## 1. Logical Organization Chart

```text
FOUNDER
  │
  │  Final Judgment / Authority
  │
  ┌──────────────────────────┼──────────────────────────┐
  │                          │                          │
  ▼                          ▼                          ▼
DISCOVERY & COVERAGE     RESEARCH INSTITUTION       INDEPENDENT ASSURANCE
  │                          │                          │
  ├─ Quality Discovery       ├─ Research Director       ├─ Structural Red Team
  ├─ Dislocation Radar       ├─ Evidence Intelligence   ├─ Independent Auditor
  ├─ Discovery Scout          ├─ Core Desk Research      │
  ├─ Candidate Builder       ├─ Business & Industry     └─ (evaluation)
  └─ Selection Engine        ├─ Financial & Management
                              ├─ Impairment Diagnosis
                              ├─ Valuation / Expectations
                              └─ Chief Underwriter

                                          │
                                          ▼
                                     Thai Editor
                                          │
                                          ▼
                                      FOUNDER
                                          │
                                          ▼
                                    Thesis Monitoring
                                          │
                                          ▼
                                    Knowledge Steward
```

### Horizontal Services

```text
Research Budget Controller
Canonical Evidence Registry
Raw Source Archive
Security / Entity Resolution Service
Source / PIT / Provenance Infrastructure
Run Manifest / Reproducibility Infrastructure
NotebookLM / Deep Research Interface
Publication Infrastructure
Evaluation Laboratory
Selection Engine (policy-governed service)
```

---

## 2. Classification Key

| Code | Classification | Description |
|------|---------------|-------------|
| **J** | HUMAN_OR_AGENT_JUDGMENT_ROLE | Requires judgment, analysis, or synthesis — may be human or AI |
| **P** | POLICY_SERVICE | Applies approved policy rules deterministically |
| **D** | DETERMINISTIC_SERVICE | Pure computation, no judgment |
| **EI** | ELASTIC_INVESTIGATOR | On-demand investigator deployed from specific evidence gaps |
| **I** | INFRASTRUCTURE | System/platform capability |
| **IA** | INDEPENDENT_ASSURANCE_ROLE | Independent challenge or verification |
| **PU** | PUBLICATION_ROLE | Written output, journalism |

---

## 3. Logical Role Registry

| # | Role | Classification | Mission | Inputs | Outputs | Cannot Combine With |
|----|------|---------------|---------|--------|---------|--------------------|
| 1 | **Research Director / Case Orchestrator** | J | Orchestrate full research on an approved case. Assign stages, manage evidence gaps, produce Research Charter, ensure quality gates are met. **Research Charter is validated by Evidence Intelligence Lead (evidence/protocol completeness) and budget-approved by Research Budget Controller. Chief Underwriter does NOT approve Charter.** | Candidate from Selection Engine, Evidence Gap Map | Research Charter, case orchestration decisions, stage transitions | Independent Auditor, Structural Red Team, Selection Engine |
| 2 | **Evidence Intelligence Lead** | J | Manage source gathering, evidence validation, canonical admission, and evidence graph maintenance for a case. Ensure source/PIT/provenance discipline. | Raw sources, Research Charter, Evidence Gap Map | Canonical Evidence Registry entries, evidence quality assessments | Independent Auditor |
| 3 | **Core Desk Researcher** | J | Perform deep desk research: read filings, synthesize cross-source evidence, produce analytical notes, identify contradictions. | Primary source foundation, Research Charter | Desk research notes, source extracts, FACT/CLAIM/INFERENCE candidates | Structural Red Team |
| 4 | **Business & Industry Analyst** | J | Analyze business quality, moat, customer economics, and industry structure. Produce quality assessment. | Canonical Evidence Registry, industry data | Quality Assessment (VERIFIED/PROBABLE/UNRESOLVED/FAILED), Industry Economics Analysis | Structural Red Team, Chief Underwriter |
| 5 | **Financial & Management Analyst** | J | Perform financial reconstruction, management assessment, capital allocation analysis, per-share economics. | Company filings, market data | Financial Reconstruction (7-10+ years), Management Assessment, Calculation Lineage | Chief Underwriter |
| 6 | **Impairment Diagnosis Specialist** | J | Diagnose impairment type (temporary/structural/mixed/unresolved), build recovery model. | Quality Assessment, Financial Reconstruction, Dislocation data | Impairment Diagnosis, Recovery Model, Thesis Killers | Chief Underwriter |
| 7 | **Valuation & Expectations Specialist** | J | Perform Reverse DCF, scenario analysis, permanent loss analysis, economic vs price damage. | Financial Reconstruction, Impairment Diagnosis, Recovery Model | Valuation scenarios, Reverse DCF, Permanent Loss Analysis, Valuation Asymmetry | Chief Underwriter |
| 8 | **Chief Underwriter** | J | Synthesize all analytical work + Red Team + Audit into final research verdict. | All analytical outputs, Red Team findings, Audit Report | Research Verdict (QAD_CONFIRMED/.../NOT_QAD_VALUATION), monitoring indicators | Selection Engine, Portfolio Manager, any analytical role (4-7) |
| 9 | **Structural Red Team** | IA | Assume QAD thesis is wrong. Construct strongest value-trap case. Challenge all assumptions. | Full research record (analytical outputs + evidence) | Challenge outcomes (ACCEPTED/.../UNRESOLVED), strongest opposing case | Research Director, any research/analytical role (1-7) |
| 10 | **Independent Research Auditor** | IA | Verify source existence, citation correctness, PIT integrity, calculation reproducibility. | Full research record, raw sources | Audit Report (PASS/PASS_WITH_FINDINGS/FAIL), may block FOUNDER_READY | Research Director, Evidence Intelligence, any research role |
| 11 | **Thai Long-Form Research Editor** | PU | Transform research into Thai long-form journalism for publication. | Research record, research verdict | Published Thai article (FOUNDER_READY input), companion CRO article | Chief Underwriter |
| 12 | **Thesis / Knowledge Steward** | J | Monitor thesis-specific indicators. Manage knowledge compounding. Cross-case validation. | Research verdict, monitoring indicators, case outcomes | Monitoring state transitions, Candidate Lesson proposals, APPROVED KNOWLEDGE | Structural Red Team |
| 13 | **Discovery & Dislocation Scout** | J/EI | Detect, surface, connect, and raise questions from signals that structured sensors may miss. Radar Scout (CAP-011 — transitional). | External signals, ecosystem data, unstructured sources | Signal Registry entries, Task Idea Cards | Selection Engine, Chief Underwriter |
| 14 | **Elastic Investigator** | EI | Deploy on-demand from specific evidence gaps. Gather primary ecosystem intelligence. | Scuttlebutt Charter (Evidence Gap ID, falsifiable question, sources) | Investigation Reports, new evidence for Canonical Evidence Registry | (single-purpose per charter) |

---

## 4. Separation of Duties Matrix

| Role A | Role B | Conflict? | Rationale |
|--------|--------|-----------|-----------|
| Research Director | Independent Auditor | **FORBIDDEN** | Cannot audit own orchestration |
| Research Director | Structural Red Team | **FORBIDDEN** | Cannot challenge own case |
| Evidence Intelligence | Independent Auditor | **FORBIDDEN** | Cannot verify own evidence |
| Business/Industry Analyst | Chief Underwriter | **FORBIDDEN** | Underwriter must be independent of analytical work |
| Financial/Management Analyst | Chief Underwriter | **FORBIDDEN** | Underwriter must be independent of analytical work |
| Impairment Specialist | Chief Underwriter | **FORBIDDEN** | Underwriter must be independent of diagnosis |
| Valuation Specialist | Chief Underwriter | **FORBIDDEN** | Underwriter must be independent of valuation |
| Discovery Scout | Selection Engine | **FORBIDDEN** | Discovery may not self-select |
| Selection Engine | Chief Underwriter | **FORBIDDEN** | Selection may not underwrite its own choices |
| Chief Underwriter | Portfolio Manager | **FORBIDDEN** | Underwriting may not allocate capital |
| Structural Red Team | Chief Underwriter | **ALLOWED** (with findings preserved) | Red Team outputs go to Underwriter; Underwriter weighs but cannot suppress |
| Publication Editor | Thesis Creator | **ALLOWED** (with separation) | Editor edits; does not create thesis |

---

## 5. Service Registry

| # | Service | Classification | Inputs | Outputs | State | Failure Behavior |
|---|---------|---------------|--------|---------|-------|-----------------|
| S1 | **Autonomous Selection Engine** | P | CANDIDATE_REGISTRY entries, selection policy rules | Selection state (AUTO_RESEARCH_NOW/WATCH_PRICE/etc) | Stateless (per-candidate evaluation) | **SELECTION_ERROR** on system failure (never SKIP) |
| S2 | **Research Budget Controller** | P | Research Budget policy, case budget request | Budget approval or denial; budget exhaustion → INCOMPLETE | Per-case state | Budget exhausted = INCOMPLETE, not weakened gate |
| S3 | **Security / Entity Resolution** | D | Raw entity identifiers (ticker, CIK, name, exchange) | Resolved entity identity, SECURITY_MASTER update | Persistent (entity registry) | Unresolvable entity = documented exclusion, not silent omission |
| S4 | **Canonical Evidence Registry** | I | Evidence objects (FACT/CLAIM/INFERENCE/HYPOTHESIS) with provenance | Validated, curated evidence records | Persistent append-only | Write failure = evidence quarantined; retry on next tick |
| S5 | **Raw Source Archive** | I | Source documents (SEC filings, PDFs, web pages) | Immutable source file with content hash, timestamp, source_id | Append-only store | Source unreachable = skip, document gap |
| S6 | **Run Manifest Service** | I | Research run metadata | Run manifest record (research_run_id, model, cost, PIT, etc.) | Append-only | Run start record created even if run fails (partial manifest) |
| S7 | **Point-in-Time Lock** | D | Case AS_OF_DATE, evidence timestamps, source timestamps | PIT-validated evidence context for each case | Query-time evaluation | LIVE: flagged/UPDATE tag; **SEALED: HARD BLOCKED**; REPLAY: provenance-recorded exception |
| S8 | **Retry / Research Execution Controller** | I | Research stage execution request, retry policy, budget state | Stage execution, retry scheduling, failure disposition | Per-case state | Stage FAILED → max 3 retries; after 3 → stage marked FAILED; case continues with documented failure |
| S9 | **Case Locking / Idempotency** | D | Case ID, version, request type | Lock/unlock state; deduplication by key | Stateful (case locks) | Duplicate case Open request → return existing case, no second write |
| S10 | **NotebookLM / Deep Research Interface** | I | Research question, source corpus, prior evidence | Synthesis output, source pointers (NON-CANONICAL) | Stateless | Research failure = documented, not silent blank |
| S11 | **Publication Renderer** | D | Research verdict, evidence synthesis, Thai editorial template | Rendered publication draft (markdown) | Stateless | Template error = plain output, not failed publication |
| S12 | **Evaluation Harness** | I | Sealed outcome corpus, PIT snapshots, evaluation policy | Evaluation metrics (Type A + Type B) | Stateless (evaluation run) | Partial evaluation = **EVALUATION_INCOMPLETE** (not partial results; cannot satisfy evaluation gate) |

---

## 6. Role Compatibility (Runtime Implementation)

Each logical role may be implemented by a different runtime entity (Hermes profile, subagent, or deterministic service). Roles may be **COMBINED** in one entity only if they have no conflict AND the combination is actively justified.

### Permitted Combinations (no conflict)

| Entity | Roles | Justification |
|--------|-------|---------------|
| Research Desk | Research Director + Core Desk Researcher | Same entity orchestrates AND performs desk research (standard practice) |
| Business & Finance Desk | Business/Industry Analyst + Financial/Management Analyst | Interrelated analytical domains |
| Impairment & Valuation Desk | Impairment Specialist + Valuation Specialist | Sequential analytical chain |
| Evidence Desk | Evidence Intelligence Lead + Evidence Registry (S4/S5) operations | Evidence gathering and management |
| Edit Desk | Thai Editor + Publication Renderer (S10) operation | Publication chain |
| Monitor Desk | Thesis/Knowledge Steward + Monitoring operations | Ongoing surveillance |
| Discovery Desk | Discovery/Dislocation Scout + Discovery operations | Signal detection |
| Independent Desk | Can implement EITHER Red Team OR Auditor (NOT both for same case) | Independence requires separation from thesis |

### Forbidden Combinations (always separate)

| Must Be Separate | Reason |
|-----------------|--------|
| Selection Engine ≠ Research Director | Selection policy must not be influenced by the researcher |
| Research Director ≠ Independent Auditor | Cannot audit own work |
| Chief Underwriter ≠ any analytical role | Underwriter must be independent judgment |
| Structural Red Team ≠ Research Director | Cannot challenge own case |
| Chief Underwriter ≠ Portfolio Manager | Underwriting is research, not allocation |

---

## 7. Minimum Runtime Profiles (Logical Map Only — NOT a Hermes profile count)

The architecture permits one runtime profile to implement multiple compatible low-conflict functions where justified, and prohibits combination where separation of duties matters.

### Independence Domains (Minimum)

| Domain | Roles | Authority Boundary |
|--------|-------|-------------------|
| **A — Research / Evidence / Compatible Analysts** | Roles 1, 2, 3, 4, 5, 6, 7, 12, 13, 14 | May be combined within A subject to individual separation rules |
| **B — Chief Underwriter** | Role 8 only | **Must be independent of Domain A** |
| **C — Structural Red Team** | Role 9 only | **Must be independent of A and B** |
| **D — Independent Auditor** | Role 10 only | **Must be independent of A, B, and C** |
| **E — Thai Editor** | Role 11 only | **Must be independent of thesis creation (Roles 1, 8)** |

Selection Engine is a POLICY SERVICE (fully separate from all domains).

**No fewer than 5 independent authority entities** (one per domain A–E). These are authority boundaries, not Hermes profile counts. A single runtime entity may implement multiple roles within Domain A where no individual separation rule is violated. But Domains A, B, C, D, and E must never be collapsed into fewer than 5 independent authority entities.

### Permitted Combinations (within Domain A)

| Entity | Roles | Justification |
|--------|-------|---------------|
| Research Desk | Research Director + Core Desk Researcher | Same entity orchestrates AND performs desk research (standard practice) |
| Business & Finance Desk | Business/Industry Analyst + Financial/Management Analyst | Interrelated analytical domains |
| Impairment & Valuation Desk | Impairment Specialist + Valuation Specialist | Sequential analytical chain |
| Evidence Desk | Evidence Intelligence Lead + Evidence Registry (S4/S5) operations | Evidence gathering and management |
| Edit Desk | Thai Editor + Publication Renderer (S10) operation | Publication chain |
| Monitor Desk | Thesis/Knowledge Steward + Monitoring operations | Ongoing surveillance |
| Discovery Desk | Discovery/Dislocation Scout + Discovery operations | Signal detection |
| Independent Desk | Can implement EITHER Red Team OR Auditor (NOT both for same case) | Independence requires separation from thesis |

<!-- 2026-08-19 14:00 UTC+7 -->