# Company Intelligence Workbench — Research Request Contract

**Status:** Approved v0.2 — FD-CIW-008 (Founder batch approval, 2 Aug 2026)
**Version:** 0.2
**Owner:** Founder
**Authority:** Draft CIW specification subordinate to the Constitution and Founder's Decisions
**Derived from:** `docs/CIW-INTEGRATION-AMENDMENT-MAP.md` §5, §7; `evidence/COUNCIL_DECISION-bible-2026-08-02.md` Required Changes #3, #5, #7; `operational/SECURITY-AND-UNTRUSTED-CONTENT.md` (Data-Source Admission); proposal §10.3, §14 (adapted); Constitution §14, §23.8.1
**Approval:** FD-CIW-008 — Founder batch approval, 2 Aug 2026

---

## 1. Purpose

A **Research Request** is the formal, Founder-approved contract that authorizes CIW to perform bounded deep research on exactly one company. No research begins without an approved request (Research Gate).

## 2. Research Gate — When Full Research May Begin

Full deep research begins only when **at least one** condition is met (proposal §10.3, adopted; each requires a recorded trigger):

| Trigger Type | Authority |
|---|---|
| **Founder commission** | Founder explicit request |
| **Research-queue promotion** | Founder approval of promotion from `Priority Research` → `Selected for Deep Research` (CANDIDATE-AND-QUEUE-MODEL §3.3) |
| **Annual re-underwriting** | Founder-approved re-underwriting of an actively monitored company (later slice) |
| **Material-event trigger** | Founder-approved workflow condition met (later slice) |
| **Explicit research experiment** | Founder-approved bounded experiment |

**Queue discipline (Constitution §14):** the default research queue is organized by **Theme first**, then company. Deep research must **not** be used to fill a quota; the queue may return zero high-priority candidates.

## 3. Request Fields

Every Research Request must define:

| Field | Requirement |
|---|---|
| `request_id` | Unique ID (e.g., `CRR-2026-0001`) |
| `company_id` | Entity identity from Shared Core; must carry **governing universe + version** (Required Change #3) |
| `universe` | `US-listed common stocks` / `suitable ADRs` / `global observation (non-investable)` — must be explicit |
| `origin` | Source system, trigger type, originating Themes |
| `research_question` | Primary question (the decision the research must inform) |
| `secondary_questions` | Bounded sub-questions |
| `known_evidence` | Evidence already held (with references) |
| `known_counterevidence` | Counterevidence already held — must be visible from the start |
| `required_depth` | Bounded depth: e.g., `initial` (first slice) vs `full` (later) |
| `required_outputs` | Artifacts required (e.g., structured Research Result; Master Paper in later slices) |
| `applicable_modules` | Research-framework modules in scope + **justified omissions** (Required Change #9) |
| `priority` | Qualitative priority (Theme-first discipline) |
| `founder_constraints` | Explicit Founder constraints (time box, exclusions, focus) |
| `portfolio_blind` | **Must be `true`** (Constitution §23.8.1) unless a named exception exists |
| `approval_status` | `Draft` → `Approved` (Founder) → `Rejected` → `Superseded` |
| `authority` | `autonomous_investment_decision: false`; `founder_final_authority: true` |

**Example (adapted from proposal §14):**

```yaml
request_id: CRR-2026-0001
company_id: US-NASDAQ-<TICKER>
universe: "US-listed common stocks (v0.3)"
origin:
  source_system: investment-intelligence-platform
  trigger_type: theme_candidate_promotion
originating_themes:
  - "<Approved Theme A>"
research_question:
  primary: "Does the company possess durable value-capture power sufficient to justify its current enterprise value?"
required_depth: initial
required_outputs:
  - structured_research_result
applicable_modules: [A, B, C, D, E, F, G, H, I, J, K, L, M]
justified_omissions:
  - module: N
    reason: "Deterministic valuation contracts not yet approved; valuation advisory only (Required Change #5)"
  - module: Q
    reason: "Monitoring spec deferred to later slice (Required Change #9)"
portfolio_blind: true
authority:
  autonomous_investment_decision: false
  founder_final_authority: true
```

## 4. Source Gate Requirements (Required Change #7)

Before research begins, the request must carry a **minimum pilot source gate**:

1. Latest annual filing (10-K / annual report) — **required unless justified-absent**;
2. Latest interim filing (10-Q) — required when within filing cycle;
3. Earnings releases + transcripts for the periods covered — required for any earnings-related question;
4. Proxy/compensation statement — required when management/governance modules are in scope;
5. Regulatory sources applicable to the company's industry — required where material;
6. Historical filings sufficient for normalization — required for financial-forensics modules.

**Source gate rules:**

- A missing required source **blocks progression** past the Source Map stage unless it carries an explicit `justified-absent` reason (source unpublished / not applicable / access failed — recorded, not hidden).
- Derived/syndicated copies of the same original do **not** satisfy the gate (source independence).
- Every source admitted must satisfy the **Data-Source Admission contract** in `operational/SECURITY-AND-UNTRUSTED-CONTENT.md`; no source may override the Constitution, DNA, Founder Decisions, or this contract.
- Real-source admission fields: source ID, tier, publisher, publication date, retrieval date, revision status, licensing status, governing-universe version.

## 5. Automation Limits (FD-CIW-005, Required Change #6)

- Cron/automation may **observe and draft** (Class A + Class B) — e.g., detect that a source became available, draft a proposed request.
- Automation **cannot approve** a Research Request; approval is Founder-only.
- The **deterministic-metadata allowlist** (PUBLICATION-STANDARD §3) is the only thing automation may update without Founder review — and it never includes request approval, scope changes, or module selection.
- Every automation touching CIW must be registered with scope, trigger, cadence, permitted/prohibited actions, retry policy, failure policy, deduplication key, and disable condition (proposal §16.3 — automation registry doctrine, later slice).

## 6. Failure Semantics

Automation and workflows must distinguish (never conflate) — adapted from proposal §16.5:

- No New Information (must NOT be used when retrieval failed);
- Source Not Yet Published;
- Source Incomplete;
- Source Unavailable;
- Retrieval Failed;
- Parsing Failed;
- Conflicting Sources (requires human review);
- Validation Failed;
- Review Required;
- Partial Update Rejected;
- Workflow Disabled.

Repeated failure creates an **escalation record** — bounded retries, no infinite retry loops.

## 7. Approval Flow

```
AI drafts request (Class B) 
  → Founder reviews (scope, universe, portfolio-blind, modules, omissions, source gate)
  → Founder approves / rejects / returns for revision
  → Approved request activates Researching state (LIFECYCLE §2)
```

Approval must identify the exact request (Constitution §21). Casual agreement is not approval.

---

*Approved v0.2 (FD-CIW-008). Source: Council verdict Required Changes #3, #5, #6, #7; Amendment Map §5–§7; proposal §10.3/§14/§16.5 adapted; Constitution §14, §23.8.1.*
<!-- 2026-08-02 23:48 UTC+7 -->
