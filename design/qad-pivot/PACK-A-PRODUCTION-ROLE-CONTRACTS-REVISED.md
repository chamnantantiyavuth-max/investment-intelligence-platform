# Pack A — QAD Production Role Contracts (Revised)

> **Status:** Resolution round — corrected for Pre-Code Design Gate.
> **Key changes from v1:**
> - Autonomous Selection Engine (policy-driven) separated from Chief Underwriter
> - Research Director (new role) between Selection and Underwriting
> - Research Budget Controller (policy/service, not agent)
> - 3-tier termination authority
> - Red Team has NO veto
> - False Quality gate responsibilities added
> - Impairment Analyst produces dual/competing explanations, Red Team starts from raw evidence

---

## Role Architecture (Revised)

```
AUTONOMOUS SELECTION ENGINE (policy-driven, deterministic)
           │
           │ Hard Gates + Priority Ordering
           ▼
CASE OPENER (policy service)
           │
           ▼
    RESEARCH DIRECTOR (Role 1a)
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
EVIDENCE      ANALYSIS
BUILDING      PHASE
    │             │
    └──────┬──────┘
           ▼
    IMPAIRMENT DIAGNOSIS (Role 8)
           │
           ▼
    NORMALIZATION & VALUATION (Role 9)
           │
           ▼
    STRUCTURAL RED TEAM (Role 10) [INDEPENDENT]
           │
           ▼
    CHIEF UNDERWRITER (Role 1b) [ADJUDICATION]
           │
           ▼
    AUDITOR (Role 11) [INTEGRITY CHECK]
           │
           ▼
    THAI EDITOR (Role 12)
           │
           ▼
    FOUNDER
```

---

## Role 1a: Research Director

| Field | Specification |
|-------|---------------|
| **Mission** | Lead research execution. Propose judgment-based terminations. Ensure research quality, scope adherence, and timeline. |
| **Inputs** | Opened case (from Selection Engine), Research Charter, all analytical outputs |
| **Allowed tools** | File read/write, delegation to sub-roles, read-only access to Evaluation Registry |
| **NotebookLM access** | Read — context only |
| **Model Tier** | Tier C (Decision-Critical) |
| **Required questions** | Is research on track? Are there scope violations? Does termination need consideration? Has expected information value been met? |
| **Authority** | Propose judgment-based termination (Chief Underwriter confirms). Submit budget escalation with Expected Information Value justification (Research Budget Controller applies policy). May NOT select candidates for research. May NOT overrule Chief Underwriter adjudication. Chief Underwriter/Founder budget involvement only for exceptional threshold exceedance. |
| **Escalation** | Chief Underwriter — for termination and scope disputes. Research Budget Controller — for budget escalation within policy. |
| **Forbidden actions** | Selecting own cases. Overruling Red Team without recorded evidence. Publishing before Auditor clears. |
| **Quality gates** | Research execution stays within Charter scope; stage-specific gates tracked stage-to-stage; Research Director cannot declare final publication readiness (that gate belongs to Chief Underwriter + Auditor chain). |
| **Downstream consumers** | Chief Underwriter, Auditor |

---

## Autonomous Selection Engine (Not a Role — Policy-Governed Service)

| Field | Specification |
|-------|---------------|
| **Mission** | Apply approved Hard Gates + Priority Ordering to Quality Discovery output. Determine candidate outcome. |
| **Nature** | **Policy-governed, auditable autonomous selection service.** Analytical/judgment-bearing components produce structured gate inputs (Quality status, Researchability, Temporary hypothesis, Structural alternative, Survivability, Valuation Relevance). The approved selection policy and state transition operate deterministically over those validated structured inputs. |
| **Inputs** | Structured gate inputs from analytical components (not raw model output) |
| **Hard Gates** | (1) Quality plausibility, (2) Material dislocation, (3) Identifiable economic problem, (4) Plausible temporary explanation, (5) Plausible structural alternative, (6) Researchability, (7) Survivability, (8) Preliminary valuation relevance |
| **Architecture** | `Evidence/Analysis → Structured Gate Inputs → Approved Selection Policy → Deterministic State Transition` |
| **Provenance** | Every judgment-bearing gate input preserves full provenance: which role/process produced it, which evidence supported it, which model tier was involved, timestamp. |
| **Priority Ordering** | (1) Verified Quality > Probable Quality, (2) Higher researchability, (3) Larger gap between Price Damage and Permanent Economic Damage, (4) Higher Temporary-vs-Structural uncertainty, (5) Stronger balance sheet, (6) Fresher dislocation |
| **Candidate Outcomes** | `AUTO_RESEARCH_NOW` / `WATCH_FOR_PRICE` / `WATCH_FOR_EVIDENCE` / `DATA_LIMITED_WATCH` / `REJECT` |
| **Authority** | Opens cases autonomously. Selection policy is Foundation-approved. Every selection logged with full provenance. |
| **Relationship to Chief Underwriter** | NONE — the Chief Underwriter has NO say in which cases enter the system. This eliminates the selection bias. |

---

## Role 1b: Chief Underwriter

| Field | Specification |
|-------|---------------|
| **Mission** | Synthesize all analytical work. Adjudicate Red Team challenges. Produce underwriting verdict. Confirm judgment-based terminations. |
| **Inputs** | Full analytical output from Research Director, Impairment Diagnosis, Valuation, Red Team challenges, Audit report |
| **Allowed tools** | File read/write, read-only access to all sources and calculations |
| **NotebookLM access** | Read — context only |
| **Model Tier** | **Tier C (Decision-Critical)** — never Free/Cheap |
| **Required questions** | What is the strongest case for each impairment classification? Has the Red Team been properly addressed? Is the evidence chain complete? What is the underwriting verdict? Does this case justify the research cost? |
| **Output schema** | Underwriting Verdict: verdict (QAD_CONFIRMED / QAD_PROBABLE / QAD_UNRESOLVED / NOT_QAD_STRUCTURAL / NOT_QAD_QUALITY / NOT_QAD_VALUATION), synthetic narrative, key unknowns, thesis killers |
| **Authority** | Adjudicate Red Team challenges (ACCEPT / PARTIAL / REJECT_WITH_EVIDENCE / UNRESOLVED). Confirm judgment-based termination (proposed by Research Director). Publish as Founder-Ready. May NOT select candidates for research (Selection Engine is independent). |
| **Escalation** | Founder — for unresolved material disputes, contested termination, or Red Team challenges that cannot be adjudicated |
| **Relationship to Selection Engine** | NONE — cases arrive already opened. The Underwriter adjudicates the result of research, NOT the selection of what to research. |
| **Forbidden actions** | Selecting own cases. Overruling Red Team without recorded evidence. Publishing before Auditor clears. |
| **Quality gates** | All analytical stages complete. Red Team adjudicated. Auditor passed. |

---

## Role 2: Evidence Intelligence Lead (Unchanged from v1)

… (content identical to v1 — mission, inputs, tools, questions, output, authority, escalation, forbidden actions, quality gates, downstream consumers remain the same)

---

## Role 3: Core Desk Research (Unchanged from v1)

… (content identical)

---

## Role 4: Customer/Product Investigator (Unchanged from v1)

… (spawning rule: max 3 concurrency default. >3 requires Research Director expected-information-value justification → Budget Controller applies policy; Evidence Gap ID required before spawning)

---

## Role 5: Competitor Investigator (Unchanged from v1)

…

---

## Role 6: Business & Industry Analyst (Updated — Now Includes False Quality Gate)

| Field | Specification |
|-------|---------------|
| **Mission** | Analyze business quality, moat mechanisms, and industry economics. Determine if durable business economics exist. **Perform mandatory QUALITY_VERIFICATION before impairment analysis.** |
| **Inputs** | Core Desk Research, Customer/Product evidence, Competitor evidence, Industry Notebook |
| **Key addition: QUALITY_VERIFICATION** | MUST answer: (a) What actually created historical excess economics? (b) Was the mechanism durable or transient? (c) Was historical quality caused by cycle, leverage, accounting, scarcity, temporary regulation, or another transient factor? (d) Is there customer/competitor evidence supporting genuine durability? (e) Does financial manifestation match the claimed moat? |
| **Quality states** | `VERIFIED` — durable mechanism confirmed. `PROBABLE` — evidence points to quality but uncertainty remains. `UNRESOLVED` — cannot determine; may trigger targeted evidence acquisition. `FAILED` — historical quality was misinterpreted → hard QAD rejection. |
| **False-quality hypothesis** | MUST explicitly test: "The company was never genuinely high quality; historical economics were misinterpreted." This is a mandatory alternative hypothesis. |
| **Output schema** | Business Quality Assessment + Quality Verification Statement |
| **Downstream consumers** | Impairment Specialist, Research Director, Chief Underwriter |

---

## Role 7: Financial & Management Analyst (Unchanged from v1)

…

---

## Role 8: Impairment Diagnosis Specialist (Revised — Anti-Anchoring)

| Field | Specification |
|-------|---------------|
| **Mission** | Classify deterioration. **Produce dual/competing explanations to prevent anchoring.** |
| **Required output** | (1) **Primary Diagnosis**: TEMPORARY / MOSTLY_TEMPORARY / MIXED / STRUCTURAL / UNRESOLVED with evidence chain. (2) **Strongest Competing Explanation**: the most credible alternative classification with evidence. (3) **Why Primary Currently Dominates**: explicit reasoning for preferring primary over competing. (4) **Weakest Link in Primary Diagnosis**: what part of the primary diagnosis has the weakest evidence. (5) **Evidence That Would Flip the Classification**: specific evidence that would change the diagnosis. |
| **Red Team independence** | Red Team (Role 10) begins from: Research Charter, validated Evidence Graph, financial facts, original sources — **NOT from Role 8's full narrative**. Role 8's reasoning is preserved for comparison AFTER Red Team produces its independent analysis. This prevents the primary analyst's framing from anchoring the Red Team. |
| **Quality gates** | TEMPORARY requires recovery mechanism. UNRESOLVED is valid. |

---

## Role 9: Valuation & Expectations Specialist (Unchanged from v1)

…

---

## Role 10: Structural Deterioration Red Team (Revised — No Veto)

| Field | Specification |
|-------|---------------|
| **Mission** | Assume the market is correct and the QAD thesis is wrong. Construct the strongest evidence-based structural deterioration thesis. |
| **Inputs** | Research Charter, validated Evidence Graph, financial facts, original sources — **NOT the full Impairment Analyst narrative** (prevents anchoring). |
| **Authority** | May challenge ANY conclusion. **Does NOT have veto over publication, underwriting, or case continuation.** Produces challenges with strength classification (STRONG/MODERATE/WEAK) and recommended adjudication. |
| **Adjudication** | Chief Underwriter adjudicates: ACCEPTED / PARTIALLY_ACCEPTED / REJECTED_WITH_EVIDENCE / UNRESOLVED. Every rejection requires explicit evidence. If material disagreement cannot be resolved, classify as UNRESOLVED or escalate to Founder. |
| **Forbidden actions** | Vetoing publication. Overruling Chief Underwriter. Collusion with primary research. |

---

## Role 11: Independent Research Auditor (Revised — Budget Removed)

| Field | Specification |
|-------|---------------|
| **Mission** | Check research integrity. **Does NOT approve compute budgets or manage operations.** |
| **Scope** | Source exists? Original source inspected? Citation supports claim? PIT correct? Calculation reproducible? Contradictions preserved? NotebookLM provenance checked? No self-review? |
| **Budget role** | **NONE** — Auditor does not approve, deny, or manage research budgets. Auditor verifies AFTER the fact that budget overrides were properly authorized, logged, and within policy. Budget management is handled by Research Budget Controller. |
| **Authority** | May BLOCK Founder-ready publication if quality gates fail. May require corrections and re-audit. |
| **Escalation** | Founder — if Chief Underwriter disputes AUDIT BLOCK |

---

## Research Budget Controller (Not a Role — Policy Service)

| Field | Specification |
|-------|---------------|
| **Mission** | Enforce research budgets. Route override requests. |
| **Nature** | **Policy/service** — NOT an agent. NOT a role. |
| **Behavior** | Base budget per case → soft limit reached → Research Director provides expected-information-value justification → hard limit reached → escalation request → Chief Underwriter exceptional extension request → policy approval or Founder threshold → budget override logged. |
| **Auditor relationship** | Auditor verifies post-hoc that overrides were properly authorized and logged. Auditor does NOT approve budgets. |

---

## Termination Authority (Revised — 3 Tiers)

| Tier | Type | Authority | Process |
|------|------|-----------|---------|
| **A** | HARD / DETERMINISTIC FAIL | Automatic | Unusable financial data, explicit hard balance-sheet failure, clearly absent researchability, hard universe violation. Automated. Logged. Reviewable. |
| **B** | JUDGMENT-BASED | Research Director proposes → Chief Underwriter confirms | Quality thesis weakening, evidence gap becoming insurmountable, resource not justified by expected value. |
| **C** | CONTESTED MATERIAL | Auditor checks process → unresolved → Founder | Material disagreement on termination grounds. Auditor reviews process integrity, not case merit. |

---

## Role 12: Thai Long-Form Report Editor (Unchanged from v1)
## Role 13: Thesis / Knowledge Steward (Unchanged from v1)

---

## Separation of Duties (Revised)

```
SELECTION ENGINE (policy, deterministic — independent of judgment roles)
    ↓
RESEARCH DIRECTOR (execution management)
    ↓
INVESTIGATORS → ANALYSTS → IMPAIRMENT → VALUATION
    ↓
STRUCTURAL RED TEAM [INDEPENDENT — starts from raw evidence]
    ↓
CHIEF UNDERWRITER [ADJUDICATION — including Red Team challenges]
    ↓
AUDITOR [INTEGRITY CHECK — no budget/management role]
    ↓
EDITOR → FOUNDER
```

| Independence Rule | Enforcement |
|------------------|-------------|
| Selection ≠ Underwriting | Selection Engine is policy-driven. Chief Underwriter has NO influence on case selection. |
| Red Team ≠ Primary Analysis | Red Team starts from raw sources, not analyst narrative. Different model family (Tier D). |
| Auditor ≠ Budget/Management | Auditor checks integrity only. Budget Controller is a separate policy service. |
| No Self-Review | Nobody audits own work. Nobody selects own cases. Nobody adjudicates own challenges. |
| Red Team has NO veto | Red Team produces challenges, not blocks. |

<!-- 2026-08-16 UTC+7 -->