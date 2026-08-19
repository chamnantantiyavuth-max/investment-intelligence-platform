# QAD-M4A Critical Invariants

> **Status:** M4A FINAL — FROZEN FOR M4B DERIVATION
> **Authority:** FD #133; M3 Frozen Domain Contracts
> **Purpose:** Machine-checkable rules that must always hold. Every invariant violation must be caught by automated validation.

---

## Invariant Template

```text
INVARIANT ID
  Rule
  Source
  Enforcement
  Failure Consequence
```

---

## I-1: Selection Engine Failure Never Produces REJECT/SKIP

```
INV-001
  Rule: A Selection Engine system/service failure must produce SELECTION_ERROR,
  not REJECT or SKIP.
  Source: M3-02 §4, M3-01 §7 (Failure States), QAD-M3-SERVICE-CONTRACTS.md S1
  Enforcement: Check CandidateRecord.selection_state transition.
  If failure occurred and state is REJECT or SKIP → VIOLATION.
  Failure Consequence: Candidate remains pending/retryable.
  Technical failure must never silently create a Type-B discovery miss.
```

## I-2: Technical Failure Never Silently Removes a Candidate

```
INV-002
  Rule: A technical failure in any system component must never silently
  remove a candidate from the CANDIDATE_REGISTRY.
  Source: M3-01 §7, M3-02 §5
  Enforcement: CANDIDATE_REGISTRY is append-only. Check for deletion events.
  Failure Consequence: Candidate remains in registry with error state.
```

## I-3: Budget Exhaustion = INCOMPLETE

```
INV-003
  Rule: Budget exhaustion must produce INCOMPLETE, never a weakened quality gate.
  Source: M3-01 §9, M3-03 §4
  Enforcement: If budget_state = EXHAUSTED and stage_state ≠ INCOMPLETE → VIOLATION.
  Failure Consequence: Case marked INCOMPLETE. Not published as complete research.
```

## I-4: SEALED Historical Evaluation Hard-Blocks Post-AS_OF Evidence

```
INV-004
  Rule: In SEALED_HISTORICAL_EVALUATION mode, any query returning
  post-AS_OF evidence must be blocked.
  Source: M3-SERVICES S7 (PIT Lock), QAD-M3-SERVICE-CONTRACTS.md S7
  Enforcement: PITContext.mode = SEALED and evidence.as_of > PITContext.as_of_date
  → HARD BLOCK.
  Failure Consequence: No future-information leakage into M4B fixtures.
```

## I-5: NotebookLM/DR Output Cannot Enter Canonical Evidence Without Validation

```
INV-005
  Rule: Evidence extracted from NotebookLM or Deep Research must be validated
  against original source before canonical admission.
  Source: M3-04 §4, M3-04 §2 (Layer 2 admission)
  Enforcement: If EvidenceAdmissionRecord.admission_method = AI_SYNTHESIS
  and no original_source_verified flag → VIOLATION.
  Failure Consequence: Evidence quarantined; cannot be used in analysis.
```

## I-6: L10 Cannot Be Sole Support for Material Conclusion

```
INV-006
  Rule: L10 source-tier evidence cannot independently support a material conclusion
  (quality, impairment, valuation, underwriting).
  Source: M3-04 §1, M3-04 §2.2
  Enforcement: If material conclusion cites only L10 evidence → VIOLATION.
  Failure Consequence: Conclusion flagged as insufficiently supported.
```

## I-7: Chief Underwriter Cannot Select Case

```
INV-007
  Rule: The Chief Underwriter must not select their own cases. Selection Engine
  maintains separation.
  Source: M3-09 §4.3, M3-02 §4
  Enforcement: Check entry_route for Underwriter-selected cases.
  If entry_route ≠ FOUNDER_DIRECTED and selector = Chief Underwriter → VIOLATION.
  Failure Consequence: Case selection invalidated.
```

## I-8: Auditor Cannot Author Material Thesis

```
INV-008
  Rule: The Independent Auditor must not author, contribute to, or influence
  the material thesis. Auditor checks what EXISTS, not correctness.
  Source: M3-09 §3 (Auditor does not decide thesis)
  Enforcement: Auditor role must not appear in evidence creation or analysis records.
  Failure Consequence: Audit invalidated; re-audit required.
```

## I-9: Red Team Cannot Approve Its Own Response

```
INV-009
  Rule: The Structural Red Team cannot approve or adjudicate its own challenge.
  Red Team findings are preserved verbatim; Underwriter weighs them.
  Source: M3-09 §2.4 (No veto)
  Enforcement: Red Team challenge outcome must be set by Underwriter, not Red Team.
  Failure Consequence: Challenge resolution invalidated.
```

## I-10: Publication Editor Cannot Change Analytical Conclusion

```
INV-010
  Rule: The Thai Editor may edit for clarity and readability but must not change
  analytical conclusions, remove contradictions, or add investment recommendations.
  Source: M3-09 §5.3, FD #94
  Enforcement: Publication content must be consistent with UnderwritingVerdict
  and EvidenceRecord. No contradictions removed.
  Failure Consequence: Publication flagged for editorial integrity review.
```

## I-11: FOUNDER_ENDORSED Cannot Be Created by AI/Service

```
INV-011
  Rule: Only the Founder may set FOUNDER_ENDORSED state. No AI, service, or
  automated process may create this state.
  Source: M3-09 §5.2
  Enforcement: PublicationRecord.publication_state transition to FOUNDER_ENDORSED
  must be initiated by FounderDecisionReference. Automated → BLOCKED.
  Failure Consequence: State transition rolled back; security incident logged.
```

## I-12: Derived Calculations Require Lineage

```
INV-012
  Rule: Every derived financial calculation must have explicit lineage:
  formula, inputs, result, calculator, timestamp.
  Source: M3-08 §2.3
  Enforcement: CalculationRecord must have formula, inputs[], and result.
  Missing fields → VIOLATION.
  Failure Consequence: Calculation flagged as unreproducible; cannot be used
  in underwriting.
```

## I-13: Contradictions Cannot Be Silently Deleted

```
INV-013
  Rule: Contradictory evidence must remain visible. Contradictions cannot be
  silently deleted or averaged away for presentation simplicity.
  Source: M3-04 §6, EVIDENCE-DOCTRINE
  Enforcement: ContradictionRecord with UNRESOLVED status must be preserved.
  Deletion without tombstone → VIOLATION.
  Failure Consequence: Contradiction restored; deletion recorded.
```

## I-14: Failed Research Cannot Be Represented as Complete

```
INV-014
  Rule: A research stage with FAILED or INCOMPLETE state must not be represented
  as COMPLETE for quality gate purposes.
  Source: M3-03 §4, M3-01 §7
  Enforcement: If stage_state = FAILED or INCOMPLETE and downstream stage proceeds
  as if COMPLETE → VIOLATION.
  Failure Consequence: Downstream stage blocked; escalation to Research Director.
```

## I-15: Historical Replay Cannot Leak Future Evidence

```
INV-015
  Rule: Historical evaluation/replay must use SEALED mode. Post-AS_OF evidence
  must be HARD BLOCKED. No future-information leakage.
  Source: M3-SERVICES S7, QAD-M3-SERVICE-CONTRACTS.md S7
  Enforcement: PITContext.mode = SEALED and any evidence with as_of > context_date
  is accessed → HARD BLOCK.
  Exception: REPLAY_EXCEPTION with Founder authorization and provenance.
  Failure Consequence: Evaluation invalidated; results discarded.
```

---

## Summary

| ID | Invariant | Severity | Enforceable |
|----|-----------|----------|-------------|
| INV-001 | Selection Engine never SKIP/REJECT on failure | CRITICAL | ✅ |
| INV-002 | Technical failure never removes candidate | CRITICAL | ✅ |
| INV-003 | Budget exhaustion = INCOMPLETE | HIGH | ✅ |
| INV-004 | SEALED hard-blocks post-AS_OF | CRITICAL | ✅ |
| INV-005 | NotebookLM/DR requires source validation | HIGH | ✅ |
| INV-006 | L10 not sole support | HIGH | ✅ |
| INV-007 | CU cannot select case | CRITICAL | ✅ |
| INV-008 | Auditor not thesis author | CRITICAL | ✅ |
| INV-009 | Red Team cannot self-approve | HIGH | ✅ |
| INV-010 | Editor cannot change analysis | MEDIUM | ✅ |
| INV-011 | FOUNDER_ENDORSED not AI-creatable | CRITICAL | ✅ |
| INV-012 | Calculations require lineage | HIGH | ✅ |
| INV-013 | Contradictions not silently deleted | HIGH | ✅ |
| INV-014 | Failed research ≠ complete | HIGH | ✅ |
| INV-015 | Historical replay no future leakage | CRITICAL | ✅ |

<!-- 2026-08-19 15:45 UTC+7 -->