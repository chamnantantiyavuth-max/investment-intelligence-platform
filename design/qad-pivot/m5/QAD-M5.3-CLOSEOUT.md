# QAD-M5.3 — CLOSEOUT (CORRECTION IMPLEMENTED — READY FOR FOUNDER INDEPENDENT RE-AUDIT)

> **Authority:** FOUNDER DECISION — QAD M5.3 IMPLEMENTATION (8 Sep 2026, OPTION A — GO)
> **Correction authority:** FD #138 — QAD M5.3 Correction Round GO + Founder Decisions (9 Sep 2026)
> **Status:** ✅ **CORRECTION IMPLEMENTED / READY FOR FOUNDER INDEPENDENT RE-AUDIT**
> **NOT automatically CLOSED/FROZEN** — the Founder explicitly requires a NEW
> independent Founder audit of the corrected implementation before M5.3 closure.
> **M5.3 remains a HOLD milestone until that re-audit.**
>
> **History:** the ORIGINAL 8 Sep implementation (`bac8bf4` `ceff38d` `f070771`
> `5d77c13`) failed the Founder independent audit (10 material findings).
> FD #138 authorized this correction round. The original claims are preserved
> in git history and in `QAD-M5.3-IMPLEMENTATION-MAP.md` Sections A–E (marked
> HISTORICAL; Section F is the authoritative corrected contract).

---

## 0. Independent audit verdict (9 Sep 2026) → correction driver

| Finding | Class | Correction (FD #138) |
|---|---|---|
| "max 3 retries" implemented as 3 total attempts | A — contract drift | Initial + max 3 retries = max 4 executions |
| RR-01 written for the initial execution (incl. first-run success) | A | RR-01 = retry-only; initial = SI-01 |
| retry_id not UUID v7 (and M5.3 fixture IDs) | A | RFC-9562 UUID v7 utility + fixture conformance |
| Checkpoint replay not materialized (resume = len(RR)+1) | A | RSR-01 checkpoint authority (existing schema) |
| Retried-write idempotency unproven | A | Real canonical-write retry tests (idempotent + conflict) |
| `_attempts_for()` fail-open on store read | A | Fail closed — typed error propagates, stage not run |
| RR-01 + RRM-01 partial-state window | A | Same-store atomic batch + preflight before execution |
| Public `adjudicate()` trusts caller PITC/EAR | A | ID-based public surface; object adjudicator private |
| `query()` silent-empty on store failure | A | Typed PITBlockError — never silent empty |
| Source-timestamp PIT semantics unresolved | C → Founder decided | effective = MAX(EV.as_of, source_available_at) |
| EV-hash test mislabeled as M4B TEST-7 seal | B | Deferred (Option B); relabeled record-integrity |

## 1. Scope delivered (correction round — FD #138)

| Component | Corrected behavior | Where |
|---|---|---|
| S8 Retry budget | Initial + max 3 retries; retry #3 fail → FAILED; ESCALATED removed | `qad/m53/retry_kernel.py` |
| S8 RR-01 lifecycle | Retry-only records; clean first-run = ZERO RR-01 | same |
| S8 checkpoint authority | RSR-01 stage_state/checkpoint_ref/output_ids + version-aware replay | same (uses `stage_store`) |
| S8 fail-closed history | Unreadable RR/RSR history ⇒ typed error, no stage execution | same |
| S8 RR/RRM atomicity | One `store_batch`; manifest preflight before execution | same |
| UUID v7 | `qad/ids.py` RFC-9562 generator; retry_id/stage_id comply | `qad/ids.py` (new) |
| S7 public boundary | ID-based `adjudicate(evidence_id, pitc_id)`; object adjudicator private | `qad/m53/pit_enforcement.py` |
| S7 fail-closed stores | Typed errors on store/source failure; not-found ≠ unavailable | same |
| S7 source-time PIT | effective_pit_time = MAX(EV.as_of, authoritative source time); SEALED requires publication_date | same |
| S7 seal relabel | EV canonical-hash = defense-in-depth `record_integrity` (deferred corpus seal) | same |
| Noncanonical surface | `ExecutionContext` / `StageContext` (service-layer only) | `qad/m53/retry_kernel.py` |

Corrected contract + interfaces: `design/qad-pivot/m5/QAD-M5.3-IMPLEMENTATION-MAP.md` **Section F**.
Founder decisions: `design/qad-pivot/m5/QAD-M5.3-CORRECTION-DECISION-PACKAGE.md` **§17** + FD #138.

## 2. Key corrected semantics (all from FD #138 — nothing reinvented)

- **Retry budget:** initial execution (SI-01) is NOT a retry; up to 3 RR-01
  retries follow a retryable initial failure; retry #3 fail → FAILED.
- **ESCALATED:** removed from M5.3 — never produced, `escalated_to` never set.
- **Checkpoint replay:** same (case_id, case_version, stage_name) with a
  terminal COMPLETE RSR-01 (checkpoint_ref encodes the case_version) → replay
  without re-execution and without new canonical records. Different stage or
  different case_version → NOT false-idempotent.
- **Retried-write idempotency:** same logical execution + same checkpoint +
  same canonical payload → single canonical state (store idempotency);
  different payload under the same identity → TransactionFailure wrapping
  IntegrityConflict (zero records).
- **Fail closed:** retry history / RSR state / evidence store / source archive
  read failures raise typed deterministic errors — never "no history" / empty.
- **Source-time PIT:** effective = MAX(EV.as_of, source availability);
  SEALED requires SRC-01.publication_date (missing → PIT BLOCK); LIVE/REPLAY
  fall back to retrieval_date; unresolvable/uninterpretable → FAIL CLOSED.
- **RR/RRM atomicity:** one `store_batch` per retry provenance (same store),
  manifest preflighted (exists + RUNNING) BEFORE the stage runs.
- **UUID v7:** `qad.ids.generate_uuid7()` (RFC-9562) for M5.3-generated
  canonical ids; fixtures use valid UUID v7 where frozen contracts require it.

## 3. Verification (all LOCAL, real runs — GitHub/Vercel is NOT Python CI)

| Suite | Result |
|---|---|
| M5.3 S7 + S8 targeted (`tests/qad/m53/`) | **41/41 PASS** (rewritten contract tests per FD #138) |
| UUID v7 utility (`tests/qad/test_ids.py`) | **7/7 PASS** |
| QAD persistence + conformance (`tests/qad/`) | 449/449 PASS |
| Erratum-002 five-anchor / authority-isolation / RRM lifecycle regressions | included in 449/449 (no regression) |
| Locked audit register (FD #138 date anchor updated 7 Sep → 9 Sep 2026) | 4/4 PASS |
| **Full pytest** | **688/688 PASS** (668 pre-correction − 28 replaced m53 tests + 41 new m53 + 7 ids = 688) |
| M4A validator (`validate-m4a-contracts.py`) | **173/173 PASS** (frozen M4A unchanged) |
| M4B validator (`validate-m4b-pack.py`) | **93/93 PASS** (frozen M4B unchanged) |

Test-truth chronology: 640 (Erratum-002 final) → 668 (original M5.3 impl) →
**688 (M5.3 correction round)**. The 668 total was NOT forced; the replacement
and addition counts are exact per-file.

## 4. Correction commit chain (diagnostic → fix chronology, FD #138)

1. `qad/ids.py` + `tests/qad/test_ids.py` — RFC-9562 UUID v7 utility (7 tests)
2. `tests/qad/m53/` — RED contract tests per GO §16 (diagnostic-first,
   demonstrated RED against the original `5d77c13` candidate: missing
   `ExecutionContext` surface + contract violations)
3. `qad/m53/retry_kernel.py` — corrected S8 (SRR checkpoint authority,
   retry-only RR-01, initial+3, no ESCALATED, fail-closed history, RR/RRM
   store_batch, UUID v7)
4. `qad/m53/pit_enforcement.py` — corrected S7 (ID-based surface, fail-closed
   stores, source-time PIT, integrity relabel)
5. `qad/m53/__init__.py` — export new noncanonical types
6. `tests/locked/test_audit_api.py` — register-tail date anchor (FD #138)
7. docs — MAP Section F + this closeout + decision package finalization + FD #138

## 5. §11.3 items still deferred (unchanged — NOT built)

Full Query API, filter DSL, sort/paginate framework, cross-store joins,
full-text search, time-series query engine, graph traversal, ORM/DB
abstraction, production adapter selection (SQLite/PostgreSQL/DuckDB).

## 6. Boundaries (unchanged — the correction GO did NOT authorize)

Production Release — NOT AUTHORIZED · Live Autonomous QAD — NOT
AUTHORIZED · workforce cutover — NOT AUTHORIZED · cron cutover — NOT
AUTHORIZED · fixture sealing / cost calibration / final production stack —
NOT AUTHORIZED (existing pre-production gates unchanged) · M6/M7 — NOT
STARTED · Autonomous Discovery business logic — NOT STARTED · full M4B
corpus-seal verification — DEFERRED to the fixture-sealing gate (FD #138 §12).

## 7. Stop-condition check (per FD #138 §17 — no silent scope expansion)

| Stop condition | Verdict |
|---|---|
| Mechanically requires a new canonical schema? | ❌ none (RSR-01/RRM-01/SI-01/PITC-01/EV-01/EAR-01/SRC-01 all exist and are used) |
| Requires a frozen schema field addition? | ❌ none (source-time PIT uses existing SRC-01 fields; case_version from RRM-01) |
| Requires a frozen state-machine change? | ❌ none (ESCALATED removed — the RR-01 status ENUM is untouched, only transition usage changed per Founder authority) |
| Requires a new role/authority rule? | ❌ none |
| Full §11.3 Query API / production adapter became necessary? | ❌ minimum substrate only; reference in-memory |
| Conflicting frozen authority discovered? | ❌ none — ambiguity points (ESCALATED transition, source-time PIT) were RESOLVED BY FOUNDER DECISION (FD #138), not by silent invention |

## 8. Status

```text
M5.3 — CORRECTION IMPLEMENTED / READY FOR FOUNDER INDEPENDENT RE-AUDIT
       NOT CLOSED / NOT FROZEN — new independent Founder audit required first
Working scope state — S7 ✅ (corrected) / S8 ✅ (corrected) / UUID v7 ✅ / source-time PIT ✅
S7 / S8 — implemented (reference), NOT production
Erratum-002 — FOUNDER ACCEPTED / CLOSED / FROZEN (NOT reopened)
Production / Live Autonomous QAD — NOT AUTHORIZED
M6 / M7 — NOT STARTED
```

<!-- 2026-09-09 13:30 UTC+7 -->