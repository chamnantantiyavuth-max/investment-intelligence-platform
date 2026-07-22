# Investment Intelligence Operating Model

**Status:** Approved Project Definition
**Version:** 0.1
**Owner:** Founder
**Authority:** Approved Project Definition subordinate to the Constitution and Founder's Decisions
**Derived from:** Investment Intelligence Platform Constitution v0.4, Founder Decisions #1-24
**Approval:** PD-v0.1-DUAL-INTELLIGENCE-OPERATING-MODEL (Founder Decision #24, 22 July 2026)

## 1. Purpose

Define the long-term logical operating model of the Investment Intelligence Platform without selecting a technology stack, agent framework, model provider, data vendor, final rule pack, scoring calibration, or implementation architecture.

The model establishes two equal investment-intelligence paths:

1. **Fundamental & Opportunity Intelligence** (V1+ future path)
2. **Momentum & Market Leadership Intelligence** (Alpha Momentum V0 active path)

Both paths share evidence, validation, deterministic computation, provenance, review, and Founder authorization.

This document does not place Capital Command or Trading / Execution Systems inside the Investment Intelligence Platform. Those systems are external consumers behind a formal integration boundary.

## 2. Product Boundary

The Investment Intelligence Platform is responsible for:

- discovering and structuring investment opportunities;
- acquiring and validating evidence;
- computing reproducible analytical features;
- analyzing themes, industries, products, companies, earnings, market leadership, and momentum conditions;
- challenging hypotheses and setups;
- synthesizing decision-support packages;
- recording Founder review and authorization state.

The platform is not responsible for:

- capital allocation;
- portfolio truth;
- portfolio reconciliation;
- order creation;
- order routing;
- broker execution;
- trade management;
- cash or margin control.

Downstream systems — Capital Command and Trading / Execution Systems — remain outside this project.

## 3. Target Logical Operating Model

```
FOUNDER
Final Investment Intelligence Authority
│
├── Investment Constitution
│
├── Research Orchestrator
│   │
│   ├── Shared Intelligence Core
│   │   ├── Evidence Acquisition
│   │   ├── Data Validation
│   │   ├── Deterministic Quant Engine
│   │   ├── Market Data Interface
│   │   ├── Evidence Store
│   │   └── Knowledge, Provenance & Version Control
│   │
│   ├── Fundamental & Opportunity Intelligence (V1+)
│   │   ├── Macro Analysis
│   │   ├── Industry Analysis
│   │   ├── Product Analysis
│   │   ├── Company Analysis
│   │   ├── Earnings & Change Analysis
│   │   └── Valuation Context
│   │
│   └── Momentum & Market Leadership Intelligence
│       ├── Market Regime
│       ├── Breadth & Leadership
│       ├── Fundamental Momentum
│       ├── Relative Strength
│       ├── Price–Volume Structure
│       ├── Setup / Base Structure
│       ├── Breakout Readiness
│       └── Momentum Watchlist Lifecycle
│
├── Independent Challenge
│   ├── Fundamental Thesis Challenge (V1+)
│   └── Momentum Setup Challenge
│
├── Synthesis & Decision Support
│   ├── Fundamental Research Package (V1+)
│   ├── Momentum Candidate Package
│   ├── Conflicting Evidence
│   ├── Unresolved Questions
│   └── Founder Action Options
│
└── Founder Decision Gate
    ├── Reject
    ├── Watch
    ├── Research Further
    ├── Approve Theme
    ├── Approve Fundamental Candidate (V1+)
    └── Approve Momentum Candidate

--------------- External Integration Boundary ---------------

Founder-authorized intelligence package
    ├── Capital Command
    └── Trading / Execution Systems
```

The labels above define logical responsibilities. They do not require one deployed AI agent per label.

## 4. Shared Intelligence Core

The Shared Intelligence Core is a shared platform area composed of bounded capabilities, not a single God Context.

It is authoritative for:

- source identity and source records;
- evidence provenance;
- point-in-time availability;
- data normalization and validation;
- versioned deterministic feature computation;
- missingness and conflict preservation;
- evidence and output lineage;
- audit and review history.

Strategy domains own the meaning and use of their strategy-specific features, eligibility, ranking, readiness, and prioritization rules.

AI may explain and interpret deterministic features. AI shall not silently replace their values.

## 5. Fundamental & Opportunity Intelligence (V1+)

This path evaluates business quality, structural opportunity, evidence, and change. **Implementation is deferred to V1+**. The Alpha Momentum V0 vertical slice does not require this path.

### 5.1 Macro Analysis

May interpret growth, inflation, liquidity, policy, rates, credit, currencies, and regime context.

### 5.2 Industry Analysis

May analyze industry structure, supply and demand, regulation, competitive intensity, cycle position, and profit pools.

### 5.3 Product Analysis

May analyze ETFs, funds, indices, commodities, and other instruments, including structure, liquidity, fees, tracking, premium/discount, and suitability.

### 5.4 Company Analysis

May analyze business model, moat, management, unit economics, financial quality, balance sheet, capital allocation, and competitive position.

### 5.5 Earnings & Change Analysis

May analyze releases, filings, transcripts, guidance, estimate changes, management communication, and thesis-impacting change.

### 5.6 Valuation Context

Valuation is contextual information, not the dominant authority and not an automatic veto. The function may present current and historical multiples, peer comparisons, yields, valuation percentiles, implied expectations, and transparent scenario assumptions. It shall not automatically reject a candidate merely because conventional valuation appears elevated.

Final weighting and interpretation rules remain deferred to the applicable approved strategy rule pack.

## 6. Momentum & Market Leadership Intelligence

This path evaluates where market leadership is developing and whether a candidate is becoming actionable for Founder review. It is the active path in Alpha Momentum V0.

The future rule framework may draw inspiration from O'Neil, Minervini, and other approved momentum sources. Exact rules, formulas, windows, weights, thresholds, pattern definitions, and references remain deferred until explicitly approved.

### 6.1 Market Regime

Assesses broad market conditions, index behavior, distribution pressure, volatility environment, and participation.

### 6.2 Breadth & Leadership

Assesses sector, industry, theme, and stock leadership; new-high participation; concentration; and rotation.

### 6.3 Fundamental Momentum

Assesses earnings and sales growth, acceleration, surprises, revisions, margin change, and catalyst support.

### 6.4 Relative Strength

Assesses performance versus market, sector, industry, and relevant cohorts, subject to approved point-in-time and reference-cohort contracts.

### 6.5 Price–Volume Structure

Assesses trend, accumulation/distribution, tightness, contraction, moving-average context, and support behavior.

### 6.6 Setup / Base Structure

Assesses candidate setup structure using reproducible features and approved interpretation rules. AI pattern recognition may assist but shall not be the sole authoritative detector.

### 6.7 Breakout Readiness

Assesses readiness state, event risk, liquidity, extension, overhead supply, and invalidation context. It does not create an order.

### 6.8 Momentum Watchlist Lifecycle

The watchlist lifecycle shall be a versioned, auditable state model. AI may propose a transition; approved rules and required human gates determine authoritative state.

Conceptual states include: Discovered, Qualified, Watchlist, Setup Forming, Ready for Review, Trigger Observed, Extended, Failed, Invalidated, Archived. These labels are proposals until separately approved in strategy design.

## 7. Independent Challenge

The platform shall preserve challenge independently from primary analysis.

### 7.1 Fundamental Thesis Challenge (V1+)

May identify contradictory evidence, fragile assumptions, accounting or quality concerns, concentration, cyclicality, management risk, and alternative explanations.

### 7.2 Momentum Setup Challenge

May identify late-stage setup risk, weak volume confirmation, adverse market regime, deteriorating relative strength, event risk, repeated failure, crowding, overhead supply, and slowing fundamental momentum.

A challenge function may recommend more research or prevent premature promotion where approved governance rules permit. It may not independently authorize or reject an investment.

## 8. Synthesis and Decision Support

The platform shall not compress all evidence into one unexplained score.

It shall preserve separate views for:

- Fundamental Research (V1+)
- Momentum Readiness
- Theme Quality
- Candidate Quality
- Entry Readiness
- Data Confidence
- Supporting Evidence
- Contradicting Evidence
- Assumptions
- Unresolved Questions
- Invalidation Conditions

A candidate may be fundamentally strong but not momentum-ready, or momentum-ready with only moderate long-term quality. The platform shall make this distinction visible.

## 9. Founder Decision Gate

AI proposes. The Founder authorizes material investment-intelligence states.

Research approval, investment approval, allocation approval, and execution approval are different concepts.

Within this platform, Founder decisions may include: Reject, Watch, Research Further, Approve Theme, Approve Fundamental Candidate (V1+), and Approve Momentum Candidate.

Approval inside the platform does not authorize capital allocation or execution.

## 10. Specialized Agents and Subagents

The logical responsibilities in this model may later be implemented using one general AI capability, one orchestrator with tools, several specialized agents, deterministic services plus AI interpretation, or different models for different tasks. No logical role requires a separate deployed agent by default.

A specialized agent may be created only when at least one of the following is true: it requires materially different evidence, a materially different reasoning framework, different permissions or data boundaries, independent evaluation, a clear input/output contract, parallel execution value, or model specialization producing justified quality or cost benefits.

Every material agent shall define: purpose, authority boundary, permitted evidence, prohibited actions, input contract, output contract, deterministic dependencies, provenance, validation, failure behavior, escalation, and review or approval requirements.

Delegation from one AI agent does not create additional authority.

## 11. Version Boundaries

### Current Alpha Momentum V0

The current V0 work remains narrow: Shared Intelligence Core contracts, deterministic features and data-confidence contracts, one logical Momentum Intelligence workflow, independent challenge, Founder-reviewable output, synthetic fixtures, and Founder-approved fixed historical public snapshots. No live production data. No AI-driven theme discovery. No broker, allocation, or execution functions.

V0 does not need the complete long-term multi-agent organization.

### V1 and Later

Later phases may add: real EOD data, automated monitoring, specialized momentum capabilities, Fundamental & Opportunity Intelligence workbench, AI-assisted theme discovery, richer challenge and synthesis, provider/model routing, and continuous intelligence. Each addition remains subject to material-change, design, security, evidence, and approval controls.

## 12. Required Document Synchronization

Synchronized documents (applied concurrently with this amendment):

1. `project-definition/README.md` — index this operating model
2. `project-definition/DOMAIN-ARCHITECTURE.md` — show dual intelligence paths
3. `project-definition/ALPHA-MOMENTUM-V0-SPEC.md` — map V0 to Momentum path only
4. `operational/FOUNDERS-DECISIONS.md` — record FD #23 and #24
5. `operational/SCOPE-AND-NON-SCOPE.md` — state Capital Command external
6. `operational/DOMAIN-GLOSSARY.md` — add operating model terms
7. `operational/ROADMAP.md` — add future Fundamental path sequencing
8. `operational/DEFERRED-DECISIONS.md` — verify deferred items correct
