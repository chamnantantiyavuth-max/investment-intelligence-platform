# Rule Pack and Quality Contracts

Status: Accepted Gate A Decision-Slot Artifact
Version: 0.1
Owner: Founder
Authority: Structurally approved Gate A decision-slot artifact; individual decision-slot content gains authority only through its own named Founder approval
Derived from: Constitution v0.3, Project Definition v0.1, and Approved Stable Design Plan v0.1
Drafting Authorization: AM-V0-GATE-A-DRAFTING-v0.1
Structural Acceptance: AM-V0-GATE-A-STRUCTURAL-ACCEPTANCE-v0.1
Supersedes: v0.1-draft (DS-001–DS-028, RC-001 — see Slot Supersession Map §6)

---

## 1. Inherited Approved Semantics

This section faithfully restates approved semantics that govern Candidate Quality, Theme Quality, Entry Readiness, and Alpha Momentum strategy-owned feature and rule semantics. No expansion or reinterpretation is intended.

### 1.1 Constitution v0.3

- **§10 Information Preservation:** The platform must keep Theme Quality, Candidate Quality, Entry Readiness, and Data Confidence separate. Important trade-offs must not disappear into one opaque score.
- **§13 Alpha Momentum:** Alpha Momentum separates Candidate Quality (fundamentals, growth, liquidity, relative strength, trend quality, accumulation, industry leadership, and other approved rule-pack dimensions), Theme Quality (lifecycle, breadth, leadership, evidence progression, market confirmation, fundamental confirmation, crowding, and confidence), Entry Readiness (price structure, base quality, breakout proximity, volume behavior, volatility contraction, and extension risk), and Data Confidence (freshness, completeness, reliability, conflicts, and missing data).
- **§13 Alpha Momentum — Candidate classification within a Theme:** Confirmed Leader, Emerging Challenger, Direct Beneficiary, Enabler, Bottleneck Owner, Second-order Beneficiary, Watchlist Member, Former Leader, Deteriorating Member.

### 1.2 Candidate and Queue Model (Approved Domain Specification v0.1)

- **§2.1 Candidate Quality:** Measures the quality of the company or asset itself, independent of entry timing. Domains: Fundamentals, Growth, Liquidity, Relative Strength, Trend Quality, Accumulation, Industry Leadership. Owned by Alpha Momentum strategy. Domains are deferred for finalization (OPEN-QUESTIONS.md).
- **§2.2 Theme Quality:** Measures the strength, health, and evidence backing of the Candidate's related Theme(s). Domains: Lifecycle stage, Breadth, Leadership, Evidence progression, Market confirmation, Fundamental confirmation, Crowding, Confidence. Owned by Shared Core (Theme Intelligence). Domains are deferred for finalization.
- **§2.3 Entry Readiness:** Measures whether the Candidate presents a favorable entry opportunity at this moment. Domains: Price structure, Base quality, Breakout proximity, Volume behavior, Volatility contraction, Extension risk. Owned by Alpha Momentum strategy. Domains are deferred for finalization.
- **§2.5 Separation Rule:** Four quality dimensions are presented separately. No weighted sum, composite score, or single ranking may silently absorb trade-offs. A Candidate may score well on Candidate Quality and poorly on Entry Readiness, or vice versa.
- **§3 Three Candidate Axes:** Theme Relationship Role, Leadership State, and Research State are three independent axes with distinct scope and cardinality — not one enum or global Candidate property.

### 1.3 Domain Architecture (Approved Domain Specification v0.1)

- **§1.2 Alpha Momentum Owns:** Eligibility, Filtering (whether and how Theme relationships act as filters, enrichment, or ranking inputs), Prioritization and ranking, Strategy relevance (how Candidate Quality, Entry Readiness, and Theme Quality are presented together in Alpha Momentum's context), Candidate Quality dimensions/weights/feature definitions/scoring, Entry Readiness dimensions/weights/feature definitions/scoring, Research Queue prioritization and ordering, Alpha Momentum-specific rule packs, Alpha Momentum-specific screening pipeline and stage definitions.
- **§1.2 Alpha Momentum Consumes from Shared Core:** Canonical Theme data, Evidence and source data, Entity and asset identity, Normalized data, Feature computation infrastructure, Audit infrastructure.
- **§6 What Does NOT Belong in Shared Core:** Strategy-specific scoring weights or thresholds, strategy-specific ranking or prioritization logic, strategy-specific rule packs, strategy-specific feature definitions, Entry Readiness models specific to Alpha Momentum, Candidate Quality dimensions specific to Alpha Momentum, strategy-specific eligibility/filtering/screening pipeline definitions.

### 1.4 Alpha Momentum V0 Specification (Approved Domain Specification v0.1)

- **§4.1–4.2 Pipeline Stages:** Universe Definition → Theme Context / Theme-linked Selection → Candidate Quality Assessment → Entry Readiness Assessment → Data Confidence Assessment → Research Queue Assembly. The Theme-linked pipeline demonstrated in V0 is a demonstration boundary, not the permanent Alpha Momentum pipeline architecture (§4.4).
- **§4.3 Deterministic Features:** All feature computations must be deterministic. Exact feature formulas, weights, and thresholds are deferred.
- **§4.4 Theme Context Boundary:** Future Alpha Momentum versions must preserve the ability to discover candidates through stock-first screening independent of Theme membership, enrich stock-first candidates with Theme context after discovery, and combine Theme-linked and stock-first discovery paths.

### 1.5 Theme Model (Approved Domain Specification v0.1)

- **§2 Lifecycle:** "no stage is inherently higher quality than another." Lifecycle is a separate axis from Approval Status, Monitoring Status, confidence, crowding, and evidence progression.
- **§8 Confidence:** Confidence is a separate axis. Exact measurement deferred.

### 1.6 Design Plan (Approved Stable Design Plan v0.1)

- **§7 Materiality Policy:** A decision is material if it changes or establishes domain definitions/invariants, strategy eligibility, filtering, ranking, queue behavior, thresholds, weights, formulas, evidence semantics, point-in-time behavior, missing-data behavior, human-review visibility, override semantics, or Shared Platform vs. strategy ownership.
- **§11 Rule-Authority Requirements:** Four permitted Rule Content Authorities: Founder-provided rule, existing approved Constitution or Domain Specification (only for exact rule content it explicitly specifies), approved external doctrine explicitly adopted by the Founder, explicitly approved V0 experiment assumption.

---

## 2. Active Unresolved Decision Slots

---

### Decision Slot: DS-301 — V0 Candidate Quality Domain Set

- **Identifier:** DS-301
- **Topic:** Which of the seven deferred Candidate Quality domains (Fundamentals, Growth, Liquidity, Relative Strength, Trend Quality, Accumulation, Industry Leadership) are selected for V0 scope, and in what grouping or priority
- **Decision Obligation Source:** Constitution §13 lists Candidate Quality domains. CANDIDATE-AND-QUEUE-MODEL §2.1 lists the same domains with "Domains are deferred for finalization (OPEN-QUESTIONS.md)." DOMAIN-ARCHITECTURE §1.2 assigns Alpha Momentum ownership of Candidate Quality dimensions
- **Inherited Approved Semantics:** The seven domains are a deferred menu from the approved specifications. No V0 domain set is approved. The Constitution requires Candidate Quality assessment; which sub-dimensions are included in V0 is a separate selection decision
- **Rule Content Authority:** NONE — the approved documents list domains but do not select which belong in V0 scope
- **Unresolved Operational Question:** Which of the seven Candidate Quality domains are selected for V0? Are any domains grouped, prioritized for later versions, or excluded from V0 scope?
- **Affected Artifact(s):** RULE-PACK-AND-QUALITY-CONTRACTS.md; Candidate Quality assessment output; conditional domain measurement templates
- **Decision Category:** Eligibility (domain scope)
- **Materiality:** Material — determines which aspects of Candidate Quality the V0 pipeline assesses
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** Domain list from approved specifications; V0 scope constraints; fixture data availability per domain
- **Required Output States:** An explicit V0 Candidate Quality domain set; domains not selected for V0 are deferred to later versions; each selected domain maps to a measurement contract instantiated from TPL-RP-CANDIDATE-DOMAIN
- **Required Explainability:** Which domains were selected, which were deferred, rationale, and the rule version
- **Missing-Data Question:** Not applicable at domain-selection level
- **Conflicting-Evidence Question:** Not applicable
- **Point-in-Time Question:** Not applicable at domain-selection level
- **Dependencies:** None blocking
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** No Candidate Quality domains are active; V0 cannot demonstrate Candidate Quality assessment; AC-3 cannot include Candidate Quality content
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-302 — V0 Entry Readiness Domain Set

- **Identifier:** DS-302
- **Topic:** Which of the six deferred Entry Readiness domains (Price Structure, Base Quality, Breakout Proximity, Volume Behavior, Volatility Contraction, Extension Risk) are selected for V0 scope
- **Decision Obligation Source:** Constitution §13 lists Entry Readiness domains. CANDIDATE-AND-QUEUE-MODEL §2.3 lists the same domains with "Domains are deferred for finalization." DOMAIN-ARCHITECTURE §1.2 assigns Alpha Momentum ownership of Entry Readiness dimensions
- **Inherited Approved Semantics:** The six domains are a deferred menu from the approved specifications. No V0 domain set is approved
- **Rule Content Authority:** NONE
- **Unresolved Operational Question:** Which of the six Entry Readiness domains are selected for V0?
- **Affected Artifact(s):** RULE-PACK-AND-QUALITY-CONTRACTS.md; Entry Readiness assessment output; conditional domain measurement templates
- **Decision Category:** Eligibility (domain scope)
- **Materiality:** Material — determines which aspects of Entry Readiness the V0 pipeline assesses
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** Domain list from approved specifications; V0 scope constraints; fixture data availability
- **Required Output States:** An explicit V0 Entry Readiness domain set; each selected domain maps to a measurement contract instantiated from TPL-RP-ENTRY-DOMAIN
- **Required Explainability:** Which domains were selected, which were deferred, rationale, and the rule version
- **Missing-Data Question:** Not applicable
- **Conflicting-Evidence Question:** Not applicable
- **Point-in-Time Question:** Not applicable
- **Dependencies:** None blocking
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** No Entry Readiness domains are active; V0 cannot demonstrate Entry Readiness assessment; AC-3 cannot include Entry Readiness content
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-303 — V0 Theme Quality Consumption Contract

- **Identifier:** DS-303
- **Topic:** Which already approved Shared-Core Theme Quality outputs Alpha Momentum consumes in V0; how Alpha Momentum presents and uses those outputs in strategy context; how lifecycle, Theme Confidence, crowding, and evidence progression remain separately visible; and preventing silent collapse of separate Theme axes
- **Decision Obligation Source:** Constitution §13 requires Alpha Momentum to assess Theme Quality. CANDIDATE-AND-QUEUE-MODEL §2.2 lists Theme Quality domains owned by Shared Core. DOMAIN-ARCHITECTURE §1.2: Alpha Momentum consumes canonical Theme data from Shared Core. THEME-MODEL §2: lifecycle is separate from quality ranking; "no stage is inherently higher quality than another." THEME-MODEL §8: confidence is a separate axis
- **Inherited Approved Semantics:** Shared Core owns Theme Quality definitions (DOMAIN-ARCHITECTURE §1.1). Alpha Momentum consumes Shared-Core outputs for strategy context (DOMAIN-ARCHITECTURE §1.2). Lifecycle, confidence, crowding, and evidence progression are separate axes within Theme Intelligence (THEME-MODEL §2, §8). No stage is inherently higher quality than another. This decision must not define Shared-Core Theme Quality dimensions, add or remove Theme Quality dimensions, define how lifecycle/confidence/crowding/evidence progression compose Theme Quality, or assign lifecycle an inherent quality value. If approved Shared-Core definitions are insufficient for Alpha Momentum consumption, UPSTREAM AMENDMENT REQUIRED — stop that decision path
- **Rule Content Authority:** NONE — Shared Core owns Theme Quality definitions. This slot governs Alpha Momentum consumption only
- **Unresolved Operational Question:** Which Shared-Core Theme Quality outputs does Alpha Momentum consume for V0? How does Alpha Momentum present and use those outputs in strategy context? How do lifecycle, Theme Confidence, crowding, and evidence progression remain separately visible without being silently collapsed?
- **Affected Artifact(s):** RULE-PACK-AND-QUALITY-CONTRACTS.md; Theme Card presentation (future Gate C); Alpha Momentum strategy output
- **Decision Category:** Eligibility (consumption scope)
- **Materiality:** Material — determines what Theme information informs Alpha Momentum's strategy context
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** Shared-Core Theme Quality output specification; separate-axes requirements from THEME-MODEL
- **Required Output States:** A consumption contract listing which Shared-Core outputs Alpha Momentum consumes; a method for presenting consumed outputs while keeping lifecycle, confidence, crowding, and evidence progression separately visible; the contract must not alter Shared-Core definitions
- **Required Explainability:** Which Theme Quality outputs are consumed, how they are presented, how separate axes remain visible, and the rule version
- **Missing-Data Question:** What happens when a consumed Shared-Core output is unavailable or not yet assessed for a Theme?
- **Conflicting-Evidence Question:** How does Alpha Momentum present a Theme whose separate axes point in different strategic directions?
- **Point-in-Time Question:** At what evaluation timestamp are consumed Theme Quality outputs assessed?
- **Dependencies:** Shared-Core Theme Quality output definitions; DS-306 (Theme Quality Output and Summary Policy)
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Alpha Momentum cannot reference Theme context in strategy output; AC-3 cannot include Theme Quality; UPSTREAM AMENDMENT REQUIRED if resolution attempts to define Shared-Core Theme Quality
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-304 — Candidate Quality Output and Summary Policy

- **Identifier:** DS-304
- **Topic:** How Candidate Quality sub-dimension results (for domains selected by DS-301) are presented and summarized; "no summary" is a valid outcome
- **Decision Obligation Source:** Constitution §10 requires keeping quality dimensions separate. CANDIDATE-AND-QUEUE-MODEL §2.5 prohibits a single ranking silently absorbing trade-offs. The exact presentation method for sub-dimensions within Candidate Quality is not supplied
- **Inherited Approved Semantics:** The four quality dimensions must remain separate and individually visible. Within Candidate Quality, sub-dimensions may be presented individually or summarized — but no opaque composite score may hide dimension-level trade-offs
- **Rule Content Authority:** NONE
- **Unresolved Operational Question:** How are Candidate Quality sub-dimension results presented — individually, summarized, grouped, or some combination? If summarized, by what policy that preserves visibility of individual dimensions?
- **Affected Artifact(s):** RULE-PACK-AND-QUALITY-CONTRACTS.md; Candidate Quality assessment output; Research Queue presentation
- **Decision Category:** Other (Output Policy)
- **Materiality:** Material — determines how Candidate Quality information reaches the Founder
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** DS-301 domain selection; per-domain measurement outputs; separation-rule constraints
- **Required Output States:** A deterministic output policy; "no summary — present all sub-dimensions individually" is a valid outcome; any summary method must preserve individual dimension visibility
- **Required Explainability:** Which dimensions contributed, their individual assessments, how they were summarized (if at all), and the rule version
- **Missing-Data Question:** What happens when one or more selected sub-dimensions cannot be assessed for a Candidate?
- **Conflicting-Evidence Question:** How does the output policy handle a Candidate with strong performance on some sub-dimensions and weak performance on others?
- **Point-in-Time Question:** At what evaluation timestamp are sub-dimension outputs aligned?
- **Dependencies:** DS-301 (domain selection)
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Candidate Quality output is undefined; downstream stages cannot consume Candidate Quality
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-305 — Entry Readiness Output and Summary Policy

- **Identifier:** DS-305
- **Topic:** How Entry Readiness sub-dimension results (for domains selected by DS-302) are presented and summarized
- **Decision Obligation Source:** Constitution §10; CANDIDATE-AND-QUEUE-MODEL §2.5 separation rule. The exact presentation method within Entry Readiness is not supplied
- **Inherited Approved Semantics:** Same separation constraint as DS-304, applied to Entry Readiness
- **Rule Content Authority:** NONE
- **Unresolved Operational Question:** How are Entry Readiness sub-dimension results presented?
- **Affected Artifact(s):** RULE-PACK-AND-QUALITY-CONTRACTS.md; Entry Readiness assessment output; Research Queue presentation
- **Decision Category:** Other (Output Policy)
- **Materiality:** Material
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** DS-302 domain selection; per-domain measurement outputs
- **Required Output States:** A deterministic output policy with the same validity of "no summary" as DS-304
- **Required Explainability:** Which dimensions contributed, their individual assessments, how summarized (if at all), and the rule version
- **Missing-Data Question:** What happens when one or more selected sub-dimensions cannot be assessed?
- **Conflicting-Evidence Question:** How does the output policy handle conflicting sub-dimension signals?
- **Point-in-Time Question:** At what evaluation timestamp?
- **Dependencies:** DS-302 (domain selection)
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Entry Readiness output is undefined
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-306 — Theme Quality Output and Summary Policy (Alpha Momentum Consumption)

- **Identifier:** DS-306
- **Topic:** How Theme Quality outputs consumed by Alpha Momentum (per DS-303) are presented and summarized in Alpha Momentum's strategy context; covers Alpha Momentum consumption presentation only, not canonical Shared-Core Theme Quality output design
- **Decision Obligation Source:** Constitution §10; CANDIDATE-AND-QUEUE-MODEL §2.5 separation rule. DOMAIN-ARCHITECTURE §1.2: Alpha Momentum owns strategy relevance presentation. Shared Core owns Theme Quality output design
- **Inherited Approved Semantics:** Shared Core defines canonical Theme Quality output. Alpha Momentum decides how to present consumed outputs in strategy context. This slot addresses Alpha Momentum's consumption presentation, not Shared-Core output design
- **Rule Content Authority:** NONE
- **Unresolved Operational Question:** How does Alpha Momentum present consumed Theme Quality outputs while preserving separate axes?
- **Affected Artifact(s):** RULE-PACK-AND-QUALITY-CONTRACTS.md; Alpha Momentum strategy output
- **Decision Category:** Other (Output Policy)
- **Materiality:** Material
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** DS-303 consumption contract; Shared-Core Theme Quality output specification
- **Required Output States:** A deterministic consumption-presentation policy for Alpha Momentum context; must not alter Shared-Core output design
- **Required Explainability:** Which Theme Quality outputs are shown, how they are presented, how separate axes remain visible, and the rule version
- **Missing-Data Question:** What happens when a consumed Shared-Core output is unavailable?
- **Conflicting-Evidence Question:** How are conflicting Theme Quality signals presented?
- **Point-in-Time Question:** At what evaluation timestamp?
- **Dependencies:** DS-303 (consumption contract); Shared-Core Theme Quality output definitions
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Theme Quality presentation in Alpha Momentum context is undefined
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-307 — Strategy-Relevance Policy While Preserving Separate Dimensions

- **Identifier:** DS-307
- **Topic:** How Candidate Quality, Entry Readiness, and Theme Quality are presented together in Alpha Momentum's context without collapsing into one opaque score
- **Decision Obligation Source:** DOMAIN-ARCHITECTURE §1.2: Alpha Momentum owns "Strategy relevance: how Candidate Quality, Entry Readiness, and Theme Quality combine in Alpha Momentum's context." Constitution §10: must keep them separate. CANDIDATE-AND-QUEUE-MODEL §2.5: no single ranking may silently absorb trade-offs
- **Inherited Approved Semantics:** The four quality dimensions (including Data Confidence) must remain separate, visible, and individually assessable. Alpha Momentum determines the strategic presentation relationship. No opaque composite score is permitted
- **Rule Content Authority:** NONE
- **Unresolved Operational Question:** How are the three strategy-relevant quality dimensions presented together in Alpha Momentum's context while preserving individual dimension visibility?
- **Affected Artifact(s):** RULE-PACK-AND-QUALITY-CONTRACTS.md; Research Queue prioritization; Alpha Momentum strategy output
- **Decision Category:** Other (Strategy Policy)
- **Materiality:** Material — determines the fundamental evaluation architecture for how Alpha Momentum presents Candidates
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** Candidate Quality outputs; Entry Readiness outputs; Theme Quality outputs; Data Confidence outputs
- **Required Output States:** A deterministic strategy-relevance policy; the policy must preserve individual dimension visibility; "present all dimensions independently with no synthesis" is a valid outcome
- **Required Explainability:** How each dimension is presented, their relationship in strategy context, and the rule version
- **Missing-Data Question:** What happens when one or more quality dimensions cannot be assessed for a Candidate?
- **Conflicting-Evidence Question:** How does the policy handle a Candidate with high Candidate Quality, high Theme Quality, but low Entry Readiness?
- **Point-in-Time Question:** Must all dimensions share the same evaluation timestamp?
- **Dependencies:** DS-304, DS-305, DS-306 (output policies for each quality dimension)
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Alpha Momentum cannot produce a coherent Candidate evaluation; AC-3 cannot be verified in strategy context
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-308 — Theme Context Operational Classification

- **Identifier:** DS-308
- **Topic:** Whether Candidate–Theme relationships in the Alpha Momentum pipeline act as a filter, enrichment, ranking input, or combination. This is the canonical decision; the Pipeline artifact references this identifier
- **Decision Obligation Source:** ALPHA-MOMENTUM-V0-SPEC §4.2: "Alpha Momentum decides whether they act as filter, enrichment, or ranking input." DOMAIN-ARCHITECTURE §1.2 assigns Filtering to Alpha Momentum
- **Inherited Approved Semantics:** Shared Core supplies Approved Theme relationships. Alpha Momentum decides their operational role. The V0 pipeline is a demonstration boundary per §4.4
- **Rule Content Authority:** NONE — the approved specs create the obligation to decide but do not supply the decision
- **Unresolved Operational Question:** Do Candidate–Theme relationships act as a filter, enrichment, ranking input, or combination in the Alpha Momentum pipeline?
- **Affected Artifact(s):** RULE-PACK-AND-QUALITY-CONTRACTS.md; PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md (references this slot); Alpha Momentum pipeline Theme Context stage
- **Decision Category:** Filter, Rank, Eligibility
- **Materiality:** Material — determines which Candidates enter the pipeline and how Theme context affects evaluation
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** Candidate–Theme relationship data; Approved Theme list; pipeline design constraints for stock-first path preservation
- **Required Output States:** A deterministic classification of how Theme relationships function in the pipeline; a clear rule for filter vs. enrichment vs. ranking input behavior
- **Required Explainability:** Which Candidates were included/excluded/enriched by Theme context, under what rule, and the rule version
- **Missing-Data Question:** What happens when Candidate–Theme relationship data is absent?
- **Conflicting-Evidence Question:** How is a Candidate handled with relationships to multiple Themes of differing quality?
- **Point-in-Time Question:** At what evaluation timestamp are Candidate–Theme relationships evaluated?
- **Dependencies:** DS-512 (Pipeline stage contracts — operationalizes this classification)
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Pipeline Theme Context stage cannot function; AC-5 cannot be verified
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-309 — Operational V0 Universe Boundary

- **Identifier:** DS-309
- **Topic:** Operational meaning of "US-listed common stock," ADR suitability definition, listing/de-listing point-in-time handling, duplicate listings and share classes, and public identifier requirements
- **Decision Obligation Source:** Constitution §13: "Alpha Momentum screens US-listed common stocks and suitable ADRs in V0." ALPHA-MOMENTUM-V0-SPEC §2.1: controlled subset via synthetic fixtures or approved historical snapshots
- **Inherited Approved Semantics:** The V0 universe is US-listed common stocks and suitable ADRs. V0 uses controlled fixtures. The Constitution does not supply specific exchange lists, ADR criteria, or operational boundary rules. This slot does not introduce price, liquidity, market-cap, float, or exchange filters — those require separate material eligibility decisions
- **Rule Content Authority:** NONE — the Constitution provides the broad universe definition but does not supply operational meaning
- **Unresolved Operational Question:** What exactly constitutes a "US-listed common stock"? What makes an ADR "suitable"? How are listing/delisting events handled at different evaluation dates? How are duplicate listings and multiple share classes handled? What public identifiers are required?
- **Affected Artifact(s):** RULE-PACK-AND-QUALITY-CONTRACTS.md; PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md (references this slot via DS-501); Universe Definition pipeline stage
- **Decision Category:** Eligibility
- **Materiality:** Material — determines the operational boundary of the V0 universe
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** Listing venue data; ADR classification data; corporate action data for listing/delisting events
- **Required Output States:** An operational definition of the V0 universe boundary; rules for handling edge cases (delistings, duplicate listings, share classes); the definition must not silently narrow the Constitutional universe
- **Required Explainability:** Which assets are included/excluded by the boundary definition, under what rules, and the rule version
- **Missing-Data Question:** What happens when listing venue or ADR classification data is missing?
- **Conflicting-Evidence Question:** How is an asset handled when data sources disagree on its listing status or classification?
- **Point-in-Time Question:** How are listing/delisting events handled at different evaluation dates?
- **Dependencies:** None blocking
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** The V0 universe cannot be operationally bounded; the Universe Definition stage cannot execute
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-310 — Additional Alpha Momentum Eligibility Criteria

- **Identifier:** DS-310
- **Topic:** Any eligibility rules beyond the Constitutional universe (US-listed common stocks and suitable ADRs), if any. Each additional criterion is a separate material decision
- **Decision Obligation Source:** DOMAIN-ARCHITECTURE §1.2 assigns Alpha Momentum ownership of Eligibility. Any criterion beyond the Constitutional universe is not approved and requires explicit Founder decision
- **Inherited Approved Semantics:** The Constitutional universe is the baseline. No additional eligibility rules are approved. This slot is the decision point for whether any additional criteria exist, not a proposal that they should
- **Rule Content Authority:** NONE
- **Unresolved Operational Question:** Are there additional eligibility criteria beyond US-listed common stocks and suitable ADRs? If so, what are they — each requiring its own material decision?
- **Affected Artifact(s):** RULE-PACK-AND-QUALITY-CONTRACTS.md; Alpha Momentum eligibility rules; Universe Definition pipeline stage
- **Decision Category:** Eligibility, Threshold, Filter
- **Materiality:** Material if any additional criterion is adopted; this slot itself is the decision of whether to adopt any
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** V0 scope constraints; fixture data characteristics; Founder preferences
- **Required Output States:** A determination of whether additional eligibility criteria exist for V0; if yes, each criterion is a separate material decision with its own identifier; if no, the Constitutional universe is the full eligibility set
- **Required Explainability:** Whether additional criteria were adopted, what they are, why, and the rule version
- **Missing-Data Question:** Not applicable at the decision-of-whether level
- **Conflicting-Evidence Question:** Not applicable
- **Point-in-Time Question:** Any adopted criteria must specify point-in-time behavior
- **Dependencies:** DS-309 (universe boundary)
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** It is unclear whether the Constitutional universe is the complete eligibility set or whether additional filters are expected
- **Approval Reference:**
- **Verification Evidence:** pending

---

## 3. Conditional Templates

Templates are not active decisions. They carry TPL- identifiers and are instantiated with unique DS identifiers only when a domain-selection or ordering-form decision triggers them.

### Template: TPL-RP-CANDIDATE-DOMAIN — Candidate Quality Domain Measurement Contract

- **Template ID:** TPL-RP-CANDIDATE-DOMAIN
- **Purpose:** Conditional measurement contract for each Candidate Quality domain selected by DS-301. Defines the required fields, measurement method, feature contract reference, and output format for a single domain
- **Instantiation trigger:** DS-301 includes the domain in V0 scope
- **Instantiation method:** A new unique DS identifier is created through a later named authorization
- **Required fields per instantiation:** Measurement method; feature definitions (instantiated from TPL-RP-FEATURE-CONTRACT); output type and format; missing-data behavior; conflicting-evidence behavior; point-in-time requirements; explainability contract
- **Status:** Template — not an active decision

### Template: TPL-RP-ENTRY-DOMAIN — Entry Readiness Domain Measurement Contract

- **Template ID:** TPL-RP-ENTRY-DOMAIN
- **Purpose:** Conditional measurement contract for each Entry Readiness domain selected by DS-302
- **Instantiation trigger:** DS-302 includes the domain in V0 scope
- **Instantiation method:** New unique DS identifier through later named authorization
- **Required fields per instantiation:** Same structure as TPL-RP-CANDIDATE-DOMAIN
- **Status:** Template — not an active decision

### Template: TPL-RP-THEME-CONSUMPTION — Theme Quality Consumption Contract (Per-Dimension)

- **Template ID:** TPL-RP-THEME-CONSUMPTION
- **Purpose:** Conditional consumption contract for each Theme Quality dimension consumed under DS-303. Defines how Alpha Momentum consumes and presents a single Shared-Core Theme Quality output
- **Instantiation trigger:** DS-303 identifies the dimension for Alpha Momentum consumption
- **Instantiation method:** New unique DS identifier through later named authorization
- **Required fields per instantiation:** Shared-Core output reference; consumption method; presentation method within Alpha Momentum context; how the dimension remains separately visible
- **Status:** Template — not an active decision

### Template: TPL-RP-FEATURE-CONTRACT — Feature Definition Contract

- **Template ID:** TPL-RP-FEATURE-CONTRACT
- **Purpose:** Feature definition contract template. Each selected V0 domain may instantiate feature-definition decisions with unique DS identifiers through later named authorizations. Replaces the former single catch-all "Alpha Momentum Feature Definitions" slot
- **Instantiation trigger:** A domain is selected and its measurement contract requires feature definitions
- **Required fields per instantiation:** Exact formula or computation specification; input data references; parameters; version; deterministic execution guarantee; output type; missing-input behavior; point-in-time input requirements; computation lineage metadata
- **Status:** Template — not an active decision

### Template: TPL-REFERENCE-COHORT — Reference Cohort Contract Template

- **Template ID:** TPL-REFERENCE-COHORT
- **Purpose:** Template for a Reference Cohort Contract. A real RC identifier is created only after an approved relative rule requires a cohort. No active cohort exists
- **Required fields when instantiated:** Cohort or universe definition; evaluation timestamp; public-availability cutoff; minimum valid sample size; tie behavior; missing-value behavior; universe-change behavior; survivorship treatment; revision or vintage behavior
- **Status:** Template — not an active decision. Replaces former RC-001 which was an active identifier without an approved relative rule

---

## 4. Inherited Controls

The following are inherited approved governance controls from higher-authority documents. They are not unresolved decision slots.

### Higher-Authority Escalation

- **Source:** DESIGN-PLAN.md §13; AGENTS.md authority hierarchy
- **Rule:** When a proposed design decision would change, narrow, contradict, or extend the Constitution, Founder's Decisions, or an Approved Domain Specification: stop that decision path and record UPSTREAM AMENDMENT REQUIRED. The change cannot be approved merely through Gate A, B, C, or D. It requires the applicable material-change and authority-amendment process first
- **Status:** Inherited approved governance control — not an unresolved slot

### Contradiction Visibility (Presentation Layer)

- **Source:** EVIDENCE-MODEL §7: "Contradicting evidence remains visible and is never averaged away for presentation simplicity." Constitution §10: keep dimensions separate
- **Rule:** Contradictions must remain visible in all presentations. No computation may silently compress, net, or erase contradictory evidence. This is approved rule content, not an unresolved slot. Human-facing contradiction presentation display belongs to Gate C (no identifier assigned)
- **Status:** Inherited approved rule — not an unresolved slot

---

## 5. Deferred and Future-Gate Topics

No topics deferred or moved to future gates from this artifact. All active slots (DS-301–DS-310) are Gate A.

---

## 6. Slot Supersession Map

This artifact's v0.1-draft contained 28 decision slots (DS-001–DS-028) and 1 reference cohort contract (RC-001). The following map records their dispositions in the normalized v0.2-draft. Full cross-artifact supersession details are in TRACEABILITY-AND-DECISION-REGISTER.md.

| Old ID | Disposition | Reference |
|---|---|---|
| DS-001 – DS-007 | Superseded by template | TPL-RP-CANDIDATE-DOMAIN (conditional on DS-301) |
| DS-008 | Superseded by | DS-303 (V0 Theme Quality Consumption Contract) |
| DS-009 – DS-015 | Superseded by template | TPL-RP-THEME-CONSUMPTION (conditional on DS-303) |
| DS-016 – DS-021 | Superseded by template | TPL-RP-ENTRY-DOMAIN (conditional on DS-302) |
| DS-022 | Superseded by | DS-304 (Candidate Quality Output and Summary Policy) |
| DS-023 | Superseded by | DS-305 (Entry Readiness Output and Summary Policy) |
| DS-024 | Superseded by | DS-306 (Theme Quality Output and Summary Policy) |
| DS-025 | Superseded by | DS-307 (Strategy-Relevance Policy While Preserving Separate Dimensions) |
| DS-026 | Merged into | DS-308 (Theme Context Operational Classification — canonical) |
| DS-027 | Split and superseded by | DS-309 + DS-310 (Universe Boundary + Additional Eligibility) |
| DS-028 | Superseded by template | TPL-RP-FEATURE-CONTRACT |
| RC-001 | Removed; replaced by template | TPL-REFERENCE-COHORT |

---

## 7. Verification Requirements

Per DESIGN-PLAN.md §15 and VERIFICATION-DOCTRINE.md, Gate A verification requires:

- All 10 active slots are Proposed, UNRESOLVED — FOUNDER DECISION REQUIRED
- No slot proposes an investment-rule answer, threshold, weight, formula, lookback, benchmark, taxonomy, cohort, ordering, tie-breaker, eligibility rule, aggregation, or fallback
- DS-303 limits scope to Alpha Momentum consumption; does not define Shared-Core Theme Quality
- Every slot carries Decision Obligation Source, Inherited Approved Semantics, Rule Content Authority, and Unresolved Operational Question
- Templates carry TPL- identifiers and are not counted as active decisions
- Old identifiers preserved in the Slot Supersession Map
- DR-003 remains Approved; DR-009 remains Proposed and unresolved
