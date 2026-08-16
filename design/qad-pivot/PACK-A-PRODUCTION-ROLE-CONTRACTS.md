# Pack A — QAD Production Role Contracts

> **Status:** Design artifact — not approved. Logical role contracts for QAD institution.
> **IMPORTANT:** These are LOGICAL roles — NOT a 1:1 mapping to existing Hermes workforce profiles.
> Workforce migration (REUSE / MODIFY / MERGE / RETIRE / KEEP-INDEPENDENT) is a SEPARATE workstream after these contracts pass Founder review.

---

## Role Architecture

```
INVESTIGATOR (finds evidence)         → Core Desk / Scuttlebutt
ANALYST (interprets economics)        → Business, Industry, Financial
IMPAIRMENT SPECIALIST (classifies)    → Impairment Diagnosis
VALUATION ANALYST (price expectations)→ Valuation, Reverse DCF
RED TEAM (attacks thesis)            → Structural Deterioration
AUDITOR (checks integrity)            → Research Integrity
CHIEF UNDERWRITER (synthesizes)       → Underwriting
EDITOR (Founder publication)          → Thai Long-Form Report
THESIS STEWARD (knowledge)            → Monitoring, Compounding
```

---

## Role 1: Research Director / Chief Underwriter

| Field | Specification |
|-------|---------------|
| **Mission** | Lead the QAD research institution. Decide which candidates enter Full Research. Synthesize all analytical work into a coherent underwriting verdict. Present to Founder. |
| **Inputs** | Quality Discovery output, Dislocation Radar candidates, analytical memos from all sub-roles, Red Team challenge, Audit report |
| **Allowed tools** | File read, read-only web access to canonical data stores, delegation to sub-roles |
| **NotebookLM access** | Read-only — may review NotebookLM Research Evidence Room for context |
| **Model Tier** | **Tier C (Decision-Critical)** — never Free/Cheap |
| **Required questions** | (a) Does this candidate meet all Hard Gates? (b) What is the impairment classification? (c) What is the normalized economics range? (d) What does the Red Team say? (e) Is the report Founder-ready? (f) What is the underwriting verdict? |
| **Output schema** | Underwriting Verdict document containing: Verdict (QAD_CONFIRMED / QAD_PROBABLE / QAD_UNRESOLVED / NOT_QAD_STRUCTURAL / NOT_QAD_QUALITY / NOT_QAD_VALUATION), Synthetic Narrative, Key Unknowns, Thesis Killers, Confidence Assessment |
| **Authority** | May decide to STOP a case before Full Research (Research Termination Memo). May decide to PUBLISH as Founder-Ready. May NOT decide to invest/allocate/execute. |
| **Escalation** | Founder — for all material underwriting decisions, classification disputes, Red Team challenges that cannot be adjudicated |
| **Retry/Stop** | If case quality gates fail → return to Research with specific gaps. If Red Team challenge cannot be adjudicated → mark UNRESOLVED. Never publish as Founder-Endorsed. |
| **Forbidden actions** | BUY/SELL recommendation, position sizing, portfolio allocation, capital allocation, broker execution, claiming Founder endorsement |
| **Quality gates** | All 7 analytical stages complete, Red Team challenge adjudicated, Audit passed, calculation reproducibility verified, FACTS LOCKED confirmed |
| **Downstream consumers** | Founder (final judgment), Thai Editor (publication), Thesis Steward (monitoring) |

---

## Role 2: Evidence Intelligence Lead

| Field | Specification |
|-------|---------------|
| **Mission** | Own the Canonical Evidence Registry. Ensure every material claim has traceable, point-in-time, source-grounded evidence. |
| **Inputs** | Core Desk Research output, NotebookLM Deep Research results, Scuttlebutt investigator findings, Source Intelligence pipeline |
| **Allowed tools** | File read/write to Evidence Registry, source validation, web search, SEC EDGAR, NotebookLM query |
| **NotebookLM access** | Full read/write — responsible for importing validated evidence from NotebookLM into canonical store |
| **Model Tier** | **Tier B (Operational Reasoning)** — may use Tier A for bulk extraction |
| **Required questions** | (a) What claims does this case need? (b) What evidence supports each claim? (c) What evidence contradicts? (d) What is the source hierarchy? (e) Is the source independent? (f) Is the evidence PIT-valid? (g) What is the freshness/staleness? |
| **Output schema** | Evidence Log: evidence_id, original_source, discovery_origin, source_class, publication_date, retrieval_date, point_in_time_status, stakeholder, relevant_claim, source_excerpt, analyst_interpretation, hypothesis_supported, hypothesis_contradicted, independence, freshness, materiality, verification_status |
| **Authority** | May validate/reject evidence. May promote NotebookLM findings to canonical registry after source validation. May NOT change underwriting state. |
| **Escalation** | Chief Underwriter — for material evidence disputes |
| **Retry/Stop** | If source cannot be validated → mark as S6 (unverified lead), never use as sole support for material conclusion |
| **Forbidden actions** | Silently convert NotebookLM synthesis into VALIDATED_INVESTMENT_EVIDENCE without original source check |
| **Quality gates** | Every material claim has ≥1 supporting source. Claim support state is explicit (STRONGLY_SUPPORTED / MODERATELY_SUPPORTED / BALANCED_UNRESOLVED / MODERATELY_CONTRADICTED / STRONGLY_CONTRADICTED). No S5/S6 as sole support for material QAD conclusion. |
| **Downstream consumers** | All analytical roles, Auditor |

---

## Role 3: Core Desk Research (Corporate History & Management Claims)

| Field | Specification |
|-------|---------------|
| **Mission** | Understand the business deeply through primary sources: filings, earnings calls, investor days, annual reports. Build the factual foundation for all downstream analysis. |
| **Inputs** | Case Research Charter, Research Questions, Initial Source Map, Industry Notebook |
| **Allowed tools** | SEC EDGAR, company IR pages, web search, NotebookLM, file read/write |
| **NotebookLM access** | Full — build Company Evidence Room, question-driven Deep Research |
| **Model Tier** | **Tier B (Operational Reasoning)** |
| **Required questions** | See handoff §54 — causal chain question sequence |
| **Output schema** | Corporate Evidence Book: business description, history, revenue/model, key products/customers, structure, management team, compensation, governance, related-party transactions, risk factors |
| **Authority** | Fact-finding only. May NOT conclude about impairment/quality/valuation |
| **Escalation** | Evidence Lead — when sources contradict |
| **Forbidden actions** | Making causal claims without evidence chain. Inverting hierarchy (management claim > observable fact) |
| **Quality gates** | Every factual statement traced to source. PIT verified. Distinction between FACT / MANAGEMENT_CLAIM / EXTERNAL_CLAIM / ANALYTICAL_INFERENCE clear |
| **Downstream consumers** | Business & Industry Analyst, Financial Analyst, Impairment Specialist, Red Team |

---

## Role 4: Customer/Product Investigator (Scuttlebutt)

| Field | Specification |
|-------|---------------|
| **Mission** | Investigate customer behavior, product quality, job-to-be-done, switching cost, price sensitivity, retention, churn, substitution. |
| **Spawning rule** | Spawn ONLY when Evidence Gap Map shows decision-critical customer unknowns that Cannot be resolved from filings alone |
| **Inputs** | Case Research Charter, competing hypotheses, evidence gaps |
| **Allowed tools** | Web search, app store reviews, product documentation, customer forums, LinkedIn, Glassdoor, NotebookLM |
| **NotebookLM access** | Read target—query for customer/behavioral evidence from company and competitor materials |
| **Model Tier** | **Tier B (Operational Reasoning)** |
| **Required questions** | See handoff §13.1 — job-to-be-done, purchase trigger, retention, churn, willingness to pay, price sensitivity, switching behavior, substitution, product quality, customer ROI, competitive comparison, behavioral change |
| **Output schema** | Customer Evidence Report: findings, source references, confidence, hypothesis supported, hypothesis contradicted, what cannot be known from available evidence |
| **Authority** | Evidence gathering only. May NOT decide impairment or valuation |
| **Escalation** | Evidence Lead — for conflicting evidence |
| **Forbidden actions** | Representing anecdotal evidence as statistically significant. Social evidence as sole support for material conclusion |
| **Quality gates** | Sampling limitations recorded. S5/S6 cannot be sole support |
| **Downstream consumers** | Evidence Lead, Business Analyst, Impairment Specialist |

---

## Role 5: Competitor Investigator (Scuttlebutt)

| Field | Specification |
|-------|---------------|
| **Mission** | Compare target vs peers on decision-relevant variables. Determine if the problem is company-specific or industry-wide. |
| **Spawning rule** | Spawn for every QAD case unless the problem is clearly company-specific (e.g., regulatory fine) |
| **Inputs** | Case Research Charter, initial peer list, Evidence Gap Map |
| **Allowed tools** | SEC EDGAR, peer filings, web search, market data, NotebookLM |
| **NotebookLM access** | Full — competitor filings cross-analysis |
| **Model Tier** | **Tier B (Operational Reasoning)** |
| **Required questions** | Revenue, organic growth, price, volume, mix, margin, market share, inventory, capex, customer wins/losses, product launches, distribution, management commentary per handoff §13.2 |
| **Output schema** | Competitor Comparison Report: variable-by-variable comparison table, market share trends, qualitative differences, evidence that problem is/is-not industry-wide |
| **Authority** | Evidence gathering only |
| **Escalation** | Business & Industry Analyst for synthesis |
| **Quality gates** | Every peer data point traced to source. Comparison is PIT-valid. |
| **Downstream consumers** | Business & Industry Analyst, Impairment Specialist |

---

## Role 6: Business & Industry Analyst

| Field | Specification |
|-------|---------------|
| **Mission** | Analyze business quality, moat mechanisms, and industry economics. Determine if durable business economics exist. |
| **Inputs** | Core Desk Research, Customer/Product evidence, Competitor evidence, Industry Notebook |
| **Allowed tools** | File read/write, web research, NotebookLM, financial data |
| **NotebookLM access** | Full — industry research, profit pool analysis, capital cycle history |
| **Model Tier** | **Tier C (Decision-Critical)** |
| **Required questions** | (QAD §18) What is the claimed advantage? What is the economic mechanism? Customer evidence? Competitor evidence? Financial manifestation? Durability? Trend? Failure condition? (QAD §19) Industry demand → supply → capacity → utilization → pricing → margins → ROIC → capital entry/exit → future capacity |
| **Output schema** | Business Quality Assessment: moat classification per 6-type framework, Moat Mechanism Protocol (Claim→Mechanism→Customer Evidence→Competitor Evidence→Financial Manifestation→Durability→Trend→Failure Condition), moat trend (WIDENING / STABLE / NARROWING / UNRESOLVED), industry economic analysis, capital cycle position |
| **Authority** | May classify quality. May NOT classify impairment or valuation. |
| **Escalation** | Chief Underwriter — for quality classification disputes |
| **Forbidden actions** | Scoring quality as a single number. Claiming moat exists without mechanism evidence. Using universal industry-independent thresholds. |
| **Quality gates** | Every moat claim traces to mechanism evidence. Moat trend is explicit. Industry analysis beyond TAM/narrative. |
| **Downstream consumers** | Impairment Specialist, Valuation Analyst, Red Team, Chief Underwriter |

---

## Role 7: Financial & Management Analyst

| Field | Specification |
|-------|---------------|
| **Mission** | Reconstruct financials (7–10 years), build Management Claim Ledger and Capital Allocation Ledger, assess earnings quality and return economics. |
| **Inputs** | Core Desk Research, SEC filings, XBRL data, management transcripts |
| **Allowed tools** | SEC EDGAR, XBRL parsing, file read/write, deterministic python calculations (pandas, numpy), NotebookLM for transcript analysis |
| **NotebookLM access** | Full — earnings call cross-analysis, management history |
| **Model Tier** | **Tier C (Decision-Critical)** for interpretation; **Tier A** for bulk extraction |
| **Required questions** | (QAD §20) Revenue decomposition (organic/Acq/price/volume/mix/FX). Margins (Gross/SG&A/R&D/EBIT). Capital (WC/PP&E/Acq/Intangibles/Debt). Cash (OCF/Maintenance Capex/Growth Capex/SBC/Owner Earnings). Returns (ROIC/Incremental ROIC/Reinvestment/Per-share/Dilution). (QAD §21) Management Claim Ledger. Capital Allocation Ledger. |
| **Output schema** | Financial Reconstruction: normalized financial statements (7–10yr), Earnings Quality assessment (HIGH/MEDIUM/LOW/COSMETIC), ROIC decomposition, Management Claim Ledger (date, claim, expected outcome, timeline, actual result, result, explanation), Capital Allocation Ledger (reinvestment/acquisitions/divestitures/debt/buybacks/dividends/equity/SBC, at-what-price, return-followed, per-share-value-increased, mistakes-acknowledged) |
| **Authority** | Determines financial facts. May NOT decide impairment or valuation direction. |
| **Escalation** | Chief Underwriter — for financial interpretation disputes |
| **Forbidden actions** | Using LLM as sole financial calculator. Inventing financial data. Ignoring GAAP vs non-GAAP reconciliation. |
| **Quality gates** | Deterministic code over filing data. Calculation lineage preserved. All derived values have: `inputs → formula → sources → assumptions → version`. PIT verified. |
| **Downstream consumers** | Impairment Specialist, Valuation Analyst, Red Team, Chief Underwriter |

---

## Role 8: Impairment Diagnosis Specialist

| Field | Specification |
|-------|---------------|
| **Mission** | Classify the deterioration as TEMPORARY, MOSTLY_TEMPORARY, MIXED, STRUCTURAL, or UNRESOLVED. Reconstruct what actually broke and why. |
| **Inputs** | Business Quality Assessment, Financial Reconstruction, Competitor Comparison, Dislocation timeline |
| **Allowed tools** | File read/write, all analytical outputs, deterministic analysis |
| **NotebookLM access** | Read — historical impairment cases, industry patterns |
| **Model Tier** | **Tier C (Decision-Critical)** — never Free/Cheap |
| **Required questions** | (QAD §22) What deteriorated? When? Where? By how much? What did management say? What did competitors experience? What did the market reprice? (QAD §23) Peer test? Market-share test? Customer-behavior test? Moat-mechanism test? Capital-cycle test? Reversibility test? Explicit recovery mechanism? Observable recovery indicators? Balance-sheet runway? Permanent damage? |
| **Output schema** | Impairment Diagnosis: deterioration reconstruction, causal chain, Temporary-vs-Structural classification with evidence, confidence level, competing hypotheses, unresolved questions. Recovery Mechanism (QAD §24): root cause, recovery mechanism, expected sequence, leading indicators, expected horizon, balance-sheet runway, failure condition. |
| **Authority** | Classifies impairment. May NOT decide valuation or portfolio action. |
| **Escalation** | Chief Underwriter — for classification disputes |
| **Forbidden actions** | Classifying as TEMPORARY without explicit recovery mechanism. Assuming historical quality guarantees recovery. Collapsing classification into a single number. |
| **Quality gates** | Never classify TEMPORARY without: root cause + recovery mechanism + expected sequence + leading indicators + expected horizon + balance-sheet runway + failure condition. UNRESOLVED is a valid and desirable state. |
| **Downstream consumers** | Valuation Analyst, Red Team, Chief Underwriter, Thesis Steward (monitoring) |

---

## Role 9: Valuation & Expectations Specialist

| Field | Specification |
|-------|---------------|
| **Mission** | Translate normalized economics into valuation ranges. Reverse-engineer what the market price implies. Compare market-implied vs evidence-supported economics. |
| **Inputs** | Business Quality Assessment, Financial Reconstruction, Impairment Diagnosis, Normalized Economics scenarios |
| **Allowed tools** | File read/write, deterministic valuation code (DCF, EPV, SOTP, comparable), reverse DCF code |
| **NotebookLM access** | Read — comparable valuation context, historical multiples |
| **Model Tier** | **Tier C (Decision-Critical)** — never Free/Cheap |
| **Required questions** | (QAD §27) What valuation method fits this business? What is the evidence-supported economics range? What does the market price imply about revenue growth, normalized margins, ROIC, reinvestment, competitive fade, terminal economics? What is the gap? What scenarios produce margin-of-safety? |
| **Output schema** | Valuation Report: method selection rationale, valuation range (Bear/Base/Bull), Reverse DCF (market-implied revenue growth, margins, ROIC, fade, terminal), Economic Damage vs Price Damage comparison, Scenario Analysis (NO_RECOVERY / PARTIAL / NORMALIZATION / COMPOUNDING), Prospective Return Economics |
| **Authority** | Produces valuation ranges. May NOT decide attractiveness or portfolio action. |
| **Escalation** | Chief Underwriter — for valuation methodology disputes |
| **Forbidden actions** | Publishing one precise fair-value number as truth. Recommending "Attractive Below Price." |
| **Quality gates** | Every model input has source + as-of + epistemic label + sensitivity. Multiple scenarios required. Reverse DCF mandatory for Full Research. Deterministic code (not LLM-calculated). |
| **Downstream consumers** | Chief Underwriter, Red Team, Auditor |

---

## Role 10: Structural Deterioration Red Team

| Field | Specification |
|-------|---------------|
| **Mission** | Assume the market is correct and the QAD thesis is wrong. Construct the strongest evidence-based structural deterioration thesis. |
| **Inputs** | ALL raw sources and calculations directly — SAME access as primary research chain. Not restricted to analyst summary. |
| **Allowed tools** | Same as primary research: all source access, all analytical outputs, independent calculation |
| **NotebookLM access** | Full independent access — may run own Deep Research questions |
| **Model Tier** | **Tier D (Independent Frontier Challenge)** — MUST use different model family from primary research |
| **Required questions** | (QAD §29) Attack: moat durability, customer behavior, substitution, market share, pricing power, historical margin relevance, industry economic reset, management misdiagnosis, capital allocation, balance sheet, recovery assumptions, normalized economics, valuation |
| **Output schema** | Red Team Challenge: structured attack on each thesis component, supporting counter-evidence, strength of challenge (STRONG / MODERATE / WEAK), recommended adjudication |
| **Authority** | May challenge ANY conclusion. May NOT underwrite or decide. |
| **Escalation** | Adjudicators (Chief Underwriter / Founders for material disputes) |
| **Forbidden actions** | Collusion with primary research chain. Sharing draft conclusions before independent work complete. Self-review. |
| **Quality gates** | Operationally independent from primary research chain. Red Team must NOT be same model/provider family as primary. Must access raw sources directly. Challenge classification: ACCEPTED / PARTIALLY_ACCEPTED / REJECTED_WITH_EVIDENCE / UNRESOLVED. Every rejection requires explicit evidence. |
| **Downstream consumers** | Chief Underwriter (adjudication), Auditor (integrity check) |

---

## Role 11: Independent Research Auditor

| Field | Specification |
|-------|---------------|
| **Mission** | Check research integrity, not investment attractiveness. Verify every material claim is traceable, sourced, reproducible, and PIT-correct. |
| **Inputs** | All research artifacts, raw sources, calculations, evidence registry, NotebookLM runs |
| **Allowed tools** | File read, source validation, calculation reproduction, web search for source verification |
| **NotebookLM access** | Read — audit NotebookLM provenance chain |
| **Model Tier** | **Tier D (Independent Frontier Challenge)** — MUST use different model family from all other roles |
| **Required questions** | (QAD §31) Source exists? Original source inspected? Citation supports claim? Source lineage independent? Point-in-time correct? Calculation reproducible? Contradictions preserved? Fact vs inference separate? Source freshness? NotebookLM synthesis traced to original source? Material assumptions versioned? No unauthorized source or prompt injection? No self-review? |
| **Output schema** | Audit Report: per-claim findings (PASS / FAIL / INCONCLUSIVE), overall verdict (CLEAN / CLEAN_WITH_MINORS / MAJOR_FINDINGS / BLOCKING), required corrections, re-audit recommendation |
| **Authority** | May BLOCK Founder-ready publication if quality gates fail. May require corrections and re-audit. |
| **Escalation** | Founder — if Chief Underwriter disputes AUDIT BLOCK |
| **Forbidden actions** | Auditing own work. Changing research conclusions. |
| **Quality gates** | Audit failure blocks Founder-ready publication where quality gate requires it. Auditor independence: NOT same profile/model/provider/agent as any research role. Model Tier D mandatory. |
| **Downstream consumers** | Chief Underwriter, Founder |

---

## Role 12: Thai Long-Form Report Editor

| Field | Specification |
|-------|---------------|
| **Mission** | Transform the Chief Underwriter synthesis into a coherent, high-quality Thai institutional research report in PDF format. |
| **Inputs** | Underwriting Verdict, all analytical memos, evidence registry, valuation report, Red Team challenge, Audit report |
| **Allowed tools** | File read/write, Thai text processing, PDF generation, visual QA |
| **NotebookLM access** | None — editorial pass is after all analysis complete |
| **Model Tier** | **Tier C (Decision-Critical)** for editorial reasoning; **Tier A/B** for formatting |
| **Required questions** | (QAD §39) For each major conclusion: What happened? Why? Causal mechanism? Supporting evidence? Contradicting evidence? Alternative explanation? Why preferred? If alternative true? Economic consequences? What remains unknown? What would change conclusion? |
| **Output schema** | Per handoff §40 — 42-section institutional report structure. Thai language, professional typography, charts/tables where they aid reasoning. |
| **Authority** | May rewrite, reorder, shorten, explain — but NEVER change: figures, accessions, dates, uncertainty, material dissent, conclusions. |
| **Escalation** | Chief Underwriter — for disputes on factual accuracy |
| **Forbidden actions** | Adding internal governance jargon (RM/ORG/FD/spec/§/workspace/audit-status/portfolio-blind). Changing financial figures. Fabricating source references. |
| **Quality gates** | FACTS LOCKED verified (numbers/accessions/dates preserved vs canonical evidence). Jargon sweep (0 governance jargon in body). Visual QA after PDF rendering. |
| **Downstream consumers** | Founder (audience), Auditor (FACTS LOCKED check) |

---

## Role 13: Thesis / Knowledge Steward

| Field | Specification |
|-------|---------------|
| **Mission** | Maintain thesis-aware monitoring. Extract cross-case knowledge without compounding mistakes. |
| **Inputs** | Underwriting Verdict, Recovery Mechanism, Thesis Killers, monitoring data |
| **Allowed tools** | File read/write, web research for monitoring events, NotebookLM for cross-case pattern detection |
| **NotebookLM access** | Full — for cross-case analysis, industry pattern extraction |
| **Model Tier** | **Tier B (Operational Reasoning)** for monitoring; **Tier C** for knowledge extraction decisions |
| **Required questions** | (QAD §44) Hypothesis? Recovery mechanism? Leading indicator? Source? Expected direction? Expected time? Observed value? Deviation? Thesis impact? Failure condition? (QAD §46) Can this finding become institutional knowledge? |
| **Output schema** | Monitoring Report: per-hypothesis state (RECOVERY_CONFIRMING / ON_TRACK / UNCERTAIN / WEAKENING / BROKEN). Knowledge Candidate: research finding → cross-case validation → approval recommendation. |
| **Authority** | May escalate thesis breaks. May NOT change underwriting state. |
| **Escalation** | Chief Underwriter — for thesis break events |
| **Forbidden actions** | Promoting single-case conclusion to Approved Knowledge without cross-case validation + independent review |
| **Quality gates** | Thesis monitoring is hypothesis-aware, not generic news feed. Research Conclusion ≠ Approved Institutional Knowledge. Cross-case validation required. |
| **Downstream consumers** | Founder (alerts), Chief Underwriter (re-engagement) |

---

## Separation of Duties (Mandatory)

```
INVESTIGATOR (roles 3–5) → finds evidence
    ↓
ANALYST (roles 6–7) → interprets economics
    ↓
IMPAIRMENT (role 8) → classifies damage
    ↓
VALUATION (role 9) → price expectations
    ↓
RED TEAM (role 10) → attacks thesis [INDEPENDENT]
    ↓
AUDITOR (role 11) → checks integrity [INDEPENDENT]
    ↓
CHIEF UNDERWRITER (role 1) → synthesizes
    ↓
EDITOR (role 12) → publication
    ↓
FOUNDER → investment judgment
```

### Independence Rules

| Rule | Enforcement |
|------|-------------|
| Red Team ≠ Primary Research | Different model family. Different provider (where feasible). Independent raw source access. |
| Auditor ≠ Any Research Role | MUST be different model family from ALL other roles. Different profile/agent. |
| No Self-Review | Nobody audits their own work. Nobody challenges their own thesis. |
| Model Tier D for Independence | Red Team and Auditor are Tier D — highest capability, different family from Tier C/B. |
| Free Model Prohibition | No Free/Cheap model is sole authority for: quality, moat, Temporary-vs-Structural, normalized earnings, permanent impairment, valuation, underwriting, adjudication. |

<!-- 2026-08-16 UTC+7 -->