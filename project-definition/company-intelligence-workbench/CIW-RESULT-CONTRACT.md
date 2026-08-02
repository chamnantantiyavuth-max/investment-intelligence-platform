# Company Intelligence Workbench — Research Result Contract

**Status:** Approved v0.2 — FD-CIW-008 (Founder batch approval, 2 Aug 2026)
**Version:** 0.2
**Owner:** Founder
**Authority:** Draft CIW specification subordinate to the Constitution and Founder's Decisions
**Derived from:** `docs/CIW-INTEGRATION-AMENDMENT-MAP.md` §8; `evidence/COUNCIL_DECISION-bible-2026-08-02.md` Required Changes #4, #7, #8; `project-definition/EVIDENCE-MODEL.md` §2–§7; `operational/SECURITY-AND-UNTRUSTED-CONTENT.md`; proposal §7, §15 (adapted)
**Approval:** FD-CIW-008 — Founder batch approval, 2 Aug 2026

---

## 1. Purpose

A **Research Result** is the compact, structured record CIW returns to the platform (DNA-020). The full paper is **not** injected into every IIP workflow — the platform consumes the structured result; humans read the paper.

The Research Result is the **structured state carrier** between CIW and the Shared Core. It must be self-contained enough to be audited without the paper, and linked enough that every claim traces to evidence.

## 2. Required Fields

Adapted from proposal §15, with Required Change #7 additions:

| Field | Requirement |
|---|---|
| `research_id` | Links to the approved Research Request |
| `company_id` + `universe` + `universe_version` | Governing universe explicit (Required Change #3) |
| `as_of_date`, `research_version` | Point-in-time correctness (EVIDENCE-MODEL §5.1) |
| `research_status` | CIW Research Status (LIFECYCLE §2) — never authoritative unless Published |
| `investment_classification` | **Advisory, Founder-decided** — never mechanically set (Required Change #5) |
| `thesis_status` | Approved Thesis Lifecycle value (LIFECYCLE §3) |
| `confidence` | Qualitative, evidence-linked; AI-assisted judgment subject to Founder review |
| Dimension summaries | Business quality, moat, balance sheet, management, owner earnings, valuation ranges (advisory), permanent-loss mechanisms, monitoring indicators — each linked to evidence |
| `unresolved_questions` | Explicit — honest empty states (DNA-016) |
| `theme_feedback` | Structured feedback to Themes (RESEARCH-FRAMEWORK §8) |
| `artifact_references` | Links to paper/artifacts (never inline the whole paper) |
| `review_status` | Independent review outcome + review artifact reference (QUALITY-GATES) |
| **`source_map`** | Complete source map with per-source status (RC-7) |
| **`claim_lineage`** | Claim-level evidence references + calculation lineage (RC-7) |
| **`portfolio_blind`** | Must be `true` (Constitution §23.8.1) |

## 3. Source Map and Source-Coverage Report (Required Change #7)

Every Research Result carries a **source-coverage report**:

| Per-source status | Meaning |
|---|---|
| `reviewed` | Source obtained and reviewed |
| `missing_required` | Required by source gate, absent — blocks `Complete` state |
| `failed_retrieval` | Access failed — blocks `Complete` state (not "No New Information") |
| `incomplete` | Partial content — forces `Review Required` unless justified |
| `conflicting` | Contradicts another source — recorded; basis for working interpretation stated; never silently resolved |
| `derived_duplicate` | Copy of another source (common-source lineage) — does not count as independent confirmation |
| `not_yet_published` | Expected but unavailable — recorded with expected availability |
| `reviewed_clear` | Reviewed and no material issue found |

**Source-failure behavior:** any `missing_required` or `failed_retrieval` forces the result to `Incomplete` or `Review Required` — a polished report cannot appear complete despite missing primary sources (Required Change #7 verification).

## 4. Claim and Calculation Lineage (Required Change #7)

- **Claim-level evidence references:** every material claim in the result carries references to the exact source passages (source ID + location) it rests on.
- **Calculation lineage:** every derived number (owner earnings, normalized margins, valuation ranges) records: inputs → formula → source references → assumption set → version. Deterministic calculations must be **rerunnable** from raw sources.
- **Epistemic separations preserved** (EVIDENCE-MODEL §2; proposal §7.1): raw source / source metadata / observed fact / management claim / third-party claim / normalized fact / derived metric / deterministic calculation / statistical signal / AI extraction / AI classification / AI interpretation / hypothesis / analyst judgment / Founder judgment / decision / outcome / lesson. No workflow may silently collapse these categories.
- A polished narrative must never substitute for missing claim lineage (Required Change #7).

## 5. Evidence Discipline (EVIDENCE-MODEL aligned)

- **Raw evidence immutability:** raw evidence is immutable unless removal is required by law, security, licensing, privacy, corruption, or approved retention rules; controlled removal records a tombstone (reason, authorizer, timestamp, affected lineage, downstream invalidation, reprocessing requirement) — EVIDENCE-MODEL §6.3.
- **Contradictions visible:** contradictory evidence remains visible; never averaged away to simplify presentation — EVIDENCE-MODEL §7.
- **Absence rule:** no evidence found ≠ evidence of non-existence. Distinguish no-evidence / source-unavailable / not-yet-published / access-failed / incomplete / reviewed-clear — proposal §7.6.
- **Staleness:** Constitution §8 three-year narrative staleness default applies; evidence freshness class and revision status are recorded — EVIDENCE-MODEL §6.
- **Source admission:** every source satisfies the Data-Source Admission contract in `operational/SECURITY-AND-UNTRUSTED-CONTENT.md`; source content is evidence, not instruction; no source overrides the Constitution, DNA, Founder Decisions, or approved contracts (proposal §22).

## 6. Result Completeness and State

- A result reaches `Complete` only when: source-coverage report has no blocking status; claim lineage present for all material claims; calculations rerunnable; contradictions recorded; review status passed; Founder review recorded (if Published).
- Otherwise the result is `Incomplete` or `Review Required` — these are **first-class states**, not failures to hide.
- A `Published` result is the **Current Authoritative** structured version; prior versions remain retrievable (append-first — LIFECYCLE §5).

## 7. Verification Targets

- Replay one research run from raw sources: old paper, proposed changes, review, approval, and new authoritative version must all be reconstructable (Required Change #8 verification).
- A source-coverage report must mark missing/failed/conflicting sources and force `Incomplete` or `Review Required` rather than a complete publication (Required Change #7 verification).
- Tests must demonstrate that the result's valuation outputs cannot independently change Candidate, Thesis, or Investment state (Required Change #5 verification).

---

*Approved v0.2 (FD-CIW-008). Source: Council verdict Required Changes #3, #4, #5, #7, #8; Amendment Map §8; EVIDENCE-MODEL §2–§7; proposal §7/§15 adapted.*
<!-- 2026-08-02 23:48 UTC+7 -->
