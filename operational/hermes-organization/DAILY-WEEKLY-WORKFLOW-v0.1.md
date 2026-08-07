# IIP AI Organization — Daily and Weekly Workflow

**Status:** PROPOSED OPERATIONAL STANDARD — approved for implementation by FD #54 (2026-08-05)
**Version:** 0.1
**Authority:** Subordinate to the IIP Constitution + `AI-ORGANIZATION-OPERATING-STANDARD-v0.1.md`.
**Cadence note (FD #54, F-19):** the cadence below is org process. **No new cron jobs** are authorized by this standard; every scheduled automation requires a separate named authorization (FD-CIW-005 discipline). The pilot and initial activation run manually/ad-hoc. **Exceptions granted by named FDs:** weekly Radar Scan cron (Mon 08:00 UTC+7, FD #78, 2026-08-07 — discovery-only scanning → Task Idea Cards + Radar Digest); mid-week Radar Watch cron (Thu 08:00 UTC+7, FD #80, 2026-08-07 — lighter pass, event-window coverage + data-gap retries); CIW Class A MSFT monitor (Mon 09:00, FD-CIW-013/014).

## 1. Operating Principle

The organization runs on artifacts and gates, not on continuous agent conversation. Each handoff must have a named owner, explicit inputs, a defined output, and a clear next state.

## 2. Daily Workflow

### Stage D0 — Startup and Boundary Check

**Owner:** Founder Chief of Staff Assistant
**Inputs:** active Kanban board, Founder priorities, unresolved decisions, Holds, event alerts
**Output:** Daily Work Queue

1. Confirm that every active task belongs to IIP.
2. Identify any request involving capital allocation, position management, or execution and route it out of scope (`OUT OF IIP SCOPE — REFER TO FOUNDER / CAPITAL COMMAND`).
3. Confirm portfolio-blind: no task receives holdings, positions, cost basis, transactions, or account data.
4. Check active Holds and blocked dependencies.
5. Confirm each task has one Principal owner and, where used, one Assistant.
6. Enforce work-in-progress limits (KANBAN-CONTRACT §5).

### Stage D1 — Intake and Triage

**Owner:** Founder Chief of Staff
**Recorder:** Investment Committee Secretary Assistant

Classify each intake as: anomaly; theme hypothesis; product research; macro event; company/candidate research; options/volatility question; data issue; model/quant question; risk challenge; audit/governance issue.

Each accepted item receives: task ID; research question; decision user; required-by date or event; domain owner; evidence standard; expected artifact; known dependencies; explicit non-goals. Deep-research intakes must reference `project-definition/company-intelligence-workbench/CIW-REQUEST-CONTRACT.md` (Research Gate; portfolio_blind = true) — no CIW-path work without a separate named FD (FD #44 discipline, unchanged).

### Stage D2 — Data Readiness Gate

**Owner:** Data Steward
**Support:** Data Steward Assistant

Before material analysis: (1) identify required datasets and sources; (2) verify provenance and timestamp semantics (EVIDENCE-MODEL §5); (3) assess freshness, completeness, reliability, conflicts, and revisions (EVIDENCE-MODEL §9); (4) register point-in-time limitations; (5) issue `DATA READY`, `DATA READY WITH LIMITATIONS`, or `DATA HOLD` (source-coverage statuses per CIW-RESULT-CONTRACT §3).

No downstream role may convert `DATA READY WITH LIMITATIONS` into unqualified confidence.

### Stage D3 — Domain Research

**Owner:** Relevant Domain Principal
**Support:** Relevant Assistant

The Principal must: (1) frame the question; (2) separate facts, claims, assumptions, and inferences (canonical Evidence Model taxonomy); (3) map supporting and disconfirming evidence; (4) identify alternative explanations; (5) state uncertainty; (6) define falsification and monitoring conditions; (7) produce the required artifact (mapped template). Assistants may gather and structure inputs but do not sign the conclusion.

### Stage D4 — Independent Challenge

Depending on materiality, route the draft to: Chief Risk Officer (risk and scenario challenge); Quant & Model Validator (quantitative validation); Data Steward (unresolved data issues); a second domain Principal (cross-domain review). Material items follow CIW-QUALITY-GATES §1 operational separation (no self-review; separate session/context; direct source inspection; Sol Medium where required).

The author must respond to each material challenge with: accepted; partially accepted; rejected with rationale; unresolved and escalated. Dissent remains attached to the artifact.

### Stage D5 — Committee Readiness

**Owner:** Investment Committee Secretary

The Secretary checks (administrative completeness gate — FD #54): required sections complete; evidence linked; data status visible; validation status visible; risk challenge included; dissent included; unresolved rule slots explicit; requested Founder decision phrased precisely; no capital-management content inserted; exact artifact + version identified for approval (Constitution §21, CIW founder-review-record precedent).

Output: `READY FOR FOUNDER REVIEW`; or `ADMINISTRATIVELY INCOMPLETE` with a defect list.

### Stage D6 — Daily Close

**Owner:** Founder Chief of Staff Assistant
**Custodian:** Investment Committee Secretary Assistant

Produce: completed work; new evidence; changed confidence; new contradictions; new Holds; decisions required; overdue items; next-day queue. No approval is inferred from the Daily Close.

## 3. Weekly Workflow

### Monday — Priority and Capacity Review

**Chair:** Founder Chief of Staff
Outputs: Founder-priority translation; weekly research queue; WIP allocation; dependency map; expected Founder decisions; deferred items and rationale. The Chief of Staff may reduce scope but may not invent research rules to accelerate delivery.

### Tuesday–Wednesday — Deep Research and Validation

Primary work period for evidence collection, domain analysis, data quality work, model reproduction, scenario design, falsification review. Avoid committee-style meetings during this block unless a blocker requires cross-functional resolution.

### Thursday — Cross-Functional Challenge

Required for material items: (1) domain owner presents the decision question and evidence; (2) CRO presents strongest failure scenarios; (3) Quant presents validation status where applicable; (4) Data Steward presents data limitations; (5) another domain Principal presents an alternative interpretation; (6) Secretary records unresolved disagreements. The objective is not consensus — it is a decision-ready representation of truth, uncertainty, and disagreement.

### Friday — Founder Review Pack and Institutional Memory

**Owner:** Investment Committee Secretary
**Coordinator:** Founder Chief of Staff

Founder Review Pack contains: one-page executive decision brief; material evidence; strongest counter-case; risk and validation status; unresolved decisions; recommended research disposition; explicit decision options; dissent appendix; change since prior review.

After Founder action: record the decision in the canonical register (FOUNDERS-DECISIONS.md + vault fd-register via `11-FOUNDER-DECISION-RECORD` intake); update governance state only as authorized; update monitoring conditions; preserve rejected alternatives and dissent; assign follow-up tasks; archive superseded drafts without deleting lineage.

## 4. Event-Driven Workflow

Trigger immediate triage for: material commodity supply disruption; major policy or macro regime change; earnings or guidance surprise; balance-sheet or governance event; unusual volatility, skew, or term-structure move; data revision that changes prior conclusions; model drift or failed reproduction; source credibility failure; security, licensing, or lineage incident; authority or governance breach.

Urgency changes sequence, not standards. A fast brief must still distinguish verified facts from provisional interpretation.

## 5. Routine by Role

| Role | Daily | Weekly |
|---|---|---|
| Founder Chief of Staff | Triage, dependency management, escalation | Capacity review, Founder agenda, organization review |
| IC Secretary | Decision-log maintenance, packet completeness | Founder Review Pack, decision archive |
| Commodity Product Analyst | Product and physical-market monitoring | Product dossier or theme update |
| Global Macro Strategist | Regime and event monitoring | Macro regime map and transmission review |
| Equity Alpha Analyst | Company/theme evidence updates | Candidate and earnings review |
| Options Strategist | Volatility and structure monitoring | Options research memo and scenario refresh |
| Chief Risk Officer | Challenge material drafts and event risks | Risk intelligence brief and scenario review |
| Quant & Model Validator | Reproduce material results | Validation queue and model-drift review |
| Data Steward | Data incidents, freshness, lineage | Data quality and source coverage review |
| Internal Auditor / Red Team | Exception-based monitoring | Sample audit or control review (execution via Sol Medium); monthly deeper audit preferred |

## 6. Definition of Done

A research task is not Done merely because a report exists. Minimum completion criteria: question answered within scope; evidence and lineage attached; uncertainty stated; counter-evidence included; falsification conditions defined; data status recorded; validation and risk review completed where required; unresolved decisions registered; Principal sign-off present; artifact stored in approved location; follow-up monitoring owner assigned where relevant.

---

*Daily/Weekly Workflow v0.1 — FD #54. No cron authorized by this document.*
<!-- 2026-08-05 14:45 UTC+7 -->
