# Alpha Momentum V0 Design Plan

Status: Approved Stable Design Plan
Version: 0.1
Owner: Founder
Authority: Approved stable phase-governance plan subordinate to the Constitution, Founder's Decisions, and Approved Domain Specifications; changes require an explicitly approved named amendment
Derived from: Constitution v0.3 and Project Definition v0.1
Plan Approval: AM-V0-DESIGN-PLAN-v0.1
Repository Acceptance: AM-V0-FIRST-TRANCHE-REPOSITORY-ACCEPTANCE-v0.1

## 1. Phase Objective

The Alpha Momentum V0 Design phase produces decision slots, contracts, controlled themes, fixtures, and acceptance criteria that will govern the Alpha Momentum V0 implementation.

The project enters Alpha Momentum V0 Design through explicit Founder approval of AM-V0-DESIGN-PLAN-v0.1.

V0 must prove an end-to-end Alpha Momentum slice using controlled data and predefined themes, demonstrating evidence lineage, deterministic features, separated quality dimensions, Theme Cards, a research queue, human feedback, reproducibility, and historical state changes (Constitution §20).

## 2. Permitted Scope

This design phase may:

- Define decision slots, required questions, decision obligation sources, and rule content authorities for every future investment-domain rule.
- Define rule-contract field templates and Reference Cohort Contract templates.
- Define pipeline stage contracts, queue assembly contracts, and enrichment vs. gate classification.
- Define Data Confidence semantics, point-in-time contracts, and public-availability semantics.
- Define Theme Card presentation requirements and human-review flow contracts.
- Define technology-neutral fixture shapes, synthetic and historical snapshot categories, and acceptance scenarios.
- Propose a controlled Theme set for Founder approval.
- Create ADRs when a real cross-cutting design decision arises.
- Record all decisions, their status, their decision obligation sources, and their rule content authorities in a living traceability register.

This design phase must not define rule content unless an explicit approved Rule Content Authority supplies that content. When no approved content source exists, the slot remains Status: Proposed with Resolution: UNRESOLVED — FOUNDER DECISION REQUIRED. This applies equally to Founder-provided rules, explicitly specified approved documents, adopted external doctrines, and approved V0 experiment assumptions.

## 3. Prohibited Scope

This design phase must not:

### 3.1 Investment Rule Invention

Must not invent or propose as defaults:

- Numeric thresholds
- Weights
- Formulas
- Lookback periods
- Benchmarks
- Sector or industry taxonomies
- Reference cohorts
- Queue ordering
- Tie-breakers
- Eligibility rules (beyond those in approved specifications)
- Fallback investment logic
- Missing-data substitution
- Scoring aggregation
- Pass/fail boundaries
- Lifecycle-to-strategy mappings
- Illustrative numeric examples that could be mistaken for proposed rules

### 3.2 Technology and Data

Must not:

- Select a technology stack
- Create schemas, migrations, ORM models, or persistence designs
- Install dependencies
- Write application code
- Access live or current market feeds
- Access production ingestion pipelines
- Access broker or private-account data
- Access private positions or transactions
- Access unapproved licensed data
- Create application state
- Populate fixtures or access external data (fixture shapes may be defined; fixture population requires separate authorization)

### 3.3 Repository Integrity

Must not:

- Create, modify, move, rename, or delete any file outside `design/alpha-momentum-v0/`
- Modify AGENTS.md, Founder's Decisions, Roadmap, or any authoritative document
- Modify foundation documents
- Modify project-definition/ files
- Modify Hermes configuration, memory, or skills
- Access the quarantine directory
- Access the legacy repository or archive (except through a separately authorized Legacy Knowledge Salvage)

Git mutation policy:

- No agent may autonomously stage, commit, tag, restore, reset, clean, or otherwise mutate Git state.
- Every Git mutation requires a separate exact named Founder authorization identifying the files and operation.
- Destructive reset, clean, or history rewriting remains prohibited unless a specifically approved recovery operation requires it.
- Approved gate artifacts may later be committed or checkpointed only through such separate authorization.

## 4. Deliverable Map

| # | File | Type | Gate |
|---|---|---|---|
| 1 | `README.md` | Approved Design Area Index | Plan Approval |
| 2 | `DESIGN-PLAN.md` | Approved Stable Design Plan | Plan Approval |
| 3 | `TRACEABILITY-AND-DECISION-REGISTER.md` | Living Register | All gates (continuously updated) |
| 4 | `RULE-PACK-AND-QUALITY-CONTRACTS.md` | Decision Slots | Gate A |
| 5 | `DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md` | Decision Slots | Gate A |
| 6 | `PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md` | Decision Slots | Gate A |
| 7 | `CONTROLLED-THEME-SET.md` | Gate B Artifact | Gate B |
| 8 | `THEME-CARD-AND-HUMAN-REVIEW-FLOW.md` | Decision Slots | Gate C |
| 9 | `FIXTURE-AND-ACCEPTANCE-SCENARIOS.md` | Acceptance Criteria | Gate C |
| 10 | `ADRs/` | On-Demand | Reviewed at the affected gate |

## 5. Dependency Order

```
Step 1: README.md + DESIGN-PLAN.md
    │  (No dependencies — drafted together as first tranche)
    │
    ▼
Step 2: TRACEABILITY-AND-DECISION-REGISTER.md
    │  (Depends on DESIGN-PLAN.md for gate and materiality structure)
    │
    ▼
Step 3: RULE-PACK-AND-QUALITY-CONTRACTS.md
    │  DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md
    │  PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md
    │  (Independent of each other; all depend on DESIGN-PLAN.md + TRACEABILITY register;
    │   Rule-Pack may reference Data-Confidence but must not redefine it)
    │
    ▼
─── GATE A ─── Founder reviews and approves core contract questions and decision slots
    │
    ▼
Step 4 (Optional): Legacy Knowledge Salvage
    │  (Separate named read-only authorization required;
    │   occurs after Gate A, before Gate B)
    │
    ▼
Step 5: CONTROLLED-THEME-SET.md
    │  (Depends on Gate A completion; may be informed by Legacy Salvage)
    │
    ▼
─── GATE B ─── Founder approves Theme definitions for V0 design and fixtures
    │
    ▼
Step 6: THEME-CARD-AND-HUMAN-REVIEW-FLOW.md
    │  FIXTURE-AND-ACCEPTANCE-SCENARIOS.md
    │  (Depend on CONTROLLED-THEME-SET.md approval;
    │   FIXTURE must not be finalized before CONTROLLED-THEME-SET is approved)
    │
    ▼
─── GATE C ─── Founder approves Human Review flow, fixtures, and acceptance scenarios
    │
    ▼
Step 7: Any required ADRs (may also be proposed earlier if a cross-cutting decision arises)
    │  Updated TRACEABILITY-AND-DECISION-REGISTER.md
    │
    ▼
─── GATE D ─── Design completion and implementation readiness
```

## 6. Gate A–D Structure

### Plan Approval: AM-V0-DESIGN-PLAN-v0.1

**Materiality:** Material phase-governance decision.

**Approves:**
- Phase transition into Alpha Momentum V0 Design
- File plan (which artifacts, their names, their purposes)
- Permitted and prohibited scope
- Dependency order
- Gate A–D structure
- Materiality policy
- Legacy Salvage insertion window
- Rule-authority requirements
- Unresolved-decision controls

**Does not approve:** Any future artifact content, any investment rule, any threshold, weight, formula, benchmark, taxonomy, cohort, theme selection, fixture, ADR, technology, schema, migration, dependency, or implementation.

### Gate A — Core Contract Questions and Decision Slots

**Artifacts under review:**
- `RULE-PACK-AND-QUALITY-CONTRACTS.md`
- `DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md`
- `PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md`
- `TRACEABILITY-AND-DECISION-REGISTER.md` (as evidence of completeness)

**Gate A must:**
- Identify every Founder decision required before deterministic V0 behavior can be approved
- Define all decision slots with required rule-contract fields
- Classify each decision as material or non-material
- Mark every unresolved investment-domain rule slot with Status: Proposed, Resolution: UNRESOLVED — FOUNDER DECISION REQUIRED

**Gate A must not:** Populate invented investment rules, thresholds, weights, formulas, lookback periods, benchmarks, or cohorts.

**Gate A does not:** Approve or amend DESIGN-PLAN.md. Gate A reviews the core contract question and decision-slot artifacts.

### Optional: Legacy Knowledge Salvage

- Requires a separate named read-only authorization.
- Does not block the start of V0 Design.
- Occurs after Gate A core contracts are drafted and before Gate B controlled Theme approval.
- May inform: Theme candidates, relationship examples, fixture realism, historical failure cases.
- May not establish: architecture, investment rules, weights, thresholds, benchmarks, or implementation requirements.
- All outputs must be labeled: UNTRUSTED HISTORICAL INPUT — NOT AUTHORITY.
- No legacy output may override, narrow, or substitute for an approved authority document.

### Gate B — Controlled Theme Set

**Artifact:** `CONTROLLED-THEME-SET.md`

**Approves:** Theme definitions for inclusion in the controlled V0 design and fixture set.

**Theme selection criteria** (from ALPHA-MOMENTUM-V0-SPEC §3.1):
1. Structural driver (economic, technological, policy, or demographic — not short-term catalyst)
2. Identifiable beneficiaries in the US-listed universe
3. Sufficient public-domain evidence for realistic V0 fixtures
4. Domain coverage (testability, evidence diversity, lifecycle coverage, relationship-role coverage)

**This approval is not:** A buy recommendation, investment endorsement, or runtime entity creation.

### Gate C — Human Review, Fixtures, and Acceptance Scenarios

**Artifacts:**
- `THEME-CARD-AND-HUMAN-REVIEW-FLOW.md`
- `FIXTURE-AND-ACCEPTANCE-SCENARIOS.md`
- Any required ADRs
- Updated `TRACEABILITY-AND-DECISION-REGISTER.md`

**Gate C must:**
- Demonstrate traceability from every acceptance scenario to the 10 approved V0 acceptance criteria (ALPHA-MOMENTUM-V0-SPEC §6)
- Cover contradiction and missing-evidence cases
- Distinguish presentation decisions from material human-authority decisions
- Not finalize fixtures before CONTROLLED-THEME-SET.md is approved

### Gate D — Design Completion and Implementation Readiness

**All of the following must be satisfied:**

1. All material rules explicitly approved
2. No unresolved decision affecting observable V0 output
3. Full traceability from every rule to its authority source
4. Acceptance scenarios complete and traceable to all 10 ACs
5. Independent review complete (per VERIFICATION-DOCTRINE.md)
6. No technology or implementation commitments made
7. Explicit Founder approval for transition to implementation (Phase 3)

## 7. Materiality Policy

### Plan Approval Materiality

Approval of AM-V0-DESIGN-PLAN-v0.1 is a material phase-governance decision.

### Content-Based Materiality

For design content, a decision is material if it changes or establishes:

| Domain | Examples |
|---|---|
| Domain definitions or invariants | What constitutes a Theme, Candidate, Evidence record, or quality dimension |
| Strategy eligibility | What assets qualify for Alpha Momentum screening |
| Filtering | Whether Theme relationships act as filters, enrichment, or ranking inputs |
| Ranking | What makes a Candidate higher or lower priority |
| Queue behavior | Ordering, adaptive capacity thresholds, empty-state rules |
| Thresholds | Any numeric boundary |
| Weights | Any relative importance assignment |
| Formulas | Any computation producing a score or signal |
| Evidence semantics | What counts as independent, fresh, stale, or contradictory |
| Point-in-time behavior | What data is visible at a given evaluation timestamp |
| Missing-data behavior | What happens when expected data is absent |
| Human-review visibility | What the Founder sees vs. what is computed but hidden |
| Override semantics | What an override preserves, hides, or changes |
| Shared Platform vs. strategy ownership | Whether a capability belongs to Shared Core or Alpha Momentum |

**Non-material** (may be clarified without a material-change proposal): clarifications, indexing, file organization, and presentation details — only when they add no new obligation or observable behavior.

## 8. Amendment Process

### ADR Policy

- ADRs may be proposed whenever a genuine cross-cutting design decision arises — they are not restricted to any single gate.
- An ADR is reviewed at the gate affected by that decision.
- No ADR is pre-created.
- No ADR is authorized in the first tranche.
- Each ADR is material or non-material according to its actual impact, not because it is an ADR.

### Stable Artifacts

After explicit Founder acceptance following independent diff review, DESIGN-PLAN.md becomes a stable artifact. It may change only through an explicitly approved named amendment following `operational/CHANGE-CONTROL-AND-APPROVAL.md`.

After their respective gate approvals, CONTROLLED-THEME-SET.md, RULE-PACK-AND-QUALITY-CONTRACTS.md (once rules are populated), and FIXTURE-AND-ACCEPTANCE-SCENARIOS.md also become stable.

### Living Artifacts

TRACEABILITY-AND-DECISION-REGISTER.md is a living register. Entries are continuously updated as decisions are proposed, approved, deferred, or rejected. Updating a Proposed entry does not approve it — it records the proposal. Approval requires a separate explicit Founder decision with a named approval reference.

### Required Amendment Proposal Format

Per CHANGE-CONTROL-AND-APPROVAL.md, material changes require:
1. Change title and identifier
2. Problem statement
3. Affected authoritative documents
4. Proposed behavior
5. Alternatives considered
6. Domain and user impact
7. Data and migration impact
8. Security and privacy impact
9. Verification plan
10. Rollback or recovery plan
11. Unresolved risks
12. Exact approval requested

## 9. Legacy Salvage Insertion Window

1. Legacy Knowledge Salvage is not implicitly authorized by this plan.
2. It requires a separate named read-only authorization.
3. It does not block the start of V0 Design.
4. Insertion window: after Gate A core contracts are drafted, before Gate B controlled Theme approval.
5. Permitted influence: Theme candidates, relationship examples, fixture realism, historical failure cases.
6. Prohibited influence: architecture, investment rules, weights, thresholds, benchmarks, implementation requirements.
7. Output label required: UNTRUSTED HISTORICAL INPUT — NOT AUTHORITY.
8. No legacy output may override, narrow, or substitute for an approved authority document.

## 10. Decision-Slot Template

Every unresolved investment-domain rule slot in planning-stage artifacts must use this structure:

```
### Decision Slot: [DS-XXX] — [Short Topic Name]

- **Identifier:** DS-XXX
- **Topic:** [What must be decided]
- **Affected Artifact(s):** [Which design file(s) this decision constrains]
- **Decision Obligation Source:** [The approved document explaining why the decision must exist]
- **Rule Content Authority:** [The approved source that explicitly supplies the content of the rule. If none exists: NONE]
- **Decision Category:** [Filter | Rank | Weight | Threshold | Cohort | Formula | Period | Taxonomy | Eligibility | Fallback | Other]
- **Materiality:** [Material | Non-material] — rationale
- **Required Rule-Contract Fields:** [Which fields from the Rule Contract template apply]
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Dependencies:** [Which other decision slots this one depends on]
- **Alternatives Considered:** [Describe alternatives without proposing a default]
- **Known Risks if Deferred:** [What breaks or remains undefined]
- **Approval Reference:** (blank until Founder approves)
- **Verification Evidence:** (blank until populated)
```

**Definitions:**

- **Decision Obligation Source:** The approved document explaining *why* the decision must exist (e.g., Constitution §13 requires Candidate Quality assessment; this creates an obligation to define its dimensions).
- **Rule Content Authority:** The approved source that explicitly supplies the *content* of the rule (e.g., the Founder provides a specific threshold; an approved domain specification explicitly states a formula; an adopted external doctrine supplies a specific rule).

An approved Constitution or Domain Specification may serve as Rule Content Authority only when it explicitly specifies the relevant rule content. A document that merely requires a dimension, assessment, or decision does not authorize AI to invent its rule.

When no approved content source exists, use:

- **Rule Content Authority:** NONE
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED

## 11. Rule-Authority Requirements

### Two Distinct Authority Fields

Every decision slot must distinguish:

- **Decision Obligation Source:** Why the decision must exist (the approved document creating the obligation).
- **Rule Content Authority:** What supplies the rule's content (the approved source providing the specific rule, threshold, formula, or definition).

An obligation to assess a dimension does not authorize AI to invent its measurement. Only an explicit content source may supply rule content.

### Permitted Rule Content Authorities

For every future investment-domain rule slot, the Rule Content Authority must be one of:

| # | Authority Source | Example | Notes |
|---|---|---|---|
| 1 | **Founder-provided rule** | A specific rule, threshold, or formula provided by the Founder during design | Rule Content Authority only when the Founder explicitly supplies the content |
| 2 | **Existing approved Constitution or Domain Specification** | ALPHA-MOMENTUM-V0-SPEC §3.1 for Theme selection criteria — only when the exact approved criterion itself is being applied | An approved Constitution or Domain Specification is Rule Content Authority only for the exact rule content it explicitly specifies. If it merely creates an obligation to define a rule, it is only the Decision Obligation Source. |
| 3 | **Approved external doctrine explicitly adopted by the Founder** | An O'Neil, Minervini, or Momentum Masters reference after explicit Founder adoption | Treated as untrusted external content until explicitly adopted |
| 4 | **Explicitly approved V0 experiment assumption** | A time-boxed, labeled assumption approved for V0 demonstration only | Must carry explicit V0-experiment labeling

If none of these four authorities exists, the slot must be marked with Status: Proposed, Resolution: UNRESOLVED — FOUNDER DECISION REQUIRED.

### External Doctrine Adoption Rules

An external investment doctrine is not authority merely because it is named. Before adoption it must be:

1. Identified by exact source, edition, section, or rule
2. Treated as untrusted external content
3. Checked against the Constitution and approved specifications
4. Explicitly adopted by the Founder through a named approval

### Unresolved Decision Behavior

An unresolved slot must result in one of:

- Explicit Unknown or Not Assessable state
- Deterministic Founder-approved fallback
- Explicit failure or exclusion behavior
- Blocking the affected output until a decision is approved

No AI-generated placeholder behavior is permitted.

## 12. Reference Cohort Contract Template

Any future relative rule (e.g., "top quartile," "above sector median") must define a Reference Cohort Contract:

```
### Reference Cohort Contract: [RC-XXX]

- **Cohort or Universe Definition:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Evaluation Timestamp:** [When the cohort is evaluated relative to the candidate]
- **Public-Availability Cutoff:** [Point-in-time constraint]
- **Minimum Valid Sample Size:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Tie Behavior:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Missing-Value Behavior:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Universe-Change Behavior:** [What happens when the cohort composition changes]
- **Survivorship Treatment:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Revision or Vintage Behavior:** [How restated data is handled]
```

A relative rule remains unresolved until all fields are approved. Do not choose any cohort now.

## 13. Higher-Authority Escalation

If any proposed design decision would change, narrow, contradict, or extend:

- The Constitution
- Founder's Decisions
- An Approved Domain Specification
- An approved lifecycle, governance, evidence, or human-authority rule

Stop that decision path and record:

> UPSTREAM AMENDMENT REQUIRED

The change cannot be approved merely through Gate A, B, C, or D. It requires the applicable material-change and authority-amendment process first.

## 14. Risks and Failure Controls

### Primary Risks

| Risk | Control |
|---|---|
| **Rule invention:** AI populating unresolved slots with plausible defaults | Every slot must cite one of four authorities or be marked UNRESOLVED — FOUNDER DECISION REQUIRED |
| **Premature stack selection:** Designing to fit an assumed technology | Explicit prohibition in Prohibited Scope; no deferred stack decisions are resolved |
| **Scope creep:** Expanding V0 beyond what ALPHA-MOMENTUM-V0-SPEC authorizes | DESIGN-PLAN.md locks permitted and prohibited scope against the approved spec |
| **Narrative capture:** Plausible-sounding rules treated as approved | Rule-authority requirements block any rule without a traceable source |
| **Premature complexity:** Designing for V1+ before V0 is stable | Version boundaries in approved domain specs are referenced; scope is explicitly V0 |
| **Legacy contamination:** Legacy knowledge treated as authority | Mandatory label; separate authorization required; insertion window bounded |
| **Silent amendment:** Design artifacts narrowing higher-authority documents | AGENTS.md authority hierarchy enforced; UPSTREAM AMENDMENT REQUIRED escalation |
| **Unauthorized data exposure:** Accessing live or private data | Data boundary in Prohibited Scope blocks all live/private/broker data |

### Failure Controls

1. Gate structure: No artifact advances without explicit Founder approval.
2. Independent review: Per VERIFICATION-DOCTRINE.md.
3. Git checkpoint before each gate: Per CHANGE-CONTROL-AND-APPROVAL.md.
4. Unresolved-decision tracking: All unresolved slots visible in the living TRACEABILITY register.
5. No silent fill: Rule-authority requirements block AI from inventing behavior.

## 15. Verification and Rollback

### Per-Draft Verification

Every drafting action must be followed by:
1. `git status` inspection
2. Confirmation that only authorized files were created or modified
3. Content-safety check for prohibited content

### Gate Verification

Before each gate review, per VERIFICATION-DOCTRINE.md:
1. Contradiction review
2. Terminology review
3. Authority review
4. Scope and non-scope check
5. Confirmation that no code, dependency, migration, or final stack was introduced

### Design Plan Stability

DESIGN-PLAN.md becomes stable only after:
1. It is drafted from the approved plan
2. Independently reviewed
3. Explicitly accepted into the repository by the Founder

After acceptance, it may change only through an explicitly approved named amendment.

### Rollback

The baseline rollback point for the first tranche is tag `project-definition-v0.1`, resolving to commit `6f88e19`. After a separately authorized reviewed commit, that commit may become the next named checkpoint for subsequent work. No tag is created automatically. A tag or checkpoint may be created only through a separate exact named Founder authorization after the relevant artifacts pass review.

## 16. Decision Status Definitions

The TRACEABILITY-AND-DECISION-REGISTER.md uses exactly four statuses:

| Status | Meaning |
|---|---|
| **Proposed** | The decision has been identified and described but not yet approved. May carry Resolution: UNRESOLVED — FOUNDER DECISION REQUIRED |
| **Approved** | The Founder has explicitly approved the decision with a named approval reference |
| **Deferred** | The decision is intentionally postponed to a later phase |
| **Rejected** | The decision path was considered and declined; rationale is preserved |

There is no fifth "UNRESOLVED" status. "UNRESOLVED" is a Resolution value carried by a Proposed entry.

Updating the register does not approve a Proposed decision. Approval requires a separate explicit Founder decision with a named approval reference.
