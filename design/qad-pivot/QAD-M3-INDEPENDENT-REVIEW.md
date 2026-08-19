# QAD-M3 Independent Design Consistency Review

**Reviewer:** Premium Independent Reviewer (design-contract phase)
**Date:** 2026-08-19
**Status:** PASS_WITH_FINDINGS

## Verdict Summary

The QAD-M3 domain contracts (M3-01 through M3-10) and design artifacts (Logical Organization, Role Contracts, Service Contracts, Workforce Migration Map) form a coherent, well-structured design-contract package. The separation-of-duties architecture is the strongest aspect — multiple explicit guardrails prevent role self-review, selection-underwriting collusion, NotebookLM output bypassing canonical validation, L10 evidence supporting material conclusions, budget exhaustion weakening quality gates, and silent skip of Red Team/Audit. No hidden investment authority was found, and all M2 capability dispositions are faithfully consumed.

Three findings were identified, all minor-to-medium materiality: (1) the Research Director approves their own Research Charter scope without a mandatory independent reviewer, (2) a classification counting inconsistency in the Logical Organization summary table, and (3) a Case schema field definition split across two contracts that M4A will need to reconcile. None of these findings block M3 closeout or M4A/M4B readiness, but they should be corrected for design hygiene.

The contracts are M4A/M4B-ready: every contract includes explicit schema derivation notes, enums are precise, and evaluation metrics are contract-specified with threshold calibration explicitly deferred to M4B.

---

## Question-by-Question Findings

### Q1: Self-Review?

**Verdict: FINDING**

**Details:** The Research Director (Role 1, M3-ROLES) is responsible for creating and approving the Research Charter, which defines the case scope, H1–H5 hypotheses, analytical modules, and methodology. M3-03 §2.3 lists "Research Director approval" as a Charter field. The RD's AUTHORITY block (M3-ROLES Role 1) says "Assign analytical modules, define scope, set evidence standards for the case." The QUALITY_GATE says "Research Charter must be reviewed" but does not specify an independent reviewer — by default this implies the RD reviews their own Charter.

The Charter sets the research direction, hypothesis framing, and evidence standards for the entire case. Approving one's own scope without a second set of eyes creates a self-review risk: the RD could unconsciously narrow scope to confirm their initial hypothesis, eliminate inconvenient lines of inquiry, or set evidence standards that favor a predetermined outcome. This is the weakest link in an otherwise robust separation-of-duties architecture.

**Evidence:** M3-03 §2.3 (Research Charter fields — "Research Director approval"), M3-ROLES Role 1 AUTHORITY + QUALITY_GATE, M3-LOGICAL §5 (separation matrix does not address Charter self-approval).

**Recommended correction:** Add an independent Charter reviewer. The simplest fix: require the Research Charter to be reviewed by a second logical role (either the Chief Underwriter for scope validation, or the Evidence Intelligence Lead for methodology completeness) before analytical work begins. Update M3-ROLES Role 1 QUALITY_GATE and M3-03 §2.3 to name the reviewer explicitly. The Charter should have states: DRAFT → PEER_REVIEWED → APPROVED.

**Materiality: MEDIUM** — Affects front-end research governance. The Charter frames everything downstream. However, the architecture explicitly preserves dissent and competing hypotheses (H1–H5 must exist), partially mitigating the risk of scope anchoring.

---

### Q2: Hidden Investment Authority?

**Verdict: PASS**

**Details:** Every role's FORBIDDEN_ACTIONS (M3-ROLES) explicitly prohibits investment/portfolio activities. The Chief Underwriter (Role 8) "Cannot allocate capital, cannot size positions, cannot execute trades, cannot create FOUNDER_ENDORSED state." The Valuation Specialist (Role 7) "Cannot produce a single 'fair value,' cannot issue buy/sell/hold recommendation, cannot set position size." M3-08 §6 explicitly prohibits single-point fair values and buy/sell/hold ratings. M3-09 §4.4 enumerates five Underwriter prohibitions. M3-01 §5.2 reserves all investment authority to Founder alone. Verdict states (QAD_CONFIRMED, etc.) are explicitly diagnostic, not prescriptive. The architecture maintains a clean boundary between research output and capital allocation.

**No hidden investment authority detected.**

---

### Q3: Is Any Service Incorrectly Modeled as an Agent?

**Verdict: FINDING**

**Details:** The Discovery Scout is classified as `HUMAN_OR_AGENT_JUDGMENT_ROLE (TRANSITIONAL)` in:
- M3-ROLES Role 13 (correctly — its function involves interpreting anomalies, raising discovery signals, and exercising judgment about materiality)
- M3-LOGICAL §3.1 detailed classification table (correct — `HUMAN_OR_AGENT_JUDGMENT_ROLE`)

However, M3-LOGICAL §4 (Classification Summary table) lists Discovery Scout under `POLICY_SERVICE` with count 4:
> "POLICY_SERVICE | 4 | Selection Engine, Candidate Builder, Research Budget Controller, **Discovery Scout (transitional)**"

This contradicts §3.1 and the Role Contract. The count is wrong: POLICY_SERVICE should be 3 (not 4), and HUMAN_OR_AGENT_JUDGMENT_ROLE should be 11 (not 10). The 29-component total is preserved, but the per-category counts are inaccurate.

**Recommended correction:** Move Discovery Scout from `POLICY_SERVICE` to `HUMAN_OR_AGENT_JUDGMENT_ROLE` in M3-LOGICAL §4 Classification Summary. Update the counts accordingly.

**No misclassified service-to-agent or agent-to-service conversions found** — the Discovery Scout is correctly classified as a judgment role in the authoritative Role Contract; only the summary table is wrong.

**Materiality: MINOR** — Documentation inconsistency that does not affect contract semantics. However, M4A/M4B implementers reading the summary table alone could misunderstand the Discovery Scout's authority boundaries.

---

### Q4: Can Selection and Underwriting Collude Through Shared Authority?

**Verdict: PASS**

**Details:** The separation is enforced at multiple levels:

1. **Domain contract level** (M3-02 §4.2): "Selection Engine is separate from Chief Underwriter" and "Chief Underwriter must not select its own cases"
2. **Logical Organization level** (M3-LOGICAL §5): "Selection Engine | Chief Underwriter | ❌ No | Selection ≠ Underwriting"
3. **Role Contract level** (M3-ROLES Role 8): FORBIDDEN_ACTIONS includes "Cannot select own cases (Selection Engine is separate)"
4. **Role Combination Matrix** (M3-ROLES): "8 Underwriter + anything else | ❌ No"
5. **Workforce Migration Map** (M3-MIGRATION §3.3): "Chief Underwriter (Role 8) | Cannot Combine With: Any research role, any selection role"
6. **Service level** (M3-SERVICES Service 1): "Must NOT use AI judgment"

There is no path where Selection Engine and Chief Underwriter share a profile, agent, or authority. The Underwriter cannot even share a profile with any other role, making collusion architecturally impossible.

---

### Q5: Can NotebookLM Output Bypass Canonical Validation?

**Verdict: PASS**

**Details:** The validation chain is robust and multilayered:

1. **M3-03 §5.2 Rule:** "Material finding discovered through NotebookLM or another AI synthesis must be validated against original source before canonical admission." Four-step procedure: (a) validate against original source, (b) ingest source into Raw Source Archive, (c) create Fact in Canonical Evidence Registry, (d) record both AI synthesis and source validation in provenance.

2. **M3-04 §5.3 (AI Synthesis Validation Rule):** Same four-step procedure, independently specified.

3. **M3-04 §5.1 (Admission Rules):** "Source exists: Source must be ingested in Raw Source Archive"; "PIT compliance: No evidence with date after as_of_date"

4. **M3-SERVICES Service 10 (NotebookLM Interface):** FORBIDDEN: "Output is NONCANONICAL — must NOT be admitted to Evidence Registry without independent source validation"

5. **M3-01 §3.4 (Canonical Boundary):** "AI internal reasoning | ❌ Noncanonical | Never stored as canonical truth"

6. **M3-ROLES Role 2 (Evidence Intelligence Lead):** SEPARATION_OF_DUTY requires different agent for discovery vs admission

NotebookLM output is quarantined as a noncanonical discovery layer. It cannot independently enter the Evidence Registry. No path bypasses the Admission Gate.

---

### Q6: Can Social Evidence (L10) Directly Become Thesis Truth?

**Verdict: PASS**

**Details:** L10 evidence is comprehensively quarantined from material conclusions:

**M3-04 §2.2 (L10 Rule):**
- "L10 evidence cannot independently support a material conclusion"
- L10 may: generate discovery leads, suggest investigation, corroborate higher-tier evidence
- L10 may NOT: be cited as primary support for quality/dislocation/impairment/valuation claims, be the sole evidence for a material conclusion, enter Evidence Registry without L10-origin validation note

**M3-04 §5.1 (Admission Gate):** "Source tier: L10 alone cannot support material conclusions"

**M3-ROLES Role 2:** FORBIDDEN_ACTIONS "Cannot admit L10 evidence as material support"

**M3-05 §5.2 (Evidence Admission Path):** Scuttlebutt findings pass through same Admission Gate with tier check

The design is explicit and comprehensive. L10 can generate discovery leads (Lane C) but cannot independently influence any QAD proposition.

---

### Q7: Can Budget Exhaustion Reduce Quality Gates?

**Verdict: PASS**

**Details:** Multiple explicit guardrails prevent budget exhaustion from weakening quality gates:

1. **M3-01 §6.1:** INCOMPLETE is defined as "NOT a weakened quality gate — output is marked INCOMPLETE and downstream stages must account for missing inputs"
2. **M3-01 §6.2 (Cardinal Rule):** "Failure must never silently become completeness. No automatic fallback that weakens quality gates. Downstream stages see STAGE_INCOMPLETE or STAGE_FAILED dependencies."
3. **M3-01 §6.3:** "After exhaustion → FAILED or INCOMPLETE (not weakened quality)"
4. **M3-SERVICES Service 8:** FORBIDDEN "Must NOT weaken quality gates on budget exhaustion"
5. **M3-03 §6:** "Budget exhausted: Case marked INCOMPLETE — Not a weakened-quality state"
6. **M3-09 Role 8 QUALITY_GATE:** "All preceding stages COMPLETED (not INCOMPLETE unless gap documented)" — allows INCOMPLETE with explicit documentation, not silence

The stage state machine (M3-01 §3.3) keeps COMPLETED, FAILED, INCOMPLETE, and SKIPPED as distinct states. INCOMPLETE is visible to all downstream stages. The Run Manifest records the exact budget state. No path exists where budget exhaustion produces a false COMPLETED.

---

### Q8: Can a Case Reach Founder Without Red Team/Audit Where Required?

**Verdict: PASS**

**Details:** The path to FOUNDER_READY requires both Red Team and Audit:

1. **M3-09 §4.2:** Red Team Assessment and Audit Report are mandatory Underwriter inputs
2. **M3-09 Role 8 QUALITY_GATE:** "Red Team assessment exists; Audit PASS or findings resolved"
3. **M3-09 §5.4:** "Auditor must have PASS or PASS_WITH_MINORS before FOUNDER_READY"
4. **M3-09 §3.2:** Auditor "May block FOUNDER_READY"

The only authorized skip mechanism is M3-01 §7.3: "Skip a stage | Founder | Must document rationale." This is Founder-only — no other role can authorize skipping Red Team or Audit. The override is transparent (documented in manifest).

No silent skip path exists. Red Team output is "a mandatory input to Chief Underwriting" (M3-09 §2.4). The Auditor's authority to block FOUNDER_READY is non-delegable and reports directly to Founder, bypassing the Research Director and Chief Underwriter (M3-01 §7.2).

---

### Q9: Is Any M2 Capability Silently Reclassified?

**Verdict: PASS**

**Details:** Every M2 capability consumed by M3 contracts was verified against the M2 registry (QAD-M2-LEGACY-CAPABILITY-REGISTRY.md):

| M2 Capability | M2 Disposition | M3 Consumption | Match? |
|---|---|---|---|
| CAP-001 Shared Equity Universe | REUSE | REUSE (M3-02) | ✓ |
| CAP-002 Equity Inflection | ADAPT | ADAPT (M3-02) | ✓ |
| CAP-003 Quality & Asymmetry | ADAPT | ADAPT (M3-02) | ✓ |
| CAP-009 CIW | ABSORB | ABSORB (M3-03, M3-10) | ✓ |
| CAP-011 Radar Scout | TRANSITIONAL_RETAIN | TRANSITIONAL_RETAIN (M3-02) | ✓ |
| CAP-012 Deep Research Contract | REUSE | REUSE (M3-04, M3-10) | ✓ |
| CAP-014 Thai Editorial Standard | REUSE | REUSE (M3-10) | ✓ |
| CAP-015 Live Office | REUSE | REUSE (M3-10) | ✓ |
| CAP-016 Audit Infrastructure | REUSE | REUSE (M3-10) | ✓ |
| CAP-017 Evidence Doctrine | REUSE | REUSE (M3-04) | ✓ |
| CAP-018 Hermes Workforce | TRANSITIONAL_RETAIN | TRANSITIONAL_RETAIN (M3-LOGICAL) | ✓ |

All 11 consumed capabilities match their M2 dispositions exactly. No capability is silently reclassified, downgraded, or upgraded without Foundation-aligned documentation.

The M3 contracts faithfully preserve each capability's lifecycle state and disposition as declared in the M2 registry.

---

### Q10: Can M4A/M4B Implement Contracts Deterministically?

**Verdict: FINDING**

**Details:** Overall, the contracts are M4A/M4B-ready with 9 of 10 contracts providing clear, complete schema derivation notes. However, one coordination gap exists:

**Case schema fields split across M3-01 and M3-03:**

M3-01 §11 (M4A Readiness Note) lists Case schema with: `case_id, version, company_id, as_of_date, stage_state map, manifest_id`

M3-03 §7 (M4A Readiness Note) lists Case schema with: `case_id, company_id, dislocation_event_id, entry_route, as_of_date, stage_state, charter`

M3-03 §2.2 adds further fields not listed in either M4A note: `opened_at (timestamp)`, `research_run_id`

An M4A implementer reading only one contract would produce an incomplete schema. The fields are compatible (they can be merged into a single `Case` record), but neither contract cross-references the other as the authoritative source for Case fields. M4A must recognize that Case is defined by the union of M3-01 and M3-03.

**All other aspects pass the determinism check:**
- Every contract has an explicit M4A Readiness Note with specific schema names and fields
- Enums are precise (Quality states, Impairment states, Scenario types, Verdict states, Monitoring states, Audit outcomes, Red Team outcomes)
- M3-10 §4.7 explicitly defers threshold calibration to M4B: "M3 does NOT set quantitative pass thresholds. M4B calibrates." — proper boundary between contract and calibration
- Service Contracts specify failure behavior, retry behavior, authority, and forbidden inference for all 13 services
- Role Contracts use a mandatory template with 16 fields including AUTHORITY, FORBIDDEN_ACTIONS, SEPARATION_OF_DUTY, and QUALITY_GATE

**Recommended correction:** Add a cross-reference in M3-01 §11 and M3-03 §7 clarifying that the Case schema is defined jointly across both contracts. Alternatively, designate one contract as the authoritative Case schema definition and have the other reference it.

**Materiality: MINOR** — The fields are compatible and can be merged, but M4A needs to know to read both contracts for the complete Case schema.

---

## Required Changes

| # | Finding | Correction | Owner | Materiality |
|---|---------|------------|-------|-------------|
| 1 | Q1 — Research Director approves own Research Charter without mandatory independent reviewer | Add independent reviewer (Chief Underwriter or Evidence Intelligence Lead) to Charter approval flow; update M3-03 §2.3 and M3-ROLES Role 1 QUALITY_GATE | M3 Domain Contract author | MEDIUM |
| 2 | Q3 — Classification Summary (M3-LOGICAL §4) incorrectly counts Discovery Scout under POLICY_SERVICE (4) instead of HUMAN_OR_AGENT_JUDGMENT_ROLE (should be 3/11 not 4/10) | Move Discovery Scout from POLICY_SERVICE to HUMAN_OR_AGENT_JUDGMENT_ROLE in §4 summar y table; update counts | M3-LOGICAL author | MINOR |
| 3 | Q10 — Case schema fields split across M3-01 and M3-03 without cross-reference or authoritative source designation | Add cross-reference notes in both contracts' M4A Readiness sections, or designate one contract as primary Case schema owner | M3-01 / M3-03 authors | MINOR |

## Evidence Gaps

No evidence gaps were identified during this review. All 10 domain contracts and 4 design artifacts were read in full. The M2 registry was consulted for cross-referencing all capability dispositions. The Constitution (v0.6) and DNA (v0.3) were spot-checked for foundational alignment. The review did not read every operational/ sub-module artifact (e.g., CIW pilot docs, Deep Research Contract template, Thai Editorial Standard) — those are referenced as REUSE/ABSORB sources and their consistency with M3 contracts is assumed by the M2 registry's closeout status. This is within scope for a design-contract phase review.

## Scope Expansion Check

**No expansion beyond design-contract scope detected.**

The `NEW_M3_DERIVATION` annotations in every contract header explicitly declare what is new vs frozen-materialized. Claims of derivation are consistent with the frozen architecture requirements (Constitution §1/§2, FD #130, Discovery & Coverage Operating Requirement v0.1). The following were verified as legitimate formalizations of frozen decisions rather than new investment rules:

- **M3-05 (Scuttlebutt Protocol):** Labels itself as `NEW_M3_DERIVATION` — formalizing CIW's under-specified scuttlebutt section into structured protocol. Consistent with frozen architecture gap resolution. Not new investment rules.
- **M3-07 (Impairment):** The 5-state impairment framework is derived from Constitution §1's central question and FD #130's competing hypotheses mandate. Not new investment rules.
- **M3-09 §2 (Structural Red Team):** The `ACCEPTED/PARTIALLY_ACCEPTED/REJECTED_WITH_EVIDENCE/UNRESOLVED` outcomes are derived from CIW's Challenge role evolution. Consistent with frozen architecture.

No contract introduces undisclosed investment rules, composite scores, or trading logic.

---

## Appendix: Key Architectural Strengths Noted

- **Separation-of-duties matrix** (M3-LOGICAL §5) is the strongest in any design phase reviewed — 10 non-negotiable separations with explicit rationale
- **Role Combination Matrix** (M3-ROLES) provides clear, implementable guidance for profile consolidation
- **Stage state machine** keeps COMPLETED/FAILED/INCOMPLETE/SKIPPED distinctly separate with no auto-escalation paths
- **Run Manifest** (M3-01 §9) is comprehensive — will support full reproducibility
- **Evaluation failure types** (M3-10 §4.1: Type A Research Quality, Type B Discovery Recall) are well-structured and actionable
- **Evidence Admission Gate** (M3-04 §5) with 7 admission checks covering source existence, tier, PIT, and provenance completeness
- **Workforce Migration Map** (M3-MIGRATION) correctly defers all migration to post-M3 with "Design Only — Not Authorized" warning

<!-- 2026-08-19 16:30 UTC+7 -->