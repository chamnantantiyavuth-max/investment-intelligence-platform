# QAD-M2 — Legacy Capability Registry

> **Status:** M2 TECHNICAL CLOSEOUT = **PASS** (commit `548a89d`, 17 Aug 2026)
> **M2 FINAL GOVERNANCE = PASS** (validation 18 Aug 2026: deterministic integrity checks all pass)
> **M3 = READY FOR FOUNDER AUTHORIZATION**
> **Lifecycle states:** ACTIVE / FROZEN / SUPERSEDED / TRANSITIONAL / VERIFIED_UNUSED / ARCHIVED
> **Disposition vocabulary:** REUSE / ADAPT / ABSORB / TRANSITIONAL_RETAIN / FREEZE / SUPERSEDE / DO_NOT_REUSE
> **Corrections applied** (18 Aug 2026): axes separated, child IDs assigned, CAP-018→ACTIVE, runtime annotations added, dispositions normalized to ONE primary_disposition per capability. Validation script `validate-registry.py` confirms 25/25 records deterministic.

---

## 1. Shared Equity Universe

| Field | Value |
|-------|-------|
| **capability_id** | CAP-001 |
| **source_module** | `discovery/equity_universe.py` |
| **current_authority** | FD #95, FD #130 |
| **current_state** | **ACTIVE** |
| **primary_disposition** | REUSE |
| **QAD_target_capability** | Quality Universe seed; Security Master / Researchable Universe registry foundation |
| **reusable_data** | 98 CIK-verified names, ADR flags, PIT identity, SEC company_tickers mapping |
| **reusable_logic** | CIK verification, entity resolution, membership derivation |
| **active_dependencies** | `equity_inflection/fetcher.py` (FO_UNIVERSE derived from shared layer), `quality_asymmetry/` (universe source) |
| **downstream_consumers** | Equity Inflection Scanner, Quality & Asymmetry Discovery, FO pipeline (frozen) |
| **historical_value** | Baseline for PIT discovery evaluation |
| **replacement_required** | No — QAD Quality Universe will be superset |
| **verification_status** | ✅ 10 locked tests pass |
| **archival_preconditions** | After QAD Quality Universe supersedes it and all consumers migrated |
| **governing_FD/spec** | FD #95, FD #130; QAD-DISCOVERY-AND-COVERAGE-OPERATING-REQUIREMENT.md B2 |

## 2. Equity Inflection Scanner

| Field | Value |
|-------|-------|
| **capability_id** | CAP-002 |
| **source_module** | `discovery/equity_inflection/` |
| **current_authority** | FD #88/#89 |
| **current_state** | **ACTIVE** (standing scanner) |
| **primary_disposition** | ADAPT |
| **QAD_target_capability** | Dislocation Radar input — EPS breakout detection |
| **reusable_data** | Historical PIT scan results, validation evidence pack |
| **reusable_logic** | Deterministic EPS breakout + revenue confirmation + Stage Definition v0.1 |
| **active_dependencies** | Shared Equity Universe (CAP-001) for FO_UNIVERSE; yfinance + SEC EDGAR |
| **downstream_consumers** | Radar Scout (Task Idea Card packaging); CoS triage; Research Mandates (RM-####) |
| **historical_value** | Scanner validation evidence for M4B evaluation |
| **replacement_required** | No — keep as one Dislocation-Radar input; must NOT become the canonical definition of QAD Dislocation |
| **verification_status** | ✅ 17 locked tests + 8 validation tests |
| **archival_preconditions** | After QAD Dislocation Radar (M5) can reproduce or supersede its output |
| **governing_FD/spec** | FD #88/#89, FD #130; QAD-DISCOVERY-AND-COVERAGE-OPERATING-REQUIREMENT.md B6 |

## 3. Quality & Asymmetry Discovery

| Field | Value |
|-------|-------|
| **capability_id** | CAP-003 |
| **source_module** | `discovery/quality_asymmetry/` |
| **current_authority** | FD #95 |
| **current_state** | **ACTIVE** (shadow/evidence-only) |
| **primary_disposition** | ADAPT |
| **QAD_target_capability** | Quality Discovery precursor — 4 archetype lenses (Durable Compounder / 100-Bagger / Mispriced Quality / Asymmetric Value) |
| **reusable_data** | 62 evidence blocks, archetype classification results |
| **reusable_logic** | Deterministic engine, no score (threshold PROPOSED FD #53) |
| **active_dependencies** | Shared Equity Universe (CAP-001); SEC EDGAR + yfinance |
| **downstream_consumers** | None (evidence-only firewall — never auto-cards/publish) |
| **historical_value** | Archetype evaluation methodology for QAD Quality Discovery |
| **replacement_required** | No — QAD-M5 will extend with QAD-specific quality protocol |
| **verification_status** | ✅ 10 locked tests |
| **archival_preconditions** | After QAD Quality Discovery (M5) subsumes its methodology |
| **governing_FD/spec** | FD #95, FD #130; QAD-DISCOVERY-AND-COVERAGE-OPERATING-REQUIREMENT.md B5 |

## 4. Alpha Momentum Pipeline

| Field | Value |
|-------|-------|
| **capability_id** | CAP-004 |
| **source_module** | `alpha-momentum-v0/` |
| **current_authority** | FD #65 (freeze), FD #130 (superseded as strategy) |
| **current_state** | **FROZEN** |
| **runtime_use** | **CRON EXECUTION** — Nick-Weekly Pipeline Run (AM EOD) weekly cron executes the pipeline. Last run AM-V0-20260816-150812, next 22 Aug 09:00. |
| **primary_disposition** | FREEZE |
| **reuse_policy** | DO_NOT_REUSE_MOMENTUM_LOGIC |
| **QAD_target_capability** | NONE — momentum screening, Stage Analysis, theme ranking not reusable |
| **reusable_data** | Historical candidate/theme data for evaluation; equity security metadata (symbols, exchanges) |
| **reusable_logic** | NONE (momentum logic is fundamental/impairment analysis opposite) |
| **active_dependencies** | `backend/adapters.py` (read-only API serving frozen data), `backend/api/am_routes.py` |
| **downstream_consumers** | Frontend `/am-queue`, `/am-theme` (frozen read-only surfaces); locked tests for regression |
| **historical_value** | Pipeline output for historical comparison; PIT evaluation fixture source |
| **replacement_required** | N/A — frozen as-is |
| **verification_status** | ✅ Locked tests pass (regression protection) |
| **archival_preconditions** | VERIFIED_UNUSED after QAD reaches production and no active test/API dependency remains |
| **governing_FD/spec** | FD #65 (#66 freeze), FD #130 (§13 SUPERSEDED) |

## 5. Alpha Momentum Theme Infrastructure

| Field | Value |
|-------|-------|
| **capability_id** | CAP-005 |
| **source_module** | `alpha-momentum-v0/` (Theme Cards, Controlled Theme Set) |
| **current_authority** | FD #65, FD #130 |
| **current_state** | **FROZEN** |
| **primary_disposition** | FREEZE |
| **QAD_target_capability** | NONE — Theme-first gateway is superseded |
| **reusable_data** | Theme definitions as historical reference |
| **reusable_logic** | NONE |
| **active_dependencies** | None (theme infrastructure is self-contained within frozen module) |
| **downstream_consumers** | None (theme-first research queue no longer active) |
| **historical_value** | Legacy theme structure for reference |
| **replacement_required** | N/A — frozen |
| **verification_status** | ✅ No active test failures |
| **archival_preconditions** | VERIFIED_UNUSED after QAD supersedes all theme references |
| **governing_FD/spec** | FD #65, FD #130 (§14 superseded) |

## 6. Theme Intelligence — Weak Signal / Anomaly / Hypothesis

| Field | Value |
|-------|-------|
| **capability_id** | CAP-006 |
| **source_module** | `alpha-momentum-v0/experimental/` (radar.py, anomaly detection, hypothesis engine, weak signal inbox) |
| **current_authority** | FD #27, FD #130 |
| **current_state** | **FROZEN** |
| **primary_disposition** | ADAPT (methodology only, not code) |
| **QAD_target_capability** | Supporting QAD discovery input — anomaly detection methodology may signal dislocation candidates |
| **reusable_data** | None (frozen anomaly data is historical) |
| **reusable_logic** | Anomaly detection methodology (model-agnostic) — import methodology if QAD-M5 needs it |
| **active_dependencies** | None (experimental module, no production API consumers) |
| **downstream_consumers** | None |
| **historical_value** | Proof-of-concept for AI-driven anomaly detection |
| **replacement_required** | No — QAD Dislocation Radar (M5) is a new design, not evolution |
| **verification_status** | ✅ Locked tests pass (circular guard, inbox) |
| **archival_preconditions** | After QAD-M5 anomaly/dislocation detection is operational |
| **governing_FD/spec** | FD #27, FD #130 (§5 Theme = supporting) |

## 7. Fundamental & Opportunity Pipeline

| Field | Value |
|-------|-------|
| **capability_id** | CAP-007 |
| **source_module** | `fundamental-opportunity-v0/` |
| **current_authority** | FD #40, FD #65 (freeze as strategy), FD #130 |
| **current_state** | **FROZEN** (as strategy pipeline) |
| **primary_disposition** | FREEZE (as strategy) |
| **QAD_target_capability** | Individual analytical methods may be adapted into QAD Fundamental Analysis (M8) |
| **reusable_data** | 8-company fundamental data (yfinance), pipeline output |
| **reusable_logic** | Sub-capabilities below (7a–7d) |
| **active_dependencies** | `backend/adapters.py` (read-only API), `backend/api/fo_routes.py`, locked tests |
| **downstream_consumers** | Frontend `/fo-queue`, `/fo-package`, `/fo-cheap-quality` (frozen read-only surfaces) |
| **historical_value** | Fundamental analysis methodology baseline |
| **replacement_required** | Yes — superseded by QAD-M8 Business Quality + Financial Reconstruction |
| **verification_status** | ✅ Locked tests pass |
| **archival_preconditions** | After QAD-M8 materializes and consumers migrated |
| **governing_FD/spec** | FD #40, FD #65, FD #130 |

### 7a. Moat Classification (6 types + Width/Depth/Trend) — CAP-007A

| Field | Value |
|-------|-------|
| **capability_id** | CAP-007A |
| **current_state** | **FROZEN** (methodology available) |
| **primary_disposition** | ADAPT |
| **QAD_target_capability** | QAD-M8 Business Quality will inherit 6-type moat framework (spec §3.4.1) and extend with Moat Mechanism Protocol |
| **replacement_required** | No — inherit methodology |

### 7b. Earnings Quality (HIGH/MEDIUM/LOW/COSMETIC) — CAP-007B

| Field | Value |
|-------|-------|
| **capability_id** | CAP-007B |
| **current_state** | **FROZEN** (methodology available) |
| **primary_disposition** | ADAPT |
| **QAD_target_capability** | QAD-M8 Financial Reconstruction will adopt Earnings Quality framework |
| **replacement_required** | No — adopt methodology |

### 7c. Value Trap Detector (5-question) — CAP-007C

| Field | Value |
|-------|-------|
| **capability_id** | CAP-007C |
| **current_state** | **SUPERSEDED** |
| **primary_disposition** | SUPERSEDE |
| **QAD_target_capability** | Replaced by QAD-M8 Impairment Diagnosis (Temporary/Mostly/Mixed/Structural/Unresolved) |
| **replacement_required** | Yes — QAD Impairment Diagnosis supersedes |

### 7d. Marx Signals (Profit Rate Trend + Narrative Gap) — CAP-007D

| Field | Value |
|-------|-------|
| **capability_id** | CAP-007D |
| **current_state** | **FROZEN** (informational) |
| **primary_disposition** | FREEZE |
| **QAD_target_capability** | Not directly needed; keep as informational. If useful, import methodology |
| **replacement_required** | No — granular impairment diagnosis replaces |

## 8. Institutional Intelligence / 13F Pipeline

| Field | Value |
|-------|-------|
| **capability_id** | CAP-008 |
| **source_module** | `institutional-intelligence-v0/` |
| **current_authority** | FD #42, FD #65, FD #130 |
| **current_state** | **FROZEN** (as strategy pipeline) |
| **primary_disposition** | FREEZE (as strategy) |
| **reuse_policy** | ADAPT_DATA_AS_EVIDENCE_INPUT |
| **QAD_target_capability** | 13F institutional conviction data as evidence input for QAD Business Quality analysis |
| **reusable_data** | Real 13F holdings data, super-investor watchlist, conviction signals |
| **reusable_logic** | Data fetching (SEC EDGAR), CUSIP mapping, conviction calculation |
| **active_dependencies** | `backend/adapters.py` (read-only API), `backend/api/ii_routes.py`, locked tests |
| **downstream_consumers** | Frontend `/institutional` (frozen read-only surface) |
| **historical_value** | 13F historical data for evaluation |
| **replacement_required** | No — 13F data remains usable as evidence input; not an independent QAD strategy authority |
| **verification_status** | ✅ Locked tests pass |
| **archival_preconditions** | After QAD Evidence Lead (M6/M7) has its own 13F data pipeline |
| **governing_FD/spec** | FD #42, FD #65, FD #130 |

## 9. Company Intelligence Workbench (CIW)

| Field | Value |
|-------|-------|
| **capability_id** | CAP-009 |
| **source_module** | `project-definition/company-intelligence-workbench/`, `docs/ciw-pilot-msft/` |
| **current_authority** | FD-CIW-001..016, FD #130 |
| **current_state** | **FROZEN** (pilot complete; full implementation deferred; **CIW MSFT monitoring runtime still ACTIVE** — see runtime_use below) |
| **primary_disposition** | ABSORB |
| **QAD_target_capability** | QAD Full Research Protocol evolves from CIW Research Framework (Modules A–Q). CIW Result Contract + Quality Gates directly reusable. |
| **reusable_data** | MSFT research-result v1 + v2, monitoring artifacts, CRR records |
| **reusable_logic** | Research Framework (Modules A–Q), Result Contract, Quality Gates, Source Map methodology |
| **runtime_use** | CIW MSFT Class A monitoring cron (Mon 09:00 UTC+7) = **ACTIVE** — next 24 Aug 2026. Research Framework / Modules A–Q = FROZEN. The monitor validates QAD-readiness without alert fatigue. After QAD monitoring (M12) subsumes it, the cron may be retired. |
| **active_dependencies** | `backend/audit_store.py` (audit center references CIW artifacts), `backend/org_store.py`, `discovery/quality_asymmetry/archetypes.py` (reference), `tests/locked/test_org_workflow_api.py`; CIW monitor cron (Hermes scheduler) |
| **downstream_consumers** | Audit center (`/audit`), Org Workflow API (artifact references), Research Artifact Detail |
| **historical_value** | First full research workflow pilot; lineage for QAD evolution |
| **replacement_required** | No — absorb into QAD Research Protocol; preserve lineage |
| **verification_status** | ✅ Locked tests pass |
| **archival_preconditions** | After QAD-M3 Domain Contracts materialize CIW inheritance |
| **governing_FD/spec** | FD-CIW-001..016, FD #130; QAD-M3 spec #3 (QAD-FULL-RESEARCH-PROTOCOL.md) |

## 10. Close System Product Radar

| Field | Value |
|-------|-------|
| **capability_id** | CAP-010 |
| **source_module** | `close_system/` |
| **current_authority** | FD #39, FD #57, FD #130 |
| **current_state** | **FROZEN** (synthetic-labeled, read-only API) |
| **primary_disposition** | FREEZE |
| **QAD_target_capability** | NONE — commodity macro products, not QAD company-specific equity analysis |
| **reusable_data** | None (synthetic data only) |
| **reusable_logic** | NONE |
| **active_dependencies** | `backend/adapters.py` (read-only API), `backend/api/cs_routes.py`, `discovery/cs_product/discovery.py` |
| **downstream_consumers** | Frontend `/cs-radar`, `/cs-radar/:productId` (frozen read-only surfaces); locked tests |
| **historical_value** | Commodity macro product reference |
| **replacement_required** | N/A — not mapping to QAD Dislocation |
| **verification_status** | ✅ Locked tests pass |
| **archival_preconditions** | After QAD Dislocation Radar (M5) is operational and no consumer depends on CS data |
| **governing_FD/spec** | FD #39, FD #57, FD #130 |

### 10a. CS Product Discovery (FD #97)

| Field | Value |
|-------|-------|
| **capability_id** | CAP-010A |
| **source_module** | `discovery/cs_product/` |
| **current_state** | **FROZEN** |
| **primary_disposition** | DO_NOT_REUSE |
| **QAD_target_capability** | NONE — commodity-specific macro cycle detection; QAD Dislocation is company-specific impairment diagnosis |
| **replacement_required** | N/A — QAD Dislocation Radar (M5) is a new design, not evolution |

## 11. Radar Scout (Weekly + Mid-Week)

| Field | Value |
|-------|-------|
| **capability_id** | CAP-011 |
| **source_module** | Hermes cron jobs + org-radar-scout Principal profile |
| **current_authority** | FD #71, FD #78, FD #80, FD #81, FD #82, FD #130 |
| **current_state** | **TRANSITIONAL** |
| **primary_disposition** | TRANSITIONAL_RETAIN |
| **QAD_target_capability** | External-discovery lane (Lane C) — regulatory context, competitor/supplier/customer commentary, unusual filing context, industry developments, source-specific anomalies |
| **reusable_data** | Radar Digest archive, Task Idea Card history, outcomes register |
| **reusable_logic** | Radar scanning methodology (prompts, EDGAR scan, feedback loop) |
| **active_dependencies** | 2 cron jobs (Mon 08:00 + Thu 08:00); Hermes org-radar-scout profile; kanban Inbox; CoS triage |
| **downstream_consumers** | CoS triage → Research Mandates; evidence/radar/digests/; kanban Inbox |
| **historical_value** | Discovery prior art for QAD v1 comparison |
| **replacement_required** | Yes — eventual replacement by QAD Discovery (M5/M6); but **no pre-decided retirement** — requires evidence-based migration decision |
| **verification_status** | ✅ Cron jobs active; no regression |
| **archival_preconditions** | Only after evidence-based migration decision: `Legacy Radar vs QAD Discovery incremental recall comparison` shows no material incremental value, OR Radar's function fully reproduced in QAD Discovery |
| **governing_FD/spec** | FD #71, FD #78, FD #80, FD #81, FD #82, FD #130; QAD-DISCOVERY-AND-COVERAGE-OPERATING-REQUIREMENT.md Part D |

## 12. Deep Research Standing Contract (tpl 16)

| Field | Value |
|-------|-------|
| **capability_id** | CAP-012 |
| **source_module** | `operational/hermes-organization/templates/16-DEEP-RESEARCH-STANDING-CONTRACT.md` |
| **current_authority** | FD #95, FD #130 |
| **current_state** | **ACTIVE** |
| **primary_disposition** | REUSE |
| **QAD_target_capability** | Foundation for QAD Research Protocol (mandate → evidence → cross-exam → CRO → audit → synthesis → Founder gate) |
| **reusable_data** | Template 16 contract, RM-2026-0001..0008 workflow record |
| **reusable_logic** | 11-stage workflow skeleton |
| **active_dependencies** | None (template only — instantiated per Research Mandate) |
| **downstream_consumers** | Research Mandates, IC Secretary, CRO, Auditor |
| **historical_value** | First full research workflow; QAD-M3 will extend |
| **replacement_required** | No — QAD-M3 extends into full QAD Research Protocol |
| **verification_status** | ✅ Used in 8 published research mandates |
| **archival_preconditions** | After QAD-M3 supersedes with QAD Research Protocol |
| **governing_FD/spec** | FD #95, FD #130; QAD-M3 spec #3 |

## 13. Blog / Report Infrastructure

| Field | Value |
|-------|-------|
| **capability_id** | CAP-013 |
| **source_module** | `frontend/src/pages/library/`, `backend/report_store.py`, `reports/` |
| **current_authority** | FD #62, FD #84–86, FD #96, FD #130 |
| **current_state** | **ACTIVE** |
| **primary_disposition** | REUSE |
| **QAD_target_capability** | QAD report index and publication renderer |
| **reusable_data** | All published reports (36 published, 24 Thai), library index |
| **reusable_logic** | Report rendering (react-markdown), library filtering, companion nesting |
| **active_dependencies** | Backend `/api/reports`, frontend `/library`, `/library/:slug` |
| **downstream_consumers** | Founder reading research reports, IPM (via IPM-FD-003) |
| **historical_value** | Published research library |
| **replacement_required** | No — QAD-M11 adds PDF generation alongside markdown |
| **verification_status** | ✅ Browser-verified, lint 0, build exit 0 |
| **archival_preconditions** | N/A — active surface |
| **governing_FD/spec** | FD #62, FD #84–86, FD #96, FD #130; QAD-M11 |

## 14. Thai Editorial Standard

| Field | Value |
|-------|-------|
| **capability_id** | CAP-014 |
| **source_module** | `reports/THAI-RESEARCH-EDITORIAL-STANDARD.md` |
| **current_authority** | FD #94, FD #130 |
| **current_state** | **ACTIVE** |
| **primary_disposition** | REUSE |
| **QAD_target_capability** | QAD publication quality control (10 rules, FACTS LOCKED gate) |
| **reusable_data** | Standard document |
| **reusable_logic** | Editorial workflow, Facts Locked verification |
| **active_dependencies** | IC Secretary (editor role); reports/ contract |
| **downstream_consumers** | All published reports |
| **historical_value** | Thai publication methodology |
| **replacement_required** | No — QAD-M11 extends with long-form PDF standard |
| **verification_status** | ✅ Applied to 24 Thai reports |
| **archival_preconditions** | N/A — active standard |
| **governing_FD/spec** | FD #94, FD #130; QAD-M11 |

## 15. Capital Intelligence Live Office

| Field | Value |
|-------|-------|
| **capability_id** | CAP-015 |
| **source_module** | Hermes Dashboard plugin `capital-intelligence-office` |
| **current_authority** | FD #108–110, FD #130 |
| **current_state** | **FROZEN** (production baseline; **runtime still operational** — dashboard serves at :9119, Kanban board active, WS live) |
| **runtime_use** | **OPERATIONAL** — Hermes Dashboard :9119, Kanban board live, WS live events. Founder monitors production. |
| **primary_disposition** | REUSE (as QAD monitoring dashboard) |
| **QAD_target_capability** | QAD case monitoring dashboard |
| **reusable_data** | Kanban board state, Hermes Capital Intelligence board |
| **reusable_logic** | Dashboard plugin, WS live updates, spatial floor, handoff lines |
| **active_dependencies** | Hermes Capital Intelligence board (kanban/boards/iip); WS events |
| **downstream_consumers** | Founder (dashboard at :9119) |
| **historical_value** | Production baseline frozen |
| **replacement_required** | No — QAD-M12 will define monitoring data sources |
| **verification_status** | ✅ Suite 235/235, browser-verified |
| **archival_preconditions** | After QAD-M12 monitoring is operational |
| **governing_FD/spec** | FD #108–110, FD #130; QAD-M12 |

## 16. Research Audit Infrastructure

| Field | Value |
|-------|-------|
| **capability_id** | CAP-016 |
| **source_module** | `backend/audit_store.py`, `backend/org_store.py`, `evidence/` |
| **current_authority** | FD #55–56, FD #86, FD #130 |
| **current_state** | **ACTIVE** |
| **primary_disposition** | REUSE |
| **QAD_target_capability** | QAD-M10 Audit inherits this infrastructure |
| **reusable_data** | Decision Register, Model Registry, Audit Center, org-workflow API |
| **reusable_logic** | Audit store, org store, evidence directory structure |
| **active_dependencies** | Backend `/api/decisions`, `/api/audit/*`, `/api/org-queue`; frontend `/audit` |
| **downstream_consumers** | Founder (audit center), IC Secretary, org-workflow consumers |
| **historical_value** | Governance audit trail |
| **replacement_required** | No — QAD-M10 extends, does not replace |
| **verification_status** | ✅ Locked tests pass |
| **archival_preconditions** | N/A — active infrastructure |
| **governing_FD/spec** | FD #55–56, FD #86, FD #130; QAD-M10 |

## 17. Evidence Doctrine / Evidence Model Infrastructure

| Field | Value |
|-------|-------|
| **capability_id** | CAP-017 |
| **source_module** | `operational/EVIDENCE-DOCTRINE.md`, `project-definition/EVIDENCE-MODEL.md` |
| **current_authority** | FD #130 (extended M1), Constitution §8 |
| **current_state** | **ACTIVE** |
| **primary_disposition** | REUSE |
| **QAD_target_capability** | QAD Evidence & Source Model (M3 spec #4) |
| **reusable_data** | Evidence doctrine (source authority, discovery provenance, S6, AI synthesis) |
| **reusable_logic** | Evidence separation, source authority, PIT, provenance rules |
| **active_dependencies** | All research workflows, audit, publication |
| **downstream_consumers** | Every research mandate, Audit Center, Evidence Registry |
| **historical_value** | Foundation of evidence integrity |
| **replacement_required** | No — QAD-M3 spec #4 extends and formalizes |
| **verification_status** | ✅ Constitution §8, EVIDENCE-DOCTRINE.md, QAD-M1 correction |
| **archival_preconditions** | N/A — active doctrine |
| **governing_FD/spec** | FD #130, Constitution §8; QAD-M3 spec #4 |

## 18. Hermes AI Workforce (10 org-* profiles)

| Field | Value |
|-------|-------|
| **capability_id** | CAP-018 |
| **source_module** | `operational/hermes-organization/` (role contracts, ROLE-REGISTRY, profiles) |
| **current_authority** | FD #54, FD #130 |
| **current_state** | **ACTIVE** |
| **primary_disposition** | TRANSITIONAL_RETAIN |
| **migration_instruction** | DEFER_QAD_WORKFORCE_REMAP_UNTIL_M3_ROLE_CONTRACTS_AND_WORKFORCE_MIGRATION_MAP |
| **QAD_target_capability** | Workforce mapping to be determined after Pack A (QAD logical role contracts) exist |
| **reusable_data** | Role contracts, ROLE-REGISTRY, authority matrix, kanban contracts |
| **reusable_logic** | Profile structure, delegation patterns, Holds mechanism |
| **active_dependencies** | Hermes Capital Intelligence board; kanban workflow; cron jobs; all current org-* profile operations |
| **downstream_consumers** | All current org-* profile operations (daily/weekly workflow — Radar, CoS, IC Secretary, CRO, Auditor, Data Steward, Analysts) |
| **historical_value** | First workforce integration |
| **replacement_required** | Yes — QAD logical role contracts (M3) + Workforce Migration Map |
| **verification_status** | ✅ Dry-run pilot PASS 8/8 |
| **archival_preconditions** | After QAD logical role contracts approved + WORKFORCE-MIGRATION-MAP created |
| **governing_FD/spec** | FD #54, FD #130; QAD-M3 Pack A |

## 19. Frontend / UI Platform (frozen legacy surfaces)

| Field | Value |
|-------|-------|
| **capability_id** | CAP-019 |
| **source_module** | `frontend/src/` (legacy pages: AM, FO, CS, II, WeakSignal, Dashboard — preserved as frozen) |
| **current_authority** | FD #62, FD #65, FD #86, FD #130 |
| **current_state** | **FROZEN** (read-only, no new development) |
| **primary_disposition** | FREEZE |
| **QAD_target_capability** | NONE — legacy platform surfaces are frozen as-is; screening data = report input only |
| **reusable_data** | None (frozen display only) |
| **reusable_logic** | None |
| **active_dependencies** | Backend adapters serving frozen API data; API clients (amClient, foClient, csClient, iiClient) |
| **downstream_consumers** | None (frozen surfaces not actively used for QAD) |
| **historical_value** | Platform evolution record |
| **replacement_required** | N/A — frozen archive-in-place |
| **verification_status** | ✅ Build passes, lint 0 |
| **archival_preconditions** | After QAD platform fully replaces functionality |
| **governing_FD/spec** | FD #62, FD #65, FD #86, FD #130 |

## 20. SEC EDGAR / Source Adapters

| Field | Value |
|-------|-------|
| **capability_id** | CAP-020 |
| **source_module** | `backend/adapters.py`, `institutional-intelligence-v0/fetcher.py`, `fundamental-opportunity-v0/source_adapter.py` |
| **current_authority** | FD #41, FD #42, FD #46, FD #95, FD #130 |
| **current_state** | **FROZEN** (as standalone adapters — no standalone development; **runtime still consumed by ACTIVE consumers** — see runtime_use below) |
| **primary_disposition** | ADAPT |
| **QAD_target_capability** | Source data fetching for QAD Discovery (SEC EDGAR, yfinance, 13F) |
| **reusable_data** | SEC EDGAR CIK mapping, yfinance historical data, 13F filings |
| **reusable_logic** | EDGAR filing fetch, companyfacts XBRL parsing, CUSIP mapping, yfinance adapter |
| **runtime_use** | **ACTIVE dependency of** Equity Inflection Scanner (CAP-002), Quality & Asymmetry Discovery (CAP-003); also serves FO (FROZEN), II (FROZEN), AM (FROZEN), CS (FROZEN) — see Dependency Matrix |
| **active_dependencies** | Many downstream consumers (see individual pipelines) |
| **downstream_consumers** | FO, II, AM, Equity Inflection, Quality & Asymmetry, CS pipelines |
| **historical_value** | Source data infrastructure |
| **replacement_required** | No — QAD-M6 Source Intelligence will evolve, not replace |
| **verification_status** | ✅ Locked tests pass |
| **archival_preconditions** | After QAD-M6 Source Intelligence operational |
| **governing_FD/spec** | FD #41, FD #42, FD #46, FD #95, FD #130; QAD-M6 |

## Summary: Current Lifecycle State

| Lifecycle State | Count | Capabilities |
|----------------|-------|-------------|
| **ACTIVE** | 9 | Shared Equity Universe (CAP-001), Equity Inflection Scanner (CAP-002), Quality & Asymmetry Discovery (CAP-003), Deep Research Contract (CAP-012), Blog/Report Infrastructure (CAP-013), Thai Editorial Standard (CAP-014), Research Audit Infrastructure (CAP-016), Evidence Doctrine/Model Infrastructure (CAP-017), Hermes AI Workforce (CAP-018) |
| **FROZEN** | 14 | AM Pipeline (CAP-004), AM Theme Infrastructure (CAP-005), Theme Anomaly/Weak Signal (CAP-006), FO Pipeline (CAP-007 — as strategy), Moat Classification (CAP-007A), Earnings Quality (CAP-007B), Marx Signals (CAP-007D), II Pipeline (CAP-008), CIW (CAP-009 — monitoring ACTIVE), CS Product Radar (CAP-010), CS Product Discovery (CAP-010A), Capital Intelligence Live Office (CAP-015 — runtime operational), Frontend Legacy Surfaces (CAP-019), SEC EDGAR/Source Adapters (CAP-020 — runtime consumed by ACTIVE consumers) |
| **SUPERSEDED** | 1 | Value Trap Detector — 5-question (CAP-007C), replaced by QAD Impairment Diagnosis |
| **TRANSITIONAL** | 1 | Radar Scout (CAP-011 — Weekly + Mid-Week) |
| **VERIFIED_UNUSED** | 0 | (no state change without evidence) |
| **ARCHIVED** | 0 | (physical archival deferred) |
| **Total** | **25** | Canonical capability records (child IDs included in their parent's state cohort) |

> **Note:** CAP-018 (Hermes AI Workforce) is included in the ACTIVE count because its 10 org-* profiles are still running daily operations. QAD workforce remapping is deferred — see primary_disposition = TRANSITIONAL_RETAIN with migration_instruction.

## Summary: QAD Primary Disposition

| Disposition | Count | Capabilities |
|-------------|-------|-------------|
| **REUSE** | 7 | CAP-001, CAP-012, CAP-013, CAP-014, CAP-015, CAP-016, CAP-017 |
| **ADAPT** | 6 | CAP-002, CAP-003, CAP-006, CAP-007A, CAP-007B, CAP-020 |
| **ABSORB** | 1 | CAP-009 |
| **TRANSITIONAL_RETAIN** | 2 | CAP-011, CAP-018 |
| **FREEZE** | 7 | CAP-004, CAP-005, CAP-007, CAP-007D, CAP-008, CAP-010, CAP-019 |
| **SUPERSEDE** | 1 | CAP-007C |
| **DO_NOT_REUSE** | 1 | CAP-010A |
| **Total** | **25** | Canonical capability records |

> **Derivation:** All counts derive mechanically from `QAD-M2-LEGACY-CAPABILITY-REGISTRY.md` canonical records. Manual drift is eliminated. If registry records change, regenerate this summary.

<!-- 2026-08-18 00:36 UTC+7 -->