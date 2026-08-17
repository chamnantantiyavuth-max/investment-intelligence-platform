# QAD-M2 — Dependency Matrix

> **Status:** M2 = PASS (2026-08-17)
> **Purpose:** Verify that every capability proposed for freeze/supersession has no active runtime dependency that would be broken by the state change. Distinguish: historical reference ≠ runtime dependency ≠ governance authority.

---

## Freeze Candidates — Dependency Verification

### 1. Alpha Momentum Pipeline (FROZEN)

| Dependency type | Found | Evidence | Impact |
|----------------|-------|----------|--------|
| Code imports | ✅ | `backend/adapters.py`, `backend/api/am_routes.py`, `fundamental-opportunity-v0/display.py`, `tests/locked/test_am_core_pipeline.py` | Read-only API serving frozen data; tests for regression. **No development dependency.** |
| API consumers | ✅ | Frontend `amClient.ts` → `/am-queue`, `/am-theme` | Frozen read-only surfaces. |
| Cron jobs | ❌ | No active cron depends on AM pipeline (Nick-Weekly is AM EOD refresh — pipeline runs itself, not a consumer) | OK |
| Hermes profiles | ❌ | No profile depends on AM pipeline | OK |
| Schemas | ❌ | AM schemas are self-contained | OK |
| **Verdict** | **FREEZE SAFE** | Read-only API + regression tests are expected; no active development dependency | |

### 2. Alpha Momentum Theme Infrastructure (FROZEN)

| Dependency type | Evidence | Verdict |
|----------------|----------|---------|
| Code imports | None (theme infrastructure is self-contained) | ✅ FREEZE SAFE |
| API consumers | Theme-first research queue no longer active | ✅ |
| **Verdict** | **FREEZE SAFE** | |

### 3. Theme Anomaly/Weak Signal (FROZEN)

| Dependency type | Evidence | Verdict |
|----------------|----------|---------|
| Code imports | `alpha-momentum-v0/experimental/` — self-contained | ✅ FREEZE SAFE |
| API consumers | None (experimental module, no production API) | ✅ |
| **Verdict** | **FREEZE SAFE** | |

### 4. FO Pipeline (FROZEN as strategy)

| Dependency type | Evidence | Verdict |
|----------------|----------|---------|
| Code imports | `backend/adapters.py`, `backend/api/fo_routes.py`, locked tests | ✅ Read-only API, regression tests |
| API consumers | Frontend `foClient.ts` → `/fo-queue`, `/fo-package`, `/fo-cheap-quality` | ✅ Frozen surfaces |
| Methodology reuse | Moat, Earnings Quality, Marx signals — methodology only, not pipeline code | ✅ ADAPT is separate capability |
| **Verdict** | **FREEZE SAFE** | |

### 5. II Pipeline (FROZEN as strategy)

| Dependency type | Evidence | Verdict |
|----------------|----------|---------|
| Code imports | `backend/adapters.py`, `backend/api/ii_routes.py`, locked tests | ✅ Read-only API, regression tests |
| API consumers | Frontend `iiClient.ts` → `/institutional` | ✅ Frozen surface |
| 13F data reuse | Data fetch + CUSIP mapping — methodology available for QAD evidence input | ✅ ADAPT is separate capability |
| **Verdict** | **FREEZE SAFE** | |

### 6. CS Product Radar (FROZEN)

| Dependency type | Evidence | Verdict |
|----------------|----------|---------|
| Code imports | `backend/adapters.py`, `backend/api/cs_routes.py`, `discovery/cs_product/discovery.py` | ✅ Read-only API |
| API consumers | Frontend `csClient.ts` → `/cs-radar`, `/cs-radar/:productId` | ✅ Frozen surfaces |
| **Verdict** | **FREEZE SAFE** | |

### 7. CS Product Discovery (FROZEN / DO_NOT_REUSE)

| Dependency type | Evidence | Verdict |
|----------------|----------|---------|
| Code imports | `discovery/cs_product/discovery.py` (self-contained) | ✅ FREEZE SAFE |
| Downstream | None (commodity-specific, not mapping to QAD Dislocation) | ✅ |
| **Verdict** | **FREEZE SAFE** | |

### 8. Frontend Legacy Surfaces (FROZEN)

| Dependency type | Evidence | Verdict |
|----------------|----------|---------|
| API clients | 4 clients (amClient, foClient, csClient, iiClient) — serve frozen read-only data | ✅ FROZEN (no new development) |
| Build | `npm run build` exit 0 | ✅ |
| **Verdict** | **FROZEN SAFE** | |

---

## TRANSITIONAL / ACTIVE Dependencies

### Radar Scout (TRANSITIONAL)

| Dependency | Type | Stability |
|------------|------|-----------|
| Cron `8ba233e88015` (Mon 08:00) | Runtime | ✅ Active — no change |
| Cron `cda817d17236` (Thu 08:00) | Runtime | ✅ Active — no change |
| org-radar-scout profile | Runtime | ✅ Active — no change |
| kanban Inbox → CoS triage | Workflow | ✅ Active — no change |
| evidence/radar/digests/ | Data | ✅ Active — no change |
| card-outcomes register | Governance | ✅ Active — no change |
| **M2 restriction:** No cron change, no profile rename, no freeze | | **✅ Compliant** |

### Shared Equity Universe (ACTIVE)

| Dependency | Type | Stability |
|------------|------|-----------|
| Equity Inflection Scanner (universe list) | Runtime | ✅ ACTIVE |
| Quality & Asymmetry Discovery (universe source) | Runtime | ✅ ACTIVE |
| FO pipeline (frozen, historical reference) | Runtime | ✅ FROZEN consumer |
| **M2 restriction:** Keep active; must not be frozen | | **✅ Compliant** |

### Equity Inflection Scanner (ACTIVE)

| Dependency | Type | Stability |
|------------|------|-----------|
| Shared Equity Universe | Runtime | ✅ ACTIVE |
| yfinance + SEC EDGAR | Data | ✅ ACTIVE |
| Radar Scout (Task Idea Card packaging) | Workflow | ✅ TRANSITIONAL |
| CoS triage → Research Mandates | Workflow | ✅ ACTIVE |
| **M2 restriction:** Keep running; must NOT become canonical definition of QAD Dislocation | | **✅ Compliant** |

---

## Cross-Capability Dependency Map

```
Shared Equity Universe (ACTIVE)
  ├─→ Equity Inflection Scanner (ACTIVE)
  ├─→ Quality & Asymmetry Discovery (ACTIVE)
  └─→ FO Pipeline (FROZEN)

SEC EDGAR / Source Adapters (FROZEN — ADAPT methodology)
  ├─→ AM Pipeline (FROZEN)
  ├─→ FO Pipeline (FROZEN)
  ├─→ II Pipeline (FROZEN)
  ├─→ Equity Inflection Scanner (ACTIVE)
  └─→ Quality & Asymmetry Discovery (ACTIVE)

Radar Scout (TRANSITIONAL)
  ├─→ kanban Inbox → CoS triage → Research Mandates
  └─→ evidence/radar/digests/ (data archive)

CIW (FROZEN — ABSORB lineage)
  ├─→ Audit store (ACTIVE)
  └─→ Org workflow API (ACTIVE)

Research Audit Infrastructure (ACTIVE)
  ├─→ Decision Register (ACTIVE)
  ├─→ Model Registry (ACTIVE)
  └─→ Audit Center (ACTIVE)

Blog / Report Infrastructure (ACTIVE)
  └─→ Library index (ACTIVE)
  └─→ Report article pages (ACTIVE)
```

---

## State Transition Rules (M2)

| Current State | Can Transition To | Condition |
|---------------|-------------------|-----------|
| ACTIVE | FROZEN, SUPERSEDED | Founder decision + dependency audit |
| FROZEN | VERIFIED_UNUSED | Dependency audit proves no active dependency |
| VERIFIED_UNUSED | ARCHIVED | Physical archival operation (separate authorization) |
| TRANSITIONAL | FROZEN, ACTIVE | Evidence-based decision (e.g., Radar vs QAD Discovery comparison) |
| SUPERSEDED | FROZEN | Authority migration complete |

**No direct transitions:** ACTIVE → ARCHIVED (must go through FROZEN → VERIFIED_UNUSED → ARCHIVED). TRANSITIONAL → ARCHIVED (must go through FROZEN first).

<!-- 2026-08-17 17:30 UTC+7 -->