# QAD-M3 Service Contracts

> **Status:** M3 FINAL — FROZEN FOR M4 DERIVATION
> **Authority:** FD #130; Frozen Architecture; M3-01 (QAD Operating Model §7 Reliability)
> **Traceability:** M3-01 §7 (Reliability Contract) · M3-ROLES §5 (Service Registry) · FD #130 · NEW_M3_DERIVATION (service contract format, failure semantics, PIT modes)

---

## Service Contract Template

Every service below uses this schema:

```text
service_id
classification            (P = POLICY_SERVICE, D = DETERMINISTIC, I = INFRASTRUCTURE)
deterministic_or_policy_governed
inputs
outputs
persistent_state
owner
authority
failure_behavior
retry_behavior
idempotency
logging
provenance
PIT_behavior
forbidden_inference
downstream_dependencies
```

---

## S1: Autonomous Selection Engine

| Field | Value |
|-------|-------|
| **service_id** | S1 |
| **classification** | P (POLICY_SERVICE) |
| **deterministic_or_policy_governed** | Policy-governed — applies approved selection rules deterministically. AI judgment is NOT involved in selection state assignment. |
| **inputs** | CANDIDATE_REGISTRY entries, selection policy rules (approved thresholds, exclusion criteria, watch criteria) |
| **outputs** | Selection state: `AUTO_RESEARCH_NOW / WATCH_PRICE / WATCH_EVIDENCE / DATA_LIMITED_WATCH / REJECT` |
| **persistent_state** | Stateless per-candidate evaluation. State stored in CANDIDATE_REGISTRY. |
| **owner** | Discovery & Coverage System |
| **authority** | Assign selection state per approved policy. Cannot override policy. |
| **failure_behavior** | **System/service failure must NOT produce `SKIP` or `REJECT`.** Use `SELECTION_ERROR` or `EVALUATION_UNAVAILABLE`. Candidate remains in pending state, flagged for retry or operator attention. A technical failure must never silently create a Type-B discovery miss. |
| **retry_behavior** | Max 3 retries with exponential backoff. After 3 failures → `SELECTION_ERROR` with documented reason. Operator attention required. |
| **idempotency** | Same candidate + same policy version → same output. Deterministic. |
| **logging** | Every selection evaluation: `{candidate_id, policy_version, input_signals, output_state, timestamp, rule_fired}` |
| **provenance** | Full provenance: policy version, data version, signal versions, evaluator |
| **PIT_behavior** | Evaluation uses point-in-time data as of the candidate's as-of date. Never uses future data. |
| **forbidden_inference** | ❌ Must NOT infer quality, impairment, or valuation ❌ Must NOT use AI judgment ❌ Must NOT invent new selection rules ❌ Must NOT score or rank candidates (selection state only) |
| **downstream_dependencies** | CANDIDATE_REGISTRY (write state), CASE_REGISTRY (trigger AUTO_RESEARCH_NOW → Case Open) |

---

## S2: Research Budget Controller

| Field | Value |
|-------|-------|
| **service_id** | S2 |
| **classification** | P (POLICY_SERVICE) |
| **deterministic_or_policy_governed** | Policy-governed — applies approved budget policy deterministically. |
| **inputs** | Research Budget policy, case budget request (from Research Director), case scope |
| **outputs** | Budget approval or denial; budget exhaustion → `INCOMPLETE` (not weakened quality gate) |
| **persistent_state** | Per-case budget allocation, cumulative spend |
| **owner** | Research Operations |
| **authority** | Approve/deny budget requests within policy. May reject requests exceeding policy limits. |
| **failure_behavior** | Budget system unavailable → case cannot open until restored. Budget exhausted → `INCOMPLETE`, not weakened quality. |
| **retry_behavior** | Retry budget request on system failure (max 3). Budget exhaustion is NOT retryable. |
| **idempotency** | Same case + same request → same budget allocation. Spend tracking is append-only. |
| **logging** | `{case_id, request_amount, approved_amount, cumulative_spend, policy_version, timestamp}` |
| **provenance** | Budget decisions record policy version, approver, timestamp |
| **PIT_behavior** | Budget is evaluated at request time against current policy. |
| **forbidden_inference** | ❌ Must NOT judge research quality ❌ Must NOT override budget policy without Founder authorization ❌ Must NOT weaken quality gates |
| **downstream_dependencies** | CASE_REGISTRY (budget → case open), Research stages (spend tracking) |

---

## S3: Security / Entity Resolution

| Field | Value |
|-------|-------|
| **service_id** | S3 |
| **classification** | D (DETERMINISTIC) |
| **deterministic_or_policy_governed** | Deterministic — pure computation, no judgment. |
| **inputs** | Raw entity identifiers (ticker, CIK, name, exchange, ISIN, SEDOL) |
| **outputs** | Resolved entity identity: `{entity_id, tickers[], cik, name, exchange, share_class, adr_flag, status}` |
| **persistent_state** | SECURITY_MASTER registry (authoritative entity identity) |
| **owner** | Discovery & Coverage System |
| **authority** | Resolve entity identity deterministically. Update SECURITY_MASTER on corporate actions. |
| **failure_behavior** | Unresolvable entity → documented exclusion with reason. Never silent omission. `ENTITY_UNRESOLVED` state. |
| **retry_behavior** | Retry on transient failure (3×). Permanent failure → operator attention. |
| **idempotency** | Same identifier → same resolved entity. Corporate actions cause versioned updates. |
| **logging** | `{input_identifier, resolved_entity_id, resolution_method, confidence, timestamp}` |
| **provenance** | Resolution method, source, data version recorded |
| **PIT_behavior** | Entity resolution is as-of the query date. Historical ticker/name changes preserved. |
| **forbidden_inference** | ❌ Must NOT assess quality ❌ Must NOT filter by entity type except hard exclusion list (FD #130) ❌ Must NOT rank entities |
| **downstream_dependencies** | SECURITY_MASTER (persistent), RESEARCHABLE_UNIVERSE, SIGNAL_REGISTRY, CANDIDATE_REGISTRY |

---

## S4: Canonical Evidence Registry

| Field | Value |
|-------|-------|
| **service_id** | S4 |
| **classification** | I (INFRASTRUCTURE) |
| **deterministic_or_policy_governed** | Deterministic storage and retrieval. Evidence admission is policy-governed (Evidence Lead role). |
| **inputs** | Evidence objects (FACT/CLAIM/INFERENCE/HYPOTHESIS) with full provenance, source references |
| **outputs** | Validated, curated evidence records with status, lineage, and contradiction tracking |
| **persistent_state** | Append-only evidence store. Entries never deleted; only superseded or retracted. |
| **owner** | Evidence Intelligence Lead (Role 2) |
| **authority** | Store evidence deterministically. Status transitions require authorized role. |
| **failure_behavior** | Write failure → evidence quarantined; retry on next tick. Read failure → service unavailable. |
| **retry_behavior** | Write retry 3×; quarantine after 3 failures. |
| **idempotency** | Same evidence_id + same content → same record (no duplicate). Status transitions are idempotent. |
| **logging** | Every admission, status change, and query logged with timestamp and actor |
| **provenance** | Full provenance: source_id, extractor, admitting_role, validation_status, PIT, contradictions |
| **PIT_behavior** | Every evidence entry carries its as-of timestamp. Historical queries filter by PIT. |
| **forbidden_inference** | ❌ Must NOT judge evidence quality ❌ Must NOT filter evidence by source tier alone ❌ Must NOT suppress contradictions ❌ Must NOT admit L10 as sole material support |
| **downstream_dependencies** | Evidence Graph, Analytical State, Publication, Audit |

---

## S5: Raw Source Archive

| Field | Value |
|-------|-------|
| **service_id** | S5 |
| **classification** | I (INFRASTRUCTURE) |
| **deterministic_or_policy_governed** | Deterministic — immutable storage. |
| **inputs** | Source documents (SEC filings, PDFs, web pages, data files) |
| **outputs** | Immutable source file with content hash, timestamp, source_id, retrieval metadata |
| **persistent_state** | Append-only store. Content never edited in place. Removal requires tombstone (EVIDENCE-DOCTRINE). |
| **owner** | Evidence Intelligence Lead (Role 2) |
| **authority** | Store raw sources immutably. |
| **failure_behavior** | Source unreachable → skip, document gap. An unreachable material source must produce a visible evidence gap and may force `INCOMPLETE`; must not silently become sufficient research. |
| **retry_behavior** | Retry 3× with backoff. After 3 failures → `SOURCE_UNAVAILABLE` with reason. |
| **idempotency** | Same source URL + same retrieval date → same archive entry (deduplicated). |
| **logging** | `{source_id, retrieval_date, url, content_hash, file_size, status}` |
| **provenance** | Retrieval date, source URL, content hash, retrieval method |
| **PIT_behavior** | Retrieval timestamp is the authoritative as-of for the source. Re-retrieval creates a new version. |
| **forbidden_inference** | ❌ Must NOT interpret source content ❌ Must NOT filter or transform ❌ Must NOT delete without tombstone |
| **downstream_dependencies** | Canonical Evidence Registry (S4), Evidence Graph |

---

## S6: Run Manifest Service

| Field | Value |
|-------|-------|
| **service_id** | S6 |
| **classification** | I (INFRASTRUCTURE) |
| **deterministic_or_policy_governed** | Deterministic — record-keeping. |
| **inputs** | Research run metadata (case_id, version, as_of, models, providers, prompts, sources, calculations, retries, failures) |
| **outputs** | Run manifest record (research_run_id, all run metadata) |
| **persistent_state** | Append-only. Run start record created even if run fails (partial manifest). |
| **owner** | Research Operations |
| **authority** | Record run metadata deterministically. |
| **failure_behavior** | Manifest write failure → run logged as error; retry on next tick. |
| **retry_behavior** | Retry 3×. |
| **idempotency** | Same research_run_id → same record (no duplicate). |
| **logging** | All manifest fields logged |
| **provenance** | Full provenance: model versions, provider, prompt hashes, source versions, calculation versions |
| **PIT_behavior** | Manifest records point-in-time as_of_date. Historical evaluation uses manifest as PIT anchor. |
| **forbidden_inference** | ❌ Must NOT interpret run results ❌ Must NOT modify manifest after creation |
| **downstream_dependencies** | Evaluation Harness (S11), Audit, Knowledge Steward |

---

## S7: Point-in-Time Lock

| Field | Value |
|-------|-------|
| **service_id** | S7 |
| **classification** | D (DETERMINISTIC) |
| **deterministic_or_policy_governed** | Deterministic — PIT evaluation. |
| **inputs** | Case AS_OF_DATE, evidence timestamps, source timestamps, evaluation mode |
| **outputs** | PIT-validated evidence context; mode-specific behavior |
| **persistent_state** | Stateless (query-time evaluation) |
| **owner** | Research Operations |
| **authority** | Enforce PIT discipline per mode. |
| **failure_behavior** | PIT service unavailable → queries blocked (fail closed). No PIT-unchecked evidence access. |
| **retry_behavior** | Retry 3×. |
| **idempotency** | Same PIT query → same result. |
| **logging** | `{case_id, mode, as_of_date, evidence_count_pre, evidence_count_post, timestamp}` |
| **provenance** | PIT mode, as_of_date, evaluating role |
| **PIT_behavior** | Three explicit modes: |
| | **LIVE_CASE_UPDATE** — post-AS_OF evidence allowed only as explicitly tagged `UPDATE` with provenance |
| | **SEALED_HISTORICAL_EVALUATION** — post-AS_OF evidence HARD BLOCKED. No future-information leakage. |
| | **REPLAY_EXCEPTION** — explicit, provenance-recorded exception for replay/re-evaluation |
| **forbidden_inference** | ❌ Must NOT admit post-AS_OF evidence without explicit mode tag ❌ Must NOT allow SEALED mode to be bypassed |
| **downstream_dependencies** | All analytical services, Evaluation Harness (S11) |

---

## S8: Retry / Research Execution Controller

| Field | Value |
|-------|-------|
| **service_id** | S8 |
| **classification** | I (INFRASTRUCTURE) |
| **deterministic_or_policy_governed** | Deterministic — execution control. |
| **inputs** | Research stage execution request, retry policy, budget state |
| **outputs** | Stage execution, retry scheduling, failure disposition |
| **persistent_state** | Per-case stage execution state (NOT_STARTED/IN_PROGRESS/COMPLETE/FAILED/INCOMPLETE/SKIPPED) |
| **owner** | Research Operations |
| **authority** | Execute research stages; manage retries; enforce stage ordering |
| **failure_behavior** | Stage FAILED → max 3 retries. After 3 → stage marked `FAILED`. Case continues with documented failure. |
| **retry_behavior** | Bounded retries per stage (max 3). Retry from last checkpoint; previous stage output preserved. |
| **idempotency** | Same stage + same case version → same execution (checkpoint replay). |
| **logging** | `{case_id, stage, attempt, status, checkpoint, duration, error}` |
| **provenance** | Stage execution record, checkpoint references |
| **PIT_behavior** | Stage execution uses case AS_OF_DATE for all data queries. |
| **forbidden_inference** | ❌ Must NOT skip stages ❌ Must NOT allow non-Founder stage skip ❌ Must NOT weaken quality gates on budget exhaustion |
| **downstream_dependencies** | All research stages, Case Registry |

---

## S9: Case Locking / Idempotency

| Field | Value |
|-------|-------|
| **service_id** | S9 |
| **classification** | D (DETERMINISTIC) |
| **deterministic_or_policy_governed** | Deterministic — locking and deduplication. |
| **inputs** | Case ID, case version, request type (open/modify/close) |
| **outputs** | Lock/unlock state; deduplication result |
| **persistent_state** | Stateful (case locks; version registry) |
| **owner** | Research Operations |
| **authority** | Lock case during active research; prevent concurrent modification; deduplicate case open requests |
| **failure_behavior** | Lock unavailable → request queued (not dropped). Duplicate open request → return existing case, no second write. |
| **retry_behavior** | Lock retry 3× with backoff. |
| **idempotency** | Same case_id + same version → same locked state. Duplicate request → idempotent response. |
| **logging** | `{case_id, version, request_type, lock_state, timestamp}` |
| **provenance** | Lock holder, version, timestamp |
| **PIT_behavior** | Case version is tied to AS_OF_DATE. New as-of → new case version. |
| **forbidden_inference** | ❌ Must NOT modify case content ❌ Must NOT unlock without authorization |
| **downstream_dependencies** | CASE_REGISTRY, all research stages |

---

## S10: Notebook / Deep Research Interface

| Field | Value |
|-------|-------|
| **service_id** | S10 |
| **classification** | I (INFRASTRUCTURE) |
| **deterministic_or_policy_governed** | Infrastructure — provides access to NotebookLM and Deep Research capabilities. |
| **inputs** | Research question, source corpus, prior evidence, provider configuration |
| **outputs** | Synthesis output with source pointers. **NON-CANONICAL** — must be validated against original source before canonical admission. |
| **persistent_state** | Stateless (per-request) |
| **owner** | Evidence Intelligence Lead (Role 2) |
| **authority** | Provide research discovery / interrogation capability. |
| **failure_behavior** | Research failure → documented, not silent blank. `RESEARCH_UNAVAILABLE` state. |
| **retry_behavior** | Retry 3× with different provider. After 3 → documented failure. |
| **idempotency** | Same question + same corpus → same output (provider-dependent; best effort). |
| **logging** | `{request_id, provider, model, tokens, sources, timestamp}` |
| **provenance** | Provider, model version, prompt, retrieved sources |
| **PIT_behavior** | Uses corpus as of request time. All outputs tagged with retrieval timestamp. |
| **forbidden_inference** | ❌ Must NOT declare canonical truth ❌ Must NOT make final quality/impairment/valuation determination ❌ Must NOT bypass original-source validation |
| **downstream_dependencies** | Evidence Registry (S4) — output must be validated before admission |

---

## S11: Publication Renderer

| Field | Value |
|-------|-------|
| **service_id** | S11 |
| **classification** | D (DETERMINISTIC) |
| **deterministic_or_policy_governed** | Deterministic — template-based rendering. |
| **inputs** | Research verdict, evidence synthesis, Thai editorial template, category frontmatter |
| **outputs** | Rendered publication draft (markdown, Thai language, categorized) |
| **persistent_state** | Stateless (per-publication rendering) |
| **owner** | Thai Editor (Role 11) |
| **authority** | Render publication from canonical research record. |
| **failure_behavior** | Template error → plain output (not failed publication). Rendering failure → documented error. |
| **retry_behavior** | Retry 3× with fallback template. |
| **idempotency** | Same research record + same template → same rendered output. |
| **logging** | `{publication_id, case_id, template, rendering_time, output_hash}` |
| **provenance** | Research record version, template version, rendering timestamp |
| **PIT_behavior** | Publication rendered from research record as of publication date. |
| **forbidden_inference** | ❌ Must NOT change analytical conclusions ❌ Must NOT add investment recommendations ❌ Must NOT remove contradictions ❌ Must NOT publish without Founder gate |
| **downstream_dependencies** | Library (/library), Report Store |

---

## S12: Evaluation Harness

| Field | Value |
|-------|-------|
| **service_id** | S12 |
| **classification** | I (INFRASTRUCTURE) |
| **deterministic_or_policy_governed** | Infrastructure — operates under evaluation policy. |
| **inputs** | Sealed outcome corpus (Type A + Type B), PIT snapshots, evaluation policy, historical case records |
| **outputs** | Evaluation metrics (Type A: Research Quality + Type B: Discovery Recall) |
| **persistent_state** | Stateless per evaluation run. Results stored as evaluation records. |
| **owner** | Independent evaluation function (may be delegated) |
| **authority** | Run evaluation per approved policy. Produce metrics. |
| **failure_behavior** | **Partial evaluation → `EVALUATION_INCOMPLETE`.** Cannot satisfy an evaluation gate. Must not produce partial results labeled as complete. |
| **retry_behavior** | Retry 3× from last checkpoint. |
| **idempotency** | Same sealed corpus + same PIT snapshot + same policy → same metrics. |
| **logging** | `{evaluation_run_id, type, policy_version, corpus_version, metrics, timestamp}` |
| **provenance** | Corpus version, PIT snapshot version, policy version, model versions, run manifest |
| **PIT_behavior** | Evaluation uses **SEALED_HISTORICAL_EVALUATION** mode. Post-AS_OF evidence is HARD BLOCKED. No future-information leakage. |
| **forbidden_inference** | ❌ Must NOT use post-AS_OF data ❌ Must NOT impute missing metrics ❌ Must NOT skip Type A or Type B ❌ Must NOT modify sealed corpus |
| **downstream_dependencies** | Knowledge Steward (Role 12), Founder, M4B calibration |

---

## Service Dependency Map

```text
S3 Security / Entity Resolution
    │
    ▼
S5 Raw Source Archive → S4 Canonical Evidence Registry
    │                        │
    ▼                        ▼
S1 Selection Engine     S10 Notebook/Deep Research Interface
    │                        │
    ▼                        ▼
S9 Case Locking → S8 Research Execution Controller
    │                        │
    ▼                        ▼
S2 Research Budget     S6 Run Manifest Service
    │                        │
    ▼                        ▼
S7 Point-in-Time Lock  (all analytical stages)
    │                        │
    ▼                        ▼
S11 Publication Renderer    S12 Evaluation Harness
```

All services depend on S7 (PIT Lock) for temporal integrity. S6 (Run Manifest) records every service invocation.

<!-- 2026-08-19 17:15 UTC+7 -->