# Phase 3 — Independent API / DB / Oracle Verification

## Lane summary

- API contract: **8/8 declared GET operations live and exercised**.
- Positive entity detail probes: **PASS** using IDs read from list endpoints.
- Negative AM detail probe: **PASS** (`made-up-id` returned the required 404).
- Database: **N/A by manifest** (stateless backend; no DB/auth).
- AM oracle: the AM API is an authorized `synthetic_demo` mock and is **not required** to match `alpha-momentum-v0/output/pipeline_result.json` IDs.
- FO oracle: **PASS** for fixture/API company set, names, detail structure, and independently derived Cheap & Quality membership.
- Provenance: **WARN/FAIL on two API families**; see SOL-001 and SOL-002.
- Dashboard-to-CS count agreement: **FAIL**; see SOL-003.

## Endpoint results

| Endpoint / probe | HTTP | Verification | Status |
|---|---:|---|---|
| `/api/health` | 200 | Exact body `{"status":"ok"}` | PASS |
| `/api/dashboard/summary` | 200 | Required KPI shape present; `queue_size=5` agrees with AM queue | PASS with defects SOL-001/SOL-003 |
| `/api/am-queue` | 200 | 5 themes; IDs exactly `theme-ai-infra`, `theme-glp1`, `theme-semicon`, `theme-defense`, `theme-grid`; every item `data_source=synthetic_demo` | PASS |
| `/api/am-theme/theme-ai-infra` | 200 | ID came from list endpoint; detail has `data_source=synthetic_demo` | PASS |
| `/api/am-theme/made-up-id` | 404 | Exact not-found behavior; this is correct, not a defect | PASS |
| `/api/cs-radar` | 200 | Top-level `data_source=synthetic_demo`; `assets` is a list of 2 | PASS |
| `/api/fo-queue` | 200 | 8 companies; exact fixture ID/name agreement | PASS with SOL-002 |
| `/api/fo-cheap-quality` | 200 | API returns `CRM`; independent rule derivation also returns only `CRM` | PASS with SOL-002 |
| `/api/fo-package/AAPL` | 200 | Real ID from queue; required conceptual sections present | PASS with SOL-002 |
| `/api/fo-package/made-up-id` | 404 | Additional negative boundary probe | PASS |

## Dashboard verification

Observed keys include `total_themes`, `approved_themes`, `active_signals`, `queue_size`, AM KPI fields, `am_last_run`, `cs_radar_items`, `cs_qc_met`, and `cs_regime`.

- The response has no `data_source`, `provenance`, or equivalent explicit marker despite the adapter declaring the dashboard API to be `synthetic_demo` mock data: **SOL-001**.
- `queue_size=5` agrees with the five AM mock themes.
- `cs_radar_items=8` conflicts with the two assets returned by the only live CS radar source, `/api/cs-radar`: **SOL-003**.
- `total_themes=143`, `approved_themes=12`, and `active_signals=7` are static schema defaults and have no independently discoverable fixture backing. The AM pipeline oracle contains 5 approved pipeline themes, but it is a separate real-pipeline-on-fixture source and is explicitly not wired to the mock dashboard; therefore non-equality to that pipeline is **not** itself filed as a defect.
- Static source inspection confirms `DashboardSummary()` returns schema defaults. This is not an empty-source fallback branch, but it must be explicitly labeled as demo data.

## AM oracle

`alpha-momentum-v0/output/pipeline_result.json` reports 5 queue themes with pipeline IDs such as `TH-014`, `TH-020`, `TH-030`, `TH-004`, and `TH-010`. The live AM API intentionally uses five demo IDs. Per FD #44 and the adapter, non-equivalence is authorized; the truth requirement is honest `synthetic_demo` labeling, which passed for AM queue/detail.

## FO oracle

Fixture/API IDs match exactly, including order:

`AAPL, INTC, COST, CRM, XYZ, MSFT, JNJ, GE`

- Names also match `fundamental-opportunity-v0/fixtures.py` exactly.
- AAPL detail contains `company_assessment.moat`, `earnings_quality`, dictionary `conviction`, `value_trap_verdict`, `valuation_context`, and `spec_ref`.
- The fixture and pipeline source explicitly identify the data as synthetic, but the response schemas strip/omit item-level `data_source`: **SOL-002**.
- Independent Cheap & Quality derivation from the documented 70%-of-5Y-P/E trigger and five-question rules produced scores `INTC=0`, `CRM=4`, `XYZ=1`, `GE=2`; only CRM qualifies (`score >= 4`). The live endpoint also returned only CRM.

## Hardcoded fallback / source masking review

- AM: `_MOCK_THEMES` is the declared source, not a fallback; all theme items are labeled. **PASS**.
- CS: `_MOCK_ASSETS` is the declared source, not a fallback; response is labeled. **PASS**.
- Dashboard: schema defaults are the declared static source, with no conditional empty-source fallback. Missing explicit response provenance is captured as SOL-001.
- FO: each request executes `run_pipeline()` over `FIXTURES`; no empty-source-to-hardcoded-list fallback was found. Missing item-level provenance is captured as SOL-002.

## Verification tags

`TEST_VERIFIED`, `ORACLE_VERIFIED`, `STATIC_OBSERVATION`; Browser and refresh claims are not made by this lane.

<!-- 2026-08-03 18:25 UTC+7 -->