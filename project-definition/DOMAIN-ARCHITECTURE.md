# Domain Architecture

Status: Approved Domain Specification
Version: 0.1
Owner: Founder
Authority: Approved Domain Specification subordinate to the Constitution and Founder's Decisions
Derived from: Investment Intelligence Platform Constitution v0.3
Approval: PD-v0.1-FOUNDING-DOMAIN-SPECIFICATIONS

## 1. Bounded Contexts

The platform is organized into bounded contexts. Each owns its domain logic, state, and rules.

The Shared Intelligence Core is **not one monolithic God context**. It is a shared platform area composed of bounded modules, each with clear ownership boundaries and promotion criteria.

### 1.1 Shared Intelligence Core

The Shared Core is a shared platform area composed of bounded modules. Each module has clear ownership and promotion criteria.

**Ownership rule:** A module belongs to Shared Core only when it is universally required or explicitly assigned by the Constitution.

**Shared Core modules:**

| Module | Constitutional Basis | Responsibility |
|---|---|---|
| **Source Registry** | §4 | Registration, metadata, and lifecycle of data sources |
| **Raw Evidence Preservation** | §4, §8 | Immutable storage, tombstoning, provenance |
| **Entity and Asset Identity** | §4 | Canonical entity (issuer) and asset (instrument) identity, mapping, corporate actions |
| **Data Normalization** | §4 | Standard representations, unit conversion, identifier mapping |
| **Data Quality and Freshness** | §4 | Freshness monitoring, completeness checks, conflict detection, revision tracking |
| **Feature Computation Infrastructure** | §4 | Shared computation framework, versioning, reproducibility, deterministic execution |
| **Theme Intelligence** | §5 | Canonical Theme data: lifecycle, approval status, monitoring status, governance transitions, Theme Cards, evidence-to-theme relationships |
| **Evidence Relationships** | §4 | Cross-referencing evidence to themes, entities, and candidates |
| **Human Feedback** | §4 | Recording and preserving human feedback, overrides, and their history |
| **Audit History** | §4 | System-wide audit infrastructure for all material transitions |
| **Knowledge Export** | §4 | Structured export of platform state for narrative tools |

**Feature computation boundary:**

- Shared Core provides **feature computation infrastructure**: versioned, reproducible, deterministic computation with provenance tracking.
- Each strategy **owns its own feature definitions**: which features to compute, what formulas to use, what weights to assign.
- Shared infrastructure ensures reproducibility; strategy-owned definitions ensure domain relevance.
- A feature may be promoted to Shared Core only when multiple strategies require the identical computation with identical semantics.

**Canonical Theme relationship ownership — pending Founder decision:**

Whether canonical structural Theme roles (Direct Beneficiary, Enabler, Bottleneck Owner, Second-order Beneficiary) belong to Entity–Theme relationships, Candidate–Theme relationships, or a layered combination is an **open Founder decision** (see CANDIDATE-AND-QUEUE-MODEL §3.4).

- **Recommendation:** A layered model where Shared Core maintains canonical Entity–Theme structural roles as the authoritative baseline, and strategy-specific Candidate–Theme relationships may refine or add context without silently contradicting the canonical role.
- **V0 approach:** V0 may use simplified Candidate–Theme test relationships without establishing permanent canonical ownership. The decision must be resolved before V1 or before a second strategy consumes Theme roles.
- This remains unresolved in Project Definition v0.1 and requires a separate explicit Founder decision.

**Additionally universal:**

- Authentication and authorization (when needed)
- Shared data contracts consumed by multiple strategies
- Research Queue storage and retrieval infrastructure

**Shared infrastructure, strategy-owned semantics:**

- Research Queue storage and retrieval infrastructure may be shared.
- Each strategy **owns its own prioritization, ranking, ordering, and filtering semantics.**
- The Shared Core provides data; the strategy decides what matters.

### 1.2 Alpha Momentum

**First implementation vertical slice** (Constitution §3, §13; Founder's Decision #2). Active path: Momentum & Market Leadership Intelligence per INVESTMENT-INTELLIGENCE-OPERATING-MODEL.md.

Owns:

- **Eligibility:** Which assets qualify for Alpha Momentum screening (e.g., US-listed common stocks and ADRs, minimum liquidity)
- **Filtering:** Whether and how Theme relationships act as filters, enrichment, or ranking inputs
- **Prioritization and ranking:** What makes a Candidate higher or lower priority within Alpha Momentum
- **Strategy relevance:** How Candidate Quality, Entry Readiness, and Theme Quality combine in Alpha Momentum's context
- Candidate Quality dimensions, weights, feature definitions, and scoring
- Entry Readiness dimensions, weights, feature definitions, and scoring
- Research Queue prioritization and ordering for Alpha Momentum
- Alpha Momentum-specific rule packs
- Alpha Momentum-specific screening pipeline and stage definitions

Consumes from Shared Core:

- Canonical Theme data (lifecycle, approval status, monitoring status)
- Evidence and source data
- Entity and asset identity
- Normalized data
- Feature computation infrastructure (for executing strategy-defined features)
- Audit infrastructure

### 1.3 Close System

**Second strategy world** (Constitution §15; INVESTMENT-INTELLIGENCE-OPERATING-MODEL.md). Defined later (Phase 7+).

### 1.4 Fundamental & Opportunity Intelligence (V1+)

**Future intelligence path** (INVESTMENT-INTELLIGENCE-OPERATING-MODEL.md §5). Defined later (Phase 8). Covers Macro, Industry, Product, Company, Earnings & Change Analysis, and Valuation Context. Not active in V0. Not detailed in these Project Definition documents beyond boundary marking.

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

## 2. Shared Core Promotion Criteria

A capability may be promoted into Shared Core only when **one** of the following is true:

1. **Multiple real consumers exist** — at least two strategy modules or system components genuinely require the capability with compatible semantics.
2. **Constitutional assignment** — the Constitution explicitly designates the capability as shared domain ownership (e.g., Theme Intelligence).

A capability that is merely *plausibly useful* to future strategies stays with its first consumer until a real second consumer demands it.

## 3. Domain Entity Map

```
Entity / Issuer
  │
  ├── issues or is represented by
  │
  ▼
Asset / Instrument
  │
  ├── evaluated within Strategy context as
  │
  ▼
Candidate

Evidence and Themes may relate to Entity, Asset, Candidate, and Candidate–Theme relationships.
Canonical Theme-role ownership (Entity–Theme vs. Candidate–Theme) remains a pending Founder decision.

─── Domain Relationships ───

Evidence ──────────────┐
  │                    │
  ├── Source           │
  ├── Raw Record       │
  ├── Fact / Claim     │
  ├── Derived Metric   │
  ├── AI Extraction    │
  └── Statistical Signal
                       │
                       ▼
Theme ◄────────────────┴──────────┐
  │                               │
  ├── Lifecycle (6 stages)        │
  ├── Approval Status (5 states)  │
  ├── Monitoring Status (4 states)│
  ├── Theme Card                  │
  ├── Weak Signal (V1+)           │
  └── Discovery Paths (V1+)       │
      │                           │
      │         ┌─────────────────┘
      ▼         ▼
Candidate ◄──────┴────────────────┐
  │                               │
  ├── Candidate Quality           │
  ├── Entry Readiness             │
  ├── Data Confidence             │
  ├── Theme Relationship Role ◄───┤ (Candidate–Theme)
  ├── Leadership State ◄──────────┤ (Candidate–Theme)
  └── Research State ◄────────────┤ (Candidate–Strategy–Workflow)
      │                           │
      ▼                           │
Research Queue ◄──────────────────┘
  │
  ▼
Human Review ──────────────┐
  │                        │
  ├── Feedback              │
  ├── Override              │
  └── Decision              │
      │                    │
      ▼                    │
Learning Loop (Later) ◄────┘
  │
  ├── Outcome
  ├── Postmortem
  ├── Lesson Draft
  ├── Approved Lesson
  └── Rule / Playbook Proposal
```

## 4. Information Flow

### 4.1 Evidence → Theme

Evidence is linked to Themes through relationships. A single Evidence record may support or contradict multiple Themes. Theme Quality assessment draws on linked evidence.

### 4.2 Theme → Candidate

Candidates are linked to Themes through **Candidate–Theme relationships**. This relationship carries:

- Theme Relationship Role (one primary + optional secondary roles)
- Leadership State (one current, versioned history)
- Supporting and contradicting evidence specific to this Candidate–Theme pair

A Candidate may relate to multiple Themes with different roles and leadership states in each.

Canonical structural Theme role ownership is a pending Founder decision (see CANDIDATE-AND-QUEUE-MODEL §3.4). V0 may use simplified Candidate–Theme relationships for demonstration without establishing permanent canonical ownership.

### 4.3 Candidate → Research Queue

The Research Queue is organized by Theme first, then by Candidates within each Theme.

Queue infrastructure (storage, retrieval) may be shared. Queue prioritization and ordering are **strategy-owned**. Alpha Momentum determines what makes a Candidate higher or lower priority within its own context.

### 4.4 Human Review → Learning

Human decisions, overrides, and outcomes feed the Learning Loop in Later phases. V0 defines the contracts only.

## 5. Cross-Cutting Concerns

| Concern | Owner | Notes |
|---|---|---|
| Audit trail | Shared Core | All material state transitions record actor, timestamp, reason, evidence, version |
| Versioning | Shared Core | Material transformations are versioned; history is append-only |
| Point-in-time | Shared Core | Queries must be reproducible at a given point in time |
| Immutability | Shared Core | Raw evidence is not silently edited in place; tombstones for controlled removal |
| External content | Shared Core | All ingested content is untrusted data; never treated as authority |
| Reproducibility | Shared Core | Deterministic features and versioned transformations |

## 6. What Does NOT Belong in Shared Core

- Strategy-specific scoring weights or thresholds
- Strategy-specific ranking or prioritization logic
- Strategy-specific rule packs (e.g., O'Neil, Minervini)
- Strategy-specific feature definitions (formulas, weights, which features to compute)
- Entry Readiness models specific to Alpha Momentum
- Candidate Quality dimensions specific to Alpha Momentum
- Strategy-specific eligibility, filtering, or screening pipeline definitions
- Close System suitability or macro regime logic
- Any logic with only one consumer and no constitutional mandate
