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
