# QAD-M5.3-IMPLEMENTATION-MAP

> **Authority:** FOUNDER DECISION — QAD M5.3 IMPLEMENTATION (8 Sep 2026, OPTION A — GO)
> **Status:** IMPLEMENTATION MAP (Commit 1 of the M5.3 implementation)
> **Governing baseline:** M5.2 = FOUNDER ACCEPTED / CLOSED / FROZEN · Erratum-002 =
> FOUNDER ACCEPTED / CLOSED / FROZEN · accepted LOCAL regression = 640/640
>
> **Scope discipline (per FD):** M5.3 is a **bounded reference implementation**.
> This is NOT the full §11.3 Query API, NOT a production adapter selection,
> NOT business logic. The burden of proof is on adding query surface, not on
> keeping it small.

---

## 0. FROZEN SOURCES THIS MAP DERIVES FROM

| Component | Frozen authority |
|---|---|
| RR-01 RetryRecord | M4A canonical schemas I-4 (`retry_id` UUID v7, record immutable, max 3 retries per stage → FAILED) |
| SI-01 ServiceInvocation | M4A I-3 (`invocation_id` UUID v7) |
| PITC-01 PITContext | M4A I-1 (`mode` LIVE_CASE_UPDATE / SEALED_HISTORICAL_EVALUATION / REPLAY_EXCEPTION, `as_of_date`) |
| RRM-01 RunManifest | M4A I-2 + Erratum-002 / FD #137 lifecycle (RUNNING→COMPLETED/FAILED, conditional immutability) |
| EV-01 / EAR-01 | M4A B-3 / B-8 + Erratum-002 LIVE carrier (`is_update`/`update_provenance`/`update_pit_context_id` → PITC-01) |
| S8 Retry Controller | M3-SERVICES S8 (bounded retries per stage, max 3, retry from checkpoint, idempotent) |
| PIT nine-case semantics | QAD-M4B `pit-leakage-proof.py` (accepted; NOT reinterpreted here) |
| Five-anchor topology | M5.2 persistence boundary contract §2/§12 (RawSourceArchive, EvidenceRegistry, FinancialFactStore, RunManifestStore, PITContextStore) |

**Pre-implementation gate (confirmed domain rules — verified against frozen
source above before any code):**
- RR-01 records are immutable per attempt; the retry state machine
  (RETRYING → SUCCEEDED / FAILED / ESCALATED) is driven across **distinct
  immutable attempt records**, each with its own `retry_id` (UUID v7).
- Bounded retry = max 3 attempts per stage; after 3 → FAILED (frozen
  validation rule). ESCALATED only with `escalated_to` set.
- Deterministic contract failures (ValidationFailure / IntegrityConflict /
  ImmutabilityViolation / MissingForeignKey) are NOT retried.
- PIT: pre-AS_OF allowed in all modes; SEALED post-AS_OF → HARD BLOCK;
  LIVE post-AS_OF only via the Erratum-002 carrier chain; REPLAY only via
  PITC-01 mode=REPLAY_EXCEPTION + exact `created_by == "FOUNDER"` +
  `exception_reason` present.
- No new canonical schema is required (RR-01/SI-01/RRM-01/PITC-01/EV-01/EAR-01
  all exist). No frozen state machine is changed. No adapter selection.

---

## A. S7 — FILES / INTERFACES / TESTS

### Files
- `qad/m53/__init__.py` — package docstring, re-exports
- `qad/m53/pit_enforcement.py` — `PITVerdict`, `PITEnforcementService`, `PITQueryResult`
- `qad/persistence/errors.py` — **add** `PITBlockError(PersistenceError)` (carries verdict + reason) — the only directly-required interface-surface change outside `qad/m53/`
- `tests/qad/m53/test_pit_enforcement.py` — S7 contract tests

### Interfaces (public)
```
class PITVerdict(Enum):
    ALLOWED
    BLOCKED
    SEAL_INVALIDATED

class PITBlockError(PersistenceError):
    verdict: PITVerdict
    reason: str

@dataclass(frozen=True)
class PITQueryResult:
    records: list[EvidenceRecord]     # PIT-valid, no forbidden leakage
    excluded_count: int               # post-AS_OF excluded from collection
    blocked_count: int                # integrity/seal-invalidated blocked

class PITEnforcementService:
    def __init__(self, *, pitc_store: PITContextStore,
                 evidence_registry: EvidenceRegistry,
                 source_archive: RawSourceArchive,
                 rd_role_token: str = "Research Director",      # frozen SM-12
                 founder_role_token: str = "FOUNDER"): ...

    def adjudicate(self, evidence: EvidenceRecord, pitc: PITContext,
                   ear: EvidenceAdmissionRecord | None) -> PITVerdict

    def query(self, pitc_id: str) -> PITQueryResult             # collection, EV-01 only
    def access(self, evidence_id: str, pitc_id: str) -> EvidenceRecord  # explicit; PITBlockError if forbidden

    # internal:
    def _verify_integrity(self, rec: EvidenceRecord) -> bool    # canonical-hash tamper check
    def _resolve_ear(self, evidence_id: str) -> EvidenceAdmissionRecord | None  # scan EAR-01
```

### Semantics (frozen 9-case, mapped to canonical models)
1. pre-AS_OF (`EV-01.as_of <= PITC-01.as_of_date`) → ALLOWED (all modes)
2. SEALED + post-AS_OF → BLOCKED (hard block, no override)
3. LIVE + post-AS_OF + **no valid carrier** → BLOCKED
4. LIVE + post-AS_OF + valid carrier (EAR-01.is_update ∧ update_provenance ∧
   EAR.update_pit_context_id == PITC.pit_context_id ∧ PITC.mode==LIVE ∧
   PITC.created_by exact RD token) → ALLOWED
5. REPLAY + no provenance (`exception_reason` absent) → BLOCKED
6. REPLAY + `created_by` exact FOUNDER token + `exception_reason` present → ALLOWED
7. Integrity (canonical-hash) mismatch on a sealed record → SEAL_INVALIDATED (block)
8. REPLAY + `created_by` == "Research Director" (not FOUNDER) → BLOCKED
9. REPLAY + spoofed text (`"Founder X"` ≠ exact token) → BLOCKED

**Resolution:** LIVE carrier lookups resolve through the authoritative
EvidenceRegistry (EAR-01) and PITContextStore — the five-anchor authority
pattern closed in Erratum-002 (commit `58096cc`). No registry-local shadow is
consulted. Missing authoritative store → fail closed (BLOCKED).

## B. S8 — FILES / INTERFACES / TESTS

### Files
- `qad/m53/retry_kernel.py` — `RetryableError`, `RetryPolicy`, `RetryOutcome`, `RetryKernel`
- `tests/qad/m53/test_retry_kernel.py` — S8 contract tests

### Interfaces (public)
```
class RetryableError(Exception):
    """Marker for transient, retry-worthy failures (network, rate-limit,
    timeout, 5xx). NOT for deterministic contract failures."""

@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3          # frozen M4A I-4 / S8

@dataclass(frozen=True)
class RetryOutcome:
    invocation_id: str
    attempt_records: list[RetryRecord]   # immutable RR-01 attempt log (0..max)
    status: RetryRecordStatus            # SUCCEEDED / FAILED / ESCALATED
    retried: bool
    error: str | None

class RetryKernel:
    def __init__(self, store: RunManifestStore, *, policy: RetryPolicy | None = None,
                 now: Callable[[], str] | None = None): ...

    def execute(self, invocation: ServiceInvocation, stage, *,
                payload: dict | None = None,
                escalated_to: str | None = None,
                manifest_id: str | None = None) -> RetryOutcome
```

### Semantics (frozen)
- `stage` is a callable `fn() -> None` (raises on failure). The kernel wraps a
  service invocation (SI-01 already stored; RR-01.invocation_id FK requires it).
- Each attempt writes exactly ONE immutable RR-01 (own `retry_id` UUID v7):
  - attempt in-flight → status=RETRYING
  - attempt success → status=SUCCEEDED (terminal for the group)
  - retryable failure with attempts remaining → next attempt
  - attempt budget exhausted → status=FAILED (frozen rule: after 3 → FAILED);
    if `escalated_to` provided → status=ESCALATED + `escalated_to`
- **Idempotency:** repeat `execute` with the same (invocation_id, attempt
  sequence) detects existing RR-01 attempts by (invocation_id, attempt_number)
  and reuses them — no duplicate canonical record. Same payload + same identity
  → same canonical hash. Conflicting payload under an existing attempt identity
  → `IntegrityConflict` (fail closed).
- **Deterministic contract failure** (ValidationFailure / IntegrityConflict /
  ImmutabilityViolation / MissingForeignKey) → NOT retried; single FAILED
  attempt recorded with the actual error class; original exception re-raised.
- **RRM integration:** when `manifest_id` given and the manifest exists with
  `run_state=RUNNING`, the kernel appends the retry `retry_id` reference into
  `RRM-01.failures` (existing list field — integration point). Terminal
  manifests (COMPLETED/FAILED) → rejected (fail closed, no mutation). Final
  manifest state remains governed by the Erratum-002 lifecycle — the kernel
  does NOT finalize manifests.
- No fake completion timestamps; no terminal manifest mutation; no silent
  retry of non-retryable failures.

## C. MINIMUM PIT-AWARE QUERY SUBSTRATE — FILES / INTERFACES / TESTS

- Implemented **inside** `qad/m53/pit_enforcement.py` (S7 section A):
  - `query(pitc_id)` — collection read of EV-01 adjudicated through the PIT
    lock; returns only PIT-valid records + excluded/blocked counts.
  - `access(evidence_id, pitc_id)` — explicit single-record access; forbidden
    evidence raises `PITBlockError` (deterministic) — never an empty result
    pretending the record does not exist.
- **NO** generic `load_where`, filter DSL, sort/paginate framework,
  cross-store SQL joins, full-text search, time-series engine, graph
  traversal, or ORM/DB abstraction layer. Existing `load()`/`contains()`/
  `list_all()` from `CanonicalRecordStore` are the substrate.
- Tests: the S7 test file proves the substrate mechanically (collection
  filtering excludes invalid evidence; explicit forbidden access returns
  PITBlockError; zero forbidden leakage into returned context).

## D. FROZEN AUTHORITIES PER COMPONENT

| Component | Derives from |
|---|---|
| S7 PIT lock (modes, verdicts) | M4A PITC-01 mode enum + M4B pit-leakage-proof 9-case + M5.2 §11.1 |
| S7 LIVE carrier | Erratum-002 / FD #137 (EAR-01 carrier, exact RD token, authoritative store) |
| S7 integrity/seal | M4B pit-leakage-proof TEST 7 (seal-invalidation on tamper) |
| S8 state machine | M4A RR-01 status enum + validation rule (max 3 → FAILED) + M3-SERVICES S8 |
| S8 idempotency | M3-SERVICES S8 idempotency + M5.2 §7.4 failure semantics + IntegrityConflict contract |
| S8 RRM integration | Erratum-002 RRM lifecycle (RUNNING enrichment allowed, terminal immutable) |
| Query substrate restraint | FD #4 (minimum only) + M5.2 §11.3 (explicitly deferred items) |

## E. EXPLICIT DEFERRED ITEMS (§11.3 — NOT in M5.3)

| §11.3 item | Status in M5.3 |
|---|---|
| Query API (filter/sort/paginate) | ❌ DEFERRED — only PIT-filtered EV-01 query built |
| Cross-store join queries | ❌ DEFERRED |
| Full-text search on evidence content | ❌ DEFERRED |
| Time-series queries on PIT fields | ❌ DEFERRED |
| Graph traversal (FK chains) | ❌ DEFERRED |
| Production adapter selection (SQLite/PG/DuckDB) | ❌ NOT AUTHORIZED — reference in-memory only |
| Full M5.3 S7/S8 production hardening | ❌ Scope of this milestone = reference implementation |

## COMMIT STRUCTURE (per FD #13)

1. `docs+errors`: this map + `PITBlockError` interface surface
2. `feat(qad): M5.3 S7` — PIT runtime enforcement + minimum PIT-aware query substrate + tests
3. `feat(qad): M5.3 S8` — retry kernel + RRM integration + tests
4. `docs(qad): M5.3` — closure/proof docs only

Explicit-path staging only. No `git add -A` / `.` / `--all`. Staged diff
inspected before every commit. Diagnostic→fix chronology not applicable here
(FD authorized direct bounded implementation with direct contract tests).

<!-- 2026-09-08 16:50 UTC+7 -->