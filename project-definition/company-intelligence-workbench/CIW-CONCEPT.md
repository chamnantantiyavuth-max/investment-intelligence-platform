# Company Intelligence Workbench — Concept

**Status:** Approved v0.2 — FD-CIW-008 (Founder batch approval, 2 Aug 2026)
**Version:** 0.2
**Owner:** Founder
**Authority:** Draft CIW specification subordinate to the Constitution and Founder's Decisions; does not authorize implementation
**Derived from:** `docs/CIW-INTEGRATION-AMENDMENT-MAP.md` §5–§6, §13; `evidence/COUNCIL_DECISION-bible-2026-08-02.md` Required Changes #1–#5, #9; FD-CIW-001..007; FD #24, #40, #44
**Approval:** FD-CIW-008 — Founder batch approval, 2 Aug 2026

---

## 1. What CIW Is

The Company Intelligence Workbench (CIW) is the **deferred Phase 11 Deep Research Handoff workflow** inside the approved **Fundamental & Opportunity Intelligence** path. It converts a small number of approved research requests into deeply researched, evidence-backed, falsifiable, and reviewable company cases.

CIW is:

- a **workflow**, not a fifth product layer (Required Change #1; Constitution §2 product structure retained);
- a **bounded module** in the existing repository when implementation is separately authorized (FD-CIW-002) — no sibling repository, no separate Hermes profile without evidence of a real context or permission need;
- a **research methodology**, not an operational standard (FD-CIW-003);
- **advisory**: it improves human judgment, never replaces it (Constitution §12).

CIW is **not**:

- a replacement Bible or consolidated authority document (Required Change #11);
- an investment authority, a trading/execution system, or a portfolio allocator (Constitution §18);
- a company-first screening system replacing the Theme-first direction (DNA-004, DNA-017).

## 2. Authorization Status (Read First)

**Phase 11 remains DEFERRED. FD #44 remains in force.**

- FD-CIW-001 approves the CIW **capability in principle only** — it does NOT authorize implementation, automation, schemas, repository changes, or a pilot (Required Change #2).
- A **separate, named Founder Decision superseding FD #44** is required before any implementation, pilot, schema, or automation begins.
- This specification is **documentation only**. Nothing in it activates code, data sources, pipelines, or scheduled jobs.
- Every future approval must name the exact artifact being approved (Constitution §21; casual agreement is not approval).

## 3. Position in the Operating Model

Per `INVESTMENT-INTELLIGENCE-OPERATING-MODEL.md` §3–§5, CIW lives **inside** the Fundamental & Opportunity Intelligence path — it is not a new peer path and does not change the Dual Intelligence Operating Model (FD #24).

CIW **consumes** Shared Core capabilities (source registry, evidence, entity identity, Theme Intelligence, Candidate Intelligence) and **consumes** the outputs of Fundamental & Opportunity sub-domains §5.1–§5.6 (business quality, moat, earnings quality, valuation context, value trap).

CIW deep research **extends** Phase 8 Company Analysis; Phase 8 owns the canonical classification. CIW never re-classifies a Moat, Earnings Quality rating, or Value Trap verdict — it supplies deeper evidence for those classifications (Required Change #1).

### 3.1 Responsibility Matrix (Required Change #1)

| Responsibility | Owner |
|---|---|
| Moat classification / width–depth–trend | Phase 8 (Shared Core canonical) |
| Earnings quality rating | Phase 8 |
| Value trap detection | Phase 8 |
| Source map / source gate | CIW (new, bounded) |
| Owner earnings / valuation scenarios | CIW — advisory; deterministic calculation contracts deferred |
| Independent challenge | Shared Core Independent Challenge (Phase 8 spec) — CIW executes with separation |
| Founder review / approval | Founder Decision Gate (Operating Model §9) |

Each responsibility has exactly **one owner**. CIW complements; it does not duplicate or override.

## 4. Investable Universe Boundary (Required Change #3)

- The V0 investable screening universe remains **intentionally bounded to US-listed common stocks and suitable ADRs** (DNA-017 approved text — the proposal's "Controlled Investable Scope" rewording is rejected).
- CIW may research a company **outside** the investable universe only for **global observation or non-investable research** purposes, and such research **never** admits the company to an investable Candidate workflow without a separate amendment.
- Every Research Request and every Research Result must carry its **governing universe and version** and must reject out-of-scope investable classification absent a separate amendment (Required Change #3 verification).

## 5. Valuation Is Context, Not Veto (Required Change #5)

- Valuation outputs (Modules N–Q of the research framework) are **advisory scenario analysis only** (FD #24, FD #40, `FUNDAMENTAL-OPPORTUNITY-INTELLIGENCE.md` §3.6).
- CIW **cannot** mechanically produce "Investable Candidate", "Attractive Below Price", promotion, rejection, or any portfolio action from valuation output.
- Margin-of-safety displays, maximum rational price, opportunity-cost comparisons, and sell/reduce analytical categories are **analytical scenarios**, not recommendations or vetoes.
- Official use of valuation requires **separately approved deterministic calculation contracts** (owner earnings, maintenance capex, discount rates, terminal assumptions, normalization, required return) — currently deferred.
- Verification target: valuation outputs must be unable to independently change Candidate, Thesis, or Investment state (Required Change #5).

## 6. Pilot Scope (Required Change #9, FD-CIW-007)

- **Pilot company selection is deferred** until the capability boundary, source gate, methodology authority, and pilot scope are approved (FD-CIW-007). The pilot company will be **US-listed / suitable ADR, source-rich, and portfolio-blind** (no portfolio data supplied; Constitution §23.8.1).
- The **first slice** validates only: **Approved Research Request → Source Map → bounded initial research → Independent Challenge → Founder Review → structured Research Result**.
- Deferred to later slices (NOT part of the first slice): earnings automation, recurring scheduling, canonical auto-publication, Obsidian synchronization, expanded file tree, database migration, new repository/profile, earnings-update subsystem.
- The first slice must be completable **without Cron, a new repository/profile, a database migration, or an earnings-update subsystem** (Required Change #9 verification).
- Research Modules are **applicability-based** with justified omissions — never a mandatory long-report checklist (Required Change #9).

## 7. Boundaries and Non-Scope

CIW does not (FD-CIW-001..007; Constitution §18; proposal §11.3, mined within approved boundaries):

- select companies from the global universe without an approved path;
- replace Theme Intelligence, Alpha Momentum, or the Close System;
- manage portfolio exposure, set position size, execute trades, or approve investment action;
- automatically change official strategy rules or publish material conclusions without review;
- treat the framework as a mechanical scoring model;
- receive actual holdings, position sizes, cost basis, or transaction history — **portfolio-blind by default** (Constitution §23.8.1; proposal §6.3);
- use scheduling or delegation to bypass Founder gates.

## 8. Canonical Additions Adopted (Amendment Map §3)

- **DNA-019 — Deep Research Must Earn Its Cost:** a long report is not proof of deep research; deep research must be justified by expected decision value, uncertainty reduction, strategic relevance, or learning value.
- **DNA-020 — Company Research Must Return Intelligence to the System:** company research must return structured findings to Candidate Intelligence, Theme Intelligence, industry maps, evidence progression, coverage-gap detection, and learning/postmortems — never an isolated paper archive.

These are recorded here as the intended additions; the exact DNA amendment is issued separately under Constitution §21 after this spec is approved.

## 9. Relationship to Authority Hierarchy

```
Constitution v0.4 > Founder's Decisions (#1–44 + FD-CIW-001..007) > Approved Domain Specifications > Operational doctrine
```

This document sits at the **Approved Domain Specification** level once approved. It derives from, and never alters, higher authority. Where this draft appears to extend higher-authority documents, the higher authority controls.

---

*Approved v0.2 (FD-CIW-008). Source: Council verdict Required Changes #1–#5, #9, #11; Amendment Map §5–§6, §13; FD-CIW-001..007.*
<!-- 2026-08-02 23:48 UTC+7 -->
