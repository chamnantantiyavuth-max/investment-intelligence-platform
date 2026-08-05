# Visual QA — Close System Product Detail (UI-3, FD #57)

**Task:** CS surface switch to the v0.1 pipeline artifact + `/cs-radar/:productId` detail page (D2 approved 5 Aug 2026).
**Approved objective:** FIT-GAP-v0.1.md §4.4 (CS Product Detail tabs) + FD #57 (pipeline-field admission).
**Design system:** MASTER.md v3.0 (Research Desk direction) — paper canvas, serif headlines, hairline ledgers, borderless 0–2, provenance chips, honest empty states.

## Backend (F3 flow, suite 310/310)

- `adapters.py`: `cs_radar()` / `cs_product()` read `close_system/output/pipeline_result.json` (SYNTHETIC); eligible radar products TLT/SLV/GDX/XLE in list order; ineligible COPPER excluded; `dashboard_components()` CS = pipeline-linked provenance (run_id CS-V0-20260725-183906, point_in_time, source `close_system_pipeline`) + `_cs_counts` (SOL-003 agreement).
- **ADAPTER_VERSION v4→v5** + `adapter_registry.json` v5 sha256 (recomputed after cs_product fix) + `persistence.ADAPTER_VERSION` synced.
- `cs_routes.py`: `/cs-radar` (pipeline) + `/cs-radar/{product_id}` (detail, 404) — mock `_MOCK_ASSETS` retired (q_conditions/dimensions/rule_pack had no spec/pipeline basis — Q-conditions belong to AM per `alpha-momentum-v0/q_conditions.py`).
- `main.py` dashboard: CS counts from adapter; `cs_qc_met` = display derivation (products with full 5-layer alignment, layers_aligned == 5).
- Locked tests updated (RED→GREEN): `test_cs_radar_pipeline_synthetic_demo` (4 products, admitted fields, mock-field absence), `test_cs_product_detail_and_404`, dashboard CS agreement (run_id/point_in_time/source + counts == 4/1). **310/310 passed.**

## Frontend (build exit 0, lint 0 errors, console 0 errors)

- `csClient.ts`: pipeline CSAsset type + `getCSProduct(id)` (status attached to errors).
- `CSRadarPage`: lead judgment = display ordering from admitted fields (conviction ordinal → layers_aligned; AM rankCandidates doctrine); table = Ticker (link) / Name / P1–P3 / Layers / Conviction / Recommendation; F3 "Unavailable on this surface" panel REMOVED (fields now real); synthetic banner updated.
- `CSProductDetailPage` (`/cs-radar/:id`): 5 tabs — Product Thesis (P1–P3 + rationale + discount/demand/status), Commodity Fundamentals (discount_detail + demand_detail + L3_cost/L4_supply_demand layers), Macro Context (L1_macro/L2_policy), Close System Assessment (layers_aligned/contradicting/conviction/recommendation + key_risks + honest Q-conditions note), Challenge & Evidence (honest empty + **Options Overlay deferred note**). 404 vs API-error branches. Synthetic provenance stamp in header.
- `DashboardPage` Finding 03 text: "full 5-layer alignment" (Q-conditions wording retired).
- `App.tsx`: route `cs-radar/:id`.

## Browser verification

- /cs-radar: 4 products, SLV lead (High conviction · 5/5), ticker links, banner. Screenshot 05.
- /cs-radar/SLV: header stamps (synthetic · pipeline v0.1), Product Thesis (P1–P3 PASS + rationale), Commodity Fundamentals (silver price / GSR / solar demand / supply), Close System Assessment (5/5 aligned, High, 3 key risks, Q-conditions note). Screenshot 06.
- Console 0 errors / 0 warnings on both pages.
- Mobile 390: code-level responsive audit only (browser tool lock) — EXTERNAL_NOT_TESTED.

## Border / containment audit

- 0 full-perimeter content outlines on both pages (open regions + hairline separators; synthetic banner + chips are approved functional exceptions). No new Card primitives; no progress bars; no composite scores.

## Evidence tags

`BROWSER_VERIFIED` · `SCREENSHOT_VERIFIED` (05, 06) · `FUNCTION_TEST_VERIFIED` (all 5 tabs + 404) · backend suite 310/310 `TEST_VERIFIED` · mobile `EXTERNAL_NOT_TESTED`.

## Remaining deviations

- Options Overlay tab data deferred (no options pipeline — honest note, per FD #57).
- L3_cost/L4 layers show for products that carry them; products without a layer show the section-level honest empty.

## Council round → PASS WITH FIXES (2026-08-05) — 2 findings, both remediated + re-verified

| # | Finding | Fix | Verified |
|---|---|---|---|
| 1 | target_discount_entry null rendered as empty row on Product Thesis | `CSProductDetailPage.tsx` Row fallback `"Not specified in pipeline artifact"` | Browser + screenshot 06 re-captured; console clean |
| 2 | SLV conviction "High" contradicted its rationale ("rare Maximum conviction candidate") | `close_system/fixtures.py` SLV conviction → **Maximum** (spec §5.1: 5/5 aligned + hidden corroboration + discount confirmed = Maximum); artifact regenerated via `python close_system/run.py` (run CS-V0-20260805-173203, point_in_time 2026-08-05T17:32:03; output/ is gitignored generated output — diff = run_id/point_in_time + conviction only); locked test pins updated + conviction==Maximum assertion | Suite 310/310, browser header "Maximum conviction" |

## Verdict

**PASS (implementer claim after council fixes)** — pipeline fields admitted with F3 discipline, mock-only values absent, honest empties + spec-true conviction reconciliation, detail page renders real admitted data, console clean. Independent visual review round 2 (focused retest) pending.

<!-- 2026-08-05 17:50 UTC+7 -->
