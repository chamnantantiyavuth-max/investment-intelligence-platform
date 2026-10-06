# QAD M6.0 — DESIGN-GATE CONTRACT RECONCILIATION

> **Status:** `M6.0 DESIGN / CONTRACT RECONCILIATION` — **NOT implementation authorization.**
> **Authority:** FD #148 (M6 DESIGN-GATE RECONCILIATION — R-1…R-4 rulings + PIT/REPLAY_EXCEPTION/Run-Ledger).
> **Date:** 2026-10-06 (UTC+7)
> **Base:** current `origin/main` (canonical). The September branch `docs/m6-gemini-notebook-dr @ a37e92d…` is HISTORICAL INPUT ONLY (not merged/rebased/cherry-picked).
> **Implementation:** NOT authorized. No runtime code in M6.0.

---

## 0. Purpose

Reconcile the frozen contracts so M6 (Gemini Notebook Deep Research) can be implemented truthfully. This package resolves the independent-review `C` verdict by (a) making the **explicit, narrow S10 semantic amendments** the Founder authorized, and (b) defining the M6 contracts mechanically. It does **not** preserve a misleading "zero contract change" goal: S10 retry / logging / provenance semantics are explicitly amended under FD #148.

---

## 1. Reconciled S10 retry semantics (R-1)

**Amended S10 field `retry_behavior` (see `QAD-M3-SERVICE-CONTRACTS.md` §S10, FD #148 amendment):**

- **Mode A — ≥2 compliant `deep_research_provider` implementations configured:** retry may use a **different compliant provider**; the provider change is recorded; `fallback_used` is truthful (PROV-01 `status = FALLBACK_USED` / `fallback_used` set). This preserves the original "different provider" intent.
- **Mode B — exactly ONE compliant provider configured (Gemini Notebook default):** **bounded SAME-PROVIDER retry** is permitted; **maximum 3 attempts**; each retry is recorded explicitly as **`SAME_PROVIDER_RETRY`** and **MUST NOT** be labelled provider fallback; on exhaustion the stage ends **`RESEARCH_UNAVAILABLE`**; the linked Evidence Gap (EG-01) goes to **`DEFERRED`** (or the appropriate unresolved state); **quality/evidence gates are never weakened**.

Rationale: Gemini Notebook as sole/default provider is supported **truthfully without inventing a second provider**, and **no hidden implementation-only exception** exists.

---

## 2. Telemetry truthfulness semantics (R-3)

**Principle:** `UNKNOWN / NOT_EXPOSED` is preferable to fabricated telemetry. Never fabricate or estimate underlying model identity, prompt/completion/thought tokens, or invocation cost (unless a separately approved methodology exists).

**Amended S10 `logging` / `provenance` semantics (FD #148 amendment):** `provider/model/tokens` means **record the exact values WHEN EXPOSED; otherwise record the approved truthful-unavailability state** (`NOT_EXPOSED_BY_PROVIDER` for model identity; `NOT_EXPOSED` with a reason elsewhere). No invented values.

**RRM-01:**
- `models_used[]` (**required**) → authorized sentinel **`NOT_EXPOSED_BY_PROVIDER`** when the provider does not expose the model (list[str]).
- `providers{}` (**required**) → truthfully identifies the surface, e.g. `gemini_notebook` (or the exact exposed provider surface).
- `model_versions{}` / `token_usage{}` / `cost{}` — **may be absent or empty** when not exposed.
- A provenance/run record **must explicitly state `NOT_EXPOSED`** (with reason) rather than silently omitting.

**MOD-01 / PROV-01:** **do NOT mint** a canonical MOD-01/PROV-01 with invented zeroes or guessed numerics to satisfy required numeric fields. When the surface cannot supply the required fields, the invocation is represented via the **M6 Deep Research Run Ledger + RRM linkage** (§7) instead.

---

## 3. Request-isolated Notebook lifecycle (R-4)

**Founder selection: `REQUEST-ISOLATED RECONSTRUCTION` is the M6 default.** S10 remains **logically `Stateless (per-request)`**.

Per Deep Research request:
- **one request-scoped notebook/workspace** (or an equivalent **provably clean** reconstruction);
- source set derived **deterministically from that request's approved input snapshot**;
- **no** prior Notebook chats; **no** prior Deep Research report context; **no** accumulated case-workspace context; **no** cross-request source leakage;
- **notebook/workspace identity recorded** (in the Run Ledger, §7);
- after a terminal run the workspace **may be retired/deleted** per the retention policy.

**Persistent accumulated case notebooks are NOT authorized as the M6 production default** (a future FD may authorize that model separately).

**Idempotency + retry identity:**
- **Idempotency key** = deterministic hash of `(case_id, case_version, stage, evidence_gap_id, request_payload_hash, input_snapshot_hash)`; a repeat request with the same key reuses/marks the same logical request (never a silent second run).
- **Retry identity** = `(idempotency_key, attempt_number)` with `attempt_number ∈ 1..3`; recorded in the Run Ledger; Mode A/B per §1.
- **Notebook/workspace identity** = `nb-<uuidv7>` recorded on the ledger record; bound to `(case_id, case_version, as_of, mode)`.
- **Result hash** = SHA-256 over the exact retrieved DR report bytes (+ citation/source list hash); recorded on the ledger.

---

## 4. Provider / transport abstraction (R-2)

**Transport priority (Founder policy):**
1. supported **official interface** available to the ACTUAL entitled product/account;
2. supported **connected-app / tool surface**;
3. **browser/UI automation** behind the provider adapter;
4. **manual export/import** fallback.

**Rules:** do NOT assume an Enterprise/Cloud API exists merely because Google documents one. Provider capability ≠ automation transport; transport lives **behind the adapter** and **never enters canonical domain contracts** (§4 of `QAD-EVIDENCE-AND-SOURCE-MODEL.md`: "Do not hardwire consumer UI/browser hacks into canonical domain contracts"). Browser automation (Founder-authorized for M6, behind the adapter) must: use the existing authenticated session; capture **no** credentials into the repo; put **no** credentials in logs/artifacts; detect timeouts/errors explicitly; **fail closed on navigation ambiguity**; **record transport type per run**; and a UI change must produce an **observable transport failure, not a fabricated success**; manual fallback permitted. Do not enable browser automation outside M6 scope.

---

## 5. SEALED PIT trusted capture rule (B1 — final)

**Founder rule (M6 v1, conservative): `SRC-01 ATOMIC ADMISSION IS THE ONLY TRUSTED SEALED BYTE-CAPTURE PROOF`.**

The canonical RawSourceArchive contract already establishes `admit_source(instance, raw_bytes)` as an atomic metadata + exact-byte admission operation where `SRC-01.content_hash == SHA256(raw_bytes)` is mandatory. Therefore, for `SEALED_HISTORICAL_EVALUATION` and ordinary (non-exception) replay, a source is **M6-input-eligible ONLY if ALL hold**:

- (A) a canonical `SRC-01` record exists;
- (B) its raw blob exists in RawSourceArchive;
- (C) `SRC-01.retrieval_date <= PITC-01.as_of_date`;
- (D) at evaluation time `SHA256(stored_raw_blob) == SRC-01.content_hash`;
- (E) the exact bytes supplied to the Gemini Notebook request are **BYTE-IDENTICAL** to the stored raw blob;
- (F) the hash is **reverified immediately before** constructing the request snapshot.

If ANY condition fails → classify **`UNAVAILABLE_FOR_SEALED_PIT`** and preserve/update the associated Evidence Gap (EG-01).

**SRCV-01 limitation (explicit):** M5.2 §10.4 does NOT define `SRCV-01.content_hash == SHA256(raw version bytes)`. M6 v1 MUST NOT use an `SRCV-01` record alone as trusted SEALED byte-capture proof → classify **`SRCV_ONLY_CAPTURE_PROOF = NOT_ELIGIBLE_FOR_M6_V1_SEALED`** until a future, separately governed contract defines exact version-byte storage, capture-timestamp authority, content_hash derivation, and atomic metadata↔version-byte binding. **SRCV-01 semantics are NOT amended here; no new canonical schema is added.** This deliberately trades historical coverage for correctness.

**Trusted timestamp semantics:** `SRC-01.retrieval_date` is accepted as the trusted capture timestamp **ONLY** because the source metadata and exact bytes are admitted through the canonical atomic `RawSourceArchive.admit_source(...)` boundary. It must **NOT** be accepted from: Gemini Notebook; browser metadata; webpage publication date; current web retrieval; caller-supplied unadmitted metadata; a Research Room artifact; or manually constructed detached JSON. **The M6 adapter must resolve the SRC-01 + blob from the authoritative RawSourceArchive itself; caller-provided source bytes are never authoritative.**

**Sealed snapshot construction (mechanical):** for every input source include at minimum `source_id`, `SRC-01 retrieval_date`, `SRC-01 content_hash`, `recomputed raw_blob_sha256`, `raw byte length`, `PIT as_of`, `eligibility verdict`. Compute a deterministic **`input_snapshot_hash`** over the **ordered** source-id + exact-blob-hash set plus `case_id`, `case_version`, PIT mode, `as_of`. The actual Gemini request MUST be populated **only** from the exact verified snapshot. **No live provider retrieval is allowed to augment a `SEALED_HISTORICAL_EVALUATION` request.** If the provider surface cannot disable uncontrolled web/source discovery for a SEALED request → **FAIL CLOSED: `PROVIDER_CANNOT_ENFORCE_SEALED_INPUT`**; do NOT run Deep Research in SEALED mode.

`LIVE_CASE_UPDATE` may perform current retrieval under existing LIVE rules. (S7 enforces PIT on canonical evidence at admission; Notebook-side upstream isolation is the adapter's duty.)

## 6. REPLAY_EXCEPTION separation (B4 — final)

`REPLAY_EXCEPTION` must remain **explicitly separate** from SEALED evaluation.

**Negative path (must hold):** ordinary SEALED mode cannot access post-AS_OF source bytes.

**Positive authorized path (must hold), requires ALL of:** `PITC-01.mode = REPLAY_EXCEPTION`; the Founder-authorized role/token semantics already required by the runtime (`qad/m53/pit_enforcement.py` `_adjudicate_object`); an explicit **non-empty `exception_reason`**; a provenance record; output **labelled `REPLAY_EXCEPTION`**; and output **excluded from** clean SEALED evaluation metrics, clean SEALED historical results, and any claim of no-future-information evaluation.

**Blocked path (must hold):** a `REPLAY_EXCEPTION` request lacking Founder authority **or** lacking `exception_reason` is **BLOCKED**.

**Re-labelling rule:** a REPLAY_EXCEPTION result **cannot** later be re-labelled as SEALED without creating a new valid SEALED run.

Covered by tests #18–#20 (§11).

## 7. Deep Research Run Ledger — `DeepResearchRunLedgerStore` (B2 — final)

Closes the reviewer MAJOR finding. The Research Room stays non-canonical/exploratory/ephemeral and is **NOT** the durable carrier. The ledger is:

- **durable**; **append-only during execution**; **immutable after terminalization** except explicit tombstone/administrative-correction semantics defined by this contract;
- **NON-CANONICAL for investment truth** — operational/provenance authority only;
- **separate from** the Research Room and **separate from** the 68 M4A canonical schemas;
- **NOT stored in git as runtime state**.

No canonical schema addition is authorized; no Research Room durability upgrade is authorized. The implementation backend is deferred to M6 implementation but MUST satisfy this contract.

### 7.1 `DeepResearchRunRecord` — required structure

Identity/linkage: `ledger_id`, `research_run_id`, `rrm_manifest_id`, `case_id`, `case_version`, `evidence_gap_id`, `request_id`, `idempotency_key`, `attempt_number`, `retry_mode`, `notebook_identity` (workspace id + `provider_surface`), `pit_context_id`, `pit_mode`, `as_of`, `input_snapshot_hash`, `transport_type`, `started_at`, `terminal_at`, `terminal_status`, `result_artifact_ref`, `result_sha256`.

### 7.2 Telemetry truthfulness structure (durable)

For **each** telemetry metric (model identity; prompt_tokens; completion_tokens; total_tokens if applicable; cost; provider-reported model version) store:

- `telemetry.<metric>.status` = `EXPOSED | NOT_EXPOSED`
- `telemetry.<metric>.value` = exact exposed value OR `null`
- `telemetry.<metric>.reason` = **required when `NOT_EXPOSED`**

Rules: **never store zero as shorthand for unknown**; never store an estimated value unless a separately approved methodology explicitly labels it estimated. For the current consumer Gemini Notebook surface the expected truthful state is **`NOT_EXPOSED`** for model/tokens/cost unless the live surface later provides them.

### 7.3 Durability / retention (mechanical)

- a run record is created **BEFORE** external provider execution;
- attempts are **append-only**; failures are durable; `NOT_EXPOSED` reasons are durable; discovered-source dispositions are durable;
- the terminal record is **immutable**;
- **Research Room deletion MUST NOT affect ledger records**; **notebook deletion MUST NOT affect ledger records**; result-artifact deletion/retirement MUST preserve `result_sha256` + disposition history;
- retention = at minimum the lifetime of the associated research_run / audit lineage — **no silent GC**.

### 7.4 RRM linkage

`RRM-01.deep_research_runs[]` (`Optional[list[str]]`) stores **ledger IDs only** — no dictionaries, no free-form embedded ledger objects (contract-compatible with the frozen model).

### 7.5 Source candidate disposition record

Every source discovered by Gemini Notebook / Deep Research gets **one durable ledger disposition entry**: `source_candidate_id`; URL / external identifier; fingerprint/hash when available; discovery timestamp; original-source-verification status; PIT eligibility; **disposition ∈ {`IMPORTED`, `REJECTED`, `UNAVAILABLE`, `DEFERRED`}** (exactly one); reason; `SRC-01 id` if admitted; `EV-01 id(s)` if evidence admitted; `EAR-01 id(s)` if evidence admitted. **No discovered source may disappear silently.**

### 7.6 Authority boundary (explicit)

The ledger is a **non-canonical additive operational store**, outside the 5 canonical anchors; it does not modify the 68 canonical schemas and does not convert the Research Room into a durable canonical store. If a *canonical*-store ledger were required, that is a separate Founder decision.

## 8. Failure states

| State | Trigger | Handling |
|---|---|---|
| `RESEARCH_UNAVAILABLE` | retries exhausted / provider unreachable | documented failure; EG-01 `DEFERRED` (or appropriate unresolved state); gates not weakened |
| `TRANSPORT_FAILURE` | transport error / navigation ambiguity / UI drift | **fail closed**; no fabricated success; `NOT_CLEAN`; recorded on ledger |
| `PIT_BLOCK` | SEALED source lacks qualifying pre-AS_OF bytes / missing publication_date | source `UNAVAILABLE_FOR_SEALED_PIT`; gap preserved |
| `TELEMETRY_NOT_EXPOSED` | provider hides model/tokens/cost | recorded as `NOT_EXPOSED(_BY_PROVIDER)`; never fabricated |
| `INCOMPLETE` | budget exhaustion | per Full Research Protocol; gates not weakened |

---

## 9. Non-canonical → canonical admission flow

```
Gemini Notebook DR (non-canonical; request-isolated per §3)
  → M6 Deep Research Run Ledger (§7 durable record; result hash; dispositions)
  → (Research Room, ephemeral, optional scratch)
  → source extraction → original-source verification → RawSourceArchive.admit_source() (SRC-01 + raw bytes + SHA-256)
  → dedup → contradiction preservation (CTR-01) → PIT check (S7 source-time; SEALED requires publication_date + pre-AS_OF bytes)
  → provenance check → admit_evidence() (EV-01 + EAR-01 atomic; validation_status RAW→VALIDATED)
```
No blind "Import All"; every candidate receives a durable disposition (§7).

---

## 10. Transport capability probe (read-only — actual Founder surface)

**Actual surface probed:** consumer **NotebookLM / Gemini Notebook** web app via the local browser-automation CLI `notebooklm` (v0.7.3, `notebooklm-py`; Playwright `storage_state.json`; authenticated profile `default`). No purchase / no Enterprise signup / no migration. Probe was **read-only** (`--help`, `doctor`, `status`, `list`, `metadata`, `source list`, `research status`, `artifact list`).

**Surfaces distinguished:** (A) consumer subscription surface = **the one probed**; (B) Google Workspace = not probed (not the entitled surface); (C) Enterprise/Cloud = **not assumed** (not entitled, not probed).

| Capability | Command surface | Result | Classification |
|---|---|---|---|
| notebook create | `create` | command exists | `SUPPORTED_UI_ONLY` (browser automation) |
| notebook delete/retire | `delete` | command exists | `SUPPORTED_UI_ONLY` |
| notebook list | `list` | **live FAIL** (CSRF/UI drift) | `SUPPORTED_UI_ONLY` — currently **NON-FUNCTIONAL** |
| source add | `source add` | command exists | `SUPPORTED_UI_ONLY` |
| source list | `source list` | **live FAIL** | `SUPPORTED_UI_ONLY` — currently **NON-FUNCTIONAL** |
| source removal | `source delete` | command exists | `SUPPORTED_UI_ONLY` |
| Deep Research start | `source add-research --mode deep` | command exists; live blocked | `SUPPORTED_UI_ONLY` — currently **NON-FUNCTIONAL** |
| Deep Research status | `research status/wait` | **live FAIL** | `SUPPORTED_UI_ONLY` — currently **NON-FUNCTIONAL** |
| report retrieval | `artifact list/get/export` | **live FAIL** | `SUPPORTED_UI_ONLY` — currently **NON-FUNCTIONAL** |
| citation/source retrieval | `artifact get` / `ask --json` (source refs) | command exists; live blocked | `SUPPORTED_UI_ONLY` |
| notebook/chat context reset | `ask --new` (destructive) / `clear` | command exists | `SUPPORTED_UI_ONLY` |
| exact model identity | — | no option | **`NOT_EXPOSED`** |
| token usage | — | no option | **`NOT_EXPOSED`** |
| invocation cost | — | no option | **`NOT_EXPOSED`** |
| **official Deep Research API** | — | none (third-party automation only) | **`NOT_EXPOSED`** |

**Observed transport failure (material):** every live-data operation fails with `Unexpected error: CSRF token not found in HTML. Final URL: https://notebook.google.com/ … page structure has changed.` Only local-state commands (`doctor`, `status`) succeed. This is an **observable transport failure, not a fabricated success** — consistent with R-2.

**Boundary used:** the probe did **no** create/delete/add; **no** Deep Research run; **no** source ingestion.

---

## 11. Acceptance-test plan (DESIGN ONLY — no runtime; tests 1–20)

Baseline from FD #148 (retry Mode A/B; telemetry; admission) remains in force; the set below is the FINAL mechanically-testable acceptance criteria for the M6.0 design gate.

| # | Test | Expected |
|---|---|---|
| 1 | SRC-01 atomic admission binds exact bytes | `admit_source()` stores metadata+bytes atomically; `SRC-01.content_hash == SHA256(raw_bytes)` |
| 2 | `retrieval_date <= AS_OF` | eligible only when `SRC-01.retrieval_date <= PITC-01.as_of_date` |
| 3 | stored raw hash equals `SRC-01.content_hash` | recomputed `SHA256(stored_blob) == SRC-01.content_hash` |
| 4 | provider-supplied request bytes equal stored bytes | supplied bytes byte-identical to the stored raw blob |
| 5 | detached/backdated metadata cannot authorize a source | detached/backdated metadata → `UNAVAILABLE_FOR_SEALED_PIT` (test proves post-AS_OF bytes ineligible) |
| 6 | SRCV-only proof rejected in M6 v1 SEALED | `SRCV_ONLY_CAPTURE_PROOF = NOT_ELIGIBLE_FOR_M6_V1_SEALED` |
| 7 | live web augmentation forbidden in SEALED | no provider retrieval augments a SEALED request |
| 8 | inability to disable live retrieval → FAIL CLOSED | `PROVIDER_CANNOT_ENFORCE_SEALED_INPUT`; no SEALED run |
| 9 | ledger record exists before provider call | run record created pre-execution |
| 10 | NOT_EXPOSED persisted durably with reason | status + reason durable; read-back test |
| 11 | Research Room deletion cannot erase ledger | ledger record survives |
| 12 | notebook deletion cannot erase ledger | ledger record survives |
| 13 | all source candidates have dispositions | every discovered source has exactly one disposition entry |
| 14 | Request A canary cannot leak to B | B's provider-visible inventory ⊆ B's snapshot; no A canary/citation/chat/report/identity |
| 15 | isolation must be positively verifiable | PASS requires positive proof of a clean request-scoped context |
| 16 | isolation-unverifiable → FAIL CLOSED | `REQUEST_ISOLATION_UNVERIFIED`; execution must not proceed |
| 17 | normal SEALED blocks future bytes | post-AS_OF bytes unreachable in SEALED |
| 18 | authorized REPLAY_EXCEPTION succeeds and is labelled | output labelled `REPLAY_EXCEPTION`; excluded from clean SEALED metrics |
| 19 | unauthorized exception blocked | missing Founder authority OR empty `exception_reason` → BLOCKED |
| 20 | exception results excluded from clean SEALED reporting | cannot be reported as clean SEALED; no re-labelling without a new valid SEALED run |

**B3 (§10) — isolation leakage test D (observable provider-capability test):** create Request A with unique canary material `M6_ISOLATION_CANARY_A_<fixed fixture id>` present ONLY in A's provider context/corpus; terminalize/retire A; create Request B as a fresh isolated request with a disjoint corpus. **B MUST NOT** retrieve the A canary, cite A sources, reference A's prior chat, reference A's report, or expose A's notebook identity/context; and **B's provider-visible source inventory must contain ONLY B's approved snapshot**. PASS requires **positive proof of clean context** (absence from final prose alone is NOT sufficient). If the surface cannot prove isolation → **FAIL CLOSED `REQUEST_ISOLATION_UNVERIFIED`**; the request-isolated production adapter must not proceed.

**B4 (§6) — REPLAY_EXCEPTION positive/negative:** test B4-A (properly authorized → allowed + labelled `REPLAY_EXCEPTION`, excluded from clean SEALED reporting); test B4-B (missing Founder authority OR missing `exception_reason` → BLOCKED); test B4-C (a REPLAY_EXCEPTION result cannot be re-labelled SEALED without a new valid SEALED run).

## 12. B1–B4 FINAL RECONCILIATION (FD #149) — closure of prior findings

| Prior review item | Closure |
|---|---|
| **CRITICAL** — PIT byte-level: `retrieval_date ≤ AS_OF` + SRCV hash did not prove the exact bytes were captured by AS_OF | **B1 closed:** trusted SEALED byte-capture proof = **SRC-01 atomic admission only** (six-condition rule §5) + **SRCV-only proof explicitly rejected** (`SRCV_ONLY_CAPTURE_PROOF = NOT_ELIGIBLE_FOR_M6_V1_SEALED`) + trusted timestamp = SRC-01.retrieval_date **only via the atomic admission boundary** + fail-closed tests (#1–#8). |
| **MAJOR** — telemetry `NOT_EXPOSED` had no durable home | **B2 closed:** `DeepResearchRunLedgerStore` contract (§7) with a durable per-metric `telemetry.<metric>.{status,value,reason}` structure; read-back test (#10). |
| **MINOR** — request isolation test D lacked an observable probe | **B3 closed:** canary-based provider-capability test + fail-closed `REQUEST_ISOLATION_UNVERIFIED` (§11 #14–#16). |
| **MINOR** — REPLAY_EXCEPTION test H lacked positive-path assertions | **B4 closed:** positive/blocked/re-labelling tests (§11 #18–#20). |

**Consumer transport reality (recorded, unchanged):** `CONSUMER_BROWSER_TRANSPORT = CURRENTLY NON-FUNCTIONAL` — local `notebooklm` auth `doctor`/`status` work, but live notebook/source/research operations fail with observable CSRF/UI drift; model identity / token usage / invocation cost **not exposed**. This is **NOT** a reason to weaken contracts and **NOT** permission to fabricate successful automation. M6 implementation may begin behind an adapter (deterministic adapters/mocks for contract tests; manual transport fallback where explicitly allowed) but **no automated Gemini Notebook integration may be claimed until a real live canary passes**.

**No frozen contract is amended in this task except the FD #148 S10 amendments.** B1–B4 are design/contract reconciliations within M6.0.

<!-- 2026-10-06 UTC+7 · FD #148 M6.0 reconciliation (design only) -->

<!-- 2026-10-06 UTC+7 · FD #149 B1–B4 final reconciliation (design only) -->
