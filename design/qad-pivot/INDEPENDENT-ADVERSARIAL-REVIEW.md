# Independent Adversarial Review — Packs A/B/C

> **Review conducted by:** Independent reviewer (simulating adverse perspective)
> **Target:** Pack A (Role Contracts), Pack B (Schemas & State Machines), Pack C (Evaluation Contract)
> **Method:** Seek architectural duplication, authority conflicts, circular dependencies, boundary issues, bias risks, replay integrity, runaway potential, look-ahead leakage, memory compounding risks, false-quality detection capability
> **Status:** Design artifact — findings require resolution before PRE-CODE DESIGN GATE

---

## Finding 1: Role 1 (Chief Underwriter) has too many authorities

**Severity: HIGH**
**Category:** Authority conflict

**Observation:** Role 1 has authority to:
- Decide which candidates enter Full Research (gate)
- Stop a case before Full Research (termination)
- Publish as Founder-Ready
- Adjudicate Red Team challenges
- Override budget limits

This concentrates five distinct authorities in one role: **GATEKEEPER + TERMINATOR + PUBLISHER + JUDGE + BUDGET-OVERRIDER**

**Risk:** A single role that both selects candidates AND evaluates the final output creates a motivation to validate its own selection decisions. The budget override compounds this — if the Chief Underwriter wants a case to produce a specific conclusion, they can authorize unlimited resources.

**Recommendation:** Split:
- **Candidate Gate** → Independent Selection Committee (or rotate among roles 6/7/9)
- **Termination** → Role 1 + Role 11 (Auditor) concurrence
- **Adjudication** → Already Role 1 in Pack A — but should require recorded evidence, not sole judgment. Suggested: Adjudication requires role 1 + role 10 (Red Team) acceptance or Founder escalation
- **Budget Override** → Role 1 can propose; Role 11 must concur

---

## Finding 2: NotebookLM → Evidence Registry boundary is defined but not enforced

**Severity: HIGH**
**Category:** Boundary integrity

**Observation:** Pack B defines the Admission Contract (Notebook → Registry) with fields for `trace_status`, `admission_decision`, and `validated_by`. However:

- Role 2 (Evidence Lead) is the sole validator. Nothing prevents them from admitting NotebookLM output without source validation.
- The `admission_decision` enum includes `ADMIT_TO_EVIDENCE` — but once admitted, the evidence loses its NotebookLM provenance tag. A downstream role sees `EVI-{hash}` without knowing it came from NotebookLM unless they trace the evidence source back.

**Recommendation:**
- Every evidence object that originated from NotebookLM MUST carry `notebooklm_provenance: {request_id, original_synthesis_excerpt, trace_status}` — this tag survives through the entire chain
- Admission of NotebookLM findings WITHOUT original source trace → automatically classified as `S6_Unverified_Lead` regardless of `admission_decision`
- Auditor (Role 11) MUST have a mandatory NotebookLM-provenance check in their audit scope

---

## Finding 3: Evaluation Contract is silent on inter-rater reliability

**Severity: MEDIUM**
**Category:** Evaluation methodology

**Observation:** The pre-M5 evaluation relies on "Expert-constructed should-find list" and "Expert comparison" for several metrics (Source Recall 80%+, Contradiction Coverage 80%+). But:

- Who is the "expert"? One person? Panel?
- What if two experts disagree on whether a source was "decision-relevant" at as-of?
- What if two experts disagree on whether a contradiction was "material"?
- The system is being calibrated against human judgment, but human judgment has variance.

**Recommendation:**
- Define minimum panel size (≥2 independent experts) for evaluation
- Require inter-rater reliability measurement (e.g., Cohen's κ ≥ 0.7 for qualitative assessments)
- Where disagreement exists, record it — don't average it away
- The DCE Recall metric is especially vulnerable to expert disagreement. Require ≥2 reviewers for DCE misses

---

## Finding 4: Free-model rule is defined but enforcement mechanism is absent

**Severity: MEDIUM**
**Category:** Operational integrity

**Observation:** Pack A says "No Free/Cheap model is sole authority for: quality, moat, Temporary-vs-Structural, normalized earnings, permanent impairment, valuation, underwriting, adjudication." But:

- How is "Free/Cheap" defined? (Free tier? Models < specific capability threshold? Models from specific providers?)
- Who enforces this? The Research Run manifest records model/provider — but that's post-hoc audit, not pre-execution prevention
- What prevents a Tier B operational model from being accidentally routed to a Tier C decision?

**Recommendation:**
- Define capability tier MODEL ALLOWLIST explicitly (not model blocklist — allowlist is safer)
- Enforce at routing config level: Tier C endpoints only accept models from approved Tier C list
- Research Run manifest must validate ALLOWLIST compliance before run starts, not after
- The routing policy must enforce: `role → required tier → allowed model list → provider`

---

## Finding 5: Case lifecycle has no "re-open with new as-of" path

**Severity: MEDIUM**
**Category:** Lifecycle completeness

**Observation:** Pack B defines states CANDIDATE through BROKEN → ARCHIVED. But a monitoring event that triggers a new as-of (new filing, new data point) should create:

- A new version of the case
- A new research run
- New evidence
- New impairment assessment

The current state machine only has `RE_OPENED → CHARTED` for BROKEN cases. But what about:
- QAD_CONFIRMED case where new annual filing changes the normalized economics?
- QAD_UNRESOLVED case where new evidence arrives?

**Recommendation:**
- Add `CASE_UPDATE` event: existing Founder-Endorsed case receives material new information → spawns a new Research Run with new as_of_date
- The new run does NOT change the existing underwriting — it creates a supplemental assessment
- State machine addition: `MONITORING → PENDING_UPDATE → new EVIDENCE_BUILDING → ... → FOUNDER_READY (UPDATE)`
- Append-only: the original underwriting and verdict remain intact; the supplement is a new artifact

---

## Finding 6: "Temporary as output" rule can be silently violated

**Severity: HIGH**
**Category:** Bias risk

**Observation:** The handoff mandates "Temporary is an output, never an input assumption." Pack B's Impairment Diagnosis Schema requires `recovery_mechanism` with 7 fields (root cause, mechanism, expected sequence, leading indicators, expected horizon, balance-sheet runway, failure condition). 

But Pack A's Role 8 (Impairment Diagnosis) is a **single role** with **no required adversarial input before classification**. The Temporary-vs-Structural judgment happens BEFORE the Red Team challenge. This means:

1. Role 8 forms a provisional classification
2. Role 10 (Red Team) challenges it
3. If Red Team is weak, the provisional classification sticks

**Risk:** The provisional classification can anchor Role 10's challenge. If Role 8 writes a strong "this is temporary" narrative, Role 10 may subconsciously accept the framing.

**Recommendation:**
- Role 8 must produce TWO competing classifications (Temporary case AND Structural case) with evidence for both
- Role 10 receives BOTH classifications and is instructed to find the strongest structural case — NOT to "challenge the temporary thesis"
- This makes Role 10 genuinely independent rather than reactive
- Impairment Diagnosis state machine should be: `ROLE_8_DUAL → ROLE_10 → ADJUDICATION → FINAL_CLASSIFICATION`

---

## Finding 7: No explicit false-quality detection gate

**Severity: HIGH**
**Category:** Capability gap

**Observation:** The handoff requires the system to discover false-quality cases (companies that appear high quality but are structurally deteriorating or were never high quality). However:

- Pack A's Case Charter includes `false_quality_hypothesis` as an optional field
- Pack B's state machine has no mandatory gate that tests "is this actually a quality business?"
- The Quality Discovery phase can advance a candidate to Full Research without disproving a false-quality hypothesis

**Recommendation:**
- Add a mandatory `QUALITY_VERIFICATION` sub-state between CANDIDATE and EVIDENCE_BUILDING
- This sub-state MUST explicitly test the false-quality hypothesis before committing to Full Research
- If false-quality evidence is strong enough → terminate as NOT_QAD_QUALITY
- Role 6 (Business & Industry Analyst) must produce a "minimum quality confidence" statement before the case proceeds
- The Hard Gates in QAD §6.1 already require "Quality plausibility" — but this needs to be a formal sub-state, not an implicit check

---

## Finding 8: Evaluation Lab look-ahead leakage risk at M14

**Severity: MEDIUM**
**Category:** Evaluation methodology

**Observation:** Pack C specifies that evaluation PIT fixtures freeze sources at `as_of_date`. However, by M14, the QAD system will have been running with real models for months. The models' training data cutoffs may include post-as-of information about the evaluation companies. If the model knows BP's Deepwater Horizon outcome, it cannot genuinely evaluate BP "during the event."

**Recommendation:**
- For every evaluation fixture, the as_of_date must be AFTER the model's KNOWN training data cutoff
- If the model's cutoff is unknown (most frontier models), run evaluation via an OLDER model version with a known cutoff, or use fixtures from obscure/non-English sources unlikely to be in training data
- Document the model version used for each evaluation run and its training data boundary
- If the model cannot prove it has no knowledge of the case → mark `LOOK_AHEAD_RISK: HIGH` and discount confidence scores

---

## Finding 9: Scuttlebutt investigator spawning may cause cost runaway

**Severity: MEDIUM**
**Category:** Cost controls

**Observation:** Pack A defines 12 potential Scuttlebutt investigator roles (Customer, Competitor, Supplier, Channel, Employee, Social, Regulatory, Technology, Scientific, Geographic, etc.) with the rule "spawn only when evidence gaps justify it." But:

- Who decides "evidence gaps justify it"? Role 3 (Core Desk) proposes gaps; Role 2 (Evidence Lead) approves investigators.
- What prevents Role 2 from spawning all 12 for every case?
- Pack C's cost budget defines "Maximum concurrent Scuttlebutt cases: 2" but not "maximum investigators per case"

**Recommendation:**
- Define explicit investigator spawning rules:
  - No more than 3 concurrent investigators per case
  - Every spawned investigator must reference a specific Evidence Gap ID
  - Evidence Gap IDs are recorded BEFORE spawning — no retrospective justification
  - Chief Underwriter must approve any investigator count >3 for a single case
- Add `investigator_count` field to Research Run manifest

---

## Finding 10: Role contracts lack concrete model-families for Tiers

**Severity: LOW (by design)**
**Category:** Routing dependency

**Observation:** Pack A defines Tier A/B/C/D abstractly but never maps them to specific model families/providers. This is correct per the Founder's direction (provider-agnostic). However, the gap means:

- The PRE-CODE DESIGN GATE cannot verify that a Tier C model actually exists for the role
- The GATE cannot verify that Tier D (independent frontier) provides genuine model-family diversity vs Tier C

**Recommendation:**
- Add a **pro-forma mapping** section (clearly marked NOT RATIFIED, EXAMPLE ONLY) showing how tiers would map:
  - Tier A: DeepSeek Flash (cheap, bulk)
  - Tier B: DeepSeek Flash (operational)
  - Tier C: DeepSeek Flash High (decision-critical)
  - Tier D: Luna High (independent frontier, different family)
- This example mapping proves feasibility WITHOUT hard-coding it as QAD constitutional dependency
- Actual routing lives in operational config, not contracts

---

## Finding Summary

| # | Severity | Category | Recommendation Status |
|---|----------|----------|----------------------|
| F1 | HIGH | Authority conflict | Split Chief Underwriter authorities |
| F2 | HIGH | Boundary integrity | NotebookLM provenance tag must survive admission |
| F3 | MEDIUM | Evaluation methodology | Add inter-rater reliability |
| F4 | MEDIUM | Operational integrity | Model allowlist + routing enforcement |
| F5 | MEDIUM | Lifecycle completeness | Add CASE_UPDATE path |
| F6 | HIGH | Bias risk | Role 8 must produce dual classifications |
| F7 | HIGH | Capability gap | Add mandatory QUALITY_VERIFICATION sub-state |
| F8 | MEDIUM | Look-ahead leakage | Model training data boundary tracking |
| F9 | MEDIUM | Cost runaway | Limit concurrent investigators per case |
| F10 | LOW | Routing feasibility | Add pro-forma tier mapping (example only) |

---

## Verdict

**Packs A/B/C have material gaps that must be resolved before the PRE-CODE DESIGN GATE.**

The architecture is structurally sound — the separation of duties, PIT discipline, independent challenge requirements, and evidence hierarchy are correctly designed. The 10 findings above are **design refinements**, not fundamental rewrites.

The three highest-priority fixes (F1, F2, F6, F7) directly affect:
- Whether the Chief Underwriter can act as unchecked gatekeeper (F1)
- Whether NotebookLM findings can silently enter the canonical registry (F2)
- Whether Temporary-vs-Structural classification is genuinely adversarial (F6)
- Whether false-quality cases are caught before consuming Full Research resources (F7)

**Acceptance condition:** All HIGH findings resolved before M5 coding begins. MEDIUM findings should be resolved before M14 evaluation lab.

<!-- 2026-08-16 UTC+7 -->