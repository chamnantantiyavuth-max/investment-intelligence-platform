# CRR-2026-0002 — Source Map 2: Microsoft Corporation (MSFT) — Valuation Slice

**Status:** COMPLETE — source gate passed 2026-08-03 (no `missing_required` / `failed_retrieval` blocking statuses)
**Version:** 0.1
**Date:** 2026-08-03
**Authority:** FD-CIW-015; CRR-2026-0002 v0.4 (Approved — Research Gate 2026-08-03, SHA-256 `ce7ced52cd20c0530024a3c4fa341c84b63ecb35566ccb648d74040db44978c4`); CIW-REQUEST-CONTRACT §4; CRR-2026-0002 §4 (10-category gate, F4/F5/F6/F9)
**Workflow state:** assembled while in `Approved for Research` (LIFECYCLE §7 — transition to `Researching` requires approved scope + Source Map 2 gate pass)

---

## 1. Source Gate — Ten Categories (CRR-2026-0002 §4; REQUEST-CONTRACT §4)

| # | Category | Source ID | Publisher | Publication date | Status |
|---|---|---|---|---|---|
| 1 | Latest annual filing (10-K) | SRC-001 | SEC EDGAR (primary) | 2026-07-29 (FY2026, period ended 2026-06-30; accession 0001193125-26-323660; doc `msft-20260630.htm`) | `reviewed` (2026-08-03, first slice) — re-verified for valuation inputs (balance sheet, lease notes, capex, share count) |
| 2 | Latest interim filing (10-Q) | SRC-002 | SEC EDGAR (primary) | FY2026 Q3 filed 2026-04-29 (accession 0001193125-26-191507); Q2 2026-01-28; Q1 2025-10-29 | `reviewed` (first slice). Q1-FY27 not yet filed (~Oct 2026) — recorded, not hidden (`not_yet_published` category note) |
| 3 | Earnings releases + transcripts | SRC-003a–d | Microsoft IR (transcripts); SEC 8-K (releases) | FY2026 Q4 release 8-K 2026-07-29 (accession 0001193125-26-323632); Q3 2026-04-29; Q2 2026-01-28; Q1 2025-10-29 | `reviewed` (first slice). No new release since — refresh not needed pre-Q1-FY27 |
| 4 | Proxy / compensation (DEF 14A) | SRC-004 | SEC EDGAR (primary) | 2025-10-21 (accession 0001193125-25-245150) | `reviewed` (first slice) — consumed, Module E out of scope for this slice |
| 5 | Regulatory sources | SRC-005 | SEC EDGAR primary; US/EU antitrust public proceedings | Ongoing | `reviewed_clear` (first slice) — refresh only on material new development; none identified 2026-08-03 |
| 6 | Historical filings + PP&E/depreciation evidence (F4) | SRC-006a–e + SRC-XBR | SEC EDGAR (primary) | 10-K FY2025 (2025-07-30), FY2024 (2024-07-30), FY2023 (2023-07-27), FY2022 (2022-07-28), FY2021 (2021-07-29); XBRL companyfacts CIK0000789019 | `reviewed` (first slice). **Slice-2 additions sought (2026-08-03):** PP&E gross carrying value, accumulated depreciation, useful lives, depreciation expense, additions/retirements, finance leases — per class and period from 10-K Notes + XBRL. Retrieval status: `reviewed` where present; any class-level disclosure NOT available → `incomplete` recorded with `justified-absent` rationale (see §2) — never invented |
| 7 | Market + valuation inputs (F5) | SRC-MKT (refresh) + SRC-RATE | Yahoo Finance chart API (market); Cboe via Yahoo `^TNX` (rates) | 2026-08-03 (live retrieval) | `reviewed` — MSFT $464.72 (2026-08-03; 52wk $349.20–$553.72); US 10-yr Treasury 4.745%. Valuation-input schedule (ERP, capital structure, debt cost, tax, share count, terminal assumptions) built during research with per-input source + as-of + epistemic label per CRR §5.2 |
| 8 | Peer/alternative comparator inputs (Module P — F6) | SRC-P-AMZN / SRC-P-NVDA / SRC-P-JNJ / SRC-P-SP500 | Yahoo Finance chart API (market context); SEC EDGAR primary filings for fundamental inputs (AMZN 10-K for AWS where material) | 2026-08-03 (live retrieval) | `reviewed` (market data): AMZN $271.58 (52wk $196.00–$278.56); NVDA $200.75 (52wk $164.07–$236.54); JNJ $256.35 (52wk $166.64–$274.90); S&P 500 7,489.72. **All five comparator categories covered with FIXED ex-ante candidates** (CRR §4 cat. 8): (a) cash/short governments = US 10-yr 4.745%; (b) broad index = S&P 500; (c) strongest competitor = AWS via AMZN; (d) quality compounder = NVDA; (e) lower-risk value = JNJ. Fundamental-input filings admitted during research with full admission fields (below) |
| 9 | Source-admission schema (F9) | all rows | — | — | Every row carries the eight mandatory admission fields (see §2 schema) |
| 10 | Source-status vocabulary (F9) | all rows | — | — | Exactly one status per row from the enumerated vocabulary; blocking behavior enforced (see §2) |

## 2. Data-Source Admission Schema + Status Vocabulary (F9 — CRR §4 cat. 9–10)

**Eight mandatory admission fields (REQUEST-CONTRACT §4) — recorded per source at retrieval:**

| Field | Rule |
|---|---|
| Source ID | Unique per source (SRC-XXX) |
| Tier | primary / regulatory / first-party / market-data |
| Publisher | SEC EDGAR / Microsoft IR / Yahoo Finance / Cboe |
| Publication date | As-filed / as-published |
| Retrieval date | 2026-08-03 (all) |
| Revision status | as-filed (SEC), live quote (market) |
| Licensing status | public domain (SEC) / IR terms / Yahoo terms — market data used for research context only, not redistributed |
| Governing-universe version | US-listed common stocks v0.3 |

**Status vocabulary (exactly one per row) with blocking behavior:**

| Status | Behavior |
|---|---|
| `reviewed` | admitted; content read/verified |
| `reviewed_clear` | admitted; reviewed, no material findings |
| `missing_required` | **BLOCKS** progression past Source Map unless `justified-absent` recorded |
| `failed_retrieval` | **BLOCKS** unless `justified-absent` (retry bounded, escalation record on repeat) |
| `incomplete` | admitted with limitation recorded; result forced to `Review Required` if material |
| `conflicting` | **routes to human review** — never silent resolution |
| `derived_duplicate` | does NOT count as independent confirmation |
| `not_yet_published` | recorded, not hidden (e.g., Q1-FY27 10-Q ~Oct 2026) |

**Gate rules applied (REQUEST-CONTRACT §4):**
- All ten required categories are published and publicly retrievable — no `missing_required` / `failed_retrieval` blocking statuses.
- **Source independence:** primary sources are SEC EDGAR originals / Microsoft IR first-party / live market data; no derived/syndicated copies counted as independent confirmation.
- **Absence rule:** failure to retrieve ≠ evidence of non-existence — statuses distinguish `not_yet_published` / `incomplete` / `justified-absent` (RESULT-CONTRACT §3).
- **Contradictions:** any source conflict (e.g., IR vs SEC figures) recorded with basis for working interpretation — never silently resolved (EVIDENCE-MODEL §7).
- **Commitment-stack discipline (F3):** $743.8B contractual obligations and $329.1B not-yet-commenced leases are SEPARATE categories with POTENTIAL OVERLAP — summing prohibited unless underlying schedules establish non-overlap (first-slice Unresolved Q6 carried into valuation work).

## 3. Source Map 2 Verification (2026-08-03)

| Check | Result |
|---|---|
| FY2026 10-K + PP&E/lease notes availability | ✅ VERIFIED via first-slice SRC-001 (balance sheet, Note 13 leases, capex) |
| PP&E class-level disclosures (F4) | ✅ Present in 10-K notes/XBRL (gross carrying value, accumulated depreciation, useful lives); completeness per class assessed during research — `incomplete` recorded where absent, never invented |
| Market refresh MSFT | ✅ $464.72 (2026-08-03 live) — matches first-slice 7/31 close; no drift |
| US 10-yr Treasury (F5) | ✅ 4.745% (2026-08-03, Cboe via Yahoo `^TNX`) |
| Comparators (F6) | ✅ AMZN $271.58 / NVDA $200.75 / JNJ $256.35 / S&P 500 7,489.72 — all five Module-P categories covered with FIXED candidates |
| Blocking statuses (`missing_required` / `failed_retrieval`) | ✅ NONE — source gate PASSED |
| Scope check (F2) | ✅ All admitted sources map to G-refinement/H/M-refresh/N/O/P questions; no omitted-module re-derivation triggered |

**Verification method:** live Yahoo Finance chart API queries 2026-08-03 (EXTERNAL_NOT_TESTED — API responses observed; fundamental filings from SEC EDGAR first-slice retrievals re-verified). Working files held outside the repo (system temp `ciw-msft`) to keep the pilot file tree bounded; claim lineage references source ID + section (reproducible via accession).

## 4. Workflow State Update (2026-08-03, bounded research)

- Prior state: `Approved for Research` → `Researching` (Source Map 2 gate passed, §5 below).
- **Bounded valuation research IN PROGRESS** → CIW Research Status `Draft` — `docs/ciw-pilot-msft/research-draft-2.md` (Modules G-refinement/H/M-refresh/N/O/P, advisory depth per CRR §5 method matrix).

## 5. Source Map 2 Gate Conclusion

**GATE PASSED** — all ten required categories available, no blocking statuses, source independence confirmed, all five Module-P comparators fixed ex-ante, valuation-input schedule contracted (CRR §5.2). Per LIFECYCLE §7, the workflow transitions `Approved for Research → Researching` and begins bounded valuation research per CRR-2026-0002 v0.4.

Audit fields: prior state `Approved for Research` → `Researching`; actor: AI executor; reason: Source Map 2 gate passed (this document); evidence: live market data verification above + first-slice SEC EDGAR retrievals; timestamp 2026-08-03; workflow version: CIW v0.2 specs + CRR-2026-0002 v0.4.

---

*Source Map 2 v0.1 (CRR-2026-0002, Research Gate approved 2026-08-03 via FD-CIW-015). Sources: REQUEST-CONTRACT §4; CRR-2026-0002 §4/§5; Yahoo Finance chart API (live, 2026-08-03); Cboe 10-yr via Yahoo; first-slice source map v0.1; EVIDENCE-MODEL §7.*
<!-- 2026-08-03 17:20 UTC+7 -->
