# Theme Model

Status: Approved Domain Specification
Version: 0.1
Owner: Founder
Authority: Approved Domain Specification subordinate to the Constitution and Founder's Decisions
Derived from: Investment Intelligence Platform Constitution v0.3
Approval: PD-v0.1-FOUNDING-DOMAIN-SPECIFICATIONS

## 1. Theme Entity

A Theme is a structural investment driver — not merely a label, sector, or folder. It is an evolving network of drivers, evidence, industries, companies, assets, supply-chain roles, and market behavior (DNA-008).

A Theme connects:

- **What** is changing (driver)
- **Why** it matters (evidence)
- **Who** is affected (entities, industries, assets)
- **Where** it is in its development (lifecycle)
- **How** certain we are (confidence)

## 2. Lifecycle

The lifecycle describes the Theme's market or economic development stage. It is independent of Approval Status, Monitoring Status, and confidence.

Lifecycle is a description of development, not a quality ranking. Each stage presents a different profile of opportunity, uncertainty, and crowding — no stage is inherently higher quality than another.

### 2.1 Stages

| # | Stage | Description |
|---|---|---|
| 1 | **Weak Signal** | Early indicators exist; no consensus; primarily anomaly-driven |
| 2 | **Formation** | Driver is forming; early entities are identifiable; evidence is structural or early operational |
| 3 | **Emerging Leadership** | Leaders and challengers are distinguishable; operational and early fundamental evidence exists |
| 4 | **Expansion** | Theme is broadening; second-order effects appear; market confirmation may begin |
| 5 | **Crowded / Late Stage** | Theme is widely recognized; crowding risk is material; fundamentals may still be strong |
| 6 | **Deterioration** | Driver is weakening; leadership is rotating or declining; evidence of structural decay |

### 2.2 Lifecycle Properties

- Lifecycle is a separate axis from Approval Status, Monitoring Status, confidence, crowding, and evidence progression.
- Lifecycle does not determine Approval Status or Monitoring Status. The governance axes transition independently of lifecycle, while valid Approval Status and Monitoring Status combinations remain constrained by §3.3.
- Lifecycle transitions are material and must be audited (see §4).
- Lifecycle is not strictly linear; reacceleration is possible but must be supported by evidence.

## 3. Governance

Theme governance is decomposed into two separate axes: Approval Status and Monitoring Status. They are independent of each other and of lifecycle, confidence, and crowding. All five axes remain separate.

### 3.1 Approval Status

Describes the Theme's position in the approval and promotion pipeline.

| # | Status | Description |
|---|---|---|
| 1 | **Detected Hypothesis** | An initial, unvetted theme proposal — may originate from anomaly or hypothesis generation |
| 2 | **Experimental** | An experimentally governed Theme that may be monitored and accumulate evidence but cannot affect official strategy output. Its origin may be AI, human-assisted, or deterministic. |
| 3 | **Under Human Review** | Actively being evaluated by the Founder for promotion to Approved |
| 4 | **Approved** | Human-approved as eligible for official strategy context. Monitoring activity is governed separately by Monitoring Status. Approval is not a buy recommendation or investment endorsement. |
| 5 | **Rejected** | Reviewed and declined; retains history and rationale |

### 3.2 Monitoring Status

Describes the Theme's operational monitoring state. Independent of Approval Status — Experimental and Under Human Review Themes may have Active Monitoring.

| # | Status | Description |
|---|---|---|
| 1 | **Not Monitored** | The Theme is not under active monitoring |
| 2 | **Active Monitoring** | The Theme receives ongoing monitoring, evidence updates, and candidate assessment |
| 3 | **Dormant** | A Theme that is not currently active but may be reactivated; history and evidence are preserved |
| 4 | **Archived** | Retired from active consideration; retains full history; may be reopened with a new review event |

### 3.3 Governance Rules

**Approval:**

- Any transition to Approved requires explicit Founder approval (not only Experimental → Approved).
- Approval means eligible for official strategy context. Monitoring activity is governed separately by Monitoring Status. Approval is **not** a buy recommendation, investment endorsement, capital-allocation decision, or declaration that the hypothesis is proven (Constitution §6).
- Experimental Themes may appear in separated experimental views without affecting official rankings, filters, scores, or alerts.

**Valid Approval Status + Monitoring Status combinations:**

The axes transition independently, but valid combinations are constrained by governance rules:

| Approval Status | Valid Monitoring Status values |
|---|---|
| **Detected Hypothesis** | Normally Not Monitored |
| **Experimental** | Not Monitored, Active Monitoring |
| **Under Human Review** | Not Monitored, Active Monitoring |
| **Approved** | Not Monitored, Active Monitoring, Dormant, Archived |
| **Rejected** | Normally Not Monitored or Archived. A Rejected Theme must be reopened into Experimental or Under Human Review before Active Monitoring resumes. |

These are domain semantics, not database cardinalities.

**Transition rules:**

- Rejected themes are not silently deleted. History is preserved.
- Reopening an Archived or Rejected theme creates a new review event and requires explicit approval.
- Both Approved and Rejected Themes may be Archived while history is preserved.
- Approval Status, Monitoring Status, lifecycle, confidence, and crowding remain five separate axes.

## 4. Transition Audit

Every material lifecycle, Approval Status, or Monitoring Status transition must record (Constitution §5):

| Field | Description |
|---|---|
| Prior state | The state before transition (with axis: lifecycle, approval, or monitoring) |
| New state | The state after transition |
| Reason | Human-readable explanation for the transition |
| Evidence references | Links to supporting evidence for the transition |
| Actor | Who authorized or triggered the transition |
| Timestamp | When the transition occurred |
| Rule or workflow version | The version of the rule or workflow governing this transition |

Lifecycle, Approval Status, and Monitoring Status are separate axes. A transition in one does not automatically change the others.

## 5. Discovery Paths

Theme discovery may follow four paths (DNA-006). Discovery is fully deferred to V1+ except for manual theme configuration in V0.

| Path | Description | Version |
|---|---|---|
| **Top-down** | Starting from macro, policy, technology, or structural trends | V1 (human-assisted / deterministic), V1.5 (AI-driven) |
| **Bottom-up** | Starting from anomalous asset behavior, earnings surprises, or sector rotation | V1 (human-assisted / deterministic), V1.5 (AI-driven) |
| **Event-driven** | Triggered by specific events: regulatory change, breakthrough, supply shock, geopolitical shift | V1 (human-assisted / deterministic), V1.5 (AI-driven) |
| **Change-driven** | Triggered by rate-of-change signals: acceleration, deceleration, reversal | V1 (human-assisted / deterministic), V1.5 (AI-driven) |

V0 uses only manually configured, Founder-approved themes. V1 enables all four discovery paths through human-assisted or deterministic processes; V1.5 adds AI-driven automation.

## 6. Weak Signal Inbox

The Weak Signal Inbox has two layers (Constitution §7). The model is defined now; implementation is deferred to V1.

### 6.1 Unexplained Anomalies

The system has detected meaningful change but lacks a credible explanation.

Properties:

- Detected signal (what changed)
- Magnitude and context
- Related entities (if identifiable)
- Timestamp of detection
- Status: unresolved

The system must **not** fabricate explanations merely to eliminate uncertainty.

### 6.2 Theme Hypotheses

The system can propose a driver, related entities, and a preliminary evidence structure.

Properties:

- Proposed driver (the explanation)
- Related entities (companies, industries, assets)
- Preliminary evidence (supporting and contradicting)
- Proposed lifecycle stage
- Proposed confidence
- Relationship to existing Themes (parent, child, related)
- Typical governance progression (not exhaustive): Detected Hypothesis → Experimental → Under Human Review → Approved or Rejected. A Detected Hypothesis may be rejected before experimentation; an Experimental Theme may remain Experimental under Active Monitoring without entering human review; and Under Human Review may return to Experimental when additional evidence is required.

## 7. Theme Card

A Theme Card is the primary presentation of a Theme for human review. It contains (Constitution §5; Theme Intelligence operational file):

- **Why now:** The case for attention at this moment
- **Supporting evidence:** Evidence that supports the theme thesis
- **Contradicting evidence:** Evidence that challenges or contradicts the thesis
- **Missing evidence:** What we need but do not yet have
- **Alternative explanations:** Other drivers that could explain the same observations
- **Lifecycle:** Current stage and transition history
- **Confidence:** Current confidence assessment
- **Crowding:** How widely recognized the theme is
- **Approval Status:** Current approval status and history
- **Monitoring Status:** Current monitoring status and history
- **Leaders:** Confirmed Leaders within the theme
- **Challengers:** Emerging Challengers within the theme
- **Beneficiaries:** Direct Beneficiaries, Enablers, Bottleneck Owners, Second-order Beneficiaries
- **Watchlist members:** Candidates being monitored

## 8. Confidence

Confidence is a separate axis from lifecycle, Approval Status, and Monitoring Status.

It reflects the platform's assessment of how well the theme is supported by evidence, considering:

- Quantity and quality of supporting evidence
- Presence and materiality of contradicting evidence
- Source independence and diversity
- Evidence progression stage
- Gaps in missing evidence

Exact confidence dimensions and measurement are deferred (OPEN-QUESTIONS.md). The model must support confidence as a separate, versioned property.

## 9. Version Boundaries for Theme Capabilities

| Capability | V0 | V0.5 | V1 | V1.5 | Later |
|---|---|---|---|---|---|
| Manual theme creation and configuration | ✅ | ✅ | ✅ | ✅ | ✅ |
| Lifecycle tracking and transitions | ✅ | ✅ | ✅ | ✅ | ✅ |
| Approval Status and Monitoring Status (separate axes) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Theme Card rendering | ✅ | ✅ | ✅ | ✅ | ✅ |
| Weak Signal Inbox — Unexplained Anomalies | — | — | ✅ | ✅ | ✅ |
| Weak Signal Inbox — Theme Hypotheses | — | — | ✅ | ✅ | ✅ |
| Experimental Theme tracking | — | — | ✅ | ✅ | ✅ |
| Human-assisted / deterministic discovery (all 4 paths) | — | — | ✅ | ✅ | ✅ |
| AI-driven hybrid discovery | — | — | — | ✅ | ✅ |
| Learning from theme outcomes | — | — | — | — | ✅ |
