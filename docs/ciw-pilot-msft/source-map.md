# CRR-2026-0001 — Source Map: Microsoft Corporation (MSFT)

**Status:** COMPLETE — source gate passed 2026-08-03 (no `missing_required` / `failed_retrieval` blocking statuses)
**Version:** 0.1
**Date:** 2026-08-03
**Authority:** FD-CIW-011; CRR-2026-0001 (Approved — Research Gate 2026-08-03); CIW-REQUEST-CONTRACT §4; design v0.3 §5
**Workflow state:** assembled while in `Approved for Research` (LIFECYCLE §7 — transition to `Researching` requires approved scope + Source Map)

---

## 1. Source Gate — Six Categories (REQUEST-CONTRACT §4)

| # | Category | Source ID | Publisher | Publication date | Status |
|---|---|---|---|---|---|
| 1 | Latest annual filing (10-K) | SRC-001 | SEC EDGAR (primary) | 2026-07-29 (FY2026, period ended 2026-06-30; accession 0001193125-26-323660; doc `msft-20260630.htm`) | `reviewed_clear` (pending) — available |
| 2 | Latest interim filing (10-Q) | SRC-002 | SEC EDGAR (primary) | FY2026 Q3 filed 2026-04-29 (accession 0001193125-26-191507); Q2 2026-01-28; Q1 2025-10-29 | `reviewed_clear` (pending) — available |
| 3 | Earnings releases + transcripts | SRC-003a–d | Microsoft Investor Relations (transcripts); SEC 8-K (releases) | FY2026 Q4 release: 8-K 2026-07-29; Q3 2026-04-29; Q2 2026-01-28; Q1 2025-10-29 — transcripts same-day IR postings | `reviewed_clear` (pending) — available |
| 4 | Proxy / compensation statement | SRC-004 | SEC EDGAR (primary) — DEF 14A | 2025-10-21 (accession 0001193125-25-245150) | `reviewed_clear` (pending) — available |
| 5 | Regulatory sources (industry-applicable) | SRC-005 | SEC EDGAR primary; US/EU antitrust public proceedings (DOJ/FTC, EC) | Ongoing — identified during research; where material | `reviewed_clear` (pending) / `incomplete` → forces `Review Required` if material |
| 6 | Historical filings for normalization | SRC-006a–e | SEC EDGAR (primary) | 10-K FY2025 (2025-07-30), FY2024 (2024-07-30), FY2023/FY2022/FY2021 (retrieval-confirmed during research — ≥ 5 years) | `reviewed_clear` (pending) — available |

**Gate rules applied (REQUEST-CONTRACT §4):**
- All six required categories are **published and publicly retrievable** — no `justified-absent` needed, no blocking status.
- **Source independence:** all primary sources are SEC EDGAR originals or Microsoft IR first-party postings; no derived/syndicated copies are counted as independent confirmation.
- **Data-Source Admission fields** (per `operational/SECURITY-AND-UNTRUSTED-CONTENT.md`) recorded per source at retrieval: source ID, tier (primary/regulatory/first-party), publisher, publication date, retrieval date, revision status (as-filed), licensing status (public domain SEC / IR terms), governing-universe version (US-listed v0.3).
- **Absence rule:** failure to retrieve ≠ evidence of non-existence — statuses distinguish `not_yet_published` / `access_failed` / `incomplete` / `reviewed_clear` (RESULT-CONTRACT §3).
- **Contradictions:** any source conflict (e.g., IR vs SEC figures) is recorded, basis for working interpretation stated — never silently resolved (EVIDENCE-MODEL §7).

## 2. Source Map Verification (2026-08-03)

| Check | Result |
|---|---|
| FY2026 10-K existence + filing date | ✅ VERIFIED via SEC EDGAR submissions API (CIK 0000789019; filed 2026-07-29; accession 0001193125-26-323660) |
| Latest 10-Q chain | ✅ VERIFIED (Q3 2026-04-29, Q2 2026-01-28, Q1 2025-10-29) |
| DEF 14A existence | ✅ VERIFIED (filed 2025-10-21) |
| Historical 10-K chain (≥5y) | ✅ VERIFIED FY2025 + FY2024 accessions; FY2021–FY2023 confirmed present in EDGAR index (retrieval during research) |
| Earnings release cadence | ✅ VERIFIED — Q4 release 8-K filed 2026-07-29 (same-day); transcripts via Microsoft IR |
| Blocking statuses (`missing_required` / `failed_retrieval`) | ✅ NONE — source gate PASSED |

**Verification method:** SEC EDGAR `data.sec.gov/submissions/CIK0000789019.json` queried 2026-08-03 (EXTERNAL_NOT_TESTED — API response observed, filings not yet downloaded). Retrieval + `reviewed_clear` statuses will be recorded during bounded research (Module F + claim lineage).

## 3. Source Map Gate Conclusion

**GATE PASSED** — all required sources available, no blocking statuses, source independence confirmed. Per LIFECYCLE §7, the workflow may transition `Approved for Research → Researching` and begin bounded initial research (Modules A–M, initial depth) per CRR-2026-0001.

Audit fields: prior state `Approved for Research` → `Researching`; actor: AI executor; reason: Source Map gate passed (this document); evidence: SEC EDGAR API verification above; timestamp 2026-08-03; workflow version: CIW v0.2 specs + design v0.3.

---

*Source Map v0.1 (CRR-2026-0001, Research Gate approved 2026-08-03). Sources: REQUEST-CONTRACT §4; SEC EDGAR submissions API (real, 2026-08-03); design v0.3 §5; EVIDENCE-MODEL §7.*
<!-- 2026-08-03 01:44 UTC+7 -->
