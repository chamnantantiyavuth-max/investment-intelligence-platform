# QAD Evidence, Source & Canonical Truth Model

> **Contract:** M3-04 (M3 Domain Contract Set)
> **Status:** M3 FINAL DRAFT (CORRECTION COMPLETE — AWAITING INDEPENDENT RE-REVIEW)
> **Authority:** FD #130; EVIDENCE-DOCTRINE.md; Constitution §21 (Record-Keeping); Frozen Architecture (Provenance/Evidence layers); CIW Source Lineage (CAP-009 ABSORB)
> **Traceability:** EVIDENCE-DOCTRINE (Required Separations, Source Independence, Evidence Progression, Aging, Point-in-Time, Contradictions) · CAP-009 (CIW source lineage) · CAP-017 (REUSE) · CONSTITUTION-§21 · DISCOVERY-REQ-B7 (Data Architecture) · FD #58 (Point-in-Time Rule) · FD #94 (Publication Firewall) · NEW_M3_DERIVATION (L1-L10 hierarchy, canonical layers, knowledge states)

---

## 1. Source Hierarchy (L1–L10)

All evidence in the QAD system is classified by source type. **L1–L9 are admissible source classes. Material evidentiary sufficiency is claim-specific and depends on relevance, directness, source independence, sampling quality, contradiction status, and corroboration. L10 is lead-only and can never be sole support for a material conclusion.**

| Level | Category | Examples | Typical Evidentiary Role |
|-------|----------|---------|--------------------------|
| **L1** | Corporate Primary | 10-K, 10-Q, 8-K, proxy, earnings transcript, investor day, SEC filings, corporate website (official financial data) | Foundational for financial analysis |
| **L2** | Ecosystem Primary | Customer contracts, supplier agreements, competitor cross-references, partnership disclosures | High-value corroboration |
| **L3** | Regulatory / Government | SEC filings by others, antitrust, FDA, EPA, CFTC, Fed, BLS, Census, EIA, international equivalents | Authoritative third-party data |
| **L4** | Industry / Trade | Industry associations, trade publications, independent industry research (LBMA, IEA, EIA, SIA, etc.) | Context and industry baseline |
| **L5** | Customer Reality | Customer reviews, user data, app store rankings, channel checks, customer surveys (lawful, non-MNPI) | Ground-truth signal; requires aggregation |
| **L6** | Labor / Organization | Employee reviews (Glassdoor), LinkedIn data, organizational structure, hiring trends, union disclosures | Organizational health signal |
| **L7** | Digital Observable | Patent filings, scientific publications, clinical trials, satellite imagery, web traffic, pricing data | Quantitative/verifiable signal |
| **L8** | Physical / Channel | Store visits, product inspections, channel checks, distribution observations, trade show intelligence | Direct observation |
| **L9** | Expert / Interview | Industry expert interviews, former employee interviews (must be lawful, non-confidential, non-MNPI) | Contextual insight; requires independence verification |
| **L10** | Lead-Only / Social | Social media, forums (Reddit, X/Twitter, StockTwits), anonymous blogs, unverified rumors, chat boards | **Lead-only. Cannot independently support a material conclusion.** |

### Source Weighting Rules

- **L1** sources are the foundation of any QAD case. A case with no L1 source engagement is insufficient.
- Sources at the same level from the same entity are NOT independent (e.g., 10-K and 8-K from same company are both L1 but not independent of each other).
- **Syndicated copies do not count as independent confirmation** (EVIDENCE-DOCTRINE).
- Contradiction between two L1 sources (e.g., company claim vs SEC filing) is a material finding that must be resolved.
- **L10** can provide leads/discovery hints but cannot be the sole support for any analytical conclusion, including impairment diagnosis, quality assessment, or valuation.

---

## 2. Canonical Layers

The QAD evidence system has five canonical layers:

```text
1. RAW SOURCE ARCHIVE
   ↓ ingestion, format-normalization
2. CANONICAL EVIDENCE REGISTRY
   ↓ curation, validation, cross-referencing
3. CLAIMS / CONTRADICTIONS / CALCULATIONS
   ↓ analytical processing
4. ANALYTICAL STATE
   ↓ synthesis
5. PUBLICATION / FOUNDER PRESENTATION
```

### Layer 1 — Raw Source Archive

- Immutable store of original source documents
- Content is never edited in place (EVIDENCE-DOCTRINE: tombstone + reason + authorizer + timestamp required for removal)
- Every source document has: source_id, source_type (L1-L10), retrieval_date, source_url/identifier, content_hash
- Point-in-Time: retrieval timestamp is the authoritative as-of for the source

### Layer 2 — Canonical Evidence Registry

- Curated, validated evidence objects admitted from raw sources
- Each entry has: evidence_id, source_id, evidence_type (FACT/CLAIM/INFERENCE/HYPOTHESIS), content, extractor (AI/human), validation_status, PIT, admitting_role
- Admission requires validation against original source
- NotebookLM/Deep Research output must be validated against original source before admission

### Layer 3 — Claims / Contradictions / Calculations

- Structured analytical layer: extracted claims, identified contradictions, derived calculations
- Every calculation has full lineage (formula, inputs, source references)
- Contradictions are preserved and never averaged away
- Each entry has: derived_id, evidence_ids (inputs), formula/rule, result, timestamp, calculator_role

### Layer 4 — Analytical State

- State machine per case: quality assessment, impairment diagnosis, valuation
- Each state transition records: previous_state, new_state, trigger_evidence, analyst, timestamp
- State is canonical; alternative interpretations are preserved alongside it

### Layer 5 — Publication

- Thai long-form articles on `/library`
- Publication is journalism, NOT canonical truth
- A published report may be updated via §23.9 corrections (preserve original + correction record)
- Publication decisions are Founder-gated

---

## 3. Evidence Object Taxonomy

Every evidence object in the Canonical Evidence Registry is one of:

| Type | Definition | Example | Validation Requirement |
|------|------------|---------|----------------------|
| **FACT** | Verifiable, objective piece of information directly from a source | "Revenue in FY2025 was $12.3B per 10-K p.42" | Must be traceable to original source at exact location |
| **CLAIM** | Assertion by an entity (company, management, analyst, regulator) that may be true or false | "Management claims market share increased to 35%" | Source must be identified; truth not asserted by system |
| **INFERENCE** | Conclusion drawn from facts/claims by analyst or AI, labeled with confidence | "Based on revenue growth + margin stability, pricing power appears intact. Confidence: PROBABLE" | Must be labeled as inference; chain of reasoning must be explicit |
| **HYPOTHESIS** | Testable proposition about the entity, subject to falsification | "The impairment is temporary because the demand driver is cyclical, not structural" | Must have falsification criteria; originator identified |

### Evidence Status

| Status | Meaning |
|--------|---------|
| RAW | Extracted but not validated |
| VALIDATED | Cross-referenced against original source |
| CONTRADICTED | Another evidence object contradicts this one |
| SUPERSEDED | Replaced by newer evidence (newer as-of date) |
| RETRACTED | Admitted in error; retraction recorded |
| DISPUTED | Status disputed by analyst/Red Team; under review |

---

## 4. NotebookLM / Deep Research Boundary

| Role | Permitted | Forbidden |
|------|-----------|-----------|
| **NotebookLM** | Research discovery / interrogation layer; cross-source synthesis; question-based exploration; identified material evidence (with source pointers) | ✅ |
| **NotebookLM** | Canonical database; final analyst; final auditor; final truth authority | ❌ |
| **Deep Research** | Deep corpus investigation; structured source discovery; multi-source synthesis for evidence gaps | ✅ |
| **Deep Research** | Primary decision-maker on material findings without source validation | ❌ |

**Protocol:** Material finding discovered through NotebookLM or another AI synthesis must be validated against original source before canonical admission.

**Provider Abstraction:**
- `deep_research_provider` — abstract interface for deep research (Gemini Deep Research, etc.)
- `research_corpus_provider` — abstract interface for research corpus (NotebookLM, etc.)
- Do not hardwire consumer UI/browser hacks into canonical domain contracts

---

## 5. Knowledge States

Beyond individual evidence objects, the system maintains cross-case knowledge:

| State | Definition | Admission Criteria |
|-------|------------|-------------------|
| **Research Finding** | Observation from a single case | One case |
| **Candidate Lesson** | Tentative generalization from one or more cases | Two or more cases with consistent pattern |
| **Cross-Case Validation** | Pattern tested across multiple cases with consistent results | 3+ independent cases or systematic review |
| **Independent Review** | Reviewed by independent role (not original researcher) | Review completed |
| **APPROVED KNOWLEDGE** | Validated, reviewed, and approved as institutional knowledge | Cross-case + independent review + Chief Underwriter approval |
| **Industry Playbook** | Structured knowledge about an industry: what to measure, patterns, red flags, key ratios | Multiple cases in same industry + systematic distillation |

A single research case does not automatically become institutional knowledge.

---

## 6. Contradiction Management (EVIDENCE-DOCTRINE)

- Contradicting evidence remains visible and is never averaged away merely for presentation simplicity.
- When two pieces of evidence contradict, both are preserved with explicit notation.
- Contradiction resolution requires additional evidence, not suppression.
- Red Team findings that contradict the primary thesis are preserved as material findings, not footnotes.
- Every contradiction has a status: `UNRESOLVED / PARTIALLY_RESOLVED / RESOLVED_WITH_EVIDENCE`

---

## 7. Evidence Aging (EVIDENCE-DOCTRINE)

- Evidence is retained. Current relevance changes.
- Raw evidence must not be silently edited in place.
- Unsupported narrative or intention with no measurable action within three years becomes stale by default (unless a documented long-cycle exception is approved).
- PIT discipline: all evidence carries its as-of date; evidence relevance by as-of, not by when it was entered.

---

## 8. Source Independence

- **Syndicated copies do not count as independent confirmation.**
- Multiple sources at the same level from the same entity = one data point.
- Independent confirmation requires sources from different entities or levels.
- Evidence quality improves with independent source triangulation, not with more copies of the same source.

<!-- 2026-08-19 12:15 UTC+7 -->