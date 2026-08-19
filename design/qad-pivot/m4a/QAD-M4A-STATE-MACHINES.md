# QAD-M4A Canonical State Machines

> **Status:** M4A IN PROGRESS
> **Authority:** FD #133; M3 Frozen Domain Contracts
> **Traceability:** Every state machine traces to M3 contract clause — see QAD-M4A-SCHEMA-TRACEABILITY.md

---

## State Machine Template

Every state machine defines:

```text
FROM state
    EVENT
    PRECONDITIONS
    AUTHORIZED ACTOR/SERVICE
    TO state
    SIDE EFFECTS
    FAILURE STATE
    AUDIT LOG
```

Illegal transitions must be explicit.

---

## SM-1: Candidate Selection State Machine

**Authority:** M3-02 §4 (Selection States), M3-02 §5 (Candidate Assembly)

```text
NOT_EVALUATED
    → Signal(s) detected → Candidate assembled
    → precondition: signals in SIGNAL_REGISTRY
    → authorized: Candidate Assembly
    → PENDING_EVALUATION
    → side effects: CandidateRecord created

PENDING_EVALUATION
    → Selection Engine evaluates
    → precondition: policy rules loaded
    → authorized: Selection Engine (S1)
    → AUTO_RESEARCH_NOW / WATCH_PRICE / WATCH_EVIDENCE / DATA_LIMITED_WATCH / REJECT
    → side effects: CandidateRecord.selection_state updated
    → failure: SELECTION_ERROR (candidate remains pending/retryable)

AUTO_RESEARCH_NOW
    → Capacity check → Case Open
    → precondition: Research Budget Controller approves
    → authorized: Research Director
    → CASE_OPENED
    → side effects: CaseRecord created, ResearchCharter drafted

WATCH_PRICE
    → Price threshold breached
    → precondition: threshold defined
    → authorized: automated
    → AUTO_RESEARCH_NOW
    → side effects: CandidateRecord re-evaluated

WATCH_EVIDENCE
    → Evidence condition met
    → precondition: condition defined
    → authorized: automated
    → PENDING_EVALUATION

DATA_LIMITED_WATCH
    → New data available
    → authorized: automated
    → PENDING_EVALUATION

REJECT
    → (terminal state) — may be re-evaluated on evidence change
    → authorized: Selection Engine
    → side effects: rejection_reason documented

SELECTION_ERROR
    → Retry (max 3) → retry succeeds → PENDING_EVALUATION
    → Retry exhausted → escalated to operator attention
    → failure: candidate remains in SELECTION_ERROR
```

**ILLEGAL:** Selection Engine failure → REJECT or SKIP. Technical failure must NEVER silently remove a candidate.

---

## SM-2: Case Lifecycle State Machine

**Authority:** M3-03 §3 (Stages 1-18), M3-03 §4 (Stage State Lifecycle)

```text
CASE_OPEN → CHARTER_APPROVED → SOURCE_FOUNDATION_COMPLETE
    → INITIAL_ANALYSIS_COMPLETE → DEEP_RESEARCH_COMPLETE
    → SCUTTLEBUTT_COMPLETE → EVIDENCE_CANONICAL
    → QUALITY_ANALYSIS_COMPLETE → ANALYTICAL_WORK_COMPLETE
    → IMPAIRMENT_DIAGNOSIS_COMPLETE → VALUATION_COMPLETE
    → RED_TEAM_COMPLETE → AUDIT_COMPLETE
    → UNDERWRITING_COMPLETE → FOUNDER_READY
    → FOUNDER_DECIDED → MONITORING → CLOSED

Any stage
    → Budget exhaustion → INCOMPLETE (not weakened quality)
    → Failure + retries exhausted → FAILED
    → → side effects: documented in ResearchFailureRecord

CASE_OPEN
    → Authorized: Research Director
    → precondition: candidate in AUTO_RESEARCH_NOW state
    → side effects: CaseRecord created, ResearchCharter creation initiated

CHARTER_APPROVED → SOURCE_FOUNDATION
    → Authorized: Evidence Intelligence Lead validates charter
    → precondition: H1–H5 present, charter validated, budget approved
    → side effects: ResearchCharter set to BUDGET_APPROVED

FOUNDER_READY
    → Founder reviews
    → Authorized: Founder only
    → FOUNDER_DECIDED / FOUNDER_DISAGREES / FOUNDER_REJECTS
    → side effects: PublicationRecord updated

FOUNDER_DECIDED → MONITORING
    → Authorized: Knowledge Steward
    → side effects: Monitoring indicators activated

MONITORING → CLOSED
    → Authorized: Knowledge Steward
    → precondition: thesis indicators resolved or thesis abandoned
```

**ILLEGAL:** Skip Red Team → FOUNDER_READY (Founder-only override). Skip Audit → FOUNDER_READY (Auditor must block). Budget exhaustion → any state that implies completeness.

---

## SM-3: Research Stage State Machine

**Authority:** M3-03 §4 (Stage State Lifecycle), M3-01 §7 (Reliability Contract)

```text
NOT_STARTED
    → Stage begins
    → precondition: previous stage COMPLETE
    → authorized: Research Director
    → IN_PROGRESS

IN_PROGRESS
    → Stage completes successfully → COMPLETE
    → Stage fails → retry (max 3) → succeeds → COMPLETE
    → Stage fails → retries exhausted → FAILED
    → Budget exhausted → INCOMPLETE
    → Stage deliberately skipped → SKIPPED (documented reason)
    → side effects: ResearchStageRecord updated

COMPLETE → (next stage can begin)
    → verified by: stage quality gate
    → side effects: outputs passed to next stage

FAILED → (escalation to Research Director)
    → side effects: ResearchFailureRecord created

INCOMPLETE → (documented as incomplete; not COMPLETE)
    → side effects: ResearchFailureRecord created
    → may NOT be used as "COMPLETE" for quality gate

SKIPPED → (documented reason; Founder-only for Red Team/Audit)
    → side effects: ResearchStopRecord created
```

**ILLEGAL:** INCOMPLETE → COMPLETE. FAILED → COMPLETE without correction. SKIPPED without Founder authorization for Red Team/Audit.

---

## SM-4: Evidence Admission State Machine

**Authority:** M3-04 §2 (Layer 2: Canonical Evidence Registry), M3-04 §5 (Admission Gate)

```text
RAW
    → Evidence Intelligence Lead validates
    → precondition: source exists, PIT verified, source_tier checked
    → authorized: Evidence Intelligence Lead (Role 2)
    → VALIDATED / CONTRADICTED / DISPUTED

VALIDATED → (canonical evidence, may be used in analysis)
    → side effects: EvidenceAdmissionRecord created

CONTRADICTED
    → (evidence preserved with contradiction noted)
    → side effects: ContradictionRecord created

SUPERSEDED
    → (newer evidence replaces this)
    → side effects: superseded_by pointer set

RETRACTED
    → (admitted in error; retraction recorded)
    → authorized: Evidence Intelligence Lead
    → side effects: retraction record with reason

DISPUTED
    → (status disputed by analyst/Red Team)
    → side effects: dispute record created
```

**ILLEGAL:** NotebookLM/Deep Research output → VALIDATED without original-source validation. L10 → VALIDATED as sole material support.

---

## SM-5: Hypothesis State Machine

**Authority:** M3-03 §2 (H1–H5), M3-04 §3 (HYPOTHESIS)

```text
PROPOSED
    → (stated in Research Charter)
    → side effects: HypothesisRecord created with initial plausibility

ACTIVE
    → (hypothesis under investigation)
    → evidence_for[] and evidence_against[] tracked

STRENGTHENED
    → (new evidence increases plausibility)
    → side effects: plausibility updated with timestamp and trigger

WEAKENED
    → (new evidence decreases plausibility)
    → side effects: plausibility updated with timestamp and trigger

FALSIFIED
    → (hypothesis no longer supported by evidence)
    → side effects: recorded in ResearchStopRecord

RESOLVED
    → (final disposition: confirmed or rejected)
    → side effects: verdict documented
```

**ILLEGAL:** Hypotheses collapsed into one bullish thesis. H1–H5 incomplete at Charter stage.

---

## SM-6: Impairment State Machine

**Authority:** M3-07 §3 (Impairment States)

```text
NOT_ASSESSED
    → Evidence gathered → Impairment Specialist assesses
    → authorized: Impairment Diagnosis Specialist (Role 6)
    → TEMPORARY / MOSTLY_TEMPORARY / MIXED / STRUCTURAL / UNRESOLVED

TEMPORARY → (may be updated on new evidence)
    → side effects: RecoveryModel created

MOSTLY_TEMPORARY → (may be updated on new evidence)

MIXED → (both temporary and structural elements)

STRUCTURAL → (permanent damage to business model)
    → side effects: escalated to Chief Underwriter

UNRESOLVED → (insufficient evidence)
    → side effects: evidence gaps documented
```

**ILLEGAL:** TEMPORARY without RecoveryModel. STRUCTURAL without escalation. UNRESOLVED without evidence gaps.

---

## SM-7: Challenge Resolution State Machine

**Authority:** M3-09 §2 (Structural Red Team)

```text
PENDING
    → Red Team reviews
    → precondition: full analytical record available
    → authorized: Structural Red Team (Role 9)
    → ACCEPTED / PARTIALLY_ACCEPTED / REJECTED_WITH_EVIDENCE / UNRESOLVED

ACCEPTED → (Red Team findings accepted by Underwriter)
    → side effects: findings incorporated into verdict

PARTIALLY_ACCEPTED → (some findings accepted, others rejected)

REJECTED_WITH_EVIDENCE → (Underwriter rejects with evidence)
    → side effects: evidence for rejection documented

UNRESOLVED → (Red Team and Underwriter disagree)
    → side effects: both positions preserved for Founder
```

**ILLEGAL:** Red Team findings suppressed. Red Team veto (no veto power).

---

## SM-8: Audit Gate State Machine

**Authority:** M3-09 §3 (Independent Audit)

```text
PENDING
    → Auditor reviews
    → precondition: all preceding stages complete
    → authorized: Independent Research Auditor (Role 10)
    → PASS / PASS_WITH_FINDINGS / FAIL

PASS → (case proceeds to Founder)
    → side effects: AuditReport created

PASS_WITH_FINDINGS → (minor non-blocking findings)
    → side effects: findings recorded; case proceeds

FAIL → (case blocked)
    → side effects: case blocked at FOUNDER_READY
    → cannot be overridden by Research Director
    → resolution: findings corrected → re-audit → PASS / FAIL
```

**ILLEGAL:** Auditor decides thesis. Auditor bypassed. FAIL overridden by Research Director.

---

## SM-9: Publication State Machine

**Authority:** M3-09 §5 (Publication)

```text
RESEARCH_COMPLETE
    → Thai Editor writes publication
    → authorized: Thai Editor (Role 11)
    → FOUNDER_READY

FOUNDER_READY
    → Founder reviews
    → authorized: Founder only
    → FOUNDER_ENDORSED / FOUNDER_DISAGREES / FOUNDER_REJECTS

FOUNDER_ENDORSED → (Founder agrees with thesis)
    → side effects: FD registered, article published

FOUNDER_DISAGREES → (Founder disagrees but publishes)
    → side effects: FD registered, dissent noted

FOUNDER_REJECTS → (thesis rejected)
    → side effects: FD registered, case disposition updated
```

**ILLEGAL:** AI/service creates FOUNDER_ENDORSED. Only Founder may set FOUNDER_ENDORSED.

---

## SM-10: Monitoring State Machine

**Authority:** M3-09 §6.3 (Monitoring States)

```text
ACTIVE
    → Thesis indicators tracked
    → authorized: Knowledge Steward (Role 12)
    → RECOVERY_CONFIRMING / ON_TRACK / UNCERTAIN / WEAKENING / BROKEN

RECOVERY_CONFIRMING → indicators tracking as expected
ON_TRACK → mixed signals but overall direction holds
UNCERTAIN → evidence ambiguous
WEAKENING → evidence points away from thesis
BROKEN → thesis no longer supported
    → side effects: Founder notified
```

**ILLEGAL:** BROKEN → RECOVERY_CONFIRMING without evidence. Monitoring without thesis-specific indicators.

---

## SM-11: Knowledge Promotion State Machine

**Authority:** M3-09 §7 (Knowledge Compounding)

```text
RESEARCH_FINDING
    → (single case observation)
    → requires: 2+ cases with consistent pattern
    → CANDIDATE_LESSON

CANDIDATE_LESSON
    → (tentative generalization)
    → requires: 3+ independent cases
    → CROSS_CASE_VALIDATED

CROSS_CASE_VALIDATED
    → (pattern tested across multiple cases)
    → requires: independent review
    → INDEPENDENTLY_REVIEWED

INDEPENDENTLY_REVIEWED
    → (reviewed by different role)
    → requires: Chief Underwriter approval
    → APPROVED_KNOWLEDGE

APPROVED_KNOWLEDGE
    → (institutional knowledge)
    → side effects: may be added to Industry Playbook
```

**ILLEGAL:** Single case → APPROVED_KNOWLEDGE. Knowledge without cross-case validation.

---

## SM-12: PIT Context State Machine

**Authority:** M3-SERVICES S7 (PIT Lock)

```text
LIVE_CASE_UPDATE
    → post-AS_OF evidence ALLOWED only as explicitly tagged UPDATE
    → authorized: Research Director
    → side effects: evidence tagged with UPDATE provenance

SEALED_HISTORICAL_EVALUATION
    → post-AS_OF evidence HARD BLOCKED
    → authorized: Evaluation Harness (S12)
    → side effects: any post-AS_OF query returns error
    → used for: M4B evaluation, historical benchmarks

REPLAY_EXCEPTION
    → explicit, provenance-recorded exception
    → authorized: Founder only
    → side effects: exception provenance recorded
```

**ILLEGAL:** SEALED mode bypassed. REPLAY without Founder authorization.

<!-- 2026-08-19 15:30 UTC+7 -->