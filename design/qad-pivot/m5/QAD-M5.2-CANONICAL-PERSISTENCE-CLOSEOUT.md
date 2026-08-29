# QAD-M5.2 Canonical Persistence Closeout

> **Status:** M5.2 = FINAL / CANONICAL-PERSISTENCE-CONFORMANT
> **Authority:** FD #135; M4A Canonical Schema Registry (FROZEN + Erratum 001)
> **Baseline:** `03ba6e27ad195b69ce4b243476f8121d92c9a19f` (M5.1 closed)
> **M5.2 Implementation Baseline:** recorded by git history
>
> **Design principle:** Persistence boundaries enforce what becomes machine truth.
> NotebookLM / Deep Research is NONCANONICAL until validated against original sources.
> All canonicality derives from M5.1 generated metadata — never hand-written lists.

---

## ⚠ RECONCILIATION NOTICE — 28 AUG 2026

This document records the **original M5.2 persistence closeout state** (24 Aug 2026).
Founder-directed correction Items 1–8 (25–28 Aug 2026) subsequently superseded several
technical statements.

**Current authoritative operational state:** `PROJECT_STATE.md`.

**Governance update (29 Aug 2026):**
- M5.2 = CORRECTION IN PROGRESS
  - Items 1-12 FOUNDER APPROVED / CLOSED (Item 12 FOUNDER APPROVED 29 Aug 2026)
  - Item 13 = CROSS-CONTRACT TEST CLOSURE COMPLETE / READY FOR FOUNDER APPROVAL / NOT CLOSED
  - Item 14 = pending
- M5.3 = HOLD

### Superseded sections — reconcile as follows

| Section | Original claim | Current interpretation |
|---------|---------------|----------------------|
| §4 Identity | "All identity fields are M4A-defined UUID v7 represented as str" | **Authoritative primary identity FIELD derived from generated primary_id_registry / frozen M4A metadata.** Identity formatting is schema-specific. No hand-maintained universal UUID rule. Persistence does not maintain an independent primary-ID registry. |
| §7 Transaction | Transaction.begin() → validate phase (FK, canonical, immutability, serialization+hash) → commit; no Saga/2PC/Outbox | **serialization/hash placement and implementation details superseded by Item-2/current Transaction behavior.** Current: Persistence API prechecks (tombstone, duplicate identity, authority) → Transaction._validate() → snapshot → commit → [fail → restore]. Serialization+hash computed during commit, not during validation. Saga/2PC/Outbox were never in this closeout doc — those were a Boundary Contract claim. |
| §8 Serialization | schema_id first, alphabetical fields, enum values → string, dict sorted keys, **list sorted** elements, **None excluded**, compact JSON, SHA-256 | **list order PRESERVED** (no sort); **explicit None → JSON null** (do not omit for normalisation); fail closed on unsupported types; **no default=str**; NaN/+Infinity/-Infinity rejected. Source content_hash distinction belongs to Boundary Contract reconciliation (§10), not the historical closeout §8 claim. |
| §9 Reference adapter | InMemoryBlobStore + NonCanonicalResearchArtifactStore listed; anchor adapters not yet listed | Current anchor adapter inventory: **InMemoryRawSourceArchive, InMemoryEvidenceRegistry, InMemoryFinancialFactStore, InMemoryRunManifestStore, InMemoryPITContextStore** plus generic infrastructure. Historical §9 is preserved as-is above. |
| §11 Test results | **401/401** (historical at original closeout) | **589/589 LOCAL pytest PASS** (after Item 11, 29 Aug 2026; NOT independent CI). Prior: 577/577 after Item 8 (28 Aug). |
| Governance | M5.2 = FINAL / CANONICAL-PERSISTENCE-CONFORMANT; M5.3 = PROCEED | **M5.2 = CORRECTION IN PROGRESS**; Items 1-12 CLOSED; Item 13 CROSS-CONTRACT TEST CLOSURE COMPLETE / READY FOR FOUNDER APPROVAL / NOT CLOSED; Item 14 pending; **M5.3 = HOLD**. Production Release / Live Autonomous QAD remains NOT AUTHORIZED. |

### Historical preservation

The original test counts below are **HISTORICAL AT ORIGINAL CLOSEOUT (24 AUG 2026).**
Do NOT replace with current counts as if the latter existed during the original closeout.

**Current (29 Aug 2026):** 589/589 LOCAL pytest PASS after Items 1-11. Item 12 = documentation-only update; no test delta. Prior: 577/577 after Item 8 (28 Aug). Not independent CI.

---

## 0. M5.2 Scope

M5.2 implements the persistence boundary layer for the five canonical anchors:

```text
1. Raw Source Archive        (SRC-01 SourceRecord)
2. Canonical Evidence Registry (EV-01 EvidenceRecord)
3. Financial Fact Store      (FF-01 FinancialFact + NFF normalization chain)
4. Research Run Manifest     (RRM-01 ResearchRunManifest)
5. PIT Context               (PITC-01 PITContext)
```

**Not in M5.2 scope:**
- PIT runtime enforcement (M5.3)
- Retry/reliability kernel (later M5 stage)
- Full role/service orchestration
- Production database selection
- Production deployment readiness

---

## 1. Architecture

```
qad/persistence/
├── __init__.py          — Package init, public API exports
├── errors.py            — 9 typed persistence error classes
├── interfaces.py        — Protocol classes (ports)
├── serialization.py     — Deterministic canonical serialization
├── fk_enforcer.py       — FK existence validation from FK_REGISTRY
├── immutability.py      — Immutability policy from contract descriptor
├── transaction.py       — Atomic transaction boundary
└── reference.py         — In-memory reference adapter (NON_PRODUCTION)
```

### Architecture Pattern

```text
Ports (interfaces.py)          ← contracts define what
Adapters (reference.py)        ← in-memory reference implementation
Enforcement (fk_enforcer.py,   ← cross-cutting concerns
             immutability.py,
             transaction.py)
Serialization layer             ← deterministic byte representation
```

### Backend-Agnostic Design

All stores accept M5.1 Pydantic model instances. The persistence layer never
creates a second schema definition. The reference adapter is explicitly labeled
`REFERENCE / NON_PRODUCTION` to prevent accidental production use.

---

## 2. Canonical Stores vs Schema Mapping

| Store | M4A Schemas Served | Family | FK Count |
|---|---|---|---|
| RawSourceArchive | SRC-01, SRCV-01 | B | 0 |
| CanonicalEvidenceRegistry | EV-01, EAR-01, EG-01, CLM-01, FACT-01, CTR-01, INF-01, HYP-01 | B | 25 |
| FinancialFactStore | FF-01, NFF-01, CALC-01, SCEN-01, PIE-01, RDCF-01, PLA-01, VA-01 | F | 16 |
| RunManifestStore | RRM-01, SI-01, RR-01, BU-01, MOD-01, PROV-01 | I | 10 |
| PITContextStore | PITC-01, CLK-01 | I | 2 |

Store-to-schema derivation is **mechanical**: every M4A schema is assigned by
reading its `schema_id`, `family`, and FK metadata from the generated contract
descriptor. No hand-maintained lists.

---

## 3. Noncanonical Research Room

`NonCanonicalResearchArtifactStore` is structurally separate from all canonical
stores. It:

- Has NO shared `store()` / `load()` API surface with canonical stores
- Cannot be queried as canonical evidence
- Accepts any Pydantic model (no schema_id check)
- Is explicitly NOT persisted as machine truth

This prevents accidental promotion of NotebookLM / Deep Research / LLM synthesis
to canonical evidence status.

---

## 4. Identity Keys

All identity fields (`*_id`) are M4A-defined UUID v7 represented as `str`.
The persistence layer does not generate IDs — the caller provides them.

Identity uniqueness is enforced per schema_id namespace. Same `(schema_id, record_id)`
is unique.

---

## 5. Immutability Enforcement

| M4A Policy | Persistence Behavior | Enforcement |
|---|---|---|
| RECORD_IMMUTABLE | All fields frozen after admission | Same ID + changed payload → IntegrityConflict |
| FIELD_IMMUTABLE | Specific fields frozen | Update violating frozen fields → ImmutabilityViolation |
| MUTABLE | Fields may be updated | Allowed within transaction |
| APPEND_ONLY | New version/revision on change | Prior version preserved; new version created |
| CONDITIONAL_IMMUTABLE | Not enforced in M5.2 (M5.3) | Noted; deferred |

Same ID + byte-identical payload = **IDEMPOTENT NO-OP** (no error).

---

## 6. FK Enforcement

All 87 M4A FK definitions are consumed from the generated `FK_REGISTRY`.

| FK Mode | Enforcement |
|---|---|
| Single FK | Target record must exist in store or same transaction batch |
| Collection FK | ALL members must exist |
| Same-batch resolution | FK target may be in the same validated transaction |
| Missing FK target | **Entire transaction FAILS** — zero records committed |

FK enforcement is schema_id-aware: it resolves FK target schemas via
`FK_REGISTRY[source_schema_id]` and validates against stored records.

---

## 7. Transaction Semantics

```text
Transaction.begin()
  → validate() phase:
      FK existence checks
      Canonical boundary checks
      Immutability/revision checks
      Serialization + hash
  → If ANY check fails:
      → TransactionFailure raised
      → ZERO records committed
  → If ALL checks pass:
      → Batch commit (all writes atomically)
```

No partial commit is possible. The in-memory reference adapter achieves this
via a private working dict that is only merged on successful execution.

---

## 8. Deterministic Serialization

Canonical serialization rules:
- Stable field ordering: `schema_id` first, then alphabetical by field name
- UTF-8 encoding
- Enum values → string value (not enum name)
- dict → sorted keys recursively
- list → sorted elements recursively (where order is semantically undefined)
- `None` values excluded (Optional fields not present)
- Output: JSON without whitespace, then SHA-256 hash

Round-trip: Pydantic model → canonical bytes → load → same model semantics ✅

---

## 9. Reference Adapter

`qad/persistence/reference.py` — in-memory dict-backed reference adapter.

**Label:** `REFERENCE / NON_PRODUCTION`

Supported stores:
- `InMemoryCanonicalRecordStore` — generic canonical store
- `InMemoryBlobStore` — content-addressable raw bytes
- `InMemoryRawSourceArchive` — source records + content-addressable blobs
- `InMemoryNonCanonicalResearchArtifactStore` — isolated noncanonical room
- (Concrete EvidenceRegistry, FinancialFactStore adapters use CanonicalRecordStore)

Limitations:
- No disk persistence (lost on restart)
- No concurrent access
- No production query optimization
- Not suitable for production deployment

---

## 10. Error Types (qad/persistence/errors.py)

| Error | Description |
|---|---|
| PersistenceError | Base error |
| ValidationFailure | Model validation failed |
| CanonicalBoundaryViolation | Non-canonical schema rejected from canonical store |
| IntegrityConflict | Same ID + different canonical payload |
| MissingForeignKey | FK target not found |
| ImmutabilityViolation | Update violates immutability policy |
| HashMismatch | Content hash does not match expected |
| TransactionFailure | Atomic transaction rolled back |
| NonCanonicalAdmissionRejected | Direct admission of noncanonical content rejected |

---

## 11. Test Results

| Test Area | Count | Result |
|---|---|---|
| Basic CRUD round-trip | 3 tests | PASS |
| Deterministic serialization | 2 tests | PASS |
| Immutability enforcement | 4 tests (mutable, FIELD_IMMUTABLE, RECORD_IMMUTABLE, idempotent) | PASS |
| FK enforcement | 4 tests (missing, valid, collection, same-batch) | PASS |
| Integrity conflict | 1 test (same ID different payload) | PASS |
| BlobStore content-addressability | 2 tests | PASS |
| NonCanonical isolation | 2 tests | PASS |
| Transaction rollback | 1 test | PASS |
| List/delete by schema | 1 test | PASS |
| PITContext + RunManifest round-trip | 2 tests | PASS |
| Financial Fact lineage | 1 test | PASS |
| **Total M5.2 persistence tests** | **60/60 PASS** | |
| **QAD conformance tests (M5.1 + M5.2)** | **165/165 PASS** | |
| **Full pytest** | **401/401 QAD+M5.2+core (1 pre-existing unrelated Live Office failure)** | |
| | | |
| **Historical at original closeout (24 Aug 2026).** | | |
| *Current (28 Aug 2026, Items 1-8):* | *577/577 LOCAL pytest PASS* | *Not independent CI* |
| *Current (29 Aug 2026, Items 1-11):* | *589/589 LOCAL pytest PASS (Item 12 = documentation-only update; no test delta)* | *Not independent CI* |

---

## 12. Deferred to M5.3

```text
PIT mode enforcement
  → SEALED_HISTORICAL_EVALUATION leakage prevention
  → LIVE_CASE_UPDATE policy
  → REPLAY_EXCEPTION authorization

CONDITIONAL_IMMUTABLE runtime enforcement
  → "Manifest immutable after completion"
  → "Charter immutable after BUDGET_APPROVED"

Production database selection
Full retry/reliability kernel
Complete role/service orchestration
```

M5.2 provides the persistence primitives these need (immutability enforcement,
atomic transactions, FK integrity) but does not implement the policy layer.

---

## 13. Legal / Governance

```text
M5.1 = FINAL / CONTRACT-CONFORMANT — CLOSED

M5.2 = CORRECTION IN PROGRESS
  Items 1-12 FOUNDER APPROVED / CLOSED (Item 12 29 Aug 2026)
  Item 13 = CROSS-CONTRACT TEST CLOSURE COMPLETE / READY FOR FOUNDER APPROVAL / NOT CLOSED
  Item 14 = pending

M5.3 = HOLD

Production Release = NOT AUTHORIZED
Live Autonomous QAD = NOT AUTHORIZED

Governance note (29 Aug 2026 reconciliation):
  This closeout document is a HISTORICAL artifact.  The original
  "M5.2 = FINAL / CANONICAL-PERSISTENCE-CONFORMANT" and
  "M5.3 = PROCEED UNDER FD #135" statements are superseded
  by the correction Items 1–11.  See RECONCILIATION NOTICE above.

Item-9 documentation/protocol reconciliation (Founder 28 Aug 2026):
  Item 9 = FOUNDER APPROVED / CLOSED.
  Five-anchor persistence documentation/protocol reconciliation completed.
  Generated primary-ID authority, transaction/current tombstone/version/serialization
  truth reconciled.  SRC-01.content_hash kept distinct from canonical record hash.
  Item 9 introduced NO new runtime persistence behavior — existing guards
  were documented rather than recreated.

Item-12 documentation truth update (Founder 29 Aug 2026):
  Item 12 = FOUNDER APPROVED / CLOSED / FROZEN.
  Historical closeout chronology preserved (original 24 Aug marker retained;
  separate reconciliation marker added).
  Item 9 explicit closure record, Item 10 waiver, Item 11 fail-closed truth
  all documented.
  Historical test counts (401/401, 577/577) preserved as historical evidence.
  Current test metric = 589/589 LOCAL pytest PASS (NOT independent CI).
  PROJECT_STATE temporal layers (historical vs current) correctly separated.
  No production/runtime/test/schema behavior changed under Item 12.
  4 documentation commits preserved (no squash/rewrite).

Item-13 cross-contract test closure (29 Aug 2026):
  Item 13 = CROSS-CONTRACT TEST CLOSURE COMPLETE /
            READY FOR FOUNDER APPROVAL /
            NOT CLOSED.
  8 structural bridge tests created (tests/qad/test_cross_contract_validation.py).
  No production code, M4A/M4B, or M5.3 policy changed.
  Tests cover M4B PIT-mode vocabulary, evaluation types, fixture identities,
  source-hash carrier, evidence references, AS_OF_DATE structural bridge,
  evaluation-label enum counterparts, and M5.3-deferred boundary verification.
  No cross-contract contradiction found.
  Full LOCAL regression: 597/597 PASS (589 baseline + 8 new).

Item-10 waiver (Founder 28 Aug 2026):
  Historical Live Office failure provenance was unrecoverable.
  Founder waived the requirement to reproduce the exact historical
  root cause; only the provenance requirement is waived.
  Current regression requirement is NOT waived.

Item-11 runtime fail-closed truth (Founder 29 Aug 2026):
  Canonical primary-ID resolution (reference._resolve_id() and
  Transaction._record_id()) now FAILS CLOSED when authoritative
  mapping/value is unavailable.  Heuristic FK fallback and synthetic
  identity generation removed.  Two-layer design:
  Layer 1 — wrong-but-present mapping → independent M4A oracle fails.
  Layer 2 — mapping missing/unavailable → runtime PersistenceError.
  38/38 Item-11 negative requirements covered.
```

<!-- 2026-08-24 -->
<!-- reconciliation updated 2026-08-29 -->