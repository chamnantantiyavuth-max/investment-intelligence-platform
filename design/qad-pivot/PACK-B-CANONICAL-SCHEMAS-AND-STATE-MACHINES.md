# Pack B — Canonical Schemas & State Machine Contracts

> **Status:** Design artifact — not approved. Implementation-grade schema contracts.
> **Includes:** NotebookLM Research Request/Result contracts, Discovery Provenance, Original-Source Validation, Notebook↔Registry boundary.

---

## Part 1: ID Scheme & Versioning

### ID Convention

| Object | ID Pattern | Example |
|--------|-----------|---------|
| Case | `QAD-YYYY-NNNN` | `QAD-2026-0001` |
| Research Run | `RR-{case_id}-{version}-{date}` | `RR-QAD-2026-0001-v1-20260816` |
| Source | `SRC-{type}-{hash8}` | `SRC-10K-a1b2c3d4` |
| Evidence | `EVI-{hash8}` | `EVI-f9e8d7c6` |
| Claim | `CLM-{case_id}-{NNNN}` | `CLM-QAD-2026-0001-0001` |
| Hypothesis | `HYP-{case_id}-{A/B/C}` | `HYP-QAD-2026-0001-A` |
| Challenge | `CHA-{case_id}-{NNNN}` | `CHA-QAD-2026-0001-0001` |
| Audit | `AUD-{case_id}-{round}` | `AUD-QAD-2026-0001-01` |
| Monitoring Event | `MON-{case_id}-{NNNN}` | `MON-QAD-2026-0001-0001` |
| Notebook Request | `NBR-{case_id}-{NNNN}` | `NBR-QAD-2026-0001-0001` |

### Versioning Rules

- Every object has `id`, `version` (monotonic integer starting 1), `created_at`, `updated_at`
- Case version increments on any material state change
- Evidence/Claim/Hypothesis version increments on correction (old version preserved per §23.9)
- Research Run version is immutable (append-only)
- Lineage: every object tracks `previous_version_id` and `superseded_by_id`

---

## Part 2: Case State Machine

```
                    ┌──────────────────────────────────────┐
                    │           QUALITY DISCOVERY           │
                    │  (Open system → Hard Gates check)     │
                    └──────────────┬───────────────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │       CANDIDATE IDENTIFIED    │
                    │  AUTO_RESEARCH_NOW / WATCH    │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │       RESEARCH CHARTER        │
                    │  (Approved by Chief Underwriter)│
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │       EVIDENCE BUILDING       │
                    │  Core Desk + NotebookLM +     │
                    │  Scuttlebutt (as needed)      │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │        ANALYSIS PHASE          │
                    │  Business Quality + Industry + │
                    │  Financial + Management        │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │    IMPAIRMENT DIAGNOSIS        │
                    │  Temporary/Mostly/Mixed/       │
                    │  Structural/Unresolved         │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │    NORMALIZATION & VALUATION   │
                    │  Normalized Economics + DCF +  │
                    │  Reverse DCF + Scenarios       │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │     RED TEAM CHALLENGE         │
                    │  (Independent, Tier D)         │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │          ADJUDICATION          │
                    │  Accepted/Partially/Rejected/  │
                    │  Unresolved                    │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │            AUDIT               │
                    │  (Independent, Tier D)         │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │              │                │
                    ▼              ▼                ▼
              PASS             MINORS          MAJOR/BLOCK
                    │              │                │
                    ▼              ▼                ▼
           CHIEF UNDERWRITER    CORRECT      RETURN TO EVIDENCE
                    │              │                │
                    ▼              ▼                │
           FOUNDER-READY ←─────────────────────────┘
                    │
                    ▼
              FOUNDER ENDORSED
           (explicit Founder action only)
```

### Case States

| State | Description | Transitions To |
|-------|-------------|----------------|
| `CANDIDATE` | Identified by Discovery, awaiting Charter | `CHARTED`, `WATCH_FOR_PRICE`, `WATCH_FOR_EVIDENCE`, `DATA_LIMITED_WATCH`, `REJECTED` |
| `CHARTED` | Research Charter approved | `EVIDENCE_BUILDING` |
| `EVIDENCE_BUILDING` | Sources being collected | `ANALYSIS`, `BLOCKED` (if source failure), `TERMINATED` (if quality thesis fails) |
| `ANALYSIS` | Business/Industry/Financial analysis | `IMPAIRMENT_DIAGNOSIS`, `BLOCKED`, `TERMINATED` |
| `IMPAIRMENT_DIAGNOSIS` | Damage classification | `NORMALIZATION`, `TERMINATED` (if clear structural) |
| `NORMALIZATION` | Economics + Valuation | `RED_TEAM`, `TERMINATED` |
| `RED_TEAM` | Independent challenge | `ADJUDICATION` |
| `ADJUDICATION` | Challenge resolved | `AUDIT`, `RED_TEAM` (if challenge accepted → rework) |
| `AUDIT` | Integrity check | `UNDERWRITING`, `CORRECTION`, `BLOCKED` |
| `CORRECTION` | Audit findings fixed | `AUDIT` (re-audit) |
| `UNDERWRITING` | Chief Underwriter synthesis | `FOUNDER_READY` |
| `FOUNDER_READY` | Report ready for Founder review | `FOUNDER_REVIEW`, `TERMINATED` |
| `FOUNDER_REVIEW` | Founder actively reviewing | `FOUNDER_ENDORSED`, `DISMISSED`, `EVIDENCE_BUILDING` (rework) |
| `FOUNDER_ENDORSED` | Founder explicitly approved | `MONITORING` |
| `MONITORING` | Thesis-aware monitoring | `RECOVERY_CONFIRMING`, `ON_TRACK`, `UNCERTAIN`, `WEAKENING`, `BROKEN`, `ARCHIVED` |
| `BROKEN` | Thesis break condition triggered | `RE_OPENED` (new charter), `ARCHIVED` |
| `REJECTED` | Hard gates failure | `ARCHIVED` |
| `TERMINATED` | Research stopped before full completion | `ARCHIVED` |
| `ARCHIVED` | Final state | — |

---

## Part 3: Core Schema Contracts

### Case Schema

```json
{
  "case_id": "QAD-YYYY-NNNN",
  "version": 1,
  "state": "CANDIDATE",
  "company": {
    "name": "string",
    "ticker": "string",
    "cik": "string (10-digit)",
    "sector": "string",
    "industry": "string"
  },
  "as_of_date": "YYYY-MM-DD",
  "charter": {
    "research_objective": "string",
    "market_fears": "string",
    "temporary_hypothesis": "string",
    "structural_hypothesis": "string",
    "mixed_hypothesis": "string",
    "false_quality_hypothesis": "string",
    "unattractive_valuation_hypothesis": "string",
    "primary_questions": ["string"],
    "decision_critical_unknowns": ["string"]
  },
  "research_runs": ["RR-..."],
  "impairment": null,
  "valuations": [],
  "red_team": null,
  "audit": null,
  "underwriting": null,
  "founder_review": null,
  "monitoring": [],
  "created_at": "ISO8601",
  "updated_at": "ISO8601",
  "lineage": {
    "previous_version": null,
    "superseded_by": null
  }
}
```

### Source Schema

```json
{
  "source_id": "SRC-{type}-{hash8}",
  "source_class": "S1|S2|S3|S4|S5|S6",
  "source_type": "10-K|10-Q|8-K|DEF14A|SC13D|13F-HR|TRANSCRIPT|PRESS|WEBSITE|SOCIAL|OTHER",
  "title": "string",
  "url": "string (optional)",
  "accession": "string (SEC)",
  "publication_date": "YYYY-MM-DD",
  "retrieval_date": "YYYY-MM-DD",
  "effective_period": {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"},
  "hash": "string (SHA-256)",
  "retrieval_status": "SUCCESS|FAILED|NOT_FOUND|RATE_LIMITED|BLOCKED",
  "discovery_origin": "SCANNER|RADAR|NOTEBOOKLM|MANUAL|CROSS_REFERENCE",
  "license": "PUBLIC_DOMAIN|EDGAR|PAID|OTHER",
  "point_in_time_validated": true,
  "notebooklm_id": "string (optional)",
  "notebooklm_ingested_at": "ISO8601 (optional)"
}
```

### Evidence Schema

```json
{
  "evidence_id": "EVI-{hash8}",
  "original_source": "SRC-...",
  "discovery_origin": "string",
  "source_class": "S1|S2|S3|S4|S5|S6",
  "publication_date": "YYYY-MM-DD",
  "retrieval_date": "YYYY-MM-DD",
  "point_in_time_status": "AS_OF_VALID|STALE|SUPERSEDED",
  "stakeholder": "MANAGEMENT|CUSTOMER|COMPETITOR|SUPPLIER|REGULATOR|ANALYST|MEDIA|OTHER",
  "relevant_research_question": "string",
  "relevant_claim_id": "CLM-...",
  "source_excerpt": "string",
  "analyst_interpretation": "string",
  "hypothesis_supported": "HYP-...",
  "hypothesis_contradicted": "HYP-...",
  "independence": "INDEPENDENT|CORROBORATED|SINGLE_SOURCE",
  "freshness": "CURRENT|ACCEPTABLE|STALE|EXPIRED",
  "materiality": "HIGH|MEDIUM|LOW",
  "verification_status": "VERIFIED|PARTIALLY_VERIFIED|UNVERIFIED|CONTRADICTED"
}
```

### Claim Schema

```json
{
  "claim_id": "CLM-{case_id}-{NNNN}",
  "version": 1,
  "claim_type": "FACT|MANAGEMENT_CLAIM|EXTERNAL_CLAIM|ANALYTICAL_INFERENCE|HYPOTHESIS|FORECAST",
  "statement": "string",
  "supporting_evidence": ["EVI-..."],
  "contradicting_evidence": ["EVI-..."],
  "alternative_explanations": ["string"],
  "important_unknowns": ["string"],
  "support_state": "STRONGLY_SUPPORTED|MODERATELY_SUPPORTED|BALANCED_UNRESOLVED|MODERATELY_CONTRADICTED|STRONGLY_CONTRADICTED",
  "what_would_change": "string",
  "created_by": "role_id",
  "created_at": "ISO8601",
  "lineage": {"previous_version": null, "superseded_by": null}
}
```

### Hypothesis Schema

```json
{
  "hypothesis_id": "HYP-{case_id}-{suffix}",
  "version": 1,
  "hypothesis_type": "TEMPORARY|STRUCTURAL|MIXED|FALSE_QUALITY|UNATTRACTIVE_VALUATION|UNRESOLVED",
  "statement": "string",
  "supporting_claims": ["CLM-..."],
  "contradicting_claims": ["CLM-..."],
  "key_assumptions": ["string"],
  "falsification_conditions": ["string"],
  "current_confidence": "HIGH|MEDIUM|LOW|INSUFFICIENT_EVIDENCE",
  "created_by": "role_id",
  "created_at": "ISO8601"
}
```

### Financial Fact Schema

```json
{
  "fact_id": "FIN-{case_id}-{NNNN}",
  "version": 1,
  "fact_type": "REVENUE|COGS|GROSS_PROFIT|SG&A|R&D|EBIT|NET_INCOME|OCF|CAPEX|FCF|ROIC|OTHER",
  "value": number,
  "currency": "USD",
  "unit": "MILLIONS|BILLIONS|RATIO|PERCENTAGE",
  "period": {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"},
  "source": "SRC-...",
  "calculation": {
    "formula": "string (e.g., revenue - cogs)",
    "inputs": ["FIN-...", "FIN-..."],
    "version": 1
  },
  "eps_epistemic_label": "GAAP|NON_GAAP|ADJUSTED|PROFORMA|MANAGEMENT_DEFINED",
  "point_in_time_validated": true,
  "normalized_value": null,
  "normalization_rationale": null
}
```

### Impairment Diagnosis Schema

```json
{
  "impairment_id": "IMP-{case_id}-{version}",
  "classification": "TEMPORARY|MOSTLY_TEMPORARY|MIXED|STRUCTURAL|UNRESOLVED",
  "dislocation": {
    "what": "string",
    "when": "ISO8601",
    "where": "COMPANY|SEGMENT|GEOGRAPHY|INDUSTRY",
    "by_how_much": "string (quantified)",
    "management_said": "string",
    "competitors_experienced": "string",
    "market_repriced": "string"
  },
  "causal_chain": {
    "peer_test": "string",
    "market_share_test": "string",
    "customer_behavior_test": "string",
    "moat_mechanism_test": "string",
    "capital_cycle_test": "string",
    "reversibility_test": "string"
  },
  "recovery_mechanism": {
    "root_cause": "string",
    "mechanism": "string",
    "expected_sequence": ["string"],
    "leading_indicators": ["string"],
    "expected_horizon": "string",
    "balance_sheet_runway": "string",
    "failure_condition": "string"
  },
  "permanent_damage": {
    "earning_power": "string",
    "moat": "string",
    "refinancing": "string",
    "dilution": "string",
    "balance_sheet": "string",
    "technology": "string",
    "regulation": "string",
    "industry_economics": "string"
  },
  "confidence": "HIGH|MEDIUM|LOW|INSUFFICIENT_EVIDENCE",
  "evidence_basis": ["EVI-..."],
  "created_by": "role_8",
  "created_at": "ISO8601"
}
```

### Valuation Schema

```json
{
  "valuation_id": "VAL-{case_id}-{version}",
  "method": "DCF|DISCOUNTED_OWNER_EARNINGS|EPV|SOTP|NORMALIZED_EARNINGS|ASSET_VALUE|PRIVATE_OWNER|COMPARABLE",
  "method_rationale": "string",
  "scenarios": {
    "no_recovery": {"value": number, "assumptions": ["string"]},
    "partial_recovery": {"value": number, "assumptions": ["string"]},
    "normalization": {"value": number, "assumptions": ["string"]},
    "quality_compounding": {"value": number, "assumptions": ["string"]}
  },
  "reverse_dcf": {
    "market_price": number,
    "implied_revenue_growth": number,
    "implied_normalized_margin": number,
    "implied_roic": number,
    "implied_reinvestment": number,
    "implied_competitive_fade": number,
    "implied_terminal_economics": "string",
    "evidence_supported_growth": number,
    "growth_gap": number,
    "evidence_supported_margin": number,
    "margin_gap": number
  },
  "economic_vs_price_damage": {
    "price_damage_percent": number,
    "current_economic_damage_percent": number,
    "permanent_economic_damage_percent": number,
    "market_implied_permanent_damage": number,
    "moat_trend": "WIDENING|STABLE|NARROWING|UNRESOLVED",
    "impairment_state": "string"
  },
  "every_input": [
    {"name": "string", "value": "any", "source": "SRC-...", "as_of": "YYYY-MM-DD", "epistemic_label": "string", "sensitivity": "HIGH|MEDIUM|LOW"}
  ],
  "deterministic_code_version": "string",
  "created_by": "role_9",
  "created_at": "ISO8601"
}
```

### Challenge Schema (Red Team output)

```json
{
  "challenge_id": "CHA-{case_id}-{NNNN}",
  "target_element": "MOAT|QUALITY|IMPAIRMENT|RECOVERY|NORMALIZED|VALUATION|MANAGEMENT",
  "thesis_component": "string",
  "attack": "string",
  "counter_evidence": ["EVI-..."],
  "strength": "STRONG|MODERATE|WEAK",
  "recommended_adjudication": "ACCEPTED|PARTIALLY_ACCEPTED|REJECTED_WITH_EVIDENCE|UNRESOLVED",
  "adjudication": {
    "result": "ACCEPTED|PARTIALLY_ACCEPTED|REJECTED_WITH_EVIDENCE|UNRESOLVED",
    "rationale": "string",
    "evidence": ["EVI-..."],
    "adjudicated_by": "role_1",
    "adjudicated_at": "ISO8601"
  },
  "created_by": "role_10",
  "created_at": "ISO8601"
}
```

### Audit Schema

```json
{
  "audit_id": "AUD-{case_id}-{round}",
  "round": 1,
  "findings": [
    {
      "finding_id": "F-{NN}",
      "severity": "MAJOR|MINOR|INFO",
      "category": "SOURCE|CITATION|CALCULATION|PIT|CONTRADICTION|NOTEBOOKLM|SELF_REVIEW|OTHER",
      "description": "string",
      "evidence": {"expected": "string", "found": "string"},
      "required_correction": "string",
      "re_auth_required": true
    }
  ],
  "verdict": "CLEAN|CLEAN_WITH_MINORS|MAJOR_FINDINGS|BLOCKING",
  "blocks_publication": true,
  "corrected": null,
  "re_audit": null,
  "created_by": "role_11",
  "created_at": "ISO8601"
}
```

### Underwriting Schema

```json
{
  "underwriting_id": "UND-{case_id}-{version}",
  "verdict": "QAD_CONFIRMED|QAD_PROBABLE|QAD_UNRESOLVED|NOT_QAD_STRUCTURAL|NOT_QAD_QUALITY|NOT_QAD_VALUATION",
  "synthesis": "string (narrative)",
  "key_unknowns": ["string"],
  "thesis_killers": [
    {"condition": "string", "evidence_threshold": "string", "status": "NOT_TRIGGERED|WATCH|TRIGGERED"}
  ],
  "founder_ready": true,
  "founder_endorsed": false,
  "created_by": "role_1",
  "created_at": "ISO8601"
}
```

---

## Part 4: NotebookLM Contracts

### NotebookLM Research Request Contract

```json
{
  "request_id": "NBR-{case_id}-{NNNN}",
  "case_id": "QAD-YYYY-NNNN",
  "request_type": "BROAD_SOURCE_DISCOVERY|TARGETED_DEEP_RESEARCH|COMPETITOR_ANALYSIS|INDUSTRY_RESEARCH|MANAGEMENT_HISTORY|SPECIALIST_RESEARCH",
  "question": "string (precise, falsifiable, not generic)",
  "company_context": {
    "name": "string",
    "ticker": "string",
    "industry": "string"
  },
  "initial_sources": ["SRC-...", "URLs"],
  "hypotheses_to_test": ["HYP-..."],
  "decision_critical_unknowns": ["string"],
  "desired_output_format": "EVIDENCE_SUMMARY|COMPETITOR_TABLE|TIMELINE|CROSS_SOURCE_ANALYSIS|GAP_ANALYSIS",
  "requested_by": "role_id",
  "requested_at": "ISO8601",
  "priority": "HIGH|MEDIUM|LOW",
  "budget_allocation": {
    "max_sources": number,
    "max_queries": number
  }
}
```

### NotebookLM Research Result Contract

```json
{
  "result_id": "NBR-{request_id}",
  "request_id": "NBR-...",
  "status": "COMPLETE|PARTIAL|FAILED|TIMEOUT",
  "synthesis": "string (NotebookLM output)",
  "cited_sources": [
    {
      "url": "string",
      "title": "string",
      "publication_date": "YYYY-MM-DD (if available)",
      "relevance": "HIGH|MEDIUM|LOW"
    }
  ],
  "source_count": number,
  "tokens_used": number,
  "notebooklm_session_id": "string",
  "raw_output_path": "string (stored for audit)",
  "completed_at": "ISO8601",
  "ingested_to_canonical": false,
  "ingested_by": null,
  "ingestion_audit": null
}
```

### Notebook → Canonical Registry Admission Contract

> **Rule:** NotebookLM output is `EXTERNAL_AI_RESEARCH_SYNTHESIS` — NOT `VALIDATED_INVESTMENT_EVIDENCE`.

```json
{
  "admission_id": "ADM-{request_id}-{NNNN}",
  "source_request_id": "NBR-...",
  "claim_from_notebook": "string (excerpt)",
  "original_source_traced": "SRC-... (or FAILED)",
  "trace_status": "TRACED|PARTIALLY_TRACED|FAILED",
  "validation": {
    "source_exists": true,
    "source_inspected": true,
    "citation_supports_claim": "YES|PARTIALLY|NO",
    "point_in_time_verified": true,
    "independent_corroboration": ["EVI-..."],
    "validated_by": "role_2",
    "validated_at": "ISO8601"
  },
  "admission_decision": "ADMIT_TO_EVIDENCE|ADMIT_WITH_CAVEATS|REJECT|REQUIRE_MORE_VERIFICATION",
  "canonical_evidence_id": "EVI-... (if admitted)",
  "notes": "string"
}
```

---

## Part 5: Research Run Manifest

```json
{
  "research_run_id": "RR-{case_id}-v{version}-{YYYYMMDD}",
  "case_id": "QAD-YYYY-NNNN",
  "case_version": 1,
  "as_of_date": "YYYY-MM-DD",
  "universe_version": "string",
  "selection_policy_version": "string",
  "models_used": {
    "role_1": {"tier": "C", "model_family": "string", "provider": "string"},
    "role_2": {"tier": "B", "model_family": "string", "provider": "string"},
    "role_10": {"tier": "D", "model_family": "string", "provider": "string"},
    "role_11": {"tier": "D", "model_family": "string", "provider": "string"}
  },
  "notebooklm_runs": ["NBR-..."],
  "sources_added": ["SRC-..."],
  "calculation_version": "string (git hash)",
  "started_at": "ISO8601",
  "completed_at": "ISO8601",
  "token_metrics": {"total_tokens": number, "total_cost": number, "by_role": {"role_3": number}},
  "failures": [{"stage": "string", "error": "string", "resolution": "string"}],
  "retries": number,
  "output_version": 1,
  "output_artifact_paths": ["string"]
}
```

---

## Part 6: State Transition Rules

| Rule | Description |
|------|-------------|
| **No skip states** | Case must pass through every state sequentially. No shortcut from CANDIDATE to FOUNDER_READY. |
| **Independent review separation** | RED_TEAM and AUDIT states require ROLE 10 and ROLE 11 — MUST be different model family/provider from primary research. |
| **Audit gates publication** | AUDIT verdict of MAJOR_FINDINGS or BLOCKING → case returns to CORRECTION. Never proceed to UNDERWRITING. |
| **Red Team challenges must be adjudicated** | Every challenge receives ACCEPTED/PARTIALLY/REJECTED/UNRESOLVED. Silent dismissal forbidden. |
| **Founder-Endorsed requires explicit Founder action** | System never auto-transitions FOUNDER_READY → FOUNDER_ENDORSED. |
| **Correction preserves originals** | Per §23.9: old version preserved, correction attached, never in-place mutation. |
| **Monitoring does not change underwriting** | MONITORING state may detect changes; re-opening requires Chief Underwriter decision. |
| **Termination requires memo** | Any TERMINATED state requires a Research Termination Memo with reason, evidence, remaining uncertainty, reopen conditions. |

---

## Part 7: Append-First Update Behavior

| Object | Update Rule |
|--------|-------------|
| Case | Version +1. Previous state preserved in `lineage.previous_version`. |
| Claim | Version +1. `superseded_by` points to new version. | 
| Evidence | Immutable after creation. New evidence → new EVI-ID. |
| Source | Immutable after creation. | 
| Research Run | Immutable after creation. |
| Challenge | Immutable. Adjudication is a separate `adjudication` sub-object. |
| Audit | Immutable. New round → new AUD-{round}. |
| Financial Fact | Correction = new FIN-ID with `supersedes` pointer. |

---

## Part 8: Failure & Retry States

| Failure | Behavior |
|---------|----------|
| Source retrieval fails (S1–S3) | Block case. Mark as `DATA_LIMITED`. Do not continue without resolving. |
| Source retrieval fails (S4–S6) | Log gap. Continue with caveat. |
| NotebookLM Deep Research fails | Bounded retry (max 3). On failure → log gap, continue only if non-blocking. |
| Scuttlebutt investigator fails | Retry once. On failure → log evidence gap, continue. |
| Red Team unreachable | Block case. Independence is mandatory. |
| Audit fails (BLOCKING) | Block publication. Return to CORRECTION. |
| Budget exhausted | MARK `BUDGET_EXHAUSTED → INCOMPLETE`. Never publish as Founders-Ready. |
| Model provider fails | Follow routing policy fallback chain. If all fail → block case. |

<!-- 2026-08-16 UTC+7 -->