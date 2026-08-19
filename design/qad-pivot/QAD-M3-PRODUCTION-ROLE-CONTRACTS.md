# QAD-M3 Production Role Contracts

> **Status:** M3 REVIEWED — AWAITING FOUNDER CLOSEOUT
> **Authority:** FD #130; Frozen Architecture (Separation of Duties); Constitution §2 (QAD Capabilities)
> **Traceability:** M3-01 §6 (Separation of Duties) · M3-ROLES (§3 Role Registry) · FD #130 · FROZEN-ARC-Dec-003..006
> **Contract format:** 18 mandatory fields per role per M3 Production Role Contract specification

---

## Field Template

Every role below uses this schema:

```text
Role Name
Classification           (J / IA / EI / PU — see Classification Key)
Mission                  (one-sentence purpose)
Inputs                   (what the role receives)
Canonical Inputs Allowed (source tiers L1-L10, type of evidence)
Noncanonical Inputs Allowed (secondary/synthesis sources)
Tools                    (allowed tool categories)
NotebookLM / Deep Research Access (allowed or prohibited; conditions)
Required Questions       (questions the role must answer)
Required Outputs         (what the role produces)
Output Schema            (structure of outputs)
Authority                (what the role may decide)
Escalation               (what to do when bound is exceeded)
Budget Rights            (budget authority, limits)
Stop Rights              (may stop/block/redirect?)
Forbidden Actions        (what the role must NEVER do)
Separation-of-Duty Rules (which roles it cannot combine with)
Quality Gate             (conditions that must be met before output is accepted)
Failure State            (what happens when the role cannot complete its work)
```

---

## Role 1: Research Director / Case Orchestrator

| Field | Value |
|-------|-------|
| **Classification** | J (HUMAN_OR_AGENT_JUDGMENT_ROLE) |
| **Mission** | Orchestrate full research on an approved case. Assign stages, manage evidence gaps, produce Research Charter, ensure quality gates are met. |
| **Inputs** | Candidate from Selection Engine (AUTO_RESEARCH_NOW state); Evidence Gap Map from discovery; Research Budget allocation |
| **Canonical Inputs Allowed** | L1-L9 admissible; L10 lead-only |
| **Noncanonical Inputs Allowed** | NotebookLM/Deep Research synthesis (must be validated against original source before canonical admission) |
| **Tools** | Research orchestration, document management, case management, Evidence Registry access |
| **NotebookLM / Deep Research Access** | Full access for evidence-gap exploration; all material findings must be validated against original source |
| **Required Questions** | What is the research scope? Are H1–H5 complete? What evidence gaps exist? Is the budget appropriate? |
| **Required Outputs** | Research Charter (H1–H5, key questions, scope, budget); case orchestration decisions; stage transition records |
| **Output Schema** | Research Charter: `{case_id, entity_id, h1-h5_statements, key_questions, evidence_gap_map, budget_estimate, timeline}` |
| **Authority** | Open research case; assign stages; manage evidence gaps; recommend budget to Research Budget Controller |
| **Escalation** | Budget constraint → Research Budget Controller; methodology conflict → Chief Underwriter; policy override → Founder |
| **Budget Rights** | Propose budget; cannot self-authorize |
| **Stop Rights** | May stop research stages (document reason); may not skip Red Team/Audit (Founder only) |
| **Forbidden Actions** | Self-approve own Research Charter; bypass Red Team/Audit; select own cases; recompute evidence without source |
| **Separation-of-Duty Rules** | MUST NOT combine with Independent Auditor, Structural Red Team, Selection Engine |
| **Quality Gate** | Research Charter co-approved by Evidence Intelligence Lead (validates evidence scope, H1–H5 presence, falsifiability). Budget approved by Research Budget Controller. |
| **Failure State** | Case marked `INCOMPLETE` with documented reason; budget returned to pool |

---

## Role 2: Evidence Intelligence Lead

| Field | Value |
|-------|-------|
| **Classification** | J (HUMAN_OR_AGENT_JUDGMENT_ROLE) |
| **Mission** | Manage source gathering, evidence validation, canonical admission, and evidence graph maintenance. Ensure source/PIT/provenance discipline. |
| **Inputs** | Raw sources (L1-L10), Research Charter, Evidence Gap Map |
| **Canonical Inputs Allowed** | L1-L9 admissible; L10 lead-only (cannot support material conclusion) |
| **Noncanonical Inputs Allowed** | NotebookLM/Deep Research synthesis (for gap detection only; not canonical truth) |
| **Tools** | Source retrieval, Evidence Registry, document management, PIT verification |
| **NotebookLM / Deep Research Access** | Full access for evidence gap detection; material findings must be validated against original source |
| **Required Questions** | Is each source retrievable and verified? Is PIT correct? Can evidence be independently reproduced? Are contradictions preserved? |
| **Required Outputs** | Canonical Evidence Registry entries (FACT/CLAIM/INFERENCE/HYPOTHESIS); evidence quality assessments; contradiction records |
| **Output Schema** | Evidence entry: `{evidence_id, source_id, evidence_type, content, extractor, validation_status, PIT, admitting_role, L_tier}` |
| **Authority** | Admit evidence to Canonical Registry; flag evidence quality issues; reject L10 as sole material support |
| **Escalation** | Source unreachable → document gap; PIT conflict → flag for resolution; contradictory evidence → preserve both |
| **Budget Rights** | None (source retrieval draws from case budget via Research Director) |
| **Stop Rights** | May flag blocking evidence issues; cannot stop case |
| **Forbidden Actions** | Self-review own evidence (must be audited); admit NotebookLM output without source validation; suppress contradictions |
| **Separation-of-Duty Rules** | MUST NOT combine with Independent Auditor |
| **Quality Gate** | Every admitted evidence entry verified against original source. PIT timestamp confirmed. Contradictions explicitly noted. |
| **Failure State** | Evidence gap documented; source marked `UNAVAILABLE` with reason |

---

## Role 3: Core Desk Researcher

| Field | Value |
|-------|-------|
| **Classification** | J (HUMAN_OR_AGENT_JUDGMENT_ROLE) |
| **Mission** | Perform deep desk research: read filings, synthesize cross-source evidence, produce analytical notes, identify contradictions. |
| **Inputs** | Primary source foundation, Research Charter, Canonical Evidence Registry |
| **Canonical Inputs Allowed** | L1-L9 admissible |
| **Noncanonical Inputs Allowed** | NotebookLM/Deep Research synthesis (for orientation only; material findings validated against original source) |
| **Tools** | Document reading, evidence extraction, calculation, source cross-referencing |
| **NotebookLM / Deep Research Access** | Allowed for synthesis and cross-source interrogation; material findings must be validated |
| **Required Questions** | What does each source say? What are the key claims? What contradicts? What is the evidence quality? |
| **Required Outputs** | Desk research notes, source extracts, FACT/CLAIM/INFERENCE candidates, initial gap identification |
| **Output Schema** | Research note: `{case_id, source_ids, key_findings, contradictions, evidence_quality, open_questions, analyst}` |
| **Authority** | Extract and structure evidence; flag contradictions; propose evidence candidates |
| **Escalation** | Evidence contradiction → flag to Evidence Intelligence Lead; scope ambiguity → Research Director |
| **Budget Rights** | None (allocated via case budget) |
| **Stop Rights** | None |
| **Forbidden Actions** | Make final analytical determinations (quality, impairment, valuation); admit evidence without Evidence Lead review |
| **Separation-of-Duty Rules** | MUST NOT combine with Structural Red Team |
| **Quality Gate** | All extracted claims traceable to source location. Calculations reproducible. Contradictions preserved. |
| **Failure State** | Incomplete extraction documented; gaps passed to Research Director |

---

## Role 4: Business & Industry Analyst

| Field | Value |
|-------|-------|
| **Classification** | J (HUMAN_OR_AGENT_JUDGMENT_ROLE) |
| **Mission** | Analyze business quality, moat, customer economics, and industry structure. Produce quality assessment. |
| **Inputs** | Canonical Evidence Registry, industry data, company filings, Peer data |
| **Canonical Inputs Allowed** | L1-L9 admissible |
| **Noncanonical Inputs Allowed** | Industry reports, trade data, NotebookLM industry synthesis (for orientation) |
| **Tools** | Financial analysis, industry data, moat framework, competitor analysis |
| **NotebookLM / Deep Research Access** | Allowed for industry context and competitor landscape; material findings validated |
| **Required Questions** | Is this a high-quality business? What is the moat mechanism? How durable? Is the moat strengthening or weakening? What is the industry structure? |
| **Required Outputs** | Quality Assessment (VERIFIED/PROBABLE/UNRESOLVED/FAILED); Industry Economics Analysis; Moat Analysis (type, width, depth, trend, durability) |
| **Output Schema** | Quality Assessment: `{case_id, quality_state, moat_type, moat_width, moat_depth, moat_trend, moat_durability, false_quality_test, evidence_ids}` |
| **Authority** | Assign quality state; recommend moat classification |
| **Escalation** | Quality state UNRESOLVED → additional evidence requested; false-quality concern → flag to Research Director |
| **Budget Rights** | None |
| **Stop Rights** | None |
| **Forbidden Actions** | Make impairment diagnosis; determine recovery model; assign valuation; write final verdict |
| **Separation-of-Duty Rules** | MUST NOT combine with Chief Underwriter, Structural Red Team |
| **Quality Gate** | False-Quality Test completed. Moat evidence from multiple independent sources. Quality state explicitly justified. |
| **Failure State** | Quality state UNRESOLVED with documented evidence gaps |

---

## Role 5: Financial & Management Analyst

| Field | Value |
|-------|-------|
| **Classification** | J (HUMAN_OR_AGENT_JUDGMENT_ROLE) |
| **Mission** | Perform financial reconstruction, management assessment, capital allocation analysis, per-share economics. |
| **Inputs** | Company filings, market data, management statements, proxy statements |
| **Canonical Inputs Allowed** | L1-L3 (corporate filings, regulatory, industry) |
| **Noncanonical Inputs Allowed** | Analyst estimates, news, management interviews (for context) |
| **Tools** | Financial analysis, spreadsheet, calculation engine, SEC EDGAR |
| **NotebookLM / Deep Research Access** | Limited to financial data extraction and cross-year comparison; no final calculations |
| **Required Questions** | What is the financial trajectory (7-10+ years)? How has management allocated capital? Has management kept promises? What is the per-share value creation? |
| **Required Outputs** | Financial Reconstruction (7-10+ years); Management Assessment (Decision History Ledger, Capital Allocation Ledger, Promise vs Outcome); Calculation Lineage |
| **Output Schema** | Financial Reconstruction: `{case_id, years[], revenue_bridge, margins, FCF, ROIC, leverage, per_share, capital_allocation_ledger, management_claim_ledger}` |
| **Authority** | Produce financial reconstruction; assess management track record |
| **Escalation** | Data gaps → Research Director; management concerns → flag to Research Director |
| **Budget Rights** | None |
| **Stop Rights** | None |
| **Forbidden Actions** | Determine impairment type; set recovery model; assign valuation; write final verdict |
| **Separation-of-Duty Rules** | MUST NOT combine with Chief Underwriter |
| **Quality Gate** | Every calculation has explicit lineage (formula, inputs, source references). 7-10+ years of data (minimum 5 with limitation noted). Management assessment based on decisions, not charisma. |
| **Failure State** | Incomplete reconstruction documented; data gaps listed |

---

## Role 6: Impairment Diagnosis Specialist

| Field | Value |
|-------|-------|
| **Classification** | J (HUMAN_OR_AGENT_JUDGMENT_ROLE) |
| **Mission** | Diagnose impairment type (temporary/structural/mixed/unresolved), build recovery model, identify thesis killers. |
| **Inputs** | Quality Assessment, Financial Reconstruction, Dislocation data, Industry context |
| **Canonical Inputs Allowed** | L1-L9 admissible |
| **Noncanonical Inputs Allowed** | Market commentary, analyst notes (contextual only) |
| **Tools** | Financial analysis, industry data, impairment framework |
| **NotebookLM / Deep Research Access** | Allowed for recovery-scenario analysis and comparable-case review |
| **Required Questions** | Is the impairment temporary, structural, or unresolved? What is the recovery mechanism? What evidence would flip the diagnosis? |
| **Required Outputs** | Impairment Diagnosis (TEMPORARY/MOSTLY_TEMPORARY/MIXED/STRUCTURAL/UNRESOLVED); Recovery Model (Cause→Mechanism→Evidence→Sequence→Horizon→Invalidation); Thesis Killers |
| **Output Schema** | Impairment: `{case_id, diagnosis, strongest_competing_explanation, why_primary_dominates, weakest_link, flip_evidence}`. Recovery: `{case_id, cause, mechanism, leading_evidence, expected_sequence, time_horizon, invalidation}` |
| **Authority** | Assign impairment state; define recovery model; identify thesis killers |
| **Escalation** | UNRESOLVED → additional evidence requested; STRUCTURAL → flag for impact on QAD thesis |
| **Budget Rights** | None |
| **Stop Rights** | None |
| **Forbidden Actions** | Assign valuation; write final verdict; use "historically great company, therefore will recover" as causal reasoning |
| **Separation-of-Duty Rules** | MUST NOT combine with Chief Underwriter |
| **Quality Gate** | Recovery mechanism is specific (not circular). Thesis killers are observable. Strongest competing explanation is documented. Flip evidence is concrete. |
| **Failure State** | UNRESOLVED with documented evidence gaps; recovery model may be deferred |

---

## Role 7: Valuation & Expectations Specialist

| Field | Value |
|-------|-------|
| **Classification** | J (HUMAN_OR_AGENT_JUDGMENT_ROLE) |
| **Mission** | Perform Reverse DCF, scenario analysis, permanent loss analysis, economic vs price damage comparison. |
| **Inputs** | Financial Reconstruction, Impairment Diagnosis, Recovery Model, Market data |
| **Canonical Inputs Allowed** | L1-L3 admissible |
| **Noncanonical Inputs Allowed** | Market data, analyst estimates, comparable company data (contextual) |
| **Tools** | DCF modeling, scenario analysis, market data |
| **NotebookLM / Deep Research Access** | Limited to comparable scenario research; no valuation calculations |
| **Required Questions** | What does the current price imply about future expectations? Are those expectations far worse than evidence supports? What is the permanent loss risk? |
| **Required Outputs** | Reverse DCF; Economic Scenarios (CURRENT/NO_RECOVERY/PARTIAL_RECOVERY/NORMALIZATION/QUALITY_COMPOUNDING); Permanent Loss Analysis; Economic Damage vs Price Damage; Valuation Asymmetry |
| **Output Schema** | Valuation: `{case_id, scenarios[], reverse_dcf, permanent_loss, damage_gap, asymmetry_estimate, thesis_killers_financial}` |
| **Authority** | Produce scenario-based valuation range; estimate permanent loss; identify valuation asymmetry |
| **Escalation** | Valuation range extreme → Research Director; permanent loss risk high → flag to Chief Underwriter |
| **Budget Rights** | None |
| **Stop Rights** | None |
| **Forbidden Actions** | Produce single fair-value number; write final verdict; allocate capital; recommend trade |
| **Separation-of-Duty Rules** | MUST NOT combine with Chief Underwriter |
| **Quality Gate** | Reverse DCF is mandatory. All five scenarios defined. No single fair-value number. Permanent loss analysis included. Valuation is diagnostic, not decorative. |
| **Failure State** | Valuation range too wide for conclusion → documented as UNRESOLVED |

---

## Role 8: Chief Underwriter

| Field | Value |
|-------|-------|
| **Classification** | J (HUMAN_OR_AGENT_JUDGMENT_ROLE) |
| **Mission** | Synthesize all analytical work, Red Team challenge, and Audit report into a final research verdict. |
| **Inputs** | Quality Assessment, Industry Economics, Financial Reconstruction, Management Assessment, Impairment Diagnosis, Recovery Model, Valuation/Range Analysis, Structural Red Team findings, Independent Audit Report |
| **Canonical Inputs Allowed** | All L1-L9 analytical outputs, Red Team findings, Audit Report |
| **Noncanonical Inputs Allowed** | None — Chief Underwriter works only from canonical analytical outputs |
| **Tools** | Synthesis, analytical judgment, cross-domain reasoning |
| **NotebookLM / Deep Research Access** | **NONE** — Chief Underwriter must not use AI synthesis for final verdict. Verdict is independent human (or agent) judgment based on canonical evidence. |
| **Required Questions** | Is the QAD thesis supported by the full evidence base? What is the strongest counterargument? What is the research verdict? |
| **Required Outputs** | Research Verdict (QAD_CONFIRMED/QAD_PROBABLE/QAD_UNRESOLVED/NOT_QAD_STRUCTURAL/NOT_QAD_QUALITY/NOT_QAD_VALUATION); Synthesis narrative; Scenario weightings; Key uncertainties; Thesis-specific monitoring indicators |
| **Output Schema** | Verdict: `{case_id, verdict, synthesis_narrative, scenario_weights, key_uncertainties[], monitoring_indicators[], recommendation_to_founder}` |
| **Authority** | Assign research verdict; define monitoring indicators; recommend to Founder (advisory) |
| **Escalation** | QAD_UNRESOLVED → escalate to Founder with explanation; material finding shift → re-open underwriting |
| **Budget Rights** | None |
| **Stop Rights** | May block `FOUNDER_READY` if analytical outputs are insufficient |
| **Forbidden Actions** | ❌ Choose its own cases (Selection Engine maintains separation) ❌ Allocate capital ❌ Size positions ❌ Execute trades ❌ Approve Research Charter (before research) ❌ Ignore or suppress Red Team findings ❌ Produce FOUNDER_ENDORSED state (Founder only) |
| **Separation-of-Duty Rules** | MUST NOT combine with any analytical role (4-7), MUST NOT combine with Selection Engine, MUST NOT combine with Portfolio Manager |
| **Quality Gate** | All preceding stages COMPLETED or documented INCOMPLETE. Red Team assessment exists. Audit PASS or findings resolved. No self-review. |
| **Failure State** | Verdict UNRESOLVED → escalate to Founder; cannot be delegated to analytical roles |

---

## Role 9: Structural Red Team

| Field | Value |
|-------|-------|
| **Classification** | IA (INDEPENDENT_ASSURANCE_ROLE) |
| **Mission** | Assume QAD thesis is wrong and the market may be correct. Construct the strongest value-trap case. |
| **Inputs** | Full research record (all analytical outputs, evidence, sources) |
| **Canonical Inputs Allowed** | All L1-L9 evidence |
| **Noncanonical Inputs Allowed** | None — must work from the same evidence base as the primary thesis |
| **Tools** | Analytical reasoning, challenge framework, evidence review |
| **NotebookLM / Deep Research Access** | NONE — must not use AI synthesis. Challenge is independent analytical judgment. |
| **Required Questions** | Against Quality? Against Temporary? Against Recovery? Against Management? Against Valuation? For Market Correctness? Hidden Risks? Cost of Being Wrong? |
| **Required Outputs** | Challenge outcome (ACCEPTED/PARTIALLY_ACCEPTED/REJECTED_WITH_EVIDENCE/UNRESOLVED); Strongest opposing case; Challenge findings |
| **Output Schema** | Challenge: `{case_id, outcome, strongest_opposing_case, findings[], risk_assessment, cost_of_being_wrong}` |
| **Authority** | Challenge the primary thesis; construct opposing case; preserve findings verbatim |
| **Escalation** | CRITICAL finding → Chief Underwriter must address; no veto but finding preserved |
| **Budget Rights** | None |
| **Stop Rights** | None (no veto) |
| **Forbidden Actions** | ❌ Veto the thesis (findings are advisory to Underwriter) ❌ Create new evidence ❌ Access pre-decisional charter drafts ❌ Recommend trade or allocation |
| **Separation-of-Duty Rules** | MUST NOT combine with Research Director, Core Desk Researcher, or any research/analytical role (1-7). MUST be independent of the research chain. |
| **Quality Gate** | Red Team has NO prior involvement in the case. Output is preserved verbatim. No evidence of anchoring to primary thesis. |
| **Failure State** | UNRESOLVED outcome → findings preserved; Underwriter weighs unresolved challenges |

---

## Role 10: Independent Research Auditor

| Field | Value |
|-------|-------|
| **Classification** | IA (INDEPENDENT_ASSURANCE_ROLE) |
| **Mission** | Verify source existence, citation correctness, PIT integrity, calculation reproducibility, contradiction preservation. |
| **Inputs** | Full research record, raw sources, calculation lineage |
| **Canonical Inputs Allowed** | All primary sources, all calculations, all evidence |
| **Noncanonical Inputs Allowed** | None — auditor checks what EXISTS, not what is correct |
| **Tools** | Source verification, calculation reproduction, PIT checking |
| **NotebookLM / Deep Research Access** | NONE — auditor must verify original sources directly |
| **Required Questions** | Does the cited source exist? Can the calculation be reproduced? Is PIT correct? Are contradictions preserved? Is self-review separation maintained? |
| **Required Outputs** | Audit Report: PASS/PASS_WITH_FINDINGS/FAIL; Specific findings with evidence |
| **Output Schema** | Audit: `{case_id, outcome, findings[]{check, pass_fail, evidence, required_correction}, blocker}` |
| **Authority** | May block `FOUNDER_READY`; does not decide thesis; may call for recalculation or source verification |
| **Escalation** | FAIL → case blocked until resolved; findings → Research Director for correction |
| **Budget Rights** | None |
| **Stop Rights** | **May block FOUNDER_READY** — non-delegable authority |
| **Forbidden Actions** | ❌ Decide the thesis ❌ Recommend investment action ❌ Create new evidence ❌ Approve Research Charter |
| **Separation-of-Duty Rules** | MUST NOT combine with Research Director, Evidence Intelligence Lead, or any role that produced evidence for this case |
| **Quality Gate** | All 9 audit checks completed (source existence, original-source inspection, citation correctness, PIT integrity, calculation reproducibility, contradiction preservation, model provenance, self-review separation, publication gates). |
| **Failure State** | FAIL → case blocked; findings documented; cannot be overridden by Research Director |

---

## Role 11: Thai Long-Form Research Editor

| Field | Value |
|-------|-------|
| **Classification** | PU (PUBLICATION_ROLE) |
| **Mission** | Transform research into Thai long-form journalism for publication on `/library`. |
| **Inputs** | Research record, research verdict, Full analytical package |
| **Canonical Inputs Allowed** | All canonical evidence |
| **Noncanonical Inputs Allowed** | None — publication is based on canonical research only |
| **Tools** | Writing, editing, Thai language, formatting |
| **NotebookLM / Deep Research Access** | NONE — editorial must be human writing |
| **Required Questions** | Is the article reader-friendly? Is all governance jargon removed? Are companion publications linked? Is Thai language correct? |
| **Required Outputs** | Thai long-form article (draft); Companion CRO article (if applicable); Publication metadata (category, slug, date) |
| **Output Schema** | Article: `{slug, title, category, published_date, body_thai, companion_slug, status}` |
| **Authority** | Edit for clarity, readability, and Thai language correctness; propose publication draft |
| **Escalation** | Thai language quality → external review if needed; factual ambiguity → Research Director |
| **Budget Rights** | None |
| **Stop Rights** | May recommend NOT publishing if quality insufficient |
| **Forbidden Actions** | ❌ Create new thesis ❌ Change analytical conclusions ❌ Remove contradictions ❌ Add investment recommendations ❌ Publish without Founder gate |
| **Separation-of-Duty Rules** | Must be separate from thesis creation (Chief Underwriter, Research Director) |
| **Quality Gate** | Governance jargon removed (FD #94). Companion publication linked. Thai language verified. Category frontmatter set. |
| **Failure State** | Article draft incomplete; published as DRAFT only |

---

## Role 12: Thesis / Knowledge Steward

| Field | Value |
|-------|-------|
| **Classification** | J (HUMAN_OR_AGENT_JUDGMENT_ROLE) |
| **Mission** | Monitor thesis-specific indicators. Manage knowledge compounding. Cross-case validation. |
| **Inputs** | Research verdict, monitoring indicators, case outcomes, published reports |
| **Canonical Inputs Allowed** | All canonical evidence, monitoring data |
| **Noncanonical Inputs Allowed** | News, market data, industry updates (for monitoring context) |
| **Tools** | Monitoring dashboard, evidence registry, case management |
| **NotebookLM / Deep Research Access** | Limited — for monitoring-related research and cross-case pattern identification |
| **Required Questions** | Are thesis indicators on track? Has any monitoring state changed? Are there cross-case patterns? What candidate lessons have emerged? |
| **Required Outputs** | Monitoring state updates (RECOVERY_CONFIRMING/ON_TRACK/UNCERTAIN/WEAKENING/BROKEN); Candidate Lesson proposals; Cross-case validation reports |
| **Output Schema** | Monitoring: `{case_id, monitoring_state, indicator_values[], trigger_events[], evidence_ids, steward}`. Knowledge: `{lesson_id, source_cases[], pattern, validation_status, reviewer}` |
| **Authority** | Update monitoring state; propose Candidate Lessons; trigger cross-case validation |
| **Escalation** | BROKEN state → notify Founder; single case ≠ institutional knowledge |
| **Budget Rights** | None |
| **Stop Rights** | None |
| **Forbidden Actions** | ❌ Approve knowledge without cross-case validation ❌ Change thesis verdict retroactively ❌ Automatically escalate monitoring to research mandate |
| **Separation-of-Duty Rules** | MUST NOT combine with Structural Red Team |
| **Quality Gate** | Monitoring indicators are thesis-specific (not generic news). Knowledge requires cross-case validation (3+ cases). Single case does not become institutional knowledge. |
| **Failure State** | Monitoring data unavailable → `UNCERTAIN` state; knowledge not yet validated |

---

## Role 13: Discovery & Dislocation Scout

| Field | Value |
|-------|-------|
| **Classification** | J/EI (HUMAN_OR_AGENT_JUDGMENT_ROLE / ELASTIC_INVESTIGATOR — transitional) |
| **Mission** | Detect, surface, connect, and raise questions from signals that structured sensors may miss. Radar Scout (CAP-011 — TRANSITIONAL). |
| **Inputs** | External signals, ecosystem data, unstructured sources, market data, filings |
| **Canonical Inputs Allowed** | L1-L10 (all tiers admissible for discovery; L10 lead-only) |
| **Noncanonical Inputs Allowed** | Social media, forums, news, analyst notes (for discovery leads only) |
| **Tools** | Radar scanning, signal detection, pattern recognition, web research |
| **NotebookLM / Deep Research Access** | Full access for discovery and signal detection |
| **Required Questions** | Is there a material signal that structured sensors may miss? Does this signal warrant candidate assembly? |
| **Required Outputs** | Signal Registry entries; Task Idea Cards; Discovery leads |
| **Output Schema** | Signal: `{signal_id, entity_id, signal_type, description, evidence, source_tier, entry_route, timestamp}` |
| **Authority** | Detect signals; surface to Signal Registry; create Task Idea Cards for CoS triage |
| **Escalation** | Material signal → Candidate Assembly; unclear signal → WATCH_EVIDENCE |
| **Budget Rights** | None (cron-budgeted as existing infrastructure) |
| **Stop Rights** | None |
| **Forbidden Actions** | ❌ Declare Quality ❌ Declare Temporary/Structural ❌ Value Company ❌ Write Final Thesis ❌ Approve Selection ❌ Allocate Budget ❌ Recommend Trade |
| **Separation-of-Duty Rules** | MUST NOT combine with Selection Engine, Chief Underwriter |
| **Quality Gate** | Signal is documented with source and evidence. No quality/impairment/valuation assertion. Radar raises questions; never answers them. |
| **Failure State** | Signal insufficient → no candidate; documented as `NO_SIGNAL` |

---

## Role 14: Elastic Investigator

| Field | Value |
|-------|-------|
| **Classification** | EI (ELASTIC_INVESTIGATOR) |
| **Mission** | Deploy on-demand from specific evidence gaps. Gather primary ecosystem intelligence from lawful public sources. |
| **Inputs** | Scuttlebutt Charter (Evidence Gap ID, falsifiable question, allowed sources, stop rule) |
| **Canonical Inputs Allowed** | Per charter: L1-L9 as specified; L10 only if explicitly authorized in charter |
| **Noncanonical Inputs Allowed** | Per charter only |
| **Tools** | Web research, source retrieval, evidence gathering, documentation |
| **NotebookLM / Deep Research Access** | Per charter authorization |
| **Required Questions** | What does the evidence say about the falsifiable question? What are the sampling limitations? Is the investigation complete per stop rule? |
| **Required Outputs** | Investigation Report (findings, sources, limitations, ANSWERED/NOT_ANSWERED/PARTIALLY_ANSWERED disposition); Proposed evidence for canonical admission |
| **Output Schema** | Report: `{investigation_id, evidence_gap_id, falsifiable_question, findings, sources[], sampling_limitations, disposition, proposed_evidence_ids[], stop_rule_triggered, investigator}` |
| **Authority** | Gather evidence within charter scope; document findings |
| **Escalation** | Evidence suggests need for broader investigation → Research Director; budget exhausted → report as INCOMPLETE_BUDGET |
| **Budget Rights** | None (pre-approved charter budget) |
| **Stop Rights** | Stop rule fires → investigation ends |
| **Forbidden Actions** | ❌ Exceed charter scope ❌ Use deceptive pretexting ❌ Solicit confidential information ❌ Operate without approved charter ❌ Make material conclusions beyond evidence scope |
| **Separation-of-Duty Rules** | Single-purpose per charter; must not be the same entity as the evidence evaluator |
| **Quality Gate** | Charter approved before investigation begins. All sources lawful, public, non-MNPI. Sampling limitations documented. Stop rule compliance verified. |
| **Failure State** | Budget exhausted → `INCOMPLETE_BUDGET`; source unavailable → documented gap; stop rule triggered → report as-is |

---

## Independence Domain Summary

The 14 roles organize into 4 independence domains:

```text
A — Research / Evidence / Compatible Analysts
    Roles 1, 2, 3, 4, 5, 6, 7, 12, 13, 14
    (may be combined within A subject to individual separation rules)

B — Chief Underwriter
    Role 8 only
    MUST be independent of A

C — Structural Red Team
    Role 9 only
    MUST be independent of A and B

D — Independent Auditor
    Role 10 only
    MUST be independent of A, B, and C

E — Thai Editor
    Role 11 only
    MUST be independent of thesis creation (Roles 8, 1)
```

Selection Engine is a POLICY SERVICE (not a role), fully separate from all domains.

These are authority boundaries, not Hermes profile counts. A single runtime entity may implement multiple roles within Domain A where no individual separation rule is violated. But Domains A, B, C, D, and E must never be collapsed into fewer than 5 independent authority entities.

<!-- 2026-08-19 17:00 UTC+7 -->