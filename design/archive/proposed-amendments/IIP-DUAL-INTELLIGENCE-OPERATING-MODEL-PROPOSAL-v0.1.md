# Investment Intelligence Platform
## Proposed Project Definition Amendment — Dual Intelligence Operating Model

**Status:** Proposed — Non-authoritative until explicit Founder approval  
**Proposal ID:** `IIP-DUAL-INTELLIGENCE-OPERATING-MODEL-v0.1`  
**Change class:** Material Project Definition amendment  
**Primary target:** `project-definition/INVESTMENT-INTELLIGENCE-OPERATING-MODEL.md`  
**Related constitutional proposal:** `proposed-amendments/AI-OPERATING-CONSTITUTION-v0.1.md`  
**Implementation authority:** None  
**Technology authority:** None

---

# 1. Purpose

Define the long-term logical operating model of the Investment Intelligence Platform without selecting a technology stack, agent framework, model provider, data vendor, final rule pack, scoring calibration, or implementation architecture.

The model establishes two equal investment-intelligence paths:

1. **Fundamental & Opportunity Intelligence**
2. **Momentum & Market Leadership Intelligence**

Both paths share evidence, validation, deterministic computation, provenance, review, and Founder authorization.

This document does not place Capital Command or Trading / Execution Systems inside the Investment Intelligence Platform. Those systems are external consumers behind a formal integration boundary.

---

# 2. Product Boundary

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

Potential downstream systems, including Capital Command and Trading / Execution Systems, remain outside this project.

---

# 3. Target Logical Operating Model

```text
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
│   ├── Fundamental & Opportunity Intelligence
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
│   ├── Fundamental Thesis Challenge
│   └── Momentum Setup Challenge
│
├── Synthesis & Decision Support
│   ├── Fundamental Research Package
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
    ├── Approve Fundamental Candidate
    └── Approve Momentum Candidate

--------------- External Integration Boundary ---------------

Founder-authorized intelligence package
    ├── Capital Command
    └── Trading / Execution Systems
```

The labels above define logical responsibilities. They do not require one deployed AI agent per label.

---

# 4. Shared Intelligence Core

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

---

# 5. Fundamental & Opportunity Intelligence

This path evaluates business quality, structural opportunity, evidence, and change.

## 5.1 Macro Analysis

May interpret growth, inflation, liquidity, policy, rates, credit, currencies, and regime context.

## 5.2 Industry Analysis

May analyze industry structure, supply and demand, regulation, competitive intensity, cycle position, and profit pools.

## 5.3 Product Analysis

May analyze ETFs, funds, indices, commodities, and other instruments, including structure, liquidity, fees, tracking, premium/discount, and suitability.

## 5.4 Company Analysis

May analyze business model, moat, management, unit economics, financial quality, balance sheet, capital allocation, and competitive position.

## 5.5 Earnings & Change Analysis

May analyze releases, filings, transcripts, guidance, estimate changes, management communication, and thesis-impacting change.

## 5.6 Valuation Context

Valuation is contextual information, not the dominant authority and not an automatic veto.

The function may present:

- current and historical multiples;
- peer comparisons;
- yields;
- valuation percentiles;
- implied expectations;
- transparent scenario assumptions.

It shall not automatically reject a candidate merely because conventional valuation appears elevated.

Final weighting and interpretation rules remain deferred to the applicable approved strategy rule pack.

---

# 6. Momentum & Market Leadership Intelligence

This path evaluates where market leadership is developing and whether a candidate is becoming actionable for Founder review.

The future rule framework may draw inspiration from O'Neil, Minervini, and other approved momentum sources. Exact rules, formulas, windows, weights, thresholds, pattern definitions, and references remain deferred until explicitly approved.

## 6.1 Market Regime

Assesses broad market conditions, index behavior, distribution pressure, volatility environment, and participation.

## 6.2 Breadth & Leadership

Assesses sector, industry, theme, and stock leadership; new-high participation; concentration; and rotation.

## 6.3 Fundamental Momentum

Assesses earnings and sales growth, acceleration, surprises, revisions, margin change, and catalyst support.

## 6.4 Relative Strength

Assesses performance versus market, sector, industry, and relevant cohorts, subject to approved point-in-time and reference-cohort contracts.

## 6.5 Price–Volume Structure

Assesses trend, accumulation/distribution, tightness, contraction, moving-average context, and support behavior.

## 6.6 Setup / Base Structure

Assesses candidate setup structure using reproducible features and approved interpretation rules. AI pattern recognition may assist but shall not be the sole authoritative detector.

## 6.7 Breakout Readiness

Assesses readiness state, event risk, liquidity, extension, overhead supply, and invalidation context. It does not create an order.

## 6.8 Momentum Watchlist Lifecycle

The watchlist lifecycle shall be a versioned, auditable state model. AI may propose a transition; approved rules and required human gates determine authoritative state.

Possible conceptual states include:

- Discovered
- Qualified
- Watchlist
- Setup Forming
- Ready for Review
- Trigger Observed
- Extended
- Failed
- Invalidated
- Archived

These labels are proposals until separately approved in strategy design.

---

# 7. Independent Challenge

The platform shall preserve challenge independently from primary analysis.

## 7.1 Fundamental Thesis Challenge

May identify contradictory evidence, fragile assumptions, accounting or quality concerns, concentration, cyclicality, management risk, and alternative explanations.

## 7.2 Momentum Setup Challenge

May identify late-stage setup risk, weak volume confirmation, adverse market regime, deteriorating relative strength, event risk, repeated failure, crowding, overhead supply, and slowing fundamental momentum.

A challenge function may recommend more research or prevent premature promotion where approved governance rules permit. It may not independently authorize or reject an investment.

---

# 8. Synthesis and Decision Support

The platform shall not compress all evidence into one unexplained score.

It shall preserve separate views for:

- Fundamental Research
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

---

# 9. Founder Decision Gate

AI proposes. The Founder authorizes material investment-intelligence states.

Research approval, investment approval, allocation approval, and execution approval are different concepts.

Within this platform, Founder decisions may include:

- Reject
- Watch
- Research Further
- Approve Theme
- Approve Fundamental Candidate
- Approve Momentum Candidate

Approval inside the platform does not authorize capital allocation or execution.

---

# 10. Specialized Agents and Subagents

The logical responsibilities in this model may later be implemented using:

- one general AI capability;
- one orchestrator with tools;
- several specialized agents;
- deterministic services plus AI interpretation;
- different models for different tasks.

No logical role requires a separate deployed agent by default.

A specialized agent may be created only when at least one of the following is true:

- it requires materially different evidence;
- it requires a materially different reasoning framework;
- it requires different permissions or data boundaries;
- it can be evaluated independently;
- it has a clear input/output contract;
- parallel execution provides real value;
- model specialization or routing produces justified quality or cost benefits.

Every material agent shall define:

- purpose;
- authority boundary;
- permitted evidence;
- prohibited actions;
- input contract;
- output contract;
- deterministic dependencies;
- provenance;
- validation;
- failure behavior;
- escalation;
- review or approval requirements.

Delegation from one AI agent does not create additional authority.

---

# 11. Version Boundaries

## Current Alpha Momentum V0 Design

The current V0 work should remain narrow:

- Shared Intelligence Core contracts;
- deterministic features and data-confidence contracts;
- one logical Momentum Intelligence workflow;
- independent challenge;
- Founder-reviewable output;
- synthetic fixtures and Founder-approved fixed historical public snapshots;
- no live production data;
- no AI-driven theme discovery;
- no broker, allocation, or execution functions.

V0 does not need the complete long-term multi-agent organization.

## V1 and Later

Later phases may add:

- real EOD data;
- automated monitoring;
- specialized momentum capabilities;
- Fundamental & Opportunity Intelligence workbench;
- AI-assisted theme discovery;
- richer challenge and synthesis;
- provider/model routing;
- continuous intelligence.

Each addition remains subject to material-change, design, security, evidence, and approval controls.

---

# 12. Required Document Synchronization

Subject to approval, synchronize:

1. `project-definition/README.md`
   - index this operating model.

2. `project-definition/DOMAIN-ARCHITECTURE.md`
   - show the two intelligence paths;
   - show Shared Intelligence Core;
   - show Independent Challenge, Synthesis, and Founder Decision Gate;
   - place Capital Command and Trading / Execution beyond the external boundary.

3. `project-definition/ALPHA-MOMENTUM-V0-SPEC.md`
   - map V0 to the Momentum & Market Leadership path;
   - clarify that V0 does not require all long-term specialized agents;
   - preserve deferred exact O'Neil/Minervini rule packs.

4. `operational/FOUNDERS-DECISIONS.md`
   - record approval of the dual-intelligence target model;
   - record Valuation Context as non-dominant and non-veto by default;
   - record external-system boundaries.

5. `operational/DOMAIN-GLOSSARY.md`
   - define logical role, agent, deterministic service, Research Orchestrator, Shared Intelligence Core, challenge, decision package, and external handoff.

6. `operational/SCOPE-AND-NON-SCOPE.md`
   - state that Capital Command and Trading / Execution are external.

7. `operational/ROADMAP.md`
   - preserve the current Alpha Momentum V0 phase;
   - add future sequencing without falsely marking future work active.

8. `operational/DEFERRED-DECISIONS.md`
   - retain exact agent topology, orchestration framework, models, data vendors, O'Neil/Minervini rule packs, formulas, weights, thresholds, and final workflow calibrations as deferred.

9. `proposed-amendments/AI-OPERATING-CONSTITUTION-v0.1.md`
   - add only a technology-neutral specialized-agent delegation principle;
   - do not place the detailed logical organization in the Constitution.

---

# 13. Acceptance Conditions

The amendment is acceptable only if:

- no technology stack is selected;
- no application code is written;
- no exact investment rule is invented;
- no score, threshold, period, weight, or benchmark is silently selected;
- no Capital Command or execution behavior is introduced;
- V0 remains a narrow Alpha Momentum vertical slice;
- Founder authority remains explicit;
- deterministic and AI responsibilities remain separated;
- evidence, provenance, uncertainty, and dissent remain visible;
- the exact file diff is independently reviewed before approval.
