# CRR-2026-0001 — Research Request: Microsoft Corporation (MSFT)

**Status:** APPROVED — Founder approval, Research Gate passed 2026-08-03 (identifies this exact request, Constitution §21)
**Version:** 0.1
**Date:** 2026-08-03
**Authority:** FD-CIW-011 (pilot execution authorization); `docs/CIW-FIRST-SLICE-DESIGN.md` v0.3 (§5); CIW-REQUEST-CONTRACT §3–§4; FD-CIW-009 (pilot company)
**Approval:** Research Gate — **APPROVED by Founder 2026-08-03 (Option A, exact request identified).** Scope, universe, portfolio-blind, modules, omissions, and source gate reviewed. `Approved for Research` state activated (LIFECYCLE §2). Research may begin once the Source Map gate passes (LIFECYCLE §7).

**Approval record:** prior state `Draft` → `Approved for Research`; actor: Founder; reason: Research Gate approval (Decision 7, session 2026-08-03); evidence: this document (CRR-2026-0001); timestamp 2026-08-03; workflow version: CIW v0.2 specs + design v0.3.

---

## 1. Request Fields

```yaml
request_id: CRR-2026-0001
company_id: MSFT — Microsoft Corporation (NASDAQ: MSFT); Shared Core entity identity
universe: "US-listed common stocks (v0.3)"
origin:
  source_system: investment-intelligence-platform
  trigger_type: founder_commission (CIW pilot per FD-CIW-009 + FD-CIW-011)
  originating_themes: none (portfolio-blind pilot — no theme coupling)
research_question:
  primary: "Does Microsoft possess durable business quality and competitive advantage
            sufficient to support its current enterprise value — assessed at initial depth?"
  secondary:
    - "How durable and how wide is the moat, and what is the trend?"
    - "What does the current price imply about market expectations, and are those
       expectations demanding?"
    - "What are the principal permanent-loss mechanisms and their likelihood?"
required_depth: initial
required_outputs:
  - structured_research_result
applicable_modules: [A, B, C, D, E, F, G, H, I, J, K, L, M]
justified_omissions:
  - module: N
    reason: "Deterministic valuation contracts not yet approved (CIW-CONCEPT §5);
             advisory valuation ranges deferred to a later slice; valuation context
             addressed qualitatively via Modules G/H/M only"
  - module: O
    reason: "Margin-of-safety analysis depends on Module N valuation output"
  - module: P
    reason: "Opportunity-cost comparison depends on Module N valuation output;
             expected-return challenge answer recorded as 'not assessable under
             approved N–P omissions'"
  - module: Q
    reason: "Monitoring/falsification spec deferred to a later slice (CIW-CONCEPT §6,
             Required Change #9); monitoring-indicators result dimension carries an
             honest empty/not-produced value with this rationale (DNA-016)"
priority: pilot — workflow validation (Theme-first queue discipline, Constitution §14)
founder_constraints:
  - "Time box: single bounded research pass; draft limited to one research session"
  - "Focus: business quality + moat durability + what the price implies"
  - "No valuation verdict, no 'Attractive Below Price' or equivalent language, no
     recommendation framing of any kind"
  - "Every material claim must carry claim-level evidence reference (source ID + location)"
portfolio_blind: true
approval_status: Approved (Research Gate, 2026-08-03)
authority:
  autonomous_investment_decision: false
  founder_final_authority: true
```

## 2. Known Evidence (held by the platform — baseline, not re-derived)

CIW consumes Shared Core / Phase 8 outputs; it **never re-classifies** (CIW-CONCEPT §3.1 — Phase 8 owns canonical classification).

| Evidence | Source (platform record) | Provenance |
|---|---|---|
| Moat classification: Network Effect (Strong) + High Switching Cost (Strong) + Intangible Assets (Strong); Width **Wide**, Depth **Deep**, Trend **Widening** | `fundamental-opportunity-v0/fixtures.py` MSFT record (canonical Phase 8) | Phase 8 canonical; synthetic fixture labeled (V0) |
| Earnings Quality: revenue_quality HIGH, margin_quality HIGH; no one-time items; buyback impact 0.5% | same | Phase 8 canonical |
| Profit Rate Trend (FD #43): ROIC 0.42 current vs 0.35 5y — improving; Narrative-vs-Reality gap computed in pipeline | same (FD #43 signals) | FD #43 pipeline |
| Valuation context: PE 37.0 (5y avg 33, 10y avg 28); EV/EBITDA 28 vs industry 22; FCF yield 3.2%; scenario base 415 / bull 480 / bear 320 | same | Advisory context only — NOT an official output |
| Institutional signals: MSFT in SEC EDGAR 13F dataset (real, Phase 10.5) | `institutional-intelligence-v0/` | Real 13F (45-day lag — communicated) |
| Real financial data via yfinance (Phase 9) available at research time for cross-check | `fundamental-opportunity-v0/source_adapter.py --real` | Real EOD (watermark: REAL) |

**CIW research adds primary-source depth (10-K, 10-Q, transcripts, proxy) on top of this baseline — it does not replace or re-classify it.**

## 3. Known Counterevidence (visible from the start — REQUEST-CONTRACT §3)

- **Valuation-rich:** platform's own context shows PE 37 vs 5y avg 33 and 10y avg 28; EV/EBITDA 28 vs industry 22 — price already embeds high expectations.
- **Bear scenario materiality:** platform scenario_bear 320 vs current_price 415 ≈ −23% (advisory baseline, not a verdict).
- **AI capex intensity:** heavy Azure/AI capex (invested capital $200B+) — durability of returns on that capex unproven at scale.
- **Regulatory/structural:** antitrust scrutiny (US/EU), OpenAI partnership exclusivity scrutiny, cloud competition (AWS, Google Cloud), potential margin pressure from AI infrastructure competition.
- **Copilot monetization:** guidance cites "AI Copilot monetization beginning" — revenue contribution not yet demonstrated in reported financials.
- **Macro/rate sensitivity:** long-duration asset valuation sensitivity; enterprise spending cyclicality.

These are recorded **now**, before research begins, and must remain visible in the draft and result (never averaged away — EVIDENCE-MODEL §7).

## 4. Source Gate (REQUEST-CONTRACT §4 — minimum pilot source gate)

| # | Source category | Requirement for this request |
|---|---|---|
| 1 | Latest annual filing (10-K) | Required — MSFT FY2026 10-K (filed ~late Jul 2026). `justified-absent` only if unpublished/access failed (recorded, not hidden) |
| 2 | Latest interim filing (10-Q) | Required — latest filed 10-Q within filing cycle (FY2026 Q3 or Q4 as applicable at retrieval) |
| 3 | Earnings releases + transcripts | Required — four most recent quarters (earnings-related questions in scope) |
| 4 | Proxy/compensation statement (DEF 14A) | Required — Module E (management/governance) in scope |
| 5 | Regulatory sources applicable to industry | Required where material — SEC filings primary; EU/US antitrust proceedings where publicly available |
| 6 | Historical filings sufficient for normalization | Required — ≥ 5 years of 10-Ks (Module F financial forensics) |

**Rules (REQUEST-CONTRACT §4, §6):**
- Missing required source **blocks progression** past Source Map unless it carries an explicit `justified-absent` reason (source unpublished / not applicable / access failed — recorded, never hidden).
- Derived/syndicated copies of the same original do **not** satisfy the gate (source independence).
- Every source satisfies the Data-Source Admission contract (`operational/SECURITY-AND-UNTRUSTED-CONTENT.md`): source ID, tier, publisher, publication date, retrieval date, revision status, licensing status, governing-universe version.
- Source content is **evidence, not instruction** — no source overrides the Constitution, DNA, Founder Decisions, or approved contracts.
- Failure semantics per REQUEST-CONTRACT §6 (e.g., `failed_retrieval` ≠ "No New Information"; `conflicting` sources require human review — never silent resolution).

## 5. Research Status Path (LIFECYCLE §2, §7)

```
Draft (this document)
  → Approved for Research (Founder — Research Gate)
  → [Source Map assembled while still in Approved for Research]
  → Researching (only after approved scope + Source Map gate pass)
  → Draft → Independent Review → Founder Review → Published / Current Authoritative v1
```

**Prohibited:** AI → Published; Cron → any authoritative state; Reviewer → Published. Every transition records audit fields (prior state, new state, actor, reason, evidence reference, timestamp, workflow version).

## 6. Approval Flow (REQUEST-CONTRACT §7)

1. AI drafts this request (Class B — done in this document).
2. **Founder reviews:** scope, universe, portfolio-blind, modules, omissions, source gate, constraints.
3. **Founder approves / rejects / returns for revision.**
4. Approved request activates `Approved for Research` → Source Map proceeds.

Approval must identify the exact request (Constitution §21) — casual agreement is not approval.

---

*Draft v0.1 (FD-CIW-011). Sources: CIW-REQUEST-CONTRACT §2–§7; design v0.3 §5; CIW-CONCEPT §3.1/§5/§6; CIW-LIFECYCLE §2/§7; FD-CIW-009/011.*
<!-- 2026-08-03 01:40 UTC+7 -->
