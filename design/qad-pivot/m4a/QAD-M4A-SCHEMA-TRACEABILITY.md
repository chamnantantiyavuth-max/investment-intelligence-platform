# QAD-M4A Schema Traceability Matrix

> **Status:** M4A IN PROGRESS
> **Authority:** FD #133; M3 Domain Contracts (FROZEN for M4 derivation)
> **Canonical since:** 2026-08-19
> **Purpose:** Maps every M4A canonical schema to its M3 authority source. Every schema traces to a specific M3 contract and clause.
> **Note:** The schema count header on the canonical schemas file shows 6+10+7+6+6+7+6+6+9 = 63 planned, with 61 schemas actually present (B has 9 of 10, C has 6 of 7 — the gaps are reserved for future schemas not yet designed).

---

## Traceability Key

| Abbreviation | Full Reference |
|---|---|
| M3-NN §X | M3 contract NN, Section X |
| SM-01 | SecurityMaster schema (A-1) |
| RU-01 | ResearchableUniverseRecord schema (A-2) |
| SR-01 | SignalRecord schema (A-3) |
| CR-01 | CandidateRecord schema (A-4) |
| QU-01 | QualityUniverseRecord schema (A-5) |
| CASE-01 | CaseRecord schema (A-6) |
| SRC-01 | SourceRecord schema (B-1) |
| EV-01 | EvidenceRecord schema (B-2) |
| FACT-01 | FactRecord schema (B-3) |
| CLM-01 | ClaimRecord schema (B-4) |
| INF-01 | InferenceRecord schema (B-5) |
| HYP-01 | HypothesisRecord schema (B-6) |
| CTR-01 | ContradictionRecord schema (B-7) |
| EG-01 | EvidenceGap schema (B-8) |
| EAR-01 | EvidenceAdmissionRecord schema (B-9) |
| RC-01 | ResearchCharter schema (C-1) |
| RSR-01 | ResearchStageRecord schema (C-2) |
| IC-01 | InvestigatorCharter schema (C-3) |
| RB-01 | ResearchBudgetRecord schema (C-4) |
| RFR-01 | ResearchFailureRecord schema (C-5) |
| RSR-02 | ResearchStopRecord schema (C-6) |
| QA-01 | QualityAssessment schema (D-1) |
| MA-01 | MoatAssessment schema (D-2) |
| IE-01 | IndustryEconomicsRecord schema (D-3) |
| MC-01 | ManagementClaim schema (D-4) |
| CAE-01 | CapitalAllocationEvent schema (D-5) |
| MDL-01 | ManagementDecisionLedger schema (D-6) |
| DR-01 | DislocationRecord schema (E-1) |
| IA-01 | ImpairmentAssessment schema (E-2) |
| CE-01 | CompetingExplanation schema (E-3) |
| RM-01 | RecoveryModel schema (E-4) |
| TK-01 | ThesisKiller schema (E-5) |
| FE-01 | FlipEvidence schema (E-6) |
| FF-01 | FinancialFact schema (F-1) |
| NFF-01 | NormalizedFinancialFact schema (F-2) |
| CALC-01 | CalculationRecord schema (F-3) |
| SR-02 | ScenarioRecord schema (F-4) |
| PLA-01 | PermanentLossAssessment schema (F-5) |
| RDCF-01 | ReverseDCFRecord schema (F-6) |
| VA-01 | ValuationAssessment schema (F-7) |
| RTC-01 | RedTeamChallenge schema (G-1) |
| AF-01 | AuditFinding schema (G-2) |
| AG-01 | AuditGate schema (G-3) |
| UV-01 | UnderwritingVerdict schema (G-4) |
| PUB-01 | PublicationRecord schema (G-5) |
| FDR-01 | FounderDecisionReference schema (G-6) |
| MI-01 | MonitoringIndicator schema (H-1) |
| MO-01 | MonitoringObservation schema (H-2) |
| MASS-01 | MonitoringAssessment schema (H-3) |
| CL-01 | CandidateLesson schema (H-4) |
| IKR-01 | InstitutionalKnowledgeRecord schema (H-5) |
| IPR-01 | IndustryPlaybookRecord schema (H-6) |
| RRM-01 | ResearchRunManifest schema (I-1) |
| PITC-01 | PITContext schema (I-2) |
| SI-01 | ServiceInvocation schema (I-3) |
| RR-01 | RetryRecord schema (I-4) |
| CLK-01 | CaseLock schema (I-5) |
| BU-01 | BudgetUsage schema (I-6) |
| MOD-01 | ModelInvocation schema (I-7) |
| PROV-01 | ProviderInvocation schema (I-8) |
| EHR-01 | EvaluationHarnessRun schema (I-9) |

---

## A — Identity & Coverage (6 schemas)

### A-1: SecurityMaster

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| SM-01 | M3-02 §2.1 (Registry 1) | M3-02 §2.1 (SECURITY_MASTER), M3-02 §7 (Data Architecture) | Six-registry architecture. CIK-based primary identity; ticker/sedol/cusip as aliases. Append-only; ticker changes create new records. |

**Authority Chain:** Discovery Requirement v0.1, M2 Capability CAP-001 (REUSE), M3-02 §2.1

### A-2: ResearchableUniverseRecord

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| RU-01 | M3-02 §2.2 (Registry 2) | M3-02 §2.2 (RESEARCHABLE_UNIVERSE), M3-02 §6 (Hard Filters) | Hard exclusion for non-operating vehicles. Silent omissions prohibited. State per company: INCLUDED/EXCLUDED/PENDING_RESOLUTION. |

**Authority Chain:** Discovery Requirement v0.1, DNA-004, M3-02 §2.2

### A-3: SignalRecord

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| SR-01 | M3-02 §2.3 (Registry 3) | M3-02 §2.3 (SIGNAL_REGISTRY), M3-02 §7 (Data Architecture) | Per-signal provenance. Three signal families: Quality (Lane A), Dislocation (Lane B), External (Lane C). Never deleted — only superseded. |

**Authority Chain:** Discovery Requirement v0.1, DNA-003, M3-02 §2.3

### A-4: CandidateRecord

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| CR-01 | M3-02 §2.4 (Registry 4) | M3-02 §2.4 (CANDIDATE_REGISTRY), M3-02 §4 (Selection States), M3-02 §5 (Candidate Assembly) | Six candidate states. Selection Engine is POLICY_SERVICE (not judgment role). Cannot be overridden by Research Director or Chief Underwriter. |

**Authority Chain:** Discovery Requirement v0.1, Constitution §18, M3-02 §2.4/§4/§5

### A-5: QualityUniverseRecord

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| QU-01 | M3-02 §2.5 (Registry 5) | M3-02 §2.5 (QUALITY_UNIVERSE), DNA-017, M3-06 §2.5 (Quality States) | Quality membership NOT conditioned on active dislocation. States: VERIFIED/PROBABLE/UNRESOLVED/FAILED. |

**Authority Chain:** DNA-017, M3-02 §2.5, M3-06 §2.5

### A-6: CaseRecord

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| CASE-01 | M3-01 §3.2 (Lifecycle) | M3-01 §3 (State Ownership), M3-03 §3 (Stage 1: Case Open) | Case state machine with 18+ states. Case ID format CASE-YYYY-NNN. Cannot be opened without candidate in AUTO_RESEARCH_NOW. |

**Authority Chain:** Frozen Architecture, M3-01 §3, M3-03 §3

---

## B — Source & Evidence (9 schemas)

### B-1: SourceRecord

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| SRC-01 | M3-04 §2.1 | M3-04 §1 (L1-L10), M3-04 §2 (Layer 1: Raw Source Archive) | L1–L10 source tier definitions. Content hash verified on read. Append-only; never modified. |

**Authority Chain:** Evidence Doctrine (CAP-017), M3-04 §2

### B-2: EvidenceRecord

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| EV-01 | M3-04 §3.3 | M3-04 §2 (Layer 2: Canonical Evidence Registry), M3-04 §3 (Evidence Object Taxonomy) | Five-layer canonical model. Four evidence types: FACT/CLAIM/INFERENCE/HYPOTHESIS. Admission gate controls entry. |

**Authority Chain:** Evidence Doctrine (CAP-017), M3-04 §2/§3

### B-3: FactRecord

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| FACT-01 | M3-04 §4.1 | M3-04 §3 (FACT) | Verifiable, objective information directly from source. Must be traceable to original source at exact location. |

**Authority Chain:** Evidence Doctrine (CAP-017), M3-04 §4.1

### B-4: ClaimRecord

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| CLM-01 | M3-04 §4.2 | M3-04 §3 (CLAIM) | Assertion by entity that may be true or false. Truth not asserted by system. Claimant_type enum. |

**Authority Chain:** Evidence Doctrine (CAP-017), M3-04 §4.2

### B-5: InferenceRecord

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| INF-01 | M3-04 §4.3 | M3-04 §3 (INFERENCE) | Conclusion drawn from facts/claims. Labeled with confidence (HIGH/MEDIUM/LOW/SPECULATIVE). Chain of reasoning must be explicit. |

**Authority Chain:** Evidence Doctrine (CAP-017), M3-04 §4.3

### B-6: HypothesisRecord

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| HYP-01 | M3-04 §4.4 | M3-04 §3 (HYPOTHESIS), M3-03 §2 (H1–H5) | Every case MUST have H1–H5. Falsification criteria must be specific. Authority extends from Constitution §2. |

**Authority Chain:** Constitution §2, Evidence Doctrine (CAP-017), M3-04 §4.4, M3-03 §2

### B-7: ContradictionRecord

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| CTR-01 | M3-04 §6 | M3-04 §6 (Contradiction Management), EVIDENCE-DOCTRINE | Contradictions never resolved by deleting one side. Both sides preserved. UNRESOLVED flagged for Chief Underwriter. |

**Authority Chain:** DNA-002 (Evidence First), Evidence Doctrine, M3-04 §6

### B-8: EvidenceGap

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| EG-01 | M3-03 §3.3 | M3-03 §3 (Stage 4: Evidence Gap Map), M3-05 §3 (Investigation Charter) | Gap classification: RESOLVABLE_WITH_EXISTING_SOURCES / RESOLVABLE_WITH_SCUTTLEBUTT / CURRENTLY_UNRESOLVABLE (NEW_M3_DERIVATION). |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-03 §3.3 (NEW_M3_DERIVATION), M3-05 §3

### B-9: EvidenceAdmissionRecord

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| EAR-01 | M3-04 §5 | M3-04 §2 (Layer 2), M3-09 §3 (Audit Checklist) | 7 admission checks. Evidence Intelligence Lead manages admission. AI synthesis must be validated against original source. |

**Authority Chain:** Evidence Doctrine (CAP-017), M3-04 §5, Constitution §18

---

## C — Research Governance (6 schemas)

### C-1: ResearchCharter

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| RC-01 | M3-03 §2.3 | M3-03 §3 (Stage 2: Research Charter), M3-09 §4 (Research Charter governance) | H1–H5 assessment, evidence strengths/gaps, budget, stop conditions. Charter immutable after BUDGET_APPROVED. |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-03 §2.3, DNA-019

### C-2: ResearchStageRecord

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| RSR-01 | M3-03 §3 (Stages 1-18) | M3-03 §3 (Stages 1-18), M3-03 §4 (Stage State Lifecycle) | 18-stage end-to-end flow. State machine: NOT_STARTED → IN_PROGRESS → COMPLETE/FAILED/INCOMPLETE/SKIPPED. Stage transitions append-only. |

**Authority Chain:** Frozen Architecture, M3-01 §3.3, M3-03 §3/§4

### C-3: InvestigatorCharter

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| IC-01 | M3-05 §3 | M3-05 §3 (Investigation Charter), M3-05 §4 (Investigation Protocol) | Bounded, lawful scuttlebutt investigations. 11 investigator types. Must have specific falsifiable question. Stop rule must be defined. |

**Authority Chain:** M3-05 (entire contract is NEW_M3_DERIVATION — formalized from frozen architecture requirement for elastic investigator network)

### C-4: ResearchBudgetRecord

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| RB-01 | M3-01 §9 | M3-01 §9 (Budget Discipline), M3-03 §3 (Stage 2) | Per-case budget allocation. Budget exhaustion → INCOMPLETE (not weakened quality). Budget cannot be self-authorized by Research Director. |

**Authority Chain:** Frozen Architecture, M3-01 §9

### C-5: ResearchFailureRecord

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| RFR-01 | M3-01 §6 | M3-01 §7 (Reliability Contract), M3-03 §4 (Stage State Lifecycle) | 8 failure types. Failure must never silently become completeness (Cardinal Rule, M3-01 §6.2). Max 3 retries. |

**Authority Chain:** Frozen Architecture, M3-01 §6/§7

### C-6: ResearchStopRecord

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| RSR-02 | M3-01 §3 (Stop Conditions) | M3-01 §3 (Stop Conditions), M3-03 §3 (Stage quality gates) | 6 stop reasons: HYPOTHESIS_FALSIFIED / BUDGET_EXHAUSTED / DATA_INSUFFICIENT / FOUNDER_DIRECTED / AUDITOR_BLOCKED / THESIS_KILLER_TRIGGERED. |

**Authority Chain:** CIW Inherited, M3-01 §3, M3-03 §6

---

## D — Business / Industry / Management (6 schemas)

### D-1: QualityAssessment

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| QA-01 | M3-06 §2.5 | M3-06 §2.5 (Quality Verification States), M3-06 §2.6 (False-Quality Test) | 6 False-Quality Tests: good business vs good industry, leverage, sustainability, growth value destruction, melting ice cube, owner-earnings. |

**Authority Chain:** Frozen Architecture (FD #95/#130), M3-06 §2.5

### D-2: MoatAssessment

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| MA-01 | M3-06 §2.3 | M3-06 §2.3 (Moat Analysis — FD #61), M3-06 §2.4 (Moat Dimensions) | 6 canonical moat types: SHARE_OF_MIND / NETWORK_EFFECT / HIGH_SWITCHING_COST / COST_ADVANTAGE / INTANGIBLE_ASSETS / EFFICIENT_SCALE. |

**Authority Chain:** Frozen Architecture (FD #61), M3-06 §2.3

### D-3: IndustryEconomicsRecord

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| IE-01 | M3-06 §3 | M3-06 §3 (Industry Economics Framework) | Demand → Supply → Capacity → Utilization → Pricing → Margins → ROIC → Capital Entry/Exit chain. |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-06 §3

### D-4: ManagementClaim

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| MC-01 | M3-06 §4.1 | M3-06 §4.1 (Management Claim Ledger) | Track management claims vs outcomes (FULFILLED/NOT_FULFILLED). Management assessed through Decision History, not charisma. |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-06 §4.1

### D-5: CapitalAllocationEvent

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| CAE-01 | M3-06 §4.2 | M3-06 §4.2 (Capital Allocation Ledger) | Action, amount, rationale, outcome, per-share impact. Prefer 10-15 years of data. |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-06 §4.2

### D-6: ManagementDecisionLedger

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| MDL-01 | M3-06 §4 | M3-06 §4 (Management Assessment Framework) | Aggregate management assessment. States: STRONG / ADEQUATE / WEAK / UNPROVEN. Assessment based on decisions, not charisma. |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-06 §4

---

## E — Impairment & Recovery (6 schemas)

### E-1: DislocationRecord

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| DR-01 | M3-07 §2 | M3-07 §2 (Dislocation Reconstruction) | 9 dislocation dimensions: Revenue, Volume, Price, Mix, Margin, Share, Churn, ROIC, Cash. 6 diagnostic gates. |

**Authority Chain:** Frozen Architecture, M3-07 §2

### E-2: ImpairmentAssessment

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| IA-01 | M3-07 §3 | M3-07 §3 (Impairment Diagnosis) | Impairment states: TEMPORARY / MOSTLY_TEMPORARY / MIXED / STRUCTURAL / UNRESOLVED. Mandatory: Primary Diagnosis + Strongest Competing + Why Dominates + Weakest Link + Flip Evidence. |

**Authority Chain:** Frozen Architecture (Constitution §1), M3-07 §3

### E-3: CompetingExplanation

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| CE-01 | M3-07 §3.2 | M3-07 §3.2 (Mandatory Output) | Strongest alternative explanation. Must be evidence-based, not hypothetical. |

**Authority Chain:** Frozen Architecture, M3-07 §3.2

### E-4: RecoveryModel

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| RM-01 | M3-07 §4 | M3-07 §4 (Recovery Model) | 7 recovery types. Recovery states: NOT_YET_EVIDENT / EARLY_SIGNS / CONFIRMING / STALLED / COMPLETED / NOT_APPLICABLE. |

**Authority Chain:** Frozen Architecture, M3-07 §4

### E-5: ThesisKiller

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| TK-01 | M3-07 §5 | M3-07 §4.4 (Thesis Killers) | 7 killer types: Quality, Impairment, Valuation, Balance-Sheet, Management, Industry, Regulatory. Tracked throughout case lifecycle. |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-07 §5

### E-6: FlipEvidence

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| FE-01 | M3-07 §3.2 | M3-07 §3.2 (Flip Evidence) | Specific evidence that would change impairment diagnosis. Must be concrete and observable. |

**Authority Chain:** Frozen Architecture, M3-07 §3.2

---

## F — Financial & Economic Underwriting (7 schemas)

### F-1: FinancialFact

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| FF-01 | M3-08 §2 | M3-08 §2 (Financial Reconstruction) | 7–10+ years financial reconstruction. Every fact traceable to source at exact location. |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-08 §2

### F-2: NormalizedFinancialFact

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| NFF-01 | M3-08 §2.4 | M3-08 §2.4 (Normalization Adjustments) | Adjusted/normalized financial data point. Every adjustment tagged with type and rationale. |

**Authority Chain:** Frozen Architecture, M3-08 §2.4

### F-3: CalculationRecord

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| CALC-01 | M3-08 §2.3 | M3-08 §2.3 (Calculation Lineage), M3-08 §4 (Permanent Loss) | Every calculation must have explicit formula, inputs, and result. Must be independently reproducible. No black-box calculations. |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), Evidence Doctrine, M3-08 §2.3

### F-4: ScenarioRecord

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| SR-02 | M3-08 §3 | M3-08 §3 (Economic Scenarios) | 5 scenarios: CURRENT / NO_RECOVERY / PARTIAL_RECOVERY / NORMALIZATION / QUALITY_COMPOUNDING. Explicit traceable assumptions; no blends. |

**Authority Chain:** Frozen Architecture, M3-08 §3

### F-5: PermanentLossAssessment

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| PLA-01 | M3-08 §4 | M3-08 §4 (Permanent Loss Analysis) | 6 risk dimensions: Balance-Sheet Runway, Dilution Risk, Asset Impairment, Covenant Risk, Refinancing Risk, Competitive Damage. |

**Authority Chain:** Frozen Architecture, M3-08 §4

### F-6: ReverseDCFRecord

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| RDCF-01 | M3-08 §5.1 | M3-08 §5.1 (Reverse DCF) | Reverse DCF mandatory for every case. Implied growth/margin/ROIC from current price. |

**Authority Chain:** Frozen Architecture, M3-08 §5.1

### F-7: ValuationAssessment

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| VA-01 | M3-08 §5 | M3-08 §5 (Valuation as Diagnostic Tool) | No single fair-value number. No buy/sell/hold. Valuation is diagnostic, not decorative. Asymmetry estimate: Favorable / Unfavorable / Symmetric / Unclear. |

**Authority Chain:** Frozen Architecture, M3-08 §5

---

## G — Challenge / Underwriting / Publication (6 schemas)

### G-1: RedTeamChallenge

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| RTC-01 | M3-09 §2 | M3-09 §2 (Structural Red Team) | No veto; outputs preserved even if rejected. Structurally separate. No access to modify evidence. |

**Authority Chain:** DNA-010, Constitution §10, M3-09 §2

### G-2: AuditFinding

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| AF-01 | M3-09 §3 | M3-09 §3 (Independent Audit) | 9 audit checks. Auditor may block FOUNDER_READY. Reports directly to Founder. |

**Authority Chain:** M2 Capability CAP-016 (REUSE), M3-09 §3

### G-3: AuditGate (AuditReport)

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| AG-01 | M3-09 §3 | M3-09 §3 | Aggregate audit report. Outcomes: PASS / PASS_WITH_FINDINGS / FAIL. Cannot be overridden by Research Director. |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-09 §3

### G-4: UnderwritingVerdict

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| UV-01 | M3-09 §4 | M3-09 §4 (Chief Underwriter) | Final research verdict: QAD_CONFIRMED / QAD_PROBABLE / QAD_UNRESOLVED / NOT_QAD_STRUCTURAL / NOT_QAD_QUALITY / NOT_QAD_VALUATION. Highest AI-judgment function. |

**Authority Chain:** Frozen Architecture, Constitution §18, M3-09 §4

### G-5: PublicationRecord

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| PUB-01 | M3-09 §5 | M3-09 §5 (Publication) | Publication states: RESEARCH_COMPLETE → FOUNDER_READY → FOUNDER_ENDORSED. Governance jargon removed (FD #94). Companion dissent report linked (FD #96). |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-09 §5

### G-6: FounderDecisionReference

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| FDR-01 | M3-09 §5.2 | M3-09 §5.2 | Only Founder can create FOUNDER_ENDORSED. System creates FOUNDER_READY. Decision types: ENDORSED / DISAGREES / REJECTS / POLICY_OVERRIDE. |

**Authority Chain:** Constitution §18 (Founder authority), M3-09 §5.2

---

## H — Monitoring & Knowledge (6 schemas)

### H-1: MonitoringIndicator

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| MI-01 | M3-10 §2 | M3-09 §6 (Thesis Monitoring) | Thesis-specific indicators (1-3 key indicators with thresholds, cadence, escalation). Not generic news flow. |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-10 §2

### H-2: MonitoringObservation

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| MO-01 | M3-10 §2 | M3-09 §6 | Point-in-time observation record. Append-only. |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-10 §2

### H-3: MonitoringAssessment

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| MASS-01 | M3-10 §2.1 | M3-09 §6.3 | Monitoring states: RECOVERY_CONFIRMING / ON_TRACK / UNCERTAIN / WEAKENING / BROKEN. BROKEN triggers Founder notification. |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-10 §2.1

### H-4: CandidateLesson

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| CL-01 | M3-10 §3 | M3-09 §7 (Knowledge Compounding) | Knowledge lifecycle: Research Finding → Candidate Lesson → Cross-Case Validation → Independent Review → APPROVED KNOWLEDGE. Single case does NOT automatically become institutional knowledge. |

**Authority Chain:** DNA-011/012, M3-10 §3

### H-5: InstitutionalKnowledgeRecord

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| IKR-01 | M3-10 §3.2 | M3-09 §7 | Requires cross-case validation + independent review + Chief Underwriter/Founder approval. |

**Authority Chain:** DNA-012 (Controlled Learning), M3-10 §3.2

### H-6: IndustryPlaybookRecord

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| IPR-01 | M3-10 §3 | M3-09 §7, M3-06 §3.3 | Structured knowledge about an industry. Requires multiple cases in same industry + systematic distillation. |

**Authority Chain:** CIW Inherited (FD-CIW-001..016), M3-10 §3, M3-06 §3.3

---

## I — Reproducibility & Operations (9 schemas)

### I-1: ResearchRunManifest

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| RRM-01 | M3-01 §8 | M3-01 §8 (Run Manifest) | Mandatory fields (research_run_id → output_version). Run start record created even if run fails (partial manifest). |

**Authority Chain:** Frozen Architecture, M3-01 §8

### I-2: PITContext

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| PITC-01 | M3-01 §8 (PIT Lock) | M3-01 §8 (PIT Lock), M3-SERVICES S7 (PIT Lock Service) | Three modes: LIVE_CASE_UPDATE / SEALED_HISTORICAL_EVALUATION / REPLAY_EXCEPTION. SEALED mode hard-blocks post-AS_OF evidence. |

**Authority Chain:** Evidence Doctrine (CAP-017), M3-01 §8, M3-SERVICES S7

### I-3: ServiceInvocation

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| SI-01 | M3-ROLES §5 | M3-ROLES §5 (Service Registry) | Generic service invocation record. Every service invocation recorded. Implementation-level schema. |

**Authority Chain:** Frozen Architecture, M3-ROLES §5 — field-level detail is NEW_M4A_DERIVATION (M3 defines the service concepts but not the specific invocation data model)

### I-4: RetryRecord

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| RR-01 | M3-01 §7 (Reliability) | M3-01 §7 (Reliability), M3-SERVICES S8 (Retry Controller) | Max 3 retries per stage. After 3 → FAILED. |

**Authority Chain:** Frozen Architecture, M3-01 §7, M3-SERVICES S8 — specific retry record data model is NEW_M4A_DERIVATION

### I-5: CaseLock

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| CLK-01 | M3-SERVICES S9 | M3-SERVICES S9 (Case Locking) | Per-case locking with timeout → INCOMPLETE release (NEW_M3_DERIVATION from M3-01 §8.4). Lock states: LOCKED / UNLOCKED / PENDING. |

**Authority Chain:** M3-01 §8.4 (NEW_M3_DERIVATION), M3-SERVICES S9

### I-6: BudgetUsage

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| BU-01 | M3-01 §9 | M3-01 §9 (Budget Discipline) | Per-resource budget usage. Spend tracking is append-only. Specific resource type taxonomy defined at M4A level. |

**Authority Chain:** Frozen Architecture, M3-01 §9 — per-resource tracking data model is NEW_M4A_DERIVATION

### I-7: ModelInvocation

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| MOD-01 | M3-01 §8 (Run Manifest) | M3-01 §8 (Run Manifest), M4B (Model/Cost Evaluation) | Per-model invocation tracking. Token and cost tracking for budget discipline. Field-level model tracking is an M4A implementation concern. |

**Authority Chain:** M3-01 §8 — detailed model invocation record is NEW_M4A_DERIVATION (M3 specifies run manifest concept but not per-model telemetry)

### I-8: ProviderInvocation

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| PROV-01 | M3-01 §8 | M3-01 §8 | Provider-level invocation wrapping multiple models. Fallback tracking. |

**Authority Chain:** M3-01 §8 — provider-level record is NEW_M4A_DERIVATION (M3 does not distinguish provider vs model telemetry)

### I-9: EvaluationHarnessRun

| Schema | Authority | M3 Clause | Notes |
|--------|-----------|-----------|-------|
| EHR-01 | M3-SERVICES S12 | M3-SERVICES S12 (Evaluation Harness) | Evaluation types: TYPE_A_RESEARCH_QUALITY / TYPE_B_DISCOVERY_RECALL / CALIBRATION / COST_EVAL. Partial evaluation = EVALUATION_INCOMPLETE. |

**Authority Chain:** Frozen Architecture, M3-10 §4, M3-SERVICES S12

---

## NEW_M4A_DERIVATION Items

These are schema fields, objects, or entire schemas that are necessary for implementation completeness but whose detailed structure is not explicitly traced to an M3 clause. M3 provides the conceptual authority; M4A derives the specific data model.

### Category 1: Operational Telemetry Schemas

The following schemas in section I have their overall authority in M3-01 §8 (Run Manifest) and M3-ROLES §5 (Service Registry), but M3 describes these only as concepts — the specific field-level data models (invocation IDs, status enums, timing, error tracking, fallback chains) are M4A-level implementation derivations.

| # | Schema | M3 Authority (Concept) | M4A Derivation (Fields) | Rationale |
|---|--------|----------------------|------------------------|-----------|
| 1 | **I-3: ServiceInvocation** (SI-01) | M3-ROLES §5 | Invocation status enum, duration_ms, input/output summary | M3 defines horizontal services but not a generic invocation record. M4A derives the standard invocation tracking schema from the requirement "every service invocation recorded." |
| 2 | **I-4: RetryRecord** (RR-01) | M3-01 §7, M3-SERVICES S8 | Invocation_id link, attempt_number, ESCALATED status | M3 specifies max 3 retries per stage but not the retry record data model. M4A derives the schema to satisfy bounded-retry accounting. |
| 3 | **I-6: BudgetUsage** (BU-01) | M3-01 §9 | resource_type enum (TOKEN / API_CALL / DEEP_RESEARCH / NOTEBOOKLM / COMPUTATION / STORAGE / OTHER), per-resource tracking | M3 specifies budget discipline but not a granular usage ledger. M4A derives the per-resource tracking model from the budget exhaustion → INCOMPLETE rule. |
| 4 | **I-7: ModelInvocation** (MOD-01) | M3-01 §8 | prompt_tokens, completion_tokens, cost, prompt_hash, response_hash, latency_ms, rate_limited/timeout states | M3 specifies Run Manifest (research_run_id → output_version). M4A extends this with per-model telemetry needed for cost tracking (M4B dependency) without explicit M3 mandate. |
| 5 | **I-8: ProviderInvocation** (PROV-01) | M3-01 §8 | Provider-level wrapper, fallback_used flag, model_invocation_ids[] linkage | M3 does not distinguish provider from model telemetry. M4A derives this aggregation layer to support provider failover tracking, which is implied but not specified by M3. |

### Category 2: Evidence Gap — Investigator Charter Linkage

| # | Field/Object | Schema | M3 Authority | Rationale |
|---|-------------|--------|-------------|-----------|
| 6 | `investigator_charter_id` | **B-8: EvidenceGap** (EG-01) | M3-03 §3.3 (classified gaps), M3-05 §3 (investigation contract) | M3-03 §3.3 classifies gaps as resolvable via scuttlebutt, and M3-05 §3 defines the investigation contract, but the explicit foreign-key linkage between an evidence gap row and its spawned investigator charter is an M4A derivation — M3 describes the flow as a process, not a data relationship. |

### Category 3: PIT Lock Mode Enumerations

| # | Field/Object | Schema | M3 Authority | Rationale |
|---|-------------|--------|-------------|-----------|
| 7 | `mode` enum (LIVE_CASE_UPDATE / SEALED_HISTORICAL_EVALUATION / REPLAY_EXCEPTION) | **I-2: PITContext** (PITC-01) | M3-01 §8 (PIT Lock) | M3-SERVICES S7 defines PIT Lock as an INFRASTRUCTURE service with FAIL_OPEN behavior, and M3-01 §8 mandates AS_OF_DATE locking. However, the three specific PIT modes (LIVE, SEALED, REPLAY) are M4A-level operational semantics — M3 only specifies the existence of a lock, not the mode taxonomy. |

### Category 4: Schema IDs and Naming Convention

| # | Convention | Scope | M3 Authority | Rationale |
|---|-----------|-------|-------------|-----------|
| 8 | Schema ID format (XX-NN) | All schemas | None — M4A design convention | M3 does not prescribe a schema naming convention. The SM-01 / RU-01 / SR-01 / CASE-01 / etc. naming scheme is an M4A derivation for implementation clarity. |
| 9 | UUID v7 as primary ID | Most schemas | None — M4A design choice | M3 does not mandate UUID v7 specifically. M4A derives this from the general requirement for append-only immutable records with unique identifiers. |

### Summary of NEW_M4A_DERIVATION

| Category | Count | Status |
|----------|-------|--------|
| Operational telemetry schemas | 5 | Derived from M3 concept (Run Manifest, Service Registry) |
| Evidence Gap → Investigator Charter link | 1 | Derived from M3-03/M3-05 process flow |
| PIT mode enumeration | 1 | Derived from M3 PIT Lock concept |
| Schema naming / ID conventions | 2 | M4A design decisions (no M3 precedent) |
| **Total** | **9** | |

All NEW_M4A_DERIVATION items are implementation-level concretions of M3 concepts. No M4A schema contradicts or departs from M3 authority — every schema traces to a specific M3 clause at the conceptual level. The derivations above merely specify data models where M3 defined only process, policy, or architectural requirements.

---

## Cross-Reference: M3 Contracts Used

| M3 Contract | Schemas Traced |
|-------------|---------------|
| M3-01 Operating Model | CASE-01, RSR-01, RFR-01, RSR-02, RB-01, RRM-01, PITC-01, RR-01, BU-01, MOD-01, PROV-01 |
| M3-02 Discovery & Selection | SM-01, RU-01, SR-01, CR-01, QU-01 |
| M3-03 Full Research Protocol | CASE-01, EG-01, RC-01, RSR-01, RB-01, RFR-01, HYP-01 |
| M3-04 Evidence & Source Model | SRC-01, EV-01, FACT-01, CLM-01, INF-01, HYP-01, CTR-01, EAR-01 |
| M3-05 Scuttlebutt Protocol | IC-01, EG-01 |
| M3-06 Business Quality | QU-01, QA-01, MA-01, IE-01, MC-01, CAE-01, MDL-01, IPR-01 |
| M3-07 Dislocation & Impairment | DR-01, IA-01, CE-01, RM-01, TK-01, FE-01 |
| M3-08 Financial Reconstruction | FF-01, NFF-01, CALC-01, SR-02, PLA-01, RDCF-01, VA-01 |
| M3-09 Challenge/Audit/Underwriting | PUB-01, FDR-01, RTC-01, AG-01, AF-01, UV-01 |
| M3-10 Monitoring/Knowledge | MI-01, MO-01, MASS-01, CL-01, IKR-01, IPR-01 |
| M3-LOGICAL Logical Organization | SI-01 |
| M3-ROLES Production Roles | SI-01 |
| M3-SERVICES System Services | PITC-01, RR-01, CLK-01, EHR-01 |
| M4B (forward reference) | MOD-01 |

---

<!-- 2026-08-19 15:00 UTC+7 -->