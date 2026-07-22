# Theme Intelligence

## Purpose

Discover and track structural drivers across companies, industries, supply chains, ETFs, commodities, policy, technology, and market behavior.

## Lifecycle

1. Weak Signal
2. Formation
3. Emerging Leadership
4. Expansion
5. Crowded / Late Stage
6. Deterioration

## Separate Axes

- lifecycle;
- confidence;
- Approval Status;
- Monitoring Status;
- crowding;
- evidence progression.

## Approval Status

The Theme's position in the approval and promotion pipeline.

- Detected Hypothesis
- Experimental
- Under Human Review
- Approved
- Rejected

## Monitoring Status

The Theme's operational monitoring state. Independent of Approval Status.

- Not Monitored
- Active Monitoring
- Dormant
- Archived

Experimental and Under Human Review Themes may have Active Monitoring. Monitoring does not grant official strategy eligibility. Approval does not automatically activate monitoring.

## Valid Approval Status + Monitoring Status Combinations

| Approval Status | Valid Monitoring Status values |
|---|---|
| Detected Hypothesis | Not Monitored |
| Experimental | Not Monitored, Active Monitoring |
| Under Human Review | Not Monitored, Active Monitoring |
| Approved | Not Monitored, Active Monitoring, Dormant, Archived |
| Rejected | Not Monitored, Archived |

Default governance expectations:

- A Detected Hypothesis normally begins as Not Monitored.
- A Rejected Theme normally remains Not Monitored or Archived.

A Rejected Theme must be reopened into Experimental or Under Human Review before Active Monitoring resumes.

These are domain semantics, not database cardinalities.

## Discovery Paths

- top-down;
- bottom-up;
- event-driven;
- change-driven.

## Weak Signal Inbox

- Unexplained Anomalies
- Theme Hypotheses

## Autonomy

Experimental Themes may be created and tracked automatically. They cannot alter official strategy outputs before Human Approval.

Experimental Themes may originate from AI, human-assisted, or deterministic discovery.

Experimental and Under Human Review Themes may have Active Monitoring without affecting official strategy rankings, filters, scores, or approved-strategy alerts.

## Research Presentation

Theme Cards contain:

- why now;
- supporting evidence;
- contradicting evidence;
- missing evidence;
- alternative explanations;
- lifecycle;
- confidence;
- crowding;
- Approval Status;
- Monitoring Status;
- leaders;
- challengers;
- beneficiaries;
- watchlist members.

## Minimum Transition Audit

Lifecycle, Approval Status, and Monitoring Status remain separate axes.

Every material transition records:

- prior state;
- new state;
- reason;
- evidence references;
- actor;
- timestamp;
- rule or workflow version.

Rejected, dormant, archived, or reopened themes retain history.

Any transition to Approved requires explicit Founder approval.

Human approval is required before a theme becomes eligible for official strategy context.

Theme approval is not investment approval.

## Coverage Gap Detection (Blind Spot Discovery)

The platform shall proactively identify what the Founder may have overlooked — candidates, risks, or themes that are present in the evidence but absent from the Watchlist or active monitoring.

### Detection Triggers

Coverage gap detection runs:

- After every material pipeline run
- When a new Theme is approved (cross-reference against existing Watchlist)
- When an existing Theme shows strengthening evidence but no corresponding Watchlist additions
- When a sector or industry shows leadership breadth but the Watchlist has thin or zero coverage

### Gap Types

| Gap Type | Description | Action |
|---|---|---|
| **Theme Coverage Gap** | An Approved Theme with strong evidence but zero or thin Candidate coverage in the Watchlist | Surface to Founder: "This theme is strengthening but you have no candidates tracking it." |
| **Candidate Blind Spot** | A Candidate that repeatedly appears in evidence across multiple approved themes but is absent from the Watchlist | Surface to Founder with evidence summary and thesis prompt |
| **Sector Blind Spot** | A sector or industry with improving breadth, relative strength, or fundamental momentum but no approved Theme or Watchlist coverage | Propose a new Experimental Theme or prompt Founder review |
| **Risk Blind Spot** | A risk factor (regulatory, competitive, macro) that appears in evidence across multiple Candidates or Themes but is not tracked in any thesis's key_risks | Add to relevant theses or surface as a cross-cutting concern |

### Rules

- Coverage gap detection is AI-assisted discovery, not automated decision-making. Gaps are surfaced for Founder review, never silently acted upon.
- Gap detection must reference specific evidence, not vague impressions.
- A detected gap does not create an obligation to act — the Founder may consciously choose to leave a gap uncovered.
- Gap detection results are included in the self-reflection log for traceability.

## Emergent Rule Discovery

As the AI operates across multiple pipeline runs, reviews self-reflection logs, and observes patterns in thesis outcomes, it may identify recurring heuristics, decision patterns, or potential rules that are not yet codified in any approved strategy document.

### Proposal Channel

The AI may propose an emergent rule through a structured proposal:

| Field | Description |
|---|---|
| **proposed_rule** | The rule or heuristic in plain language (e.g., "Trim any position exceeding 11% of portfolio to fund new high-conviction candidates") |
| **originating_pattern** | What recurring observation, mistake, or success prompted this proposal. Reference specific runs, theses, or outcomes. |
| **evidence** | Supporting evidence from pipeline history, self-reflection logs, or thesis outcomes |
| **counterevidence** | Known cases where the rule would have produced a worse outcome |
| **scope** | What contexts the rule applies to (specific strategy, all strategies, specific market regime) |
| **interaction** | How the rule interacts with existing approved rules — does it extend, constrain, or conflict? |

### Rules

- Emergent rules are proposals, not authority. They have no effect until Founder approves them.
- Proposals enter the same change-control pipeline as other amendments: draft → review → Founder approval → codification.
- The AI must not silently apply an emergent rule before approval.
- Rejected proposals are archived with rationale; they may be resubmitted if new evidence emerges.
- Emergent rule proposals are distinct from Weak Signal anomalies: anomalies are unexplained observations; emergent rules are proposed codifications of observed patterns.
