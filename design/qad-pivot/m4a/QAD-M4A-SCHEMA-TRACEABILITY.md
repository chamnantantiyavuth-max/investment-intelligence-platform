# QAD-M4A Schema Traceability Matrix

> **Status:** M4A IN PROGRESS
> **Authority:** FD #133; M3 Domain Contracts (FROZEN for M4 derivation)
> **Canonical schemas:** 68 (6+10+8+7+6+8+7+7+9)
> **Canonical since:** 2026-08-19
> **Purpose:** Maps every M4A canonical schema to its M3 authority source. Every schema traces to a specific M3 contract and clause.

---

## Traceability Key

| Abbreviation | Full Reference |
|---|---|
| M3-NN §X | M3 contract NN, Section X |

---

## Derivation Status Key

| Status | Meaning |
|---|---|
| **M3_AUTHORITY** | Schema directly traces to an explicit M3 contract clause. M3 defines the concept, structure, or requirements. M4A implements faithfully. |
| **NEW_M4A_DERIVATION** | Schema-level data model is new in M4A. M3 provides the conceptual authority (process, policy, or architectural requirement) but does not define the specific data structure. See Appendix A. |
| **PIT MODE — M3_AUTHORITY** | The three PIT modes (LIVE_CASE_UPDATE, SEALED_HISTORICAL_EVALUATION, REPLAY_EXCEPTION) are defined in M3-SERVICES S7. NOT NEW_M4A_DERIVATION. The field-level data model representation is M4A implementation detail. |

---

## A — Identity & Coverage (6 schemas)

### A-1: SecurityMaster

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| SM-01 | M3-02 §2 (Registry 1) | M3-02 §2.1 (SECURITY_MASTER), M3-02 §7 (Data Architecture) | **M3_AUTHORITY** — Six-registry architecture. CIK-based primary identity; ticker/sedol/cusip as aliases. Append-only; ticker changes create new records. |

**Authority Chain:** Discovery Requirement v0.1, M2 Capability CAP-001 (REUSE), M3-02 §2.1

### A-2: ResearchableUniverseRecord

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| RU-01 | M3-02 §2 (Registry 2) | M3-02 §2.2 (RESEARCHABLE_UNIVERSE), M3-02 §6 (Hard Filters) | **M3_AUTHORITY** — Hard exclusion for non-operating vehicles. Silent omissions prohibited. State per company: INCLUDED/EXCLUDED/PENDING_RESOLUTION. |

**Authority Chain:** Discovery Requirement v0.1, DNA-004, M3-02 §2.2

### A-3: SignalRecord

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| SR-01 | M3-02 §2 (Registry 3) | M3-02 §2.3 (SIGNAL_REGISTRY), M3-02 §7 (Data Architecture) | **M3_AUTHORITY** — Per-signal provenance. Three signal families: Quality (Lane A), Dislocation (Lane B), External (Lane C). Never deleted — only superseded. |

**Authority Chain:** Discovery Requirement v0.1, DNA-003, M3-02 §2.3

### A-4: CandidateRecord

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| CR-01 | M3-02 §2 (Registry 4) | M3-02 §2.4 (CANDIDATE_REGISTRY), M3-02 §4 (Selection States), M3-02 §5 (Candidate Assembly) | **M3_AUTHORITY** — Six candidate states. Selection Engine is POLICY_SERVICE (not judgment role). Cannot be overridden by Research Director or Chief Underwriter. |

**Authority Chain:** Discovery Requirement v0.1, Constitution §18, M3-02 §2.4/§4/§5

### A-5: QualityUniverseRecord

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| QU-01 | M3-02 §2 (Registry 5) | M3-02 §2.5 (QUALITY_UNIVERSE), DNA-017, M3-06 §2.5 (Quality States) | **M3_AUTHORITY** — Quality membership NOT conditioned on active dislocation. States: VERIFIED/PROBABLE/UNRESOLVED/FAILED. |

**Authority Chain:** DNA-017, M3-02 §2.5, M3-06 §2.5

### A-6: CaseRecord

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| CASE-01 | M3-01 §3.2 (Lifecycle) | M3-01 §3 (State Ownership), M3-03 §3 (Stage 1: Case Open) | **M3_AUTHORITY** — Case state machine with 18+ states. Case ID format CASE-YYYY-NNN. Cannot be opened without candidate in AUTO_RESEARCH_NOW. |

**Authority Chain:** Frozen Architecture, M3-01 §3, M3-03 §3

---

## B — Source & Evidence (10 schemas)

### B-1: SourceRecord

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| SRC-01 | M3-04 §2.1 | M3-04 §2 (Layer 1: Raw Source Archive), M3-04 §1 (L1-L10) | **M3_AUTHORITY** — L1–L10 source tier definitions. Content hash verified on read. Append-only; never modified. |

**Authority Chain:** Evidence Doctrine (CAP-017), M3-04 §2

### B-2: EvidenceRecord

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| EV-01 | M3-04 §3.3 | M3-04 §2 (Layer 2: Canonical Evidence Registry), M3-04 §3 (Evidence Object Taxonomy) | **M3_AUTHORITY** — Five-layer canonical model. Four evidence types: FACT/CLAIM/INFERENCE/HYPOTHESIS. Admission gate controls entry. |

**Authority Chain:** Evidence Doctrine (CAP-017), M3-04 §2/§3

### B-3: FactRecord

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| FACT-01 | M3-04 §4.1 | M3-04 §3 (FACT) | **M3_AUTHORITY** — Verifiable, objective information directly from source. Must be traceable to original source at exact location. |

**Authority Chain:** Evidence Doctrine (CAP-017), M3-04 §4.1

### B-4: ClaimRecord

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| CLM-01 | M3-04 §4.2 | M3-04 §3 (CLAIM) | **M3_AUTHORITY** — Assertion by entity that may be true or false. Truth not asserted by system. Claimant_type enum. |

**Authority Chain:** Evidence Doctrine (CAP-017), M3-04 §4.2

### B-5: InferenceRecord

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| INF-01 | M3-04 §4.3 | M3-04 §3 (INFERENCE) | **M3_AUTHORITY** — Conclusion drawn from facts/claims. Labeled with confidence (HIGH/MEDIUM/LOW/SPECULATIVE). Chain of reasoning must be explicit. |

**Authority Chain:** Evidence Doctrine (CAP-017), M3-04 §4.3

### B-6: HypothesisRecord

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| HYP-01 | M3-04 §4.4 | M3-04 §4.4 (HYPOTHESIS), M3-03 §2 (H1–H5) | **M3_AUTHORITY** — Every case MUST have H1–H5. Falsification criteria must be specific. Authority extends from Constitution §2. |

**Authority Chain:** Constitution §2, Evidence Doctrine (CAP-017), M3-04 §4.4, M3-03 §2

### B-7: ContradictionRecord

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| CTR-01 | M3-04 §6 | M3-04 §6 (Contradiction Management), Evidence Doctrine | **M3_AUTHORITY** — Contradictions never resolved by deleting one side. Both sides preserved. UNRESOLVED flagged for Chief Underwriter. |

**Authority Chain:** DNA-002 (Evidence First), Evidence Doctrine, M3-04 §6

### B-8: EvidenceGap

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| EG-01 | M3-03 §3.3 | M3-03 §3.3 (Evidence Gap Map), M3-05 §3 (Investigation Charter) | **M3_AUTHORITY** — Gap classification: RESOLVABLE_WITH_EXISTING_SOURCES / RESOLVABLE_WITH_SCUTTLEBUTT / CURRENTLY_UNRESOLVABLE (NEW_M3_DERIVATION). The `investigator_charter_id` foreign-key linkage is field-level NEW_M4A_DERIVATION (M3 describes the flow as process, not data relationship). |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-03 §3.3 (NEW_M3_DERIVATION), M3-05 §3

### B-9: EvidenceAdmissionRecord

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| EAR-01 | M3-04 §5 | M3-04 §2 (Layer 2), M3-09 §3 (Audit Checklist) | **M3_AUTHORITY** — 7 admission checks. Evidence Intelligence Lead manages admission. AI synthesis must be validated against original source. |

**Authority Chain:** Evidence Doctrine (CAP-017), M3-04 §5, Constitution §18

### B-10: SourceVersion

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| SRCV-01 | M3-04 §5 | M3-04 §2 (Layer 1: Raw Source Archive), M3-04 §5 (Source Archive retention) | **M3_AUTHORITY** — Versioned record of source document changes/re-retrievals. Re-retrieval creates new version. Tombstone preserves removal reason. |

**Authority Chain:** Evidence Doctrine (CAP-017), M3-04 §2/§5

---

## C — Research Governance (8 schemas)

### C-1: ResearchCharter

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| RC-01 | M3-03 §2.3 | M3-03 §3 (Stage 2: Research Charter), M3-09 §4 (Research Charter governance) | **M3_AUTHORITY** — H1–H5 assessment, evidence strengths/gaps, budget, stop conditions. Charter immutable after BUDGET_APPROVED. |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-03 §2.3, DNA-019

### C-2: ResearchStageRecord

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| RSR-01 | M3-03 §3 (Stages 1-18) | M3-03 §3 (Stages 1-18), M3-03 §4 (Stage State Lifecycle) | **M3_AUTHORITY** — 18-stage end-to-end flow. State machine: NOT_STARTED → IN_PROGRESS → COMPLETE/FAILED/INCOMPLETE/SKIPPED. Stage transitions append-only. |

**Authority Chain:** Frozen Architecture, M3-01 §3.3, M3-03 §3/§4

### C-3: InvestigatorCharter

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| IC-01 | M3-05 §3 | M3-05 §3 (Investigation Charter), M3-05 §4 (Investigation Protocol) | **M3_AUTHORITY** — Bounded, lawful scuttlebutt investigations. 11 investigator types. Must have specific falsifiable question. Stop rule must be defined. |

**Authority Chain:** M3-05 (entire contract is NEW_M3_DERIVATION — formalized from frozen architecture requirement for elastic investigator network)

### C-4: ResearchBudgetRecord

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| RB-01 | M3-01 §9 | M3-01 §9 (Budget Discipline), M3-03 §3 (Stage 2) | **M3_AUTHORITY** — Per-case budget allocation. Budget exhaustion → INCOMPLETE (not weakened quality). Budget cannot be self-authorized by Research Director. |

**Authority Chain:** Frozen Architecture, M3-01 §9

### C-5: ResearchFailureRecord

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| RFR-01 | M3-01 §6 | M3-01 §7 (Reliability Contract), M3-03 §4 (Stage State Lifecycle) | **M3_AUTHORITY** — 8 failure types. Failure must never silently become completeness (Cardinal Rule, M3-01 §6.2). Max 3 retries. |

**Authority Chain:** Frozen Architecture, M3-01 §6/§7

### C-6: HypothesisSet

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| HS-01 | M3-03 §2 | M3-03 §2 (H1–H5 mandatory), M3-03 §3 (Stage 2: Research Charter) | **M3_AUTHORITY** — Complete set of H1–H5 competing hypotheses. Must contain exactly H1–H5. Incomplete set → Charter cannot be approved. |

**Authority Chain:** Constitution §2, M3-03 §2/§3

### C-7: InvestigationReport

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| IR-01 | M3-05 §5 | M3-05 §5 (Investigation Output), M3-05 §4 (Investigation Protocol), M3-ROLES Role 14 | **M3_AUTHORITY** — Scuttlebutt investigation report from Elastic Investigator. Output: Evidence IDs + Report + Source List. Proposed evidence noncanonical until admitted. |

**Authority Chain:** M3-05 §5 (NEW_M3_DERIVATION), M3-ROLES Role 14

### C-8: ResearchStopRecord

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| RSR-02 | M3-01 §3 | M3-01 §3 (Stop Conditions), M3-03 §6 (Stop Conditions) | **M3_AUTHORITY** — 6 stop reasons: HYPOTHESIS_FALSIFIED / BUDGET_EXHAUSTED / DATA_INSUFFICIENT / FOUNDER_DIRECTED / AUDITOR_BLOCKED / THESIS_KILLER_TRIGGERED. |

**Authority Chain:** CIW Inherited, M3-01 §3, M3-03 §6

---

## D — Business / Industry / Management (7 schemas)

### D-1: QualityAssessment

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| QA-01 | M3-06 §2.5 | M3-06 §2.4/§2.5 (Quality Verification States, False-Quality Test) | **M3_AUTHORITY** — 6 False-Quality Tests: good business vs good industry, leverage, sustainability, growth value destruction, melting ice cube, owner-earnings. |

**Authority Chain:** Frozen Architecture (FD #95/#130), M3-06 §2.5

### D-2: MoatAssessment

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| MA-01 | M3-06 §2.3 | M3-06 §2.3 (Moat Analysis — FD #61), M3-06 §2.4 (Moat Dimensions) | **M3_AUTHORITY** — 6 canonical moat types: SHARE_OF_MIND / NETWORK_EFFECT / HIGH_SWITCHING_COST / COST_ADVANTAGE / INTANGIBLE_ASSETS / EFFICIENT_SCALE. |

**Authority Chain:** Frozen Architecture (FD #61), M3-06 §2.3

### D-3: IndustryEconomicsRecord

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| IE-01 | M3-06 §3 | M3-06 §3/§3.2 (Industry Economics Framework) | **M3_AUTHORITY** — Demand → Supply → Capacity → Utilization → Pricing → Margins → ROIC → Capital Entry/Exit chain. |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-06 §3

### D-4: ManagementClaim

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| MC-01 | M3-06 §4.1 | M3-06 §4.2 (Management Claim Ledger) | **M3_AUTHORITY** — Track management claims vs outcomes (FULFILLED/NOT_FULFILLED). Management assessed through Decision History, not charisma. |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-06 §4.1

### D-5: CapitalAllocationEvent

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| CAE-01 | M3-06 §4.2 | M3-06 §4.3 (Capital Allocation Ledger) | **M3_AUTHORITY** — Action, amount, rationale, outcome, per-share impact. Prefer 10-15 years of data. |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-06 §4.2

### D-6: ManagementDecisionLedger

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| MDL-01 | M3-06 §4 | M3-06 §4 (Management Assessment Framework) | **M3_AUTHORITY** — Aggregate management assessment. States: STRONG / ADEQUATE / WEAK / UNPROVEN. Assessment based on decisions, not charisma. |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-06 §4

### D-7: ManagementOutcome

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| MO-02 | M3-06 §4.1 | M3-06 §4.2 (Management Claim Ledger), M3-06 §4.4 (Promise vs Outcome) | **M3_AUTHORITY** — Measured outcome of a management decision or claim. Variance types: MET / EXCEEDED / MISSED / UNCLEAR / PENDING. |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-06 §4.1/§4.4

---

## E — Impairment & Recovery (6 schemas)

### E-1: DislocationRecord

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| DR-01 | M3-07 §2 | M3-07 §2 (Dislocation Reconstruction) | **M3_AUTHORITY** — 9 dislocation dimensions: Revenue, Volume, Price, Mix, Margin, Share, Churn, ROIC, Cash. 6 diagnostic gates. |

**Authority Chain:** Frozen Architecture, M3-07 §2

### E-2: ImpairmentAssessment

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| IA-01 | M3-07 §3 | M3-07 §3 (Impairment Diagnosis) | **M3_AUTHORITY** — Impairment states: TEMPORARY / MOSTLY_TEMPORARY / MIXED / STRUCTURAL / UNRESOLVED. Mandatory: Primary Diagnosis + Strongest Competing + Why Dominates + Weakest Link + Flip Evidence. |

**Authority Chain:** Frozen Architecture (Constitution §1), M3-07 §3

### E-3: CompetingExplanation

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| CE-01 | M3-07 §3.2 | M3-07 §3.2 (Mandatory Output) | **M3_AUTHORITY** — Strongest alternative explanation. Must be evidence-based, not hypothetical. |

**Authority Chain:** Frozen Architecture, M3-07 §3.2

### E-4: RecoveryModel

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| RM-01 | M3-07 §4 | M3-07 §4 (Recovery Model) | **M3_AUTHORITY** — 7 recovery types. Recovery states: NOT_YET_EVIDENT / EARLY_SIGNS / CONFIRMING / STALLED / COMPLETED / NOT_APPLICABLE. |

**Authority Chain:** Frozen Architecture, M3-07 §4

### E-5: ThesisKiller

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| TK-01 | M3-07 §4.4 | M3-07 §5 (Thesis Killers) | **M3_AUTHORITY** — 7 killer types: Quality, Impairment, Valuation, Balance-Sheet, Management, Industry, Regulatory. Tracked throughout case lifecycle. |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-07 §5

### E-6: FlipEvidence

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| FE-01 | M3-07 §3.2 | M3-07 §3.2 (Flip Evidence) | **M3_AUTHORITY** — Specific evidence that would change impairment diagnosis. Must be concrete and observable. |

**Authority Chain:** Frozen Architecture, M3-07 §3.2

---

## F — Financial & Economic Underwriting (8 schemas)

### F-1: FinancialFact

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| FF-01 | M3-08 §2 | M3-08 §2 (Financial Reconstruction) | **M3_AUTHORITY** — 7–10+ years financial reconstruction. Every fact traceable to source at exact location. |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-08 §2

### F-2: NormalizedFinancialFact

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| NFF-01 | M3-08 §2.4 | M3-08 §2.4 (Normalization Adjustments), M3-08 §3.2 (Normalized Estimation Method) | **M3_AUTHORITY** — Adjusted/normalized financial data point. Every adjustment tagged with type and rationale. |

**Authority Chain:** Frozen Architecture, M3-08 §2.4/§3.2

### F-3: CalculationRecord

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| CALC-01 | M3-08 §2.3 | M3-08 §2.3 (Calculation Lineage), M3-08 §4 (Permanent Loss) | **M3_AUTHORITY** — Every calculation must have explicit formula, inputs, and result. Must be independently reproducible. No black-box calculations. |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), Evidence Doctrine, M3-08 §2.3

### F-4: ScenarioRecord

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| SCEN-01 | M3-08 §3 | M3-08 §3 (Economic Scenarios) | **M3_AUTHORITY** — 5 scenarios: CURRENT / NO_RECOVERY / PARTIAL_RECOVERY / NORMALIZATION / QUALITY_COMPOUNDING. Explicit traceable assumptions; no blends. Replaces obsolete SR-02. |

**Authority Chain:** Frozen Architecture, M3-08 §3

### F-5: PermanentLossAssessment

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| PLA-01 | M3-08 §4 | M3-08 §5.1 (Permanent Loss Analysis) | **M3_AUTHORITY** — 6 risk dimensions: Balance-Sheet Runway, Dilution Risk, Asset Impairment, Covenant Risk, Refinancing Risk, Competitive Damage. |

**Authority Chain:** Frozen Architecture, M3-08 §4

### F-6: ReverseDCFRecord

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| RDCF-01 | M3-08 §5.1 | M3-08 §5.3 (Reverse DCF) | **M3_AUTHORITY** — Reverse DCF mandatory for every case. Implied growth/margin/ROIC from current price. |

**Authority Chain:** Frozen Architecture, M3-08 §5.1

### F-7: ValuationAssessment

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| VA-01 | M3-08 §5 | M3-08 §5 (Valuation as Diagnostic Tool) | **M3_AUTHORITY** — No single fair-value number. No buy/sell/hold. Valuation is diagnostic, not decorative. Asymmetry estimate: Favorable / Unfavorable / Symmetric / Unclear. |

**Authority Chain:** Frozen Architecture, M3-08 §5

### F-8: PriceImpliedExpectation

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| PIE-01 | M3-08 §5.2 | M3-08 §5.4 (Price-Implied Expectations) | **M3_AUTHORITY** — What the current market price implies about future expectations. Must compare implied expectations to at least 3 scenario assumptions. |

**Authority Chain:** Frozen Architecture, M3-08 §5.2

---

## G — Challenge / Underwriting / Publication (7 schemas)

### G-1: RedTeamChallenge

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| RTC-01 | M3-09 §2 | M3-09 §2 (Structural Red Team) | **M3_AUTHORITY** — No veto; outputs preserved even if rejected. Structurally separate. No access to modify evidence. |

**Authority Chain:** DNA-010, Constitution §10, M3-09 §2

### G-2: AuditFinding

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| AF-01 | M3-09 §3 | M3-09 §3 (Independent Audit) | **M3_AUTHORITY** — 9 audit checks. Auditor may block FOUNDER_READY. Reports directly to Founder. |

**Authority Chain:** M2 Capability CAP-016 (REUSE), M3-09 §3

### G-3: AuditGate (AuditReport)

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| AG-01 | M3-09 §3 | M3-09 §3 (Independent Audit) | **M3_AUTHORITY** — Aggregate audit report. Outcomes: PASS / PASS_WITH_FINDINGS / FAIL. Cannot be overridden by Research Director. |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-09 §3

### G-4: UnderwritingVerdict

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| UV-01 | M3-09 §4 | M3-09 §4 (Chief Underwriter) | **M3_AUTHORITY** — Final research verdict: QAD_CONFIRMED / QAD_PROBABLE / QAD_UNRESOLVED / NOT_QAD_STRUCTURAL / NOT_QAD_QUALITY / NOT_QAD_VALUATION. Highest AI-judgment function. |

**Authority Chain:** Frozen Architecture, Constitution §18, M3-09 §4

### G-5: PublicationRecord

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| PUB-01 | M3-09 §5 | M3-09 §5 (Publication) | **M3_AUTHORITY** — Publication states: RESEARCH_COMPLETE → FOUNDER_READY → FOUNDER_ENDORSED. Governance jargon removed (FD #94). Companion dissent report linked (FD #96). |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-09 §5

### G-6: FounderDecisionReference

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| FDR-01 | M3-09 §5.2 | M3-09 §5.2 (Founder Decision vs System) | **M3_AUTHORITY** — Only Founder can create FOUNDER_ENDORSED. System creates FOUNDER_READY. Decision types: ENDORSED / DISAGREES / REJECTS / POLICY_OVERRIDE. |

**Authority Chain:** Constitution §18 (Founder authority), M3-09 §5.2

### G-7: ChallengeResponse

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| CRESP-01 | M3-09 §2.4 | M3-09 §2.4 (Red Team no veto; findings preserved), M3-09 §4 (Underwriter synthesis) | **M3_AUTHORITY** — Chief Underwriter's response to Red Team challenge. Red Team findings cannot be suppressed. Rejected findings must include evidence basis. |

**Authority Chain:** Constitution §10 (Dissent), M3-09 §2.4/§4

---

## H — Monitoring & Knowledge (7 schemas)

### H-1: MonitoringIndicator

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| MI-01 | M3-10 §2 | M3-10 §2 (Monitoring), M3-10 §2.2 (Monitoring Indicators) | **M3_AUTHORITY** — Thesis-specific indicators (1-3 key indicators with thresholds, cadence, escalation). Not generic news flow. |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-10 §2

### H-2: MonitoringObservation

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| MO-01 | M3-10 §2 | M3-10 §2 (Monitoring) | **M3_AUTHORITY** — Point-in-time observation record. Append-only. |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-10 §2

### H-3: MonitoringAssessment

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| MASS-01 | M3-10 §2.1 | M3-10 §2.1 (Monitoring States) | **M3_AUTHORITY** — Monitoring states: RECOVERY_CONFIRMING / ON_TRACK / UNCERTAIN / WEAKENING / BROKEN. BROKEN triggers Founder notification. |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-10 §2.1

### H-4: CandidateLesson

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| CL-01 | M3-10 §3 | M3-10 §3 (Knowledge Lifecycle) | **M3_AUTHORITY** — Knowledge lifecycle: Research Finding → Candidate Lesson → Cross-Case Validation → Independent Review → APPROVED KNOWLEDGE. Single case does NOT automatically become institutional knowledge. |

**Authority Chain:** DNA-011/012, M3-10 §3

### H-5: InstitutionalKnowledgeRecord

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| IKR-01 | M3-10 §3.2 | M3-10 §3.2 (Knowledge Stages) | **M3_AUTHORITY** — Requires cross-case validation + independent review + Chief Underwriter/Founder approval. |

**Authority Chain:** DNA-012 (Controlled Learning), M3-10 §3.2

### H-6: IndustryPlaybookRecord

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| IPR-01 | M3-10 §3 | M3-10 §3 (Knowledge Compounding), M3-06 §3.3 (Competitive Position) | **M3_AUTHORITY** — Structured knowledge about an industry. Requires multiple cases in same industry + systematic distillation. |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-10 §3, M3-06 §3.3

### H-7: CrossCaseValidation

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| CCV-01 | M3-10 §3.1 | M3-10 §3.1 (Knowledge Lifecycle), M3-10 §3.1 (Cross-Case Validation) | **M3_AUTHORITY** — Record of cross-case validation. Requires 3+ independent cases. Validation results: CONFIRMED / PARTIALLY_CONFIRMED / INCONCLUSIVE / REJECTED. |

**Authority Chain:** DNA-012 (Controlled Learning), M3-10 §3.1

---

## I — Reproducibility & Operations (9 schemas)

### I-1: ResearchRunManifest

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| RRM-01 | M3-01 §9 | M3-01 §9 (Run Manifest) | **M3_AUTHORITY** — Mandatory fields (research_run_id → output_version). Run start record created even if run fails (partial manifest). |

**Authority Chain:** Frozen Architecture, M3-01 §9

### I-2: PITContext

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| PITC-01 | M3-SERVICES S7 | M3-SERVICES S7 (PIT Lock Service), M3-01 §9.1 (Point-in-Time Lock) | **PIT MODE — M3_AUTHORITY** — Three PIT modes (LIVE_CASE_UPDATE, SEALED_HISTORICAL_EVALUATION, REPLAY_EXCEPTION) are explicitly defined in M3-SERVICES S7. NOT NEW_M4A_DERIVATION. SEALED mode hard-blocks post-AS_OF evidence. FAIL_CLOSED behavior. The field-level data model (ID scheme, enums) is M4A implementation detail. |

**Authority Chain:** Evidence Doctrine (CAP-017), M3-01 §9.1, M3-SERVICES S7

### I-3: ServiceInvocation

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| SI-01 | M3-ROLES §5 | M3-ROLES §5 (Service Registry) | **M3_AUTHORITY** — Every service invocation recorded. M3 defines Service Registry concept; specific invocation tracking data model (status enum, duration_ms, input/output summary) is field-level NEW_M4A_DERIVATION. |

**Authority Chain:** Frozen Architecture, M3-ROLES §5

### I-4: RetryRecord

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| RR-01 | M3-SERVICES S8 | M3-SERVICES S8 (Retry Controller), M3-01 §7 (Reliability) | **M3_AUTHORITY** — Max 3 retries per stage. After 3 → FAILED. M3 specifies bounded-retry policy; specific retry record data model (invocation_id link, attempt_number, ESCALATED status) is field-level NEW_M4A_DERIVATION. |

**Authority Chain:** Frozen Architecture, M3-01 §7, M3-SERVICES S8

### I-5: CaseLock

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| CLK-01 | M3-SERVICES S9 | M3-SERVICES S9 (Case Locking) | **M3_AUTHORITY** — Per-case locking with timeout → INCOMPLETE release (NEW_M3_DERIVATION from M3-01 §8.4). Lock states: LOCKED / UNLOCKED / PENDING. |

**Authority Chain:** M3-01 §8.4 (NEW_M3_DERIVATION), M3-SERVICES S9

### I-6: BudgetUsage

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| BU-01 | M3-01 §9 | M3-01 §9 (Budget Discipline) | **M3_AUTHORITY** — Per-resource budget usage. Spend tracking is append-only. M3 specifies budget discipline; per-resource tracking data model (resource_type enum: TOKEN / API_CALL / DEEP_RESEARCH / NOTEBOOKLM / COMPUTATION / STORAGE / OTHER) is field-level NEW_M4A_DERIVATION. |

**Authority Chain:** Frozen Architecture, M3-01 §9

### I-7: ModelInvocation

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| MOD-01 | M3-01 §8 | M3-01 §8 (Run Manifest), M4B (forward reference) | **M3_AUTHORITY** — Per-model invocation tracking. M3 specifies Run Manifest concept; detailed model telemetry (prompt_tokens, completion_tokens, cost, prompt_hash, latency_ms, rate_limited/timeout states) is field-level NEW_M4A_DERIVATION. |

**Authority Chain:** M3-01 §8

### I-8: ProviderInvocation

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| PROV-01 | M3-01 §8 | M3-01 §8 | **M3_AUTHORITY** — Provider-level invocation wrapping multiple models. Fallback tracking. Provider-level record data model is field-level NEW_M4A_DERIVATION (M3 does not distinguish provider vs model telemetry). |

**Authority Chain:** M3-01 §8

### I-9: EvaluationHarnessRun

| Schema | Authority | M3 Clause | M4 Derivation |
|--------|-----------|-----------|--------------|
| EHR-01 | M3-SERVICES S12 | M3-SERVICES S12 (Evaluation Harness) | **M3_AUTHORITY** — Evaluation types: TYPE_A_RESEARCH_QUALITY / TYPE_B_DISCOVERY_RECALL / CALIBRATION / COST_EVAL. Partial evaluation = EVALUATION_INCOMPLETE. |

**Authority Chain:** Frozen Architecture, M3-10 §4, M3-SERVICES S12

---

## Appendix A: NEW_M4A_DERIVATION Items

These are schema fields, objects, or data models that are necessary for implementation completeness but whose detailed structure is not explicitly traced to an M3 clause. M3 provides the conceptual authority; M4A derives the specific data model.

### Category 1: Operational Telemetry — Field-Level Data Models

The following schemas in section I have their overall authority in M3-01 §8 (Run Manifest), M3-ROLES §5 (Service Registry), or M3-SERVICES S8/S9/S12, but M3 describes these only as concepts — the specific field-level data models (invocation IDs, status enums, timing, error tracking, resource types, fallback chains) are M4A-level implementation derivations.

| # | Schema | M3 Authority (Concept) | M4A Derivation (Fields) | Rationale |
|---|--------|----------------------|------------------------|-----------|
| 1 | **I-3: ServiceInvocation** (SI-01) | M3-ROLES §5 | Invocation status enum, duration_ms, input/output summary | M3 defines horizontal services but not a generic invocation record. M4A derives the standard invocation tracking schema from the requirement "every service invocation recorded." |
| 2 | **I-4: RetryRecord** (RR-01) | M3-01 §7, M3-SERVICES S8 | Invocation_id link, attempt_number, ESCALATED status | M3 specifies max 3 retries per stage but not the retry record data model. M4A derives the schema to satisfy bounded-retry accounting. |
| 3 | **I-6: BudgetUsage** (BU-01) | M3-01 §9 | resource_type enum (TOKEN / API_CALL / DEEP_RESEARCH / NOTEBOOKLM / COMPUTATION / STORAGE / OTHER), per-resource tracking | M3 specifies budget discipline but not a granular usage ledger. M4A derives the per-resource tracking model from the budget exhaustion → INCOMPLETE rule. |
| 4 | **I-7: ModelInvocation** (MOD-01) | M3-01 §8 | prompt_tokens, completion_tokens, cost, prompt_hash, response_hash, latency_ms, rate_limited/timeout states | M3 specifies Run Manifest (research_run_id → output_version). M4A extends this with per-model telemetry needed for cost tracking (M4B dependency) without explicit M3 mandate. |
| 5 | **I-8: ProviderInvocation** (PROV-01) | M3-01 §8 | Provider-level wrapper, fallback_used flag, model_invocation_ids[] linkage | M3 does not distinguish provider from model telemetry. M4A derives this aggregation layer to support provider failover tracking, which is implied but not specified by M3. |

### Category 2: Evidence Gap — Investigator Charter Foreign Key

| # | Field | Schema | M3 Authority | Rationale |
|---|-------|--------|-------------|-----------|
| 6 | `investigator_charter_id` | **B-8: EvidenceGap** (EG-01) | M3-03 §3.3 (classified gaps), M3-05 §3 (investigation contract) | M3-03 §3.3 classifies gaps as resolvable via scuttlebutt, and M3-05 §3 defines the investigation contract, but the explicit foreign-key linkage between an evidence gap row and its spawned investigator charter is an M4A derivation — M3 describes the flow as a process, not a data relationship. |

### Category 3: Schema IDs and Naming Convention

| # | Convention | Scope | M3 Authority | Rationale |
|---|-----------|-------|-------------|-----------|
| 7 | Schema ID format (XX-NN) | All schemas | None — M4A design convention | M3 does not prescribe a schema naming convention. The SM-01 / RU-01 / SR-01 / CASE-01 / etc. naming scheme is an M4A derivation for implementation clarity. |
| 8 | UUID v7 as primary ID | Most schemas | None — M4A design choice | M3 does not mandate UUID v7 specifically. M4A derives this from the general requirement for append-only immutable records with unique identifiers. |

### Summary of NEW_M4A_DERIVATION

| Category | Count | Status |
|----------|-------|--------|
| Operational telemetry — field-level data models | 5 | Derived from M3 concept (Run Manifest, Service Registry) |
| Evidence Gap → Investigator Charter foreign key | 1 | Derived from M3-03/M3-05 process flow |
| Schema naming / ID conventions | 2 | M4A design decisions (no M3 precedent) |
| **Total** | **8** | |

All NEW_M4A_DERIVATION items are implementation-level concretions of M3 concepts. No M4A schema contradicts or departs from M3 authority — every schema traces to a specific M3 clause at the conceptual level. The derivations above merely specify data models where M3 defined only process, policy, or architectural requirements.

PIT modes (LIVE_CASE_UPDATE, SEALED_HISTORICAL_EVALUATION, REPLAY_EXCEPTION) are explicitly **NOT** NEW_M4A_DERIVATION — they are M3-SERVICES S7 authority, frozen in M3.

---

## Cross-Reference: M3 Contracts Used

| M3 Contract | Schemas Traced |
|---|---|
| M3-01 Operating Model | CASE-01, RSR-01, RFR-01, RSR-02, RB-01, RRM-01, PITC-01, RR-01, BU-01, MOD-01, PROV-01 |
| M3-02 Discovery & Selection | SM-01, RU-01, SR-01, CR-01, QU-01 |
| M3-03 Full Research Protocol | CASE-01, EG-01, RC-01, RSR-01, RB-01, RFR-01, HYP-01, HS-01, IR-01, RSR-02 |
| M3-04 Evidence & Source Model | SRC-01, EV-01, FACT-01, CLM-01, INF-01, HYP-01, CTR-01, EAR-01, SRCV-01 |
| M3-05 Scuttlebutt Protocol | IC-01, EG-01, IR-01 |
| M3-06 Business Quality | QU-01, QA-01, MA-01, IE-01, MC-01, CAE-01, MDL-01, MO-02, IPR-01 |
| M3-07 Dislocation & Impairment | DR-01, IA-01, CE-01, RM-01, TK-01, FE-01 |
| M3-08 Financial Reconstruction | FF-01, NFF-01, CALC-01, SCEN-01, PLA-01, RDCF-01, VA-01, PIE-01 |
| M3-09 Challenge/Audit/Underwriting | PUB-01, FDR-01, RTC-01, AG-01, AF-01, UV-01, CRESP-01 |
| M3-10 Monitoring/Knowledge | MI-01, MO-01, MASS-01, CL-01, IKR-01, IPR-01, CCV-01 |
| M3-LOGICAL Logical Organization | SI-01 |
| M3-ROLES Production Roles | SI-01, IR-01 |
| M3-SERVICES System Services | PITC-01, RR-01, CLK-01, EHR-01 |
| M4B (forward reference) | MOD-01 |

---

<!-- 2026-08-19 15:00 UTC+7 -->