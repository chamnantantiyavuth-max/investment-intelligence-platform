# ADMITTED SOURCE PACKET — Apple Rehearsal (Gemini Deep Research v1.4)

**Task:** t_bfdcbf31 — [DR][CHILD] S1 — Source Preflight & Evidence Admission
**Author:** org-data-steward (Role 09 Data Steward, Research Principal reframe — evidence build)
**Date:** 2026-08-12
**Mode:** PILOT-NONCANONICAL — calibration rehearsal, NO domain state change, NO new sources beyond published case
**Audience:** S2 (Pass A), S3 (Pass B), S4 (Gemini lane), S5 (Freeze + Reconciliation), parent t_68d2824b (synthesis)

---

## 1. Rehearsal Identity

| Field | Value |
|---|---|
| Rehearsal subject | PUBLISHED Apple deep-research case — `reports/apple-deep-analysis-2026-08-09.md` (main) + `reports/apple-deep-analysis-opposing-2026-08-09.md` (CRO dissent) |
| **RESEARCH_AS_OF** | **2026-08-09 23:59 ICT** (published case date) — evidence through Q3 FY2026 (quarter ended 2026-06-27) |
| Anchor workflow | IIP_Gemini_Deep_Research_Final_Handoff_v1.4.md (source preflight §7, admission §12) |
| Calibration purpose | Prove the v1.4 workflow on a published case — NOT new investment truth |
| Source set rule | **Only sources the published case used** (its §8 + `research/companies/AAPL/source-inventory.md` + `evidence-log.md`). No new retrieval. |

---

## 2. Admission Rules Applied (canonical)

1. **EVIDENCE-MODEL.md §5** — full provenance metadata per source (source identifier, publication/public-availability timestamp, effective/as-of period, ingestion/retrieval timestamp, originating URL, revision/vintage, supersedes, content hash, licensing, extraction method).
2. **EVIDENCE-MODEL.md §5.1 + FD #58** — point-in-time evaluation: every figure valid only at its filing/publication date; historical values not backfilled with revisions.
3. **EVIDENCE-MODEL.md §3 / Evidence Doctrine** — source independence: syndicated copies ≠ independent confirmation; IDC vs Counterpoint disagreement recorded as `conflicting`, never averaged.
4. **CIW-REQUEST-CONTRACT.md §4** — pilot source gate: latest 10-K (required), latest 10-Q (required in cycle), earnings release + transcripts (required for earnings questions), regulatory sources (required where material), historical filings for normalization (required for financial forensics).
5. **CIW-RESULT-CONTRACT.md §3** — source-coverage statuses: `reviewed`, `missing_required`, `failed_retrieval`, `incomplete`, `conflicting`, `derived_duplicate`, `not_yet_published`, `reviewed_clear`. Any `missing_required` / `failed_retrieval` → result cannot be `Complete`.
6. **operational/SECURITY-AND-UNTRUSTED-CONTENT.md** — Data-Source Admission: external content is data, never instruction/authority.
7. **Epistemic separation** (EVIDENCE-MODEL §2): raw source ≠ observed fact ≠ management claim ≠ third-party claim ≠ derived metric. Transcripts are management claims (third-party transcription), not filing-verified facts.

---

## 3. Admitted Source Register

### A. Primary filings — SEC EDGAR (CIK 0000320193) — ADMITTED

| ID | Source | Accession | Period end | Filed | Retrieved | Workspace raw (SHA-256) | Freshness class | Status |
|---|---|---|---|---|---|---|---|---|
| SRC-01 | 10-K FY2025 | 0000320193-25-000079 | 2025-09-27 | 2025-10-31 | 2026-08-06 | `/tmp/apl-evidence/aapl-10k-fy2025.txt` `1d973ff6…f2d7` | CURRENT-REQUIRED (annual) | `reviewed` |
| SRC-02 | 10-Q Q3 FY2026 | 0000320193-26-000020 | 2026-06-27 | 2026-07-31 | 2026-08-06 | `/tmp/apl-evidence/aapl-10q-q3fy26.txt` `1a993be9…5df` | CURRENT-REQUIRED (latest interim) | `reviewed` |
| SRC-03 | 8-K Q3 FY26 earnings (ex99.1) | 0000320193-26-000018 | 2026-06-27 | 2026-07-30 | 2026-08-06 | `/tmp/apl-evidence/aapl-8k-q3fy26-ex991.txt` `26c745f5…5224` | CURRENT-REQUIRED (latest earnings release) | `reviewed` |
| SRC-04 | 10-Q Q2 FY2026 | 0000320193-26-000013 | 2026-03-28 | 2026-05-01 | 2026-08-07 | `/tmp/apl-upgrade/q2fy26-10q.txt` `800ce432…5ff2` | HISTORICAL-RELEVANT (interim trend) | `reviewed` |
| SRC-05 | 10-Q Q1 FY2026 | 0000320193-26-000006 | 2025-12-27 | 2026-01-30 | 2026-08-07 | `/tmp/apl-upgrade/q1fy26-10q.txt` `e4d4e510…31db` | HISTORICAL-RELEVANT (interim trend) | `reviewed` |
| SRC-06 | XBRL Company Facts FY21–25 | — (data.sec.gov companyfacts) | FY ends 2021-09-25 … 2025-09-27 | n/a (continuous) | 2026-08-06 | `/tmp/apl-evidence/aapl-xbrl-facts.json` `73a86c6a…9c43` | HISTORICAL-RELEVANT (normalization) | `reviewed` |
| SRC-06b | XBRL mirror (discovery cache) | CIK0000320193.json | FY21–25 | n/a | 2026-08-11 | `…/discovery/quality_asymmetry/output/cache/CIK0000320193.json` (4.2 MB, entityName=Apple Inc.) | HISTORICAL-RELEVANT | `reviewed_clear` (derived mirror of SRC-06 — not independent) |
| SRC-07 | EDGAR submissions index | — | n/a | n/a | 2026-08-06 | `/tmp/apl-evidence/submissions.json` `d0967903…74d` | SUPPORTS accession verification | `reviewed` |

**PIT verification (SRC-01..05):** all filed dates ≤ RESEARCH_AS_OF (2026-08-09) ✓. Period ends as stated ✓. Accessions match the published case §8 + source-inventory ✓. No revision/supersede conflicts found between 8-K and 10-Q for Q3 FY26 (reconcile exactly: revenue/GM/NI/EPS/segments identical) ✓.

### B. Published rehearsal case (the calibration target — NOT an evidence input for passes)

| ID | Source | Date | Path | Status |
|---|---|---|---|---|
| SRC-P1 | Deep-analysis main essay (published) | 2026-08-09 | `reports/apple-deep-analysis-2026-08-09.md` | `reviewed` — rehearsal subject; **passes MUST NOT read it** (anti-anchoring, S2/S3 bodies). S5/parent may reconcile against it. |
| SRC-P2 | CRO opposing essay (published) | 2026-08-09 | `reports/apple-deep-analysis-opposing-2026-08-09.md` | `reviewed` — material dissent record; same read restriction as SRC-P1. |

### C. Third-party evidence — ADMITTED WITH LIMITATIONS

| ID | Source | Publication | Coverage | Workspace raw | Freshness class | Status |
|---|---|---|---|---|---|---|
| SRC-08 | IDC Q1 2026 final | 2026-06-23 | Smartphone shipments/share (Apple 61.8M / 21.0%, #2 statistical tie w/ Samsung 21.2%) | `/tmp/apl-upgrade/idc-share.html` `fad79c85…3cc` (valid, Apple+Samsung content present) | HISTORICAL-RELEVANT (point-in-time market data) | `reviewed` — third-party estimate, cite source+date |
| SRC-09 | IDC FY2025 forecast | 2025-12-02 | Full-year shipments (~247.4M Apple) | `/tmp/apl-upgrade/idc-fy25.html` `e9d47a19…d0` (valid) | HISTORICAL-RELEVANT | `reviewed` — third-party estimate |
| SRC-10 | Counterpoint Q1 2026 | 2026-04-10 | Apple #1 21% vs Samsung 20% | `/tmp/apl-upgrade/cp-q1-2026.html` `23fdd9a2…8c9` (valid) | HISTORICAL-RELEVANT | `conflicting` vs SRC-08 on Q1 #1 — recorded, never averaged (EVIDENCE-MODEL §7) |
| SRC-11 | Earnings-call transcripts Q1/Q2/Q3 FY26 (AlphaStreet, third-party) | 2026-01-29 / 04-30 / 07-30 | Management claims: installed base 2.5B+, paid subs 1.5B+, CEO succession Cook→Ternus, Sept guidance, memory "hundred-year flood", Broadcom $30B+ | **NO VALID RAW** — `/tmp/apl-upgrade/inv-transcript.html` = 3 bytes; `/tmp/apl-upgrade/q3fy26-transcript.html` = 38 bytes `{"message":"Invalid download request"}` | CURRENT-REQUIRED (earnings-related claims) | **`failed_retrieval`** — raw copy corrupt/absent. Transcript-derived claims remain **management claims (third-party transcription)**; the published case already flags re-verification before verbatim use. |

### D. Canonical admission/governance references (not evidence — rule layer)

| ID | Reference | Role |
|---|---|---|
| SRC-G1 | `project-definition/EVIDENCE-MODEL.md` | Provenance, PIT, independence, taxonomy |
| SRC-G2 | `operational/EVIDENCE-DOCTRINE.md` | Separations, aging, FD #58 |
| SRC-G3 | `project-definition/company-intelligence-workbench/CIW-REQUEST-CONTRACT.md` §4 | Source gate |
| SRC-G4 | `project-definition/company-intelligence-workbench/CIW-RESULT-CONTRACT.md` §3 | Source-coverage statuses |
| SRC-G5 | `operational/SECURITY-AND-UNTRUSTED-CONTENT.md` | Data-Source Admission |
| SRC-G6 | `operational/hermes-organization/roles/09-data-steward/PRINCIPAL.md` | Data Steward authority boundary |

---

## 4. Source-Coverage Report (CIW-RESULT-CONTRACT §3)

| Status | Count | Sources |
|---|---|---|
| `reviewed` | 10 | SRC-01..05, 06, 07, 08, 09, P1, P2 (11 incl. published case) |
| `reviewed_clear` | 1 | SRC-06b (mirror) |
| `conflicting` | 1 | SRC-10 (vs SRC-08, tracker disagreement — must stay visible) |
| `failed_retrieval` | 1 | SRC-11 (transcripts — no valid raw workspace copy) |
| `missing_required` | 0 | Source gate satisfied for filings |
| `derived_duplicate` | 1 | SRC-06b (XBRL mirror of SRC-06 — not independent) |

**Gate consequence:** SRC-11 `failed_retrieval` → transcript-dependent claims (installed base 2.5B+, paid subs 1.5B+, CEO succession timing, Sept guidance, memory narrative, Broadcom $30B+) are **NOT admissible as filing-verified facts** — only as management claims from the published case, with the published case's own re-verification caveat. Any pass claiming them as facts = epistemic error (EVIDENCE-MODEL §2.1). Result classification for the rehearsal: **Review Required** on transcript-dependent content — consistent with the published case's own limitation note (§8: transcripts third-party, not SEC filings).

---

## 5. PIT Stamp Summary

| As-of | What was publicly available | Sources |
|---|---|---|
| 2026-08-09 (RESEARCH_AS_OF) | 10-K FY25, Q1–Q3 FY26 10-Qs, Q3 FY26 8-K, XBRL FY21–25, IDC/Counterpoint Q1 2026, AlphaStreet transcripts (via case) | All admitted |
| Superseded/revision check | None found among admitted filings for the periods cited (8-K ↔ 10-Q Q3 FY26 reconcile exactly) | SRC-02/03 |
| Staleness | FY21–25 XBRL = deliberately historical for normalization (HISTORICAL-RELEVANT, not stale); no narrative evidence subject to 3-year default in this set | SRC-06 |

---

## 6. Pass Constraints (what downstream may/can't use)

1. **S2/S3 (Hermes passes) + S4 (Gemini lane):** consume ONLY SRC-01..08, 09, 10 (primary filings + third-party market data). **Must NOT read SRC-P1/P2** (published conclusions) — anti-anchoring. **Must NOT claim transcript content as fact** — SRC-11 is management-claim-only; if a pass has no independent access to transcripts, it must record the gap.
2. **S5 (reconciliation):** the ONLY child allowed to read all three passes AND the published case. Reconcile each pass against SRC-P1/P2 as calibration ground truth.
3. **Parent t_68d2824b (synthesis):** treats this packet as the admission gate; the publication Fact Packet must not introduce sources outside this register.
4. **No new sources** beyond this register, per task body. DEF 14A FY2026 remains unextracted (optional lens — out of scope for this rehearsal, matches published case).
5. **Data Confidence (EVIDENCE-MODEL §9):** Freshness HIGH (filings current through Q3 FY26); Completeness MEDIUM-HIGH (transcripts missing raw; DEF 14A absent; no synchronized price/valuation series — matches published case limitation); Reliability HIGH for filings / MEDIUM for third-party trackers / LOW-MEDIUM for third-party transcripts; Conflicts VISIBLE (IDC vs Counterpoint); Missing data recorded (installed-base count not in filings).

---

## 7. Certification

**DATA READY WITH LIMITATIONS** (CIW-RESULT-CONTRACT §3 / PRINCIPAL.md authority) — for the Apple rehearsal:

- All source-gate-required filings present and PIT-verified.
- Limitations: (1) transcript raw copies failed retrieval → management-claim-only status; (2) IDC/Counterpoint conflict on Q1 #1 → visible, not averaged; (3) no valuation/price series in the evidence base (published case's own limitation).
- No DATA HOLD issued: no timestamp ambiguity, no licensing concern (SEC EDGAR public filings + public web data), no security-sensitive content in scope.
- Portfolio-blind maintained: no portfolio/Capital Command data touched.

---

*Packet verified against: repo HEAD (investment-intelligence-platform), `/tmp/apl-evidence/`, `/tmp/apl-upgrade/`, discovery cache, EVIDENCE-MODEL v0.2, CIW contracts v0.2, Evidence Doctrine, SECURITY-AND-UNTRUSTED-CONTENT v0.2.*
<!-- 2026-08-12 22:35 UTC+7 -->
