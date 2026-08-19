# QAD-M4A Canonical Schema Registry

> **Status:** M4A IN PROGRESS
> **Authority:** FD #133; M3 Domain Contracts (FROZEN for M4 derivation)
> **Traceability:** Every schema traces to M3 contract clause — see QAD-M4A-SCHEMA-TRACEABILITY.md
> **Design principle:** Technology-neutral JSON Schema-like pseudocode. No production database technology chosen.

---

# Schema Design Template

Every schema below uses:

```text
schema_id
version
purpose
authority_source (M3 contract clause)
owner (logical role)
required_fields
optional_fields
field_types
enums
IDs / foreign keys
PIT fields
provenance fields
validation_rules
immutability_rules
revision_rules
failure_semantics
canonical_vs_noncanonical_boundary
```

---

## A — Identity & Coverage (6 schemas)

### A-1: SecurityMaster

| Field | Value |
|-------|-------|
| **schema_id** | SM-01 |
| **purpose** | Canonical identity for every known security. Ground truth for entity resolution. |
| **authority_source** | M3-02 §2 (Registry 1: SECURITY_MASTER), M3-02 §7 (Data Architecture) |
| **owner** | Security / Entity Resolution Service (S3) |
| **required_fields** | `entity_id`, `primary_ticker`, `cik`, `name`, `exchange`, `security_type`, `status` |
| **optional_fields** | `isin`, `sedol`, `adr_flag`, `dual_listings[]`, `ticker_history[]`, `corporate_actions[]`, `sector`, `industry` |
| **enums** | `security_type: COMMON_EQUITY / ADR / PREFERRED / WARRANT / ETF / FUND / OTHER` |
| | `status: ACTIVE / DELISTED / MERGED / ACQUIRED / SPINOFF / UNKNOWN` |
| **IDs / foreign keys** | `entity_id: UUID v7` (primary), `cik: string` (SEC identifier), `primary_ticker: string` |
| **PIT fields** | `as_of_date`, `effective_date`, `termination_date` |
| **provenance fields** | `source`, `retrieval_timestamp`, `data_version`, `resolver` |
| **validation_rules** | Every entity must have at least one ticker or CIK. Duplicate CIK must be resolved to same entity. |
| **immutability_rules** | `entity_id` immutable. Ticker changes create ticker_history entries. |
| **revision_rules** | Corporate actions create new version with superseded_by pointer. |
| **failure_semantics** | Unresolvable entity → `ENTITY_UNRESOLVED` state (documented exclusion, not silent omission). |
| **canonical_boundary** | Canonical. All other registries reference SM-01 entity_id. |

### A-2: ResearchableUniverseRecord

| Field | Value |
|-------|-------|
| **schema_id** | RU-01 |
| **purpose** | Every researchable operating company with explicit inclusion/exclusion state. No silent omissions. |
| **authority_source** | M3-02 §2 (Registry 2: RESEARCHABLE_UNIVERSE), M3-02 §6 (Hard Filters) |
| **owner** | Discovery & Coverage System |
| **required_fields** | `entity_id`, `inclusion_state`, `inclusion_reason`, `as_of_date` |
| **optional_fields** | `exclusion_category`, `exclusion_detail`, `quality_flag`, `dislocation_flag`, `last_reviewed` |
| **enums** | `inclusion_state: INCLUDED / EXCLUDED / PENDING_REVIEW / DATA_LIMITED` |
| | `exclusion_category: NON_OPERATING / SHELL / DUPLICATE / UNRESOLVED_IDENTITY / NO_FINANCIAL_HISTORY / OTHER_APPROVED` |
| **IDs / foreign keys** | `entity_id → SM-01.entity_id` |
| **PIT fields** | `as_of_date`, `last_reviewed` |
| **provenance fields** | `reviewer`, `rule_version`, `data_version` |
| **validation_rules** | Every exclusion must have a documented reason. No silent omissions. |
| **immutability_rules** | Inclusion state changes are append-only (new version per change). |
| **revision_rules** | Re-review creates new version. |
| **failure_semantics** | Entity cannot be resolved → `EXCLUDED` with `UNRESOLVED_IDENTITY` reason. |
| **canonical_boundary** | Canonical. |

### A-3: SignalRecord

| Field | Value |
|-------|-------|
| **schema_id** | SR-01 |
| **purpose** | All detected anomalies/dislocations/quality signals with full provenance. |
| **authority_source** | M3-02 §2 (Registry 3: SIGNAL_REGISTRY), M3-02 §7 (Data Architecture) |
| **owner** | Signal Detection Layer |
| **required_fields** | `signal_id`, `entity_id`, `signal_type`, `signal_family`, `detection_timestamp`, `entry_route` |
| **optional_fields** | `signal_value`, `signal_threshold`, `signal_evidence`, `signal_description`, `data_version`, `rule_version`, `model_version` |
| **enums** | `signal_type: QUALITY / DISLOCATION / EXTERNAL / FOUNDER_DIRECTED` |
| | `signal_family: PRICE_DISLOCATION / MULTIPLE_COMPRESSION / EARNINGS_REVISION / REVENUE_DETERIORATION / MARGIN_ANOMALY / WORKING_CAPITAL / GOVERNANCE / REGULATORY / INDUSTRY_SHOCK / COMPETITOR_DIVERGENCE / NARRATIVE_GAP / EXTERNAL` |
| | `entry_route: QUALITY_FIRST / DISLOCATION_FIRST / EXTERNAL / FOUNDER_DIRECTED` |
| **IDs / foreign keys** | `signal_id: UUID v7`, `entity_id → SM-01.entity_id` |
| **PIT fields** | `detection_timestamp`, `as_of_date` |
| **provenance fields** | `detector`, `data_version`, `rule_version`, `model_version`, `source` |
| **validation_rules** | Signal is append-only. Never deleted. New signal supersedes old. |
| **immutability_rules** | Signal content immutable after creation. |
| **revision_rules** | N/A (append-only). |
| **failure_semantics** | Successful scan with no material signal → `NO_SIGNAL`. Technical/data/detector failure → `DETECTION_ERROR` (candidate retryable; never silent Type-B miss). |
| **canonical_boundary** | Canonical. |

### A-4: CandidateRecord

| Field | Value |
|-------|-------|
| **schema_id** | CR-01 |
| **purpose** | Companies that passed signal assembly into candidates. Tracks selection state. |
| **authority_source** | M3-02 §2 (Registry 4: CANDIDATE_REGISTRY), M3-02 §4 (Selection States), M3-02 §5 (Candidate Assembly) |
| **owner** | Candidate Assembly |
| **required_fields** | `candidate_id`, `entity_id`, `signal_ids[]`, `selection_state`, `entry_route`, `entry_timestamp`, `evidence_freshness` |
| **optional_fields** | `quality_flag`, `dislocation_flag`, `watch_price`, `watch_conditions`, `rejection_reason` |
| **enums** | `selection_state: AUTO_RESEARCH_NOW / WATCH_PRICE / WATCH_EVIDENCE / DATA_LIMITED_WATCH / REJECT / SELECTION_ERROR` |
| | `entry_route: QUALITY_FIRST / DISLOCATION_FIRST / EXTERNAL / FOUNDER_DIRECTED` |
| **IDs / foreign keys** | `candidate_id: UUID v7`, `entity_id → SM-01.entity_id`, `signal_ids[] → SR-01.signal_id` |
| **PIT fields** | `entry_timestamp`, `last_evaluated` |
| **provenance fields** | `selector`, `policy_version`, `data_version` |
| **validation_rules** | Selection Engine failure must produce `SELECTION_ERROR`, never `REJECT` or `SKIP`. Founder-directed = `FOUNDER_DIRECTED` entry_route. Selection Engine must NOT score or rank candidates (M3 S1). |
| **immutability_rules** | Selection state transitions are append-only. |
| **revision_rules** | Re-evaluation creates new state version. |
| **failure_semantics** | Selection Engine failure → `SELECTION_ERROR` (candidate remains pending/retryable). Technical failure never silently produces REJECT/SKIP. |
| **canonical_boundary** | Canonical. |

### A-5: QualityUniverseRecord

| Field | Value |
|-------|-------|
| **schema_id** | QU-01 |
| **purpose** | Companies with accumulated evidence of high quality. Membership does NOT require dislocation. |
| **authority_source** | M3-02 §2 (Registry 5: QUALITY_UNIVERSE), DNA-017, M3-06 §2.5 (Quality States) |
| **owner** | Quality Discovery |
| **required_fields** | `entity_id`, `quality_state`, `assessment_date`, `evidence_ids[]` |
| **optional_fields** | `moat_types[]`, `moat_width`, `moat_depth`, `moat_trend`, `moat_durability` |
| **enums** | `quality_state: VERIFIED / PROBABLE / UNRESOLVED / FAILED` |
| **IDs / foreign keys** | `entity_id → SM-01.entity_id`, `evidence_ids[] → EV-01.evidence_id` |
| **PIT fields** | `assessment_date`, `as_of_date` |
| **provenance fields** | `assessor`, `rule_version`, `data_version` |
| **validation_rules** | Quality membership does NOT require dislocation. False-Quality Test must be documented. |
| **immutability_rules** | State transitions preserve history. |
| **revision_rules** | Quality refresh creates new version. |
| **failure_semantics** | UNRESOLVED with documented evidence gaps. |
| **canonical_boundary** | Canonical. |

### A-6: CaseRecord

| Field | Value |
|-------|-------|
| **schema_id** | CASE-01 |
| **purpose** | Companies that opened Full QAD Research. |
| **authority_source** | M3-01 §3 (State Ownership), M3-03 §3 (Stage 1: Case Open) |
| **owner** | Research Director (Role 1) |
| **required_fields** | `case_id`, `entity_id`, `candidate_id`, `as_of_date`, `case_state`, `research_director`, `opened_at` |
| **optional_fields** | `case_version`, `charter_id`, `budget_id`, `manifest_id`, `closed_at`, `closing_reason` |
| **enums** | `case_state: CASE_OPEN / CHARTER_APPROVED / SOURCE_FOUNDATION_COMPLETE / INITIAL_ANALYSIS_COMPLETE / DEEP_RESEARCH_COMPLETE / SCUTTLEBUTT_COMPLETE / EVIDENCE_CANONICAL / QUALITY_ANALYSIS_COMPLETE / ANALYTICAL_WORK_COMPLETE / IMPAIRMENT_DIAGNOSIS_COMPLETE / VALUATION_COMPLETE / RED_TEAM_COMPLETE / AUDIT_COMPLETE / UNDERWRITING_COMPLETE / FOUNDER_READY / FOUNDER_DECIDED / MONITORING / CLOSED` |
| **IDs / foreign keys** | `case_id: CASE-YYYY-NNN`, `entity_id → SM-01.entity_id`, `candidate_id → CR-01.candidate_id` |
| **PIT fields** | `as_of_date`, `opened_at`, `closed_at` |
| **provenance fields** | `research_director`, `opening_note` |
| **validation_rules** | Case cannot be opened without candidate in AUTO_RESEARCH_NOW state. New as-of → new case version. |
| **immutability_rules** | Case state transitions are append-only. Case locked during active research. |
| **revision_rules** | New as-of → new case version with superseded_by pointer. |
| **failure_semantics** | Budget exhausted → `INCOMPLETE` (not weakened quality gate). |
| **canonical_boundary** | Canonical. |

---

## B — Source & Evidence (10 schemas)

### B-1: SourceRecord

| Field | Value |
|-------|-------|
| **schema_id** | SRC-01 |
| **purpose** | Immutable source document reference. |
| **authority_source** | M3-04 §1 (L1-L10), M3-04 §2 (Layer 1: Raw Source Archive) |
| **owner** | Evidence Intelligence Lead (Role 2) |
| **required_fields** | `source_id`, `source_type`, `retrieval_date`, `url_or_identifier`, `content_hash`, `source_tier` |
| **optional_fields** | `title`, `author`, `publication_date`, `file_size`, `language`, `pages_referenced[]` |
| **enums** | `source_tier: L1 / L2 / L3 / L4 / L5 / L6 / L7 / L8 / L9 / L10` |
| | `source_type: SEC_FILING / TRANSCRIPT / PRESS_RELEASE / NEWS / ANALYST_REPORT / GOVERNMENT_DATA / INDUSTRY_REPORT / PATENT / SCIENTIFIC / SOCIAL_MEDIA / FORUM / INTERVIEW / CHANNEL_CHECK / OTHER` |
| **IDs / foreign keys** | `source_id: UUID v7` |
| **PIT fields** | `retrieval_date`, `publication_date` |
| **provenance fields** | `retriever`, `retrieval_method`, `source_url_hash` |
| **validation_rules** | Content hash must match file. L10 tagged as lead-only. |
| **immutability_rules** | Content never edited in place. Removal requires tombstone (EVIDENCE-DOCTRINE). |
| **revision_rules** | Re-retrieval creates new source version. |
| **failure_semantics** | Source unreachable → `SOURCE_UNAVAILABLE` with reason. Material source unreachable may force `INCOMPLETE`. |
| **canonical_boundary** | Canonical (Layer 1: Raw Source Archive). |

### B-2: EvidenceRecord

| Field | Value |
|-------|-------|
| **schema_id** | EV-01 |
| **purpose** | Canonical evidence object. Curated, validated entry admitted from raw sources. |
| **authority_source** | M3-04 §2 (Layer 2: Canonical Evidence Registry), M3-04 §3 (Evidence Object Taxonomy) |
| **owner** | Evidence Intelligence Lead (Role 2) |
| **required_fields** | `evidence_id`, `source_id`, `evidence_type`, `content`, `extractor`, `validation_status`, `as_of`, `admitting_role`, `source_tier` |
| **optional_fields** | `contradicts_ids[]`, `superseded_by_id`, `confidence`, `context`, `extraction_method` |
| **enums** | `evidence_type: FACT / CLAIM / INFERENCE / HYPOTHESIS` |
| | `validation_status: RAW / VALIDATED / CONTRADICTED / SUPERSEDED / RETRACTED / DISPUTED` |
| **IDs / foreign keys** | `evidence_id: UUID v7`, `source_id → SRC-01.source_id`, `contradicts_ids[] → EV-01.evidence_id` |
| **PIT fields** | `as_of`, `validation_timestamp` |
| **provenance fields** | `extractor`, `admitting_role`, `validation_method`, `source_version` |
| **validation_rules** | NotebookLM/Deep Research output must be validated against original source before admission. L10 cannot be sole support for material conclusion. |
| **immutability_rules** | Evidence content immutable after admission. Status changes are append-only. |
| **revision_rules** | Superseded evidence points to successor. |
| **failure_semantics** | Admission validation fails → evidence quarantined with reason. |
| **canonical_boundary** | Canonical (Layer 2). NotebookLM/DR output is NONCANONICAL until validated. |

### B-3: FactRecord

| Field | Value |
|-------|-------|
| **schema_id** | FACT-01 |
| **purpose** | Verifiable, objective piece of information directly from a source. |
| **authority_source** | M3-04 §3 (FACT) |
| **owner** | Evidence Intelligence Lead (Role 2) |
| **required_fields** | `fact_id`, `evidence_id`, `source_location`, `statement`, `verification_status` |
| **optional_fields** | `numerical_value`, `unit`, `precision`, `page_number`, `paragraph` |
| **enums** | `verification_status: VERIFIED / UNVERIFIED / DISPUTED` |
| **IDs / foreign keys** | `fact_id: UUID v7`, `evidence_id → EV-01.evidence_id` |
| **PIT fields** | `as_of` |
| **provenance fields** | `extractor`, `source_location` |
| **validation_rules** | Must be traceable to original source at exact location. |
| **immutability_rules** | Fact content immutable. |
| **revision_rules** | Correction creates new fact with superseded_by pointer. |
| **failure_semantics** | Cannot verify → `UNVERIFIED` status. |
| **canonical_boundary** | Canonical. |

### B-4: ClaimRecord

| Field | Value |
|-------|-------|
| **schema_id** | CLM-01 |
| **purpose** | Assertion by an entity (company, management, analyst, regulator) that may be true or false. |
| **authority_source** | M3-04 §3 (CLAIM) |
| **owner** | Evidence Intelligence Lead (Role 2) |
| **required_fields** | `claim_id`, `evidence_id`, `claimant`, `statement`, `claim_date` |
| **optional_fields** | `outcome`, `outcome_date`, `variance`, `resolution` |
| **enums** | `claimant_type: MANAGEMENT / ANALYST / REGULATOR / CUSTOMER / COMPETITOR / OTHER` |
| **IDs / foreign keys** | `claim_id: UUID v7`, `evidence_id → EV-01.evidence_id` |
| **PIT fields** | `claim_date`, `outcome_date` |
| **provenance fields** | `extractor`, `source` |
| **validation_rules** | Source must be identified. Truth not asserted by system. |
| **immutability_rules** | Claim content immutable. |
| **revision_rules** | Outcome updates create new version. |
| **failure_semantics** | N/A (claim is recorded regardless of truth). |
| **canonical_boundary** | Canonical. |

### B-5: InferenceRecord

| Field | Value |
|-------|-------|
| **schema_id** | INF-01 |
| **purpose** | Conclusion drawn from facts/claims by analyst or AI, labeled with confidence. |
| **authority_source** | M3-04 §3 (INFERENCE) |
| **owner** | Core Desk Researcher (Role 3) |
| **required_fields** | `inference_id`, `evidence_ids[]`, `conclusion`, `confidence`, `inference_chain`, `inferrer` |
| **optional_fields** | `alternative_conclusions[]`, `supporting_evidence[]`, `contradicting_evidence[]` |
| **enums** | `confidence: HIGH / MEDIUM / LOW / SPECULATIVE` |
| **IDs / foreign keys** | `inference_id: UUID v7`, `evidence_ids[] → EV-01.evidence_id` |
| **PIT fields** | `inference_timestamp`, `as_of` |
| **provenance fields** | `inferrer`, `inference_method` |
| **validation_rules** | Must be labeled as inference. Chain of reasoning must be explicit. |
| **immutability_rules** | Inference immutable. Alternative inferences preserved. |
| **revision_rules** | New evidence → new inference version. |
| **failure_semantics** | Confidence below threshold → flagged as SPECULATIVE. |
| **canonical_boundary** | Canonical. |

### B-6: HypothesisRecord

| Field | Value |
|-------|-------|
| **schema_id** | HYP-01 |
| **purpose** | Testable proposition about the entity, subject to falsification. |
| **authority_source** | M3-04 §3 (HYPOTHESIS), M3-03 §2 (H1–H5) |
| **owner** | Research Director (Role 1) |
| **required_fields** | `hypothesis_id`, `case_id`, `hypothesis_label`, `statement`, `falsification_criteria`, `initial_plausibility`, `originator` |
| **optional_fields** | `current_plausibility`, `evidence_for[]`, `evidence_against[]`, `status_history[]` |
| **enums** | `hypothesis_label: H1 / H2 / H3 / H4 / H5` |
| | `plausibility: PLAUSIBLE / IMPLAUSIBLE / UNCLEAR` |
| **IDs / foreign keys** | `hypothesis_id: UUID v7`, `case_id → CASE-01.case_id` |
| **PIT fields** | `created_at`, `last_updated` |
| **provenance fields** | `originator`, `research_charter` |
| **validation_rules** | Every case MUST have H1–H5. Falsification criteria must be specific. |
| **immutability_rules** | Hypothesis statement immutable. Plausibility updates preserve history. |
| **revision_rules** | Plausibility shift recorded with timestamp and trigger. |
| **failure_semantics** | Cannot determine plausibility → UNCLEAR. |
| **canonical_boundary** | Canonical. |

### B-7: ContradictionRecord

| Field | Value |
|-------|-------|
| **schema_id** | CTR-01 |
| **purpose** | Record of contradictory evidence. Both sides preserved. |
| **authority_source** | M3-04 §6 (Contradiction Management), EVIDENCE-DOCTRINE |
| **owner** | Evidence Intelligence Lead (Role 2) |
| **required_fields** | `contradiction_id`, `evidence_ids[]`, `contradiction_type`, `resolution_status`, `discovered_by` |
| **optional_fields** | `resolution_evidence_id`, `resolution_timestamp`, `notes` |
| **enums** | `contradiction_type: DIRECT / CIRCUMSTANTIAL / NUMERICAL / TEMPORAL` |
| | `resolution_status: UNRESOLVED / PARTIALLY_RESOLVED / RESOLVED_WITH_EVIDENCE` |
| **IDs / foreign keys** | `contradiction_id: UUID v7`, `evidence_ids[] → EV-01.evidence_id` |
| **PIT fields** | `discovered_at`, `resolution_timestamp` |
| **provenance fields** | `discovered_by`, `resolver` |
| **validation_rules** | Contradicting evidence cannot be silently deleted or averaged away. |
| **immutability_rules** | Contradiction record immutable. Resolution status updates preserve history. |
| **revision_rules** | Resolution creates new version. |
| **failure_semantics** | UNRESOLVED contradiction flagged for Chief Underwriter. |
| **canonical_boundary** | Canonical. |

### B-8: EvidenceGap

| Field | Value |
|-------|-------|
| **schema_id** | EG-01 |
| **purpose** | Structured record of an unresolved question requiring evidence. |
| **authority_source** | M3-03 §3 (Stage 4: Evidence Gap Map), M3-05 §3 (Investigation Charter) |
| **owner** | Research Director (Role 1) |
| **required_fields** | `gap_id`, `case_id`, `question`, `importance`, `operational_status`, `resolvability_class`, `created_by` |
| **optional_fields** | `investigator_charter_id`, `resolution_evidence_id`, `resolved_at`, `falsifiable_question` |
| **enums** | `operational_status: OPEN / IN_PROGRESS / PARTIALLY_CLOSED / CLOSED / DEFERRED / UNRESOLVED`
| | `importance: CRITICAL / HIGH / MEDIUM / LOW`
| | `resolvability_class: RESOLVABLE_WITH_EXISTING_SOURCES / RESOLVABLE_WITH_SCUTTLEBUTT / CURRENTLY_UNRESOLVABLE` |
| **IDs / foreign keys** | `gap_id: UUID v7`, `case_id → CASE-01.case_id` |
| **PIT fields** | `created_at`, `resolved_at` |
| **provenance fields** | `created_by`, `resolver` |
| **validation_rules** | Each gap must be falsifiable. Vague "need more research" is insufficient. |
| **immutability_rules** | Gap content immutable. |
| **revision_rules** | Status updates create new version. |
| **failure_semantics** | Budget exhausted → `DEFERRED` with reason. |
| **canonical_boundary** | Canonical. |

### B-9: EvidenceAdmissionRecord

| Field | Value |
|-------|-------|
| **schema_id** | EAR-01 |
| **purpose** | Audit trail for every evidence admission to canonical registry. |
| **authority_source** | M3-04 §2 (Layer 2), M3-09 §3 (Audit Checklist) |
| **owner** | Evidence Intelligence Lead (Role 2) |
| **required_fields** | `admission_id`, `evidence_id`, `admitting_role`, `admission_timestamp`, `validation_method`, `source_tier_check` |
| **optional_fields** | `validation_notes`, `original_source_verified`, `pit_verified`, `contradiction_check` |
| **enums** | `admission_method: DIRECT_SOURCE / AI_EXTRACTION / AI_SYNTHESIS / HUMAN_ANALYSIS / SCUTTLEBUTT` |
| **IDs / foreign keys** | `admission_id: UUID v7`, `evidence_id → EV-01.evidence_id` |
| **PIT fields** | `admission_timestamp`, `source_as_of` |
| **provenance fields** | `admitting_role`, `validation_method` |
| **validation_rules** | AI/NotebookLM synthesis must be validated against original source. L10 cannot be admitted as sole material support. |
| **immutability_rules** | Admission record immutable. |
| **revision_rules** | N/A. |
| **failure_semantics** | Validation fails → evidence quarantined. |
| **canonical_boundary** | Canonical (audit layer). |

### B-10: SourceVersion

| Field | Value |
|-------|-------|
| **schema_id** | SRCV-01 |
| **purpose** | Versioned record of source document changes/re-retrievals. |
| **authority_source** | M3-04 §2 (Layer 1: Raw Source Archive), M3-04 §5 (Source Archive retention) |
| **owner** | Evidence Intelligence Lead (Role 2) |
| **required_fields** | `version_id`, `source_id`, `version_number`, `retrieval_date`, `content_hash` |
| **optional_fields** | `previous_version_id`, `change_reason`, `file_size`, `format` |
| **enums** | `change_reason: INITIAL_RETRIEVAL / RE_RETRIEVAL / CORRECTION / REMOVAL_TOMBSTONE` |
| **IDs / foreign keys** | `version_id: UUID v7`, `source_id → SRC-01.source_id` |
| **PIT fields** | `retrieval_date` |
| **provenance fields** | `retriever`, `retrieval_method` |
| **validation_rules** | Re-retrieval creates new version. Tombstone records removal reason and authorizer. |
| **immutability_rules** | Version record immutable. |
| **revision_rules** | N/A (append-only versions). |
| **failure_semantics** | Source cannot be re-retrieved → previous version retained with note. |
| **canonical_boundary** | Canonical. |

---

## C — Research Governance (8 schemas)

### C-1: ResearchCharter

| Field | Value |
|-------|-------|
| **schema_id** | RC-01 |
| **purpose** | Binding research contract for a case. |
| **authority_source** | M3-03 §3 (Stage 2: Research Charter), M3-09 §4 (Research Charter governance) |
| **owner** | Research Director (Role 1) |
| **required_fields** | `charter_id`, `case_id`, `hypothesis_ids[]`, `key_questions[]`, `evidence_scope`, `budget_estimate`, `director`, `evidence_lead_validation` |
| **optional_fields** | `timeline`, `budget_approved`, `budget_controller`, `source_plan`, `material_blind_spots[]` |
| **enums** | `charter_state: DRAFT / VALIDATED / BUDGET_APPROVED / ACTIVE / COMPLETED` |
| **IDs / foreign keys** | `charter_id: UUID v7`, `case_id → CASE-01.case_id`, `hypothesis_ids[] → HYP-01.hypothesis_id` |
| **PIT fields** | `created_at`, `approved_at` |
| **provenance fields** | `director`, `evidence_lead`, `budget_controller` |
| **validation_rules** | Charter must contain H1–H5. Evidence Lead validates evidence scope completeness. Budget Controller authorizes budget. Chief Underwriter does NOT approve Charter. |
| **immutability_rules** | Charter immutable after BUDGET_APPROVED. |
| **revision_rules** | Material scope change → new charter version. |
| **failure_semantics** | Budget not approved → charter cannot proceed. |
| **canonical_boundary** | Canonical. |

### C-2: ResearchStageRecord

| Field | Value |
|-------|-------|
| **schema_id** | RSR-01 |
| **purpose** | Per-stage execution record within a research case. |
| **authority_source** | M3-03 §3 (Stages 1-18), M3-03 §4 (Stage State Lifecycle) |
| **owner** | Research Director (Role 1) |
| **required_fields** | `stage_id`, `case_id`, `stage_name`, `stage_state`, `started_at`, `responsible_role` |
| **optional_fields** | `completed_at`, `checkpoint_ref`, `output_ids[]`, `issues[]`, `decisions[]`, `retry_count`, `failure_reason` |
| **enums** | `stage_name: CASE_OPEN / CHARTER / SOURCE_FOUNDATION / INITIAL_ANALYSIS / DEEP_RESEARCH / SCUTTLEBUTT / CANONICAL_ADMISSION / QUALITY_ANALYSIS / ANALYTICAL_WORK / IMPAIRMENT / VALUATION / RED_TEAM / AUDIT / UNDERWRITING / PUBLICATION / FOUNDER_REVIEW / MONITORING / KNOWLEDGE` |
| | `stage_state: NOT_STARTED / IN_PROGRESS / COMPLETE / FAILED / INCOMPLETE / SKIPPED` |
| **IDs / foreign keys** | `stage_id: UUID v7`, `case_id → CASE-01.case_id` |
| **PIT fields** | `started_at`, `completed_at` |
| **provenance fields** | `responsible_role`, `checkpoint_ref` |
| **validation_rules** | No stage may be skipped without documented reason. INCOMPLETE ≠ COMPLETE. |
| **immutability_rules** | Stage state transitions are append-only. |
| **revision_rules** | Restart from last checkpoint preserves previous output. |
| **failure_semantics** | Budget exhaustion → INCOMPLETE (not weakened quality). Max 3 retries → FAILED. |
| **canonical_boundary** | Canonical. |

### C-3: InvestigatorCharter

| Field | Value |
|-------|-------|
| **schema_id** | IC-01 |
| **purpose** | Charter for each scuttlebutt/elastic investigation. |
| **authority_source** | M3-05 §3 (Investigation Charter), M3-05 §4 (Investigation Protocol) |
| **owner** | Research Director (Role 1) |
| **required_fields** | `investigator_charter_id`, `gap_id`, `investigator_type`, `falsifiable_question`, `allowed_source_classes[]`, `stop_rule`, `budget` |
| **optional_fields** | `population_represented`, `sampling_limitations`, `time_window`, `geography`, `independence_check`, `expected_information_value`, `output_evidence_ids[]` |
| **enums** | `investigator_type: CUSTOMER / COMPETITOR / SUPPLIER / DISTRIBUTOR / EMPLOYEE / DIGITAL / REGULATORY / TECHNOLOGY / SCIENTIFIC / GEOGRAPHIC / INDUSTRY_SPECIALIST` |
| | `expected_information_value: PLAUSIBLE_HIGH / PLAUSIBLE_MEDIUM / PLAUSIBLE_LOW` |
| **IDs / foreign keys** | `investigator_charter_id: UUID v7`, `gap_id → EG-01.gap_id` |
| **PIT fields** | `created_at`, `completed_at` |
| **provenance fields** | `authorizing_role`, `budget_controller` |
| **validation_rules** | Must have specific falsifiable question. Stop rule must be defined. All sources must be lawful/public/non-MNPI. |
| **immutability_rules** | Charter immutable after approval. |
| **revision_rules** | Scope change requires new charter. |
| **failure_semantics** | Budget exhausted → `INCOMPLETE_BUDGET`. |
| **canonical_boundary** | Canonical. |

### C-4: ResearchBudgetRecord

| Field | Value |
|-------|-------|
| **schema_id** | RB-01 |
| **purpose** | Per-case budget allocation and spend tracking. |
| **authority_source** | M3-01 §9 (Budget Discipline), M3-03 §3 (Stage 2) |
| **owner** | Research Budget Controller (S2) |
| **required_fields** | `budget_id`, `case_id`, `allocated_amount`, `approved_by`, `policy_version` |
| **optional_fields** | `cumulative_spend`, `remaining_budget`, `spend_breakdown[]`, `budget_exhausted` |
| **enums** | `budget_state: APPROVED / ACTIVE / EXHAUSTED / CLOSED` |
| **IDs / foreign keys** | `budget_id: UUID v7`, `case_id → CASE-01.case_id` |
| **PIT fields** | `approved_at`, `last_updated` |
| **provenance fields** | `approved_by`, `policy_version` |
| **validation_rules** | Budget exhaustion → INCOMPLETE (not weakened quality). Budget cannot be self-authorized by Research Director. |
| **immutability_rules** | Spend records are append-only. |
| **revision_rules** | Budget increase requires Founder override. |
| **failure_semantics** | Budget exhausted → EXHAUSTED state. |
| **canonical_boundary** | Canonical. |

### C-5: ResearchFailureRecord

| Field | Value |
|-------|-------|
| **schema_id** | RFR-01 |
| **purpose** | Record of research failures, retries, and resolutions. |
| **authority_source** | M3-01 §7 (Reliability Contract), M3-03 §4 (Stage State Lifecycle) |
| **owner** | Research Director (Role 1) |
| **required_fields** | `failure_id`, `case_id`, `stage_name`, `failure_type`, `failure_reason`, `retry_count`, `resolution` |
| **optional_fields** | `error_details`, `recovery_action`, `escalated_to` |
| **enums** | `failure_type: DATA_UNAVAILABLE / BUDGET_EXHAUSTED / RETRY_LIMIT / MODEL_FAILURE / AUDITOR_BLOCK / PIT_VIOLATION / SELECTION_ERROR / EVALUATION_INCOMPLETE` |
| | `resolution: RESOLVED / ESCALATED / UNRESOLVED / WORKAROUND` |
| **IDs / foreign keys** | `failure_id: UUID v7`, `case_id → CASE-01.case_id` |
| **PIT fields** | `failure_timestamp`, `resolution_timestamp` |
| **provenance fields** | `recorder`, `escalation_target` |
| **validation_rules** | Failure must never silently become completeness. |
| **immutability_rules** | Failure record immutable. |
| **revision_rules** | Resolution updates create new version. |
| **failure_semantics** | N/A (this IS the failure record). |
| **canonical_boundary** | Canonical. |

### C-7: HypothesisSet

| Field | Value |
|-------|-------|
| **schema_id** | HS-01 |
| **purpose** | Complete set of H1–H5 competing hypotheses for a case. |
| **authority_source** | M3-03 §2 (H1–H5 mandatory), M3-03 §3 (Stage 2: Research Charter) |
| **owner** | Research Director (Role 1) |
| **required_fields** | `hypothesis_set_id`, `case_id`, `hypothesis_ids[]`, `charter_id` |
| **optional_fields** | `dominant_hypothesis`, `shift_history[]` |
| **enums** | N/A |
| **IDs / foreign keys** | `hypothesis_set_id: UUID v7`, `case_id → CASE-01.case_id`, `hypothesis_ids[] → HYP-01.hypothesis_id` |
| **PIT fields** | `created_at`, `last_shift_at` |
| **provenance fields** | `creator` |
| **validation_rules** | Must contain exactly H1–H5. If any hypothesis absent, research cannot proceed. |
| **immutability_rules** | Set immutable after Charter approval. Hypothesis shifts recorded in shift_history. |
| **revision_rules** | New evidence → new hypothesis set version. |
| **failure_semantics** | Incomplete set → Charter cannot be approved. |
| **canonical_boundary** | Canonical. |

### C-8: InvestigationReport

| Field | Value |
|-------|-------|
| **schema_id** | IR-01 |
| **purpose** | Output of Role 14 (Elastic Investigator) — scuttlebutt investigation report. |
| **authority_source** | M3-03 Stage 6 (Scuttlebutt), M3-05 §4 (Investigation Protocol), M3-ROLES Role 14 |
| **owner** | Elastic Investigator (Role 14) |
| **required_fields** | `investigation_id`, `investigator_charter_id`, `evidence_gap_id`, `falsifiable_question`, `findings[]`, `disposition`, `investigator` |
| **optional_fields** | `sources[]`, `sampling_limitations`, `proposed_evidence_ids[]`, `stop_rule_triggered`, `completed_at` |
| **enums** | `disposition: ANSWERED / NOT_ANSWERED / PARTIALLY_ANSWERED` |
| | `stop_rule: EVIDENCE_SUFFICIENT / BUDGET_EXHAUSTED / COUNTER_EVIDENCE_FOUND / TIME_EXPIRED` |
| **IDs / foreign keys** | `investigation_id: UUID v7`, `investigator_charter_id → IC-01.investigator_charter_id`, `evidence_gap_id → EG-01.gap_id` |
| **PIT fields** | `started_at`, `completed_at` |
| **provenance fields** | `investigator`, `charter_version` |
| **validation_rules** | Investigation must have approved charter before start. All sources must be lawful/public/non-MNPI. |
| **immutability_rules** | Report immutable after submission. |
| **revision_rules** | N/A (new investigation for new evidence). |
| **failure_semantics** | Budget exhausted → `INCOMPLETE_BUDGET` disposition. |
| **canonical_boundary** | Canonical. Proposed evidence noncanonical until admitted. |

### C-6: ResearchStopRecord

| Field | Value |
|-------|-------|
| **schema_id** | RSR-02 |
| **purpose** | Record of research stop decisions and justifications. |
| **authority_source** | M3-01 §3 (Stop Conditions), M3-03 §3 (Stage quality gates) |
| **owner** | Research Director (Role 1) |
| **required_fields** | `stop_id`, `case_id`, `stage_name`, `stop_reason`, `authorized_by` |
| **optional_fields** | `evidence_trigger`, `alternative_path`, `resume_condition` |
| **enums** | `stop_reason: HYPOTHESIS_FALSIFIED / BUDGET_EXHAUSTED / DATA_INSUFFICIENT / FOUNDER_DIRECTED / AUDITOR_BLOCKED / THESIS_KILLER_TRIGGERED` |
| **IDs / foreign keys** | `stop_id: UUID v7`, `case_id → CASE-01.case_id` |
| **PIT fields** | `stop_timestamp` |
| **provenance fields** | `authorized_by` |
| **validation_rules** | Founder-only skip of Red Team/Audit must be documented. |
| **immutability_rules** | Stop record immutable. |
| **revision_rules** | Resume creates new record. |
| **failure_semantics** | N/A. |
| **canonical_boundary** | Canonical. |

---

## D — Business / Industry / Management (7 schemas)

### D-1: QualityAssessment

| Field | Value |
|-------|-------|
| **schema_id** | QA-01 |
| **purpose** | Quality state assignment for a case. |
| **authority_source** | M3-06 §2.5 (Quality Verification States), M3-06 §2.6 (False-Quality Test) |
| **owner** | Business & Industry Analyst (Role 4) |
| **required_fields** | `assessment_id`, `case_id`, `quality_state`, `false_quality_test_completed`, `evidence_ids[]`, `assessor` |
| **optional_fields** | `moat_assessment_id`, `industry_economics_id`, `notes` |
| **enums** | `quality_state: VERIFIED / PROBABLE / UNRESOLVED / FAILED` |
| **IDs / foreign keys** | `assessment_id: UUID v7`, `case_id → CASE-01.case_id`, `evidence_ids[] → EV-01.evidence_id` |
| **PIT fields** | `assessment_date`, `as_of` |
| **provenance fields** | `assessor`, `method_version` |
| **validation_rules** | False-Quality Test must be completed and documented. |
| **immutability_rules** | Assessment immutable after approval. |
| **revision_rules** | New evidence → new assessment version. |
| **failure_semantics** | UNRESOLVED with documented evidence gaps. |
| **canonical_boundary** | Canonical. |

### D-2: MoatAssessment

| Field | Value |
|-------|-------|
| **schema_id** | MA-01 |
| **purpose** | Moat analysis per FD #61 taxonomy. |
| **authority_source** | M3-06 §2.3 (Moat Analysis — FD #61), M3-06 §2.4 (Moat Dimensions) |
| **owner** | Business & Industry Analyst (Role 4) |
| **required_fields** | `moat_assessment_id`, `case_id`, `moat_types[]`, `moat_width`, `moat_depth`, `moat_trend`, `moat_durability`, `evidence_ids[]` |
| **optional_fields** | `mechanism_evidence{type: evidence[]}`, `false_quality_concerns[]` |
| **enums** | `moat_type: SHARE_OF_MIND / NETWORK_EFFECT / HIGH_SWITCHING_COST / COST_ADVANTAGE / INTANGIBLE_ASSETS / EFFICIENT_SCALE` |
| | `moat_width: NARROW / MODERATE / WIDE` |
| | `moat_depth: SHALLOW / MODERATE / DEEP` |
| | `moat_trend: STRENGTHENING / STABLE / WEAKENING / AT_RISK` |
| | `moat_durability: YEARS / DECADE_PLUS / UNCERTAIN` |
| **IDs / foreign keys** | `moat_assessment_id: UUID v7`, `case_id → CASE-01.case_id` |
| **PIT fields** | `assessment_date` |
| **provenance fields** | `assessor` |
| **validation_rules** | Moat TYPE must be one of the 6 canonical types. Mechanism/evidence tests are separate from moat type. |
| **immutability_rules** | Assessment immutable. |
| **revision_rules** | New evidence → new version. |
| **failure_semantics** | Moat unclear → type set to empty with evidence gaps documented. |
| **canonical_boundary** | Canonical. |

### D-3: IndustryEconomicsRecord

| Field | Value |
|-------|-------|
| **schema_id** | IE-01 |
| **purpose** | Industry structure analysis. |
| **authority_source** | M3-06 §3 (Industry Economics Framework) |
| **owner** | Business & Industry Analyst (Role 4) |
| **required_fields** | `industry_economics_id`, `case_id`, `demand_driver`, `supply_structure`, `capacity_utilization`, `pricing_dynamics`, `evidence_ids[]` |
| **optional_fields** | `margins_normal`, `roic_industry`, `capital_entry_barriers`, `future_capacity_pipeline`, `porter_forces{}` |
| **IDs / foreign keys** | `industry_economics_id: UUID v7`, `case_id → CASE-01.case_id` |
| **PIT fields** | `assessment_date` |
| **provenance fields** | `assessor` |
| **validation_rules** | Industry analysis must use Demand→Supply→Capacity→Utilization→Pricing→Margins→ROIC→Entry/Exit chain. |
| **immutability_rules** | Assessment immutable. |
| **revision_rules** | New data → new version. |
| **failure_semantics** | Industry data insufficient → documented gap. |
| **canonical_boundary** | Canonical. |

### D-4: ManagementClaim

| Field | Value |
|-------|-------|
| **schema_id** | MC-01 |
| **purpose** | Management public statement tracked against outcome. |
| **authority_source** | M3-06 §4.1 (Management Claim Ledger) |
| **owner** | Financial & Management Analyst (Role 5) |
| **required_fields** | `claim_id`, `case_id`, `statement`, `claim_date`, `claimant`, `source_id` |
| **optional_fields** | `outcome`, `outcome_date`, `variance`, `variance_explanation` |
| **IDs / foreign keys** | `claim_id: UUID v7`, `case_id → CASE-01.case_id`, `source_id → SRC-01.source_id` |
| **PIT fields** | `claim_date`, `outcome_date` |
| **provenance fields** | `extractor`, `source` |
| **validation_rules** | Every material forward-looking statement tracked. Variance explained or flagged. |
| **immutability_rules** | Claim immutable. |
| **revision_rules** | Outcome update creates new version. |
| **failure_semantics** | N/A. |
| **canonical_boundary** | Canonical. |

### D-5: CapitalAllocationEvent

| Field | Value |
|-------|-------|
| **schema_id** | CAE-01 |
| **purpose** | Major capital allocation decision. |
| **authority_source** | M3-06 §4.2 (Capital Allocation Ledger) |
| **owner** | Financial & Management Analyst (Role 5) |
| **required_fields** | `event_id`, `case_id`, `decision_type`, `amount`, `decision_date`, `outcome`, `evidence_ids[]` |
| **optional_fields** | `per_share_impact`, `rationale`, `source_id` |
| **enums** | `decision_type: ACQUISITION / BUYBACK / DIVIDEND / DEBT_ISSUANCE / EQUITY_ISSUANCE / CAPEX / R&D / DIVESTITURE / OTHER` |
| **IDs / foreign keys** | `event_id: UUID v7`, `case_id → CASE-01.case_id` |
| **PIT fields** | `decision_date`, `outcome_date` |
| **provenance fields** | `extractor`, `source` |
| **validation_rules** | Prefer 10-15 years of data. |
| **immutability_rules** | Event immutable. |
| **revision_rules** | Outcome update creates new version. |
| **failure_semantics** | Data unavailable → documented gap. |
| **canonical_boundary** | Canonical. |

### D-6: ManagementDecisionLedger

| Field | Value |
|-------|-------|
| **schema_id** | MDL-01 |
| **purpose** | Aggregate management assessment based on decision history. |
| **authority_source** | M3-06 §4 (Management Assessment Framework) |
| **owner** | Financial & Management Analyst (Role 5) |
| **required_fields** | `ledger_id`, `case_id`, `management_quality`, `capital_allocation_quality`, `promise_ratio`, `evidence_ids[]` |
| **optional_fields** | `incentive_alignment`, `per_share_trend`, `ma_history_summary`, `concerns[]` |
| **enums** | `management_quality: STRONG / ADEQUATE / WEAK / UNPROVEN` |
| | `capital_allocation_quality: VALUE_CREATING / NEUTRAL / VALUE_DESTROYING / UNCLEAR` |
| **IDs / foreign keys** | `ledger_id: UUID v7`, `case_id → CASE-01.case_id` |
| **PIT fields** | `assessment_date` |
| **provenance fields** | `assessor` |
| **validation_rules** | Assessment based on decisions, not charisma. 10-15 year track record preferred. |
| **immutability_rules** | Assessment immutable. |
| **revision_rules** | New evidence → new version. |
| **failure_semantics** | Insufficient data → UNPROVEN management quality. |
| **canonical_boundary** | Canonical. |

---

### D-7: ManagementOutcome

| Field | Value |
|-------|-------|
| **schema_id** | MO-02 |
| **purpose** | Measured outcome of a management decision or claim. |
| **authority_source** | M3-06 §4.1 (Management Claim Ledger), M3-06 §4.4 (Promise vs Outcome) |
| **owner** | Financial & Management Analyst (Role 5) |
| **required_fields** | `outcome_id`, `case_id`, `management_claim_id`, `measured_outcome`, `outcome_date`, `variance` |
| **optional_fields** | `variance_explanation`, `evidence_ids[]`, `is_resolved` |
| **enums** | `variance_type: MET / EXCEEDED / MISSED / UNCLEAR / PENDING` |
| **IDs / foreign keys** | `outcome_id: UUID v7`, `case_id → CASE-01.case_id`, `management_claim_id → MC-01.claim_id` |
| **PIT fields** | `outcome_date`, `assessment_date` |
| **provenance fields** | `assessor`, `evidence_ids[]` |
| **validation_rules** | Every material forward-looking statement must have tracked outcome. Variance explained or flagged. |
| **immutability_rules** | Outcome record immutable. |
| **revision_rules** | New data → new version. |
| **failure_semantics** | Outcome cannot be determined → variance = UNCLEAR. |
| **canonical_boundary** | Canonical. |

---

## E — Impairment & Recovery (6 schemas)

### E-1: DislocationRecord

| Field | Value |
|-------|-------|
| **schema_id** | DR-01 |
| **purpose** | Record of what broke and why. |
| **authority_source** | M3-07 §2 (Dislocation Reconstruction) |
| **owner** | Impairment Diagnosis Specialist (Role 6) |
| **required_fields** | `dislocation_id`, `case_id`, `broken_variables[]`, `root_cause`, `cause_classification`, `peer_test_result`, `moat_test_result` |
| **optional_fields** | `reversibility_assessment`, `balance_sheet_runway`, `external_evidence_ids[]`, `price_test_result`, `thesis_killers[]` |
| **enums** | `cause_classification: CYCLICAL / COMPETITIVE / TECHNOLOGICAL / REGULATORY / COMPANY_SPECIFIC / MACRO / MIXED` |
| | `broken_variable: REVENUE / VOLUME / PRICE / MIX / MARGIN / MARKET_SHARE / CHURN / ROIC / CASH_CONVERSION` |
| **IDs / foreign keys** | `dislocation_id: UUID v7`, `case_id → CASE-01.case_id` |
| **PIT fields** | `assessment_date` |
| **provenance fields** | `assessor` |
| **validation_rules** | Each broken variable must be specifically identified. Vague "macro headwinds" insufficient. |
| **immutability_rules** | Record immutable. |
| **revision_rules** | New evidence → new version. |
| **failure_semantics** | Cannot determine cause → `MIXED` classification. |
| **canonical_boundary** | Canonical. |

### E-2: ImpairmentAssessment

| Field | Value |
|-------|-------|
| **schema_id** | IA-01 |
| **purpose** | Impairment type diagnosis. |
| **authority_source** | M3-07 §3 (Impairment Diagnosis) |
| **owner** | Impairment Diagnosis Specialist (Role 6) |
| **required_fields** | `impairment_id`, `case_id`, `diagnosis`, `primary_diagnosis`, `strongest_competing_explanation`, `why_primary_dominates`, `weakest_link`, `flip_evidence`, `evidence_ids[]` |
| **optional_fields** | `competing_hypothesis_evidence[]`, `impairment_dimensions{}` |
| **enums** | `diagnosis: TEMPORARY / MOSTLY_TEMPORARY / MIXED / STRUCTURAL / UNRESOLVED` |
| **IDs / foreign keys** | `impairment_id: UUID v7`, `case_id → CASE-01.case_id` |
| **PIT fields** | `assessment_date` |
| **provenance fields** | `assessor` |
| **validation_rules** | Must include all 5 mandatory output fields. Flip evidence must be concrete and observable. |
| **immutability_rules** | Assessment immutable. |
| **revision_rules** | New evidence → new version. |
| **failure_semantics** | UNRESOLVED with documented evidence gaps. |
| **canonical_boundary** | Canonical. |

### E-3: CompetingExplanation

| Field | Value |
|-------|-------|
| **schema_id** | CE-01 |
| **purpose** | Strongest alternative explanation for impairment. |
| **authority_source** | M3-07 §3.2 (Mandatory Output) |
| **owner** | Impairment Diagnosis Specialist (Role 6) |
| **required_fields** | `explanation_id`, `impairment_id`, `alternative_diagnosis`, `supporting_evidence_ids[]`, `why_not_primary` |
| **optional_fields** | `evidence_that_would_change_priority[]` |
| **enums** | `alternative_diagnosis: TEMPORARY / MOSTLY_TEMPORARY / MIXED / STRUCTURAL / UNRESOLVED` |
| **IDs / foreign keys** | `explanation_id: UUID v7`, `impairment_id → IA-01.impairment_id` |
| **PIT fields** | `assessment_date` |
| **provenance fields** | `assessor` |
| **validation_rules** | Must be evidence-based, not hypothetical. |
| **immutability_rules** | Explanation immutable. |
| **revision_rules** | New evidence → new version. |
| **failure_semantics** | N/A. |
| **canonical_boundary** | Canonical. |

### E-4: RecoveryModel

| Field | Value |
|-------|-------|
| **schema_id** | RM-01 |
| **purpose** | Defined recovery path from dislocation. |
| **authority_source** | M3-07 §4 (Recovery Model) |
| **owner** | Impairment Diagnosis Specialist (Role 6) |
| **required_fields** | `recovery_id`, `case_id`, `cause`, `recovery_mechanism`, `leading_evidence`, `expected_sequence`, `time_horizon`, `invalidation` |
| **optional_fields** | `recovery_scenario`, `evidence_ids[]`, `thesis_killers[]` |
| **enums** | `recovery_scenario: V_SHAPED / U_SHAPED / L_SHAPED / W_SHAPED` |
| **IDs / foreign keys** | `recovery_id: UUID v7`, `case_id → CASE-01.case_id` |
| **PIT fields** | `assessment_date`, `time_horizon` |
| **provenance fields** | `assessor` |
| **validation_rules** | Recovery mechanism must be specific. "Historically great company, therefore will recover" is FORBIDDEN as causal reasoning. |
| **immutability_rules** | Model immutable. |
| **revision_rules** | New evidence → new version. |
| **failure_semantics** | Cannot define recovery → UNRESOLVED. |
| **canonical_boundary** | Canonical. |

### E-5: ThesisKiller

| Field | Value |
|-------|-------|
| **schema_id** | TK-01 |
| **purpose** | Specific, observable event that would invalidate the thesis. |
| **authority_source** | M3-07 §4.4 (Thesis Killers) |
| **owner** | Impairment Diagnosis Specialist (Role 6) |
| **required_fields** | `thesis_killer_id`, `case_id`, `condition`, `evidence_type`, `severity`, `trigger_status` |
| **optional_fields** | `trigger_timestamp`, `resolution`, `evidence_id` |
| **enums** | `severity: CRITICAL / HIGH / MEDIUM / LOW` |
| | `trigger_status: NOT_TRIGGERED / MONITORING / TRIGGERED / RESOLVED` |
| **IDs / foreign keys** | `thesis_killer_id: UUID v7`, `case_id → CASE-01.case_id` |
| **PIT fields** | `defined_at`, `trigger_timestamp` |
| **provenance fields** | `definer` |
| **validation_rules** | Must be specific and observable. Not vague risk factors. |
| **immutability_rules** | Killer definition immutable. |
| **revision_rules** | Trigger status updates append-only. |
| **failure_semantics** | TRIGGERED → escalated to Chief Underwriter. |
| **canonical_boundary** | Canonical. |

### E-6: FlipEvidence

| Field | Value |
|-------|-------|
| **schema_id** | FE-01 |
| **purpose** | Specific evidence that would change impairment diagnosis. |
| **authority_source** | M3-07 §3.2 (Flip Evidence) |
| **owner** | Impairment Diagnosis Specialist (Role 6) |
| **required_fields** | `flip_evidence_id`, `impairment_id`, `condition`, `would_flip_to`, `observability` |
| **optional_fields** | `evidence_source`, `timeframe`, `probability_if_observed` |
| **enums** | `would_flip_to: TEMPORARY / MOSTLY_TEMPORARY / MIXED / STRUCTURAL / UNRESOLVED` |
| **IDs / foreign keys** | `flip_evidence_id: UUID v7`, `impairment_id → IA-01.impairment_id` |
| **PIT fields** | `defined_at` |
| **provenance fields** | `definer` |
| **validation_rules** | Must be concrete and observable. Not theoretical. |
| **immutability_rules** | Definition immutable. |
| **revision_rules** | N/A. |
| **failure_semantics** | N/A. |
| **canonical_boundary** | Canonical. |

---

## F — Financial & Economic Underwriting (8 schemas)

### F-1: FinancialFact

| Field | Value |
|-------|-------|
| **schema_id** | FF-01 |
| **purpose** | Raw financial data point from source. |
| **authority_source** | M3-08 §2 (Financial Reconstruction) |
| **owner** | Financial & Management Analyst (Role 5) |
| **required_fields** | `financial_fact_id`, `case_id`, `metric_name`, `value`, `unit`, `period`, `fiscal_year`, `source_id` |
| **optional_fields** | `segment`, `currency`, `is_gaap`, `footnote`, `restatement_flag` |
| **enums** | `metric_family: REVENUE / COGS / SG&A / R&D / D&A / OPERATING_INCOME / NET_INCOME / EPS / FCF / CAPEX / WORKING_CAPITAL / DEBT / EQUITY / ROIC / MARGIN / SHARE_COUNT / OTHER` |
| **IDs / foreign keys** | `financial_fact_id: UUID v7`, `case_id → CASE-01.case_id`, `source_id → SRC-01.source_id` |
| **PIT fields** | `period`, `fiscal_year`, `as_of` |
| **provenance fields** | `extractor`, `source_location` |
| **validation_rules** | Every fact traceable to source at exact location. |
| **immutability_rules** | Fact immutable. Restatement creates new fact. |
| **revision_rules** | Restatement creates new version with superseded_by pointer. |
| **failure_semantics** | Fact cannot be verified → flagged. |
| **canonical_boundary** | Canonical. |

### F-2: NormalizedFinancialFact

| Field | Value |
|-------|-------|
| **schema_id** | NFF-01 |
| **purpose** | Adjusted/normalized financial data point. |
| **authority_source** | M3-08 §2.4 (Normalization Adjustments) |
| **owner** | Financial & Management Analyst (Role 5) |
| **required_fields** | `normalized_fact_id`, `financial_fact_id`, `adjusted_value`, `adjustment_type`, `adjustment_rationale`, `adjuster` |
| **optional_fields** | `adjustment_amount`, `is_permanent`, `source_id` |
| **enums** | `adjustment_type: NON_RECURRING / CYCLICAL / ACQUISITION_ACCOUNTING / PENSION / STOCK_COMPENSATION / DEFERRED_TAX / EXTRAORDINARY / OTHER` |
| | `is_permanent: PERMANENT / TEMPORARY / UNCERTAIN` |
| **IDs / foreign keys** | `normalized_fact_id: UUID v7`, `financial_fact_id → FF-01.financial_fact_id` |
| **PIT fields** | `adjustment_date` |
| **provenance fields** | `adjuster`, `methodology` |
| **validation_rules** | Every adjustment tagged with type and rationale. |
| **immutability_rules** | Adjustment immutable. |
| **revision_rules** | New methodology → new version. |
| **failure_semantics** | Cannot normalize → documented as UNCERTAIN. |
| **canonical_boundary** | Canonical. |

### F-3: CalculationRecord

| Field | Value |
|-------|-------|
| **schema_id** | CALC-01 |
| **purpose** | Derived calculation with full lineage. |
| **authority_source** | M3-08 §2.3 (Calculation Lineage), M3-08 §4 (Permanent Loss) |
| **owner** | Financial & Management Analyst (Role 5) |
| **required_fields** | `calculation_id`, `case_id`, `formula`, `inputs[]`, `result`, `calculated_by`, `timestamp` |
| **optional_fields** | `input_fact_ids[]`, `error_margin`, `notes` |
| **IDs / foreign keys** | `calculation_id: UUID v7`, `case_id → CASE-01.case_id` |
| **PIT fields** | `timestamp`, `as_of` |
| **provenance fields** | `calculated_by`, `formula_version`, `input_fact_ids[]` |
| **validation_rules** | Every calculation must have explicit formula, inputs, and result. Must be independently reproducible. |
| **immutability_rules** | Calculation record immutable. |
| **revision_rules** | Recalculation creates new version. |
| **failure_semantics** | Cannot reproduce → flagged for Auditor. |
| **canonical_boundary** | Canonical. |

### F-4: ScenarioRecord

| Field | Value |
|-------|-------|
| **schema_id** | SCEN-01 |
| **purpose** | Economic scenario assumption set. |
| **authority_source** | M3-08 §3 (Economic Scenarios) |
| **owner** | Valuation & Expectations Specialist (Role 7) |
| **required_fields** | `scenario_id`, `case_id`, `scenario_type`, `assumptions{}`, `intrinsic_value_estimate`, `creator` |
| **optional_fields** | `probability_weight`, `sensitivity_analysis{}`, `evidence_ids[]` |
| **enums** | `scenario_type: CURRENT / NO_RECOVERY / PARTIAL_RECOVERY / NORMALIZATION / QUALITY_COMPOUNDING` |
| **IDs / foreign keys** | `scenario_id: UUID v7`, `case_id → CASE-01.case_id` |
| **PIT fields** | `created_at`, `as_of` |
| **provenance fields** | `creator` |
| **validation_rules** | All 5 scenario types must be defined. Each scenario has explicit assumptions for revenue growth, margin, tax rate, CapEx, WC, ROIC, WACC, time horizon. |
| **immutability_rules** | Scenario record immutable. |
| **revision_rules** | New data → new version. |
| **failure_semantics** | Scenario cannot be defined → documented as not applicable. |
| **canonical_boundary** | Canonical. |

### F-5: PermanentLossAssessment

| Field | Value |
|-------|-------|
| **schema_id** | PLA-01 |
| **purpose** | Assessment of permanent economic loss under each scenario. |
| **authority_source** | M3-08 §4 (Permanent Loss Analysis) |
| **owner** | Valuation & Expectations Specialist (Role 7) |
| **required_fields** | `assessment_id`, `case_id`, `balance_sheet_runway`, `dilution_risk`, `asset_impairment_risk`, `covenant_risk`, `refinancing_risk`, `competitive_damage` |
| **optional_fields** | `permanent_loss_range{}`, `recovery_capital_needed`, `evidence_ids[]` |
| **enums** | `risk_level: NONE / LOW / MEDIUM / HIGH / CRITICAL` |
| **IDs / foreign keys** | `assessment_id: UUID v7`, `case_id → CASE-01.case_id` |
| **PIT fields** | `assessment_date` |
| **provenance fields** | `assessor` |
| **validation_rules** | Must include all 6 risk dimensions. |
| **immutability_rules** | Assessment immutable. |
| **revision_rules** | New data → new version. |
| **failure_semantics** | Cannot assess → documented as uncertain. |
| **canonical_boundary** | Canonical. |

### F-6: ReverseDCFRecord

| Field | Value |
|-------|-------|
| **schema_id** | RDCF-01 |
| **purpose** | Reverse DCF analysis — what growth does the market price imply? |
| **authority_source** | M3-08 §5.1 (Reverse DCF) |
| **owner** | Valuation & Expectations Specialist (Role 7) |
| **required_fields** | `r_dcf_id`, `case_id`, `current_price`, `implied_growth_rate`, `implied_terminal_value`, `scenario_comparison{}`, `analyst` |
| **optional_fields** | `years_of_no_recovery_priced_in`, `recovery_rate_implied`, `sensitivity_range{}` |
| **IDs / foreign keys** | `r_dcf_id: UUID v7`, `case_id → CASE-01.case_id` |
| **PIT fields** | `analysis_date`, `price_as_of` |
| **provenance fields** | `analyst`, `method_version` |
| **validation_rules** | Reverse DCF is mandatory for every case. Must compare implied growth to scenario assumptions. |
| **immutability_rules** | Record immutable. |
| **revision_rules** | Price change → new version. |
| **failure_semantics** | Cannot calculate → documented as not applicable. |
| **canonical_boundary** | Canonical. |

### F-7: ValuationAssessment

| Field | Value |
|-------|-------|
| **schema_id** | VA-01 |
| **purpose** | Overall valuation assessment — diagnostic tool, not fair-value number. |
| **authority_source** | M3-08 §5 (Valuation as Diagnostic Tool) |
| **owner** | Valuation & Expectations Specialist (Role 7) |
| **required_fields** | `valuation_id`, `case_id`, `scenario_values{}`, `economic_damage`, `price_damage`, `damage_gap`, `asymmetry_estimate`, `r_dcf_id`, `permanent_loss_id` |
| **optional_fields** | `valuation_range{}`, `thesis_killers_financial[]`, `evidence_ids[]` |
| **IDs / foreign keys** | `valuation_id: UUID v7`, `case_id → CASE-01.case_id`, `r_dcf_id → RDCF-01.r_dcf_id`, `permanent_loss_id → PLA-01.assessment_id` |
| **PIT fields** | `assessment_date`, `price_as_of` |
| **provenance fields** | `assessor` |
| **validation_rules** | No single fair-value number. Always a range or scenario. Valuation is diagnostic, not decorative. |
| **immutability_rules** | Assessment immutable. |
| **revision_rules** | New data → new version. |
| **failure_semantics** | Range too wide → documented as UNRESOLVED. |
| **canonical_boundary** | Canonical. |

---

### F-8: PriceImpliedExpectation

| Field | Value |
|-------|-------|
| **schema_id** | PIE-01 |
| **purpose** | What the current market price implies about future expectations. |
| **authority_source** | M3-08 §5.2 (Price-Implied Expectations) |
| **owner** | Valuation & Expectations Specialist (Role 7) |
| **required_fields** | `expectation_id`, `case_id`, `current_price`, `implied_growth_rate`, `implied_terminal_value`, `recovery_rate_implied`, `scenario_comparison{}` |
| **optional_fields** | `years_of_no_recovery_priced_in`, `implied_terminal_multiple`, `sensitivity_range{}` |
| **enums** | N/A |
| **IDs / foreign keys** | `expectation_id: UUID v7`, `case_id → CASE-01.case_id` |
| **PIT fields** | `analysis_date`, `price_as_of` |
| **provenance fields** | `analyst`, `method_version` |
| **validation_rules** | Must compare implied expectations to at least 3 scenario assumptions. |
| **immutability_rules** | Record immutable. |
| **revision_rules** | Price change → new version. |
| **failure_semantics** | Cannot calculate → documented. |
| **canonical_boundary** | Canonical. |

---

## G — Challenge / Underwriting / Publication (7 schemas)

### G-1: RedTeamChallenge

| Field | Value |
|-------|-------|
| **schema_id** | RTC-01 |
| **purpose** | Structural Red Team challenge output. |
| **authority_source** | M3-09 §2 (Structural Red Team) |
| **owner** | Structural Red Team (Role 9) |
| **required_fields** | `challenge_id`, `case_id`, `outcome`, `strongest_opposing_case`, `findings[]`, `risk_assessment`, `cost_of_being_wrong` |
| **optional_fields** | `quality_challenge`, `temporary_challenge`, `recovery_challenge`, `management_challenge`, `valuation_challenge`, `market_correctness_case`, `hidden_risks[]` |
| **enums** | `outcome: ACCEPTED / PARTIALLY_ACCEPTED / REJECTED_WITH_EVIDENCE / UNRESOLVED` |
| **IDs / foreign keys** | `challenge_id: UUID v7`, `case_id → CASE-01.case_id` |
| **PIT fields** | `challenge_date` |
| **provenance fields** | `reviewer` |
| **validation_rules** | Red Team must have NO prior involvement in case. Output preserved verbatim. |
| **immutability_rules** | Challenge output immutable. |
| **revision_rules** | N/A. |
| **failure_semantics** | UNRESOLVED outcome preserved. |
| **canonical_boundary** | Canonical. |

### G-2: AuditFinding

| Field | Value |
|-------|-------|
| **schema_id** | AF-01 |
| **purpose** | Individual audit finding. |
| **authority_source** | M3-09 §3 (Independent Audit) |
| **owner** | Independent Research Auditor (Role 10) |
| **required_fields** | `finding_id`, `audit_id`, `check_name`, `pass_fail`, `evidence`, `required_correction` |
| **optional_fields** | `severity`, `resolved`, `resolution_timestamp`, `resolver` |
| **enums** | `check_name: SOURCE_EXISTENCE / ORIGINAL_SOURCE_INSPECTION / CITATION_CORRECTNESS / PIT_INTEGRITY / CALCULATION_REPRODUCIBILITY / CONTRADICTION_PRESERVATION / MODEL_PROVENANCE / SELF_REVIEW_SEPARATION / PUBLICATION_GATES` |
| | `pass_fail: PASS / FAIL / NOT_APPLICABLE` |
| **IDs / foreign keys** | `finding_id: UUID v7`, `audit_id → AG-01.audit_id` |
| **PIT fields** | `check_timestamp` |
| **provenance fields** | `auditor` |
| **validation_rules** | Every audit check must be completed. |
| **immutability_rules** | Finding immutable. |
| **revision_rules** | Resolution creates new version. |
| **failure_semantics** | FAIL → case blocked. |
| **canonical_boundary** | Canonical. |

### G-3: AuditGate (AuditReport)

| Field | Value |
|-------|-------|
| **schema_id** | AG-01 |
| **purpose** | Complete audit report for a case. |
| **authority_source** | M3-09 §3 |
| **owner** | Independent Research Auditor (Role 10) |
| **required_fields** | `audit_id`, `case_id`, `outcome`, `findings[]`, `auditor`, `completed_at` |
| **optional_fields** | `blocker`, `notes` |
| **enums** | `outcome: PASS / PASS_WITH_FINDINGS / FAIL` |
| **IDs / foreign keys** | `audit_id: UUID v7`, `case_id → CASE-01.case_id`, `findings[] → AF-01.finding_id` |
| **PIT fields** | `completed_at` |
| **provenance fields** | `auditor` |
| **validation_rules** | Auditor may block FOUNDER_READY. Auditor does not decide thesis. |
| **immutability_rules** | Report immutable. |
| **revision_rules** | Re-audit creates new version. |
| **failure_semantics** | FAIL → case blocked. Cannot be overridden by Research Director. |
| **canonical_boundary** | Canonical. |

### G-4: UnderwritingVerdict

| Field | Value |
|-------|-------|
| **schema_id** | UV-01 |
| **purpose** | Final research verdict from Chief Underwriter. |
| **authority_source** | M3-09 §4 (Chief Underwriter) |
| **owner** | Chief Underwriter (Role 8) |
| **required_fields** | `verdict_id`, `case_id`, `verdict`, `synthesis_narrative`, `scenario_weights{}`, `key_uncertainties[]`, `monitoring_indicators[]`, `recommendation_to_founder`, `underwriter` |
| **optional_fields** | `red_team_challenge_id`, `audit_report_id`, `dissent_notes`, `additional_evidence_ids[]` |
| **enums** | `verdict: QAD_CONFIRMED / QAD_PROBABLE / QAD_UNRESOLVED / NOT_QAD_STRUCTURAL / NOT_QAD_QUALITY / NOT_QAD_VALUATION` |
| **IDs / foreign keys** | `verdict_id: UUID v7`, `case_id → CASE-01.case_id`, `red_team_challenge_id → RTC-01.challenge_id`, `audit_report_id → AG-01.audit_id` |
| **PIT fields** | `verdict_date` |
| **provenance fields** | `underwriter` |
| **validation_rules** | Chief Underwriter cannot select own cases. Verdict is advisory to Founder. Recommendation annotated as "advisory — does not equal endorsement." |
| **immutability_rules** | Verdict immutable. |
| **revision_rules** | New evidence → new verdict version. |
| **failure_semantics** | UNRESOLVED → escalated to Founder. |
| **canonical_boundary** | Canonical. Recommendation to Founder is advisory. |

### G-5: PublicationRecord

| Field | Value |
|-------|-------|
| **schema_id** | PUB-01 |
| **purpose** | Publication record for library article. |
| **authority_source** | M3-09 §5 (Publication) |
| **owner** | Thai Editor (Role 11) |
| **required_fields** | `publication_id`, `case_id`, `slug`, `title`, `category`, `published_date`, `publication_state`, `editor` |
| **optional_fields** | `companion_slug`, `body_thai`, `body_english`, `verdict_id`, `research_complete_date` |
| **enums** | `publication_state: RESEARCH_COMPLETE / FOUNDER_READY / FOUNDER_ENDORSED / FOUNDER_DISAGREES / FOUNDER_REJECTS` |
| | `category: STOCK_FROM_ANOMALY / STOCK_FROM_REQUEST / CLOSE_SYSTEM_PRODUCT / WEEKLY_INTELLIGENCE` |
| **IDs / foreign keys** | `publication_id: UUID v7`, `case_id → CASE-01.case_id`, `verdict_id → UV-01.verdict_id` |
| **PIT fields** | `published_date` |
| **provenance fields** | `editor`, `research_verdict` |
| **validation_rules** | Never FOUNDER_ENDORSED unless Founder explicitly acts. Governance jargon removed (FD #94). Companion publication linked (FD #96). |
| **immutability_rules** | Publication immutable after Founder action. |
| **revision_rules** | §23.9 corrections preserve original + correction record. |
| **failure_semantics** | Publication not ready → RESEARCH_COMPLETE state. |
| **canonical_boundary** | Publication is NONCANONICAL for investment truth. Canonical for record. |

### G-6: FounderDecisionReference

| Field | Value |
|-------|-------|
| **schema_id** | FDR-01 |
| **purpose** | Reference to Founder's decision on a case. |
| **authority_source** | M3-09 §5.2 |
| **owner** | Founder |
| **required_fields** | `founder_decision_id`, `case_id`, `decision_type`, `decision_date`, `fd_number` |
| **optional_fields** | `notes`, `publication_id` |
| **enums** | `decision_type: ENDORSED / DISAGREES / REJECTS / POLICY_OVERRIDE` |
| **IDs / foreign keys** | `founder_decision_id: UUID v7`, `case_id → CASE-01.case_id`, `publication_id → PUB-01.publication_id` |
| **PIT fields** | `decision_date` |
| **provenance fields** | `founder` |
| **validation_rules** | Only Founder can create FOUNDER_ENDORSED. |
| **immutability_rules** | Decision immutable. |
| **revision_rules** | N/A. |
| **failure_semantics** | N/A. |
| **canonical_boundary** | Canonical (final authority). |

---

### G-7: ChallengeResponse

| Field | Value |
|-------|-------|
| **schema_id** | CRESP-01 |
| **purpose** | Chief Underwriter's response to Red Team challenge findings. |
| **authority_source** | M3-09 §2.4 (Red Team no veto; findings preserved), M3-09 §4 (Underwriter synthesis) |
| **owner** | Chief Underwriter (Role 8) |
| **required_fields** | `response_id`, `challenge_id`, `case_id`, `responses[]`, `adopted_findings[]`, `rejected_findings[]`, `underwriter` |
| **optional_fields** | `rejection_evidence[]`, `notes` |
| **enums** | N/A |
| **IDs / foreign keys** | `response_id: UUID v7`, `challenge_id → RTC-01.challenge_id`, `case_id → CASE-01.case_id` |
| **PIT fields** | `response_date` |
| **provenance fields** | `underwriter` |
| **validation_rules** | Red Team findings cannot be suppressed. Rejected findings must include evidence basis. |
| **immutability_rules** | Response immutable. |
| **revision_rules** | N/A. |
| **failure_semantics** | N/A. |
| **canonical_boundary** | Canonical. |

---

## H — Monitoring & Knowledge (7 schemas)

### H-1: MonitoringIndicator

| Field | Value |
|-------|-------|
| **schema_id** | MI-01 |
| **purpose** | Thesis-specific monitoring indicator. |
| **authority_source** | M3-09 §6 (Thesis Monitoring) |
| **owner** | Thesis / Knowledge Steward (Role 12) |
| **required_fields** | `indicator_id`, `case_id`, `indicator_name`, `indicator_type`, `baseline_value`, `current_value`, `frequency`, `owner` |
| **optional_fields** | `threshold_alert`, `last_observed`, `trend`, `notes` |
| **enums** | `indicator_type: RECOVERY / WARNING / THESIS_KILLER` |
| **IDs / foreign keys** | `indicator_id: UUID v7`, `case_id → CASE-01.case_id` |
| **PIT fields** | `last_observed`, `as_of` |
| **provenance fields** | `owner`, `definition_source` |
| **validation_rules** | Indicators are thesis-specific, not generic news flow. |
| **immutability_rules** | Indicator definition immutable. |
| **revision_rules** | Value updates append-only. |
| **failure_semantics** | Data unavailable → `UNCERTAIN`. |
| **canonical_boundary** | Canonical. |

### H-2: MonitoringObservation

| Field | Value |
|-------|-------|
| **schema_id** | MO-01 |
| **purpose** | Point-in-time observation of monitoring indicator. |
| **authority_source** | M3-09 §6 |
| **owner** | Thesis / Knowledge Steward (Role 12) |
| **required_fields** | `observation_id`, `indicator_id`, `observed_value`, `observation_date`, `observer` |
| **optional_fields** | `evidence_id`, `trigger_event`, `notes` |
| **IDs / foreign keys** | `observation_id: UUID v7`, `indicator_id → MI-01.indicator_id` |
| **PIT fields** | `observation_date` |
| **provenance fields** | `observer` |
| **validation_rules** | Observations are append-only. |
| **immutability_rules** | Observation immutable. |
| **revision_rules** | N/A. |
| **failure_semantics** | Observation unavailable → flagged. |
| **canonical_boundary** | Canonical. |

### H-3: MonitoringAssessment

| Field | Value |
|-------|-------|
| **schema_id** | MASS-01 |
| **purpose** | Periodic monitoring state assessment. |
| **authority_source** | M3-09 §6.3 |
| **owner** | Thesis / Knowledge Steward (Role 12) |
| **required_fields** | `assessment_id`, `case_id`, `monitoring_state`, `assessment_date`, `indicator_ids[]`, `assessor` |
| **optional_fields** | `trigger_events[]`, `evidence_ids[]`, `narrative` |
| **enums** | `monitoring_state: RECOVERY_CONFIRMING / ON_TRACK / UNCERTAIN / WEAKENING / BROKEN` |
| **IDs / foreign keys** | `assessment_id: UUID v7`, `case_id → CASE-01.case_id`, `indicator_ids[] → MI-01.indicator_id` |
| **PIT fields** | `assessment_date` |
| **provenance fields** | `assessor` |
| **validation_rules** | BROKEN state triggers notification to Founder. |
| **immutability_rules** | Assessment immutable. |
| **revision_rules** | New data → new version. |
| **failure_semantics** | Uncertainty → UNCERTAIN state. |
| **canonical_boundary** | Canonical. |

### H-4: CandidateLesson

| Field | Value |
|-------|-------|
| **schema_id** | CL-01 |
| **purpose** | Tentative generalization from one or more cases. |
| **authority_source** | M3-09 §7 (Knowledge Compounding) |
| **owner** | Thesis / Knowledge Steward (Role 12) |
| **required_fields** | `lesson_id`, `source_case_ids[]`, `pattern`, `validation_status`, `proposer` |
| **optional_fields** | `cross_validation_ids[]`, `reviewer`, `review_date`, `industry_playbook_id` |
| **enums** | `validation_status: RESEARCH_FINDING / CANDIDATE_LESSON / CROSS_CASE_VALIDATED / INDEPENDENTLY_REVIEWED / APPROVED_KNOWLEDGE` |
| **IDs / foreign keys** | `lesson_id: UUID v7`, `source_case_ids[] → CASE-01.case_id` |
| **PIT fields** | `proposed_date`, `review_date` |
| **provenance fields** | `proposer`, `reviewer` |
| **validation_rules** | Single case does NOT automatically become institutional knowledge. Cross-case validation requires 3+ cases. |
| **immutability_rules** | Lesson content immutable. |
| **revision_rules** | New evidence → new version. |
| **failure_semantics** | Validation fails → remains at current status. |
| **canonical_boundary** | Canonical. |

### H-5: InstitutionalKnowledgeRecord

| Field | Value |
|-------|-------|
| **schema_id** | IKR-01 |
| **purpose** | Approved institutional knowledge. |
| **authority_source** | M3-09 §7 |
| **owner** | Thesis / Knowledge Steward (Role 12) |
| **required_fields** | `knowledge_id`, `lesson_id`, `knowledge_statement`, `approval_date`, `approved_by` |
| **optional_fields** | `industry_playbook_id`, `supporting_evidence_ids[]`, `contradicting_evidence_ids[]` |
| **IDs / foreign keys** | `knowledge_id: UUID v7`, `lesson_id → CL-01.lesson_id` |
| **PIT fields** | `approval_date` |
| **provenance fields** | `approved_by`, `review_chain` |
| **validation_rules** | Requires cross-case validation + independent review + Chief Underwriter approval. |
| **immutability_rules** | Knowledge immutable. |
| **revision_rules** | Contradicting evidence → new version with superseded_by pointer. |
| **failure_semantics** | N/A. |
| **canonical_boundary** | Canonical. |

### H-6: IndustryPlaybookRecord

| Field | Value |
|-------|-------|
| **schema_id** | IPR-01 |
| **purpose** | Structured knowledge about an industry. |
| **authority_source** | M3-09 §7, M3-06 §3.3 |
| **owner** | Thesis / Knowledge Steward (Role 12) |
| **required_fields** | `playbook_id`, `industry`, `key_metrics[]`, `warning_signs[]`, `knowledge_ids[]`, `approval_date` |
| **optional_fields** | `supply_chain_structure`, `what_to_measure`, `competitive_dynamics`, `capital_cycle_patterns` |
| **IDs / foreign keys** | `playbook_id: UUID v7`, `knowledge_ids[] → IKR-01.knowledge_id` |
| **PIT fields** | `approval_date`, `last_updated` |
| **provenance fields** | `creator`, `approver` |
| **validation_rules** | Requires multiple cases in same industry + systematic distillation. |
| **immutability_rules** | Playbook immutable. |
| **revision_rules** | New industry knowledge → new version. |
| **failure_semantics** | Insufficient cases → not yet created. |
| **canonical_boundary** | Canonical. |

---

### H-7: CrossCaseValidation

| Field | Value |
|-------|-------|
| **schema_id** | CCV-01 |
| **purpose** | Record of cross-case validation for a candidate lesson. |
| **authority_source** | M3-09 §7 (Knowledge Compounding), M3-09 §7.1 (Cross-Case Validation) |
| **owner** | Thesis / Knowledge Steward (Role 12) |
| **required_fields** | `validation_id`, `lesson_id`, `validating_case_ids[]`, `pattern_consistent`, `validator`, `validation_date` |
| **optional_fields** | `inconsistent_case_ids[]`, `notes`, `industry_playbook_id` |
| **enums** | `validation_result: CONFIRMED / PARTIALLY_CONFIRMED / INCONCLUSIVE / REJECTED` |
| **IDs / foreign keys** | `validation_id: UUID v7`, `lesson_id → CL-01.lesson_id`, `validating_case_ids[] → CASE-01.case_id` |
| **PIT fields** | `validation_date` |
| **provenance fields** | `validator`, `method` |
| **validation_rules** | Requires 3+ independent cases for cross-case validation. Single case cannot validate. |
| **immutability_rules** | Validation record immutable. |
| **revision_rules** | New case → new validation version. |
| **failure_semantics** | REJECTED → lesson remains at CANDIDATE_LESSON status. |
| **canonical_boundary** | Canonical. |

---

## I — Reproducibility & Operations (9 schemas)

### I-1: ResearchRunManifest

| Field | Value |
|-------|-------|
| **schema_id** | RRM-01 |
| **purpose** | Complete record of a research run for reproducibility. |
| **authority_source** | M3-01 §8 (Run Manifest) |
| **owner** | Run Manifest Service (S6) |
| **required_fields** | `manifest_id`, `case_id`, `case_version`, `as_of_date`, `universe_version`, `selection_policy_version`, `models_used[]`, `providers{}`, `start_time`, `completion_time` |
| **optional_fields** | `model_versions{}`, `prompts_contracts[]`, `notebook_runs[]`, `deep_research_runs[]`, `sources_added`, `calculation_version`, `token_usage{}`, `cost{}`, `retries`, `failures[]`, `output_version` |
| **IDs / foreign keys** | `manifest_id: UUID v7`, `case_id → CASE-01.case_id` |
| **PIT fields** | `as_of_date`, `start_time`, `completion_time` |
| **provenance fields** | All fields above are provenance. |
| **validation_rules** | Run start record created even if run fails (partial manifest). |
| **immutability_rules** | Manifest immutable after run completion. |
| **revision_rules** | N/A (one per run). |
| **failure_semantics** | Partial manifest if run fails. |
| **canonical_boundary** | Canonical. |

### I-2: PITContext

| Field | Value |
|-------|-------|
| **schema_id** | PITC-01 |
| **purpose** | Point-in-time context for a query or evaluation. |
| **authority_source** | M3-01 §8 (PIT Lock), M3-SERVICES S7 (PIT Lock) |
| **owner** | Point-in-Time Lock Service (S7) |
| **required_fields** | `pit_context_id`, `as_of_date`, `mode`, `case_id`, `created_by` |
| **optional_fields** | `evidence_count_pre`, `evidence_count_post`, `exception_reason` |
| **enums** | `mode: LIVE_CASE_UPDATE / SEALED_HISTORICAL_EVALUATION / REPLAY_EXCEPTION` |
| **IDs / foreign keys** | `pit_context_id: UUID v7`, `case_id → CASE-01.case_id` |
| **PIT fields** | `as_of_date`, `created_at` |
| **provenance fields** | `created_by`, `mode` |
| **validation_rules** | SEALED mode hard-blocks post-AS_OF evidence. LIVE mode requires explicit UPDATE tag. REPLAY exception requires provenance. |
| **immutability_rules** | Context immutable. |
| **revision_rules** | N/A. |
| **failure_semantics** | PIT service unavailable → queries blocked (fail closed). |
| **canonical_boundary** | Canonical. |

### I-3: ServiceInvocation

| Field | Value |
|-------|-------|
| **schema_id** | SI-01 |
| **purpose** | Record of a service invocation. |
| **authority_source** | M3-ROLES §5 (Service Registry) |
| **owner** | Run Manifest Service (S6) |
| **required_fields** | `invocation_id`, `service_id`, `case_id`, `request_type`, `invoked_at`, `status` |
| **optional_fields** | `input_summary`, `output_summary`, `error`, `duration_ms`, `retry_count` |
| **enums** | `status: SUCCESS / FAILURE / PARTIAL / TIMEOUT` |
| **IDs / foreign keys** | `invocation_id: UUID v7`, `case_id → CASE-01.case_id` |
| **PIT fields** | `invoked_at`, `completed_at` |
| **provenance fields** | `service_id`, `case_id` |
| **validation_rules** | Every service invocation recorded. |
| **immutability_rules** | Invocation record immutable. |
| **revision_rules** | N/A. |
| **failure_semantics** | Failure recorded with error details. |
| **canonical_boundary** | Canonical. |

### I-4: RetryRecord

| Field | Value |
|-------|-------|
| **schema_id** | RR-01 |
| **purpose** | Record of retry attempts for a failed operation. |
| **authority_source** | M3-01 §7 (Reliability), M3-SERVICES S8 (Retry Controller) |
| **owner** | Retry / Research Execution Controller (S8) |
| **required_fields** | `retry_id`, `invocation_id`, `attempt_number`, `attempted_at`, `status`, `error` |
| **optional_fields** | `resolution`, `escalated_to` |
| **enums** | `status: RETRYING / SUCCEEDED / FAILED / ESCALATED` |
| **IDs / foreign keys** | `retry_id: UUID v7`, `invocation_id → SI-01.invocation_id` |
| **PIT fields** | `attempted_at` |
| **provenance fields** | `invocation_id` |
| **validation_rules** | Max 3 retries per stage. After 3 → FAILED. |
| **immutability_rules** | Record immutable. |
| **revision_rules** | N/A. |
| **failure_semantics** | After 3 retries → FAILED. |
| **canonical_boundary** | Canonical. |

### I-5: CaseLock

| Field | Value |
|-------|-------|
| **schema_id** | CLK-01 |
| **purpose** | Lock state for a case during active research. |
| **authority_source** | M3-SERVICES S9 (Case Locking) |
| **owner** | Case Locking / Idempotency Service (S9) |
| **required_fields** | `lock_id`, `case_id`, `case_version`, `lock_state`, `locked_by`, `locked_at` |
| **optional_fields** | `unlocked_at`, `lock_reason` |
| **enums** | `lock_state: LOCKED / UNLOCKED / PENDING` |
| **IDs / foreign keys** | `lock_id: UUID v7`, `case_id → CASE-01.case_id` |
| **PIT fields** | `locked_at`, `unlocked_at` |
| **provenance fields** | `locked_by` |
| **validation_rules** | Case cannot be modified during active research. New as-of → new case version. |
| **immutability_rules** | Lock record immutable. |
| **revision_rules** | N/A. |
| **failure_semantics** | Lock unavailable → request queued. |
| **canonical_boundary** | Canonical. |

### I-6: BudgetUsage

| Field | Value |
|-------|-------|
| **schema_id** | BU-01 |
| **purpose** | Per-resource budget usage record. |
| **authority_source** | M3-01 §9 (Budget Discipline) |
| **owner** | Research Budget Controller (S2) |
| **required_fields** | `usage_id`, `budget_id`, `resource_type`, `amount_consumed`, `usage_timestamp`, `case_id` |
| **optional_fields** | `provider`, `model`, `tokens`, `cost` |
| **enums** | `resource_type: TOKEN / API_CALL / DEEP_RESEARCH / NOTEBOOKLM / COMPUTATION / STORAGE / OTHER` |
| **IDs / foreign keys** | `usage_id: UUID v7`, `budget_id → RB-01.budget_id` |
| **PIT fields** | `usage_timestamp` |
| **provenance fields** | `resource_type`, `provider` |
| **validation_rules** | Spend tracking is append-only. |
| **immutability_rules** | Usage record immutable. |
| **revision_rules** | N/A. |
| **failure_semantics** | Budget exhausted → EXHAUSTED state. |
| **canonical_boundary** | Canonical. |

### I-7: ModelInvocation

| Field | Value |
|-------|-------|
| **schema_id** | MOD-01 |
| **purpose** | Record of a model invocation. |
| **authority_source** | M3-01 §8 (Run Manifest), M4B (Model/ Cost Evaluation) |
| **owner** | Run Manifest Service (S6) |
| **required_fields** | `model_invocation_id`, `case_id`, `model`, `provider`, `prompt_tokens`, `completion_tokens`, `cost`, `invoked_at`, `status` |
| **optional_fields** | `prompt_hash`, `response_hash`, `latency_ms`, `retry_count`, `error` |
| **enums** | `status: SUCCESS / FAILURE / RATE_LIMITED / TIMEOUT` |
| **IDs / foreign keys** | `model_invocation_id: UUID v7`, `case_id → CASE-01.case_id` |
| **PIT fields** | `invoked_at` |
| **provenance fields** | `model`, `provider` |
| **validation_rules** | Every model invocation recorded for cost tracking. |
| **immutability_rules** | Record immutable. |
| **revision_rules** | N/A. |
| **failure_semantics** | Failure recorded. |
| **canonical_boundary** | Canonical. |

### I-8: ProviderInvocation

| Field | Value |
|-------|-------|
| **schema_id** | PROV-01 |
| **purpose** | Record of a provider invocation (may wrap multiple models). |
| **authority_source** | M3-01 §8 |
| **owner** | Run Manifest Service (S6) |
| **required_fields** | `provider_invocation_id`, `case_id`, `provider`, `service`, `cost`, `invoked_at`, `status` |
| **optional_fields** | `model_invocation_ids[]`, `error`, `fallback_used` |
| **enums** | `status: SUCCESS / FAILURE / FALLBACK_USED` |
| **IDs / foreign keys** | `provider_invocation_id: UUID v7`, `case_id → CASE-01.case_id`, `model_invocation_ids[] → MOD-01.model_invocation_id` |
| **PIT fields** | `invoked_at` |
| **provenance fields** | `provider`, `service` |
| **validation_rules** | Fallback must be recorded explicitly. |
| **immutability_rules** | Record immutable. |
| **revision_rules** | N/A. |
| **failure_semantics** | Fallback used recorded. |
| **canonical_boundary** | Canonical. |

### I-9: EvaluationHarnessRun

| Field | Value |
|-------|-------|
| **schema_id** | EHR-01 |
| **purpose** | Record of an evaluation harness execution. |
| **authority_source** | M3-SERVICES S12 (Evaluation Harness) |
| **owner** | Evaluation Harness (S12) |
| **required_fields** | `eval_run_id`, `evaluation_type`, `policy_version`, `corpus_version`, `pit_snapshot`, `started_at`, `status` |
| **optional_fields** | `completed_at`, `metrics{}`, `fixture_results[]`, `failures[]`, `token_usage`, `cost` |
| **enums** | `evaluation_type: TYPE_A_RESEARCH_QUALITY / TYPE_B_DISCOVERY_RECALL / CALIBRATION / COST_EVAL` |
| | `status: IN_PROGRESS / COMPLETE / EVALUATION_INCOMPLETE / FAILED` |
| **IDs / foreign keys** | `eval_run_id: UUID v7` |
| **PIT fields** | `started_at`, `completed_at`, `pit_snapshot` |
| **provenance fields** | `policy_version`, `corpus_version`, `pit_snapshot` |
| **validation_rules** | Partial evaluation = EVALUATION_INCOMPLETE (cannot satisfy gate). Post-AS_OF data HARD BLOCKED in SEALED mode. |
| **immutability_rules** | Run record immutable. |
| **revision_rules** | N/A. |
| **failure_semantics** | EVALUATION_INCOMPLETE — cannot satisfy evaluation gate. |
| **canonical_boundary** | Canonical. |

<!-- 2026-08-19 15:00 UTC+7 -->