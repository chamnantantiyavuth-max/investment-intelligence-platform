# QAD-M5.2 Item 10 — Full Regression Proof

> **Status:** CURRENT REGRESSION GREEN / HISTORICAL FAILURE PROVENANCE INCOMPLETE / FOUNDER WAIVER REQUIRED
> **Classification:** REGRESSION PROOF ONLY
> **Authority:** FD #135; Founder 25 Aug 2026 correction ("FULL REGRESSION MUST BE GREEN")
> **Date:** 2026-08-28
> **Baseline:** Items 1–9 FOUNDER APPROVED / CLOSED (e9446af..1dd4d89)

---

## 1. Recovered Item-10 Authority

**Source:** 25 Aug 2026 correction session (Founder, 7-core-defect message)

> **`10. FULL REGRESSION MUST BE GREEN`**
>
> "Current actual session result was:
> `full pytest = 400/401, exit 1`
> not `401/401 PASS`."
>
> "Reproduce the Live Office failure exactly. If it is mutable-environment/test
> drift: repair deterministically without weakening approved semantics. Do NOT
> mutate live operational state merely to make the test pass."
>
> "Required final gate:
> `python -m pytest tests/ -q` → 100% PASS"

**Acceptance criteria:** `python -m pytest tests/ -q` from clean `main` → exit 0, 100% pass.

---

## 2. Exact Acceptance Command Result

```
> python -m pytest tests/ -q --tb=no
577 passed, 11 warnings in 5.72s
exit code: 0
```

No skipped, no xfailed, no xpassed. 11 warnings are Pydantic deprecation notices (unchanged across Items 1–9).

---

## 3. Historical Live Office Failure — Provenance

### 3.1 What the historical record says

The original M5.2 closeout (`340fe3c`, 24 Aug 2026) reported:

> **"401/401 QAD+M5.2+core (1 pre-existing unrelated Live Office failure)"**

The Founder's independent investigation at `70b8f45` (25 Aug) established:

> **`400/401, exit 1` — 1 Live Office failure**

The closeout's "401/401" claim was inaccurate — the suite was 400/401 with 1 failure.

### 3.2 What we know about the failure

| Fact | Evidence |
|------|----------|
| Suite at `70b8f45` | 400/401, exit 1 (Founder observation) |
| Persistence tests at `70b8f45` | 60/60 PASS (commit `70b8f45` record) |
| QAD tests at `70b8f45` | 165/165 PASS (commit `70b8f45` record) |
| Failure description | "Live Office failure" (Founder and commit messages) |
| Live-board test exists | `test_s1_load_board_include_archived_is_a_superset` reads live Hermes board `"iip"` |
| Test file unchanged | `tests/test_capital_office_semantics.py` was NOT modified between `70b8f45` and `da9eafb` |
| Suite after `da9eafb` | 414/414 PASS (commit `da9eafb` record — still calls prior "Live Office failure") |

### 3.3 What we do NOT know

| Unknown | Reason |
|---------|--------|
| Exact failing pytest node ID | No historical pytest output/transcript recovered |
| Exact traceback/assertion | No historical pytest output/transcript recovered |
| Whether it was `test_s1_load_board_include_archived_is_a_superset` | Plausible (reads live board), but unproven |
| Why it became green | Test file unchanged; board state may have changed naturally between runs |

### 3.4 Conclusion

**LIVE OFFICE FAILURE PROVENANCE NOT FULLY RECOVERED.**

The historical exact-reproduction acceptance criterion from Item-10 authority
remains UNPROVEN at the exact node-ID/traceback level.

Founder waiver is required to close Item 10 on current-state regression proof
(577/577 PASS) without the exact historical provenance.

---

## 4. py314 Scope Explanation

### 4.1 Pytest configuration

`pytest.ini` at repository root contains:

```ini
testpaths = tests
norecursedirs = py314
```

`tests/py314/` is **intentionally excluded** from the normal pytest regression suite.

### 4.2 Acceptance command scope

The Item-10 authority command:

> `python -m pytest tests/ -q`

uses the configured `pytest.ini`. Therefore `tests/py314/` is **not part of** the Item-10 regression universe.

### 4.3 py314 environment note

`tests/py314/test_quality_asymmetry_fetcher.py` has a pre-existing pandas ABI mismatch error (numpy cp314 binaries under Python 3.11 venv). This is:

- **EXCLUDED** from the Item-10 acceptance suite by `pytest.ini`
- Not an Item 1–9 regression
- Environment-dependent (requires system Python 3.14 or rebuilt numpy)

---

## 5. Exact Mutually Exclusive Collection Counts

### 5.1 By module

| Module | Path | Count |
|--------|------|-------|
| QAD contract conformance | `tests/qad/test_contract_conformance.py` | 105 |
| QAD persistence (6 modules) | `tests/qad/persistence/` | 236 |
| **QAD total** | | **341** |
| Locked API tests (18 files) | `tests/locked/` | 162 |
| Root tests (equity + capital) | `tests/test_*.py` (5 files) | 74 |
| **GRAND TOTAL** | | **577** |

**Proof of sum:**
- `105 + 236 = 341` (QAD total)
- `341 + 162 + 74 = 577` (grand total) ✅

### 5.2 QAD persistence submodules (exact collection counts)

| File | Count |
|------|-------|
| `tests/qad/persistence/test_persistence_core.py` | 100 |
| `tests/qad/persistence/test_primary_id_registry.py` | 9 |
| `tests/qad/persistence/test_admit_source_atomicity.py` | 28 |
| `tests/qad/persistence/test_evidence_admission_gate.py` | 35 |
| `tests/qad/persistence/test_financial_fact_lineage.py` | 37 |
| `tests/qad/persistence/test_canonical_serialization.py` | 27 |
| **QAD persistence total** | **236** |

### 5.3 Excluded by pytest.ini

| Path | Reason | Count |
|------|--------|-------|
| `tests/py314/` | `norecursedirs = py314` in `pytest.ini` | 5 tests (environment-specific) |

---

## 6. Corrected Regression Matrix

| Area | Frozen Item | Existing Tests | Positive Proof | Negative Proof | Regression Status |
|------|-------------|---------------|----------------|----------------|-------------------|
| Contract generation | M4A/M4B | 105 | schema→store, FK→REGISTRY, primary_id→registry | FAKE-99 rejection | ✅ GREEN |
| CanonicalRecordStore | Items 1,2,3 | 100 | store/load/list/contains/get_hash | tombstone exclusion, integrity conflict, batch duplicate, write to tombstoned rejected | ✅ GREEN |
| Transaction | Item 2 | (included in 100) | commit-phase atomicity, snapshot/restore | **validation failure** (FK/immutability/boundary/contract) → zero mutation, no rollback needed; **commit-phase failure** → snapshot/restore → zero partial state | ✅ GREEN |
| Serialization | Item 8 | 27 | deterministic hash, stable bytes, historical hash stability | NaN/+Infinity/-Infinity rejection, unsupported types fail-closed, no default=str | ✅ GREEN |
| FK enforcement | Item 1 | (included in 100) | single/collection/same-batch resolution | missing FK → validation failure → zero mutation | ✅ GREEN |
| Immutability | Item 3 | (included in 100) | mutable-field update, FIELD_IMMUTABLE enforcement | RECORD_IMMUTABLE violation → zero mutation | ✅ GREEN |
| Tombstone | Item 3 | (included in 100) | tombstone, is_tombstoned, load_historical | active reads exclude tombstoned; write to tombstoned → IntegrityConflict | ✅ GREEN |
| Version/history | Item 4 | (included in 100) | version preservation, load_version, v0001 labels | silent overwrite blocked; prior version auto-preserved | ✅ GREEN |
| RawSourceArchive | Item 5 | 28 | admit_source, content_hash binding, raw bytes, atomic metadata+bytes | SRC-01 direct store rejected, overwrite rejected, tombstone preserves history | ✅ GREEN |
| EvidenceRegistry | Item 6 | 35 | admit_evidence, EAR creation, source FK to RawSourceArchive | NEW EV-01 direct store rejected, EAR-01 direct store rejected, SRC-01 through ER rejected, model_copy bypass blocked, AI gate (original_source_verified=="true"), batch bypass blocked | ✅ GREEN |
| FinancialFactStore | Item 7 | 37 | FF lineage, NFF→FF formal lineage, CALC provenance, SCEN standalone | missing FF source → fail-closed, unresolved CALC provenance → failure, missing NFF parent → failure | ✅ GREEN |
| Protocol/docs | Item 9 | 0 (doc-only) | N/A | N/A | ✅ GREEN (doc-only) |
| Cross-contract | M4A/M4B/PIT | 105 (shared) | validator, schema constraints | FAKE-99 rejection | ✅ GREEN |

### 6.1 Transaction validation — correction note

The reference adapter's current behavior:

```
Persistence API prechecks (tombstone, batch identity, authority)
  → Transaction._validate() (canonical-boundary, contract, FK, immutability)
    → failure: zero mutation, no rollback needed
    → success: Snapshot → Commit → [fail → Restore → raise] → Done
```

**Validation failures** (FK violation, immutability violation, canonical-boundary violation, contract-validation violation) are caught **before any mutation** — no snapshot, no rollback, zero committed state.

**Commit-phase failures** use snapshot/restore rollback to guarantee zero partial state.

---

## 7. Independent CI Truth

| Check | Evidence |
|-------|----------|
| `.github/workflows/` directory | **DOES NOT EXIST** |
| GitHub combined status | Vercel deployment only |
| Python pytest CI | **NO INDEPENDENT PYTEST CI EVIDENCE** |
| Current proof | Local pytest only (577/577, this artifact) |

**Verdict:** The only regression proof is local pytest. No automated CI validates Python regression on push or PR.

---

## 8. Historical Test-Count Chronology

| Count | Date | Context |
|-------|------|---------|
| **401/401** (closeout claim) | 24 Aug 2026 | Original M5.2 closeout — reported 401/401 but actual was 400/401 with 1 failure |
| **400/401** (actual) | 24–25 Aug 2026 | Founder confirmed: 400 passed, 1 Live Office failure, exit 1 |
| **414/414** | 25 Aug (Item 1) | After primary-ID mechanical derivation fix |
| **422/422** | 25 Aug (Item 3) | After tombstone corrections |
| **449/449** | 26 Aug (Item 4) | After append-only version preservation |
| **469/469** | 26 Aug (Item 5) | After raw-source admission (byte binding) |
| **512/512** | 26 Aug (Item 6) | After evidence admission gate (1 no-op test removed) |
| **527/527** | 26 Aug (Item 7) | After financial-fact lineage |
| **550/550** | 28 Aug (Item 7 micro) | After read-isolation micro-closure |
| **568/568** | 28 Aug (Item 8 partial) | During fail-closed serialization |
| **577/577 CURRENT** | 28 Aug 2026 | After Item 8 proof closure; Item 9 doc-only (suite unchanged) |

---

## 9. Scope Declaration

| Property | Value |
|----------|-------|
| Production code changes | NONE |
| Executable test additions | NONE |
| Runtime behavior changes | NONE |
| Documents modified | THIS FILE ONLY |
| PROJECT_STATE update | Status: "Item 10 PROOF COMPLETE — CURRENT REGRESSION GREEN / HISTORICAL PROVENANCE INCOMPLETE / FOUNDER WAIVER REQUIRED" |
| pytest.ini modification | NONE |

**ITEM 10 — CURRENT REGRESSION GREEN / HISTORICAL FAILURE PROVENANCE INCOMPLETE / FOUNDER WAIVER REQUIRED**

**NOT CLOSED.** Items 11–14 **⏳ HOLD.** M5.3 **⏳ HOLD.**
<!-- 2026-08-28 23:55 UTC+7 -->