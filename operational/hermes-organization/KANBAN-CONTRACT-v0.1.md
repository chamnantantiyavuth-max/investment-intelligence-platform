# IIP AI Organization — Kanban Contract

**Status:** PROPOSED OPERATIONAL STANDARD — approved for implementation by FD #54 (2026-08-05)
**Version:** 0.1
**Authority:** Subordinate to the IIP Constitution + `AI-ORGANIZATION-OPERATING-STANDARD-v0.1.md`.
**Runtime vehicle (FD #54, F-12):** **repo-based single board** at `operational/hermes-organization/kanban/` (the Hermes kanban toolset is disabled in profile config; enabling it would require a separate config decision). Git history is the audit trail; single-writer discipline applies.

## 1. One Organization, One Board

The IIP uses one canonical organization board. Roles may create filtered views, but not competing workflow systems. The board is operational tracking only — card state never equals domain state (see §3).

## 2. Columns (Operational Only)

| Column | Entry Rule | Exit Rule |
|---|---|---|
| Inbox | New request, anomaly, or idea captured | Minimum intake fields completed |
| Triage | Owner and value not yet confirmed | Scope, owner, artifact, and non-goals defined |
| Scoped | Research contract exists | Required data and sources identified |
| Data Ready | Data Steward status recorded | Principal begins analysis |
| In Research | Active domain work | Principal draft complete |
| Cross-Review | Independent domain/risk review active | Challenges answered or registered |
| Validation | Quant/data/risk validation active | Required Hold cleared or limitations accepted for review |
| Founder Review | Packet administratively complete (IC Secretary gate) | Explicit Founder decision or return request |
| Monitoring | Approved or retained research under observation | Review trigger, dormancy, supersession, or archival |
| Blocked | Cannot proceed due to named dependency | Dependency resolved and return column recorded |
| Closed | Work completed, rejected, superseded, or archived | Reopen only with reason and lineage |

## 3. Mandatory Card Fields (Canonical States Only)

```yaml
card_id:
title:
research_question:
decision_user: Founder
workflow_column:            # §2 column — OPERATIONAL ONLY, never a domain state
approval_status:            # CANONICAL: Detected Hypothesis | Experimental | Under Human Review | Approved | Rejected
monitoring_status:          # CANONICAL: Not Monitored | Active Monitoring | Dormant | Archived
thesis_status:              # CANONICAL: Proposed | Under Review | Confirmed | Weakened | Invalidated | Waiting (if applicable)
research_state:             # CANONICAL: Watchlist | Priority Research | Selected for Deep Research | Archived (if applicable)
artifact_state:             # CANONICAL: Draft | Reviewed Draft | Founder-Reviewed | Current Authoritative | Superseded | Archived | Rejected
domain:
principal_owner:
assistant_owner:
priority:                   # P0-P3 (operational)
materiality:                # M0-M4 (see §4)
created_at:
required_by:
expected_artifact:
evidence_standard:
data_status:                # NOT ASSESSED | DATA READY | DATA READY WITH LIMITATIONS | DATA HOLD
validation_status:          # NOT REQUIRED | PENDING | VALIDATED | VALIDATED WITH LIMITATIONS | VALIDATION HOLD
risk_status:                # NOT REVIEWED | REVIEWED | REVIEWED WITH OPEN RISKS | RISK HOLD
audit_status:
open_decision_slots: []
dependencies: []
blocked_reason:
next_action:
last_updated:
```

**State rule:** a card move never changes `approval_status`, `monitoring_status`, `thesis_status`, `research_state`, or `artifact_state`. Those change only through the canonical transition rules (Constitution §5; CANDIDATE-AND-QUEUE-MODEL §3.3; CIW-LIFECYCLE §5) with audit fields (prior state, new state, reason, evidence refs, actor, timestamp, rule/workflow version).

## 4. Labels

### Domain

COMMODITY · MACRO · EQUITY · OPTIONS · QUANT · DATA · RISK · GOVERNANCE · CROSS-ASSET

### Materiality (operational triage scale — subordinate to the canonical "material change" definition in `operational/CHANGE-CONTROL-AND-APPROVAL.md`)

- M0 — administrative
- M1 — routine research
- M2 — material interpretation
- M3 — Founder decision required (material per CHANGE-CONTROL-AND-APPROVAL)
- M4 — constitutional, security, or canonical-rule impact (material; full change-control proposal + Founder gate)

M3/M4 items always require the change-control proposal and Founder gate; the M-scale never narrows the canonical material-change definition.

### Data / Validation / Risk Status

As in §3 card fields. Vocabulary is canonical-aligned (EVIDENCE-MODEL §9 Data Confidence; CIW-RESULT-CONTRACT §3 source-coverage statuses).

## 5. Work-in-Progress Limits

- Each Principal: maximum 1 M2/M3 item in `In Research` at a time.
- Each Assistant: maximum 2 active support tasks.
- Organization-wide `Cross-Review`: maximum 5 items.
- Organization-wide `Founder Review`: maximum 3 material items unless Founder requests otherwise.
- No role may start new discretionary work while an older item is blocked solely by its own incomplete action.

The purpose of WIP limits is to improve completion and depth, not to maximize agent utilization.

## 6. Movement Rights

- Assistants may move cards from Inbox through Data Ready only under Principal instruction (each move logged).
- Principals may move their work through In Research and request Cross-Review.
- Validators may move work into Blocked by issuing a formal Hold (FD #54 — Hold = org-workflow pause; canonical state untouched).
- The IC Secretary alone moves a complete packet into Founder Review and may return a packet as ADMINISTRATIVELY INCOMPLETE (administrative gate only — FD #54).
- Only an explicit Founder decision may change `approval_status` to `Approved`/`Rejected` (or any other canonical state transition per §3 rule).
- The Internal Auditor may return any card to Blocked for governance defects (GOVERNANCE HOLD — org-workflow scope).

## 7. Blocked Card Standard

A blocked card must state: exact blocker; owner of resolution; whether the blocker is evidence, data, rule, authority, capacity, or external dependency; work that may continue safely; next review trigger; escalation date or event. `Waiting` without a named condition is not an acceptable blocker.

## 8. Board Swimlanes (filtered views)

1. Theme Intelligence · 2. Alpha Momentum / Market Leadership · 3. Commodity Product Research · 4. Macro Regime Research · 5. Equity Alpha Research · 6. Options and Volatility Research · 7. Quant and Model Validation · 8. Data Quality and Lineage · 9. Risk Challenges · 10. Governance and Audit · 11. Radar Intake (Task Idea Cards — FD #71)

## 9. Weekly Board Review

The weekly review answers: What changed materially? Which tasks are generating decision value? Which tasks are merely accumulating information? Which cards are blocked by unresolved Founder decisions? Which work should be killed, narrowed, or archived? Which approved items require monitoring rather than more research? Are any roles operating outside authority?

## 10. Board Mechanics (repo-based)

- Board file: `kanban/board.md` (columns + current card IDs).
- Cards: `kanban/cards/<card_id>.yaml` (schema §3).
- Holds: `kanban/holds/<hold_id>.yaml` (schema: scope, trigger, evidence, remediation, owner, review condition, partial-work allowance, clear record).
- Writer discipline: single writer at a time (CoS Assistant under instruction); all changes via git commits on the org branch; conflicts resolved by the CoS, escalated to Founder if material.

---

*Kanban Contract v0.1 — FD #54. Board state is operational; canonical states live in the Constitution/domain specs.*
<!-- 2026-08-05 14:45 UTC+7 -->
