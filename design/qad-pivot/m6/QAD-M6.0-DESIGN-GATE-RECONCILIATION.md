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

## 5. Pre-AS_OF byte-snapshot contract (PIT)

For `SEALED_HISTORICAL_EVALUATION` and ordinary (non-exception) replay, Gemini Notebook may receive **only** source bytes whose historical availability is provable **≤ PIT AS_OF**. First-implementation conservative rule: **`PRE-AS_OF CAPTURE REQUIRED`**.

**Accepted proof (primary):** canonical **RawSourceArchive** history — `SRC-01` / `SRCV-01`, exact `content_hash`, immutable bytes, `retrieval_date ≤ AS_OF` (and, where available, a trusted version-specific capture/availability record bound to the byte hash). **The exact bytes supplied to Gemini Notebook must hash-identically to the qualifying archived version.**

**Rejected:** a document with `publication_date ≤ AS_OF` whose **exact supplied bytes were captured only AFTER AS_OF** — **NOT eligible** for SEALED input. **Do NOT use current web retrieval to reconstruct historical sealed knowledge.**

**If no qualifying pre-AS_OF byte snapshot exists:** classify the source **`UNAVAILABLE_FOR_SEALED_PIT`** and **preserve the gap**.

`LIVE_CASE_UPDATE` may perform current retrieval under existing LIVE rules. (S7 enforces PIT on **canonical evidence at admission**; Notebook-side upstream isolation is the adapter's duty.)

---

## 6. REPLAY_EXCEPTION separation

`REPLAY_EXCEPTION` must remain **explicitly separate** from SEALED evaluation. Require: `PITC-01.mode = REPLAY_EXCEPTION`; the Founder-authorized role semantics already required by the runtime (`qad/m53/pit_enforcement.py` `_adjudicate_object`); explicit **`exception_reason`**; provenance; **output labelled as exception/re-evaluation**; **never** reported as a clean SEALED historical result. **Tests must prove** ordinary SEALED/replay cannot obtain the exception path accidentally.

---

## 7. Deep Research Run Ledger (durable source-candidate disposition carrier)

The **Research Room remains non-canonical, exploratory, ephemeral** — therefore it is **NOT** the durable carrier. Design: **`M6 Deep Research Run Ledger`**.

**Ledger record (one per DR run) — durable, immutable after terminalization, non-canonical investment truth (operational/provenance record):**

| Field | Notes |
|---|---|
| `ledger_id` | UUID v7 |
| `research_run_id` | links to the run (RRM-01 `manifest_id`) |
| `case_id`, `case_version` | case linkage |
| `evidence_gap_id` | EG-01 linkage |
| `request_id` | the DR request identity |
| `notebook_identity` | workspace id + provider surface |
| `transport_used` | official / connector / browser-ui / manual-export |
| `result_artifact_ref`, `result_hash` | artifact reference + SHA-256 |
| `pit_snapshot_ref` | PIT context / input-snapshot hash + mode |
| `started_at`, `ended_at`, `terminal_status` | timestamps + terminal state |
| `attempts[]` | retry identity + mode (`SAME_PROVIDER_RETRY` / provider-change) |

**Per discovered source candidate (child records):** source URL/identifier; source fingerprint/hash (when available); **disposition ∈ {`IMPORTED`, `REJECTED`, `UNAVAILABLE`, `DEFERRED`}**; reason; original-source-verification status; **PIT eligibility** (`ELIGIBLE_PRE_AS_OF` / `UNAVAILABLE_FOR_SEALED_PIT` / `LIVE_RETRIEVAL`); canonical `SRC-01` / `EV-01` / `EAR-01` IDs when admitted.

**RRM linkage:** `RRM-01.deep_research_runs[]` (`Optional[list[str]]`) holds **REFERENCES (ids)** to Run Ledger records — **contract-compatible** (implementation model is `list[str]`). **Do NOT stuff structured dictionaries into `deep_research_runs[]`.**

**Authority-boundary note (explicit):** the ledger is a **non-canonical operational store**, additive and **outside** the 5 canonical anchors; it does **not** modify the 68 canonical schemas and does **not** convert the Research Room into a durable canonical store. If the Founder later requires the ledger to be a *canonical* store (schema-level), that is a separate Founder decision (not taken here). Physical backend choice is deferred to implementation (repo evidence artifacts OR a dedicated non-canonical store).

---

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

## 11. Acceptance-test plan (RED before code — §11)

| # | Test | Expected |
|---|---|---|
| A | same-provider retry allowed ONLY in single-provider mode | Mode B only when exactly 1 compliant provider; recorded `SAME_PROVIDER_RETRY`; never `FALLBACK_USED` |
| B | alternate-provider fallback with a 2nd compliant provider | Mode A; provider change recorded; `fallback_used` truthful |
| C | retry exhaustion | `RESEARCH_UNAVAILABLE` + EG-01 `DEFERRED`; gates unchanged |
| D | request B cannot observe request A context | isolated workspace; no prior chat/report context on B |
| E | SEALED receives only exact pre-AS_OF archived bytes | byte hash == qualifying SRCV-01 version |
| F | post-AS_OF re-retrieval w/ old publication_date | REJECTED for SEALED (`UNAVAILABLE_FOR_SEALED_PIT`) |
| G | byte hash mismatch | **fail closed** |
| H | REPLAY_EXCEPTION requires explicit authorized context | ordinary SEALED/replay cannot take the exception path |
| I | unknown telemetry | recorded `NOT_EXPOSED(_BY_PROVIDER)`; never 0/guessed |
| J | no MOD-01/PROV-01 fabricated | not minted when required numerics unknown |
| K | every discovered source | durable disposition on the Run Ledger |
| L | Research Room deletion cannot erase the ledger | ledger survives; RRM reference intact |
| M | canonical admission | still requires original-source verification + PIT + EAR-01 |

---

## 12. Open items carried to the independent review

- S10 amendment wording (§1/§2) is explicit and non-hidden.
- Run Ledger is a non-canonical durable operational store (§7) — authority-boundary assumption stated.
- Transport: consumer surface currently NON-FUNCTIONAL via automation (§10) — implementation must handle a broken transport (fail closed) and may need the manual export/import path until the automation is repaired.

<!-- 2026-10-06 UTC+7 · FD #148 M6.0 reconciliation (design only) -->
