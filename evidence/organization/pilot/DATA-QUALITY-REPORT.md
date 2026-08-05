# Data Quality Report — Data Steward (Pilot Simulation)

> PILOT SIMULATION — per role contract `roles/09-data-steward/PRINCIPAL.md` + template 06. Assesses the published CIW result's source map (CRR-2026-0001, MSFT, proposed v1). Org-workflow artifact; changes NO canonical state.

- **Report ID:** ORG-2026-0002-DQR
- **Dataset / source:** `docs/ciw-pilot-msft/research-result.md` §8 source map (10 source rows) + `docs/ciw-pilot-msft/source-map.md`
- **Intended use:** org-workflow bounded consumption (pilot review brief)
- **Data Steward:** Data Steward (simulated)
- **Status:** **DATA READY WITH LIMITATIONS** (then DATA HOLD issued on the underlying map for licensing documentation — see HOLD-DATA-001; cleared after this report documents the field)

## Provenance

All 10 source rows carry source identity + publication/effective/ingestion timestamps + revision/vintage per the result's §8 table and source-map.md. [STATIC_OBSERVATION]

## Timestamp Semantics

- Public availability: recorded per source (filings as filed; transcript on event date).
- Effective / as-of: financials FY2026-06-30; market data 2026-07-31 close; research as-of 2026-08-03.
- Ingestion: 2026-08-03 (per result header).
- Revision / vintage: FY21–FY25 10-Ks (SRC-006a–e) retained for normalization; supersession append-first per CIW-LIFECYCLE §5.

## Freshness

Market quote (SRC-MKT) 2026-07-31 vs research as-of 2026-08-03 = 1 trading-day lag — within the AM ≤7d staleness bound; flagged as limitation for any price-sensitive use. All filings current at retrieval. ✅

## Completeness and Missingness

Source-coverage report: **no `missing_required` / `failed_retrieval` / `conflicting` / `incomplete` blocking statuses** (10/10 rows `reviewed` or `reviewed_clear`). Honest empty states preserved (Modules N/Q omitted by approved request — recorded, not hidden). ✅

## Reliability

Primary SEC filings (10-K/10-Q/8-K/XBRL) + earnings transcripts; market quote from approved market data path. Independent Challenge verified material metrics against XBRL raw facts (rounds 1–2, per artifact §7/§9). ✅

## Conflicts Across Sources

None recorded in the artifact; CRR advisory baseline (PE 37, base $415) kept visible as superseded-stale alongside current Module M data — contradiction preserved, not averaged. ✅

## Point-in-Time Integrity

Point-in-time semantics documented (as-of 2026-08-03; financials FY26-06-30); historical filings used for normalization with vintage labels. [EVIDENCE-MODEL §5.1] ✅

## Source-Coverage Status (per source)

SRC-001 `reviewed` · SRC-002 `reviewed` · SRC-003a `reviewed` · SRC-003t `reviewed` · SRC-003b–d `reviewed` · SRC-004 `reviewed` · SRC-005 `reviewed_clear` (filing-based; ongoing proceedings recorded) · SRC-006a–e `reviewed` · SRC-XBR `reviewed` · SRC-MKT `reviewed`

## Schema, Units, Identifiers, and Transformations

Consistent USD, share counts, fiscal-year conventions; calculations rerunnable per artifact §9/draft §6 (lineage recorded). ✅

## Licensing, Privacy, and Retention

**LIMITATION (DATA HOLD trigger):** the result's source map does not explicitly document licensing/retention status per EVIDENCE-MODEL §5 field set (field present for some rows, not systematically). Remediation applied in this report: licensing = "public SEC filings / issuer releases — permitted for internal research use; verify terms before any redistribution or external publication"; retention = per project data policy, tombstone-capable (EVIDENCE-MODEL §6.3). Documented → HOLD-DATA-001 cleared by issuer (Data Steward). ✅

## Known Limitations

1. Market quote 1-day lag (≤7d bound OK).
2. Licensing/retention field not systematic in the source map (now documented here; source-map.md update pending a follow-up task if Founder directs).
3. XBRL fact licensing assumption recorded, not verified against terms.

## Downstream Artifacts Affected

EQUITY-RESEARCH-BRIEF.md (data status field); IC-DECISION-PACK.md (data status section); any org artifact consuming SRC-MKT must carry the staleness note.

## Required Remediation

None blocking for org-workflow use; licensing documentation completed in this report. A source-map.md field backfill is a follow-up item (Founder decision optional).

## Steward Sign-Off

DATA READY WITH LIMITATIONS — cleared for org-workflow consumption. **No canonical state touched.**
<!-- 2026-08-05 15:25 UTC+7 -->
