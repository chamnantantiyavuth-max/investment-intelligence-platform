# Fundamental & Opportunity Intelligence

**Status:** Approved Domain Specification
**Version:** 0.1
**Owner:** Founder
**Authority:** Approved Domain Specification subordinate to the Constitution and Founder's Decisions
**Derived from:** INVESTMENT-INTELLIGENCE-OPERATING-MODEL.md §5; CLOSE-SYSTEM-PRODUCT-RADAR.md (5 Intelligence Layers); FD #24
**Approval:** TBD (Founder review pending)

---

## 1. Strategy Identity

### 1.1 What It Is

Fundamental & Opportunity Intelligence is the **second intelligence path** in the Dual Intelligence Operating Model. It evaluates **business quality, structural opportunity, and evidence of durable competitive advantage** — answering a different question from Momentum.

| Path | Question It Answers | Active |
|---|---|---|
| **Momentum & Market Leadership** | What is working now? Where is leadership emerging? | V0 ✅ |
| **Fundamental & Opportunity** | What is built to last? Where is quality mispriced? | V1+ |

The two paths are complementary, not competitive. A candidate may be fundamentally strong but not yet momentum-ready — or momentum-ready with only moderate long-term quality. The platform makes this distinction visible.

### 1.2 Philosophy

| Principle | Description |
|---|---|
| **Quality First** | The primary lens is business quality — moat, unit economics, management, and competitive position |
| **Evidence Over Narrative** | Every quality assessment must be traceable to specific evidence, not story-telling |
| **Patience Compatible** | Long holding periods are natural when the thesis is structural quality at a reasonable price |
| **Valuation is Context, Not Veto** | Elevated valuation does not automatically reject — it is one data point among many |
| **Layers × Domains** | Analysis is structured as an analytical matrix: 5 intelligence layers applied across 6 sub-domains |

### 1.3 Not Active in V0

Fundamental & Opportunity Intelligence is **deferred to V1+**. The current V0 vertical slice (Alpha Momentum) operates entirely within the Momentum & Market Leadership path. This document defines the domain model for future implementation — no code, no pipeline, no data sources are activated.

---

## 2. The Unified Analytical Framework

### 2.1 Concept: Layers × Domains

Fundamental & Opportunity Intelligence uses a unified analytical framework that combines two dimensions:

- **5 Intelligence Layers** (จาก Close System Product Radar — Phase 7): The analytical *method* — how to think about opportunities across any asset class
- **6 Sub-Domains** (จาก Operating Model §5): The analytical *targets* — what to analyze within the Fundamental path

```
                    LAYERS (How)
         Macro  Policy  Cost    S/D   Hidden
          │       │      │       │       │
    ┌─────┼───────┼──────┼───────┼───────┼─────┐
    │     ▼       ▼      ▼       ▼       ▼     │
    │  Macro Analysis                          │
    │  Industry Analysis                       │  DOMAINS
    │  Product Analysis                        │  (What)
    │  Company Analysis                        │
    │  Earnings & Change Analysis              │
    │  Valuation Context                       │
    └──────────────────────────────────────────┘
```

Each sub-domain draws on the layers most relevant to its analytical purpose. No sub-domain uses all layers equally — some layers are primary, others contextual.

### 2.2 The Five Intelligence Layers

Defined in `CLOSE-SYSTEM-PRODUCT-RADAR.md` §4. Applied here with Fundamental-specific interpretation:

| Layer | Core Question | Applied to Fundamental |
|---|---|---|
| **1. Macro** | What is the economic regime? | Growth/inflation regime, rate cycle, sector rotation, risk appetite |
| **2. Policy** | What are governments doing? | Regulatory risk, antitrust, industry subsidies, tax policy, trade policy |
| **3. Cost Structure** | Where is the price floor? | Unit economics, operating leverage, margin structure, cost advantages |
| **4. Supply/Demand** | Where is the imbalance? | Industry capacity, competitive dynamics, market share shifts, pricing power |
| **5. Hidden Signals** | What hasn't the market priced in? | Insider activity, institutional flows, short interest, earnings revision trends, management behavior |

### 2.3 Layer × Domain Matrix

| Sub-Domain | Macro | Policy | Cost Structure | Supply/Demand | Hidden Signals |
|---|---|---|---|---|---|
| **Macro Analysis** | ● | ● | | | |
| **Industry Analysis** | | ● | ● | ● | ○ |
| **Product Analysis** | ○ | ○ | ● | ● | |
| **Company Analysis** | | | ● | ● | ● |
| **Earnings & Change** | ○ | ● | | | ● |
| **Valuation Context** | ○ | | ○ | ○ | ○ |

● = Primary layer (directly drives analysis)  
○ = Contextual layer (informs but does not drive)

---

## 3. Six Sub-Domains

### 3.1 Macro Analysis

**Purpose:** Identify the macroeconomic regime to determine whether conditions support or threaten the fundamental thesis. Macro analysis frames the opportunity — it does not make the decision.

| Primary Layers | What to Analyze |
|---|---|
| **Macro** | GDP growth trajectory, inflation rate and direction, central bank policy stance, yield curve shape, credit spreads |
| **Policy** | Fiscal policy (spending, deficits), monetary policy (QE/QT), currency regime, capital controls |

**Key Questions:**
- Is the economy expanding, contracting, or transitioning?
- Are real interest rates supportive of equity valuations or creating headwinds?
- Is the credit cycle tightening or loosening — and what does that mean for leveraged companies?
- Which sectors benefit from the current macro regime?

**Output:** Macro regime classification + sector-level implications. This is context for all other sub-domains — not a standalone buy/sell signal.

**Relationship to Close System:** Close System uses Macro to identify commodity cycles and risk appetite. Fundamental uses the same layer to identify growth/value regime and sector rotation. Same data, different question.

---

### 3.2 Industry Analysis

**Purpose:** Evaluate the structural health and competitive dynamics of the industry in which a company operates. A great company in a deteriorating industry faces persistent headwinds.

| Primary Layers | What to Analyze |
|---|---|
| **Supply/Demand** | Industry capacity utilization, new capacity pipeline, demand growth trajectory, substitution threats |
| **Cost Structure** | Industry cost curve, marginal producer economics, fixed vs variable cost composition, barriers to entry |
| **Policy** | Industry-specific regulation, licensing requirements, environmental compliance costs, tariff exposure |

**Key Questions:**
- Is the industry growing, stable, or declining? At what rate? For what structural reason?
- How concentrated is the industry? Are there natural monopolies, fragmented competition, or disruptive entrants?
- Where are the profit pools — which part of the value chain captures the most value?
- What is the industry's position in its cycle — early, mid, late, trough?
- Are there regulatory or technological threats that could reshape the industry within 3-5 years?

**Output:** Industry health assessment + competitive position map + profit pool analysis. Feeds directly into Company Analysis.

**Cross-Layer Example:**
```
Policy: EU Carbon Border Adjustment Mechanism → increases cost for high-emission imports
Cost Structure: Steel industry — marginal producer cost rising $50/ton from carbon tariffs
Supply/Demand: Domestic steel producers gain pricing power vs imports
→ Industry structure shifting in favor of low-carbon domestic producers
```

---

### 3.3 Product Analysis

**Purpose:** Evaluate ETFs, funds, indices, and commodities as investable products — their structure, liquidity, costs, and suitability for different strategies.

This sub-domain directly bridges to **Close System Product Radar** (Phase 7). The same 5-layer framework applies. Fundamental & Opportunity adds the company/earnings lens that Close System does not.

| Primary Layers | What to Analyze |
|---|---|
| **Cost Structure** | Expense ratio, tracking error, bid-ask spread, premium/discount to NAV, tax efficiency |
| **Supply/Demand** | AUM flows, authorized participant activity, creation/redemption mechanics, liquidity |
| **Macro** | (Contextual) Asset class correlation to macro regime — when does this product work? |
| **Policy** | (Contextual) Regulatory treatment, tax status, cross-border accessibility |

**Product types covered:**
- Broad market ETFs (SPY, QQQ, IWM)
- Sector/thematic ETFs (XLF, XLE, GDX)
- Commodity products (GLD, SLV, USO, DBA)
- Fixed income (TLT, TIP, LQD)
- International/EM products (EEM, EFA)

**Overlap with Close System Product Radar:**
Close System scans products for the 3 eligibility criteria (P1-P3). Fundamental Product Analysis provides the deeper analytical layer — the "why" behind Close System's "what." Both use the same 5 layers but at different depth.

---

### 3.4 Company Analysis

**Purpose:** Evaluate individual companies for durable competitive advantage, quality management, sound financial structure, and rational capital allocation. This is the analytical core of the Fundamental path.

| Primary Layers | What to Analyze |
|---|---|
| **Cost Structure** | Gross margins, operating margins, unit economics, fixed vs variable cost composition, operating leverage, cost advantages vs competitors |
| **Supply/Demand** | Market share trajectory, pricing power, customer concentration, supplier dependence, competitive moat durability |
| **Hidden Signals** | Insider buying/selling patterns, institutional ownership changes, management compensation structure, share buyback behavior, related-party transactions |

**Key Questions — Business Model:**
- How does the company make money? Is the unit economics attractive and improving?
- **Moat Classification** — which of the 6 moat types apply? At what strength?

### 3.4.1 Moat Classification System

Every company assessment must classify competitive advantage across 6 moat types, then assess width, depth, and trend.

**Six Moat Types:**

| # | Moat Type | Description | Example |
|---|-----------|-------------|---------|
| 1 | **Share of Mind** | Brand dominance — customer thinks of this brand first in category | Apple, Nike, Coca-Cola |
| 2 | **Network Effect** | Value increases as more users join the network | Visa, Meta, Microsoft (LinkedIn) |
| 3 | **High Switching Cost** | Customer faces material cost/time/risk to switch away | Oracle, SAP, Salesforce |
| 4 | **Cost Advantage** | Sustainably lower cost structure than competitors | Costco, Walmart, TSMC |
| 5 | **Intangible Assets** | Patents, regulatory licenses, proprietary data, IP | ASML, Pfizer, Moody's |
| 6 | **Efficient Scale** | Natural monopoly/oligopoly — market size supports few players | Utilities, Railroads, Airports |

**Moat Width:**

| Width | Criteria |
|---|---|
| **Wide** | Multiple moat types, global coverage, structural advantage |
| **Narrow** | Single moat type, limited scope, contestable |
| **None** | No structural competitive advantage identified |

**Moat Depth:**

| Depth | Criteria |
|---|---|
| **Deep** | 10+ year durability — competitor would need decade+ to breach |
| **Moderate** | 3-10 year durability — defendable but requires continued investment |
| **Shallow** | <3 year durability — easily replicable, temporary advantage |

**Moat Trend:** Stable / Widening / Narrowing

**Moat × Conviction Table:**

| Width | Depth | Conviction Cap |
|---|---|---|
| Wide + Deep | → | Maximum conviction eligible |
| Wide + Moderate/Shallow | → | High conviction cap |
| Narrow + Deep | → | High conviction cap (niche dominance) |
| Narrow + Moderate/Shallow | → | Moderate conviction cap |
| None | → | Requires extraordinary earnings growth to compensate |

**Aggregation:** Companies with multiple moat types score higher — the moats compound. A company with Share of Mind + Switching Cost + Cost Advantage is stronger than one with any single moat type.

**Key Questions — Financial Quality:**
- Is the balance sheet strong enough to survive a downturn without dilution or distress?
- How much debt? At what cost? When does it mature? Fixed or floating?
- Are earnings of high quality (cash-backed, recurring) or low quality (non-recurring, accounting-driven)?
- What is the free cash flow conversion rate? Is FCF growing?

**Key Questions — Capital Allocation:**
- Is management a good steward of capital? Track record on M&A, buybacks, dividends, reinvestment?
- Are buybacks value-accretive (below intrinsic value) or compensation-driven (offsetting dilution)?
- Is M&A disciplined or empire-building? What is the ROIC on past acquisitions?

**Key Questions — Management:**
- Is management competent? Honest? Aligned with shareholders?
- Does management communicate candidly about challenges, or always spin positively?
- Is there excessive turnover in key positions (CFO, auditor, general counsel)?

**Output:** Company quality assessment + moat analysis + financial health score + capital allocation report card. Feeds into Valuation Context.

**Cross-Layer Example:**
```
Cost Structure: Company A gross margin 65% vs industry 45% → pricing power or cost advantage
Supply/Demand: Company A gaining 200bp market share/year for 3 consecutive years
Hidden Signals: CEO purchased $5M of stock on open market last month; no insider selling in 2 years
→ Quality signal converging across 3 independent layers
```

---

### 3.5 Earnings & Change Analysis

**Purpose:** Track earnings releases, guidance changes, and material corporate events. Identify whether new information confirms, weakens, or invalidates the fundamental thesis.

This is the **highest-frequency** sub-domain — it reacts to discrete information events, unlike the structural analysis in Company/Industry which changes slowly.

| Primary Layers | What to Analyze |
|---|---|
| **Hidden Signals** | Earnings surprise magnitude and quality, guidance revision direction and magnitude, analyst estimate dispersion and revision trends, conference call tone/sentiment changes |
| **Policy** | Regulatory filings (8-K, proxy statements, 13-D/G), antitrust developments, patent rulings, FDA decisions |
| **Macro** | (Contextual) Currency impact on multinational earnings, commodity input cost changes, interest expense trajectory |

**Key Questions:**
- Did the company beat, meet, or miss? Was the beat quality (revenue-driven, margin expansion) or cosmetic (share count reduction, one-time items)?
- Did management raise or lower guidance? By how much? What was the stated reason?
- What changed in the narrative — new product announcement, market entry, competitive warning, regulatory update?
- Are analyst revisions converging (consensus forming) or diverging (uncertainty increasing)?
- Does this earnings report confirm, weaken, or invalidate the fundamental thesis?

**Thesis Impact Classification:**

| Impact | Criteria | Action |
|---|---|---|
| **Confirms** | Results align with or exceed thesis expectations; guidance supports trajectory | Maintain thesis; adjust estimates |
| **Weakens** | One or more thesis elements challenged by new data; thesis still intact overall | Flag for review; tighten monitoring |
| **Invalidates** | Core thesis assumption broken by new information | Archive thesis; remove from active consideration |
| **Insufficient** | Not enough new information to change thesis status | Maintain; note what to watch next quarter |

### 3.5.1 Earnings Quality — Explicit Dimension

Every earnings event must be assessed for quality — not just whether the company beat or missed. Quality determines whether the beat/miss is sustainable.

**Quality Rating Scale:**

| Rating | Criteria | Conviction Impact |
|---|---|---|
| **HIGH** | Revenue-driven growth, margin expansion, high FCF conversion (>1.0x EPS), no material one-time items, organic demand driver | Strengthens thesis |
| **MEDIUM** | Mixed sources — some organic growth plus some financial engineering (buybacks, cost-cutting), moderate FCF conversion | Neutral — wait for next quarter |
| **LOW** | Cost-cutting driven, declining revenue, unsustainable margin improvement, low FCF conversion | Weakens thesis |
| **COSMETIC** | Share buybacks masking EPS decline, one-time gains, accounting changes, non-recurring revenue | Red flag — investigate before acting on numbers |

**Quality Assessment Structure (per earnings event):**

```
Earnings Event: AAPL Q3 2024
├── Surprise Direction: BEAT (+4.2%)
├── Surprise Magnitude: +4.2% vs consensus EPS $1.35
├── Quality Rating: HIGH
│   ├── Revenue Quality: HIGH — Services revenue +14% YoY (organic growth driver)
│   ├── Margin Quality: HIGH — Gross margin expanded 180bp (mix shift to services)
│   ├── Cash Conversion: HIGH — FCF/EPS ratio 1.15x (real earnings, not accounting)
│   ├── One-Time Items: NONE — no significant adjustments needed
│   └── Share Count Impact: LOW — buybacks added +0.3% to EPS (minimal)
├── Guidance: Raised FY revenue +$0.5B (organic demand, not cost-cutting)
└── Thesis Impact: CONFIRMS — Services moat widening, margin expansion on track
```

**Integration:** Surprise Direction + Magnitude = quantitative. Quality Rating = qualitative. Thesis Impact = connects earnings event back to fundamental thesis.

**Output:** Earnings event summary + thesis impact assessment + revision tracker. Feeds into Independent Challenge.

---

### 3.6 Valuation Context

**Purpose:** Present valuation data as contextual information — not as a gate, not as a veto. Help the Founder understand what expectations are embedded in the current price.

**Constitutional rule (Operating Model §5.6):** Valuation is contextual information, not the dominant authority and not an automatic veto. The platform shall not automatically reject a candidate merely because conventional valuation appears elevated.

| Contextual Layers | What to Present |
|---|---|
| **Cost Structure** | (Contextual) P/E, EV/EBIT, P/FCF relative to company's own history and margin structure |
| **Supply/Demand** | (Contextual) Valuation percentile vs industry peers, vs sector, vs market |
| **Macro** | (Contextual) Current multiple vs historical average at this point in the rate/cycle regime |
| **Hidden Signals** | (Contextual) Implied growth expectations (reverse DCF) — what growth rate does the current price assume? |

**What Valuation Context Shows:**
- Current multiples (P/E, EV/EBITDA, P/B, P/S, P/FCF) vs 5-year and 10-year history
- Peer comparison — where does this company rank in its industry?
- Implied expectations — what revenue/earnings growth is priced in?
- Yield and cash return (dividend + buyback yield) vs alternatives (bond yields)
- Scenario ranges — what is the valuation under bear/base/bull assumptions?

**What Valuation Context Does NOT Do:**
- ❌ Generate a "buy" or "sell" signal
- ❌ Automatically filter or reject candidates above a threshold
- ❌ Compress multiple valuation dimensions into a single score
- ❌ Override a strong fundamental thesis with a mechanical valuation screen

**Rationale:** The best companies often appear "expensive" on conventional metrics because the market correctly anticipates durable growth. Conversely, cheap companies are often cheap for good reasons (structural decline, poor management, broken business model). Valuation provides context for position sizing (in Capital Command) and conviction calibration — it does not replace business quality analysis.

**Output:** Valuation context dashboard — multiple views, no single conclusion. The Founder interprets.

### 3.6.1 Valuation Priorities (Founder-Ordered)

Valuation is non-dominant and non-veto per Operating Model §5.6. The platform prioritizes:

| Priority | View | Purpose |
|---|---|---|
| 1 | **Cheap vs Own History** | P/E, P/B, EV/EBITDA vs 5Y/10Y average — is the company cheaper than its own past? |
| 2 | **Unusually Cheap Flag** | Alert when valuation falls below -2σ of historical range |
| 3 | Peer comparison | Rank vs industry, sector, market |
| 4 | Implied growth (reverse DCF) | What growth rate does current price assume? |

### 3.6.2 Value Trap Detector

**Trigger:** "Unusually Cheap" flag fires when valuation is below -2σ of own history.

**MANDATORY 5-Question Check (every flagged candidate):**

| # | Question | What to Look For |
|---|---|---|
| Q1 | Earnings still growing? | Revenue + EPS trajectory — flat or declining = red flag |
| Q2 | Industry growing or declining? | Structural decline vs cyclical dip — TAM direction matters |
| Q3 | Moat intact or eroding? | Refer to §3.4.1 Moat Classification — is the moat still there? |
| Q4 | Management credible? | Missed guidance pattern, CEO turnover, broken promises |
| Q5 | Cheap for a GOOD reason? | After Q1-Q4: is the low valuation justified by real problems? |

**Value Trap Scoring:**

| Score | Meaning | Action |
|---|---|---|
| 5/5 Pass | NOT a value trap — genuinely cheap, business intact | 🟢 Add to "Cheap & Quality" watchlist |
| 3-4/5 Pass | Mixed — some concerns but not trap-level | 🟡 Flag for deeper research |
| 1-2/5 Pass | Likely value trap — structural problems masked by low multiple | 🔴 Do not add; document why |
| 0/5 Pass | Definite value trap — cheap for obvious, terminal reasons | 🔴 Archive with trap evidence |

**"Cheap & Quality" Watchlist:** Separate from Momentum watchlist. Tracks companies that are unusually cheap relative to own history AND pass Value Trap detection. Founder may use for opportunistic entry when momentum thesis aligns.

```
Unusually Cheap Flag: INTC P/E 14x vs 5Y avg 22x (-2.1σ)
    ↓
Value Trap Check:
├── Q1: Earnings still growing? → ❌ Revenue -8% YoY, EPS -35%
├── Q2: Industry growing or declining? → ❌ PC TAM flat, x86 share loss to ARM
├── Q3: Moat intact or eroding? → ❌ Process leadership lost to TSMC, Apple defected
├── Q4: Management credible? → ⚠️ 4th CEO in 6 years, missed foundry targets
└── Q5: Cheap for a GOOD reason? → ✅ YES — structural decline, not cyclical dip
    ↓
VERDICT: VALUE TRAP (0/5) — cheap for legitimate reasons. Do NOT add.
```

---

## 4. Independent Challenge — Fundamental Thesis Challenge

### 4.1 Purpose

The platform shall preserve challenge independently from primary analysis. For every fundamental thesis, a dedicated challenge function identifies what could be wrong — contradictory evidence, fragile assumptions, and alternative explanations.

### 4.2 Challenge Domains

| Challenge Domain | What It Looks For |
|---|---|
| **Contradictory Evidence** | Evidence that directly contradicts a thesis element — declining margins while thesis assumes margin expansion |
| **Fragile Assumptions** | Assumptions that carry disproportionate weight — if this one thing is wrong, the whole thesis fails |
| **Accounting Quality** | Aggressive revenue recognition, capitalized expenses that should be operating costs, frequent "one-time" charges, auditor changes |
| **Concentration Risk** | Customer concentration (>25% from one customer), supplier concentration, geographic concentration, product concentration |
| **Cyclicality Mispricing** | Cyclical company priced as if secular grower — peak earnings mistaken for normalized earnings |
| **Management Credibility** | Pattern of missed guidance, overly optimistic language, compensation misaligned with shareholders |
| **Alternative Explanations** | Alternative narrative that fits the same evidence — e.g., growth driven by macro tailwind, not company execution |
| **Balance Sheet Stress** | Refinancing risk, covenant proximity, off-balance-sheet liabilities, pension obligations |

### 4.3 Challenge Rules

- Challenge is **preserved independently** — not integrated into a composite score
- The same evidence may support the thesis AND appear in the challenge — contradiction is visible, not resolved
- A challenge finding does **not** automatically reject — it flags for deeper investigation
- The Founder sees both the thesis AND the challenge — the tension is the product
- Challenge may recommend "more research" or "prevent premature promotion" — but may not independently authorize or reject

---

## 5. Synthesis — Fundamental Research Package

### 5.1 Purpose

The platform shall not compress all evidence into one score. The Fundamental Research Package presents multiple independent views, preserving separation between quality dimensions.

### 5.2 Package Structure

A Fundamental Research Package for a candidate includes:

| Section | Content |
|---|---|
| **Thesis Summary** | Concise narrative — what the opportunity is, why it exists, what must go right |
| **Thesis Lifecycle** | Current status: Proposed → Under Review → Confirmed/Weakened/Invalidated/Waiting |
| **Conviction** | Qualitative: Low / Moderate / High / Maximum — with supporting rationale |
| **Macro Context** | Regime classification, relevant macro signals, sector implications |
| **Industry Assessment** | Structure, competitive dynamics, profit pools, cycle position |
| **Company Assessment** | Moat, unit economics, financial quality, capital allocation, management |
| **Earnings Trajectory** | Recent results, guidance, revision trends, thesis impact |
| **Valuation Context** | Multiple views, peer comparison, implied expectations |
| **Key Risks** | Thesis-specific risks with falsifiable conditions |
| **Independent Challenge** | Contradictions, fragile assumptions, alternative explanations |
| **Supporting Evidence** | Evidence references with provenance |
| **Contradicting Evidence** | Evidence that challenges the thesis — visible, not hidden |
| **Open Questions** | What remains unknown; what the next information event should answer |

### 5.3 Presentation Rules

- Each section is independently visible — the Founder can read any section without reading others
- No weighted sum, composite score, or single ranking
- Quality, Valuation, Conviction, and Data Confidence remain separate axes
- Evidence references link to source records with provenance
- The Founder sees both thesis and challenge — the tension is the value

---

## 6. Founder Decision Gate

### 6.1 Fundamental Candidate Decisions

Within the Fundamental & Opportunity path, the Founder may:

| Decision | Description |
|---|---|
| **Reject** | Thesis does not hold up; candidate removed from active consideration; history preserved |
| **Watch** | Thesis is plausible but evidence insufficient; monitor for confirming/disconfirming events |
| **Research Further** | Thesis shows promise but gaps exist; direct deeper analysis on specific areas |
| **Approve Fundamental Candidate** | Thesis approved; candidate enters Fundamental Watchlist; eligible for Capital Command consideration |

**Critical distinction:** "Approve Fundamental Candidate" means the platform's intelligence work supports further consideration. It does **not** authorize capital allocation, position sizing, or execution. Those decisions belong to Capital Command and the Founder outside this platform.

### 6.2 Separated from Momentum Decisions

A candidate may be:
- Fundamentally Approved but not Momentum Ready
- Momentum Ready but not Fundamentally Approved
- Both
- Neither

The platform preserves these as independent states. There is no forced reconciliation.

---

## 7. Relationship to Other Strategies

### 7.1 vs Alpha Momentum (Momentum & Market Leadership)

| Dimension | Fundamental & Opportunity | Alpha Momentum |
|---|---|---|
| **Question** | What is built to last? | What is working now? |
| **Time Horizon** | Years | Weeks to months |
| **Primary Lens** | Business quality, moat, earnings | Price structure, RS, theme momentum |
| **Valuation Role** | Context (non-dominant) | Not directly assessed |
| **Entry Signal** | Quality at reasonable price | Stage 2 breakout |
| **Challenge Focus** | Accounting, management, moat fragility | Late-stage risk, weak volume, adverse regime |
| **Output** | Fundamental Research Package | Theme-first Research Queue |

### 7.2 vs Close System Product Radar

Both share the **5 Intelligence Layers** framework. The difference is analytical depth and product scope:

| Dimension | Fundamental & Opportunity | Close System Product Radar |
|---|---|---|
| **Product Universe** | Individual companies + ETFs/Commodities | ETFs, Commodities, Indices only |
| **Depth** | Deep — Company, Earnings, Management | Broad — Macro, Policy, Cost, S/D scanning |
| **Layers** | Same 5 layers, applied differently | Same 5 layers, commodity-focused |
| **Company Analysis** | Yes — core analytical pillar | No — individual companies excluded by P1 |
| **Output** | Deep research package per candidate | Radar scan — which products meet P1-P3 |

They complement: Close System scans broadly for discounted products; Fundamental goes deep on specific companies. A Close System finding (e.g., "rare earth ETF at discount") could trigger Fundamental deep research on the top holdings of that ETF.

---

## 8. Relationship to Shared Intelligence Core

Fundamental & Opportunity Intelligence **consumes** from Shared Core:

| Shared Core Module | Use in Fundamental Path |
|---|---|
| **Source Registry** | Register company filings, earnings data, industry reports, macro data sources |
| **Raw Evidence Preservation** | Immutable storage of 10-K/Q, transcripts, guidance, insider filings |
| **Evidence Model** | Link all fundamental evidence (earnings data, management commentary, industry reports) to candidates and theses |
| **Entity & Asset Identity** | Canonical company identity across exchanges, share classes, corporate actions |
| **Data Quality & Freshness** | Track staleness of financial data, flag restatements, monitor filing delays |
| **Feature Computation** | Run deterministic financial calculations (FCF yield, ROIC, margin trends) — versioned and reproducible |
| **Audit History** | Record all thesis transitions, challenge findings, and Founder decisions |

---

## 9. Version Boundaries

| Capability | V0 | V1 | V1.5 | Later |
|---|---|---|---|---|
| Domain model + sub-domain definitions | — | ✅ | ✅ | ✅ |
| Layer × Domain matrix | — | ✅ | ✅ | ✅ |
| Independent Challenge specification | — | ✅ | ✅ | ✅ |
| Synthesis Package specification | — | ✅ | ✅ | ✅ |
| Macro Analysis — synthetic fixtures | — | ✅ | ✅ | ✅ |
| Industry Analysis — synthetic fixtures | — | ✅ | ✅ | ✅ |
| Company Analysis — synthetic fixtures | — | ✅ | ✅ | ✅ |
| Earnings & Change — synthetic events | — | ✅ | ✅ | ✅ |
| Valuation Context dashboard | — | ✅ | ✅ | ✅ |
| Real data — filings, transcripts, estimates | — | — | ✅ | ✅ |
| Automated challenge detection | — | — | — | ✅ |
| Fundamental + Momentum dual-view display | — | — | ✅ | ✅ |
| Integration with Capital Command | — | — | — | ✅ |

**Note:** V0 does not include any Fundamental & Opportunity capabilities. The path is defined for future implementation. The 5 Intelligence Layers framework, however, is available immediately — it was built in Phase 7 and applies across all strategies.

---

## 10. Constitutional Compliance

| Constitutional Requirement | How Fundamental & Opportunity Complies |
|---|---|
| §1 — Reduce search space | Narrows universe to candidates with durable quality + structural opportunity |
| §2 — Part of Strategy Control Center | Peer strategy to Alpha Momentum and Close System |
| §5 — Theme Intelligence optional | May consume theme data but does not require it for core analysis |
| §10 — Keep dimensions separate | Quality, Valuation, Conviction, Data Confidence are independent axes |
| §13 — Preserve evidence | All sub-domain assessments reference specific evidence with provenance |
| §23 — AI Intelligence Layer | AI assists with layer × domain synthesis; Founder makes final determination |
| §23.8.1 — Blind Portfolio | Fundamental analysis operates portfolio-blind — scans the universe, not holdings |
| Operating Model §5.6 — Valuation non-dominant | Valuation Context presents data, does not veto or gate |
| No broker/execution/allocation | Output is a Research Package — what merits investigation, not what to trade |
| Independent Challenge preserved | Challenge findings are visible alongside thesis — not averaged away |
