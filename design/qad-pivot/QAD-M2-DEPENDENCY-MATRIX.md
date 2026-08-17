# QAD-M2 — Dependency Matrix (Corrected)

> **Status:** M2 DEPENDENCY AUDIT = ACTIVE (M2 FINAL GOVERNANCE = PENDING — see closeout)
> **Purpose:** Verify that every capability proposed for freeze/supersession has no active runtime dependency that would be broken by the state change. Distinguish: historical reference ≠ runtime dependency ≠ governance authority.
> **Correction (18 Aug 2026):** Runtime dependencies audited per Founder review — Nick-Weekly cron, CIW monitor, Workforce runtime, and FROZEN-but-runtime-ACTIVE annotations added.

---

## Freeze Candidates — Dependency Verification

### 1. Alpha Momentum Pipeline (FROZEN)

| Dependency type | Found | Evidence | Impact |
|----------------|-------|----------|--------|
| Code imports | ✅ | `backend/adapters.py`, `backend/api/am_routes.py`, `fundamental-opportunity-v0/display.py`, `tests/locked/test_am_core_pipeline.py` | Read-only API serving frozen data; tests for regression. **No development dependency.** |
| API consumers | ✅ | Frontend `amClient.ts` → `/am-queue`, `/am-theme` | Frozen read-only surfaces. |
| **Cron jobs** | **✅ FOUND** | **Nick-Weekly Pipeline Run (AM EOD)** — weekly cron, last run AM-V0-20260816-150812, next 22 Aug 09:00 (per PROJECT_STATE). The cron **executes the AM pipeline itself** — this is active runtime use, not a downstream consumer. | **⚠ FREEZE SAFE for development; runtime execution continues. M3 must account for this cron in transition planning.** |
| Hermes profiles | ❌ | No profile depends on AM pipeline | OK |
| Schemas | ❌ | AM schemas are self-contained | OK |
| **Verdict** | **FREEZE SAFE (with runtime note)** | Read-only API + regression tests + Nick-Weekly cron execution are expected. **Do not disable the cron.** | |

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

### 9. Capital Intelligence Live Office (FROZEN production baseline — runtime operational)

| Dependency type | Evidence | Verdict |
|----------------|----------|---------|
| Dashboard | Serves at :9119 via detached VBS | ✅ **RUNTIME OPERATIONAL** — frozen for development only |
| WS events | Active — live state updates | ✅ Operational |
| Kanban board | Active — kanban/boards/iip | ✅ Operational |
| **Verdict** | **FREEZE SAFE for development; runtime continues** | |

---

## ACTIVE / TRANSITIONAL Dependencies — Full Coverage

### Radar Scout (TRANSITIONAL) — CAP-011

| Dependency | Type | Stability |
|------------|------|-----------|
| Cron `8ba233e88015` (Mon 08:00) | Runtime | ✅ Active — no change |
| Cron `cda817d17236` (Thu 08:00) | Runtime | ✅ Active — no change |
| org-radar-scout profile | Runtime | ✅ Active — no change |
| kanban Inbox → CoS triage | Workflow | ✅ Active — no change |
| evidence/radar/digests/ | Data | ✅ Active — no change |
| card-outcomes register | Governance | ✅ Active — no change |
| Hermes scheduler (job registration) | Runtime | ✅ Active |
| EDGAR filings scan (FD #81) | Data | ✅ Active |
| **M2 restriction:** No cron change, no profile rename, no freeze | | **✅ Compliant** |

### Shared Equity Universe (ACTIVE) — CAP-001

| Dependency | Type | Stability |
|------------|------|-----------|
| Equity Inflection Scanner (universe list) | Runtime | ✅ ACTIVE |
| Quality & Asymmetry Discovery (universe source) | Runtime | ✅ ACTIVE |
| FO pipeline (frozen, historical reference) | Runtime | ✅ FROZEN consumer |
| Backend test fixtures | Test | ✅ Locked tests |
| **M2 restriction:** Keep active; must not be frozen | | **✅ Compliant** |

### Equity Inflection Scanner (ACTIVE) — CAP-002

| Dependency | Type | Stability |
|------------|------|-----------|
| Shared Equity Universe | Runtime | ✅ ACTIVE |
| yfinance + SEC EDGAR (via Source Adapters — FROZEN) | Data | ✅ Active runtime |
| Radar Scout (Task Idea Card packaging) | Workflow | ✅ TRANSITIONAL |
| CoS triage → Research Mandates | Workflow | ✅ ACTIVE |
| Hermes scheduler (standing scanner) | Runtime | ✅ ACTIVE |
| `discovery/equity_inflection/` code | Code | ✅ ACTIVE |
| Locked tests (17 + 8 validation) | Test | ✅ PASS |
| **M2 restriction:** Keep running; must NOT become canonical definition of QAD Dislocation | | **✅ Compliant** |

### Quality & Asymmetry Discovery (ACTIVE, shadow/evidence-only) — CAP-003

| Dependency | Type | Stability |
|------------|------|-----------|
| Shared Equity Universe | Runtime | ✅ ACTIVE |
| SEC EDGAR + yfinance (via Source Adapters — FROZEN) | Data | ✅ Active runtime |
| `discovery/quality_asymmetry/` code | Code | ✅ ACTIVE |
| Locked tests (10) | Test | ✅ PASS |
| **No downstream consumer** (evidence-only firewall) | — | ✅ By design |
| **M2 restriction:** Keep as shadow; no auto-cards/publish | | **✅ Compliant** |

### Deep Research Standing Contract (ACTIVE) — CAP-012

| Dependency | Type | Stability |
|------------|------|-----------|
| Template 16 document | Code | ✅ ACTIVE |
| IC Secretary (instantiates per RM) | Workflow | ✅ ACTIVE |
| CRO + Auditor workforce roles | Workflow | ✅ ACTIVE |
| None (template only — no runtime cron/API) | Runtime | ✅ Template-only |
| **M2 restriction:** Keep active; M3 extends into QAD Research Protocol | | **✅ Compliant** |

### Blog / Report Infrastructure (ACTIVE) — CAP-013

| Dependency | Type | Stability |
|------------|------|-----------|
| Backend `/api/reports` | API | ✅ ACTIVE |
| Frontend `/library`, `/library/:slug` | Frontend | ✅ ACTIVE |
| `reports/` directory contract | Data | ✅ ACTIVE |
| IPM (via IPM-FD-003, one-way) | Consumer | ✅ ACTIVE |
| Vercel production deployment | Runtime | ✅ ACTIVE |
| npm build (report type validation) | Build | ✅ PASS |
| **M2 restriction:** Keep active; M11 adds PDF generation | | **✅ Compliant** |

### Thai Editorial Standard (ACTIVE) — CAP-014

| Dependency | Type | Stability |
|------------|------|-----------|
| IC Secretary (editor role) | Workflow | ✅ ACTIVE |
| `reports/THAI-RESEARCH-EDITORIAL-STANDARD.md` | Code | ✅ ACTIVE |
| All published reports (24 Thai) | Data | ✅ ACTIVE |
| **M2 restriction:** Keep active; M11 extends with long-form PDF standard | | **✅ Compliant** |

### Research Audit Infrastructure (ACTIVE) — CAP-016

| Dependency | Type | Stability |
|------------|------|-----------|
| Backend `/api/decisions`, `/api/audit/*`, `/api/org-queue` | API | ✅ ACTIVE |
| Frontend `/audit` (Decision Register, Audit Center, Model Registry) | Frontend | ✅ ACTIVE |
| `backend/audit_store.py`, `backend/org_store.py` | Code | ✅ ACTIVE |
| `evidence/` directory | Data | ✅ ACTIVE |
| Locked tests | Test | ✅ PASS |
| **M2 restriction:** Keep active; M10 extends | | **✅ Compliant** |

### Evidence Doctrine / Model Infrastructure (ACTIVE) — CAP-017

| Dependency | Type | Stability |
|------------|------|-----------|
| `operational/EVIDENCE-DOCTRINE.md` | Code | ✅ ACTIVE |
| `project-definition/EVIDENCE-MODEL.md` | Code | ✅ ACTIVE |
| Constitution §8 | Governance | ✅ ACTIVE |
| All research workflows (evidence separation, PIT, provenance) | Workflow | ✅ ACTIVE |
| Every research mandate | Consumer | ✅ ACTIVE |
| **M2 restriction:** Keep active; M3 spec #4 extends | | **✅ Compliant** |

### Hermes AI Workforce (ACTIVE — QAD remapping deferred) — CAP-018

| Dependency | Type | Stability |
|------------|------|-----------|
| 10 org-* Principal profiles | Runtime | ✅ ACTIVE — daily operations |
| 10 Assistant subagent contracts | Runtime | ✅ ACTIVE |
| Hermes Capital Intelligence board | Runtime | ✅ ACTIVE |
| kanban workflow (card states, lanes) | Workflow | ✅ ACTIVE |
| cron jobs (Radar, CIW monitor, Nick-Weekly) | Runtime | ✅ ACTIVE — scheduled |
| Holds mechanism | Governance | ✅ ACTIVE |
| Locked tests (org-workflow API) | Test | ✅ PASS |
| **M2 restriction:** Do not remap. M3 logical contracts first, then migration map. | | **✅ Compliant** |

---

## FROZEN Capabilities with Active Runtime Use

### SEC EDGAR / Source Adapters (CAP-020) — FROZEN for standalone development

| Runtime Consumer | Dependency Type | Status |
|-----------------|----------------|--------|
| Equity Inflection Scanner (CAP-002 — ACTIVE) | Data fetch (yfinance + EDGAR) | ✅ Active |
| Quality & Asymmetry Discovery (CAP-003 — ACTIVE) | Data fetch | ✅ Active |
| FO Pipeline (CAP-007 — FROZEN) | Historical data | ✅ FROZEN consumer |
| II Pipeline (CAP-008 — FROZEN) | 13F filings | ✅ FROZEN consumer |
| AM Pipeline (CAP-004 — FROZEN) | Historical data | ✅ FROZEN consumer |
| **M2 consequence:** FROZEN ≠ safe-to-disable. Must remain operational until all ACTIVE consumers migrated. | | |

### CIW (CAP-009) — FROZEN for implementation, ABSORB disposition

| Runtime Component | Dependency Type | Status |
|-----------------|----------------|--------|
| CIW MSFT Class A monitoring cron (Mon 09:00) | Runtime | ✅ ACTIVE — next 24 Aug |
| Audit center references (CIW artifact links) | API | ✅ ACTIVE read-only |
| Org Workflow API (artifact references) | API | ✅ ACTIVE |
| Research Artifact Detail page | Frontend | ✅ ACTIVE |
| **M2 consequence:** The monitoring cron must continue. CIW Research Framework = FROZEN, but monitor = ACTIVE until QAD M12 subsumes it. | | |

### Capital Intelligence Live Office (CAP-015) — FROZEN production baseline

| Runtime Component | Dependency Type | Status |
|-----------------|----------------|--------|
| Hermes Dashboard :9119 | Runtime | ✅ Operational via VBS |
| Kanban board (kanban/boards/iip) | Data | ✅ Active |
| WS live events | Runtime | ✅ Active |
| Founder monitoring dashboard | User | ✅ Active |
| **M2 consequence:** No further development, but runtime continues. | | |

---

## Cross-Capability Dependency Map (Corrected Runtime View)

```
Shared Equity Universe (ACTIVE)
  ├─→ Equity Inflection Scanner (ACTIVE)         ← runtime
  ├─→ Quality & Asymmetry Discovery (ACTIVE)     ← runtime
  └─→ FO Pipeline (FROZEN)                       ← historical reference

SEC EDGAR / Source Adapters (FROZEN — runtime ACTIVE for consumers)
  ├─→ AM Pipeline (FROZEN)                       ← historical
  ├─→ FO Pipeline (FROZEN)                       ← historical
  ├─→ II Pipeline (FROZEN)                       ← historical
  ├─→ Equity Inflection Scanner (ACTIVE)         ← runtime ⟵ LIVE
  └─→ Quality & Asymmetry Discovery (ACTIVE)     ← runtime ⟵ LIVE

Radar Scout (TRANSITIONAL)
  ├─→ kanban Inbox → CoS triage → Research Mandates  ← runtime
  ├─→ evidence/radar/digests/ (data archive)          ← runtime
  └─→ [Nick-Weekly AM EOD cron] (separate pipeline, not Radar-dependent)

CIW (FROZEN — monitor ACTIVE)
  ├─→ Audit store (ACTIVE)                             ← read-only
  ├─→ Org workflow API (ACTIVE)                        ← read-only
  └─→ CIW MSFT Class A monitoring (ACTIVE)             ← runtime ⟵ LIVE

Hermes AI Workforce (ACTIVE)
  ├─→ All org-* profiles (ACTIVE)                      ← runtime
  ├─→ Kanban board (ACTIVE)                            ← runtime
  ├─→ Cron jobs ×4 (ACTIVE)                            ← runtime
  └─→ All published research workflows                 ← runtime

Alpha Momentum Pipeline (FROZEN — Nick-Weekly runtime)
  ├─→ Backend read-only API (FROZEN)                   ← frozen
  ├─→ Frontend frozen surfaces (FROZEN)                ← frozen
  └─→ Nick-Weekly EOD cron (ACTIVE)                    ← runtime ⟵ LIVE

Research Audit Infrastructure (ACTIVE)
  ├─→ Decision Register (ACTIVE)
  ├─→ Model Registry (ACTIVE)
  └─→ Audit Center (ACTIVE)

Blog / Report Infrastructure (ACTIVE)
  ├─→ Library index (ACTIVE)
  ├─→ Report article pages (ACTIVE)
  └─→ Vercel deployment (ACTIVE)
```

---

## State Transition Rules (M2)

| Current State | Can Transition To | Condition |
|---------------|-------------------|-----------|
| ACTIVE | FROZEN, SUPERSEDED | Founder decision + dependency audit |
| FROZEN | VERIFIED_UNUSED | Dependency audit proves **no active runtime dependency** (cron, API consumer, workforce, data consumer all verified) |
| VERIFIED_UNUSED | ARCHIVED | Physical archival operation (separate authorization) |
| TRANSITIONAL | FROZEN, ACTIVE | Evidence-based decision (e.g., Radar vs QAD Discovery comparison) |
| SUPERSEDED | FROZEN | Authority migration complete |

> **⚠ FROZEN ≠ safe-to-disable.** A FROZEN capability with active runtime use (cron, API consumers, data dependencies) must continue operating until all ACTIVE consumers are migrated. See FROZEN-with-runtime-use section above.

**No direct transitions:** ACTIVE → ARCHIVED (must go through FROZEN → VERIFIED_UNUSED → ARCHIVED). TRANSITIONAL → ARCHIVED (must go through FROZEN first).

<!-- 2026-08-18 00:36 UTC+7 -->