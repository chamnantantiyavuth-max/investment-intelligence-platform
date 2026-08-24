# QAD-M5.2 Persistence Boundary Contract

> **Status:** NEW_M5_IMPLEMENTATION_DERIVATION
> **Authority:** FD #135
> **Date:** 2026-08-24
> **Spec Source:** `QAD-M4A-CANONICAL-SCHEMAS.md` (68 frozen schemas, M4A-FROZEN+ERRATUM-001)
> **Generator:** M5.2-20260824
> **Predecessor:** `QAD-M4A-CANONICAL-SCHEMAS.md` (M4A boundary metadata), `qad/contract/canonical_boundary.py`, `qad/contract/fk_registry.py`, `qad/contract/contract_descriptor.json`

---

## Table of Contents

1. [Architecture Overview — Ports & Adapters](#1-architecture-overview--ports--adapters)
2. [The Five Canonical Stores](#2-the-five-canonical-stores)
3. [Noncanonical Research Room](#3-noncanonical-research-room)
4. [Identity Key Policy](#4-identity-key-policy)
5. [Version Semantics](#5-version-semantics)
6. [FK Enforcement at Persistence Layer](#6-fk-enforcement-at-persistence-layer)
7. [Transaction Boundaries](#7-transaction-boundaries)
8. [Deterministic Canonical Serialization](#8-deterministic-canonical-serialization)
9. [Reference Adapter Scope](#9-reference-adapter-scope)
10. [Deferred to M5.3](#10-deferred-to-m53)
11. [Schema-to-Store Derivation](#11-schema-to-store-derivation)
12. [Appendix A: Full Store-to-Schema Map](#appendix-a-full-store-to-schema-map)
13. [Appendix B: FK Graph by Store](#appendix-b-fk-graph-by-store)
14. [Appendix C: Immutable-field Policy Summary](#appendix-c-immutable-field-policy-summary)

---

## 1. Architecture Overview — Ports & Adapters

The M5.2 persistence boundary introduces a **ports-and-adapters** architecture that separates the canonical domain from any specific storage technology. No production stack is selected here; the contract defines the shape of the persistence boundary that any adapter must satisfy.

### 1.1 High-Level Structure

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     CANONICAL DOMAIN (inside hexagon)                    │
│                                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Identity │  │ Evidence │  │Governance│  │ Analytics│  │ Operations│  │
│  │  Store   │  │  Store   │  │  Store   │  │  Store   │  │  Store   │  │
│  │  (Port)  │  │  (Port)  │  │  (Port)  │  │  (Port)  │  │  (Port)  │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  │
│       │              │             │             │             │        │
│       └──────────────┴─────────────┴─────────────┴─────────────┘        │
│                              │                                           │
│                    Port Interface Layer                                   │
│                    (StorePort Protocol)                                   │
└───────────────────────────────┬───────────────────────────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │   Adapter Boundary    │
                    │ (technology-specific) │
                    └───────────────────────┘
```

### 1.2 Port Interface

Every canonical store exposes a **StorePort** — an abstract interface that defines:

- `save(record: CanonicalRecord) -> Result[RecordId, StoreError]` — persist a single canonical record
- `save_batch(records: list[CanonicalRecord]) -> Result[list[RecordId], StoreError]` — batch persist (all-or-nothing per store)
- `load(record_id: RecordId) -> Result[CanonicalRecord, StoreError]` — load by identity key
- `load_by_fk(target: str, fk_value: str) -> Result[list[CanonicalRecord], StoreError]` — load by foreign key
- `exists(record_id: RecordId) -> bool` — existence check
- `delete(record_id: RecordId) -> Result[None, StoreError]` — logical or physical delete (per schema immutability rules)

### 1.3 Adapter Contract

An adapter is any implementation of the StorePort protocol for a specific schema. The adapter must:

1. Enforce all **immutability rules** declared in the M4A schema metadata (see §5).
2. Enforce all **FK references** declared in `fk_registry.py` (see §6).
3. Produce **deterministic canonical serialization** for every stored record (see §8).
4. Honor **transaction boundaries** (see §7).
5. Reject writes that violate the **canonical boundary** — noncanonical data must use the Research Room (see §3).

### 1.4 Layer Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                             │
│  (Domain services, research workflows, agents)                    │
├──────────────────────────────────────────────────────────────────┤
│                      PORT LAYER                                   │
│  StorePort (abstract) — 5 ports, one per canonical store          │
├──────────────────────────────────────────────────────────────────┤
│                     ADAPTER LAYER                                  │
│  IdentityStoreAdapter  EvidenceStoreAdapter  GovernanceStoreAdapter│
│  AnalyticsStoreAdapter  OperationsStoreAdapter                     │
│  + ResearchRoomAdapter (noncanonical)                             │
├──────────────────────────────────────────────────────────────────┤
│                 PERSISTENCE TECHNOLOGY                             │
│  (Not selected — may be SQL, document store, key-value, etc.)     │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. The Five Canonical Stores

All 68 M4A schemas are canonical. The noncanonical set is empty (no noncanonical M4A schemas exist). The five stores are derived mechanically from the M4A family letter (see §11).

### 2.1 Identity Store (Family A)

**Schemas:** 6

| Schema ID | Name | Required FK Targets |
|-----------|------|---------------------|
| SM-01 | SecurityMaster | (none — root anchor) |
| RU-01 | ResearchableUniverseRecord | SM-01.entity_id |
| SR-01 | SignalRecord | SM-01.entity_id |
| CR-01 | CandidateRecord | SM-01.entity_id, SR-01.signal_id |
| QU-01 | QualityUniverseRecord | SM-01.entity_id, EV-01.evidence_id |
| CASE-01 | CaseRecord | SM-01.entity_id, CR-01.candidate_id |

**Purpose:** Ground truth for entity identity, universe membership, signal detection, candidate selection, quality assessment, and case lifecycle. Every other store references this store via `entity_id` or `case_id`.

### 2.2 Evidence Store (Family B)

**Schemas:** 10

| Schema ID | Name | Required FK Targets |
|-----------|------|---------------------|
| SRC-01 | SourceRecord | (none) |
| EV-01 | EvidenceRecord | SRC-01.source_id, EV-01.evidence_id (self-ref) |
| FACT-01 | FactRecord | EV-01.evidence_id |
| CLM-01 | ClaimRecord | EV-01.evidence_id |
| INF-01 | InferenceRecord | EV-01.evidence_id |
| HYP-01 | HypothesisRecord | CASE-01.case_id |
| CTR-01 | ContradictionRecord | EV-01.evidence_id |
| EG-01 | EvidenceGap | CASE-01.case_id |
| EAR-01 | EvidenceAdmissionRecord | EV-01.evidence_id |
| SRCV-01 | SourceVersion | SRC-01.source_id |

**Purpose:** Immutable source documents, canonical evidence objects, fact/claim/inference/hypothesis taxonomy, contradiction management, evidence gaps, and admission audit trail.

### 2.3 Governance Store (Family C)

**Schemas:** 8

| Schema ID | Name | Required FK Targets |
|-----------|------|---------------------|
| RC-01 | ResearchCharter | CASE-01.case_id, HYP-01.hypothesis_id |
| RSR-01 | ResearchStageRecord | CASE-01.case_id |
| IC-01 | InvestigatorCharter | EG-01.gap_id |
| RB-01 | ResearchBudgetRecord | CASE-01.case_id |
| RFR-01 | ResearchFailureRecord | CASE-01.case_id |
| HS-01 | HypothesisSet | CASE-01.case_id, HYP-01.hypothesis_id |
| IR-01 | InvestigationReport | IC-01.investigator_charter_id, EG-01.gap_id |
| RSR-02 | ResearchStopRecord | CASE-01.case_id |

**Purpose:** Research charter, stage execution, budget allocation, failure recording, hypothesis set management, scuttlebutt investigation charters and reports, and stop decisions.

### 2.4 Analytics Store (Families D + E + F)

**Schemas:** 21

| Schema ID | Name | Required FK Targets |
|-----------|------|---------------------|
| QA-01 | QualityAssessment | CASE-01.case_id, EV-01.evidence_id |
| MA-01 | MoatAssessment | CASE-01.case_id |
| IE-01 | IndustryEconomicsRecord | CASE-01.case_id |
| MC-01 | ManagementClaim | CASE-01.case_id, SRC-01.source_id |
| CAE-01 | CapitalAllocationEvent | CASE-01.case_id |
| MDL-01 | ManagementDecisionLedger | CASE-01.case_id |
| MO-02 | ManagementOutcome | CASE-01.case_id, MC-01.claim_id |
| DR-01 | DislocationRecord | CASE-01.case_id |
| IA-01 | ImpairmentAssessment | CASE-01.case_id |
| CE-01 | CompetingExplanation | IA-01.impairment_id |
| RM-01 | RecoveryModel | CASE-01.case_id |
| TK-01 | ThesisKiller | CASE-01.case_id |
| FE-01 | FlipEvidence | IA-01.impairment_id |
| FF-01 | FinancialFact | CASE-01.case_id, SRC-01.source_id |
| NFF-01 | NormalizedFinancialFact | FF-01.financial_fact_id |
| CALC-01 | CalculationRecord | CASE-01.case_id |
| SCEN-01 | ScenarioRecord | CASE-01.case_id |
| PLA-01 | PermanentLossAssessment | CASE-01.case_id |
| RDCF-01 | ReverseDCFRecord | CASE-01.case_id |
| VA-01 | ValuationAssessment | CASE-01.case_id, RDCF-01.r_dcf_id, PLA-01.assessment_id |
| PIE-01 | PriceImpliedExpectation | CASE-01.case_id |

**Purpose:** Business & industry analysis, management assessment, impairment diagnosis, recovery modeling, financial reconstruction, normalization, calculations, scenario analysis, valuation, and price-implied expectations.

### 2.5 Operations Store (Families G + H + I)

**Schemas:** 23

| Schema ID | Name | Required FK Targets |
|-----------|------|---------------------|
| RTC-01 | RedTeamChallenge | CASE-01.case_id |
| AF-01 | AuditFinding | AG-01.audit_id |
| AG-01 | AuditGate (AuditReport) | CASE-01.case_id, AF-01.finding_id |
| UV-01 | UnderwritingVerdict | CASE-01.case_id, RTC-01.challenge_id, AG-01.audit_id |
| PUB-01 | PublicationRecord | CASE-01.case_id, UV-01.verdict_id |
| FDR-01 | FounderDecisionReference | CASE-01.case_id, PUB-01.publication_id |
| CRESP-01 | ChallengeResponse | RTC-01.challenge_id, CASE-01.case_id |
| MI-01 | MonitoringIndicator | CASE-01.case_id |
| MO-01 | MonitoringObservation | MI-01.indicator_id |
| MASS-01 | MonitoringAssessment | CASE-01.case_id, MI-01.indicator_id |
| CL-01 | CandidateLesson | CASE-01.case_id |
| IKR-01 | InstitutionalKnowledgeRecord | CL-01.lesson_id |
| IPR-01 | IndustryPlaybookRecord | IKR-01.knowledge_id |
| CCV-01 | CrossCaseValidation | CL-01.lesson_id, CASE-01.case_id |
| RRM-01 | RunManifestRecord | CASE-01.case_id |
| PITC-01 | PITContext | CASE-01.case_id |
| SI-01 | ServiceInvocation | CASE-01.case_id |
| RR-01 | RetryRecord | SI-01.invocation_id |
| CLK-01 | CaseLock | CASE-01.case_id |
| BU-01 | BudgetUsage | RB-01.budget_id |
| MOD-01 | ModelInvocation | CASE-01.case_id |
| PROV-01 | ProviderInvocation | CASE-01.case_id, MOD-01.model_invocation_id |
| EHR-01 | EvaluationHarnessRun | (none) |

**Purpose:** Red Team challenge, audit, underwriting, publication, Founder decisions, monitoring, institutional knowledge, reproducibility (run manifests, invocations, retries, locks, budget usage), and evaluation harness.

---

## 3. Noncanonical Research Room

### 3.1 Rationale

The M4A defines a strict canonical boundary. Per `canonical_boundary.py`, all 68 schemas are canonical. However, the M4A evidence boundary explicitly states:

> **EV-01:** *"Canonical (Layer 2). NotebookLM/DR output is NONCANONICAL until validated."*
> **IR-01:** *"Canonical. Proposed evidence noncanonical until admitted."*
> **PUB-01:** *"Publication is NONCANONICAL for investment truth. Canonical for record."*

This means raw AI-generated output (NotebookLM, Deep Research) and unvalidated intermediary artifacts must be stored **outside** the canonical stores.

### 3.2 Research Room Boundary

The **Research Room** is a noncanonical persistence zone with the following properties:

1. **No immutability guarantees** — data can be overwritten, deleted, or modified freely.
2. **No FK enforcement** — references to canonical records are advisory, not enforced.
3. **No PIT enforcement** — data is not subject to point-in-time locking.
4. **No version semantics** — no versioning contract.
5. **No serialization contract** — representation is free-form.
6. **Ephemeral by default** — data may be garbage-collected without notice.

### 3.3 Isolation Rules

| Aspect | Canonical Store | Research Room |
|--------|----------------|---------------|
| Schema | M4A contract | Free-form (JSON, markdown, etc.) |
| Immutability | Enforced per M4A rules | None |
| FK validation | Enforced | None |
| PIT lock | Enforced (M5.3) | None |
| Serialization | Deterministic | Free-form |
| Retention | Permanent | Ephemeral |
| Audit trail | Full (EAR, provenance) | None |

### 3.4 Admission Gate

Data moves from the Research Room into the canonical Evidence Store only through the **Evidence Admission Gate**, which enforces:

1. Validation against original source (NotebookLM/DR → original source verification).
2. Validation of source tier (L10 cannot be sole support for material conclusion).
3. Creation of `EvidenceAdmissionRecord` (EAR-01) as immutable audit trail.
4. Assignment of `validation_status` (RAW → VALIDATED).
5. PIT snapshots are captured at admission time.

### 3.5 Research Room Adapter

A `ResearchRoomAdapter` implements a minimal `StorePort`-like interface but with **no enforcement guarantees**. It is a sandbox for exploration, not a persistence contract.

---

## 4. Identity Key Policy

### 4.1 Key Type

All identity keys are **UUID v7** represented as **strings** in the canonical domain.

**Rationale:**
- UUID v7 is time-ordered (MSB encodes Unix timestamp), enabling natural sort by creation time.
- String representation avoids binary encoding issues across adapters.
- UUID v7 provides 122 bits of random entropy, sufficient for collision-free identity across all IIP records.

### 4.2 Key Fields

The following fields are identity keys (primary keys), all typed as `UUID v7`:

| Schema | Identity Key | Exception |
|--------|-------------|-----------|
| SM-01 | `entity_id` | — |
| RU-01 | `entity_id` | (inherits from SM-01) |
| SR-01 | `signal_id` | — |
| CR-01 | `candidate_id` | — |
| QU-01 | `entity_id` | (inherits from SM-01) |
| CASE-01 | `case_id` | Format: `CASE-YYYY-NNN` (human-readable, not UUID) |
| SRC-01 | `source_id` | — |
| EV-01 | `evidence_id` | — |
| FACT-01 | `fact_id` | — |
| CLM-01 | `claim_id` | — |
| INF-01 | `inference_id` | — |
| HYP-01 | `hypothesis_id` | — |
| CTR-01 | `contradiction_id` | — |
| EG-01 | `gap_id` | — |
| EAR-01 | `admission_id` | — |
| SRCV-01 | `version_id` | — |
| RC-01 | `charter_id` | — |
| RSR-01 | `stage_id` | — |
| IC-01 | `investigator_charter_id` | — |
| RB-01 | `budget_id` | — |
| RFR-01 | `failure_id` | — |
| HS-01 | `hypothesis_set_id` | — |
| IR-01 | `investigation_id` | — |
| RSR-02 | `stop_id` | — |
| QA-01 | `assessment_id` | — |
| MA-01 | `moat_assessment_id` | — |
| IE-01 | `industry_economics_id` | — |
| MC-01 | `claim_id` | — |
| CAE-01 | `event_id` | — |
| MDL-01 | `ledger_id` | — |
| MO-02 | `outcome_id` | — |
| DR-01 | `dislocation_id` | — |
| IA-01 | `impairment_id` | — |
| CE-01 | `explanation_id` | — |
| RM-01 | `recovery_id` | — |
| TK-01 | `thesis_killer_id` | — |
| FE-01 | `flip_evidence_id` | — |
| FF-01 | `financial_fact_id` | — |
| NFF-01 | `normalized_fact_id` | — |
| CALC-01 | `calculation_id` | — |
| SCEN-01 | `scenario_id` | — |
| PLA-01 | `assessment_id` | — |
| RDCF-01 | `r_dcf_id` | — |
| VA-01 | `valuation_id` | — |
| PIE-01 | `expectation_id` | — |
| RTC-01 | `challenge_id` | — |
| AF-01 | `finding_id` | — |
| AG-01 | `audit_id` | — |
| UV-01 | `verdict_id` | — |
| PUB-01 | `publication_id` | — |
| FDR-01 | `founder_decision_id` | — |
| CRESP-01 | `response_id` | — |
| MI-01 | `indicator_id` | — |
| MO-01 | `observation_id` | — |
| MASS-01 | `assessment_id` | — |
| CL-01 | `lesson_id` | — |
| IKR-01 | `knowledge_id` | — |
| IPR-01 | `playbook_id` | — |
| CCV-01 | `validation_id` | — |
| RRM-01 | `manifest_id` | — |
| PITC-01 | `pit_context_id` | — |
| SI-01 | `invocation_id` | — |
| RR-01 | `retry_id` | — |
| CLK-01 | `lock_id` | — |
| BU-01 | `usage_id` | — |
| MOD-01 | `model_invocation_id` | — |
| PROV-01 | `provider_invocation_id` | — |
| EHR-01 | `eval_run_id` | — |

### 4.3 Exception: CaseRecord

`CASE-01.case_id` uses the format `CASE-YYYY-NNN` (a human-readable sequential identifier, e.g., `CASE-2026-042`). This is the only exception. All other identity keys are UUID v7 strings.

### 4.4 Generation Policy

- UUID v7 generation must use a cryptographically secure random source.
- The adapter must NOT modify the identity key after generation — keys are set by the domain layer before persistence.
- Keys are immutable once persisted (per `immutable_policy`: `FIELD_IMMUTABLE` or `RECORD_IMMUTABLE`).

---

## 5. Version Semantics

### 5.1 Immutability Policies from M4A Metadata

The `contract_descriptor.json` encodes per-field `immutable_policy` values. The persistence layer must enforce these rules at write time.

The policies are:

| Policy | Meaning | Enforcement |
|--------|---------|-------------|
| `RECORD_IMMUTABLE` | The entire record is immutable once written — no updates allowed. | Adapter must reject any update. Re-insertion must fail or be a no-op (idempotent). |
| `FIELD_IMMUTABLE` | This specific field cannot change after initial write. Other fields may be mutable. | Adapter must reject writes that change this field. |
| `MUTABLE` | Field can be freely updated. | No enforcement. |
| `APPEND_ONLY_STATE` | State-transition field — only forward transitions are allowed. | Adapter must validate state transitions against the enum sequence. |

### 5.2 Versioning Rules per M4A Schema

Each schema in the M4A document declares `immutability_rules` and `revision_rules`. The persistence layer must implement these semantics:

| Immutability Rule Type | Examples | Persistence Contract |
|------------------------|----------|----------------------|
| **Content immutable** | EV-01, FACT-01, CLM-01, INF-01, CTR-01, EG-01, EAR-01, SRCV-01, RFR-01, RSR-02, all Family D/E/F/G/H/I records | `RECORD_IMMUTABLE` — once written, the record must never be modified in place. |
| **State transitions append-only** | CASE-01, CR-01, RU-01, QU-01, RSR-01, HS-01 | State changes create new versions. Previous state preserved. |
| **Superseded_by pointer** | SM-01, CASE-01, HYP-01, INF-01, CL-01, IKR-01 | New version has `superseded_by` pointer to successor. |
| **Ticker/claim history append-only** | SM-01 (ticker_history), MC-01, MO-02 | History is append-only list. |
| **Locked during active research** | CASE-01, CLK-01 | Case-lock service must gate writes. |

### 5.3 Version Key

For schemas that support revision (state transitions), the version key is a tuple:

```
(CASE_VERSION, AS_OF_DATE, SEQUENCE_NUMBER)
```

The `AS_OF_DATE` is the PIT field that determines which version is active for a given point-in-time query. The `SEQUENCE_NUMBER` is a monotonically increasing integer per (case, as_of) group.

### 5.4 Immutable Record Enforcement

The adapter must:

1. **Reject any UPDATE** on a `RECORD_IMMUTABLE` schema (return `RecordImmutableError`).
2. **Reject any UPDATE** to a `FIELD_IMMUTABLE` field (return `FieldImmutableError`).
3. **Validate state transitions** for `APPEND_ONLY_STATE` fields — only forward enum transitions are accepted.
4. **Reject DELETE** on canonical schemas — deletion is not permitted. Use logical tombstone or superseded_by pointer.

---

## 6. FK Enforcement at Persistence Layer

### 6.1 FK Registry

All foreign keys are declared in `qad/contract/fk_registry.py`. Total FK references: **87**, spanning all 68 schemas.

### 6.2 Enforcement Rules

The persistence layer must enforce FK integrity at write time:

| Cardinality | Enforcement |
|-------------|-------------|
| `single` | Target record must exist in the referenced store before the referencing record can be written. |
| `list` | Every target in the list must exist in the referenced store before the referencing record can be written. |

### 6.3 Cross-Store FK Dependencies

FKs that cross store boundaries (the most architecturally significant):

| From Store | Schema | FK Field | Target Store | Target Schema |
|------------|--------|----------|--------------|---------------|
| Governance | RSR-01, RB-01, RFR-01, HS-01, RSR-02, RC-01 | `case_id` | Identity | CASE-01 |
| Analytics | QA-01, MA-01, IE-01, MC-01, CAE-01, MDL-01, MO-02, DR-01, IA-01, RM-01, TK-01, FF-01, CALC-01, SCEN-01, PLA-01, RDCF-01, VA-01, PIE-01 | `case_id` | Identity | CASE-01 |
| Operations | RTC-01, AG-01, UV-01, PUB-01, FDR-01, MI-01, MASS-01, CL-01, RRM-01, PITC-01, SI-01, CLK-01, MOD-01, PROV-01 | `case_id` | Identity | CASE-01 |
| Evidence | HYP-01, EG-01 | `case_id` | Identity | CASE-01 |
| Evidence | EV-01 | `source_id` | Evidence | SRC-01 |
| Operations | BU-01 | `budget_id` | Governance | RB-01 |

**Observation:** `CASE-01.case_id` is the most referenced FK target in the system — 40+ schemas reference it. This makes the Identity Store (specifically CaseRecord) the **central hub** of the FK graph.

### 6.4 Cross-Store FK Constraints

Adapters that implement multiple stores (e.g., a single SQL database) must enforce cross-store FK constraints. Adapters that use separate persistence backends per store must implement **application-level FK verification** or **eventual FK consistency** with explicit documentation.

### 6.5 Self-Referencing FKs

These schemas have self-referencing FKs (contradicts, supersedes):

| Schema | Self-Ref Field | Cardinality | Purpose |
|--------|---------------|-------------|---------|
| EV-01 | `contradicts_ids` | list | Contradicting evidence |
| EV-01 | `superseded_by_id` | single | Superseded evidence |

### 6.6 Deletion Policy

Canonical records are never deleted. FK targets must not be removed while referenced records exist. The adapter must:

1. Reject DELETE on any canonical record that is referenced by another record.
2. Support logical tombstone (e.g., status change to `SUPERSEDED` or `RETRACTED`).

---

## 7. Transaction Boundaries

### 7.1 All-or-Nothing per Store

Each canonical store defines its own transaction boundary. A write to a single store must be atomic:

- **Single record write:** Must succeed or fail atomically.
- **Batch write (same store):** Must succeed or fail atomically. Partial success is not permitted.
- **Cross-store writes:** The application layer (not the adapter) is responsible for coordinating cross-store transactions. The adapter exposes `begin_transaction()`, `commit()`, and `rollback()` per store.

### 7.2 Cross-Store Transaction Strategy

When a single domain operation writes to multiple stores (e.g., creating a new CaseRecord + ResearchStageRecord + ResearchBudgetRecord), the strategy is:

1. **Saga pattern** (preferred): Each store write is a local transaction. If a later write fails, compensating actions roll back earlier writes.
2. **Two-phase commit** (optional): When the adapter stack supports distributed transactions.
3. **Outbox pattern** (for async): Write to an outbox table within the first store's transaction; a background process delivers to other stores.

### 7.3 Transactional Guarantees

| Property | Guarantee |
|----------|-----------|
| Atomicity | Per-store write is atomic. Cross-store coordination is application-layer. |
| Consistency | FK constraints are validated before commit. Immutability policies are enforced before commit. |
| Isolation | At least READ_COMMITTED. Adapter may implement SERIALIZABLE for PIT operations. |
| Durability | Writes are durable on commit. In-memory-only adapters are not permitted for canonical stores. |

### 7.4 Failure Semantics

| Failure | Behavior |
|---------|----------|
| Write fails pre-commit | No partial state. Retry is safe. |
| Write fails mid-commit | Adapter must detect and recover (idempotency key). |
| FK violation | Write rejected with `FKViolationError`. No partial state. |
| Immutability violation | Write rejected with `ImmutabilityViolationError`. No partial state. |

---

## 8. Deterministic Canonical Serialization

### 8.1 Purpose

Every canonical record must have a **deterministic serialization** — a byte-exact representation that can be hashed, compared, and verified across adapters. This guarantees:

- Reproducible content hashes for evidence integrity.
- Cross-adapter record comparison.
- Idempotent writes (same serialized bytes → same record).

### 8.2 Serialization Contract

```
CanonicalSerializer:
  Input:  CanonicalRecord (typed Python object with M4A fields)
  Output: bytes (UTF-8 JSON with sorted keys)

  Rules:
    1. Fields are serialized in lexicographic key order (sorted by field name).
    2. Nested objects are serialized recursively with sorted keys.
    3. Lists are serialized in insertion order (preserved as-is).
    4. Null/missing optional fields are omitted.
    5. Enums are serialized as their string values.
    6. UUIDs are serialized as lowercase strings.
    7. Timestamps are serialized as ISO 8601 strings in UTC.
    8. No whitespace padding (compact JSON).
    9. The serialized form is NOT stored alongside the record — it is a derived artifact.
```

### 8.3 Content Hash

Every record that carries a `content_hash` field (SRC-01, SRCV-01) must compute its hash over the deterministic serialization of the record's **content fields** (excluding provenance/metadata fields).

Hash algorithm: **SHA-256**.

### 8.4 Serialization Bypass

The Research Room has no serialization contract. Data stored there may use any representation.

---

## 9. Reference Adapter Scope

### 9.1 What M5.2 Defines

M5.2 defines the **persistence boundary contract** — the abstract interfaces, rules, and invariants that any adapter must satisfy. It does NOT select or implement a production adapter.

### 9.2 Reference Adapter

A **reference adapter** is an in-memory implementation of all 5 StorePorts + ResearchRoomAdapter, used for:

1. **Testing** — unit tests for domain logic without database dependencies.
2. **Prototyping** — rapid iteration on workflows before production adapter selection.
3. **Contract verification** — validate that the StorePort interface is complete and correct.

### 9.3 Reference Adapter Properties

| Property | Value |
|----------|-------|
| Backend | In-memory `dict[str, CanonicalRecord]` |
| FK enforcement | Full (all 87 FKs validated) |
| Immutability enforcement | Full (per M4A metadata) |
| Serialization | Deterministic (per §8) |
| Transactions | In-memory snapshot isolation |
| PIT enforcement | Not implemented (deferred to M5.3) |
| Retry kernel | Not implemented (deferred to M5.3) |
| Production readiness | Not a goal |

### 9.4 Out of Scope for M5.2

The following are explicitly **not** part of the M5.2 persistence contract:

- **Production adapter selection** (SQLite, PostgreSQL, DuckDB, etc.)
- **Connection pooling, replication, sharding**
- **Backup and disaster recovery**
- **Performance benchmarks and optimization**
- **Schema migration tooling**
- **Monitoring, metrics, and observability**

These are deferred to M5.4+ production planning.

---

## 10. Deferred to M5.3

### 10.1 PIT Enforcement (Point-in-Time Lock)

The M4A specifies PIT semantics for every schema (see `pit_fields` in each schema definition). PIT enforcement is a **cross-cutting concern** that requires:

- A PIT Lock Service (`PITC-01`).
- Query-time filtering to exclude records with `as_of > query_time`.
- Hard-blocking post-AS_OF data in SEALED mode.
- Replay exceptions for evaluation harness.

**Deferred to M5.3** because PIT enforcement is a query-time concern that depends on the adapter's query API, which is not yet defined.

### 10.2 Retry Kernel

The M4A specifies retry semantics (max 3 retries per stage, `RR-01` RetryRecord). The retry kernel is a **service-layer concern** that requires:

- Retry state machine (RETRYING → SUCCEEDED / FAILED / ESCALATED).
- Idempotency guarantees for retried writes.
- Integration with the Run Manifest (RRM-01).

**Deferred to M5.3** because the retry kernel is a service (not a persistence) concern.

### 10.3 Other Deferred Items

| Item | Reason |
|------|--------|
| Query API (filter, sort, paginate) | Depends on adapter selection |
| Cross-store join queries | Depends on adapter selection |
| Full-text search on evidence content | Depends on adapter selection |
| Time-series queries on PIT fields | Depends on adapter selection |
| Graph traversal (FK chains) | Depends on adapter selection |

---

## 11. Schema-to-Store Derivation

### 11.1 Mechanical Rule

The mapping from M4A schema to canonical store is **derived mechanically** from the M4A metadata — specifically from the `family` letter in `canonical_boundary.py`:

```
Family A  → Identity Store
Family B  → Evidence Store
Family C  → Governance Store
Families D+E+F → Analytics Store
Families G+H+I → Operations Store
```

### 11.2 Derivation Code

The following Python code generates the store mapping mechanically:

```python
"""Mechanical schema-to-store derivation from M4A metadata."""

# Source: canonical_boundary.py
SCHEMA_FAMILIES = {
    # ... (69 entries from canonical_boundary.py)
}

STORE_MAP = {
    "A": "IDENTITY",
    "B": "EVIDENCE",
    "C": "GOVERNANCE",
    "D": "ANALYTICS",
    "E": "ANALYTICS",
    "F": "ANALYTICS",
    "G": "OPERATIONS",
    "H": "OPERATIONS",
    "I": "OPERATIONS",
}

def schema_to_store(schema_id: str) -> str:
    """Return the canonical store name for a given schema_id."""
    family = SCHEMA_FAMILIES[schema_id]
    return STORE_MAP[family]

def store_schemas(store_name: str) -> list[str]:
    """Return all schema IDs belonging to a given store."""
    return [
        sid for sid, fam in SCHEMA_FAMILIES.items()
        if STORE_MAP[fam] == store_name
    ]
```

### 11.3 Verification

| Store | Family | Count | Schemas |
|-------|--------|-------|---------|
| Identity | A | 6 | SM-01, RU-01, SR-01, CR-01, QU-01, CASE-01 |
| Evidence | B | 10 | SRC-01, EV-01, FACT-01, CLM-01, INF-01, HYP-01, CTR-01, EG-01, EAR-01, SRCV-01 |
| Governance | C | 8 | RC-01, RSR-01, IC-01, RB-01, RFR-01, HS-01, IR-01, RSR-02 |
| Analytics | D+E+F | 7+6+8 = 21 | QA-01, MA-01, IE-01, MC-01, CAE-01, MDL-01, MO-02, DR-01, IA-01, CE-01, RM-01, TK-01, FE-01, FF-01, NFF-01, CALC-01, SCEN-01, PLA-01, RDCF-01, VA-01, PIE-01 |
| Operations | G+H+I | 7+7+9 = 23 | RTC-01, AF-01, AG-01, UV-01, PUB-01, FDR-01, CRESP-01, MI-01, MO-01, MASS-01, CL-01, IKR-01, IPR-01, CCV-01, RRM-01, PITC-01, SI-01, RR-01, CLK-01, BU-01, MOD-01, PROV-01, EHR-01 |
| **Total** | | **68** | |

### 11.4 Noncanonical Schemas

The noncanonical set is empty. All 68 M4A schemas are canonical. The Research Room is a logical zone, not a schema family.

---

## Appendix A: Full Store-to-Schema Map

### A.1 Identity Store (6 schemas)

```
SM-01  SecurityMaster
RU-01  ResearchableUniverseRecord
SR-01  SignalRecord
CR-01  CandidateRecord
QU-01  QualityUniverseRecord
CASE-01  CaseRecord
```

### A.2 Evidence Store (10 schemas)

```
SRC-01  SourceRecord
EV-01   EvidenceRecord
FACT-01  FactRecord
CLM-01  ClaimRecord
INF-01  InferenceRecord
HYP-01  HypothesisRecord
CTR-01  ContradictionRecord
EG-01   EvidenceGap
EAR-01  EvidenceAdmissionRecord
SRCV-01  SourceVersion
```

### A.3 Governance Store (8 schemas)

```
RC-01   ResearchCharter
RSR-01  ResearchStageRecord
IC-01   InvestigatorCharter
RB-01   ResearchBudgetRecord
RFR-01  ResearchFailureRecord
HS-01   HypothesisSet
IR-01   InvestigationReport
RSR-02  ResearchStopRecord
```

### A.4 Analytics Store (21 schemas)

```
QA-01   QualityAssessment
MA-01   MoatAssessment
IE-01   IndustryEconomicsRecord
MC-01   ManagementClaim
CAE-01  CapitalAllocationEvent
MDL-01  ManagementDecisionLedger
MO-02   ManagementOutcome
DR-01   DislocationRecord
IA-01   ImpairmentAssessment
CE-01   CompetingExplanation
RM-01   RecoveryModel
TK-01   ThesisKiller
FE-01   FlipEvidence
FF-01   FinancialFact
NFF-01  NormalizedFinancialFact
CALC-01  CalculationRecord
SCEN-01  ScenarioRecord
PLA-01  PermanentLossAssessment
RDCF-01  ReverseDCFRecord
VA-01   ValuationAssessment
PIE-01  PriceImpliedExpectation
```

### A.5 Operations Store (23 schemas)

```
RTC-01  RedTeamChallenge
AF-01   AuditFinding
AG-01   AuditGate (AuditReport)
UV-01   UnderwritingVerdict
PUB-01  PublicationRecord
FDR-01  FounderDecisionReference
CRESP-01  ChallengeResponse
MI-01   MonitoringIndicator
MO-01   MonitoringObservation
MASS-01  MonitoringAssessment
CL-01   CandidateLesson
IKR-01  InstitutionalKnowledgeRecord
IPR-01  IndustryPlaybookRecord
CCV-01  CrossCaseValidation
RRM-01  RunManifestRecord
PITC-01  PITContext
SI-01   ServiceInvocation
RR-01   RetryRecord
CLK-01  CaseLock
BU-01   BudgetUsage
MOD-01  ModelInvocation
PROV-01  ProviderInvocation
EHR-01  EvaluationHarnessRun
```

---

## Appendix B: FK Graph by Store

### B.1 Identity Store FK Targets

| Schema | FK Field | Target | Store |
|--------|----------|--------|-------|
| SM-01 | (none) | — | — |
| RU-01 | entity_id | SM-01 | Identity |
| SR-01 | entity_id | SM-01 | Identity |
| CR-01 | entity_id | SM-01 | Identity |
| CR-01 | signal_ids | SR-01 | Identity |
| QU-01 | entity_id | SM-01 | Identity |
| QU-01 | evidence_ids | EV-01 | Evidence |
| CASE-01 | entity_id | SM-01 | Identity |
| CASE-01 | candidate_id | CR-01 | Identity |

### B.2 Evidence Store FK Targets

| Schema | FK Field | Target | Store |
|--------|----------|--------|-------|
| SRC-01 | (none) | — | — |
| EV-01 | source_id | SRC-01 | Evidence |
| EV-01 | contradicts_ids | EV-01 | Evidence (self) |
| FACT-01 | evidence_id | EV-01 | Evidence |
| CLM-01 | evidence_id | EV-01 | Evidence |
| INF-01 | evidence_ids | EV-01 | Evidence |
| HYP-01 | case_id | CASE-01 | Identity |
| CTR-01 | evidence_ids | EV-01 | Evidence |
| EG-01 | case_id | CASE-01 | Identity |
| EAR-01 | evidence_id | EV-01 | Evidence |
| SRCV-01 | source_id | SRC-01 | Evidence |

### B.3 Governance Store FK Targets

| Schema | FK Field | Target | Store |
|--------|----------|--------|-------|
| RC-01 | case_id | CASE-01 | Identity |
| RC-01 | hypothesis_ids | HYP-01 | Evidence |
| RSR-01 | case_id | CASE-01 | Identity |
| IC-01 | gap_id | EG-01 | Evidence |
| RB-01 | case_id | CASE-01 | Identity |
| RFR-01 | case_id | CASE-01 | Identity |
| HS-01 | case_id | CASE-01 | Identity |
| HS-01 | hypothesis_ids | HYP-01 | Evidence |
| IR-01 | investigator_charter_id | IC-01 | Governance |
| IR-01 | evidence_gap_id | EG-01 | Evidence |
| RSR-02 | case_id | CASE-01 | Identity |

### B.4 Analytics Store FK Targets

| Schema | FK Field | Target | Store |
|--------|----------|--------|-------|
| QA-01 | case_id | CASE-01 | Identity |
| QA-01 | evidence_ids | EV-01 | Evidence |
| MA-01 | case_id | CASE-01 | Identity |
| IE-01 | case_id | CASE-01 | Identity |
| MC-01 | case_id | CASE-01 | Identity |
| MC-01 | source_id | SRC-01 | Evidence |
| CAE-01 | case_id | CASE-01 | Identity |
| MDL-01 | case_id | CASE-01 | Identity |
| MO-02 | case_id | CASE-01 | Identity |
| MO-02 | management_claim_id | MC-01 | Analytics |
| DR-01 | case_id | CASE-01 | Identity |
| IA-01 | case_id | CASE-01 | Identity |
| CE-01 | impairment_id | IA-01 | Analytics |
| RM-01 | case_id | CASE-01 | Identity |
| TK-01 | case_id | CASE-01 | Identity |
| FE-01 | impairment_id | IA-01 | Analytics |
| FF-01 | case_id | CASE-01 | Identity |
| FF-01 | source_id | SRC-01 | Evidence |
| NFF-01 | financial_fact_id | FF-01 | Analytics |
| CALC-01 | case_id | CASE-01 | Identity |
| SCEN-01 | case_id | CASE-01 | Identity |
| PLA-01 | case_id | CASE-01 | Identity |
| RDCF-01 | case_id | CASE-01 | Identity |
| VA-01 | case_id | CASE-01 | Identity |
| VA-01 | r_dcf_id | RDCF-01 | Analytics |
| VA-01 | permanent_loss_id | PLA-01 | Analytics |
| PIE-01 | case_id | CASE-01 | Identity |

### B.5 Operations Store FK Targets

| Schema | FK Field | Target | Store |
|--------|----------|--------|-------|
| RTC-01 | case_id | CASE-01 | Identity |
| AF-01 | audit_id | AG-01 | Operations |
| AG-01 | case_id | CASE-01 | Identity |
| AG-01 | findings | AF-01 | Operations |
| UV-01 | case_id | CASE-01 | Identity |
| UV-01 | red_team_challenge_id | RTC-01 | Operations |
| UV-01 | audit_report_id | AG-01 | Operations |
| PUB-01 | case_id | CASE-01 | Identity |
| PUB-01 | verdict_id | UV-01 | Operations |
| FDR-01 | case_id | CASE-01 | Identity |
| FDR-01 | publication_id | PUB-01 | Operations |
| CRESP-01 | case_id | CASE-01 | Identity |
| CRESP-01 | challenge_id | RTC-01 | Operations |
| MI-01 | case_id | CASE-01 | Identity |
| MO-01 | indicator_id | MI-01 | Operations |
| MASS-01 | case_id | CASE-01 | Identity |
| MASS-01 | indicator_ids | MI-01 | Operations |
| CL-01 | source_case_ids | CASE-01 | Identity |
| IKR-01 | lesson_id | CL-01 | Operations |
| IPR-01 | knowledge_ids | IKR-01 | Operations |
| CCV-01 | lesson_id | CL-01 | Operations |
| CCV-01 | validating_case_ids | CASE-01 | Identity |
| RRM-01 | case_id | CASE-01 | Identity |
| PITC-01 | case_id | CASE-01 | Identity |
| SI-01 | case_id | CASE-01 | Identity |
| RR-01 | invocation_id | SI-01 | Operations |
| CLK-01 | case_id | CASE-01 | Identity |
| BU-01 | budget_id | RB-01 | Governance |
| MOD-01 | case_id | CASE-01 | Identity |
| PROV-01 | case_id | CASE-01 | Identity |
| PROV-01 | model_invocation_ids | MOD-01 | Operations |
| EHR-01 | (none) | — | — |

---

## Appendix C: Immutable-field Policy Summary

### C.1 Schema-Level Immutability

| Policy | Schemas with this Policy |
|--------|--------------------------|
| **RECORD_IMMUTABLE** (entire record never changes) | BU-01, CALC-01, CCV-01, CL-01, CLK-01, CLM-01, FACT-01, INF-01, MOD-01, PROV-01, RR-01, RRM-01, SI-01, SRC-01, SRCV-01, EV-01 (content), CTR-01, EG-01, EAR-01, RFR-01, RSR-02, AF-01, AG-01, UV-01, PUB-01, FDR-01, CRESP-01, MI-01, MO-01, MASS-01, IKR-01, IPR-01, CCV-01, PITC-01, EHR-01, DR-01, IA-01, CE-01, RM-01, TK-01, FE-01, FF-01, NFF-01, SCEN-01, PLA-01, RDCF-01, VA-01, PIE-01, QA-01, MA-01, IE-01, MC-01, CAE-01, MDL-01, MO-02, RC-01, IC-01, IR-01, HS-01 |
| **APPEND_ONLY_STATE** (state transitions only) | CASE-01, CR-01, RU-01, QU-01, RSR-01, RB-01 |

### C.2 Field-Level Immutability

Fields with `FIELD_IMMUTABLE` policy (from `contract_descriptor.json` analysis):

- All PIT fields (`as_of_date`, `entry_timestamp`, `opened_at`, `closed_at`, `completed_at`, `check_timestamp`, `usage_timestamp`, `decision_date`, `outcome_date`...)
- All identity key fields with `FIELD_IMMUTABLE` policy
- Self-referencing FK fields (`contradicts_ids`, `superseded_by_id`)

### C.3 MUTABLE Fields

Fields with `MUTABLE` policy are mostly found in:

- Family G schemas (CRESP-01, AF-01, AG-01) — response fields, notes, resolution fields
- Selected PIT fields in Family D/E schemas (CAE-01, CE-01, MC-01) — outcome tracking, assessment dates

---

## Document Metadata

| Field | Value |
|-------|-------|
| Document ID | QAD-M5.2-PERSISTENCE-BOUNDARY-CONTRACT |
| Version | 1.0 |
| Status | NEW_M5_IMPLEMENTATION_DERIVATION |
| Authority | FD #135 |
| Date | 2026-08-24 |
| Spec Source | QAD-M4A-CANONICAL-SCHEMAS.md (M4A-FROZEN+ERRATUM-001) |
| Schemas Covered | 68 (all canonical) |
| Stores Defined | 5 canonical + 1 Research Room |
| FK References | 87 (from fk_registry.py) |
| Generator | M5.2-20260824 |
| Next Phase | M5.3 (PIT enforcement, retry kernel, query API) |