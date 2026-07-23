# Emergent Rule Discovery — Template

**Status:** Operational Template  
**Version:** v0.1  
**Owner:** AI Intelligence Layer (Founder-reviewed)  
**Authority:** THEME-INTELLIGENCE.md §Emergent Rule Discovery (FD #25)  

---

## Purpose

As the AI operates across multiple pipeline runs, reviews self-reflection logs, and observes patterns in thesis outcomes, it may identify recurring heuristics, decision patterns, or potential rules that are not yet codified in any approved strategy document.

Emergent rules are **proposals**, not authority. They have no effect until Founder approves them.

---

## Proposal Pipeline

```
AI Observation → Proposal Draft → Founder Review → 
  ├── Approved → Codified in strategy document
  ├── Rejected → Archived with rationale (may resubmit if new evidence)
  └── Revision Requested → AI revises and resubmits
```

---

## Proposal Format

```markdown
# Emergent Rule Proposal: {short_title}

**Proposal ID:** ERP-{NNN}
**Status:** Draft | Under Review | Approved | Rejected
**Proposed By:** AI ({model})
**Date:** {date}
**Related Pipeline Runs:** {run_ids}

---

## Proposed Rule

{The rule or heuristic in plain language.}

**Example:** "The Research Queue should not contain more than 3 candidates from the same sector unless each candidate represents a distinct structural driver."

## Originating Pattern

{What recurring observation, mistake, or success prompted this proposal. Reference specific runs, theses, or outcomes.}

**Example:** "Across 5 pipeline runs, the Semiconductor theme (TH-004) consistently dominated the queue with 3+ candidates while other approved themes had zero or one. This reflects sector concentration risk rather than genuine breadth of opportunity."

## Supporting Evidence

{Evidence from pipeline history, self-reflection logs, or thesis outcomes that supports the rule.}

- Run AM-V0-20260720: 3/6 candidates in TH-004
- Run AM-V0-20260722: 3/6 candidates in TH-004
- Run AM-V0-20260723: 3/6 candidates in TH-004
- Coverage gap reports show TH-030 and TH-020 with zero candidates

## Counter-Evidence

{Known cases where the rule would have produced a worse outcome.}

**Example:** "In 2023, limiting semiconductor candidates would have missed NVDA's historic move. Sector concentration is sometimes justified by genuine breadth of opportunity."

## Scope

{What contexts the rule applies to.}

- [ ] Alpha Momentum V0 only
- [ ] All Momentum & Market Leadership strategies
- [ ] All strategies (Shared Core rule)
- [ ] Specific market regime: {e.g., bull market, sector rotation}

## Interaction with Existing Rules

{How the rule interacts with existing approved rules — does it extend, constrain, or conflict?}

**Example:** "This rule extends DS-508 (Show-all — no quality threshold) by adding a sector-concentration awareness check. It does not conflict with existing rules because no sector-limit rule currently exists. It constrains the Research Queue display layer only, not the pipeline."

## Implementation Impact

{What would change if this rule is approved.}

- Files affected: {list}
- Pipeline stage: {which stage, if any}
- Display impact: {what changes visually}
- Backward compatibility: {does it break existing behavior?}

## Founder Decision

- [ ] **Approve** — codify as {amendment type}
- [ ] **Reject** — archive with rationale
- [ ] **Revise** — request changes: {what to change}
```

---

## Rules

1. Emergent rules are proposals — they have no effect until Founder approves.
2. Proposals enter the same change-control pipeline as other amendments: draft → review → Founder approval → codification.
3. The AI must not silently apply an emergent rule before approval.
4. Rejected proposals are archived with rationale; they may be resubmitted if new evidence emerges.
5. Emergent rule proposals are distinct from Weak Signal anomalies: anomalies are unexplained observations; emergent rules are proposed codifications of observed patterns.
6. Proposals are stored in `operational/emergent-rules/` with status in filename or frontmatter.
