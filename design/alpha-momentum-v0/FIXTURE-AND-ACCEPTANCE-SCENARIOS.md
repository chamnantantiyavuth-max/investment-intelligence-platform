# Fixture and Acceptance Scenarios — Gate C

Status: Approved — Gate C Complete (Founder Review 22 Jul 2026)
Version: 1.0
Owner: Founder
Authority: Gate C artifact subordinate to the Constitution, Founder's Decisions, Approved Domain Specifications, and Approved Stable Design Plan v0.1
Derived from: Constitution v0.3, Project Definition v0.1 (ALPHA-MOMENTUM-V0-SPEC §8, EVIDENCE-MODEL, THEME-MODEL, CANDIDATE-AND-QUEUE-MODEL, HUMAN-REVIEW-AND-LEARNING-MODEL)
Draft Authorization: Founder Decision #19 (Gate C Authorization)
Prerequisite: CONTROLLED-THEME-SET.md v1.0 (Gate B Complete)

---

## 1. Purpose

This document defines:

1. **Fixture categories** — the two permitted data sources for V0 testing
2. **Fixture shapes** — technology-neutral descriptions of every domain entity required for V0 acceptance testing
3. **Minimum fixture set** — the minimal data required to exercise all V0 acceptance criteria
4. **Acceptance scenarios** — Given/When/Then cases with known answers, traceable to the 10 approved V0 ACs (ALPHA-MOMENTUM-V0-SPEC §6)
5. **Contradiction and missing-evidence cases** — specific scenarios that verify the platform handles uncertainty correctly

All fixtures are **technology-neutral**. They describe domain shapes, not database rows, CSV columns, or JSON fields. Implementation representations remain deferred.

---

## 2. Fixture Categories

Per ALPHA-MOMENTUM-V0-SPEC §8.1, V0 uses exactly two permitted fixture categories:

### 2.1 Category A — Fully Synthetic Fixtures

| Property | Requirement |
|---|---|
| **Content** | Entirely generated; no connection to real companies, events, or market data |
| **Naming** | Fictional company names, fictional tickers (e.g., "SYNTH-01", "ACME Corp") |
| **Data values** | Plausible but invented; not derived from any real financial data |
| **Labeling** | Every fixture carries: `[SYNTHETIC — FOR V0 TESTING ONLY]` |
| **Use case** | Exercising domain logic without any real-world contamination |

### 2.2 Category B — Founder-Approved Fixed Historical Public Snapshots

| Property | Requirement |
|---|---|
| **Content** | Real public-domain data frozen at a specific historical date |
| **Source** | Public filings (10-K/10-Q), publicly available market data, public-domain industry classifications |
| **Freeze date** | Explicit as-of date; data never updated after freeze |
| **Labeling** | Every fixture carries: `[HISTORICAL SNAPSHOT — AS OF <date> — NOT LIVE DATA — FOR V0 TESTING ONLY]` |
| **Use case** | Verifying domain logic against real-world data shapes without live-data dependency |

### 2.3 Prohibited Fixture Content (Both Categories)

Per ALPHA-MOMENTUM-V0-SPEC §8.4:

- ❌ Real company financials that could be mistaken for live data (except in clearly labeled Category B)
- ❌ Real portfolio identifiers or account numbers
- ❌ Real broker accounts, execution endpoints, private positions
- ❌ Personally identifiable information
- ❌ Licensed data used without permission
- ❌ Unlabeled current market data
- ❌ Live/current market feeds

---

## 3. Fixture Shapes

### 3.1 Theme Fixture

Each Theme fixture must contain:

| Field | Type | Required | Example (Synthetic) | Example (Historical — AI Infrastructure, July 2024) |
|---|---|---|---|---|
| **Theme ID** | Identifier | ✅ | THEME-SYN-01 | TH-004 (Semiconductors) |
| **Theme Name** | Text | ✅ | "Quantum Widget Supply Chain" | "Semiconductors" |
| **Industry** | Text (Finviz) | ✅ | "Synthetic - Advanced Widgets" | "Semiconductors" |
| **Sector** | Text (Finviz) | ✅ | "Technology" | "Technology" |
| **Lifecycle** | Enum | ✅ | Expansion | Expansion |
| **Approval Status** | Enum | ✅ | Approved | Approved |
| **Monitoring Status** | Enum | ✅ | Active Monitoring | Active Monitoring |
| **Why-Now Case** | Text | ✅ | "Quantum widgets enable 10x compute..." | "AI compute demand driving 200%+ data center revenue growth..." |
| **Supporting Evidence** | Evidence refs | ≥2 records | EV-SYN-001, EV-SYN-002 | Real public-domain data references |
| **Contradicting Evidence** | Evidence refs | ≥1 record | EV-SYN-003 | Real public-domain data references |
| **Missing Evidence** | Text markers | ≥1 marker | "Missing: long-term widget durability data" | "Missing: inference-to-training compute ratio long-term" |
| **Confidence** | Enum/text | ✅ | Medium | High |
| **Lifecycle Transition History** | Audit records | ≥1 transition | Weak Signal → Formation (2023-Q1) | Formation → Emerging (2022) → Expansion (2024) |
| **Approval Transition History** | Audit records | ≥1 transition | Detected → Under Review → Approved | Detected → Under Review → Approved |
| **Fixture Category** | Enum | ✅ | Synthetic | Founder-Approved Historical Snapshot |
| **As-Of Date** | Date | ✅ | 2024-06-30 | 2024-07-01 |
| **NOT LIVE DATA Marker** | Text | ✅ | Visible on all rendered output | Visible on all rendered output |

### 3.2 Entity / Issuer Fixture

| Field | Type | Required | Example (Synthetic) |
|---|---|---|---|
| **Entity ID** | Identifier | ✅ | ENT-SYN-001 |
| **Entity Name** | Text | ✅ | "ACME Quantum Widgets Inc." |
| **Sector** | Text | ✅ | "Technology" |
| **Industry** | Text | ✅ | "Synthetic - Advanced Widgets" |

### 3.3 Asset / Instrument Fixture

| Field | Type | Required | Example (Synthetic) |
|---|---|---|---|
| **Asset ID** | Identifier | ✅ | AST-SYN-001 |
| **Ticker** | Text | ✅ | "SYNTH01" |
| **Entity ID** | Ref → Entity | ✅ | ENT-SYN-001 |
| **Exchange** | Text | ✅ | "NYSE (synthetic)" |
| **Asset Type** | Enum | ✅ | Common Stock |
| **Fixture Category** | Enum | ✅ | Synthetic |

### 3.4 Evidence Fixture

| Field | Type | Required | Example |
|---|---|---|---|
| **Evidence ID** | Identifier | ✅ | EV-SYN-001 |
| **Evidence Type** | Enum (Constitution §8) | ✅ | Raw Source Record / Observed Fact / Claim / etc. |
| **Content** | Text | ✅ | "ACME Q2 2024 revenue: $2.3B, +45% YoY" |
| **Source Identifier** | Ref → Source Registry | ✅ | SRC-SYN-001 |
| **Publication Timestamp** | DateTime | ✅ | 2024-07-15T08:00:00Z |
| **Effective Period** | DateRange | ✅ | 2024-Q2 |
| **Evidence Relationship** | Enum | ✅ | Supporting / Contradicting / Missing |
| **Linked Theme ID** | Ref → Theme | ✅ | THEME-SYN-01 |
| **Linked Candidate** | Ref → Candidate (optional) | — | AST-SYN-001 |
| **Fixture Category** | Enum | ✅ | Synthetic |

### 3.5 Candidate Fixture

| Field | Type | Required | Example |
|---|---|---|---|
| **Candidate ID** | Identifier | ✅ | CAND-SYN-001 |
| **Asset ID** | Ref → Asset | ✅ | AST-SYN-001 |
| **Strategy Context** | Enum | ✅ | Alpha Momentum |
| **Candidate Quality — Fundamentals** | Label (deferred) | ✅ | "Strong" |
| **Candidate Quality — Growth** | Label (deferred) | ✅ | "Accelerating" |
| **Candidate Quality — Liquidity** | Label (deferred) | ✅ | "Adequate" |
| **Candidate Quality — Relative Strength** | Label (deferred) | ✅ | "Leading" |
| **Entry Readiness — Price Structure** | Label (deferred) | ✅ | "Stage 2 — Advancing" |
| **Entry Readiness — Base Quality** | Label (deferred) | ✅ | "Constructive" |
| **Entry Readiness — Breakout Proximity** | Label (deferred) | ✅ | "Near" |
| **Entry Readiness — Extension Risk** | Label (deferred) | ✅ | "Low" |
| **Data Confidence** | Label | ✅ | "High — 7/8 fields fresh" |

### 3.6 Candidate–Theme Relationship Fixture

| Field | Type | Required | Example |
|---|---|---|---|
| **Relationship ID** | Identifier | ✅ | CTR-SYN-001 |
| **Candidate ID** | Ref → Candidate | ✅ | CAND-SYN-001 |
| **Theme ID** | Ref → Theme | ✅ | THEME-SYN-01 |
| **Primary Role** | Enum | ✅ | Direct Beneficiary |
| **Secondary Roles** | Enum[] | — | [Enabler] |
| **Leadership State** | Enum | ✅ | Confirmed Leader |
| **Leadership Transition History** | Audit records | ≥1 record | Emerging Challenger → Confirmed Leader (2024-Q1) |
| **Evidence References** | Ref[] → Evidence | ≥1 per role | EV-SYN-001, EV-SYN-002 |

### 3.7 Research State Fixture

| Field | Type | Required | Example |
|---|---|---|---|
| **Candidate ID** | Ref → Candidate | ✅ | CAND-SYN-001 |
| **Strategy Context** | Enum | ✅ | Alpha Momentum |
| **Current State** | Enum | ✅ | Priority Research |
| **Transition History** | Audit records | ≥1 record | Watchlist → Priority Research (2024-07-20, Founder action) |

### 3.8 Human Override Fixture

Per HUMAN-REVIEW-AND-LEARNING-MODEL §2.1 (all 8 fields required):

| Field | Value (Example) |
|---|---|
| **System Assessment** | "Candidate Quality: Strong. Entry Readiness: Near. Recommendation: Promote to Priority Research." |
| **Machine Dissent** | "Warning: Data Confidence Low — 3/8 fields stale. Contradiction: competitor earnings decelerating." |
| **Unresolved Counter-Evidence** | "EV-SYN-003: Industry growth rate declining from 12% to 4% YoY." |
| **Founder Rationale** | "I believe the industry data lags — our channel checks show reacceleration. Promoting despite machine caution." |
| **Required Confirmation** | "Next 2 quarterly reports must show ≥10% revenue growth." |
| **Reassessment Point** | 2025-01-15 |
| **Eventual Outcome** | Pending |
| **Decision Type and Scope** | "Research State promotion: Watchlist → Priority Research for CAND-SYN-001" |

### 3.9 Research Queue Fixture

| Field | Type | Required | Example |
|---|---|---|---|
| **Queue ID** | Identifier | ✅ | Q-SYN-001 |
| **Snapshot Timestamp** | DateTime | ✅ | 2024-07-22T10:00:00Z |
| **Strategy Context** | Enum | ✅ | Alpha Momentum |
| **Themes in Queue** | Theme[] | ≥1 | [THEME-SYN-01, THEME-SYN-02, THEME-SYN-03] |
| **Theme Ordering** | Ordered list | ✅ | THEME-SYN-01, THEME-SYN-02, THEME-SYN-03 |
| **Candidates per Theme** | Ordered list | ≥0 | CAND-SYN-001, CAND-SYN-002 |
| **Empty Themes** | Theme[] | ≥1 | THEME-SYN-03 (0 candidates) |
| **Total Candidate Count** | Integer | ✅ | 2 |

---

## 4. Minimum Fixture Set

Per ALPHA-MOMENTUM-V0-SPEC §8.3, the minimum V0 fixture must satisfy all of the following. This section maps each requirement to specific fixture instances.

### 4.1 Minimum Fixture Inventory

| # | Requirement (SPEC §8.3) | Fixture Instance | Category |
|---|---|---|---|
| F1 | Small controlled universe | 3 Entity + 5 Asset fixtures | Synthetic |
| F2 | 2-3 Founder-approved themes | 3 themes: TH-004 (Semiconductors, Expansion), TH-014 (Medical Devices, Emerging), TH-010 (Solar, Formation) | Historical Snapshot + Synthetic evidence overlay |
| F3 | ≥1 theme with supporting + contradicting evidence | TH-004: supporting (AI demand), contradicting (cycle risk) | Historical Snapshot |
| F4 | ≥1 theme with explicit missing-evidence markers | TH-010: missing project ROI data | Historical Snapshot |
| F5 | ≥1 Candidate with multiple relationship roles | NVDA (synthetic representation): Direct Beneficiary + Enabler in TH-004 | Synthetic + Historical identifiers |
| F6 | ≥1 Leadership State transition | INTC (synthetic): Confirmed Leader → Former Leader in TH-004 | Synthetic |
| F7 | ≥1 Theme lifecycle transition | TH-014: Formation → Emerging Leadership | Synthetic |
| F8 | ≥1 Approval Status transition | TH-004: Detected Hypothesis → Under Human Review → Approved | Synthetic |
| F9 | ≥1 Monitoring Status transition | TH-010: Not Monitored → Active Monitoring | Synthetic |
| F10 | ≥1 Human Override in Pending state | Override on INTC Candidate in TH-004 | Synthetic |
| F11 | ≥1 Research Queue returning zero | Queue snapshot where all themes return 0 qualified candidates (all candidates below quality thresholds) | Synthetic |

### 4.2 Fixture Instance Map

```
Theme TH-004 (Semiconductors, Expansion, Approved, Active Monitoring)
├── Entity: NVIDIA Corp (historical identifier, synthetic data)
│   └── Asset: NVDA (historical ticker, synthetic price/fundamentals)
│       └── Candidate CAND-001: role=Direct Beneficiary+Enabler, leadership=Confirmed Leader
│           ├── Evidence EV-001: supporting (AI GPU revenue)
│           ├── Evidence EV-002: supporting (data center growth)
│           └── Evidence EV-003: contradicting (semiconductor cycle risk)
├── Entity: Intel Corp (historical identifier, synthetic data)
│   └── Asset: INTC (historical ticker, synthetic price/fundamentals)
│       └── Candidate CAND-002: role=Direct Beneficiary, leadership=Former Leader
│           ├── Leadership transition: Confirmed Leader → Former Leader (2021-Q3)
│           └── Human Override OVR-001: Founder overrides system demotion recommendation
│
Theme TH-014 (Medical Devices, Emerging Leadership, Approved, Active Monitoring)
├── Lifecycle transition: Formation → Emerging Leadership (2023-Q2)
├── Entity: Medtronic (historical identifier, synthetic data)
│   └── Asset: MDT → Candidate CAND-003: role=Direct Beneficiary, leadership=Confirmed Leader
│
Theme TH-010 (Solar, Formation, Approved, Active Monitoring)
├── Monitoring transition: Not Monitored → Active Monitoring (2024-Q1)
├── Missing evidence markers:
│   - Missing: solar project ROI at sustained 5%+ interest rates
│   - Missing: utility-scale battery storage cost trajectory
└── Entity: First Solar (historical identifier, synthetic data)
    └── Asset: FSLR → Candidate CAND-004: role=Direct Beneficiary, leadership=Emerging Challenger
```

---

## 5. Acceptance Scenarios

Each scenario is traceable to one or more of the 10 V0 acceptance criteria (ALPHA-MOMENTUM-V0-SPEC §6). All scenarios use data from the minimum fixture set (§4).

### 5.1 Evidence Lineage Scenarios

#### Scenario AC1-1: Trace Candidate Quality to Raw Source

**Traceability:** AC-1 (Evidence lineage)

```
GIVEN the fixture set is loaded
  AND Candidate CAND-001 (NVDA in TH-004) has Candidate Quality "Strong"
WHEN a human reviewer expands CAND-001 and selects "Trace Evidence"
THEN the system displays:
  - Raw source record EV-001 (AI GPU revenue data)
  - Extraction step: Raw Source → Observed Fact
  - Normalization step: Observed Fact → Normalized Fact
  - Feature computation step: Normalized Fact → "Revenue Growth: 45% YoY"
  - Assessment step: "Revenue Growth: 45% YoY" → Candidate Quality "Strong"
  AND each step shows its version, timestamp, and transformation method
  AND the reviewer can navigate forward and backward through the chain
```

#### Scenario AC1-2: Trace Through Human Override

**Traceability:** AC-1, AC-6

```
GIVEN Candidate CAND-002 (INTC in TH-004) has an active Human Override OVR-001
WHEN the reviewer views CAND-002's assessment
THEN the system displays:
  - System Assessment: "Candidate Quality: Weak. Leadership: Former Leader."
  - Override: "Founder overrides — maintain at Watchlist."
  AND the evidence lineage for the system assessment remains fully traceable
  AND the override does not erase the original assessment's evidence chain
```

### 5.2 Deterministic Features Scenarios

#### Scenario AC2-1: Reproducible Pipeline Run

**Traceability:** AC-2 (Deterministic features), AC-7 (Reproducibility)

```
GIVEN the fixture set is loaded at point-in-time 2024-07-01
  AND the pipeline version is v0.1.0
WHEN the screening pipeline runs on the fixture data
THEN the output is captured as Run-1
WHEN the same pipeline (v0.1.0) runs again on the same fixture data at the same point-in-time
THEN the output (Run-2) is identical to Run-1
  AND all Candidate Quality labels match
  AND all Entry Readiness labels match
  AND all Data Confidence labels match
  AND queue ordering is identical
```

#### Scenario AC2-2: Deterministic Feature with Missing Input

**Traceability:** AC-2

```
GIVEN Candidate CAND-004 (FSLR in TH-010) has 3 of 8 expected data fields populated
WHEN the pipeline computes Candidate Quality for CAND-004
THEN the 3 available fields produce deterministic labels
  AND the 5 missing fields produce "Unknown — Missing Data" labels
  AND Data Confidence shows "Low — 3/8 fields fresh"
  AND the result is reproducible across multiple runs
```

### 5.3 Separated Dimensions Scenarios

#### Scenario AC3-1: Four Dimensions Displayed Separately

**Traceability:** AC-3 (Separated dimensions)

```
GIVEN all Candidates in the fixture set have been assessed
WHEN the Reviewer views any Candidate Detail
THEN the display shows four distinct sections:
  - Candidate Quality (Fundamentals, Growth, Liquidity, RS, etc.)
  - Theme Quality (Lifecycle, Breadth, Leadership, Evidence, Crowding, Confidence)
  - Entry Readiness (Price Structure, Base Quality, Breakout Proximity, Volume, Extension)
  - Data Confidence (Freshness, Completeness, Reliability, Conflicts, Missing)
  AND no single composite number or score is displayed that combines these dimensions
  AND each dimension shows its component sub-dimensions with individual labels
```

#### Scenario AC3-2: Trade-off Visibility

**Traceability:** AC-3, AC-4

```
GIVEN Candidate CAND-003 (MDT in TH-014) has:
  - Candidate Quality: "Strong"
  - Entry Readiness: "Not Ready — Extended"
WHEN the Reviewer views CAND-003
THEN both assessments are visible simultaneously
  AND the system does not produce a single ranking that hides the trade-off
  AND the Theme Card for TH-014 lists CAND-003 with both labels visible
```

### 5.4 Theme Card Scenarios

#### Scenario AC4-1: Complete Theme Card Renders

**Traceability:** AC-4 (Theme Cards)

```
GIVEN Theme TH-004 (Semiconductors) is loaded with all fixtures
WHEN the Reviewer opens the full Theme Card for TH-004
THEN all required fields (§2.1 of THEME-CARD-AND-HUMAN-REVIEW-FLOW.md) are present:
  - Theme Name: "Semiconductors"
  - Lifecycle: "Expansion" (green)
  - Approval Status: "Approved"
  - Monitoring Status: "Active Monitoring"
  - Why-Now Case: present
  - Supporting Evidence: bullet list with ≥2 items
  - Contradicting Evidence: bullet list with ≥1 item (visible, not hidden)
  - Missing Evidence: present (or explicitly marked "None identified")
  - Alternative Explanations: present (or section hidden if none)
  - Confidence: present
  - Candidate Summary Table: CAND-001 and CAND-002 listed
```

#### Scenario AC4-2: Theme Card with Zero Candidates

**Traceability:** AC-4, AC-5

```
GIVEN Theme TH-010 (Solar) has no qualified Candidates (CAND-004 below quality threshold)
WHEN the Reviewer opens the full Theme Card for TH-010
THEN Theme-level information (fields 1-14) renders normally
  AND the Candidate Summary section shows:
    "No qualified candidates — theme is monitored but no actionable setups at this time."
  AND the table is not padded with fabricated candidates
```

### 5.5 Research Queue Scenarios

#### Scenario AC5-1: Theme-First Queue with Adaptive Capacity

**Traceability:** AC-5 (Research Queue)

```
GIVEN the fixture set has 3 Themes with varying Candidate counts:
  - TH-004: 2 qualified Candidates
  - TH-014: 1 qualified Candidate
  - TH-010: 0 qualified Candidates
WHEN the Reviewer opens the Research Queue
THEN the queue displays:
  - Theme cards ordered by sector
  - TH-004 with 2 Candidates
  - TH-014 with 1 Candidate
  - TH-010 with 0 Candidates (Honest Empty)
  AND total queue size is 3 (not padded to a target count)
  AND the queue does not lower thresholds to fill a quota
```

#### Scenario AC5-2: Empty Queue

**Traceability:** AC-5, AC-9

```
GIVEN all Candidates in the fixture set fall below the quality threshold
  AND the fixture includes an empty-queue snapshot Q-SYN-EMPTY
WHEN the Reviewer opens the Research Queue
THEN the queue displays:
  "No candidates meet current quality thresholds across any monitored theme."
  AND the count of actively monitored themes is shown (e.g., "3 themes monitored")
  AND no fabricated candidates are displayed
  AND the system does not silently lower thresholds
```

### 5.6 Human Feedback Scenarios

#### Scenario AC6-1: Override with All 8 Fields

**Traceability:** AC-6 (Human feedback)

```
GIVEN Candidate CAND-002 (INTC in TH-004) is displayed
  AND the system recommends demoting CAND-002 from Watchlist to Archived
WHEN the Founder records a Human Override:
  - System Assessment: captured automatically
  - Machine Dissent: captured automatically
  - Unresolved Counter-Evidence: EV-003 preserved
  - Founder Rationale: "Maintaining Watchlist — thesis still viable"
  - Required Confirmation: "Next earnings must show stabilization"
  - Reassessment Point: 2025-01-15
  - Eventual Outcome: Pending
  - Decision Type: Research State — maintain Watchlist
THEN all 8 fields are persisted
  AND the original system assessment remains visible
  AND the override does not delete or hide the system's recommendation
  AND the override appears in the Candidate's audit history
```

#### Scenario AC6-2: Override History Preserved

**Traceability:** AC-6, AC-8

```
GIVEN Candidate CAND-002 has Override OVR-001 (from AC6-1)
WHEN the Reviewer views CAND-002's history
THEN the override is listed chronologically
  AND the system assessment at override time is visible
  AND the Founder's rationale is visible
  AND later corrections do not erase this override record
```

### 5.7 Historical State Scenarios

#### Scenario AC8-1: Lifecycle Transition Audit

**Traceability:** AC-8 (Historical state)

```
GIVEN Theme TH-014 has a lifecycle transition: Formation → Emerging Leadership (2023-Q2)
WHEN the Reviewer queries TH-014's lifecycle history
THEN the audit record shows:
  - Prior state: Formation
  - New state: Emerging Leadership
  - Reason: "Leadership distinguishable; operational evidence accumulating"
  - Evidence references: linked
  - Actor: Founder
  - Timestamp: 2023-Q2 date
  - Rule/workflow version: recorded
```

#### Scenario AC8-2: Point-in-Time Query

**Traceability:** AC-8

```
GIVEN Theme TH-004 had Approval Status "Under Human Review" at 2024-01-01
  AND was later approved to "Approved" at 2024-03-15
WHEN the Reviewer queries TH-004's state at point-in-time 2024-02-01
THEN Approval Status shows "Under Human Review"
  AND the later "Approved" transition is not visible in this historical view
WHEN the Reviewer queries at point-in-time 2024-04-01
THEN Approval Status shows "Approved"
```

### 5.8 Candidate Axes Scenarios

#### Scenario AC9-1: Three Axes Scoped Correctly

**Traceability:** AC-9 (Three candidate axes)

```
GIVEN Candidate CAND-001 (NVDA):
  - Theme Relationship Role: Direct Beneficiary + Enabler (in TH-004)
  - Leadership State: Confirmed Leader (in TH-004)
  - Research State: Priority Research (in Alpha Momentum workflow)
WHEN the Reviewer views CAND-001
THEN the three axes are displayed in separate sections:
  - Theme Relationship Role: shown under Theme context
  - Leadership State: shown under Theme context
  - Research State: shown under Workflow context
  AND no axis is presented as a global Candidate property
```

#### Scenario AC9-2: Candidate in Multiple Themes

**Traceability:** AC-9

```
GIVEN a synthetic Candidate CAND-005 is linked to two Themes:
  - TH-004 (Semiconductors): role=Enabler, leadership=Emerging Challenger
  - TH-009 (Semi Equipment): role=Direct Beneficiary, leadership=Confirmed Leader
WHEN the Reviewer views CAND-005
THEN the Theme Card for TH-004 shows CAND-005 as "Enabler / Emerging Challenger"
  AND the Theme Card for TH-009 shows CAND-005 as "Direct Beneficiary / Confirmed Leader"
  AND CAND-005's Research State is consistent regardless of which Theme is viewed
```

### 5.9 Contradiction and Missing Evidence Scenarios

#### Scenario CON-1: Contradicting Evidence Remains Visible

**Traceability:** AC-1, AC-3, AC-4

```
GIVEN Theme TH-004 has supporting evidence EV-001 and contradicting evidence EV-003
WHEN the Reviewer views the TH-004 Theme Card
THEN both supporting and contradicting evidence are displayed
  AND contradicting evidence is NOT:
    - Hidden behind a toggle by default
    - In a smaller font or lower-contrast treatment
    - Summarized into a single "risk score" that erases specifics
  AND the presence of contradicting evidence does not prevent TH-004
    from appearing in the Research Queue
```

#### Scenario CON-2: Missing Evidence Markers

**Traceability:** AC-4

```
GIVEN Theme TH-010 has explicitly marked missing evidence
WHEN the Reviewer views the TH-010 Theme Card
THEN the Missing Evidence section shows:
  - "Missing: solar project ROI at sustained 5%+ interest rates"
  - "Missing: utility-scale battery storage cost trajectory"
  AND these are displayed in a separate section from supporting and contradicting
  AND the missing evidence contributes to the Data Confidence assessment
```

#### Scenario CON-3: Data Confidence Reflects Gaps

**Traceability:** AC-3, AC-9

```
GIVEN Candidate CAND-004 (FSLR in TH-010) has 3/8 fields populated
WHEN the pipeline computes Data Confidence
THEN the result is "Low — 3/8 fields fresh"
  AND the 5 missing fields are identified by name
  AND this low confidence is displayed alongside (not replacing) Candidate Quality
  AND the Reviewer can see both "Candidate Quality: Moderate" AND "Data Confidence: Low"
```

### 5.10 No Live-Data Contamination Scenario

#### Scenario AC10-1: Fixture Category Enforcement

**Traceability:** AC-10 (No live-data contamination)

```
GIVEN the V0 pipeline is configured with the minimum fixture set
WHEN any fixture is loaded or displayed
THEN its fixture category (Synthetic or Historical Snapshot) is recorded
  AND the "NOT LIVE DATA — FOR V0 TESTING ONLY" marker is present on all output
  AND no fixture lacks a category label
  AND no fixture references a live data source or real-time feed
  AND the system rejects any fixture that lacks a fixture category
```

---

## 6. Scenario Traceability Matrix

| Scenario | AC-1 | AC-2 | AC-3 | AC-4 | AC-5 | AC-6 | AC-7 | AC-8 | AC-9 | AC-10 |
|---|---|---|---|---|---|---|---|---|---|---|
| AC1-1 (Evidence lineage) | ✅ | — | — | — | — | — | — | — | — | — |
| AC1-2 (Lineage through override) | ✅ | — | — | — | — | ✅ | — | — | — | — |
| AC2-1 (Reproducible run) | — | ✅ | — | — | — | — | ✅ | — | — | — |
| AC2-2 (Missing input deterministic) | — | ✅ | — | — | — | — | — | — | — | — |
| AC3-1 (Four dimensions separate) | — | — | ✅ | — | — | — | — | — | — | — |
| AC3-2 (Trade-off visible) | — | — | ✅ | ✅ | — | — | — | — | — | — |
| AC4-1 (Complete Theme Card) | — | — | — | ✅ | — | — | — | — | — | — |
| AC4-2 (Zero-candidate Theme Card) | — | — | — | ✅ | ✅ | — | — | — | — | — |
| AC5-1 (Theme-first queue) | — | — | — | — | ✅ | — | — | — | — | — |
| AC5-2 (Empty queue) | — | — | — | — | ✅ | — | — | — | ✅ | — |
| AC6-1 (Override 8 fields) | — | — | — | — | — | ✅ | — | — | — | — |
| AC6-2 (Override history) | — | — | — | — | — | ✅ | — | ✅ | — | — |
| AC8-1 (Lifecycle audit) | — | — | — | — | — | — | — | ✅ | — | — |
| AC8-2 (Point-in-time query) | — | — | — | — | — | — | — | ✅ | — | — |
| AC9-1 (Three axes scoped) | — | — | — | — | — | — | — | — | ✅ | — |
| AC9-2 (Multi-theme candidate) | — | — | — | — | — | — | — | — | ✅ | — |
| CON-1 (Contradiction visible) | ✅ | — | ✅ | ✅ | — | — | — | — | — | — |
| CON-2 (Missing evidence) | — | — | — | ✅ | — | — | — | — | — | — |
| CON-3 (Data Confidence) | — | — | ✅ | — | — | — | — | — | ✅ | — |
| AC10-1 (No live data) | — | — | — | — | — | — | — | — | — | ✅ |

**Coverage:** All 10 ACs covered by at least one scenario. Contradiction and missing-evidence cases (CON-1 through CON-3) provide additional coverage for AC-1, AC-3, AC-4, and AC-9.

---

## 7. Known-Answer Verification

For each scenario, the expected output is specified in the THEN clause. These are **known answers** that must be verified independently of the implementation:

1. **Deterministic output** — AC2-1 requires bitwise-identical outputs from two pipeline runs
2. **Structural output** — AC3-1 requires exactly 4 sections, not 1 composite score
3. **Content output** — AC4-1 requires specific fields present in Theme Card
4. **Behavioral output** — AC5-2 requires empty queue, not fabricated candidates
5. **Audit output** — AC8-1 requires specific fields in transition audit record

Verification method per scenario is specified in §8.

---

## 8. Verification Plan

### 8.1 Verification by Scenario Type

| Scenario Type | Verification Method |
|---|---|
| Deterministic output (AC2-1) | Run pipeline twice; diff outputs; assert identical |
| Structural output (AC3-1, AC4-1) | Inspect rendered output; assert section count and field presence |
| Content output (AC4-1 fields) | Assert specific strings present in output |
| Behavioral output (AC5-2) | Configure all candidates below threshold; assert queue empty + message present |
| Audit output (AC8-1) | Query audit trail; assert all required fields present and non-null |
| Point-in-time (AC8-2) | Query at two timestamps; assert different states returned |
| Negative assertion (AC10-1) | Assert no live-data markers absent; assert fixture category present on all records |

### 8.2 Independent Review

Per VERIFICATION-DOCTRINE.md, acceptance verification must include independent review:

- Reviewer must not rely solely on pipeline self-report
- Reviewer must inspect at least one raw fixture → output trace end-to-end
- For deterministic features: reviewer runs pipeline independently and compares output
- For presentation scenarios: reviewer inspects actual rendered output, not just test pass/fail

---

## 9. Decision Status

| Decision | Status |
|---|---|
| **Gate C — Fixture and Acceptance Scenarios** | ✅ **APPROVED** (Founder review 22 Jul 2026) |
| **Minimum Fixture Set (§4)** | Approved |
| **All Acceptance Scenarios (§5)** | Approved — 20 scenarios covering all 10 ACs |
| **Traceability Matrix (§6)** | Approved — full coverage confirmed |

---

## Amendment History

| Date | Change | Authority |
|---|---|---|
| 22 July 2026 | v0.1 — Initial Gate C fixture and acceptance scenarios draft | Founder Decision #19 |
| 22 July 2026 | v1.0 — Founder review complete: all fixtures and 20 scenarios approved. Gate C COMPLETE. | Founder Decision #19 |
