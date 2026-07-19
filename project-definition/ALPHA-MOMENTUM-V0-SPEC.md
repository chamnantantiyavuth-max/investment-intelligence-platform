# Alpha Momentum V0 Specification

Status: Approved Domain Specification
Version: 0.1
Owner: Founder
Authority: Approved Domain Specification subordinate to the Constitution and Founder's Decisions
Derived from: Investment Intelligence Platform Constitution v0.3
Approval: PD-v0.1-FOUNDING-DOMAIN-SPECIFICATIONS

## 1. Purpose

Alpha Momentum V0 is the first end-to-end vertical slice of the Investment Intelligence Platform (Constitution §3, §20; Founder's Decision #2).

V0 must prove that the domain model, evidence lineage, quality dimension separation, Theme Card, Research Queue, human feedback, reproducibility, and historical state tracking all work together in a working system — using fully synthetic fixtures or Founder-approved fixed historical public snapshots with Founder-approved controlled themes.

V0 is a **proof of concept**, not a production system.

## 2. Controlled Universe

### 2.1 V0 Investable Universe

US-listed common stocks and suitable ADRs (Constitution §13; DNA-017).

In V0, this universe is represented by fully synthetic fixtures or Founder-approved fixed historical public snapshots. V0 prohibits: live/current market feeds, production ingestion, broker/private account data, unlabeled current data, and unapproved licensed feeds.

### 2.2 Universe Constraints

- **V0 size:** A controlled subset sufficient to demonstrate all domain concepts (not the full US market).
- **Point-in-time:** V0 data must carry timestamps and be queryable at a given point in time, even if synthetically constructed.
- **No private positions:** No real portfolio identifiers, account numbers, broker accounts, execution endpoints, or private transactions.

## 3. Controlled Themes

V0 uses **Founder-approved controlled themes** only. No AI theme discovery. No Weak Signal Inbox. No Experimental Themes.

### 3.1 Theme Selection Criteria

A theme is eligible for the V0 controlled set when it meets the following:

1. **Structural:** The theme represents a structural economic, technological, policy, or demographic driver — not a short-term catalyst, rumor, or single-event narrative.
2. **Identifiable beneficiaries:** Companies in the US-listed universe can be identified as Direct Beneficiaries, Enablers, Bottleneck Owners, or Second-order Beneficiaries.
3. **Evidence availability:** Sufficient public-domain evidence exists to construct realistic V0 fixtures for demonstration purposes.
4. **Domain coverage:** The controlled set should collectively exercise required domain cases. Testability, evidence diversity, lifecycle coverage, and relationship-role coverage take priority over novelty.

### 3.2 Theme Approval Process

1. **Founder proposes** one or more candidate themes meeting the selection criteria. Platform records each as a Theme entity with Detected Hypothesis Approval Status.
2. **Founder begins formal review** → Approval Status transitions to Under Human Review.
3. **Founder explicitly approves** each theme for the V0 controlled set → Approval Status transitions to Approved.
4. **Monitoring Status is set independently.** For the V0 controlled set, Monitoring Status is normally set to Active Monitoring.
5. **Approved V0 Theme fixtures are configured** with evidence, candidates, and relationships.

The actual V0 theme list is **deferred** to Founder selection at implementation time. This specification does not invent or populate a theme list.

### 3.3 Theme Documentation Requirements

Each V0 controlled theme must be documented with:

- Driver description (what is changing and why)
- Evidence structure (supporting, contradicting, missing — even if synthetic)
- Industry and sector mapping
- Candidate map (leaders, challengers, and beneficiaries — individual V0 themes need not populate every Theme Relationship Role; unsupported roles are shown as empty or unknown. Fixture coverage across the full V0 set should ensure all roles appear somewhere.)
- Lifecycle stage with rationale
- Confidence assessment with rationale

## 4. Screening Pipeline (Conceptual)

V0 demonstrates a conceptual screening pipeline. The pipeline is not required to be production-grade or performant.

### 4.1 Pipeline Stages

```
Universe Definition
  → Theme Context / Theme-linked Selection (Candidate–Theme relationships)
    → Candidate Quality Assessment
      → Entry Readiness Assessment
        → Data Confidence Assessment
          → Research Queue Assembly
```

### 4.2 Stage Descriptions

| Stage | Description | Owner |
|---|---|---|
| **Universe Definition** | Select the controlled US-listed universe for the pipeline run | Alpha Momentum |
| **Theme Context / Theme-linked Selection** | Identify Candidates linked to active Approved Themes via Candidate–Theme relationships. Shared Core supplies Approved Theme relationships; Alpha Momentum decides whether they act as filter, enrichment, or ranking input. | Alpha Momentum |
| **Candidate Quality Assessment** | Assess each Candidate on fundamentals, growth, liquidity, relative strength, trend quality, accumulation, industry leadership | Alpha Momentum |
| **Entry Readiness Assessment** | Assess each Candidate on price structure, base quality, breakout proximity, volume behavior, volatility contraction, extension risk | Alpha Momentum |
| **Data Confidence Assessment** | Assess freshness, completeness, reliability, conflicts, and missing data for each Candidate's underlying data | Shared Core |
| **Research Queue Assembly** | Order by Theme, then by strategy-owned prioritization within each Theme | Alpha Momentum |

### 4.3 Deterministic Features

All feature computations must be deterministic: the same input produces the same output. Reproducibility is required (Constitution §20).

V0 features need not be final or production-grade. Exact feature formulas, weights, and thresholds are deferred.

### 4.4 Theme Context Boundary

The Theme-linked pipeline demonstrated in V0 is a **demonstration boundary**, not the permanent Alpha Momentum pipeline architecture.

Future Alpha Momentum versions must preserve the ability to:

- Discover candidates through stock-first screening (e.g., fundamental and technical filters) independent of Theme membership.
- Enrich stock-first candidates with Theme context after discovery.
- Combine Theme-linked and stock-first discovery paths.

V0 demonstrates the Theme-linked path because it exercises the full domain model (Evidence → Theme → Candidate → Queue). It does not preclude or replace stock-first discovery in later versions.

## 5. Required V0 Outputs

V0 must produce:

### 5.1 Theme Cards

For each Approved V0 theme, a Theme Card containing:

- Theme name and driver summary
- Why-now case
- Lifecycle stage, Approval Status, and Monitoring Status
- Confidence assessment
- Supporting, contradicting, and missing evidence
- Alternative explanations (if applicable)
- Candidate lists organized by Theme Relationship Role and Leadership State
- Watchlist members

### 5.2 Research Queue

A Theme-first Research Queue that:

- Groups Candidates by Theme
- Presents Candidate assessments with four separated quality dimensions
- Supports adaptive capacity (may return zero high-priority candidates)
- Provides human-readable explanations for prioritization

### 5.3 Evidence Lineage

For any assessment, the ability to trace back to:

- Raw source records
- Extraction and normalization steps
- Feature computation versions
- Any human overrides or judgments

### 5.4 Historical State

The ability to:

- View any Theme, Candidate, or assessment at a prior point in time
- See lifecycle, Approval Status, and Monitoring Status transition history with full audit fields
- See override history with original system assessments preserved

### 5.5 Human Feedback

The ability to:

- Record a Human Override with all 8 required fields
- View override history without the original assessment being hidden
- Change Research State for any Candidate

## 6. V0 Acceptance Criteria

V0 is accepted when it demonstrates all of the following (derived from Constitution §20):

| # | Criterion | Evidence Required |
|---|---|---|
| AC-1 | **Evidence lineage** | A human reviewer can trace a Candidate Quality assessment back through features, normalized data, and raw source records |
| AC-2 | **Deterministic features** | Running the same pipeline on the same fixture data twice produces identical results |
| AC-3 | **Separated dimensions** | Candidate Quality, Theme Quality, Entry Readiness, and Data Confidence are presented as distinct assessments — not one composite score |
| AC-4 | **Theme Cards** | Each V0 theme renders a complete Theme Card with all required fields |
| AC-5 | **Research Queue** | The queue is Theme-first, supports adaptive capacity, and can return zero candidates |
| AC-6 | **Human feedback** | An override can be recorded with all 8 fields; the original system assessment remains visible |
| AC-7 | **Reproducibility** | A pipeline run can be repeated with the same inputs and version references, producing identical outputs |
| AC-8 | **Historical state** | Theme lifecycle, Approval Status, and Monitoring Status transitions are recorded with full audit trails and are queryable |
| AC-9 | **Three candidate axes with correct scoping** | A Candidate–Theme relationship carries Theme Relationship Role(s) and Leadership State. A Candidate–Strategy–Workflow context carries Research State. All three axes are presented separately and scoped correctly — not as global Candidate properties |
| AC-10 | **No live-data or production-integration contamination** | Only fully synthetic fixtures or Founder-approved fixed historical public snapshots are used. No live feeds, no production ingestion, no broker data, no unlabeled current data, no unapproved licensed feeds. Any provisional technology used for V0 is not claimed as a final stack selection. |

## 7. V0 Non-Scope (Explicit)

V0 does **not** include:

- Live or current market feeds
- Production data ingestion
- Broker connectivity, order execution, or portfolio allocation
- Unapproved licensed data vendor feeds
- Weak Signal Inbox (Unexplained Anomalies or Theme Hypotheses)
- AI-driven theme discovery (any form)
- Experimental Theme creation or tracking
- Learning Loop closure (outcomes, postmortems, lessons, rule changes)
- Close System (any)
- Global expansion (any)
- Deep Research handoff (any)
- Production-scale performance or scalability
- Final scoring weights, thresholds, or rule packs
- Production UI or deployment infrastructure
- Obsidian or NotebookLM export

## 8. Data Requirements

### 8.1 Permitted Fixture Categories

V0 uses exactly two permitted fixture categories:

1. **Fully synthetic fixtures:** Generated data with no connection to real companies or events.
2. **Founder-approved fixed historical public snapshots:** Real public-domain data frozen at a specific historical date, clearly labeled as such.

Every fixture must carry:

- **Fixture category:** Synthetic or Founder-Approved Historical Snapshot.
- **As-of date:** The point-in-time the fixture represents.
- **Visible marker:** A clear "NOT LIVE DATA — FOR V0 TESTING ONLY" designation on any rendered output.

Historical snapshots must not be mistaken for current market data or investment advice.

### 8.2 Fixture Data Characteristics

V0 fixtures must:

- Be sufficient to exercise all domain entities and relationships
- Carry timestamps enabling point-in-time queries
- Include deliberate quality variation (some records fresh, some stale; some complete, some with gaps)
- Include deliberate contradictions (conflicting evidence for the same theme)
- Include sufficient entities to demonstrate the three candidate axes and Theme-first queue

### 8.3 Minimum V0 Fixture

V0 must include a minimal test fixture exercising all domain concepts. The fixture must include (without inventing theme names — actual themes are Founder-selected later):

- A small controlled universe of assets (entities and instruments).
- Two or three Founder-approved themes (selected at implementation time, not specified here).
- For at least one theme: both supporting and contradicting evidence cases.
- For at least one theme: explicit missing-evidence markers.
- At least one Candidate with multiple Theme Relationship Roles (e.g., primary Direct Beneficiary + secondary Enabler).
- At least one Candidate–Theme relationship with a Leadership State transition in its audit history.
- At least one Theme lifecycle transition, one Approval Status transition, and one Monitoring Status transition.
- At least one Human Override in Pending state.
- At least one Research Queue view that returns zero high-priority candidates.

This fixture set ensures the V0 acceptance criteria can be tested against real domain complexity while using only permitted fixture categories.

### 8.4 What Fixtures Must NOT Contain

- Real company financials that could be mistaken for live data
- Real portfolio identifiers or account numbers
- Real broker accounts, account identifiers, sessions, execution endpoints, private positions, or private transactions
- Personally identifiable information
- Licensed or copyrighted data used without permission
- Unlabeled current market data
- Live/current market feeds
- Production ingestion pipelines
- Unapproved licensed data vendor feeds

**Permitted in clearly labeled fixed historical public snapshots:** public issuer names, ticker symbols, listing exchange identifiers, and other public-domain identifiers.
