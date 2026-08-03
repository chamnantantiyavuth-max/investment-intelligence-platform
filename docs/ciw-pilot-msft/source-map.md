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
| 1 | Latest annual filing (10-K) | SRC-001 | SEC EDGAR (primary) | 2026-07-29 (FY2026, period ended 2026-06-30; accession 0001193125-26-323660; doc `msft-20260630.htm`) | `reviewed` — 2026-08-03; full text converted, Item 1/1A/7/8 read (2026-08-03) |
| 2 | Latest interim filing (10-Q) | SRC-002 | SEC EDGAR (primary) | FY2026 Q3 filed 2026-04-29 (accession 0001193125-26-191507); Q2 2026-01-28; Q1 2025-10-29 | `reviewed` — FY26 Q3 retrieved + income statement/segment tables read; Q2/Q1 accessions verified |
| 3 | Earnings releases + transcripts | SRC-003a–d | Microsoft Investor Relations (transcripts); SEC 8-K (releases) | FY2026 Q4 release: 8-K 2026-07-29 (accession 0001193125-26-323632; exhibit `msft-ex99_1.htm`); Q3 2026-04-29; Q2 2026-01-28; Q1 2025-10-29 — transcripts retrieved via Microsoft IR (Q4 `TranscriptQandAFY26q4.docx`, Q3 `TranscriptQandAFY26Q3`, Q2 `TranscriptQandAFY26q2`, Q1 `TranscriptFY26Q1.docx`) | `reviewed` — all four press releases + four transcripts retrieved and read (2026-08-03) |
| 4 | Proxy / compensation statement | SRC-004 | SEC EDGAR (primary) — DEF 14A | 2025-10-21 (accession 0001193125-25-245150; doc `d908201ddef14a.htm`) | `reviewed` — CD&A, Summary Compensation Table, board/governance read |
| 5 | Regulatory sources (industry-applicable) | SRC-005 | SEC EDGAR primary; US/EU antitrust public proceedings (DOJ/FTC, EC) | Ongoing — identified during research; where material | `reviewed_clear` — filing-based items reviewed (Item 1A, Note 14 contingencies); ongoing proceedings (IDPC LinkedIn appeal, antitrust) recorded as unresolved risk in draft §8 |
| 6 | Historical filings for normalization | SRC-006a–e | SEC EDGAR (primary) | 10-K FY2025 (2025-07-30), FY2024 (2024-07-30), FY2023 (2023-07-27), FY2022 (2022-07-28), FY2021 (2021-07-29) | `reviewed` — FY25 business/text converted + read; FY21–FY24 financial data via SEC XBRL companyfacts cross-check (SRC-XBR) |

**Structured data source (added during research):** SRC-XBR — SEC EDGAR XBRL company facts (`data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json`, retrieved 2026-08-03) — primary structured financial backbone for Modules F/G/H. **Market data (added):** SRC-MKT — Yahoo Finance chart API, MSFT $464.72 (2026-07-31 close), 52wk $349.20–$553.72.

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

**Verification method:** SEC EDGAR `data.sec.gov/submissions/CIK0000789019.json` queried 2026-08-03 (EXTERNAL_NOT_TESTED — API response observed, filings not yet downloaded). **Retrieval completed during bounded research (2026-08-03):** all sources downloaded from SEC EDGAR originals / Microsoft IR first-party postings; statuses updated to `reviewed` / `reviewed_clear` per RESULT-CONTRACT §3. Working files held outside the repo (system temp `ciw-msft`) to keep the pilot file tree bounded; claim lineage references source ID + section (reproducible via accession).

## 2B. Workflow State Update (2026-08-03, bounded research)

- Prior state: `Approved for Research` → `Researching` (Source Map gate passed, §3 below).
- **Bounded initial research COMPLETE (2026-08-03)** → CIW Research Status now `Draft` — `docs/ciw-pilot-msft/research-draft.md` v0.1 (Modules A–M, initial depth; 16 quality gates self-checked; claim lineage + calculation lineage recorded).
- Next: **Independent Challenge (Sol Medium, separate context — mandatory, QUALITY-GATES §1)** → Founder Review → structured `research-result.md`.

## 3. Source Map Gate Conclusion

**GATE PASSED** — all required sources available, no blocking statuses, source independence confirmed. Per LIFECYCLE §7, the workflow may transition `Approved for Research → Researching` and begin bounded initial research (Modules A–M, initial depth) per CRR-2026-0001.

Audit fields: prior state `Approved for Research` → `Researching`; actor: AI executor; reason: Source Map gate passed (this document); evidence: SEC EDGAR API verification above; timestamp 2026-08-03; workflow version: CIW v0.2 specs + design v0.3.

---

*Source Map v0.1 (CRR-2026-0001, Research Gate approved 2026-08-03). Sources: REQUEST-CONTRACT §4; SEC EDGAR submissions API (real, 2026-08-03); design v0.3 §5; EVIDENCE-MODEL §7.*
<!-- 2026-08-03 01:44 UTC+7 -->
