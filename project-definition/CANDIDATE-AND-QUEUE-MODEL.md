# Candidate and Queue Model

Status: Approved Domain Specification
Version: 0.1
Owner: Founder
Authority: Approved Domain Specification subordinate to the Constitution and Founder's Decisions
Derived from: Investment Intelligence Platform Constitution v0.3
Approval: PD-v0.1-FOUNDING-DOMAIN-SPECIFICATIONS

## 1. Candidate Identity

The platform distinguishes three technology-neutral identity concepts:

### 1.1 Entity / Issuer

The legal or operating entity behind one or more securities (e.g., a corporation, its management, its business operations). The Entity is the subject of fundamental analysis and thematic relevance.

### 1.2 Asset / Instrument

A specific listed security or tradable instrument issued by an Entity (e.g., common stock, ADR). One Entity may have multiple Assets/Instruments across exchanges or share classes.

### 1.3 Candidate

A Candidate is an Asset/Instrument evaluated within a specific Strategy context, referencing its Issuer where applicable. It is not a global property of the Asset — it is a strategy-specific evaluation context.

In V0: a Candidate is a US-listed common stock or suitable ADR (the Asset), referencing its issuing company (the Entity), evaluated within Alpha Momentum.

A Candidate is not inherently "good" or "bad." Its assessments are always contextual — relative to a Theme, a strategy, and a point in time.

## 2. Four Quality Dimensions

The platform keeps four quality dimensions separate (Constitution §10, §13). They must not be collapsed into one opaque score.

### 2.1 Candidate Quality

**What it measures:** The quality of the company or asset itself, independent of entry timing.

**Domains (deferred finalization — OPEN-QUESTIONS.md):**

- Fundamentals (earnings, sales, margins, ROE, etc.)
- Growth (trajectory, acceleration, sustainability)
- Liquidity (volume, float, institutional interest)
- Relative strength (price performance vs. market and sector)
- Trend quality (smoothness, duration, institutional character)
- Accumulation (volume patterns suggesting institutional buying)
- Industry leadership (position within industry group)

**Owner:** Alpha Momentum strategy.

### 2.2 Theme Quality

**What it measures:** The strength, health, and evidence backing of the Candidate's related Theme(s).

**Domains (deferred finalization):**

- Lifecycle stage (each stage presents a different opportunity, uncertainty, and crowding profile — no stage is inherently higher quality)
- Breadth (number and diversity of participating entities)
- Leadership (clarity and strength of leaders and challengers)
- Evidence progression (how far evidence has advanced from structural to confirmed)
- Market confirmation (whether price behavior supports the theme)
- Fundamental confirmation (whether company fundamentals reflect the theme driver)
- Crowding (how widely recognized the theme is)
- Confidence (how well-supported the theme thesis is)

**Owner:** Shared Core (Theme Intelligence).

### 2.3 Entry Readiness

**What it measures:** Whether the Candidate presents a favorable entry opportunity at this moment.

**Domains (deferred finalization):**

- Price structure (base, consolidation, or trend pattern)
- Base quality (duration, depth, contraction characteristics)
- Breakout proximity (how close to a potential entry point)
- Volume behavior (volume on up vs. down days, recent patterns)
- Volatility contraction (narrowing ranges suggesting coiling)
- Extension risk (how far above a logical entry or moving average)

**Owner:** Alpha Momentum strategy.

### 2.4 Data Confidence

**What it measures:** The reliability and completeness of the data underlying the Candidate's assessments.

**Domains:**

- Freshness of underlying data
- Completeness of required fields
- Reliability of sources
- Conflicts between sources
- Missing data

**Owner:** Shared Core.

### 2.5 Separation Rule

These four dimensions are presented separately. No weighted sum, composite score, or single ranking may silently absorb trade-offs between them. A Candidate may score well on Candidate Quality and poorly on Entry Readiness, or vice versa. The system must make these trade-offs visible.

## 3. Three Candidate Axes

A Candidate has three independent axes of classification. They are not one enum. Each axis has distinct scope and cardinality:

- **Theme Relationship Role:** one or more per Candidate–Theme relationship, with optional primary role designation.
- **Leadership State:** normally one current value per Candidate–Theme relationship, with versioned transition history.
- **Research State:** normally one current value per Candidate–Strategy–Workflow context.

These axes operate at different scopes (Candidate–Theme vs. Candidate–Strategy–Workflow) and are not global Candidate properties.

### 3.1 Theme Relationship Role

**Scope:** Candidate–Theme relationship (not global to the Candidate).

**Values:**

| Value | Description |
|---|---|
| **Direct Beneficiary** | The Candidate directly benefits from the Theme driver (e.g., a company whose primary product addresses the theme) |
| **Enabler** | The Candidate provides critical infrastructure, technology, or services that enable the Theme |
| **Bottleneck Owner** | The Candidate controls a scarce resource, patent, regulatory approval, or other chokepoint the Theme depends on |
| **Second-order Beneficiary** | The Candidate benefits indirectly — through increased demand for complementary products, regional exposure, or supply-chain position |

**Constraints:**

- A Candidate–Theme relationship may carry **one or more roles**.
- One role may be designated as **primary**; others are **secondary**.
- Each role assignment must support: **evidence references, confidence, effective dates, and change history**.
- The same Candidate may have **different roles in different Themes**.

### 3.2 Leadership State

**Scope:** Candidate–Theme relationship (not global to the Candidate).

**Values:**

| Value | Description |
|---|---|
| **Emerging Challenger** | The Candidate is gaining position but has not yet established clear leadership |
| **Confirmed Leader** | The Candidate is a recognized leader within the Theme (market share, revenue exposure, mindshare, price leadership) |
| **Former Leader** | The Candidate was a Confirmed Leader but has lost position (may still be a Beneficiary or Watchlist member) |
| **Deteriorating Member** | The Candidate's position, fundamentals, or relevance to the Theme is declining |

**Constraints:**

- Each Candidate–Theme relationship normally has **one current Leadership State**.
- Leadership State transitions are **versioned** and must preserve **transition history** (prior state, new state, reason, evidence, actor, timestamp).
- The same Candidate may have **different leadership states across different Themes**.

### 3.3 Research State

**Scope:** Candidate within a specific Strategy or Research Workflow (not global to the Candidate).

**Values:**

| Value | Description |
|---|---|
| **Watchlist** | The Candidate is being monitored but has not been promoted for active research |
| **Priority Research** | The Candidate has been identified as deserving deeper investigation |
| **Selected for Deep Research** | The Candidate is undergoing or queued for detailed research (Company Intelligence Workbench — Later phases) |
| **Archived** | The Candidate has been removed from active consideration within this workflow; history preserved |

**Constraints:**

- A Candidate normally has **one current Research State per Strategy–Workflow context**.
- Research State is **not a global Candidate property**. Different strategies or workflows may assign different research states to the same Candidate.
- Transitions must be audited.
- Archived Candidates retain history and may be reactivated.

### 3.4 Open Decision: Canonical Theme Role Ownership

**Founder decision required — not yet resolved:** Whether canonical structural Theme roles (Direct Beneficiary, Enabler, Bottleneck Owner, Second-order Beneficiary) belong to:

1. **Entity–Theme relationships** — the role is a property of the company's structural relationship to the Theme, independent of any strategy.
2. **Candidate–Theme relationships** — the role is always assessed within a strategy's evaluation context.
3. **A layered combination** — Entity–Theme carries the canonical structural role; Candidate–Theme may refine or override it for strategy-specific purposes.

**Recommendation (not decided):** A layered model (option 3). Shared Core would maintain canonical Entity–Theme structural roles as the authoritative baseline. Strategy-specific Candidate–Theme relationships could refine or add context but could not silently contradict the canonical role without an explicit override and rationale.

**V0 approach:** V0 may use simplified Candidate–Theme test relationships without establishing permanent canonical ownership. This decision is not required for V0 but must be resolved before V1 or before a second strategy consumes Theme roles.

**Impact:** This decision affects where role data is authored, how contradictions between structural and strategy-specific roles are resolved, and which context owns role transition history.

## 4. Theme-First Research Queue

### 4.1 Structure

The Research Queue is organized by **Theme Card first**, then by Candidates within each Theme (Constitution §14).

A Theme Card presents:

- Theme summary and why-now case
- Lifecycle, confidence, approval status, and monitoring status
- Candidate lists organized by Theme Relationship Role and Leadership State
- Supporting and contradicting evidence summary

Within a Theme, Candidates are ordered by strategy-owned prioritization.

### 4.2 Adaptive Capacity

Queue capacity is **adaptive** (Founder's Decision #9). It does not fill a fixed quota.

It may return:

- Zero high-priority candidates (DNA-016: Honest Empty States)
- A small number of high-conviction candidates
- A larger number when breadth is high and evidence is strong

Capacity is determined by the number of candidates that meet the strategy's quality thresholds, not by a target count.

### 4.3 Infrastructure vs. Semantics

- **Shared Core** may provide queue storage, retrieval, and presentation infrastructure.
- **Each strategy** owns its prioritization, ranking, ordering, and filtering semantics.
- Alpha Momentum determines what makes a Candidate higher or lower priority within Alpha Momentum's research queue.

## 5. Version Boundaries for Candidate and Queue Capabilities

| Capability | V0 | V0.5 | V1 | V1.5 | Later |
|---|---|---|---|---|---|
| Candidate entity with four quality dimensions | ✅ | ✅ | ✅ | ✅ | ✅ |
| Three candidate axes (role, leadership, research) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Theme-first Research Queue with adaptive capacity | ✅ | ✅ | ✅ | ✅ | ✅ |
| Synthetic candidate data | ✅ | — | — | — | — |
| Real EOD candidate data | — | ✅ | ✅ | ✅ | ✅ |
| Experimental theme candidates (separated from official) | — | — | ✅ | ✅ | ✅ |
| AI-driven candidate discovery within themes | — | — | — | ✅ | ✅ |
| Deep Research handoff | — | — | — | — | ✅ |
