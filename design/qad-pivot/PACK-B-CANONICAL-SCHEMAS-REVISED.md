# Pack B — Canonical Schemas & State Machines (Revised)

> **Status:** Resolution round — corrected for Pre-Code Design Gate.
> **Key changes from v1:**
> - Persistent NotebookLM discovery provenance (survives source promotion)
> - S6_UNVERIFIED_LEAD invariant for unvalidated NotebookLM synthesis
> - Case version/update lifecycle (new as-of → new version)
> - QUALITY_VERIFICATION state added
> - State machine updated for ALL corrections
> - Negative test requirements for NotebookLM self-promotion prevention

---

## Part 1: ID Scheme & Versioning (Unchanged from v1)

…

---

## Part 2: Case State Machine (Revised)

```
                    ┌──────────────────────────────────────┐
                    │      AUTONOMOUS SELECTION ENGINE      │
                    │  (Policy-driven Hard Gates)           │
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
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │      EVIDENCE BUILDING        │
                    │  Core Desk + NotebookLM +     │
                    │  Scuttlebutt (as needed)      │
                    │  Sources retrieved + validated │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────────┐
                    │       QUALITY VERIFICATION        │ ← NEW
                    │  Was historical quality real?     │
                    │  VERIFIED / PROBABLE /            │
                    │  UNRESOLVED / FAILED              │
                    └──────┬───────────────┬───────────┘
                           │               │
                           ▼               ▼
                   ANALYSIS PHASE      NOT_QAD_QUALITY
                     (proceed)           (terminated)
                           │
                           ▼
                    ┌──────────────────────────────┐
                    │    IMPAIRMENT DIAGNOSIS        │
                    │  Dual explanations produced    │
                    │  (Primary + Competing)         │
                    └──────────────┬───────────────┘
                           │
                           ▼
                    ┌──────────────────────────────┐
                    │    NORMALIZATION & VALUATION   │
                    └──────────────┬───────────────┘
                           │
                           ▼
                    ┌──────────────────────────────┐
                    │     RED TEAM CHALLENGE         │
                    │  Starts from raw evidence,     │
                    │  NOT analyst narrative         │
                    │  No veto power                 │
                    └──────────────┬───────────────┘
                           │
                           ▼
                    ┌──────────────────────────────┐
                    │     CHIEF UNDERWRITER          │
                    │  Adjudication + Synthesis     │
                    └──────────────┬───────────────┘
                           │
                           ▼
                    ┌──────────────────────────────┐
                    │            AUDIT               │
                    └──────────────┬───────────────┘
                           │
                    ┌──────┴──────┐
                    │             │
                    ▼             ▼
              PASS / MINORS   MAJOR / BLOCK
                    │             │
                    ▼             ▼
            FOUNDER-READY    CORRECTION → re-AUDIT
                    │
                    ▼
              FOUNDER ENDORSED
           (explicit Founder action only)
                    │
                    ▼
               MONITORING
                    │
              (possible update)
                    │
                    ▼
            CASE UPDATE (new as-of)
                    │
                    ▼
          NEW RESEARCH RUN (immutable)
       (new version, same case lineage)
```

### New States Added

| State | Description | Transitions To |
|-------|-------------|----------------|
| `QUALITY_VERIFICATION` | Was historical quality real? Determine VERIFIED/PROBABLE/UNRESOLVED/FAILED | `ANALYSIS`, `NOT_QAD_QUALITY` |
| `NOT_QAD_QUALITY` | Quality FAILED — business never had durable economics | `ARCHIVED` |
| `CASE_UPDATE` | New information available for an existing case | `new EVIDENCE_BUILDING` |
| `CORRECTION` | Audit findings being fixed | `AUDIT` (re-audit) |

### Case Versioning (Revised)

| Version | As-Of | Event | 
|---------|-------|-------|
| v1 | 2026-08-16 | Initial |
| v2 | 2026-11-10 | Post-earnings update |

- Case version increments on new as-of (material new information)
- Each version has its own Research Run(s) — immutable
- Prior Evidence/Claims/Diagnosis retrievable from previous version
- Change package records: what changed, why, new evidence added, old evidence superseded
- Monitoring events may trigger new version (e.g., thesis break, new filing)
- No future evidence silently backfills a past as-of snapshot

---

## Part 3: Persistent NotebookLM Provenance

### Evidence Schema — Discovery Provenance Extension

Every evidence object gains persistent `discovery_origin`:

```yaml
evidence_id: EVI-{hash8}
original_source:
  source_id: SRC-...
  source_class: S1|S2|S3|S4|S5|S6
  publication_date: YYYY-MM-DD
  retrieval_date: YYYY-MM-DD
  # ... other source fields ...

# NEW: persistent discovery route
discovery_origin:                # ← THIS SURVIVES FOREVER
  type: DIRECT_SOURCE          # discovered_directly
       | WEB_SEARCH            # discovered via web search
       | NOTEBOOKLM            # discovered via NotebookLM
       | SCUTTLEBUTT           # discovered via investigator
       | CROSS_REFERENCE       # discovered via another source
       | OTHER
  notebook_id: null            # if NOTEBOOKLM
  request_id: null             # if NOTEBOOKLM
  deep_research_run_id: null   # if NOTEBOOKLM
  synthesis_excerpt: null      # if NOTEBOOKLM — excerpt where found
  discovered_source_url: null  # the URL NotebookLM found

# NEW: validation record
validation:
  original_source_retrieved: true   # was the source actually retrieved?
  original_source_hash: abc123      # hash of retrieved source
  validator: role_2                 # who validated
  validation_status: VERIFIED       # VERIFIED|PARTIALLY_VERIFIED|UNVERIFIED

# source_class vs discovery_origin are INDEPENDENT dimensions:
# Example: EVI could be:
#   source_class: S1 (it's a filing — authoritative)
#   discovery_origin.type: NOTEBOOKLM (but NotebookLM found it)
# Both metadata survive forever.
```

### Hard Invariant: NotebookLM → S6 by default

```yaml
RULE: "NotebookLM synthesis without original-source validation = S6_UNVERIFIED_LEAD"
SCOPE: ALL evidence discovered via NotebookLM
ENFORCEMENT:
  - Evidence with discovery_origin.type = NOTEBOOKLM and
    validation.original_source_retrieved = false
    MUST be classified source_class = S6
  - Even if NotebookLM output appears to cite sources,
    the source class is S6 until an independent role
    retrieves and inspects the original.
EXCEPTIONS: NONE
```

### Negative Test Requirements

```
TEST: "NotebookLM_cannot_self_promote"
GIVEN: Evidence with discovery_origin.type = NOTEBOOKLM
  AND validation.original_source_retrieved = false
WHEN: Any role attempts to set source_class to S1-S5
THEN: System MUST reject. source_class stays S6.

TEST: "NotebookLM_provenance_survives_promotion"
GIVEN: Evidence with discovery_origin.type = NOTEBOOKLM
  AND later validation.original_source_retrieved = true
  AND source_class promoted to S1
WHEN: Querying discovery_origin
THEN: discovery_origin.type MUST still show NOTEBOOKLM
  (both "source authority" AND "discovery route" preserved)
```

### Two Dimensions Concept

```
SOURCE AUTHORITY (what is truth?)
  S1 — Authoritative Primary (filing, audited)
  S2 — Ecosystem Primary (competitor/customer disclosure)
  S3 — Observable Operational (prices, public inventories)
  S4 — Specialist Secondary (trade publications)
  S5 — Anecdotal / Social
  S6 — Unverified Lead

DISCOVERY ROUTE (how was it found?)
  DIRECT_SOURCE — manual/file navigation
  WEB_SEARCH — search engine
  NOTEBOOKLM — NotebookLM Deep Research
  SCUTTLEBUTT — investigator
  CROSS_REFERENCE — found by reading another source
  OTHER

These are INDEPENDENT axes.
A filing discovered via NotebookLM is:
  Authority: S1
  Route: NOTEBOOKLM
Both metadata survive forever.
```

---

## Part 4: State Transition Rules (Revised)

| Rule | Description |
|------|-------------|
| **QUALITY_VERIFICATION mandatory** | Case must pass through QUALITY_VERIFICATION before IMPAIRMENT_DIAGNOSIS. Only FAILED → NOT_QAD_QUALITY terminates. UNRESOLVED may trigger targeted evidence acquisition. |
| **Impairment dual explanations** | Role 8 must produce Primary + Strongest Competing + Weakest Link + Flip Evidence. Red Team starts from raw evidence graph, not analyst narrative. |
| **Red Team no veto** | Red Team produces challenges. Chief Underwriter adjudicates. Material unresolved disagreements → UNRESOLVED classification or Founder escalation. |
| **Case update preserves lineage** | New as-of → new version. Prior version retrievable. Each Research Run immutable. Change package recorded. |
| **Audit checks integrity, not budgets** | Auditor never approves compute budgets. Budget Controller is a separate policy service. Auditor verifies logging post-hoc. |
| **Autonomous selection is policy-driven** | Selection Engine applies Hard Gates deterministically. Chief Underwriter has NO role in case selection. |

---

## Part 5: NotebookLM Contracts (Unchanged from v1)

---

## Part 6: Research Run Manifest (Unchanged from v1)

---

## Part 7: Append-First Update Behavior (Extended)

| Object | Update Rule |
|--------|-------------|
| **Case** | Version +1 on new as-of. Previous version fully retrievable. `lineage` tracks version chain. |
| **Claim** | Version +1 on correction. `superseded_by` points to new. |
| **Evidence** | Immutable after creation. Provenance (source authority + discovery route) never changes. New evidence = new EVI-ID. |
| **Source** | Immutable after creation. |
| **Research Run** | Immutable after creation. |
| **Impairment Diagnosis** | New version on re-assessment. Old classification preserved. |
| **Challenge** | Immutable. Adjudication is a separate sub-object. |
| **Audit** | Immutable. New round → new AUD-{round}. |

---

## Part 8: Failure & Retry States (Revised)

| Failure | Behavior |
|---------|----------|
| Quality FAILED | Case terminates as NOT_QAD_QUALITY. Research Termination Memo created. |
| Source retrieval fails (S1–S3) | Block case. Mark DATA_LIMITED. Do not continue without resolving. |
| NotebookLM unvalidated | Evidence stays S6. Cannot support material QAD conclusion. |
| Red Team unreachable | Block case (independence is mandatory for full research). |
| Audit BLOCKING | Block publication. Return to CORRECTION. |
| Budget exhausted | MARK BUDGET_EXHAUSTED → INCOMPLETE. Never publish as Founder-Ready. |
| Model provider fails | Follow routing policy fallback chain. |

<!-- 2026-08-16 UTC+7 -->