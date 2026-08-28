# QAD-M5.2 Persistence Boundary Contract

> **Status:** RECONCILIATION — 28 AUG 2026  
> Items 1–8 FOUNDER APPROVED / CLOSED. Item 9 = DOCUMENTATION / PROTOCOL RECONCILIATION ONLY.  
> See also: `QAD-M5.2-CANONICAL-PERSISTENCE-CLOSEOUT.md` (historical closeout, reconciled).
> 
> **Authority:** FD #135; M4A Canonical Schema Registry (FROZEN + Erratum 001)
> **Date:** 2026-08-28
> **Spec Source:** `QAD-M4A-CANONICAL-SCHEMAS.md` (68 frozen schemas, M4A-FROZEN+ERRATUM-001)
> **Generator:** M5.2-20260828
> **Predecessor:** `QAD-M4A-CANONICAL-SCHEMAS.md` (M4A boundary metadata), `qad/contract/canonical_boundary.py`, `qad/contract/fk_registry.py`, `qad/contract/contract_descriptor.json`

---

## Table of Contents

1. [Architecture Overview — M5.2 Five-Anchor Topology](#1-architecture-overview--m52-five-anchor-topology)
2. [The Five Canonical Anchors](#2-the-five-canonical-anchors)
3. [Noncanonical Research Room](#3-noncanonical-research-room)
4. [Identity Key Policy](#4-identity-key-policy)
5. [Version Semantics](#5-version-semantics)
6. [FK Enforcement at Persistence Layer](#6-fk-enforcement-at-persistence-layer)
7. [Transaction Boundaries](#7-transaction-boundaries)
8. [Deterministic Canonical Serialization](#8-deterministic-canonical-serialization)
9. [Reference Adapter Scope](#9-reference-adapter-scope)
10. [Source Hash Distinction](#10-source-hash-distinction)
11. [Deferred to M5.3](#11-deferred-to-m53)
12. [Schema-to-Anchor Derivation](#12-schema-to-anchor-derivation)
13. [Appendix A: Full Anchor-to-Schema Map](#appendix-a-full-anchor-to-schema-map)
14. [Appendix B: FK Graph by Store](#appendix-b-fk-graph-by-store)
15. [Appendix C: Immutable-field Policy Summary](#appendix-c-immutable-field-policy-summary)

---

## 1. Architecture Overview — M5.2 Five-Anchor Topology

The M5.2 persistence boundary defines **five canonical anchors** — distinct store responsibilities — backed by a shared `CanonicalRecordStore` base. The contract separates the canonical domain from any specific storage technology. No production stack is selected here; the contract defines the shape of the persistence boundary that any adapter must satisfy.

### 1.1 Five Anchors

| # | Anchor | Responsibility | Schemas |
|---|--------|---------------|---------|
| 1 | **RawSourceArchive** | Raw source bytes + SRC-01 metadata, content-addressed, versioned, tombstone-aware | SRC-01, SRCV-01 |
| 2 | **EvidenceRegistry** | Evidence admission gate, FK-on-source, immutable-after-admission | EV-01, EAR-01, EG-01, CLM-01, FACT-01, CTR-01, INF-01, HYP-01 |
| 3 | **FinancialFactStore** | Financial facts, normalisation chain, lineage | FF-01, NFF-01, CALC-01, SCEN-01, PIE-01, RDCF-01, PLA-01, VA-01 |
| 4 | **RunManifestStore** | Run manifests and service invocations (pure CR) | RRM-01, SI-01, RR-01, BU-01, MOD-01, PROV-01 |
| 5 | **PITContextStore** | PIT context and case locks (pure CR) | PITC-01, CLK-01 |

**CanonicalRecordStore** is shared base infrastructure — it provides the generic `store()`/`load()`/`contains()`/`get_canonical_hash()`/tombstone semantics for all five anchors. It is NOT a sixth anchor.

Non-anchor canonical schemas (families A, C, D, E, G, H) use the generic `CanonicalRecordStore` via their respective future adapters. The M5.2 scope does not define those adapters — they are mechanically derived from the same base contract.

### 1.2 Protocol Interface

Every canonical store exposes a `Protocol` (structural typing) interface in `qad/persistence/interfaces.py`. The current protocol vocabulary:

| Method | Purpose | Part of |
|--------|---------|---------|
| `store(instance) -> CanonicalHash` | Persist a single canonical record | All stores |
| `store_batch(instances) -> list[CanonicalHash]` | Atomic batch persist | CanonicalRecordStore |
| `load(schema_id, record_id) -> BaseModel` | Retrieve by identity | All stores |
| `contains(schema_id, record_id) -> bool` | Existence check (active reads exclude tombstoned) | CanonicalRecordStore |
| `get_canonical_hash(schema_id, record_id) -> CanonicalHash` | Return stored canonical hash | CanonicalRecordStore |
| `delete(schema_id, record_id) -> None` | Logical tombstone (NOT physical hard delete) | CanonicalRecordStore |
| `delete_batch(pairs) -> None` | Atomic batch tombstone | CanonicalRecordStore |
| `list_ids(schema_id) -> list[RecordID]` | List active record IDs | CanonicalRecordStore |
| `list_all(schema_id) -> list[BaseModel]` | List all active records | CanonicalRecordStore |
| `tombstone(schema_id, record_id, reason, authorizer)` | Explicit tombstone with metadata | CanonicalRecordStore |
| `is_tombstoned(schema_id, record_id) -> bool` | Check tombstone status | CanonicalRecordStore |
| `load_historical(schema_id, record_id) -> BaseModel` | Load regardless of tombstone | CanonicalRecordStore |
| `admit_source(instance, raw_bytes) -> CanonicalHash` | Atomic source admission | RawSourceArchive |
| `store_version(instance, version_label) -> CanonicalHash` | Store a versioned snapshot | RawSourceArchive |
| `load_version(record_id, version_label) -> tuple[BaseModel, bytes\|None]` | Load historical version | RawSourceArchive |
| `list_versions(record_id) -> list[str]` | List version labels | RawSourceArchive |
| `admit_evidence(evidence, admission) -> CanonicalHash` | Atomic evidence admission | EvidenceRegistry |
| `get_lineage(schema_id, record_id) -> list[BaseModel]` | Lineage chain | FinancialFactStore |

**Obsolete vocabulary (removed from current contract):** `save()`, `save_batch()`, `exists()`, `load_by_fk()`, `begin_transaction()`, `commit()`, `rollback()`, `StorePort`.

### 1.3 Adapter Contract

An adapter is any implementation of the store Protocol(s) for a specific schema family. The adapter must:

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
│                      PORT LAYER (Protocols)                       │
│  CanonicalRecordStore (base)                                      │
│  ├── RawSourceArchive    (+admit_source, versioning, tombstone)   │
│  ├── EvidenceRegistry    (+admit_evidence, admission gate)        │
│  ├── FinancialFactStore  (+get_lineage, source authority)         │
│  ├── RunManifestStore    (pure CanonicalRecordStore extension)    │
│  └── PITContextStore     (pure CanonicalRecordStore extension)    │
│  NonCanonicalResearchArtifactStore (separate hierarchy)           │
├──────────────────────────────────────────────────────────────────┤
│                     ADAPTER LAYER                                  │
│  In-memory reference adapter (reference.py) — NON_PRODUCTION      │
│  Future adapters: SQLite, PostgreSQL, DuckDB, etc.                │
├──────────────────────────────────────────────────────────────────┤
│                 PERSISTENCE TECHNOLOGY                             │
│  (Not selected — may be SQL, document store, key-value, etc.)     │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. The Five Canonical Anchors

All 68 M4A schemas are canonical. The five anchors are the stores with distinct responsibilities beyond generic CRUD. Non-anchor schemas use the generic `CanonicalRecordStore` base.

### 2.1 RawSourceArchive (Anchor 1)

**Schemas:** SRC-01, SRCV-01

**Purpose:** Immutable source document storage — atomic metadata+bytes admission, content-addressed, versioned, tombstone-aware. The ONLY entry point for SRC-01. No shadow copies exist in any other store.

| Schema ID | Name | Required FK Targets |
|-----------|------|---------------------|
| SRC-01 | SourceRecord | (none) |
| SRCV-01 | SourceVersion | SRC-01.source_id |

**Admission gate:** `admit_source(instance, raw_bytes)` binds metadata SHA-256(raw_bytes) atomically. Direct `store(SRC-01)` prohibited. `store_batch` containing SRC-01 prohibited. Admitted raw bytes cannot be overwritten. Tombstone preserves historical state.

### 2.2 EvidenceRegistry (Anchor 2)

**Schemas:** EV-01, EAR-01, EG-01, CLM-01, FACT-01, INF-01, HYP-01, CTR-01

| Schema ID | Name | Required FK Targets |
|-----------|------|---------------------|
| EV-01 | EvidenceRecord | SRC-01.source_id, EV-01.evidence_id (self-ref) |
| FACT-01 | FactRecord | EV-01.evidence_id |
| CLM-01 | ClaimRecord | EV-01.evidence_id |
| INF-01 | InferenceRecord | EV-01.evidence_id |
| HYP-01 | HypothesisRecord | CASE-01.case_id |
| CTR-01 | ContradictionRecord | EV-01.evidence_id |
| EG-01 | EvidenceGap | CASE-01.case_id |
| EAR-01 | EvidenceAdmissionRecord | EV-01.evidence_id |

**Purpose:** Canonical evidence objects with admission gate. `admit_evidence()` is the ONLY path for new EV-01+EAR-01. Direct `store(EV-01)` for non-existent evidence rejected. Direct `store(EAR-01)` rejected. Existing admitted EV-01: status/mutable field transitions only. Source FK enforced against authoritative RawSourceArchive. `store_batch` rejects EV-01/EAR-01/SRC-01 as admission bypasses.

### 2.3 FinancialFactStore (Anchor 3)

**Schemas:** FF-01, NFF-01, CALC-01, SCEN-01, PIE-01, RDCF-01, PLA-01, VA-01

| Schema ID | Name | Required FK Targets |
|-----------|------|---------------------|
| FF-01 | FinancialFact | CASE-01.case_id, SRC-01.source_id |
| NFF-01 | NormalizedFinancialFact | FF-01.financial_fact_id |
| CALC-01 | CalculationRecord | CASE-01.case_id |
| SCEN-01 | ScenarioRecord | CASE-01.case_id |
| PIE-01 | PriceImpliedExpectation | CASE-01.case_id |
| RDCF-01 | ReverseDCFRecord | CASE-01.case_id |
| PLA-01 | PermanentLossAssessment | CASE-01.case_id |
| VA-01 | ValuationAssessment | CASE-01.case_id, RDCF-01.r_dcf_id, PLA-01.assessment_id |

**Purpose:** Financial records with lineage support. FF-01.source_id validated against authoritative RawSourceArchive (no shadow copies). Schema-aware `get_lineage(schema_id, record_id)`.

### 2.4 RunManifestStore (Anchor 4)

**Schemas:** RRM-01, SI-01, RR-01, BU-01, MOD-01, PROV-01

| Schema ID | Name | Required FK Targets |
|-----------|------|---------------------|
| RRM-01 | RunManifestRecord | CASE-01.case_id |
| SI-01 | ServiceInvocation | CASE-01.case_id |
| RR-01 | RetryRecord | SI-01.invocation_id |
| BU-01 | BudgetUsage | RB-01.budget_id |
| MOD-01 | ModelInvocation | CASE-01.case_id |
| PROV-01 | ProviderInvocation | CASE-01.case_id, MOD-01.model_invocation_id |

**Purpose:** Run manifests are written once (RECORD_IMMUTABLE). Pure CR extension of CanonicalRecordStore.

### 2.5 PITContextStore (Anchor 5)

**Schemas:** PITC-01, CLK-01

| Schema ID | Name | Required FK Targets |
|-----------|------|---------------------|
| PITC-01 | PITContext | CASE-01.case_id |
| CLK-01 | CaseLock | CASE-01.case_id |

**Purpose:** PIT context records are written once (RECORD_IMMUTABLE). Pure CR extension of CanonicalRecordStore.

**Non-anchor schemas** (families A, C, D, E, G, H — 22 schemas) use the generic `CanonicalRecordStore` via their respective future adapters. Schema-to-anchor derivation is mechanical (see §12).

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

### 4.1 Principles

- The authoritative primary identity field is **derived from generated metadata** in the `primary_id_registry` / M4A-generated schema registry — NOT from a hand-maintained list in this contract.
- Format constraints belong to individual frozen schemas/models. Persistence does not maintain an independent primary-ID registry.
- Illustrative examples below are representative, NOT an authoritative exhaustive list.

### 4.2 Key Type

Record identity fields (`*_id`) are typed as strings in the canonical domain. The format is schema-defined in M4A; most are UUID v7 (time-ordered, 122-bit entropy). The only exception is `CASE-01.case_id` which uses the human-readable format `CASE-YYYY-NNN`.

### 4.3 Generation Policy

- UUID v7 generation must use a cryptographically secure random source.
- The adapter must NOT modify the identity key after generation — keys are set by the domain layer before persistence.
- Keys are immutable once persisted (per `immutable_policy`: `FIELD_IMMUTABLE` or `RECORD_IMMUTABLE`).

### 4.4 Identity Key Fields (illustrative — not authoritative)

The authoritative source is `primary_id_registry` (generated from M4A schema metadata). Common identity key fields include:

- `entity_id` (SM-01, RU-01, QU-01)
- `case_id` (CASE-01, format `CASE-YYYY-NNN`)
- `source_id` (SRC-01)
- `evidence_id` (EV-01)
- Record-specific `*_id` fields per schema

Do NOT treat this list as an exhaustive PK registry. The generated `primary_id_registry` is the single source of truth.

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

### 5.3 Version History (Item 4 Behavior)

The persistence layer implements the following versioning semantics (Item 4, correction):

#### Generic CanonicalRecordStore history

- Prior canonical record auto-preserved where the schema's versioning policy requires it (APPEND_ONLY_STATE / APPEND_ONLY schemas).
- Schema-qualified history keyed by `(schema_id, record_id)`.
- Monotonic version labels: `v0001`, `v0002`, ..., `v0010` (zero-padded numeric ordering).
- Historical access via `load_version(schema_id, record_id, version_label)` retrieves preserved prior versions.
- No silent overwrite of append-only history — when a versioned record is updated, the prior version is preserved in `_versions` before the new write.

#### RawSourceArchive explicit version API

- `store_version(instance, version_label)` — public API for SRC-01 versioned snapshots.
- For SRC-01, `store_version` is **guarded**:
  1. Admitted SRC-01 already exists in the archive.
  2. Raw bytes exist for the source record.
  3. SHA-256(raw_bytes) matches existing SRC-01.content_hash (binding intact).
  4. Incoming canonical payload matches admitted canonical payload (identical-snapshot only).
- `load_version(record_id, version_label) -> tuple[BaseModel, bytes | None]` — retrieves a specific version + its raw blob.
- `list_versions(record_id) -> list[str]` — version labels, newest first.
- `store_version` is NOT simply "the SRCV-01 API" — it enforces metadata-bytes binding integrity. SRCV-01 schema equivalence is established by frozen M4A, not inferred here.

Do NOT conflate generic CanonicalRecordStore version history with RawSourceArchive-specific source-version API. The former is a write-time side-effect; the latter is a first-class versioned snapshot API with guarded admission semantics.

### 5.4 Immutable Record Enforcement

The adapter must:

1. **Reject any UPDATE** on a `RECORD_IMMUTABLE` schema (return `RecordImmutableError`).
2. **Reject any UPDATE** to a `FIELD_IMMUTABLE` field (return `FieldImmutableError`).
3. **Validate state transitions** for `APPEND_ONLY_STATE` fields — only forward enum transitions are accepted.
4. **Logical tombstone** — hard physical delete is FORBIDDEN. The record stays in the store for audit/historical recovery. Active reads exclude tombstoned records. Explicit historical access may retrieve preserved records.

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

Adapters that implement multiple stores (e.g., a single SQL database) must enforce cross-store FK constraints. Adapters that use separate persistence backends per store must implement **application-level FK verification** — required FK targets must resolve before canonical commit.

> **Frozen invariant:** Required FK targets must resolve before canonical commit. Intentional dangling required FKs are NOT permitted, regardless of backend topology. Future distributed implementations may choose coordination technology but may not admit unresolved required FKs.

### 6.5 Self-Referencing FKs

These schemas have self-referencing FKs (contradicts, supersedes):

| Schema | Self-Ref Field | Cardinality | Purpose |
|--------|---------------|-------------|---------|
| EV-01 | `contradicts_ids` | list | Contradicting evidence |
| EV-01 | `superseded_by_id` | single | Superseded evidence |

### 6.6 Deletion Policy

Canonical records are **never physically hard-deleted**. The persistence layer:

1. **Logical tombstone is the ONLY canonical delete operation.** `delete()` / `delete_batch()` mark records as tombstoned — the record's data, canonical hash, and history remain preserved.
2. Active reads (`load`, `contains`, `list_ids`, `list_all`) EXCLUDE tombstoned records.
3. Explicit historical access (`load_historical`, `load_version`) may retrieve preserved records.
4. Tombstone metadata (reason, authorizer, timestamp) is retained per Evidence Doctrine.

> **Inbound-FK deletion guard:** The current reference adapter does NOT implement an automatic inbound-FK tombstone guard (no check that another record references the target before tombstoning). This is a future implementation concern for production adapters. Frozen invariant: FK targets should not be silently tombstoned while active references exist — enforcement mechanism is deferred.

---

## 7. Transaction Boundaries

### 7.1 All-or-Nothing per Store

Each canonical store defines its own transaction boundary. A write to a single store must be atomic:

- **Single record write:** Must succeed or fail atomically.
- **Batch write (same store):** Must succeed or fail atomically. Partial success is not permitted.
- **Cross-store writes:** The application layer (not the adapter) is responsible for coordinating cross-store transactions.

### 7.2 Current Reference Behavior (In-Memory Adapter)

The in-memory reference adapter uses snapshot/restore rollback:

```text
Persistence API prechecks (before Transaction):
  - tombstone rejection
  - duplicate batch identity rejection
  - source/admission authority checks (RawSourceArchive, EvidenceRegistry)
  - instance preparation (SM-01 ticker_history enrichment)

Then Transaction._validate() runs before any mutation:
  - Canonical boundary check (schema_id vs CANONICAL_SCHEMAS)
  - Schema/contract validation (Pydantic model validation)
  - FK existence validation (against FK_REGISTRY)
  - Immutability policy enforcement
  └─ failure → raise; ZERO mutation

Transaction._commit() (after successful validation):
  1. Snapshot captured (deep-copy of entire store state)
  2. Canonical hash computation
  3. Write to internal dict structures
  4. └─ failure → Restore Snapshot → raise
  5. Success
```

Snapshot is captured **AFTER** successful validation and immediately before commit.

Persistence API prechecks (tombstone, duplicate identity, source authority) are
separate from Transaction._validate() — they run before Transaction execution
and protect against admission bypasses.

No Saga, no two-phase commit, no outbox pattern. These are **FUTURE PRODUCTION ADAPTER GUIDANCE** only, not current runtime behavior.

### 7.3 Transactional Guarantees

| Property | Guarantee |
|----------|-----------|
| Atomicity | Per-store write is atomic. Cross-store coordination is application-layer. |
| Consistency | FK constraints validated before commit. Immutability policies enforced before commit. |
| Isolation | **NONE / NOT PROVIDED** (reference adapter). Snapshot/restore rollback mechanism only — no concurrency safety, no database isolation level, no READ_COMMITTED, no SERIALIZABLE. |
| Durability | In-memory reference adapter: No durability (NON_PRODUCTION). Production adapters: durable on commit. |

> **FUTURE PRODUCTION ADAPTER GUIDANCE:** Production adapters must provide at least READ_COMMITTED isolation. The reference adapter is NOT a model for production isolation guarantees.

### 7.4 Failure Semantics

| Failure | Behavior |
|---------|----------|
| Write fails pre-commit | No partial state. Retry is safe. |
| Write fails mid-commit | Snapshot restored — zero partial state. Retry is safe. |
| FK violation | Entire transaction FAILS — zero records committed. |
| Immutability violation | Entire transaction FAILS — zero records committed. |

---

## 8. Deterministic Canonical Serialization

### 8.1 Purpose

Every canonical record must have a **deterministic serialization** — a byte-exact representation that can be hashed, compared, and verified across adapters. This guarantees:

- Reproducible content hashes for evidence integrity.
- Cross-adapter record comparison.
- Idempotent writes (same serialized bytes → same record).

### 8.2 Serialization Contract (Item 8 Correction)

```text
CanonicalSerializer (qad/persistence/serialization.py):
  Input:  Pydantic BaseModel instance
  Output: bytes (compact UTF-8 JSON)

  Rules (Item 8, frozen):
    1. schema_id field serialized FIRST (always top of output)
    2. Remaining top-level fields: deterministic order (alphabetical by field name)
    3. Nested dict keys: deterministic (sorted alphabetically)
    4. List order: PRESERVED as-is (do NOT sort canonical lists)
    5. Explicit None → JSON null (do NOT omit None for normalisation)
    6. Enum → .value (string value, not enum name)
    7. date → ISO 8601 string
    8. datetime → ISO 8601 string in UTC
    9. bytes → hex string
    10. Compact UTF-8 JSON (no whitespace padding)
    11. Unsupported Python values → FAIL CLOSED (TypeError)
    12. No default=str (must fail on unhandled types)
    13. NaN / +Infinity / -Infinity → REJECTED (fail closed)
    14. SHA-256 canonical hash derived from canonical bytes

  NOT part of this contract:
    - Semantic equivalence (different representations of the same value)
    - Normalisation of None (do not strip None for compactness)
    - Recursive list sorting (lists are insertion-order)
```

### 8.3 Content Hash (Legacy — superseded)

The historical §8.3 reference to `content_hash` computed over "content fields only" is superseded.
Use [§10 Source Hash Distinction](#10-source-hash-distinction) for the authoritative treatment.

### 8.4 Serialization Bypass

The Research Room has no serialization contract. Data stored there may use any representation.

---

## 9. Reference Adapter Scope

### 9.1 Reference Adapter

**`qad/persistence/reference.py`** is an **in-memory dict-backed reference adapter**, explicitly labeled:

> **REFERENCE / NON_PRODUCTION**

It is NOT a production persistence backend.

### 9.2 Purpose

1. **Testing** — unit tests for domain logic without database dependencies.
2. **Contract verification** — validate that the Protocol interface is complete and correct.
3. **Prototyping** — rapid iteration on workflows before production adapter selection.

### 9.3 Limitations

| Property | Value |
|----------|-------|
| Backend | In-memory `dict[str, dict[str, _Record]]` |
| FK enforcement | Full (all 87 FKs validated) |
| Immutability enforcement | Full (per M4A metadata) |
| Serialization | Deterministic (per §8) |
| Transactions | In-memory snapshot isolation |
| Durability | **No durability** (data lost on process restart) |
| Concurrency | **No concurrent-access guarantee** |
| Production readiness | **Not a goal** |
| PIT enforcement | Not implemented (deferred) |
| Retry kernel | Not implemented (deferred) |

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

## 10. Source Hash Distinction

**MANDATORY — CONFLATION OF SRC-01.content_hash WITH canonical_hash IS A DEFECT.**

### 10.1 Source Content Hash (SRC-01.content_hash)

```
content_hash = SHA-256(raw source bytes)
```

- Computed over the **original raw source bytes** (web scrape, PDF, API response).
- Bound by `admit_source()`: atomically links `raw_bytes ↔ SHA-256 ↔ SRC-01.content_hash`.
- Purpose: content-addressing, integrity verification against the original source.
- Independent of canonical serialization.

### 10.2 Canonical Record Hash (canonical_hash)

```
canonical_hash = SHA-256(canonical serialized record)
```

- Computed over the **canonical serialized form** of the entire record (per §8 rules).
- Purpose: record-level integrity, idempotent writes, cross-adapter comparison.
- Derived from the deterministic JSON representation.

### 10.3 Relationship

| Property | SRC-01.content_hash | canonical_hash |
|----------|---------------------|----------------|
| Input | Raw source bytes | Canonical serialization of SourceRecord |
| Algorithm | SHA-256 | SHA-256 |
| Changes when | Source bytes change | Any field in SourceRecord changes |
| Binding | `admit_source()` enforces match | Computed on every store() |
| Independence | Independent of record schema | Schema-dependent |

**SRC-01.content_hash** and **canonical_hash** are different hashes with different purposes.
Do NOT conflate them. The canonical hash of a SourceRecord is NOT the source content hash.

### 10.4 SRCV-01 (SourceVersion)

SRCV-01 does NOT have `content_hash` in its frozen M4A schema. Do NOT invent content_hash derivation semantics for SRCV-01. If a version-level content binding is needed, it must be defined contract-specific — do not copy SRC-01 behavior without explicit authorization.

---

## 11. Deferred to M5.3

### 11.1 PIT Enforcement (Point-in-Time Lock)

The M4A specifies PIT semantics for every schema (see `pit_fields` in each schema definition). PIT enforcement is a **cross-cutting concern** that requires:

- A PIT Lock Service (`PITC-01`).
- Query-time filtering to exclude records with `as_of > query_time`.
- Hard-blocking post-AS_OF data in SEALED mode.
- Replay exceptions for evaluation harness.

**Deferred to M5.3** because PIT enforcement is a query-time concern that depends on the adapter's query API, which is not yet defined.

### 11.2 Retry Kernel

The M4A specifies retry semantics (max 3 retries per stage, `RR-01` RetryRecord). The retry kernel is a **service-layer concern** that requires:

- Retry state machine (RETRYING → SUCCEEDED / FAILED / ESCALATED).
- Idempotency guarantees for retried writes.
- Integration with the Run Manifest (RRM-01).

**Deferred to M5.3** because the retry kernel is a service (not a persistence) concern.

### 11.3 Other Deferred Items

| Item | Reason |
|------|--------|
| Query API (filter, sort, paginate) | Depends on adapter selection |
| Cross-store join queries | Depends on adapter selection |
| Full-text search on evidence content | Depends on adapter selection |
| Time-series queries on PIT fields | Depends on adapter selection |
| Graph traversal (FK chains) | Depends on adapter selection |

---

## 12. Schema-to-Anchor Derivation

### 12.1 Explicit Anchor Mapping

The five-anchor mapping is the **explicit reconciled M5.2 persistence mapping**, informed by
frozen M4A schema/family metadata. Family letter alone is NOT a complete derivation rule
because:

- Family B splits into **RawSourceArchive** (SRC-01, SRCV-01) and **EvidenceRegistry** (8 evidence-family schemas)
- Family I splits into **RunManifestStore** (6 manifest schemas) and **PITContextStore** (2 context schemas)
- **FinancialFactStore** uses an explicit financial subset (Family F schemas with lineage/source-authority requirements)

The mapping is:

```
Family B → Anchor-based stores (see §2)
  SRC-01, SRCV-01        → RawSourceArchive
  EV-01, EAR-01, EG-01,   → EvidenceRegistry
  CLM-01, FACT-01, CTR-01,
  INF-01, HYP-01
Families F (financial)    → FinancialFactStore
  FF-01, NFF-01, CALC-01,
  SCEN-01, PIE-01, RDCF-01,
  PLA-01, VA-01
Family I (operations)     → RunManifestStore + PITContextStore
  RRM-01, SI-01, RR-01,
  BU-01, MOD-01, PROV-01
  PITC-01, CLK-01
Families A, C, D, E, G, H → Generic CanonicalRecordStore
  (non-anchor, future adapters)
```

### 12.2 Verification

| Anchor | Family | Count | Schemas |
|--------|--------|-------|---------|
| RawSourceArchive | B | 2 | SRC-01, SRCV-01 |
| EvidenceRegistry | B | 8 | EV-01, EAR-01, EG-01, CLM-01, FACT-01, CTR-01, INF-01, HYP-01 |
| FinancialFactStore | F | 8 | FF-01, NFF-01, CALC-01, SCEN-01, PIE-01, RDCF-01, PLA-01, VA-01 |
| RunManifestStore | I | 6 | RRM-01, SI-01, RR-01, BU-01, MOD-01, PROV-01 |
| PITContextStore | I | 2 | PITC-01, CLK-01 |
| **Non-anchor** | A, C, D, E, G, H | 42 | 42 non-anchor schemas (future adapters) |
| **Total** | | **68** | |

### 12.3 Noncanonical Schemas

The noncanonical set is empty. All 68 M4A schemas are canonical. The Research Room is a logical zone, not a schema family.

---

## Appendix A: Full Anchor-to-Schema Map

### A.1 RawSourceArchive (2 schemas)

```
SRC-01  SourceRecord
SRCV-01  SourceVersion
```

### A.2 EvidenceRegistry (8 schemas)

```
EV-01   EvidenceRecord
FACT-01  FactRecord
CLM-01  ClaimRecord
INF-01  InferenceRecord
HYP-01  HypothesisRecord
CTR-01  ContradictionRecord
EG-01   EvidenceGap
EAR-01  EvidenceAdmissionRecord
```

### A.3 FinancialFactStore (8 schemas)

```
FF-01   FinancialFact
NFF-01  NormalizedFinancialFact
CALC-01  CalculationRecord
SCEN-01  ScenarioRecord
PIE-01  PriceImpliedExpectation
RDCF-01  ReverseDCFRecord
PLA-01  PermanentLossAssessment
VA-01   ValuationAssessment
```

### A.4 RunManifestStore (6 schemas)

```
RRM-01  RunManifestRecord
SI-01   ServiceInvocation
RR-01   RetryRecord
BU-01   BudgetUsage
MOD-01  ModelInvocation
PROV-01  ProviderInvocation
```

### A.5 PITContextStore (2 schemas)

```
PITC-01  PITContext
CLK-01   CaseLock
```

### A.6 Non-Anchor Schemas (42 schemas, future adapters via generic CanonicalRecordStore)

Families A (Identity), C (Governance), D+E (Quality/Moat), G+H (Challenge/Monitoring/Knowledge)

Non-anchor schemas are managed by the generic `CanonicalRecordStore` base. Their M5.2 scope does not define dedicated adapters — those are mechanically derived from the same contract when authorized.

---

## Appendix B: FK Graph by Store

> **NOTE:** The "Store" labels in this appendix (Identity / Evidence / Governance / Analytics / Operations) reflect the M4A family grouping — they are **historical/conceptual grouping**, NOT the current M5.2 store topology. The current M5.2 topology is the five-anchor model in §2. FK targets remain authoritative as declared in `qad/contract/fk_registry.py` (87 FKs across 68 schemas). Anchor-relevant cross-references: EV-01.source_id → SRC-01 (EvidenceRegistry → RawSourceArchive); FF-01.source_id → SRC-01 (FinancialFactStore → RawSourceArchive); EAR-01.evidence_id → EV-01 (self-anchor); RRM-01/SI-01/PITC-01/CLK-01.case_id → CASE-01 (RunManifestStore/PITContextStore → future Identity adapter).

### B.1 Identity Group FK Targets

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
| Version | 2.0 — RECONCILIATION (28 Aug 2026) |
| Status | RECONCILIATION — Items 1–8 CLOSED; Item 9 in progress |
| Authority | FD #135; M4A Canonical Schema Registry (FROZEN + Erratum 001) |
| Date | 2026-08-28 |
| Spec Source | QAD-M4A-CANONICAL-SCHEMAS.md (M4A-FROZEN+ERRATUM-001) |
| Schemas Covered | 68 (all canonical) |
| Anchors Defined | 5 (RawSourceArchive, EvidenceRegistry, FinancialFactStore, RunManifestStore, PITContextStore) |
| FK References | 87 (from fk_registry.py) |
| Generator | M5.2-20260828 |
| Next Phase | M5.3 (PIT enforcement, retry kernel, query API) |
| Predecessor | v1.0 (2026-08-24, NEW_M5_IMPLEMENTATION_DERIVATION) — superseded by this reconciliation |