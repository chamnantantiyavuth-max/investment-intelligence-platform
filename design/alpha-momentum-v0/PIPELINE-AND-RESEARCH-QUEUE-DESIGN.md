# Pipeline and Research Queue Design

Status: Accepted Gate A Decision-Slot Artifact
Version: 0.1
Owner: Founder
Authority: Structurally approved Gate A decision-slot artifact; individual decision-slot content gains authority only through its own named Founder approval
Derived from: Constitution v0.3, Project Definition v0.1, and Approved Stable Design Plan v0.1
Drafting Authorization: AM-V0-GATE-A-DRAFTING-v0.1
Structural Acceptance: AM-V0-GATE-A-STRUCTURAL-ACCEPTANCE-v0.1
Supersedes: v0.1-draft (DS-201–DS-218 — see Slot Supersession Map §7)

---

## 1. Inherited Approved Semantics

This section faithfully restates approved semantics that govern the Alpha Momentum screening pipeline stages, Research Queue structure, and related domain rules. No expansion or reinterpretation is intended.

### 1.1 Constitution v0.3

- **§14 Theme-First Research Queue:** The research queue is organized by Theme Card before individual stock ranking. Queue capacity is adaptive. It must not fill a quota with weak candidates. It may return zero high-priority candidates.

### 1.2 Alpha Momentum V0 Specification (Approved Domain Specification v0.1)

- **§4.1–4.2 Pipeline Stages:** Six conceptual stages: Universe Definition → Theme Context / Theme-linked Selection → Candidate Quality Assessment → Entry Readiness Assessment → Data Confidence Assessment → Research Queue Assembly. Ownership assigned per stage.
- **§4.3 Deterministic Features:** All feature computations must be deterministic. Reproducibility is required.
- **§4.4 Theme Context Boundary:** The Theme-linked pipeline is a demonstration boundary. Future versions must preserve stock-first discovery, Theme context enrichment, and combined discovery paths.
- **§5.2 Research Queue:** Theme-first, groups Candidates by Theme, presents four separated quality dimensions, supports adaptive capacity, may return zero high-priority candidates, provides human-readable explanations for prioritization.

### 1.3 Candidate and Queue Model (Approved Domain Specification v0.1)

- **§4.1 Structure:** Research Queue organized by Theme Card first, then Candidates within each Theme. Within a Theme, Candidates ordered by strategy-owned prioritization.
- **§4.2 Adaptive Capacity:** Queue capacity is adaptive. Not a fixed quota. May return zero, a small number, or a larger number. Capacity is quality-driven, not target-driven.
- **§4.3 Infrastructure vs. Semantics:** Shared Core may provide queue infrastructure. Each strategy owns its prioritization, ranking, ordering, and filtering semantics.

### 1.4 Domain Architecture (Approved Domain Specification v0.1)

- **§1.2 Alpha Momentum Owns:** Prioritization and ranking, Research Queue prioritization and ordering, Alpha Momentum-specific screening pipeline and stage definitions.
- **§1.1 Shared Core — Research Queue:** Infrastructure may be shared; semantics are strategy-owned.

### 1.5 Founder's Decisions

- **#8:** Research Queue is Theme-first.
- **#9:** Queue capacity is adaptive and may return zero candidates.

### 1.6 Design Plan (Approved Stable Design Plan v0.1)

- **§6 Gate A must not:** Populate eligibility gates, sort keys, tie-breakers, thresholds, ranking rules, or fallback behavior.
- **§7 Materiality Policy:** Material decisions include filtering, ranking, queue behavior, and missing-data behavior.

---

## 2. Active Unresolved Decision Slots

---

### Decision Slot: DS-501 — Operational V0 Universe Boundary in Pipeline Context

- **Identifier:** DS-501
- **Topic:** How the universe boundary (defined by DS-309 in RULE-PACK-AND-QUALITY-CONTRACTS.md) is operationally applied at the Universe Definition pipeline stage — what the stage consumes, what it emits, and how boundary-edge cases are handled
- **Decision Obligation Source:** ALPHA-MOMENTUM-V0-SPEC §4.2 defines Universe Definition stage. DS-309 defines the boundary. This slot addresses pipeline-specific operationalization
- **Inherited Approved Semantics:** The Universe Definition stage exists. The universe boundary is defined by DS-309. The stage must operate deterministically
- **Rule Content Authority:** NONE — DS-309 supplies the boundary; this slot operationalizes it
- **Unresolved Operational Question:** How is the universe boundary operationally applied in the pipeline? What does the stage emit? What happens to assets outside the boundary?
- **Affected Artifact(s):** PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md; Universe Definition stage implementation
- **Decision Category:** Filter, Eligibility
- **Materiality:** Material — determines which assets proceed to subsequent stages
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** DS-309 boundary definition; asset inventory data
- **Required Output States:** A deterministic stage behavior contract: what the stage consumes, what it emits, and what happens to out-of-boundary assets
- **Required Explainability:** Which assets were included, excluded, and under what rule
- **Missing-Data Question:** What happens when boundary-determining data is missing for an asset?
- **Conflicting-Evidence Question:** How is an asset handled when data sources disagree on its boundary classification?
- **Point-in-Time Question:** At what evaluation timestamp is universe membership assessed? How are listing/delisting events handled?
- **Dependencies:** DS-309 (universe boundary definition); DS-310 (additional eligibility criteria); DS-512 (stage contracts)
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Universe Definition stage cannot execute
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-502 — Theme Context Stage Behavior

- **Identifier:** DS-502
- **Topic:** Pipeline-specific operational behavior of the Theme Context stage, referencing canonical DS-308 for the filter/enrichment/ranking classification
- **Decision Obligation Source:** ALPHA-MOMENTUM-V0-SPEC §4.2 defines Theme Context stage. DS-308 defines the classification. This slot addresses pipeline-specific operationalization
- **Inherited Approved Semantics:** The Theme Context stage exists. Its classification (filter/enrichment/ranking) is determined by DS-308. The V0 pipeline is a Theme-linked demonstration boundary per §4.4
- **Rule Content Authority:** NONE — DS-308 supplies the classification; this slot operationalizes it
- **Unresolved Operational Question:** Given the classification from DS-308, how does the Theme Context stage behave in the pipeline? What does it consume and emit? How does it handle Candidates with zero, one, or multiple Theme relationships?
- **Affected Artifact(s):** PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md; Theme Context stage implementation
- **Decision Category:** Filter, Rank
- **Materiality:** Material — determines how Theme context affects Candidate flow
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** DS-308 classification; Candidate–Theme relationship data; Approved Theme list
- **Required Output States:** A deterministic stage behavior contract specifying what happens to Candidates with zero, one, or multiple Theme relationships
- **Required Explainability:** Which Candidates were included/excluded/enriched by Theme context, under what rules
- **Missing-Data Question:** What happens when Candidate–Theme relationship data is absent?
- **Conflicting-Evidence Question:** How is a Candidate with relationships to multiple Themes handled when Themes have different quality profiles?
- **Point-in-Time Question:** At what evaluation timestamp are Candidate–Theme relationships evaluated?
- **Dependencies:** DS-308 (Theme Context classification); DS-512 (stage contracts)
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Theme Context stage cannot function; AC-5 cannot be verified
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-503 — Candidate Quality Assessment — Gate/Rank/Enrichment Effects

- **Identifier:** DS-503
- **Topic:** Whether Candidate Quality output (as defined by DS-304 in RULE-PACK-AND-QUALITY-CONTRACTS.md) acts as a gate, ranking input, enrichment label, or combination in the pipeline flow
- **Decision Obligation Source:** ALPHA-MOMENTUM-V0-SPEC §4.2 defines Candidate Quality Assessment stage. DOMAIN-ARCHITECTURE §1.2 assigns Alpha Momentum ownership of prioritization and ranking
- **Inherited Approved Semantics:** The Candidate Quality Assessment stage exists. Its output format is determined by DS-304. This slot decides how the pipeline uses that output
- **Rule Content Authority:** NONE
- **Unresolved Operational Question:** Does Candidate Quality output act as a gate, ranking input, enrichment label, or combination in the pipeline flow?
- **Affected Artifact(s):** PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md; Candidate Quality Assessment stage implementation
- **Decision Category:** Filter, Rank
- **Materiality:** Material — determines whether Candidate Quality gates Candidates out or merely contributes to ordering
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** DS-304 output policy; Candidate Quality assessment outputs
- **Required Output States:** A deterministic stage-effects specification
- **Required Explainability:** How Candidate Quality affected each Candidate's pipeline trajectory
- **Missing-Data Question:** What happens when Candidate Quality cannot be assessed for a Candidate?
- **Conflicting-Evidence Question:** How does the stage handle a Candidate with mixed sub-dimension results?
- **Point-in-Time Question:** At what evaluation timestamp is Candidate Quality assessed?
- **Dependencies:** DS-304 (Candidate Quality output policy); DS-301 (domain selection)
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Candidate Quality stage output format is undefined
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-504 — Entry Readiness Assessment — Gate/Rank/Enrichment Effects

- **Identifier:** DS-504
- **Topic:** Whether Entry Readiness output (as defined by DS-305) acts as a gate, ranking input, enrichment label, or combination in the pipeline flow
- **Decision Obligation Source:** ALPHA-MOMENTUM-V0-SPEC §4.2 defines Entry Readiness Assessment stage. DOMAIN-ARCHITECTURE §1.2 assigns Alpha Momentum ownership
- **Inherited Approved Semantics:** The Entry Readiness Assessment stage exists. Its output format is determined by DS-305
- **Rule Content Authority:** NONE
- **Unresolved Operational Question:** Does Entry Readiness output act as a gate, ranking input, enrichment label, or combination?
- **Affected Artifact(s):** PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md; Entry Readiness Assessment stage implementation
- **Decision Category:** Filter, Rank
- **Materiality:** Material
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** DS-305 output policy; Entry Readiness assessment outputs
- **Required Output States:** A deterministic stage-effects specification
- **Required Explainability:** How Entry Readiness affected each Candidate's pipeline trajectory
- **Missing-Data Question:** What happens when Entry Readiness cannot be assessed?
- **Conflicting-Evidence Question:** How does the stage handle conflicting sub-dimension signals?
- **Point-in-Time Question:** At what evaluation timestamp?
- **Dependencies:** DS-305 (Entry Readiness output policy); DS-302 (domain selection)
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Entry Readiness stage output format is undefined
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-505 — Data Confidence Assessment — Gate/Warning Effects

- **Identifier:** DS-505
- **Topic:** Whether Data Confidence output (as defined by DS-412 in DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md) acts as a gate, advisory warning, enrichment, or purely informational in the Alpha Momentum pipeline
- **Decision Obligation Source:** ALPHA-MOMENTUM-V0-SPEC §4.2 defines Data Confidence Assessment stage with Shared Core ownership. Alpha Momentum decides how the pipeline uses the output
- **Inherited Approved Semantics:** The Data Confidence Assessment stage exists. Shared Core owns the assessment. Alpha Momentum decides how the pipeline uses it
- **Rule Content Authority:** NONE
- **Unresolved Operational Question:** Does Data Confidence output act as a gate, advisory warning, enrichment, or purely informational in the pipeline flow?
- **Affected Artifact(s):** PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md; Data Confidence Assessment stage pipeline behavior
- **Decision Category:** Filter, Rank
- **Materiality:** Material — determines whether low Data Confidence excludes Candidates or merely informs
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** DS-412 output format; Data Confidence assessment outputs
- **Required Output States:** A deterministic stage-effects specification
- **Required Explainability:** How Data Confidence affected each Candidate's pipeline trajectory
- **Missing-Data Question:** What happens when Data Confidence cannot be assessed?
- **Conflicting-Evidence Question:** How does the stage interact with conflict preservation rules?
- **Point-in-Time Question:** At what evaluation timestamp?
- **Dependencies:** DS-412 (Data Confidence scope levels and roll-up policy); all Data Confidence dimension slots
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Data Confidence stage behavior is undefined
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-506 — Theme-First Queue Assembly

- **Identifier:** DS-506
- **Topic:** Structural rules for assembling the queue by Theme first, then Candidates; what the stage produces and how prior stage outputs are consumed
- **Decision Obligation Source:** ALPHA-MOMENTUM-V0-SPEC §4.2: "Order by Theme, then by strategy-owned prioritization within each Theme." Constitution §14: Theme-first. CANDIDATE-AND-QUEUE-MODEL §4.1: Theme-first structure
- **Inherited Approved Semantics:** Queue is Theme-first. Within-Theme ordering is strategy-owned. The structural assembly rules (how Themes are grouped, how Candidates are placed) are not fully supplied. The V0 pipeline is a Theme-linked demonstration boundary per §4.4
- **Rule Content Authority:** ALPHA-MOMENTUM-V0-SPEC §4.2 — for the structural rule: "Order by Theme, then by strategy-owned prioritization within each Theme"
- **Unresolved Operational Question:** How is the queue assembled? What does the stage consume from prior stages? What does it emit? How are Themes grouped when a Candidate relates to multiple Themes?
- **Affected Artifact(s):** PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md; Research Queue Assembly stage implementation
- **Decision Category:** Rank
- **Materiality:** Material — determines the structure of the final queue output
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** Outputs from all prior pipeline stages; Candidate–Theme relationship data
- **Required Output States:** A deterministic queue assembly contract; Theme-first grouping; stage output specification
- **Required Explainability:** Why each Theme is positioned where it is, why each Candidate is within its Theme
- **Missing-Data Question:** What happens when a Candidate has Theme Quality data but no Candidate Quality or Entry Readiness data?
- **Conflicting-Evidence Question:** How does the queue handle a Candidate linked to multiple Themes?
- **Point-in-Time Question:** At what evaluation timestamp is the queue assembled?
- **Dependencies:** DS-307 (Strategy-Relevance Policy); DS-308 (Theme Context classification); DS-503–DS-505 (stage effects)
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Research Queue cannot be assembled; AC-5 cannot be verified
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-507 — V0 Prioritization Output Form

- **Identifier:** DS-507
- **Topic:** Whether V0 requires ordered, tiered/grouped, unordered, or no Theme/Candidate prioritization output. This is the parent decision; within-Theme ordering, Theme-level ordering, and tie behavior are conditional and become active only when an ordering-dependent form is selected
- **Decision Obligation Source:** Constitution §14: Research Queue is Theme-first. No prioritization output form is mandated. DESIGN-PLAN.md §6: Gate A must not decide queue ordering
- **Inherited Approved Semantics:** The queue exists and is Theme-first. The output form (ordered, tiered, unordered, none) is not specified
- **Rule Content Authority:** NONE
- **Unresolved Operational Question:** Does V0 require a prioritization output? If so, what form — ordered list, tiered groups, unordered set, other?
- **Affected Artifact(s):** PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md; Research Queue Assembly output; conditional ordering templates
- **Decision Category:** Rank
- **Materiality:** Material — determines whether and how the queue communicates priority to the Founder
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** V0 scope and objectives; Founder review workflow expectations
- **Required Output States:** A deterministic output form selection; if "ordered" is selected, child templates TPL-PIPELINE-WITHIN-THEME-ORDERING, TPL-PIPELINE-THEME-LEVEL-ORDERING, and TPL-PIPELINE-TIE-BEHAVIOR become active; if "unordered," "tiered," or "none" is selected, those templates remain inactive
- **Required Explainability:** The selected output form and its rationale
- **Missing-Data Question:** Not applicable at form-selection level
- **Conflicting-Evidence Question:** Not applicable
- **Point-in-Time Question:** Not applicable at form-selection level
- **Dependencies:** DS-506 (Queue Assembly)
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Queue output form is undefined; downstream consumers cannot interpret queue structure
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-508 — Adaptive-Capacity Decision Policy

- **Identifier:** DS-508
- **Topic:** The decision policy governing how many Candidates appear in the queue: quality-driven inclusion rules, no fixed quota, and valid empty-queue outcome. The decision policy may or may not use thresholds — "policy" does not presume "thresholds"
- **Decision Obligation Source:** Constitution §14: "Queue capacity is adaptive. It must not fill a quota with weak candidates. It may return zero high-priority candidates." Founder's Decision #9. CANDIDATE-AND-QUEUE-MODEL §4.2: "Capacity is determined by the number of candidates that meet the strategy's quality thresholds, not by a target count"
- **Inherited Approved Semantics:** Queue capacity is adaptive. It must not fill a quota. It may return zero Candidates. Capacity is quality-driven, not target-driven. The phrase "quality thresholds" in CANDIDATE-AND-QUEUE-MODEL §4.2 describes the conceptual principle — it does not mandate numeric thresholds as the implementation method
- **Rule Content Authority:** Constitution §14 + Founder's Decision #9 + CANDIDATE-AND-QUEUE-MODEL §4.2 — for the principles: adaptive, no quota, quality-driven, zero-allowed
- **Unresolved Operational Question:** What is the decision policy for inclusion? How is the quality bar expressed? How does the queue scale with Candidate quality? Is "zero" a valid operational output with defined behavior?
- **Affected Artifact(s):** PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md; Research Queue Assembly; Research Queue output
- **Decision Category:** Threshold, Filter
- **Materiality:** Material — determines which Candidates appear in the queue and how many
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** Candidate assessments from all prior pipeline stages; quality dimension outputs
- **Required Output States:** A deterministic inclusion policy; guaranteed ability to return zero Candidates; no fixed quota; the policy may express inclusion criteria without using numeric thresholds
- **Required Explainability:** Inclusion policy, which Candidates met or did not meet it, why the queue contains N Candidates
- **Missing-Data Question:** What happens when inclusion depends on a dimension that cannot be assessed?
- **Conflicting-Evidence Question:** How does the policy handle a Candidate that meets one dimension's bar but not another's?
- **Point-in-Time Question:** At what evaluation timestamp is the policy evaluated?
- **Dependencies:** DS-307 (Strategy-Relevance Policy); DS-503–DS-505 (stage effects)
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Queue capacity cannot adapt; AC-5 cannot be verified
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-509 — Queue Empty-State Operational Contract

- **Identifier:** DS-509
- **Topic:** Gate A operational contract for the empty-queue state: zero Candidates is a valid output; operational output state and required reason/audit categories; lineage to the rules and inputs producing the empty state; downstream contract behavior
- **Decision Obligation Source:** Constitution §14: may return zero. CANDIDATE-AND-QUEUE-MODEL §4.2: "Zero high-priority candidates (DNA-016: Honest Empty States)"
- **Inherited Approved Semantics:** The queue may return zero Candidates. The system must not fabricate Candidates. Gate A scope is limited to operational contract: output state, reason/audit categories, lineage, and downstream behavior. Human-facing presentation (UI wording, page layout, visual prominence, near-miss display, display order) belongs to Gate C (no identifier assigned)
- **Rule Content Authority:** NONE — the principle is approved; the operational contract is not
- **Unresolved Operational Question:** What is the operational output state when the queue is empty? What reason/audit categories are required? What lineage links the empty state to the rules and inputs that produced it? What downstream contracts govern empty-state propagation?
- **Affected Artifact(s):** PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md; Research Queue Assembly; downstream consumers of queue output
- **Decision Category:** Fallback
- **Materiality:** Material — determines how the system communicates absence of opportunities
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** Queue assembly output (empty); pipeline stage outputs showing exclusion reasons
- **Required Output States:** A deterministic empty-state output contract; reason/audit categories; lineage references; downstream contract behavior; the system must not fabricate Candidates or lower standards automatically
- **Required Explainability:** Why the queue is empty, which rules/filters produced the empty state, lineage to inputs
- **Missing-Data Question:** Is an empty queue caused by missing data distinguishable from one caused by quality failures?
- **Conflicting-Evidence Question:** Not directly applicable
- **Point-in-Time Question:** Does the empty-state output carry the evaluation timestamp?
- **Dependencies:** DS-508 (Adaptive-Capacity Policy); DS-506 (Queue Assembly); DS-510 (Explainability and Audit Contract)
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Empty queue may appear as system error; AC-5 cannot be verified with proper operational behavior
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-510 — Explainability, Audit, and Rule-Result Lineage Contract

- **Identifier:** DS-510
- **Topic:** Logical minimum content required for deterministic explanation, audit, rule-result lineage, rule version linkage, input and evidence references, evaluation timestamp, and reproducibility. Gate A owns the logical minimum content; Gate C owns human-facing presentation, layout, wording, visual hierarchy, and display ordering (no Gate C identifier assigned)
- **Decision Obligation Source:** ALPHA-MOMENTUM-V0-SPEC §5.2: "human-readable explanations for prioritization." §5.3: evidence lineage traceability. §5.4: historical state queryability. Constitution §19: explainability, reproducibility. DOMAIN-ARCHITECTURE §5: audit trail for material transitions
- **Inherited Approved Semantics:** The queue must provide human-readable explanations. Evidence lineage must be traceable. Historical state must be queryable. Audit infrastructure exists. Reproducibility is required. The logical minimum content for these requirements is not supplied. Human-facing presentation belongs to Gate C
- **Rule Content Authority:** NONE — the requirements exist but the contract content is not supplied
- **Unresolved Operational Question:** What is the logical minimum content for each queue position explanation? What must the audit output contain per pipeline run? What metadata must accompany every rule output to establish deterministic lineage?
- **Affected Artifact(s):** PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md; All pipeline stages; Audit infrastructure
- **Decision Category:** Other (Explainability, Audit)
- **Materiality:** Material — determines whether pipeline outputs are independently verifiable
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** Pipeline run metadata; stage inputs and outputs; rule versions; evidence references
- **Required Output States:** A deterministic explainability and audit contract specifying what must be recorded, at what level, for each pipeline run and each queue position; rule-result lineage requirements linking every output to rule version, inputs, and evaluation timestamp
- **Required Explainability:** This slot defines explainability requirements — the output must enable tracing any queue decision back to the rule, inputs, and evidence
- **Missing-Data Question:** What audit record is produced when a stage cannot execute due to missing data?
- **Conflicting-Evidence Question:** Does the audit output distinguish between conflicting data and absent data?
- **Point-in-Time Question:** The audit output must record the evaluation timestamp and all point-in-time data references used
- **Dependencies:** DS-513 (Rule Lifecycle Contract — for rule version linkage); all pipeline stage slots
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Pipeline runs cannot be audited; AC-1, AC-7 cannot be verified
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-511 — Stock-First Discovery Path Preservation

- **Identifier:** DS-511
- **Topic:** Design constraints the V0 pipeline must satisfy to avoid precluding future stock-first discovery (screening Candidates independent of Theme membership), per §4.4
- **Decision Obligation Source:** ALPHA-MOMENTUM-V0-SPEC §4.4: "Future Alpha Momentum versions must preserve the ability to: discover candidates through stock-first screening independent of Theme membership; enrich stock-first candidates with Theme context after discovery; combine Theme-linked and stock-first discovery paths"
- **Inherited Approved Semantics:** Future versions must preserve stock-first discovery capability. V0 is a Theme-linked demonstration boundary, not the permanent architecture. This requirement is explicit approved rule content
- **Rule Content Authority:** ALPHA-MOMENTUM-V0-SPEC §4.4 — for the requirement to preserve future stock-first capability
- **Unresolved Operational Question:** What specific design constraints must the V0 pipeline satisfy now to avoid closing off the stock-first path?
- **Affected Artifact(s):** PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md; Alpha Momentum pipeline architecture; future V1+ pipeline design
- **Decision Category:** Other (Architecture Constraint)
- **Materiality:** Material — determines whether V0 design closes off required future capability
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** Current V0 pipeline stage design; DS-308 (Theme Context classification); understanding of stock-first screening requirements
- **Required Output States:** A set of design constraints the V0 pipeline must satisfy; these are architectural constraints, not investment rules
- **Required Explainability:** How each V0 pipeline decision preserves or constrains the stock-first path
- **Missing-Data Question:** Not directly applicable
- **Conflicting-Evidence Question:** Not directly applicable
- **Point-in-Time Question:** The stock-first path must also support point-in-time evaluation
- **Dependencies:** DS-502 (Theme Context stage behavior); DS-308 (Theme Context classification)
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** V0 pipeline architecture may hard-code Theme-linked-only discovery; §4.4 requirement cannot be verified as preserved
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-512 — Logical Stage Dependencies and Input/Output Contracts

- **Identifier:** DS-512
- **Topic:** What each pipeline stage requires and produces; logical dependencies between stages; deterministic evaluation requirements; how missing or empty inputs propagate. Covers what were previously separate stage contract (DS-217), intermediate empty-state (DS-216), and execution concerns
- **Decision Obligation Source:** ALPHA-MOMENTUM-V0-SPEC §4.1 defines stages and their logical sequence. DESIGN-PLAN.md §7 identifies stage contracts as material. Physical execution parallelism is deferred to architecture/implementation planning
- **Inherited Approved Semantics:** The six pipeline stages exist in a defined logical sequence. Each has a described purpose. Deterministic execution is required. This slot addresses logical dependencies and deterministic evaluation requirements, not physical runtime scheduling
- **Rule Content Authority:** NONE
- **Unresolved Operational Question:** What are the exact input and output contracts per stage? What are the logical dependencies? How are missing or empty inputs handled and propagated?
- **Affected Artifact(s):** PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md; All pipeline stage implementations
- **Decision Category:** Other (Data Contract)
- **Materiality:** Material — determines what data flows between stages
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** Resolved stage classification decisions; quality dimension output specifications
- **Required Output States:** A deterministic input/output contract per stage; logical dependency specification; empty/missing input propagation rules
- **Required Explainability:** The contract itself must be documented for auditability
- **Missing-Data Question:** How is missing data represented in stage output — explicit markers or omission? How do downstream stages handle it?
- **Conflicting-Evidence Question:** How does the contract distinguish assessed-but-conflicting from not-assessed?
- **Point-in-Time Question:** Does each stage output carry the evaluation timestamp and provenance references?
- **Dependencies:** DS-501–DS-506 (stage-specific operational decisions); RULE-PACK and DATA-CONFIDENCE output specifications
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Pipeline stages cannot be connected; stages cannot know what to expect or produce
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-513 — Rule Lifecycle, Version, Authority, and Effective-Date Contract

- **Identifier:** DS-513
- **Topic:** Canonical cross-cutting contract for rule lifecycle, versioning, authority, and effective-date semantics. Canonical owner: Pipeline artifact. All other Gate A artifacts reference this slot rather than creating duplicate lifecycle/version decisions
- **Decision Obligation Source:** DESIGN-PLAN.md §8 requires stable artifacts with versioned amendment processes. DESIGN-PLAN.md §11 requires every rule to trace to its Rule Content Authority. DOMAIN-ARCHITECTURE §5 requires versioning for material transformations. No operational rule-lifecycle contract is supplied
- **Inherited Approved Semantics:** Material rules must be versioned. Amendments require named approvals. Rule authority must be traceable. The operational contract for rule identifiers, version semantics, effective dates, supersession, retirement, and evaluation-time rule-version selection is not supplied
- **Rule Content Authority:** NONE
- **Unresolved Operational Question:** What is the operational contract for: stable rule identifiers; version semantics; authority and approval reference recording; effective-from status and date semantics; supersession relationships; retirement/deactivation semantics; evaluation-time rule-version selection; linkage to deterministic rule-result lineage (DS-510)?
- **Affected Artifact(s):** PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md (canonical owner); referenced by all Gate A artifacts; all rule outputs
- **Decision Category:** Other (Governance Contract)
- **Materiality:** Material — determines whether rules have deterministic version identity and traceable authority
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** Existing versioning requirements from DESIGN-PLAN.md and DOMAIN-ARCHITECTURE; rule-authority hierarchy
- **Required Output States:** A deterministic rule-lifecycle contract; no selected format, numbering convention, date rule, or transition behavior is proposed
- **Required Explainability:** For any rule output: rule identifier, version, authority reference, effective status, and the contract version
- **Missing-Data Question:** What happens when a rule output references a rule version that has been retired?
- **Conflicting-Evidence Question:** How is a conflict between two active rule versions resolved?
- **Point-in-Time Question:** How does the evaluation-time rule-version selection work — which version of a rule governs a pipeline run at a given evaluation timestamp?
- **Dependencies:** DS-510 (Explainability, Audit, and Rule-Result Lineage — for lineage linkage)
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Rules lack deterministic identity and version traceability; AC-7 (reproducibility) cannot be fully verified
- **Approval Reference:**
- **Verification Evidence:** pending

---

## 3. Conditional Templates

Templates are not active decisions. They carry TPL- identifiers and are instantiated with unique DS identifiers only when DS-507 selects an ordering-dependent output form.

### Template: TPL-PIPELINE-WITHIN-THEME-ORDERING — Within-Theme Candidate Ordering Policy

- **Template ID:** TPL-PIPELINE-WITHIN-THEME-ORDERING
- **Purpose:** Conditional contract for within-Theme Candidate ordering. Instantiated with a unique DS identifier through later named authorization only if DS-507 selects an ordering-dependent output form
- **Required fields per instantiation:** Ordering policy (what dimensions inform ordering, without proposing concrete sort keys); tie-behavior reference; explainability requirements
- **Status:** Template — not an active decision

### Template: TPL-PIPELINE-THEME-LEVEL-ORDERING — Theme-Level Ordering Policy

- **Template ID:** TPL-PIPELINE-THEME-LEVEL-ORDERING
- **Purpose:** Conditional contract for Theme-level ordering. Instantiated only if DS-507 selects an ordering-dependent output form requiring Theme ordering
- **Required fields per instantiation:** Ordering policy (what dimensions inform Theme ordering); tie-behavior reference
- **Status:** Template — not an active decision

### Template: TPL-PIPELINE-TIE-BEHAVIOR — Tie Behavior Policy

- **Template ID:** TPL-PIPELINE-TIE-BEHAVIOR
- **Purpose:** Conditional contract for tie behavior. Instantiated only if DS-507 selects an ordering form that creates tie cases
- **Required fields per instantiation:** Tie resolution policy (without proposing concrete tie-breaker rules); fallback behavior when all resolution methods are exhausted
- **Status:** Template — not an active decision

---

## 4. Inherited Controls

### Higher-Authority Escalation

- **Source:** DESIGN-PLAN.md §13; AGENTS.md authority hierarchy
- **Rule:** Same as documented in RULE-PACK-AND-QUALITY-CONTRACTS.md §4. Applicable to any pipeline decision that would change or narrow higher authority
- **Status:** Inherited approved governance control

### Contradiction Visibility (Presentation Layer)

- **Source:** EVIDENCE-MODEL §7
- **Rule:** Contradictions must remain visible. Human-facing presentation belongs to Gate C
- **Status:** Inherited approved rule

---

## 5. Deferred and Future-Gate Topics

### Deferred Beyond Gate A

| Topic | Old ID | Rationale |
|---|---|---|
| Stage Execution Order and Parallelism | DS-215 (old) | Physical execution parallelism is a runtime scheduling concern. Deferred to architecture/implementation planning after Gate D. Gate A addresses logical dependencies and deterministic evaluation requirements only (DS-512) |

### Moved to Future Gate C (No Identifier Assigned)

| Topic | Old ID | Rationale |
|---|---|---|
| Theme Card and Research Queue Relationship | DS-218 (old) | Presentation/human-review-flow decision. Natural owner is Gate C artifact THEME-CARD-AND-HUMAN-REVIEW-FLOW.md per DESIGN-PLAN.md §4. No Gate C identifier assigned — requires separate Gate C drafting authorization |
| Human-Facing Empty-State Presentation | — (split from old DS-208) | UI wording, page layout, visual prominence, near-miss display, display order. Gate A operational contract (DS-509) covers output state, reason categories, lineage, and downstream behavior. Presentation belongs to Gate C |
| Human-Facing Contradiction Visibility and Display | — (split from old DS-113) | Gate A data-layer detection and preservation is DS-405. Human-facing display and presentation belongs to Gate C |

---

## 6. Slot Supersession Map

This artifact's v0.1-draft contained 18 decision slots (DS-201–DS-218). Full cross-artifact supersession details are in TRACEABILITY-AND-DECISION-REGISTER.md.

| Old ID | Disposition | Reference |
|---|---|---|
| DS-201 | Merged and superseded by | DS-501 (references DS-309 for boundary) |
| DS-202 | Merged into | DS-308 (canonical — in Rule-Pack artifact; this artifact references DS-308 via DS-502) |
| DS-203 | Superseded by | DS-503 |
| DS-204 | Superseded by | DS-504 |
| DS-205 | Superseded by | DS-505 |
| DS-206 | Superseded by | DS-506 |
| DS-207 | Superseded by | DS-508 |
| DS-208 | Superseded by | DS-509 (operational contract); human-facing presentation split to Gate C |
| DS-209 | Superseded by template | TPL-PIPELINE-WITHIN-THEME-ORDERING (conditional on DS-507) |
| DS-210 | Superseded by template | TPL-PIPELINE-THEME-LEVEL-ORDERING (conditional on DS-507) |
| DS-211 | Superseded by template | TPL-PIPELINE-TIE-BEHAVIOR (conditional on DS-507) |
| DS-212 | Merged into | DS-510 |
| DS-213 | Merged into | DS-510 |
| DS-214 | Superseded by | DS-511 |
| DS-215 | Deferred beyond Gate A | Architecture/implementation planning (no identifier) |
| DS-216 | Absorbed into | DS-512 (stage contracts handle empty-output propagation) |
| DS-217 | Absorbed into | DS-512 (merged into logical stage dependencies and contracts) |
| DS-218 | Moved to Gate C | No identifier assigned |

---

## 7. Verification Requirements

- All 13 active slots are Proposed, UNRESOLVED — FOUNDER DECISION REQUIRED
- No slot proposes prohibited content
- Every slot carries Decision Obligation Source, Inherited Approved Semantics, Rule Content Authority, and Unresolved Operational Question
- DS-509 limits scope to operational contract; human-facing presentation belongs to Gate C
- DS-510 separates logical explainability/audit content from Gate C presentation
- DS-513 is the only canonical Rule Lifecycle/Version/Authority/Effective-Date decision
- No DS identifiers reused from old range
- No Gate C identifiers assigned
- Templates are conditional on DS-507 and carry TPL- identifiers
