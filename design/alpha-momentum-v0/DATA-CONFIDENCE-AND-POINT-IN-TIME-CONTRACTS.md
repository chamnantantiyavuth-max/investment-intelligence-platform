# Data Confidence and Point-in-Time Contracts

Status: Accepted Gate A Decision-Slot Artifact
Version: 0.1
Owner: Founder
Authority: Structurally approved Gate A decision-slot artifact; individual decision-slot content gains authority only through its own named Founder approval
Derived from: Constitution v0.3, Project Definition v0.1, and Approved Stable Design Plan v0.1
Drafting Authorization: AM-V0-GATE-A-DRAFTING-v0.1
Structural Acceptance: AM-V0-GATE-A-STRUCTURAL-ACCEPTANCE-v0.1
Supersedes: v0.1-draft (DS-101–DS-114 — see Slot Supersession Map §6)

---

## 1. Inherited Approved Semantics

This section faithfully restates approved semantics that govern Data Confidence, evidence provenance, point-in-time correctness, and related domain rules. No expansion or reinterpretation is intended.

### 1.1 Constitution v0.3

- **§8 Evidence Doctrine:** The system distinguishes raw source records, observed facts, claims, normalized facts, derived metrics, statistical signals, AI extractions, AI classifications, hypotheses, human judgments, approved decisions, outcomes, and lessons. Multiple links copied from one source are not independent evidence. Evidence relevance may decay. Raw evidence and history are not silently edited in place.
- **§8 Controlled Removal:** When removal is required, evidence content may be quarantined or deleted through a controlled process recording a tombstone, reason, authorizer, timestamp, affected lineage, and downstream reprocessing requirements.
- **§8 Three-Year Default:** Unsupported narrative or intention-based evidence that has no measurable action within three years is stale by default, unless a documented long-cycle exception and milestones are approved.
- **§10 Information Preservation:** The platform must keep Data Confidence separate from Theme Quality, Candidate Quality, and Entry Readiness.
- **§13 Alpha Momentum — Data Confidence:** Freshness, completeness, reliability, conflicts, and missing data.
- **§19 Architecture Principles:** Point-in-time correctness and reproducibility are architectural principles.

### 1.2 Evidence Model (Approved Domain Specification v0.1)

- **§2 Information and Record Type Taxonomy:** Evidence and Observation Records (§2.1) are distinct from Epistemic and Governance Records (§2.2). Only Evidence and Observation Records may serve as supporting or contradicting evidence. AI Extraction and AI Classification are explicit subtypes of Claim, not Observed Facts. Human review alone does not convert an AI-derived record into an Observed Fact.
- **§3 Source Independence:** Syndicated copies, republications, and aggregated feeds deriving from the same originating source do not count as independent confirmation. Source independence assessment requires originating source identification, derivation chain, and independence classification (independent, derived, syndicated, unknown).
- **§5 Provenance:** Every evidence record must carry: Source identifier, Ingestion timestamp, Publication/public-availability timestamp, Effective/as-of period, Observation timestamp, Originating URL or reference, Revision or vintage, Supersedes/superseded-by, Content hash or source version, Licensing/retention classification, Timezone, Extraction method, Extraction version, Raw record reference.
- **§5.1 Point-in-Time Evaluation:** Historical evaluation must use information that was publicly available at the evaluation timestamp, not the latest revised value. When a source issues a revision, the platform must preserve the original record, record the revision as a new record with supersedes/superseded-by linkage, ensure historical evaluations see only the original record (or both with provenance clarity), and not silently replace or backfill historical data.
- **§6 Aging and Staleness:** Evidence relevance may decay. The model must support freshness as a dimension of Data Confidence, aging signals, and explicit staleness markers.
- **§7 Contradicting Evidence:** Contradicting evidence remains visible and is never averaged away for presentation simplicity. The model must support linking contradicting evidence, preserving contradictions in displays, and preventing score compression.
- **§9 Data Confidence:** Data Confidence is a separate axis. Dimensions: Freshness, Completeness, Reliability, Conflicts, Missing data. Applies at multiple levels: individual evidence records, aggregated assessments, overall system state. Exact measurement is deferred.

### 1.3 Candidate and Queue Model (Approved Domain Specification v0.1)

- **§2.4 Data Confidence:** Measures the reliability and completeness of the data underlying the Candidate's assessments. Owned by Shared Core.
- **§2.5 Separation Rule:** Data Confidence is one of four separated quality dimensions.

### 1.4 Domain Architecture (Approved Domain Specification v0.1)

- **§1.1 Shared Core — Data Quality and Freshness:** Freshness monitoring, completeness checks, conflict detection, revision tracking.
- **§5 Cross-Cutting Concerns:** Point-in-time queries must be reproducible at a given point in time. Raw evidence is not silently edited in place.

### 1.5 Alpha Momentum V0 Specification (Approved Domain Specification v0.1)

- **§2.2 Universe Constraints:** V0 data must carry timestamps and be queryable at a given point in time.
- **§8.1–8.2 Fixture Requirements:** Fixtures must carry timestamps, include deliberate quality variation, and include deliberate contradictions.

### 1.6 Design Plan (Approved Stable Design Plan v0.1)

- **§11 Rule-Authority Requirements:** Four permitted Rule Content Authorities.

---

## 2. Active Unresolved Decision Slots

---

### Decision Slot: DS-401 — Freshness and Staleness

- **Identifier:** DS-401
- **Topic:** Operational freshness periods, aging signals, staleness markers, and decay semantics per evidence type; consolidation of what were previously separate freshness (DS-101) and staleness (DS-110) decisions
- **Decision Obligation Source:** Constitution §13: Freshness as Data Confidence dimension. Constitution §8: three-year default for unsupported narrative evidence. EVIDENCE-MODEL §6: relevance decay, aging signals, staleness markers. EVIDENCE-MODEL §9: Freshness dimension
- **Inherited Approved Semantics:** Freshness is a Data Confidence dimension. Evidence relevance may decay. Constitution §8 provides explicit rule content: unsupported narrative/intention-based evidence with no measurable action within three years is stale by default, unless a documented long-cycle exception and milestones are approved. For all other evidence types, no freshness periods or staleness rules are supplied
- **Rule Content Authority:** Constitution §8 — for the three-year default for unsupported narrative evidence only. For all other evidence types: NONE
- **Unresolved Operational Question:** What are the operational freshness periods and staleness rules for each non-narrative evidence type? How does the constitutional three-year default interact with other staleness rules? What constitutes an aging signal vs. a staleness marker?
- **Affected Artifact(s):** DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md; Data Confidence assessment output; Evidence records
- **Decision Category:** Period, Threshold
- **Materiality:** Material — determines whether evidence is treated as current or stale
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** Evidence records with timestamps; evidence type classification; evaluation timestamps
- **Required Output States:** A deterministic freshness and staleness classification per evidence type and per record; explicit staleness markers that do not delete records; the constitutional three-year default applied to narrative evidence
- **Required Explainability:** Evidence age, freshness classification, staleness classification, applicable rule, and the rule version
- **Missing-Data Question:** What happens when an evidence record lacks the timestamps needed for freshness/staleness assessment?
- **Conflicting-Evidence Question:** How is staleness assessed when different staleness rules could apply to the same record?
- **Point-in-Time Question:** Freshness and staleness are relative to the evaluation timestamp — at what date are they assessed?
- **Dependencies:** DS-412 (roll-up policy); DS-410 (revision handling — revisions affect freshness of originals)
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Stale evidence may be treated as current; AC-3 cannot include meaningful freshness
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-402 — Completeness and Expected-Data Contract

- **Identifier:** DS-402
- **Topic:** What fields, periods, or entities are expected per evidence type; how completeness is measured; and the operational expected-data contract
- **Decision Obligation Source:** Constitution §13: Completeness. EVIDENCE-MODEL §9: Completeness as Data Confidence dimension
- **Inherited Approved Semantics:** Completeness is a Data Confidence dimension. What constitutes "expected" data is not supplied
- **Rule Content Authority:** NONE
- **Unresolved Operational Question:** What data is expected per evidence type? How is completeness measured when expectations vary by evidence type, by time period, or by entity?
- **Affected Artifact(s):** DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md; Data Confidence assessment output; Evidence records
- **Decision Category:** Threshold, Formula
- **Materiality:** Material — determines whether incomplete data triggers reduced Data Confidence
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** Evidence record schema definitions; expected-field specifications per evidence type; evidence record data
- **Required Output States:** A deterministic completeness assessment per evidence record; identification of missing expected fields; an expected-data contract per evidence type
- **Required Explainability:** Expected fields, present fields, missing fields, completeness classification, and the rule version
- **Missing-Data Question:** This dimension is about missing data — what is the meta-behavior when the expected-field definition itself is missing?
- **Conflicting-Evidence Question:** How is completeness assessed when different sources provide different field coverage?
- **Point-in-Time Question:** Are expected fields time-dependent?
- **Dependencies:** DS-412 (roll-up policy)
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Data Confidence cannot assess completeness
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-403 — Reliability

- **Identifier:** DS-403
- **Topic:** How reliability is determined: source track record, extraction accuracy, known issues, and the operational method for assigning reliability per evidence record or per source
- **Decision Obligation Source:** Constitution §13: Reliability. EVIDENCE-MODEL §9: Reliability as Data Confidence dimension
- **Inherited Approved Semantics:** Reliability is a Data Confidence dimension. No operational measurement method is supplied
- **Rule Content Authority:** NONE
- **Unresolved Operational Question:** How is reliability operationally determined? At what level — per source, per record, per extraction? How are extraction accuracy and known issues incorporated?
- **Affected Artifact(s):** DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md; Data Confidence assessment output; Source Registry
- **Decision Category:** Formula, Threshold
- **Materiality:** Material — determines whether data from unreliable sources is discounted
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** Source metadata; source track record data; extraction confidence scores; known issue registry
- **Required Output States:** A deterministic reliability assessment per evidence record or per source
- **Required Explainability:** Source identifier, reliability classification, known issues, extraction accuracy, and the rule version
- **Missing-Data Question:** What happens when a source has no established track record?
- **Conflicting-Evidence Question:** How is reliability assessed when a source is reliable for one data type but unreliable for another?
- **Point-in-Time Question:** At what evaluation timestamp is reliability assessed? Does reliability change over time?
- **Dependencies:** DS-412 (roll-up policy); DS-404 (source independence — may inform reliability)
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Data Confidence cannot assess reliability
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-404 — Source Independence and Derivation Classification

- **Identifier:** DS-404
- **Topic:** Originating source identification, derivation chain tracing, and independence classification (independent, derived, syndicated, unknown)
- **Decision Obligation Source:** EVIDENCE-MODEL §3: "Source independence assessment requires: originating source identification, derivation chain, independence classification (independent, derived, syndicated, unknown)." Constitution §8: "Multiple links copied from one source are not independent evidence"
- **Inherited Approved Semantics:** The independence classification categories (independent, derived, syndicated, unknown) and the requirement to identify originating sources and derivation chains are explicit approved rule content from EVIDENCE-MODEL §3. The operational implementation method is not supplied
- **Rule Content Authority:** EVIDENCE-MODEL §3 — for the classification categories and the requirement to identify originating sources and derivation chains
- **Unresolved Operational Question:** What operational method determines the originating source and derivation chain for each evidence record? How are edge cases (syndicated with modification, translated sources, multi-stage derivations) classified?
- **Affected Artifact(s):** DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md; Evidence records; Source Registry
- **Decision Category:** Other (Classification)
- **Materiality:** Material — determines whether evidence is treated as independent confirmation
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** Source metadata; derivation chain data; evidence record provenance
- **Required Output States:** A deterministic independence classification per evidence record; identification of originating source and derivation chain
- **Required Explainability:** Originating source, derivation chain, independence classification, and the rule version
- **Missing-Data Question:** What happens when the derivation chain cannot be traced?
- **Conflicting-Evidence Question:** How is a record classified when different derivation paths suggest different independence classifications?
- **Point-in-Time Question:** At what evaluation timestamp is independence assessed?
- **Dependencies:** Source Registry; DS-403 (reliability — independence may inform reliability)
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Source independence cannot be assessed; multiple copies from one source may be treated as independent
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-405 — Conflict Detection and Preservation

- **Identifier:** DS-405
- **Topic:** What constitutes a material conflict between independent sources; how conflicts are detected and preserved in the data layer; consolidation of what were previously separate conflicts assessment (DS-104) and conflict-related enforcement (DS-113) decisions
- **Decision Obligation Source:** Constitution §13: Conflicts. EVIDENCE-MODEL §9: Conflicts as Data Confidence dimension. EVIDENCE-MODEL §7: contradictions remain visible and are never averaged away
- **Inherited Approved Semantics:** Conflicts are a Data Confidence dimension. Contradictions must be preserved in the data layer and never silently compressed. This slot addresses data-layer conflict detection and preservation. Human-facing contradiction presentation and display belongs to Gate C (no identifier assigned)
- **Rule Content Authority:** NONE — the approved documents require conflict detection and preservation but do not supply materiality thresholds or detection methods
- **Unresolved Operational Question:** What constitutes a material conflict? How are conflicts detected across sources? How are they preserved in the data layer without being silently compressed?
- **Affected Artifact(s):** DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md; Data Confidence assessment output; Evidence records
- **Decision Category:** Threshold, Formula
- **Materiality:** Material — determines how conflicting data affects confidence and is preserved
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** Evidence records for the same entity/metric from independent sources; source independence classifications; point-in-time evidence values
- **Required Output States:** A deterministic conflict detection method; a preservation rule ensuring conflicts are not silently compressed; identification of conflicting sources, disputed values, and conflict magnitude
- **Required Explainability:** Conflicting sources, disputed values, conflict magnitude, conflict classification, and the rule version
- **Missing-Data Question:** What happens when only one source provides a value — is absence of confirming/conflicting sources treated as neutral or reduced confidence?
- **Conflicting-Evidence Question:** This dimension is about conflicting evidence — how is a multi-source conflict with three different values handled?
- **Point-in-Time Question:** At what evaluation timestamp are conflicts assessed? How are time-staggered source reports handled?
- **Dependencies:** DS-404 (source independence); DS-412 (roll-up policy)
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Data Confidence cannot assess conflicts; contradictions may be silently absorbed
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-406 — Missing Evidence

- **Identifier:** DS-406
- **Topic:** Operational identification, classification, and handling of expected-but-absent evidence, distinct from incompleteness of present records
- **Decision Obligation Source:** Constitution §10: platform must keep track of missing evidence. Constitution §13: Missing data as Data Confidence dimension. EVIDENCE-MODEL §9: Missing data dimension. THEME-MODEL §7: Theme Cards must display missing evidence
- **Inherited Approved Semantics:** Missing evidence must be tracked. Theme Cards must display it. Missing data is a Data Confidence dimension. No operational classification or handling rules are supplied
- **Rule Content Authority:** NONE
- **Unresolved Operational Question:** How is missing evidence operationally identified? What classification scheme applies? How does absence affect Data Confidence?
- **Affected Artifact(s):** DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md; Data Confidence assessment output; Theme Cards
- **Decision Category:** Threshold, Formula
- **Materiality:** Material — determines how absence of expected evidence affects confidence
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** Expected evidence inventory per Theme/Candidate; actual evidence records; missing evidence markers
- **Required Output States:** A deterministic missing-evidence assessment per Theme/Candidate; identification of what is missing and its materiality
- **Required Explainability:** What evidence is expected but absent, why it is expected, its materiality, and the rule version
- **Missing-Data Question:** This dimension is about missing data — what is the meta-behavior when the expected-evidence inventory itself is incomplete?
- **Conflicting-Evidence Question:** How is missing evidence distinguished from evidence that exists but is contradictory?
- **Point-in-Time Question:** Are expectations time-dependent?
- **Dependencies:** DS-412 (roll-up policy); Theme/Candidate expected-evidence definitions
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Missing evidence cannot be systematically identified; Theme Cards lack structured missing-evidence content
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-407 — Public-Availability Timestamp

- **Identifier:** DS-407
- **Topic:** Operational rules for determining and recording when information was first publicly available; guaranteed separation from ingestion timestamp
- **Decision Obligation Source:** EVIDENCE-MODEL §5 requires "Publication / public-availability timestamp." §5.1 requires historical evaluation to use information publicly available at the evaluation timestamp. The timestamp must remain separate from ingestion timestamp (AM-V0-GATE-A-DRAFTING-v0.1)
- **Inherited Approved Semantics:** Every evidence record must carry a public-availability timestamp, separate from the ingestion timestamp. Historical evaluation uses public-availability time, not ingestion time
- **Rule Content Authority:** NONE — the requirement to carry the timestamp is approved; the operational rule for determining it per evidence type is not
- **Unresolved Operational Question:** How is the public-availability timestamp determined for each evidence type? What event establishes it?
- **Affected Artifact(s):** DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md; Evidence record schema; Point-in-time evaluation engine
- **Decision Category:** Period
- **Materiality:** Material — determines what data is visible at any given evaluation timestamp
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** Evidence type classification; source-specific publication conventions; ingestion pipeline metadata
- **Required Output States:** A deterministic rule for assigning the public-availability timestamp per evidence type; guaranteed separation from ingestion timestamp
- **Required Explainability:** Public-availability timestamp, how it was determined, ingestion timestamp, and the rule version
- **Missing-Data Question:** What happens when the public-availability timestamp cannot be determined?
- **Conflicting-Evidence Question:** How is the timestamp determined when source publication time conflicts with third-party availability records?
- **Point-in-Time Question:** This slot defines the timestamp that governs point-in-time visibility
- **Dependencies:** DS-408 (ingestion timestamp); DS-409 (effective period); DS-411 (point-in-time visibility)
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Point-in-time evaluation cannot be implemented; AC-7 and AC-8 cannot be verified
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-408 — Ingestion Timestamp

- **Identifier:** DS-408
- **Topic:** Operational rules for determining and recording when a record was ingested into the platform; guaranteed separation from public-availability timestamp
- **Decision Obligation Source:** EVIDENCE-MODEL §5 requires "Ingestion timestamp." Authorization metadata: "Public-availability timestamp and ingestion timestamp must remain separate"
- **Inherited Approved Semantics:** Every evidence record must carry an ingestion timestamp, separate from the public-availability timestamp
- **Rule Content Authority:** NONE — the requirement to carry the timestamp is approved; the operational rule for determining it is not
- **Unresolved Operational Question:** What event establishes the ingestion timestamp? How is separation from the public-availability timestamp enforced?
- **Affected Artifact(s):** DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md; Evidence record schema; Ingestion pipeline
- **Decision Category:** Period
- **Materiality:** Non-material for V0 rule semantics but material for audit integrity
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** Ingestion pipeline event data; server clock; source-provided timestamps
- **Required Output States:** A deterministic rule for assigning the ingestion timestamp; guaranteed separation from public-availability timestamp
- **Required Explainability:** Ingestion timestamp, how it was determined, and its relationship to the public-availability timestamp
- **Missing-Data Question:** What happens when the ingestion event lacks a reliable timestamp?
- **Conflicting-Evidence Question:** How is the timestamp determined when multiple ingestion events occur for the same content?
- **Point-in-Time Question:** The ingestion timestamp is metadata, not a visibility gate; should downstream processes record it for reproducibility?
- **Dependencies:** DS-407 (public-availability timestamp)
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Evidence records lack reliable ingestion metadata
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-409 — Effective / As-Of and Forecast-Target Periods

- **Identifier:** DS-409
- **Topic:** Operational rules for determining the date or date range an evidence record describes, including forward-looking forecast/projection target periods
- **Decision Obligation Source:** EVIDENCE-MODEL §5 requires "Effective / as-of period — The date or date range the information describes"
- **Inherited Approved Semantics:** Every evidence record must carry an effective/as-of period. No operational determination rules are supplied. Forward-looking forecast/projection periods are not separately addressed
- **Rule Content Authority:** NONE
- **Unresolved Operational Question:** How is the effective period determined per evidence type? How are forecast/projection target periods distinguished from historical effective periods?
- **Affected Artifact(s):** DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md; Evidence record schema; Point-in-time evaluation engine
- **Decision Category:** Period
- **Materiality:** Material — determines whether data is correctly attributed to the period it describes
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** Evidence type classification; source content describing covered periods
- **Required Output States:** A deterministic rule for assigning effective/as-of period per evidence type; distinction between historical and forecast periods
- **Required Explainability:** Effective/as-of period, how determined, forecast vs. historical classification, and the rule version
- **Missing-Data Question:** What happens when an evidence record does not explicitly state its effective period?
- **Conflicting-Evidence Question:** How is the effective period determined when source-stated period conflicts with content?
- **Point-in-Time Question:** How does a historical query interact with effective period vs. public-availability timestamp?
- **Dependencies:** DS-407 (public-availability timestamp); DS-411 (point-in-time visibility)
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Evidence records cannot be correctly attributed to time periods; AC-8 cannot be verified
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-410 — Revision and Vintage Handling

- **Identifier:** DS-410
- **Topic:** Preservation of originals, supersedes/superseded-by linkage, point-in-time version visibility, and vintage effect on Data Confidence
- **Decision Obligation Source:** EVIDENCE-MODEL §5.1: preserve original record, record revision as new record with linkage, historical evaluations see only original (or both with clarity), do not silently replace or backfill. EVIDENCE-MODEL §5 requires "Revision or vintage" and "Supersedes / superseded-by" fields
- **Inherited Approved Semantics:** The revision handling principles are explicit approved rule content: preserve originals, link revisions, do not backfill, historical queries use original or both with provenance. The operational implementation method is not supplied
- **Rule Content Authority:** EVIDENCE-MODEL §5.1 — for the principles: preserve originals, link revisions, do not backfill, historical queries use original or both with provenance
- **Unresolved Operational Question:** What operational method establishes revision relationships between records? How does vintage affect Data Confidence? How are conflicting revisions (correction to a revision) handled?
- **Affected Artifact(s):** DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md; Evidence record schema; Point-in-time evaluation engine
- **Decision Category:** Formula, Period
- **Materiality:** Material — determines integrity of point-in-time historical evaluation
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** Evidence records with potential revision relationships; source-issued correction or restatement notices; vintage identifiers
- **Required Output States:** A deterministic rule for establishing revision relationships; a rule for which version(s) a point-in-time query sees; a rule for revision effect on Data Confidence
- **Required Explainability:** Revision chain, which version was visible at a given evaluation timestamp, and the rule version
- **Missing-Data Question:** What happens when a revision exists but the original record was never ingested?
- **Conflicting-Evidence Question:** How are conflicting revisions (correction to a revision) handled?
- **Point-in-Time Question:** This slot is fundamentally about point-in-time version visibility
- **Dependencies:** DS-407 (public-availability timestamp); DS-409 (effective period); DS-411 (point-in-time visibility)
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Point-in-time evaluation cannot correctly handle revised data; AC-8 cannot be verified
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-411 — Point-in-Time Visibility

- **Identifier:** DS-411
- **Topic:** The exact rules governing what data is visible at a given evaluation timestamp, combining public-availability timestamp, effective/as-of period, revision status, and staleness
- **Decision Obligation Source:** EVIDENCE-MODEL §5.1: "Historical evaluation must use information that was publicly available at the evaluation timestamp, not the latest revised value." ALPHA-MOMENTUM-V0-SPEC §2.2: "V0 data must be queryable at a given point in time"
- **Inherited Approved Semantics:** Historical evaluation must use publicly available data at the evaluation timestamp. V0 data must be point-in-time queryable. The operational visibility function combining all timestamp dimensions is not supplied
- **Rule Content Authority:** NONE — the principle is approved; the operational visibility function is not
- **Unresolved Operational Question:** What is the exact visibility function given an evaluation timestamp? How do public-availability, effective period, revision status, and staleness interact in determining visibility?
- **Affected Artifact(s):** DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md; Point-in-time evaluation engine; Pipeline stage outputs at historical dates
- **Decision Category:** Formula, Period
- **Materiality:** Material — determines correctness of every historical assessment; directly affects AC-7 and AC-8
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** Evidence records with all timestamp fields; revision linkages; staleness markers; evaluation timestamp
- **Required Output States:** A deterministic point-in-time visibility function: given an evaluation timestamp, return the set of visible evidence records and the version of each
- **Required Explainability:** Which records were included/excluded, which version was used, and the rule version for any given historical query
- **Missing-Data Question:** What happens when a record is missing a required timestamp — is it included, excluded, or flagged?
- **Conflicting-Evidence Question:** How does visibility resolve when a record's public-availability timestamp is after the evaluation timestamp but its effective period covers it?
- **Point-in-Time Question:** This slot defines the point-in-time visibility function itself
- **Dependencies:** DS-407 (public-availability timestamp); DS-409 (effective period); DS-410 (revision handling); DS-401 (staleness)
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Historical queries cannot be executed correctly; AC-7 and AC-8 cannot be verified
- **Approval Reference:**
- **Verification Evidence:** pending

---

### Decision Slot: DS-412 — Data Confidence Scope Levels and Roll-Up Policy

- **Identifier:** DS-412
- **Topic:** What Data Confidence means at per-record, per-Candidate, per-Theme, and system-wide levels; whether and how confidence rolls up across levels. Consolidation of what were previously separate aggregation (DS-105) and scope-level (DS-114) decisions
- **Decision Obligation Source:** EVIDENCE-MODEL §9: "Data Confidence applies at multiple levels: individual evidence records, aggregated assessments, and overall system state." CANDIDATE-AND-QUEUE-MODEL §2.4: Data Confidence measures reliability of data underlying Candidate assessments
- **Inherited Approved Semantics:** Data Confidence applies at multiple levels. It is a separate axis from other quality dimensions. No roll-up method is supplied. "No roll-up" is a valid outcome
- **Rule Content Authority:** NONE
- **Unresolved Operational Question:** What does Data Confidence mean at each scope level? Does confidence roll up from per-record to per-Candidate to per-Theme? If so, by what policy?
- **Affected Artifact(s):** DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md; Data Confidence assessment output; Candidate assessments; Theme Cards
- **Decision Category:** Formula, Threshold
- **Materiality:** Material — determines what Data Confidence means when presented alongside other quality dimensions
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Founder Decision Required:** Yes
- **Required Inputs:** Per-record Data Confidence assessments; evidence-to-Candidate and evidence-to-Theme relationships
- **Required Output States:** A deterministic Data Confidence assessment at each scope level; the assessment must remain separate from Candidate Quality, Theme Quality, and Entry Readiness; "no roll-up — each level independently assessed" is a valid outcome
- **Required Explainability:** Which evidence records contributed, their individual confidence levels, roll-up method (if any), and the rule version
- **Missing-Data Question:** What happens when a scope level has no linked evidence records?
- **Conflicting-Evidence Question:** How is a Candidate-level assessment handled when some evidence records have high confidence and others low?
- **Point-in-Time Question:** At what evaluation timestamp is scope-level Data Confidence assessed?
- **Dependencies:** DS-401 through DS-406 (all dimension decisions)
- **Alternatives to Evaluate: Not populated during Gate A drafting. Alternatives require separate Founder-guided analysis and must not be inferred or proposed by AI.
- **Known Risks if Deferred:** Data Confidence cannot be meaningfully presented at Candidate and Theme levels; AC-3 cannot show useful Data Confidence
- **Approval Reference:**
- **Verification Evidence:** pending

---

## 3. Conditional Templates

No templates are defined in this artifact. All 12 slots are active Gate A decisions.

---

## 4. Inherited Controls

### Higher-Authority Escalation

- **Source:** DESIGN-PLAN.md §13; AGENTS.md authority hierarchy
- **Rule:** Same as documented in RULE-PACK-AND-QUALITY-CONTRACTS.md §4. Applicable to any Data Confidence decision that would change or narrow higher authority
- **Status:** Inherited approved governance control

### Contradiction Visibility (Presentation Layer)

- **Source:** EVIDENCE-MODEL §7
- **Rule:** Contradictions must remain visible. Human-facing presentation display belongs to Gate C. Data-layer detection and preservation belongs to DS-405
- **Status:** Inherited approved rule

---

## 5. Deferred and Future-Gate Topics

No topics deferred or moved to future gates from this artifact.

---

## 6. Slot Supersession Map

This artifact's v0.1-draft contained 14 decision slots (DS-101–DS-114). Full cross-artifact supersession details are in TRACEABILITY-AND-DECISION-REGISTER.md.

| Old ID | Disposition | Reference |
|---|---|---|
| DS-101 | Merged into | DS-401 (Freshness and Staleness) |
| DS-102 | Superseded by | DS-402 (Completeness and Expected-Data Contract) |
| DS-103 | Superseded by | DS-403 (Reliability) |
| DS-104 | Merged into | DS-405 (Conflict Detection and Preservation) |
| DS-105 | Merged into | DS-412 (Scope Levels and Roll-Up Policy) |
| DS-106 | Superseded by | DS-406 (Missing Evidence) |
| DS-107 | Superseded by | DS-407 (Public-Availability Timestamp) |
| DS-108 | Superseded by | DS-409 (Effective / As-Of and Forecast-Target Periods) |
| DS-109 | Superseded by | DS-410 (Revision and Vintage Handling) |
| DS-110 | Merged into | DS-401 (Freshness and Staleness) |
| DS-111 | Superseded by | DS-411 (Point-in-Time Visibility) |
| DS-112 | Superseded by | DS-408 (Ingestion Timestamp) |
| DS-113 | Merged into | DS-405 (Conflict Detection and Preservation — data layer); contradiction presentation moved to Gate C |
| DS-114 | Merged into | DS-412 (Scope Levels and Roll-Up Policy) |

---

## 7. Verification Requirements

- All 12 active slots are Proposed, UNRESOLVED — FOUNDER DECISION REQUIRED
- No slot proposes prohibited content
- Every slot carries Decision Obligation Source, Inherited Approved Semantics, Rule Content Authority, and Unresolved Operational Question
- DS-405 limits scope to data-layer detection and preservation; human-facing presentation belongs to Gate C
- No DS identifiers reused from old range
- References DS-513 (Rule Lifecycle) from Pipeline artifact for rule-version linkage
