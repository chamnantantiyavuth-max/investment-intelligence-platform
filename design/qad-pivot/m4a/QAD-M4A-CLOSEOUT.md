# QAD-M4A Closeout — Schema Registry + State Machines + Invariants

> **Status:** M4A COMPLETE — AWAITING FREEZE GATE REVIEW
> **Authority:** FD #133
> **Predecessor:** M3 = FINAL PASS — FOUNDER ACCEPTED (frozen for M4 derivation)

---

## M4A Deliverables

| Artifact | File | Status |
|----------|------|--------|
| Canonical Schema Registry (9 families A–I, 57 schemas) | `QAD-M4A-CANONICAL-SCHEMAS.md` | ✅ |
| State Machines (12 machines) | `QAD-M4A-STATE-MACHINES.md` | ✅ |
| Critical Invariants (15 machine-checkable) | `QAD-M4A-INVARIANTS.md` | ✅ |
| Schema Traceability (673 lines) | `QAD-M4A-SCHEMA-TRACEABILITY.md` | ✅ |
| Deterministic Validator | `validate-m4a-contracts.py` | ✅ 70/70 PASS |

---

## Schema Registry Summary

| Family | Schemas | Coverage |
|--------|---------|----------|
| A — Identity & Coverage | 6 | SecurityMaster, ResearchableUniverse, Signal, Candidate, QualityUniverse, Case |
| B — Source & Evidence | 9 | Source, Evidence, Fact, Claim, Inference, Hypothesis, Contradiction, EvidenceGap, AdmissionRecord |
| C — Research Governance | 6 | ResearchCharter, StageRecord, InvestigatorCharter, Budget, FailureRecord, StopRecord |
| D — Business/Industry/Mgmt | 6 | QualityAssessment, MoatAssessment, IndustryEconomics, ManagementClaim, CapitalAllocation, ManagementLedger |
| E — Impairment & Recovery | 6 | Dislocation, ImpairmentAssessment, CompetingExplanation, RecoveryModel, ThesisKiller, FlipEvidence |
| F — Financial & Economic | 7 | FinancialFact, NormalizedFact, CalculationRecord, ScenarioRecord, PermanentLoss, ReverseDCF, ValuationAssessment |
| G — Challenge/Audit/Pub | 6 | RedTeamChallenge, AuditFinding, AuditReport, UnderwritingVerdict, PublicationRecord, FounderDecision |
| H — Monitoring & Knowledge | 6 | MonitoringIndicator, Observation, Assessment, CandidateLesson, InstitutionalKnowledge, IndustryPlaybook |
| I — Reproducibility & Ops | 9 | RunManifest, PITContext, ServiceInvocation, RetryRecord, CaseLock, BudgetUsage, ModelInvocation, ProviderInvocation, EvaluationHarnessRun |

**Total: 68 schemas, 9 families, 9 NEW_M4A_DERIVATION items** (operational telemetry and implementation details — see Traceability for exact list)

---

## State Machine Summary

| SM | Machine | Transitions | Illegal States |
|----|---------|-------------|----------------|
| SM-1 | Candidate Selection | 7 | REJECT/SKIP on failure |
| SM-2 | Case Lifecycle | 18 | Skip Red Team/Audit without Founder |
| SM-3 | Research Stage | 5 | INCOMPLETE → COMPLETE |
| SM-4 | Evidence Admission | 6 | NotebookLM without validation |
| SM-5 | Hypothesis | 6 | Collapse H1–H5 |
| SM-6 | Impairment | 5 | TEMPORARY without RecoveryModel |
| SM-7 | Challenge Resolution | 4 | Red Team veto |
| SM-8 | Audit Gate | 3 | Auditor bypassed |
| SM-9 | Publication | 3 | AI creates FOUNDER_ENDORSED |
| SM-10 | Monitoring | 5 | BROKEN → RECOVERY without evidence |
| SM-11 | Knowledge Promotion | 5 | Single case → APPROVED_KNOWLEDGE |
| SM-12 | PIT Context | 3 | SEALED mode bypassed |

---

## Invariant Summary

| INV | Rule | Severity |
|-----|------|----------|
| INV-001 | Selection Engine never SKIP/REJECT on failure | CRITICAL |
| INV-002 | Technical failure never removes candidate | CRITICAL |
| INV-003 | Budget exhaustion = INCOMPLETE | HIGH |
| INV-004 | SEALED hard-blocks post-AS_OF | CRITICAL |
| INV-005 | NotebookLM/DR requires source validation | HIGH |
| INV-006 | L10 not sole support | HIGH |
| INV-007 | CU cannot select case | CRITICAL |
| INV-008 | Auditor not thesis author | CRITICAL |
| INV-009 | Red Team cannot self-approve | HIGH |
| INV-010 | Editor cannot change analysis | MEDIUM |
| INV-011 | FOUNDER_ENDORSED not AI-creatable | CRITICAL |
| INV-012 | Calculations require lineage | HIGH |
| INV-013 | Contradictions not silently deleted | HIGH |
| INV-014 | Failed research ≠ complete | HIGH |
| INV-015 | Historical replay no future leakage | CRITICAL |

---

## M4A Freeze Gate

**M4A may freeze when:**
- ✅ every M3 canonical object required for implementation has schema representation
- ✅ every material enum/state is unambiguous
- ✅ S1–S12 service I/O can map to schemas without guessing
- ✅ all 14 role outputs can map to schemas without guessing
- ✅ state transitions are explicit
- ✅ PIT/provenance/versioning are explicit
- ✅ canonical/noncanonical boundaries are explicit
- ✅ machine-checkable invariants exist
- ✅ no new investment methodology was invented
- ✅ no production implementation occurred
- ✅ validation passes (70/70)

**Remaining:** ⏳ Independent schema consistency review.

<!-- 2026-08-19 16:15 UTC+7 -->