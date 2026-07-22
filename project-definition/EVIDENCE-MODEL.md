# Evidence Model

Status: Approved Domain Specification
Version: 0.1
Owner: Founder
Authority: Approved Domain Specification subordinate to the Constitution and Founder's Decisions
Derived from: Investment Intelligence Platform Constitution v0.3
Approval: PD-v0.1-FOUNDING-DOMAIN-SPECIFICATIONS

## 1. Evidence as a Foundational Domain Object

Evidence is a foundational domain object (DNA-002). Every hypothesis, theme, candidate assessment, decision, and lesson must remain traceable to its supporting and contradicting evidence.

Not every record in the platform is evidence. The system distinguishes between evidence/observation records and epistemic/governance records that are products of reasoning about evidence.

## 2. Information and Record Type Taxonomy

The system handles multiple categories of information. They are not all evidence. They are not interchangeable.

### 2.1 Evidence and Observation Records

Records that capture or represent observable phenomena, source content, or derived measurements. These may serve as supporting or contradicting evidence.

| # | Type | Description | Produced By |
|---|---|---|---|
| 1 | **Raw Source Record** | The unmodified source document or data as ingested | Ingestion pipeline |
| 2 | **Observed Fact** | A directly observable, verifiable data point confirmed through source-grounded verification or direct measurement | Extraction with verification |
| 3 | **Claim** | A statement that may remain unverified. Subtypes: **Source Claim** (originating from source content), **AI Extraction** (structured data extracted by AI from unstructured sources), **AI Classification** (a category or label assigned by AI) | Source content, AI pipeline |
| 4 | **Normalized Fact** | A fact transformed to a standard representation | Normalization pipeline |
| 5 | **Derived Metric** | A computed value from one or more facts | Feature computation |
| 6 | **Statistical Signal** | A statistically identified pattern or anomaly | Signal detection |
| 7 | **Founder Knowledge Record** | Knowledge, insight, pattern recognition, or investment reasoning explicitly recorded by the Founder. Sources include: Obsidian vault notes, trading journals, meeting notes, investment diaries, post-trade reflections, and strategy documents. Unlike external source records, Founder Knowledge Records carry the Founder's own interpretation, priorities, and philosophy. | Founder-authored content ingestion |

**AI-derived records:** AI Extraction and AI Classification are explicit subtypes of Claim, not Observed Facts. Their lineage must record model, version, prompt version, input references, confidence, and review status (per AI Governance operational file).

- Human review may mark an AI Extraction or AI Classification as **reviewed** or **accepted**.
- Human review alone does not automatically convert an AI-derived record into an Observed Fact. Promotion to Observed Fact requires direct source-grounded verification or independent measurement.
- AI Classification normally remains a Classification even when accepted — its epistemic status does not change.
- Normalization changes representation (e.g., units, format), not epistemic status. A normalized Claim remains a Claim; a normalized Observed Fact remains an Observed Fact.

### 2.2 Epistemic and Governance Records

Records that represent interpretations, judgments, decisions, or learned conclusions. These are **not evidence** — they are products of reasoning about evidence. They reference evidence but are not themselves evidence.

| # | Type | Description | Produced By |
|---|---|---|---|
| 7 | **Hypothesis** | A proposed explanation linking observations to a theme or driver | AI or human |
| 8 | **Human Judgment** | An assessment, interpretation, or evaluation by the Founder | Human review |
| 9 | **Approved Decision** | A formal decision by the Founder (theme approval, override, etc.) | Human authority |
| 10 | **Outcome** | The realized result of a decision or tracked hypothesis | Time + measurement |
| 11 | **Lesson** | A reviewed and approved learning from outcomes | Human-approved postmortem |

### 2.3 Usage Rules

- Only Evidence and Observation Records (§2.1) may serve as supporting or contradicting evidence for a Theme, Candidate, or Hypothesis.
- Epistemic and Governance Records (§2.2) reference evidence but are not themselves evidence.
- A Theme Card's "supporting evidence" and "contradicting evidence" sections draw from §2.1 only.
- Hypotheses, Judgments, Decisions, Outcomes, and Lessons carry their own governance and versioning requirements.

## 3. Source Independence

Multiple links copied from one source are **not** independent evidence (Constitution §8).

Syndicated copies, republications, and aggregated feeds that derive from the same originating source do not count as independent confirmation.

Source independence assessment requires:

- Originating source identification
- Derivation chain (who republished what from whom)
- Independence classification: independent, derived, syndicated, unknown

## 4. Evidence Progression

No evidence type dominates universally. Different themes may follow different valid progressions.

Typical progression (Constitution §9):

```
Structural Signal
  → Operational Action
    → Fundamental Confirmation
      → Market Confirmation
        → Broad Adoption / Crowding
```

A theme at the Structural Signal stage with strong, diverse structural evidence may be higher quality than a theme at Market Confirmation driven by a single, narrow signal. Progression stage and evidence quality are separate assessments.

## 5. Provenance

Every evidence record must carry provenance metadata:

| Field | Description |
|---|---|
| Source identifier | Which source registry entry produced this record |
| Ingestion timestamp | When the record was ingested into the platform |
| Publication / public-availability timestamp | When the information was first publicly available (may differ from ingestion or observation) |
| Effective / as-of period | The date or date range the information describes (e.g., a quarterly report covers Q1 2025) |
| Observation timestamp | When the fact or event occurred (may differ from publication) |
| Originating URL or reference | Where the content was retrieved from |
| Revision or vintage | Version, revision number, or vintage identifier from the source |
| Supersedes / superseded-by | References to prior or subsequent versions of the same record |
| Content hash or source version | A checksum or version identifier enabling integrity verification |
| Licensing / retention classification | Permitted use, retention period, and removal requirements |
| Timezone | Timezone of timestamps when material to interpretation |
| Extraction method | How the record was produced (manual, automated, AI extraction, etc.) |
| Extraction version | Version of the extraction method or pipeline |
| Raw record reference | Link to the immutable raw source record |

### 5.1 Point-in-Time Evaluation

Historical evaluation must use information that was publicly available at the evaluation timestamp, not the latest revised value.

When a source issues a revision (e.g., restated earnings, corrected filing), the platform must:

- Preserve the original record with its original publication timestamp.
- Record the revision as a new record with supersedes/superseded-by linkage.
- Ensure that any historical evaluation referencing the original timestamp sees only the original record (or both, with provenance clarity).
- Not silently replace or backfill historical data with revised values.

AI-extracted and AI-classified records additionally require (AI Governance operational file):

- Model identifier and version
- Workflow or prompt version
- Input evidence references
- Confidence score
- Review status

## 6. Aging and Staleness

Evidence is retained. Current relevance changes.

### 6.1 Relevance Decay

Evidence relevance may decay over time. The model must support:

- Freshness as a dimension of Data Confidence
- Aging signals that reduce current relevance without deleting history
- Explicit staleness markers that do not remove the record

### 6.2 Three-Year Narrative Default

Unsupported narrative or intention-based evidence that has no measurable action within three years becomes **stale by default** (Constitution §8).

A documented long-cycle exception may override the default if:

- The exception is explicitly approved
- Milestones and review dates are specified
- The long-cycle rationale is recorded

### 6.3 Controlled Removal and Tombstoning

Raw evidence must not be silently edited in place. When legal, privacy, licensing, security, corruption, or retention requirements demand removal, the content may be quarantined or deleted through a controlled process that records (Constitution §8):

| Tombstone Field | Description |
|---|---|
| Record identifier | What was removed or quarantined |
| Reason | Legal, privacy, licensing, security, corruption, or retention basis |
| Authorizer | Who authorized the removal |
| Timestamp | When the removal occurred |
| Affected lineage | What downstream records depend on the removed evidence |
| Reprocessing requirements | What must be invalidated, recalculated, or reviewed |

The historical fact that a record existed may remain while prohibited content is removed.

## 7. Contradicting Evidence

Contradicting evidence remains visible and is never averaged away for presentation simplicity (Evidence Doctrine).

The model must support:

- Linking contradicting evidence to the same hypothesis, theme, or candidate as supporting evidence
- Preserving contradictions in Theme Cards, research views, and exports
- Preventing score compression that silently absorbs contradictions

## 8. Relationship to Themes and Candidates

Evidence links to Themes and Candidates through relationships:

- **Evidence → Theme:** Evidence supports, contradicts, or is missing for a Theme's thesis.
- **Evidence → Candidate:** Evidence supports or contradicts a Candidate's role, leadership, or quality within a Theme.
- **Evidence → Candidate–Theme relationship:** Evidence specific to why this Candidate matters for this Theme.

The same Evidence record may link to multiple Themes and Candidates with different relationship types.

## 9. Data Confidence

Data Confidence is a separate axis from Theme Quality, Candidate Quality, and Entry Readiness (Constitution §10, §13).

It assesses the reliability of the data underlying any assessment. Dimensions include:

| Dimension | Description |
|---|---|
| Freshness | How recent the data is relative to expectations |
| Completeness | Whether expected fields, periods, or entities are present |
| Reliability | Source track record, extraction accuracy, known issues |
| Conflicts | Whether independent sources disagree materially |
| Missing data | What expected data is absent |

Data Confidence applies at multiple levels: individual evidence records, aggregated assessments, and overall system state. Exact measurement is deferred.

## 10. Version Boundaries for Evidence Capabilities

| Capability | V0 | V0.5 | V1 | V1.5 | Later |
|---|---|---|---|---|---|---|
| Evidence and observation record model | ✅ | ✅ | ✅ | ✅ | ✅ |
| Epistemic and governance record model | ✅ | ✅ | ✅ | ✅ | ✅ |
| Source registry (synthetic sources only) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Founder Knowledge Record ingestion (Obsidian, journals, diaries) | — | — | ✅ | ✅ | ✅ |
| Raw evidence preservation and immutability | ✅ | ✅ | ✅ | ✅ | ✅ |
| Tombstoning process | ✅ | ✅ | ✅ | ✅ | ✅ |
| Provenance metadata (full set) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Point-in-time evaluation | — | ✅ | ✅ | ✅ | ✅ |
| Real source ingestion and reconciliation | — | ✅ | ✅ | ✅ | ✅ |
| Data quality monitoring | — | ✅ | ✅ | ✅ | ✅ |
| AI extraction and classification lineage | — | — | — | ✅ | ✅ |
