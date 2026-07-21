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
- **Rule Content Authority:** Constitution §8 — for the three-year default for unsupported narrative evidence only. Founder-provided rule — for the V0 operational rule covering all other evidence types
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision:**
  - **Hard rule (Constitution §8, applies now):** Unsupported narrative/intention-based evidence (e.g., "management says they plan to enter AI market" but no contracts, hiring, or capex follows) with zero measurable action within 3 years from the statement date → automatically marked **stale**. This is not a V0 simplification — it is constitutional rule content that applies at all versions.
  - **V0 rule for all other evidence types:** Freshness is fixture-assigned. The fixture creator sets a `freshness_status` per record: `current`, `aging`, or `stale`, plus a `freshness_expiry_date`. No automatic computation in V0 — we're not ingesting real data yet. The fixture creator controls all values to demonstrate the concept.
  - **What this looks like in practice:**
    - Earnings report from last quarter → fixture marks it `current`, expires after next earnings date
    - Price data from 6 months ago → fixture marks it `aging` (still relevant but not latest)
    - Old news article with no follow-up → fixture marks it `stale`
    - "CEO says AI is coming" from 2021, zero execution since → Constitution §8 kicks in → `stale` (unless approved long-cycle exception)
  - **Deferred to V0.5:** Real-time freshness computation — automatic expiry-date calculation based on evidence type, automated aging signals from timestamp comparison, freshness period configuration per evidence type. All of this needs real data ingestion to be meaningful.
- **Affected Artifact(s):** DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md; Data Confidence assessment output; Evidence records
- **Decision Category:** Period, Threshold
- **Materiality:** Material — determines whether evidence is treated as current or stale
- **Status:** Approved
- **Resolution:** RESOLVED — Constitution §8 hard rule for narrative evidence + V0 fixture-assigned freshness for all other types
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** Evidence records with timestamps; evidence type classification; evaluation timestamps
- **Required Output States:** Every evidence record carries a `freshness_status` (current/aging/stale) and `freshness_expiry_date`. Narrative evidence additionally checked against the constitutional 3-year default.
- **Required Explainability:** Evidence age, freshness classification, staleness classification, applicable rule, and the rule version
- **Missing-Data Question:** Records missing timestamps needed for freshness → flagged `Not Assessable`
- **Conflicting-Evidence Question:** When different staleness rules could apply to the same record (e.g., a narrative statement also containing factual data) → the stricter rule wins
- **Point-in-Time Question:** Freshness and staleness are assessed relative to the evaluation timestamp of the pipeline run
- **Dependencies:** DS-412 (roll-up policy); DS-410 (revision handling — revisions affect freshness of originals)
- **Alternatives to Evaluate:** Evaluated by Founder — V0 fixture-assigned approach chosen to match controlled synthetic data reality; constitutional hard rule applied immediately
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-3B-DIMENSIONS-v0.1
- **Verification Evidence:** Founder approved V0 fixture-assigned freshness with Constitution §8 hard rule in session

---

### Decision Slot: DS-402 — Completeness and Expected-Data Contract

- **Identifier:** DS-402
- **Topic:** What fields, periods, or entities are expected per evidence type; how completeness is measured; and the operational expected-data contract
- **Decision Obligation Source:** Constitution §13: Completeness. EVIDENCE-MODEL §9: Completeness as Data Confidence dimension
- **Inherited Approved Semantics:** Completeness is a Data Confidence dimension. What constitutes "expected" data is not supplied
- **Rule Content Authority:** Founder-provided rule — this decision
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (V0 Fixture-Defined Expected-Data Contract):**
  - **What "completeness" means:** For each type of evidence record, there's a checklist of fields that should be present. If a field is missing, the record is incomplete. Simple as that.
  - **V0 approach:** The fixture creator defines an "expected fields" template per evidence type. Each record is checked against its template. Missing fields = reduced completeness.
  - **Concrete example — Earnings Report record type:**
    - Expected: `ticker, report_date, revenue, eps, net_income, operating_margin`
    - Record A has all 6 → completeness = full
    - Record B is missing `operating_margin` → completeness = partial (5/6 fields present)
  - **Concrete example — Price Data record type:**
    - Expected: `ticker, date, open, high, low, close, volume`
    - Record has all 7 → complete
    - Record missing `volume` → partial
  - **Output:** Each evidence record gets a `completeness_status`: `complete`, `partial` (with list of missing fields and ratio), or `empty` (no expected fields present). Each evidence type has its expected-field template documented.
  - **Deferred to V0.5:** Automatic expected-field template generation, dynamic completeness rules based on entity/sector/period, handling of optional vs. mandatory fields per evidence type. All of this requires real data sources to design meaningfully.
- **Affected Artifact(s):** DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md; Data Confidence assessment output; Evidence records
- **Decision Category:** Threshold, Formula
- **Materiality:** Material — determines whether incomplete data triggers reduced Data Confidence
- **Status:** Approved
- **Resolution:** RESOLVED — V0: fixture-defined expected-field templates per evidence type; completeness = present fields / expected fields
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** Evidence record schema definitions; expected-field specifications per evidence type; evidence record data
- **Required Output States:** Per evidence type: a documented expected-field template. Per evidence record: `completeness_status` (complete/partial/empty) plus missing-field list and completeness ratio.
- **Required Explainability:** Expected fields, present fields, missing fields, completeness classification, and the rule version
- **Missing-Data Question:** Meta-behavior: when the expected-field template itself is missing for an evidence type, records of that type are flagged `Not Assessable`
- **Conflicting-Evidence Question:** When different sources provide different field coverage for the same type of information, each record is assessed against its own type's template independently
- **Point-in-Time Question:** Expected-field templates may change over time — the template version applied is the one effective at the evaluation timestamp
- **Dependencies:** DS-412 (roll-up policy)
- **Alternatives to Evaluate:** Evaluated by Founder — fixture-defined template approach chosen for V0 simplicity
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-3B-DIMENSIONS-v0.1
- **Verification Evidence:** Founder approved V0 fixture-defined expected-data contract in session

---

### Decision Slot: DS-403 — Reliability

- **Identifier:** DS-403
- **Topic:** How reliability is determined: source track record, extraction accuracy, known issues, and the operational method for assigning reliability per evidence record or per source
- **Decision Obligation Source:** Constitution §13: Reliability. EVIDENCE-MODEL §9: Reliability as Data Confidence dimension
- **Inherited Approved Semantics:** Reliability is a Data Confidence dimension. No operational measurement method is supplied
- **Rule Content Authority:** Founder-provided rule — this decision
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (V0 Fixture-Assigned Reliability per Source):**
  - **What "reliability" means:** How much we trust the source that provided this data. A direct SEC filing is more reliable than a news article. A known-good data vendor is more reliable than an unverified scraper.
  - **V0 approach:** Reliability is assigned per source (not per individual record) at fixture creation time. Since V0 uses only synthetic data, most sources are marked `high` reliability by default — but the fixture creator can deliberately mark some sources `low` to demonstrate how the system handles unreliable data.
  - **Reliability levels:** `high` (trusted — e.g., SEC filing, established vendor), `medium` (usable but verify — e.g., reputable news outlet), `low` (treat with caution — e.g., unverified third-party, AI extraction without human review), `unknown` (new source, no track record yet).
  - **Source-level, not record-level:** The reliability label applies to the source. All records from that source inherit its reliability. This keeps it simple — no per-record reliability calculus needed in V0.
  - **Concrete example:** Fixture has 3 sources: "SEC EDGAR" (`high`), "Bloomberg" (`high`), "Random Blog Scraper" (`low`). Any earnings data from "Random Blog Scraper" is flagged `low` reliability regardless of content.
  - **Deferred to V0.5:** Per-record reliability (where a normally-reliable source has a known bad record), automated source track-record scoring, extraction accuracy integration, known-issue registry. All of this needs real data to be meaningful.
- **Affected Artifact(s):** DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md; Data Confidence assessment output; Source Registry
- **Decision Category:** Formula, Threshold
- **Materiality:** Material — determines whether data from unreliable sources is discounted
- **Status:** Approved
- **Resolution:** RESOLVED — V0: fixture-assigned reliability per source (high/medium/low/unknown), inherited by all records from that source
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** Source metadata; source track record data; extraction confidence scores; known issue registry
- **Required Output States:** Each source in the Source Registry carries a `reliability` field. Each evidence record inherits the reliability of its source.
- **Required Explainability:** Source identifier, reliability classification, known issues, extraction accuracy, and the rule version
- **Missing-Data Question:** A source with no reliability assignment defaults to `unknown`
- **Conflicting-Evidence Question:** When a source is reliable for one data type but unreliable for another (e.g., Bloomberg for prices vs. estimates) → deferred to V0.5 per-data-type reliability
- **Point-in-Time Question:** Reliability is assessed at the evaluation timestamp — a source's reliability may change over time (e.g., source quality degrades)
- **Dependencies:** DS-412 (roll-up policy); DS-404 (source independence — may inform reliability)
- **Alternatives to Evaluate:** Evaluated by Founder — source-level V0 approach chosen for simplicity; per-record and per-data-type deferred
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-3B-DIMENSIONS-v0.1
- **Verification Evidence:** Founder approved V0 source-level fixture-assigned reliability in session

---

### Decision Slot: DS-404 — Source Independence and Derivation Classification

- **Identifier:** DS-404
- **Topic:** Originating source identification, derivation chain tracing, and independence classification (independent, derived, syndicated, unknown)
- **Decision Obligation Source:** EVIDENCE-MODEL §3: "Source independence assessment requires: originating source identification, derivation chain, independence classification (independent, derived, syndicated, unknown)." Constitution §8: "Multiple links copied from one source are not independent evidence"
- **Inherited Approved Semantics:** The independence classification categories (independent, derived, syndicated, unknown) and the requirement to identify originating sources and derivation chains are explicit approved rule content from EVIDENCE-MODEL §3. The operational implementation method is not supplied
- **Rule Content Authority:** EVIDENCE-MODEL §3 — for the classification categories and the requirement to identify originating sources and derivation chains. Founder-provided rule — for the V0 operational method
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (V0 Fixture-Assigned Independence Classification):**
  - **What "independence" means:** If Reuters and Bloomberg both report the same earnings number, that looks like 2 confirmations. But if Reuters simply republished Bloomberg's report, it's really just 1 source — counting it twice creates false confidence. The independence classification prevents this.
  - **4 categories (approved by EVIDENCE-MODEL §3):**
    - `independent` — this record comes from its own original source, not copied from another
    - `derived` — this record was computed or transformed from another source (e.g., a ratio calculated from raw data)
    - `syndicated` — this record is a republication of another source's content (e.g., Reuters republishing a Bloomberg scoop)
    - `unknown` — we can't determine the derivation chain
  - **V0 approach:** The fixture creator assigns the independence classification per record. The fixture also documents the `originating_source` (who first published this) and `derivation_chain` (the path from original to this record). Since V0 uses synthetic data, all records can be `independent` by default unless the fixture deliberately models a syndication/derivation scenario.
  - **Concrete example:** Fixture defines 3 records about NVDA earnings: SEC filing (independent), Bloomberg article citing the SEC filing (derived → originating_source: SEC), Yahoo Finance republishing Bloomberg (syndicated → originating_source: Bloomberg). The system knows only the SEC filing is truly independent.
  - **Deferred to V0.5:** Automated derivation chain detection, cross-source content fingerprinting, syndication detection from URL/canonical-link patterns. All of this requires real multi-source data.
- **Affected Artifact(s):** DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md; Evidence records; Source Registry
- **Decision Category:** Other (Classification)
- **Materiality:** Material — determines whether evidence is treated as independent confirmation
- **Status:** Approved
- **Resolution:** RESOLVED — V0: fixture-assigned independence classification per record, using EVIDENCE-MODEL §3 categories
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** Source metadata; derivation chain data; evidence record provenance
- **Required Output States:** Each evidence record carries: `independence` (independent/derived/syndicated/unknown), `originating_source`, and `derivation_chain`.
- **Required Explainability:** Originating source, derivation chain, independence classification, and the rule version
- **Missing-Data Question:** Records where derivation chain cannot be traced default to `unknown`
- **Conflicting-Evidence Question:** When different derivation paths suggest different classifications → most conservative wins (if any path shows derived/syndicated, the record is not independent)
- **Point-in-Time Question:** Independence is assessed at the evaluation timestamp — a record's derivation chain is a property of the record, not time-dependent
- **Dependencies:** Source Registry; DS-403 (reliability — independence may inform reliability)
- **Alternatives to Evaluate:** Evaluated by Founder — V0 fixture-assigned approach chosen for simplicity; automated detection deferred
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-3B-DIMENSIONS-v0.1
- **Verification Evidence:** Founder approved V0 fixture-assigned independence classification in session

---

### Decision Slot: DS-405 — Conflict Detection and Preservation

- **Identifier:** DS-405
- **Topic:** What constitutes a material conflict between independent sources; how conflicts are detected and preserved in the data layer; consolidation of what were previously separate conflicts assessment (DS-104) and conflict-related enforcement (DS-113) decisions
- **Decision Obligation Source:** Constitution §13: Conflicts. EVIDENCE-MODEL §9: Conflicts as Data Confidence dimension. EVIDENCE-MODEL §7: contradictions remain visible and are never averaged away
- **Inherited Approved Semantics:** Conflicts are a Data Confidence dimension. Contradictions must be preserved in the data layer and never silently compressed. This slot addresses data-layer conflict detection and preservation. Human-facing contradiction presentation and display belongs to Gate C (no identifier assigned)
- **Rule Content Authority:** Founder-provided rule — this decision
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (V0 Fixture-Injected Conflicts):**
  - **What "conflict" means:** Two independent sources report different values for the same thing. Example: Source A says NVDA Q2 revenue = $30B, Source B (independent) says $28B. The difference ($2B gap) is a conflict. The system records both values — it does not average them ($29B) or pick one.
  - **V0 approach:** Conflicts are deliberately injected by the fixture creator. No automatic conflict detection algorithm runs in V0. The fixture creator defines: which records conflict, what the conflicting values are, and whether the conflict is `material` (would change an assessment) or `minor` (cosmetic difference).
  - **Preservation rule (hard, applies at all versions):** Conflicts are never compressed, averaged, or silently resolved. When a conflict exists, all conflicting values are preserved and visible. This is not a V0 simplification — it is a constitutional requirement (EVIDENCE-MODEL §7).
  - **Conflict structure:** Each conflict record links to the conflicting evidence records and stores: `conflict_type` (value_disagreement, classification_disagreement, temporal_inconsistency), `conflict_magnitude` (the size of the gap — e.g., $2B difference), `conflict_materiality` (material/minor), and `conflicting_values` (the different values from each source).
  - **Edge cases:** One source only → no conflict, but absence of confirmation is noted (not the same as a conflict). Three different values from three independent sources → all three are preserved. Time-staggered reports → if Source A reports Q2 revenue on July 15 and Source B reports a different Q2 revenue on August 1, both are preserved with their public-availability timestamps.
  - **Deferred to V0.5:** Automated conflict detection (statistical outlier detection, cross-source value comparison at scale), automated materiality thresholds, temporal conflict resolution logic. All of this needs real multi-source data.
- **Affected Artifact(s):** DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md; Data Confidence assessment output; Evidence records
- **Decision Category:** Threshold, Formula
- **Materiality:** Material — determines how conflicting data affects confidence and is preserved
- **Status:** Approved
- **Resolution:** RESOLVED — V0: fixture-injected conflicts with explicit materiality; preservation rule (no compression, no averaging) applies at all versions
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** Evidence records for the same entity/metric from independent sources; source independence classifications; point-in-time evidence values
- **Required Output States:** Conflict records link conflicting evidence and store: conflict_type, conflict_magnitude, conflict_materiality, conflicting_values. No silent compression or averaging.
- **Required Explainability:** Conflicting sources, disputed values, conflict magnitude, conflict classification, and the rule version
- **Missing-Data Question:** Single-source values without independent confirmation are not conflicts — they are noted as "unconfirmed" (distinct from "conflicted")
- **Conflicting-Evidence Question:** Multi-source conflicts with 3+ different values → all preserved; no picking a "winner"
- **Point-in-Time Question:** Conflicts are assessed at the evaluation timestamp — a conflict that existed at one point may be resolved later (e.g., by a correction)
- **Dependencies:** DS-404 (source independence); DS-412 (roll-up policy)
- **Alternatives to Evaluate:** Evaluated by Founder — V0 fixture-injected conflicts chosen to demonstrate the concept; automated detection deferred
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-3B-DIMENSIONS-v0.1
- **Verification Evidence:** Founder approved V0 fixture-injected conflicts with mandatory preservation rule in session

---

### Decision Slot: DS-406 — Missing Evidence

- **Identifier:** DS-406
- **Topic:** Operational identification, classification, and handling of expected-but-absent evidence, distinct from incompleteness of present records
- **Decision Obligation Source:** Constitution §10: platform must keep track of missing evidence. Constitution §13: Missing data as Data Confidence dimension. EVIDENCE-MODEL §9: Missing data dimension. THEME-MODEL §7: Theme Cards must display missing evidence
- **Inherited Approved Semantics:** Missing evidence must be tracked. Theme Cards must display it. Missing data is a Data Confidence dimension. No operational classification or handling rules are supplied
- **Rule Content Authority:** Founder-provided rule — this decision
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (V0 Fixture-Defined Missing-Evidence Inventory):**
  - **How this differs from Completeness (DS-402):** Completeness checks whether a record we *have* is missing fields. Missing Evidence tracks records we *don't have at all* but should. Example: we have NVDA's earnings for Q1 and Q3, but Q2 is missing entirely → that's missing evidence. We have Q2 earnings but it's missing the `operating_margin` field → that's incompleteness (DS-402).
  - **V0 approach:** The fixture creator defines an "expected evidence inventory" per Theme and per Candidate — a list of what evidence *should* exist. Missing items are explicitly tagged. The system does not guess what's missing.
  - **Missing evidence classification:**
    - `expected_missing` — we know this should exist but we don't have it (e.g., Q2 earnings not yet filed, or a known data gap)
    - `structural_gap` — this type of evidence would normally exist for this kind of analysis but was never part of the data scope (e.g., insider transaction data was not ingested)
    - `unexpected_absence` — evidence that was expected based on pattern but confirmation is pending (e.g., a company that always reports by week 4 is now at week 6 with no filing)
  - **Output:** Each Theme/Candidate carries a `missing_evidence` list showing: what's missing, its classification, why it was expected, and its materiality (would its absence change an assessment?).
  - **Deferred to V0.5:** Automated expected-evidence generation (inferring what should exist from patterns, sector norms, filing calendars), automatic gap detection, dynamic missing-evidence scoring. All of this requires real data patterns.
- **Affected Artifact(s):** DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md; Data Confidence assessment output; Theme Cards
- **Decision Category:** Threshold, Formula
- **Materiality:** Material — determines how absence of expected evidence affects confidence
- **Status:** Approved
- **Resolution:** RESOLVED — V0: fixture-defined expected-evidence inventory per Theme/Candidate; three-category classification
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** Expected evidence inventory per Theme/Candidate; actual evidence records; missing evidence markers
- **Required Output States:** Per Theme/Candidate: `missing_evidence` list with classification, expected-by date, and materiality.
- **Required Explainability:** What evidence is expected but absent, why it is expected, its materiality, and the rule version
- **Missing-Data Question:** Meta-behavior: when the expected-evidence inventory itself is incomplete, this is noted as a `structural_gap` at the assessment level
- **Conflicting-Evidence Question:** Missing evidence is distinct from contradictory evidence (DS-405) — missing = we don't have it, conflict = we have two versions that disagree
- **Point-in-Time Question:** Expected-evidence inventories are time-dependent — what's expected at one evaluation date may differ from another (e.g., a quarterly filing that hasn't happened yet isn't "missing," it's "not yet due")
- **Dependencies:** DS-412 (roll-up policy); Theme/Candidate expected-evidence definitions
- **Alternatives to Evaluate:** Evaluated by Founder — V0 fixture-defined inventory approach chosen for simplicity; automated detection deferred
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-3B-DIMENSIONS-v0.1
- **Verification Evidence:** Founder approved V0 fixture-defined missing-evidence inventory in session

---

### Decision Slot: DS-407 — Public-Availability Timestamp

- **Identifier:** DS-407
- **Topic:** Operational rules for determining and recording when information was first publicly available; guaranteed separation from ingestion timestamp
- **Decision Obligation Source:** EVIDENCE-MODEL §5 requires "Publication / public-availability timestamp." §5.1 requires historical evaluation to use information publicly available at the evaluation timestamp. The timestamp must remain separate from ingestion timestamp (AM-V0-GATE-A-DRAFTING-v0.1)
- **Inherited Approved Semantics:** Every evidence record must carry a public-availability timestamp, separate from the ingestion timestamp. Historical evaluation uses public-availability time, not ingestion time
- **Rule Content Authority:** Founder-provided rule — this decision
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (V0 Synthetic Fixture Rule):**
  - In V0, all data comes from controlled synthetic fixtures. The public-availability timestamp is explicitly assigned per record by the fixture creator.
  - **Format:** `YYYY-MM-DD` (date only — sufficient for V0 end-of-day evaluation granularity)
  - **Separation guarantee:** The public-availability timestamp field is structurally separate from the ingestion timestamp field. Both must exist but their values are independently assigned.
  - **Operational complexity deferred:** Real-source public-availability determination rules (source scraping timestamps, press release times, filing timestamps) are deferred to V0.5 when real data ingestion begins.
- **Affected Artifact(s):** DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md; Evidence record schema; Point-in-time evaluation engine
- **Decision Category:** Period
- **Materiality:** Material — determines what data is visible at any given evaluation timestamp
- **Status:** Approved
- **Resolution:** RESOLVED — V0: fixture-defined per record, `YYYY-MM-DD` format, separate from ingestion timestamp
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** Evidence type classification; source-specific publication conventions; ingestion pipeline metadata
- **Required Output States:** A deterministic rule: public-availability timestamp is fixture-assigned per record in `YYYY-MM-DD` format; guaranteed separate field from ingestion timestamp
- **Required Explainability:** Public-availability timestamp, how it was determined (fixture-assigned in V0), ingestion timestamp, and the rule version
- **Missing-Data Question:** In V0, records missing a public-availability timestamp are flagged as "Not Assessable" for point-in-time queries
- **Conflicting-Evidence Question:** Not applicable in V0 — fixture creator controls all timestamps
- **Point-in-Time Question:** This slot defines the timestamp that governs point-in-time visibility
- **Dependencies:** DS-408 (ingestion timestamp); DS-409 (effective period); DS-411 (point-in-time visibility)
- **Alternatives to Evaluate:** Evaluated by Founder — V0 fixture-assigned approach chosen to match controlled synthetic data reality; operational detail deferred to V0.5
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-3A-TIMESTAMPS-v0.1
- **Verification Evidence:** Founder approved V0 fixture-defined approach with `YYYY-MM-DD` format in session

---

### Decision Slot: DS-408 — Ingestion Timestamp

- **Identifier:** DS-408
- **Topic:** Operational rules for determining and recording when a record was ingested into the platform; guaranteed separation from public-availability timestamp
- **Decision Obligation Source:** EVIDENCE-MODEL §5 requires "Ingestion timestamp." Authorization metadata: "Public-availability timestamp and ingestion timestamp must remain separate"
- **Inherited Approved Semantics:** Every evidence record must carry an ingestion timestamp, separate from the public-availability timestamp
- **Rule Content Authority:** Founder-provided rule — this decision
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (V0 Synthetic Fixture Rule):**
  - In V0, all data is loaded from controlled synthetic fixtures. The ingestion timestamp is the timestamp at which the fixture record is first loaded into the platform.
  - **Format:** `YYYY-MM-DD HH:MM:SS` (datetime — captures the actual moment of loading)
  - **Separation guarantee:** Structurally separate field from public-availability timestamp. In V0 with fixture data, ingestion time may be close to or equal to fixture creation time — this is acceptable because there is no real ingestion pipeline.
  - **Operational complexity deferred:** Real ingestion pipeline timestamp determination (server clock synchronization, timezone handling, batched vs. streaming ingestion) is deferred to V0.5.
- **Affected Artifact(s):** DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md; Evidence record schema; Ingestion pipeline
- **Decision Category:** Period
- **Materiality:** Non-material for V0 rule semantics but material for audit integrity
- **Status:** Approved
- **Resolution:** RESOLVED — V0: timestamp of fixture load, `YYYY-MM-DD HH:MM:SS` format, separate from public-availability timestamp
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** Ingestion pipeline event data; server clock; source-provided timestamps
- **Required Output States:** A deterministic rule: ingestion timestamp is the moment of fixture load in `YYYY-MM-DD HH:MM:SS` format; guaranteed separate field from public-availability timestamp
- **Required Explainability:** Ingestion timestamp, how it was determined (fixture load time in V0), and its relationship to the public-availability timestamp
- **Missing-Data Question:** In V0, records without a load event use the fixture batch load timestamp
- **Conflicting-Evidence Question:** Not applicable in V0
- **Point-in-Time Question:** The ingestion timestamp is metadata, not a visibility gate; recorded for reproducibility and audit
- **Dependencies:** DS-407 (public-availability timestamp)
- **Alternatives to Evaluate:** Evaluated by Founder — V0 fixture-load-time approach chosen to match controlled synthetic data reality; operational detail deferred to V0.5
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-3A-TIMESTAMPS-v0.1
- **Verification Evidence:** Founder approved V0 fixture-load-time approach with `YYYY-MM-DD HH:MM:SS` format in session

---

### Decision Slot: DS-409 — Effective / As-Of and Forecast-Target Periods

- **Identifier:** DS-409
- **Topic:** Operational rules for determining the date or date range an evidence record describes, including forward-looking forecast/projection target periods
- **Decision Obligation Source:** EVIDENCE-MODEL §5 requires "Effective / as-of period — The date or date range the information describes"
- **Inherited Approved Semantics:** Every evidence record must carry an effective/as-of period. No operational determination rules are supplied. Forward-looking forecast/projection periods are not separately addressed
- **Rule Content Authority:** Founder-provided rule — this decision
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (V0 Synthetic Fixture Rule):**
  - In V0, the effective period is explicitly assigned per record by the fixture creator.
  - **Format:** Single date `YYYY-MM-DD` for point-in-time data (e.g., stock price on a date) or date range `YYYY-MM-DD / YYYY-MM-DD` for period data (e.g., quarterly earnings).
  - **Classification flag:** Each record carries a `period_type` field with values `historical` or `forecast`. Historical periods describe events that have already occurred. Forecast periods describe projections/estimates for future periods. This flag is structurally separate from the date value.
  - **Examples:**
    - Q1 2025 earnings actual: `effective: 2025-01-01 / 2025-03-31, period_type: historical`
    - Q3 2025 earnings estimate: `effective: 2025-07-01 / 2025-09-30, period_type: forecast`
    - Daily closing price June 15: `effective: 2025-06-15, period_type: historical`
  - **Operational complexity deferred:** Real-source effective period determination (parsing filing dates, fiscal calendar mapping, forecast horizon conventions) is deferred to V0.5.
- **Affected Artifact(s):** DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md; Evidence record schema; Point-in-time evaluation engine
- **Decision Category:** Period
- **Materiality:** Material — determines whether data is correctly attributed to the period it describes
- **Status:** Approved
- **Resolution:** RESOLVED — V0: fixture-defined per record; single date or range; `period_type` flag (historical/forecast)
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** Evidence type classification; source content describing covered periods
- **Required Output States:** A deterministic rule: effective period is fixture-assigned per record as single date or date range; `period_type` flag distinguishes historical from forecast
- **Required Explainability:** Effective/as-of period, how determined (fixture-assigned in V0), forecast vs. historical classification, and the rule version
- **Missing-Data Question:** In V0, records missing an effective period are flagged "Not Assessable" for time-attributed queries
- **Conflicting-Evidence Question:** Not applicable in V0 — fixture creator controls period attribution
- **Point-in-Time Question:** How does a historical query interact with effective period vs. public-availability timestamp? (Resolved in DS-411)
- **Dependencies:** DS-407 (public-availability timestamp); DS-411 (point-in-time visibility)
- **Alternatives to Evaluate:** Evaluated by Founder — V0 fixture-assigned approach with historical/forecast distinction; operational detail deferred to V0.5
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-3A-TIMESTAMPS-v0.1
- **Verification Evidence:** Founder approved V0 fixture-defined approach with `period_type` flag in session

---

### Decision Slot: DS-410 — Revision and Vintage Handling

- **Identifier:** DS-410
- **Topic:** Preservation of originals, supersedes/superseded-by linkage, point-in-time version visibility, and vintage effect on Data Confidence
- **Decision Obligation Source:** EVIDENCE-MODEL §5.1: preserve original record, record revision as new record with linkage, historical evaluations see only original (or both with clarity), do not silently replace or backfill. EVIDENCE-MODEL §5 requires "Revision or vintage" and "Supersedes / superseded-by" fields
- **Inherited Approved Semantics:** The revision handling principles are explicit approved rule content: preserve originals, link revisions, do not backfill, historical queries use original or both with provenance. The operational implementation method is not supplied
- **Rule Content Authority:** EVIDENCE-MODEL §5.1 — for the principles: preserve originals, link revisions, do not backfill, historical queries use original or both with provenance. Founder-provided rule — for the V0 operational method
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision:**
  - **กฎตายตัว (ใช้ทุก version):** หลักการจาก EVIDENCE-MODEL §5.1 เป็นกฎที่ต้องทำตามเสมอ:
    1. เก็บข้อมูลต้นฉบับไว้ตลอด ห้ามลบหรือเขียนทับ
    2. เมื่อมีการแก้ไขย้อนหลัง (เช่นบริษัท restate งบการเงิน) → สร้าง record ใหม่ ไม่ใช่แก้ record เดิม
    3. record ใหม่กับ record เดิมต้องเชื่อมโยงกัน (record ใหม่ชี้ว่าแก้มาจาก record ไหน — `supersedes` / `superseded_by`)
    4. เวลาดูข้อมูลย้อนหลังในอดีต → ต้องเห็นข้อมูลที่มีอยู่ ณ วันนั้น ไม่ใช่ข้อมูลที่ถูกแก้ทีหลัง
    5. ห้ามเอางบที่ถูก restate แล้วไปแปะทับงบเดิมในอดีต (no backfill)
  - **V0:** fixture creator สร้าง revision chain ตัวอย่างเพื่อสาธิต — เช่น งบ Q1/2025 ประกาศครั้งแรกวันที่ 15 เม.ย., ต่อมาบริษัทแก้ไขวันที่ 1 มิ.ย. → มี 2 records เชื่อมกัน, ถ้า query วันที่ 20 เม.ย. จะเห็นแค่ record แรก (ยังไม่มี record แก้ไข)
  - **เลื่อนไป V0.5:** ระบบตรวจจับการแก้ไขอัตโนมัติจาก source, การ reconcile revision chain ที่ซับซ้อน (แก้แล้วแก้อีก), ผลกระทบของ revision ต่อ Data Confidence แบบอัตโนมัติ — ทั้งหมดนี้ต้องรอข้อมูลจริง
- **Affected Artifact(s):** DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md; Evidence record schema; Point-in-time evaluation engine
- **Decision Category:** Formula, Period
- **Materiality:** Material — determines integrity of point-in-time historical evaluation
- **Status:** Approved
- **Resolution:** RESOLVED — EVIDENCE-MODEL §5.1 หลักการ revision handling เป็นกฎตายตัว; V0 สาธิตด้วย synthetic revision chain
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** Evidence records with potential revision relationships; source-issued correction or restatement notices; vintage identifiers
- **Required Output States:** ทุก evidence record มี field `supersedes` และ `superseded_by` สำหรับเชื่อมโยง revision chain. การ query ย้อนหลังเลือก version ที่มีอยู่ ณ evaluation date โดยอัตโนมัติ
- **Required Explainability:** Revision chain, which version was visible at a given evaluation timestamp, and the rule version
- **Missing-Data Question:** กรณีมี revision แต่ไม่เคย ingest ต้นฉบับมาก่อน → revision record ถูกบันทึกตามปกติ, `supersedes` field ว่าง (ไม่รู้ว่าแก้อะไร)
- **Conflicting-Evidence Question:** กรณีแก้แล้วแก้อีก (แก้ revision) → chain ต่อกันเป็นทอดๆ, ทุก version ถูกเก็บหมด
- **Point-in-Time Question:** หัวใจของ slot นี้คือ version visibility ณ evaluation date
- **Dependencies:** DS-407 (public-availability timestamp); DS-409 (effective period); DS-411 (point-in-time visibility)
- **Alternatives to Evaluate:** Evaluated by Founder — หลักการ revision handling จาก EVIDENCE-MODEL ใช้ทันที; V0 synthetic chain สำหรับสาธิต
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-3C-CAPSTONE-v0.1
- **Verification Evidence:** Founder approved EVIDENCE-MODEL §5.1 principles as hard rules with V0 synthetic demonstration in session

---

### Decision Slot: DS-411 — Point-in-Time Visibility

- **Identifier:** DS-411
- **Topic:** The exact rules governing what data is visible at a given evaluation timestamp, combining public-availability timestamp, effective/as-of period, revision status, and staleness
- **Decision Obligation Source:** EVIDENCE-MODEL §5.1: "Historical evaluation must use information that was publicly available at the evaluation timestamp, not the latest revised value." ALPHA-MOMENTUM-V0-SPEC §2.2: "V0 data must be queryable at a given point in time"
- **Inherited Approved Semantics:** Historical evaluation must use publicly available data at the evaluation timestamp. V0 data must be point-in-time queryable. The operational visibility function combining all timestamp dimensions is not supplied
- **Rule Content Authority:** Founder-provided rule — this decision
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (V0 Simple Visibility Function):**
  - **จุดประสงค์:** เวลาเราถามว่า "ณ วันที่ 30 มิ.ย. 2025 ระบบรู้อะไรบ้างเกี่ยวกับหุ้น NVDA?" — ระบบต้องตอบโดยใช้ข้อมูลที่โลกรู้แล้ว ณ วันนั้นเท่านั้น ไม่ใช้ข้อมูลที่ออกมาทีหลัง
  - **กฎการมองเห็นของ V0 — เรียบง่ายที่สุด:**
    - ข้อมูลจะถูกมองเห็นก็ต่อเมื่อ: **วันที่ข้อมูลเผยแพร่สู่สาธารณะ ≤ วันที่เราประเมิน**
    - เขียนเป็นสูตรง่ายๆ: `pub_date <= eval_date` → มองเห็น, `pub_date > eval_date` → มองไม่เห็น
  - **สิ่งที่กฎนี้รวมอยู่แล้ว:**
    - งบ Q1/2025 ที่ประกาศ 15 เม.ย. → มองเห็นถ้า eval_date ≥ 15 เม.ย.
    - งบเดียวกันที่ถูกแก้ไข 1 มิ.ย. → version แรกมองเห็นวันที่ 15 เม.ย. - 31 พ.ค., version แก้ไขมองเห็นตั้งแต่วันที่ 1 มิ.ย.
    - ราคาหุ้นวันที่ 20 มิ.ย. → มองเห็นตั้งแต่วันที่ 20 มิ.ย. เป็นต้นไป (หรือ 21 มิ.ย. ถ้าเป็นข้อมูลสิ้นวัน)
  - **ข้อมูลเก่าไม่หาย — แค่ถูก mark:** ข้อมูลที่มี `freshness_status = stale` ยังมองเห็นอยู่ตามกฎ visibility ปกติ ความเก่า (staleness) เป็นป้ายบอกคุณภาพ ไม่ใช่ตัวซ่อนข้อมูล
  - **เลื่อนไป V0.5:** visibility function ที่ซับซ้อนขึ้น — เช่น แยกตามประเภทข้อมูล (price data อาจ delay 1 วัน, filing data อาจ delay ตามเวลาที่ SEC ประมวลผล), การจัดการกรณีข้อมูลมาจาก timezone ต่างกัน, การจัดการกรณีข้อมูลมีทั้ง pub_date และ effective_date ที่เหลื่อมกัน
- **Affected Artifact(s):** DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md; Point-in-time evaluation engine; Pipeline stage outputs at historical dates
- **Decision Category:** Formula, Period
- **Materiality:** Material — determines correctness of every historical assessment; directly affects AC-7 and AC-8
- **Status:** Approved
- **Resolution:** RESOLVED — V0: `pub_date <= eval_date`; staleness เป็นป้ายคุณภาพ ไม่ใช่ตัวซ่อน
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** Evidence records with all timestamp fields; revision linkages; staleness markers; evaluation timestamp
- **Required Output States:** ฟังก์ชัน visibility: รับ evaluation date → คืนชุดข้อมูลที่มองเห็นได้ (เฉพาะ records ที่ `pub_date <= eval_date`), ระบุ version ที่ถูกต้องตาม revision chain
- **Required Explainability:** รายการข้อมูลที่ถูกรวม/ไม่รวม, version ที่ใช้, และ rule version สำหรับทุกการ query ย้อนหลัง
- **Missing-Data Question:** ข้อมูลที่ missing pub_date → flag `Not Assessable` และไม่ถูกรวมในผลลัพธ์
- **Conflicting-Evidence Question:** กรณี pub_date หลัง eval_date แต่ effective_date ครอบคลุม eval_date (เช่น forecast ที่ย้อนมองอดีต) → ไม่มองเห็น (เราไม่ใช้ข้อมูลที่ยังไม่เกิด ณ เวลานั้น)
- **Point-in-Time Question:** slot นี้คือนิยามของ point-in-time visibility function เอง
- **Dependencies:** DS-407 (public-availability timestamp); DS-409 (effective period); DS-410 (revision handling); DS-401 (staleness)
- **Alternatives to Evaluate:** Evaluated by Founder — V0 simple visibility function เลือกเพื่อให้ตรงกับข้อมูลสังเคราะห์ที่เราควบคุมเอง
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-3C-CAPSTONE-v0.1
- **Verification Evidence:** Founder approved V0 simple `pub_date <= eval_date` visibility function in session

---

### Decision Slot: DS-412 — Data Confidence Scope Levels and Roll-Up Policy

- **Identifier:** DS-412
- **Topic:** What Data Confidence means at per-record, per-Candidate, per-Theme, and system-wide levels; whether and how confidence rolls up across levels. Consolidation of what were previously separate aggregation (DS-105) and scope-level (DS-114) decisions
- **Decision Obligation Source:** EVIDENCE-MODEL §9: "Data Confidence applies at multiple levels: individual evidence records, aggregated assessments, and overall system state." CANDIDATE-AND-QUEUE-MODEL §2.4: Data Confidence measures reliability of data underlying Candidate assessments
- **Inherited Approved Semantics:** Data Confidence applies at multiple levels. It is a separate axis from other quality dimensions. No roll-up method is supplied. "No roll-up" is a valid outcome
- **Rule Content Authority:** Founder-provided rule — this decision
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (No Roll-Up — Independent Per-Level Assessment):**
  - **ปัญหาที่ slot นี้แก้:** สมมติว่าเรามีข้อมูล 10 records เกี่ยวกับ NVDA — 8 records มี Data Confidence สูง, 2 records มีต่ำ ถ้าเรา "roll-up" (รวมคะแนน) เราอาจได้ค่าเฉลี่ยที่ดู OK แต่ซ่อนความจริงที่ว่า 2 records นั้นไม่น่าเชื่อถือ → เราอาจตัดสินใจผิดเพราะเห็นแต่ค่าเฉลี่ย
  - **การตัดสินใจ: ไม่ roll-up — แต่ละระดับประเมินแยกกันอิสระ**
  - **3 ระดับของ Data Confidence:**
    1. **ระดับ record เดี่ยว** — แต่ละ evidence record มี Data Confidence ของตัวเอง (มาจาก DS-401 ถึง DS-406: ความสด, ความครบถ้วน, ความน่าเชื่อถือของแหล่งที่มา, ความเป็นอิสระ, ความขัดแย้ง, ข้อมูลที่หายไป)
    2. **ระดับ Candidate** — เมื่อดู Candidate ตัวหนึ่ง (เช่น NVDA) Data Confidence ในระดับนี้จะแสดง "ภาพรวม" ของ evidence records ทั้งหมดที่โยงกับ Candidate นี้ — แต่ไม่ใช่ค่าเฉลี่ย! เป็นการแสดงผลว่า: มีกี่ records, แต่ละอันเชื่อถือได้ระดับไหน, มี conflict ไหม, มีอะไรขาดหาย — ให้ Founder เห็นภาพเอง
    3. **ระดับ Theme** — เหมือนระดับ Candidate แต่ขยายเป็นทุก Candidate ภายใต้ Theme นั้น
  - **ไม่มีสูตร roll-up:** ไม่มีสูตรคำนวณที่รวม DC จาก 10 records เป็นตัวเลขเดียว ไม่มี weighted average ไม่มี composite score — เพราะการยุบค่าจะซ่อนความแตกต่างที่สำคัญ (Constitution §10)
  - **วิธีแสดงผล:** แต่ละระดับแสดง DC dimensions (DS-401–DS-406) แยกกัน เช่น ระดับ Candidate: "Freshness: มี 3 records stale จาก 10, Completeness: 8/10 records ครบถ้วน, Reliability: 7 จากแหล่ง high, 2 จาก medium, 1 จาก low, Conflicts: พบ 1 conflict มูลค่า $2B, Missing: ขาด insider trading data"
  - **เลื่อนไป V0.5:** aggregate scoring methods (ถ้าต้องการในอนาคต), automated threshold-based warning systems, dynamic confidence-weighted adjustments — ทั้งหมดนี้ต้องมีข้อมูลจริงและความต้องการที่ชัดเจนก่อน
- **Affected Artifact(s):** DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md; Data Confidence assessment output; Candidate assessments; Theme Cards
- **Decision Category:** Formula, Threshold
- **Materiality:** Material — determines what Data Confidence means when presented alongside other quality dimensions
- **Status:** Approved
- **Resolution:** RESOLVED — ไม่ roll-up; 3 ระดับ (record / Candidate / Theme) อิสระ; แสดง DC dimensions แยกกัน
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** Per-record Data Confidence assessments; evidence-to-Candidate and evidence-to-Theme relationships
- **Required Output States:** การประเมิน Data Confidence อิสระในแต่ละระดับ. แต่ละระดับแสดง DC dimensions แยกเป็นรายข้อ — ไม่มีตัวเลขรวม.
- **Required Explainability:** มี evidence records ไหนบ้างที่ถูกนำมาพิจารณา, แต่ละอันมี DC level อะไร, วิธีการแสดงผล (แยกรายมิติ), และ rule version
- **Missing-Data Question:** ระดับที่ไม่มี evidence records เลย (เช่น Candidate ที่ยังไม่เคยถูกประเมิน) → แสดง "No Data" พร้อมเหตุผล
- **Conflicting-Evidence Question:** ระดับ Candidate ที่มีทั้ง records ที่ DC สูงและต่ำ → แสดงการกระจายตัวตามจริง ไม่ยุบรวม
- **Point-in-Time Question:** การประเมิน DC ทุกระดับใช้ evaluation timestamp เดียวกันกับการ run pipeline
- **Dependencies:** DS-401 through DS-406 (all dimension decisions — all resolved)
- **Alternatives to Evaluate:** Evaluated by Founder — no-roll-up เลือกเพื่อรักษาการแยกมิติตาม Constitution §10
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-3C-CAPSTONE-v0.1
- **Verification Evidence:** Founder approved no-roll-up independent per-level assessment in session

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

- All 12 active slots are Approved under AM-V0-WAVE-3A-TIMESTAMPS-v0.1, AM-V0-WAVE-3B-DIMENSIONS-v0.1, and AM-V0-WAVE-3C-CAPSTONE-v0.1. Data Confidence artifact: 12/12 complete.
- No slot proposes prohibited content
- Every slot carries Decision Obligation Source, Inherited Approved Semantics, Rule Content Authority, and Unresolved Operational Question
- DS-405 limits scope to data-layer detection and preservation; human-facing presentation belongs to Gate C
- No DS identifiers reused from old range
- References DS-513 (Rule Lifecycle) from Pipeline artifact for rule-version linkage
