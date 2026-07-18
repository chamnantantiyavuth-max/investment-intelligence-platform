# Investment Intelligence Platform Constitution

## Version 0.1 — Approved Working Constitution

### Status

Approved by the Founder as the working constitutional baseline.

This document is not a final product specification or final architecture. It defines the product's mission, authority model, core boundaries, and principles that downstream specifications must respect.

## 1. Mission

The Investment Intelligence Platform exists to reduce the global investment search space while preserving evidence, uncertainty, disagreement, and decision history.

It helps answer:

> What deserves further investigation?

It does not autonomously answer:

> What should be bought, sold, or allocated?

## 2. Product Structure

The primary entry point is the Strategy Control Center, leading to:

1. Alpha Momentum
2. Close System
3. Future strategy modules

A Shared Intelligence Core supports all strategies.

## 3. Development Direction

Alpha Momentum is the first implementation vertical slice.

The shared core must remain strategy-independent enough to support Close System later without forcing a rewrite, while avoiding premature abstractions for hypothetical future needs.

## 4. Shared Intelligence Core

Conceptual responsibilities include:

- source registry;
- raw evidence preservation;
- entity and asset identity;
- data normalization;
- freshness, quality, conflicts, and revisions;
- feature computation;
- Theme Intelligence;
- evidence relationships;
- human feedback;
- audit history;
- knowledge export.

## 5. Theme Intelligence

Theme Intelligence is a first-class shared capability.

It supports:

- top-down discovery;
- bottom-up discovery;
- event-driven discovery;
- change-driven discovery;
- discovery of new themes;
- lifecycle tracking of existing themes.

Initial lifecycle:

1. Weak Signal
2. Formation
3. Emerging Leadership
4. Expansion
5. Crowded / Late Stage
6. Deterioration

Lifecycle, confidence, and governance status are separate dimensions.

Governance states may include:

- Detected Hypothesis
- Experimental
- Under Human Review
- Approved
- Actively Tracked
- Dormant
- Rejected
- Archived

## 6. Two-Tier Autonomy

AI may create and monitor Experimental Themes.

Experimental Themes may accumulate evidence, map assets, track breadth, identify leaders, and request human review.

They may not affect official strategy rankings until approved by the Founder.

## 7. Weak Signal Inbox

The inbox has two layers:

### Unexplained Anomalies

The system has detected meaningful change but lacks a credible explanation.

### Theme Hypotheses

The system can propose a driver, related entities, and a preliminary evidence structure.

The system must not invent explanations merely to eliminate uncertainty.

## 8. Evidence Doctrine

The system distinguishes:

- raw source records;
- observed facts;
- claims;
- normalized facts;
- derived metrics;
- statistical signals;
- AI extractions;
- AI classifications;
- hypotheses;
- human judgments;
- approved decisions;
- outcomes;
- lessons.

Multiple links copied from one source are not independent evidence.

Evidence relevance may decay. Raw evidence and history are not silently deleted.

Narrative, plans, and intentions require independent corroboration or observable action before gaining material influence.

Unsupported narrative or intention-based evidence that has no measurable action within three years is stale by default, unless a documented long-cycle exception and milestones are approved.

## 9. Evidence Progression

No evidence type dominates universally.

Typical progression may include:

Structural Signal  
→ Operational Action  
→ Fundamental Confirmation  
→ Market Confirmation  
→ Broad Adoption / Crowding

Different themes may follow different valid progressions.

## 10. Information Preservation

The platform must keep separate:

- Theme Quality;
- Candidate Quality;
- Entry Readiness;
- Data Confidence;
- lifecycle;
- confidence;
- supporting evidence;
- contradicting evidence;
- missing evidence;
- crowding;
- alternative explanations.

Important trade-offs must not disappear into one opaque score.

## 11. Falsification

Every material hypothesis must include:

- supporting evidence;
- contradicting evidence;
- missing evidence;
- alternative explanations;
- confirmation milestones;
- invalidation conditions;
- what would change our mind;
- current confidence.

Observed contradictions, plausible alternatives, and generic risks must remain distinct.

The system must not fabricate weak opposition merely to appear balanced.

## 12. Human Authority

The Founder has final authority.

A Human Override must preserve:

- system assessment;
- machine dissent;
- unresolved counter-evidence;
- Founder rationale;
- required confirmation;
- reassessment point;
- eventual outcome.

## 13. Alpha Momentum

Alpha Momentum screens US-listed common stocks and suitable ADRs in V0 while receiving global Theme Intelligence.

It separates:

### Candidate Quality

Fundamentals, growth, liquidity, relative strength, trend quality, accumulation, industry leadership, and other approved rule-pack dimensions.

### Theme Quality

Lifecycle, breadth, leadership, evidence progression, market confirmation, fundamental confirmation, crowding, and confidence.

### Entry Readiness

Price structure, base quality, breakout proximity, volume behavior, volatility contraction, and extension risk.

### Data Confidence

Freshness, completeness, reliability, conflicts, and missing data.

Within a theme, candidates may be classified as:

- Confirmed Leader
- Emerging Challenger
- Direct Beneficiary
- Enabler
- Bottleneck Owner
- Second-order Beneficiary
- Watchlist Member
- Former Leader
- Deteriorating Member

## 14. Theme-First Research Queue

The research queue is organized by Theme Card before individual stock ranking.

Queue capacity is adaptive. It must not fill a quota with weak candidates.

It may return zero high-priority candidates.

## 15. Close System

Close System is the second strategy world.

Future design must distinguish:

- Asset Suitability
- Current Opportunity
- Macro Regime
- Instrument Structure
- Capital Lock-up Risk
- Structural Decay
- Liquidity
- Operational Complexity
- Data Confidence

The absence of a stop loss does not eliminate opportunity cost, capital lock-up, correlated driver exposure, structural decay, or recovery-duration risk.

## 16. Learning Loop

Evidence  
→ Hypothesis  
→ Theme  
→ Candidate  
→ Research  
→ Human Decision  
→ Outcome  
→ Postmortem  
→ Lesson Draft  
→ Human Approval  
→ Approved Knowledge  
→ Versioned Rule, Skill, or Playbook Proposal

AI-generated lessons do not change official behavior automatically.

## 17. Knowledge Architecture

The application is the structured source of truth for evidence, states, lineage, decisions, overrides, outcomes, lessons, and rule versions.

Obsidian and NotebookLM are narrative learning layers for case studies, postmortems, approved lessons, patterns, anti-patterns, and playbooks.

## 18. Initial Non-Scope

- broker connectivity;
- order execution;
- automated allocation;
- autonomous buy or sell recommendations;
- real-time high-frequency infrastructure;
- full global equity screening in V0;
- automatic rule modification;
- final technology or data-vendor selection;
- graph-database requirement;
- production-scale autonomous global scanning in V0.

## 19. Architecture Principles

- modular monolith first;
- immutable raw evidence;
- versioned material transformations;
- point-in-time correctness;
- reproducibility;
- explainability;
- replaceable AI components;
- vertical slices;
- no premature graph database;
- no premature distributed architecture.

## 20. V0 Thesis

V0 proves an end-to-end Alpha Momentum slice using controlled data and predefined themes.

It must demonstrate:

- evidence lineage;
- deterministic features;
- separated candidate, theme, entry, and data-confidence dimensions;
- Theme Cards;
- research queue;
- human feedback;
- reproducibility;
- historical state changes.

## 21. Amendment Authority

The Constitution may be amended only through an explicit proposal that states:

- affected Founder Decision;
- reason;
- trade-offs;
- downstream impact;
- Founder approval;
- amendment history.

## 22. Closing Principle

Preserve evidence.  
Preserve uncertainty.  
Preserve dissent.  
Make hypotheses falsifiable.  
Let machines discover and organize.  
Let humans approve and decide.  
Learn from every important outcome without rewriting history.
