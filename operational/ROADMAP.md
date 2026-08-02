# Roadmap

## Phase 0 — Constitution and Product Definition
Approve foundation documents.
**Status: Complete**
- Constitution v0.4 (AI Operating Constitution §23, FD #23)
- Operating Model v0.1 (Dual Intelligence paths, FD #24)

## Phase 1 — Domain Definition
Define Evidence, Theme, Candidate, Human Review, and Knowledge models.
**Status: Complete**
- 10 domain specifications approved (project-definition/)
- FD #1-25 approved
- Nick Intelligence Integration (FD #25) — 11 model enhancements

## Phase 2 — Alpha Momentum V0 Design
Controlled universe, controlled themes, rule-pack contracts, fixtures, acceptance criteria.
**Status: Complete** (21-22 July 2026)

Completed checkpoints:
- Design Plan v0.1 (AM-V0-DESIGN-PLAN-v0.1)
- Gate A complete: 35/35 slots approved, 6 waves + DR-006
- Gate B complete: 143 themes (DR-005)
- Gate C complete: 7 HC slots, 20 acceptance scenarios, 10 ACs
- Gate D complete: independent audit passed, 4 findings resolved
- DR-006 (Canonical Theme-Role Ownership) approved

## Phase 3 — Alpha Momentum V0 Implementation
Synthetic data and complete end-to-end vertical slice.
**Status: Complete** (22 July 2026)

- 6-stage pipeline (S1 Universe → S6 Queue)
- 3 themes, 5 candidates (including NVDA multi-theme)
- Claude-inspired HTML UI
- All 10 ACs verified
- Provisional technology: Python + pandas + Jinja2

## Phase 4 — Real EOD Data
Source adapters, raw preservation, normalization, freshness, reconciliation.
**Status: Complete** (22 July 2026)

- yfinance source adapter (source_adapter.py)
- 24h JSON cache
- run_real.py entry point (system Python 3.14 due to numpy compat)
- run.py = synthetic fixtures

Phase 5 — Theme Intelligence V1
Weak Signal Inbox, anomalies, Theme Hypotheses, Experimental Theme Radar.
**Status: Complete** — FD #27, 23 July 2026

## Phase 6 — Learning Loop
Outcomes, postmortems, approved lessons, narrative export.
**Status: Complete** — FD #28, 24 July 2026

## Phase 7 — Close System Definition and Vertical Slice
Macro, ETF, commodity, suitability, opportunity, capital-lock-up risk.
**Status: Complete** — FD #39, 25 July 2026
- Q-Conditions (exit rules) + O'Neil/Minervini Rule Pack spec delivered

## Phase 8 — Fundamental & Opportunity Intelligence
Fundamental workbench: Macro, Industry, Product, Company, Earnings, Valuation Context.
**Status: Complete** — FD #40, 25 July 2026

## Phase 9 — Real Data Integration
Feed yfinance real financial data into Fundamental & Opportunity pipeline.
**Status: Complete** — FD #41, 26 July 2026

- source_adapter.py: yfinance → company dict + 24h JSON cache
- pipeline.py: accepts optional companies param (None = fixtures)
- run.py --real: real data mode
- Display: dynamic watermark (SYNTHETIC vs REAL EOD)
- Tickers: AAPL, MSFT, NVDA, GOOGL, AMZN, META, TSLA, JNJ (8)

## Phase 10 — Institutional Intelligence
Track hedge fund & institutional investor 13F filings, concentration ratios, and conviction signals.
**Status: Complete** — FD #42, 26 July 2026; Phase 10.5 real 13F via SEC EDGAR (FD #42 amended, 28 July 2026)

- SEC 13F filings → InstitutionalSignal output
- Concentration Ratio → Conviction (Max/High/Moderate/Low/Minimal)
- Action Detection (NEW/ADD/REDUCE/EXIT/MAINTAIN)
- Super-Investor Watchlist (~60 funds, 5 categories)
- Feeds: AM (conviction boost), FO (Hidden Signals), Theme (sector rotation), CS (macro positioning)

## Phase 11 — Deep Research Handoff

Company Intelligence Workbench (CIW): bounded deep-research handoff within the Fundamental & Opportunity path (Operating Model §5.7).
**Status: Concept + specs approved; implementation deferred.**
- Concept approved in principle (FD-CIW-001, 2 Aug 2026) — NOT a fifth product layer
- CIW spec v0.2 approved (FD-CIW-008, 2 Aug 2026): `project-definition/company-intelligence-workbench/` (CONCEPT, RESEARCH-FRAMEWORK, LIFECYCLE, REQUEST-CONTRACT, RESULT-CONTRACT, QUALITY-GATES, PUBLICATION-STANDARD)
- Implementation, pilot, schemas, and automation remain DEFERRED until a separate named Founder Decision supersedes FD #44
- Pilot company selection deferred (FD-CIW-007) — shortlist after targeted amendments

---

**Amendment record (Constitution §21):** Phase 11 row filled 2026-08-02 — affected FD: FD-CIW-001, FD-CIW-008; reason: previously empty row; trade-offs: none (deferral status unchanged); downstream impact: CIW specs; Founder approval: FD-CIW-008 (batch); amendment history: Phase 11 empty → filled with CIW status.
<!-- 2026-08-02 23:45 UTC+7 -->
