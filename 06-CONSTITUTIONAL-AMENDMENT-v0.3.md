# Constitutional Amendment v0.3

## Status

**Founder-approved**

## Approval Statement

The Founder approved Material Change Proposal CA-v0.3-THEME-GOVERNANCE-AXES, authorizing amendment of the Investment Intelligence Platform Constitution and the operational documents listed below.

## Purpose

Decompose the flat Theme governance-state list into two separate, independently transitioning axes: Approval Status and Monitoring Status.

## Problem Addressed

The prior governance model combined approval-pipeline states (Detected Hypothesis, Experimental, Under Human Review, Approved, Rejected) and operational monitoring states (Actively Tracked, Dormant, Archived) in one flat list. This created semantic ambiguity: Experimental and Under Human Review Themes could be actively monitored without being Approved; Approved Themes could be Not Monitored; Rejected Themes could be Archived while preserving their rejection history; and eligibility for official strategy context was conflated with monitoring activity.

## Approved Semantic Changes

### Constitution §5 — Theme Intelligence

Theme governance is represented by two separate axes:

**Approval Status:** Detected Hypothesis, Experimental, Under Human Review, Approved, Rejected

**Monitoring Status:** Not Monitored, Active Monitoring, Dormant, Archived

Approval Status and Monitoring Status are independent of lifecycle, confidence, and crowding. A transition in one axis does not automatically change another axis, while valid combinations remain governed by approved domain rules.

Valid-combination semantics:

- Detected Hypothesis: normally Not Monitored.
- Experimental: Not Monitored or Active Monitoring.
- Under Human Review: Not Monitored or Active Monitoring.
- Approved: Not Monitored, Active Monitoring, Dormant, or Archived.
- Rejected: normally Not Monitored or Archived. Active Monitoring requires reopening into Experimental or Under Human Review.

Experimental and Under Human Review Themes may be actively monitored without affecting official strategy rankings, filters, scores, or approved-strategy alerts.

Archiving does not erase approval history or rejection history.

### Constitution §6 — Two-Tier Autonomy

Experimental Themes may originate from AI, human-assisted, or deterministic discovery. They may have Active Monitoring without affecting official strategy outputs.

An Approved Theme is eligible for official strategy context. Monitoring activity is governed separately by Monitoring Status.

Approval is not a buy recommendation, investment endorsement, capital-allocation decision, or declaration that the hypothesis is proven.

### Every material transition

Must record the prior value, new value, reason, evidence references, actor, timestamp, and relevant rule or workflow version. Any transition to Approved requires explicit Founder approval.

## Affected Authoritative Documents

| Document | Change |
|---|---|
| `02-PROJECT-CONSTITUTION.md` | Header v0.2→v0.3; §5 rewritten with two-axis governance; §6 revised; Amendment Record v0.3 appended |
| `operational/THEME-INTELLIGENCE.md` | Governance section decomposed into Approval Status + Monitoring Status; valid-combination rules added; transition audit updated; Experimental Theme origin clarified |
| `operational/DOMAIN-GLOSSARY.md` | Governance State replaced with Approval Status + Monitoring Status; Experimental Theme and Approved Theme entries revised |
| `03-OPERATIONAL-DOCUMENTS-INDEX.md` | Amendment added to Governance History |
| `README.md` | Foundation v0.2→v0.3; history entry added |
| `06-CONSTITUTIONAL-AMENDMENT-v0.3.md` | This file — created |

## Product Impact

This amendment clarifies Theme governance semantics without changing:

- the product mission;
- Theme Intelligence philosophy;
- Two-Tier Autonomy;
- Alpha Momentum direction;
- Close System boundary;
- V0 scope;
- official investment-decision authority.

Monitoring activity is no longer conflated with official approval. Approval eligibility is no longer conflated with active monitoring.

## Data and Migration Impact

- No database exists.
- No schema or migration is authorized by this amendment.
- No production data exists.
- Future implementations must model Approval Status and Monitoring Status separately.
- Existing Project Definition drafts (under `project-definition/`) already reflect the approved two-axis model.

## Security and Privacy Impact

No new security, privacy, secret-handling, retention, or access risk is introduced.

## Verification Requirements

Per `operational/VERIFICATION-DOCTRINE.md`:

- Confirm only the six authorized files changed or were created.
- Confirm all old flat governance-state wording is removed from current authoritative definitions.
- Confirm Approval Status and Monitoring Status values are identical across the Constitution, Theme Intelligence, and Domain Glossary.
- Confirm Experimental Themes may have Active Monitoring.
- Confirm Monitoring Status does not grant official strategy eligibility.
- Confirm Approval does not automatically activate monitoring.
- Confirm Rejected Themes must reopen before Active Monitoring.
- Confirm amendment history is recorded.
- Confirm `project-definition/` files remain unchanged.
- Run documentation verification.
- Report Git status and focused diff summary.

## Rollback Point

The `foundation-v0.2` Git tag is the rollback point.

## Unresolved Decisions

Canonical Theme-role ownership (whether structural Theme roles belong to Entity–Theme relationships, Candidate–Theme relationships, or a layered combination) remains an **explicit pending Founder decision**. This amendment does not resolve or alter that issue.

## Next Gate

Complete independent diff review, then commit only the six authorized amendment files and tag `foundation-v0.3`. The `project-definition/` documents remain untracked Drafts for Founder Review and require a separate approval and commit.
