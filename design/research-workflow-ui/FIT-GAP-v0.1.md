# Research Workflow UI — Fit-Gap Analysis

**Status:** PROPOSED — FOUNDER REVIEW REQUIRED
**Version:** 0.1 (draft for review — NOT approved, NOT canonical)
**Date:** 2026-08-05
**Author:** IIP profile (Hermes Agent), read-only discovery pass
**Source proposal:** ChatGPT IA/navigation recommendation (2026-08-05): Research Desk + Research Artifact Detail + Dashboard→Briefing upgrade + Close System Product Detail + 12 shared components, phased UI-1/UI-2/UI-3.
**Scope:** READ-ONLY. No code, no API changes, no schema, no design tokens changed. All build decisions below require explicit Founder approval (D1–D4 in §8). Follows Option A chosen by Founder: fit-gap + blueprint BEFORE any build (mirrors FD #54 path: fit-gap → design → approval).

---

## 1. Executive Summary

**The direction is sound and consistent with IIP doctrine** (evidence-first, no composite scores, no chain-of-thought, roles as logical responsibilities — matches Constitution + Operating Model + FD #54). The core thesis — *design around the Research Artifact and Decision Workflow, not the org chart* — is correct, and the Agent→UI mapping matches the 10 installed org profiles (org-cos..org-auditor) exactly.

**But the proposal assumes a data layer that does not exist.** IIP's API serves 7 strategy endpoints only; there is no research/artifact/org-workflow endpoint. The good news: **the data the proposal needs already exists in the repo** — kanban cards (YAML), holds (YAML), CIW MSFT research artifacts (markdown, real), org templates (15 forms), and the CS pipeline artifact (richer than the current mock API admits). The missing piece is a **read-only file adapter** (new API surface — requires authorization per FD #44 boundary) plus, for CS Product Detail, a **separate FD to admit CS pipeline fields** (F3 adapter flow).

**Verdict:** Adopt the structure with three adjustments:
1. **Data layer first** (read-only adapter + Founder gate) — every page in the proposal consumes org-workflow data.
2. **CS Product Detail is buildable but conditional** — the pipeline artifact (SYNTHETIC, verified) contains layers L1–L5, discount/demand details, conviction, key risks; the current mock admits almost none of it. Options Overlay has **no data source anywhere** — defer that tab.
3. **Cut ~30% of the proposal:** Cross-Domain Intelligence (no data), Options Overlay (no data), EpistemicStatusBadge rebuilt on the CANONICAL EVIDENCE-MODEL §2 taxonomy (not the ad-hoc list), DecisionPacketView read-only (no UI write-back), Decision Register / Model Registry / Audit Center deferred (ChatGPT's own UI-3 — agreed).

---

## 2. Ground Truth — Verified Data Sources (all read this session)

| # | Source | Path | Content | Real for UI? |
|---|---|---|---|---|
| 1 | Kanban board | `operational/hermes-organization/kanban/board.md` | 11 columns (Inbox→Triage→Scoped→Data Ready→In Research→Cross-Review→Validation→Founder Review→Monitoring→Blocked→Closed); 5 pilot cards | YES — operational tracking (never domain state, KANBAN-CONTRACT §1) |
| 2 | Kanban cards | `kanban/cards/ORG-2026-000X.yaml` | 23-field schema: workflow_column, approval_status, monitoring_status, thesis_status, research_state, artifact_state, domain, principal/assistant_owner, priority, materiality, data_status, validation_status, risk_status, audit_status, open_decision_slots, dependencies, blocked_reason, next_action, last_updated | YES — exactly the ResearchArtifactRow fields |
| 3 | Holds | `kanban/holds/HOLD-DATA-001.yaml`, `HOLD-RISK-001.yaml` | scope, trigger, evidence, remediation, owner, review condition, partial-work allowance, clear record | YES — HoldBanner data |
| 4 | CIW MSFT artifacts (REAL) | `docs/ciw-pilot-msft/` | research-result.md v1 + research-result-2.md v2 (Published), research-draft v0.5, challenge-review rounds 1–5, founder-review-record, source-map (8 sources), CRR-2026-0001/0002 | YES — first real Artifact Detail content |
| 5 | Org templates | `operational/hermes-organization/templates/01..15` | research request, evidence record, brief, data-quality, quant-validation, risk-challenge, options memo, IC decision pack, founder decision record, weekly brief, audit finding, change request, worklog | Schema for tabs; mostly no instance data yet |
| 6 | Org pilot artifacts | `evidence/organization/pilot/` | IC decision pack, equity brief, worklogs (dry-run pilot, simulated) | Partial — labeled pilot/simulated |
| 7 | CS pipeline artifact (SYNTHETIC) | `close_system/output/pipeline_result.json` | per product: p1/p2/p3_pass + rationales, discount_type/depth/detail (gold_price, avg_aisc, marginal_aisc), demand_type/detail, layers L1_macro/L2_policy/L3_cost/L4_supply_demand/L5_hidden (+signal+note), layers_aligned/contradicting, conviction, key_risks, recommendation + rationale; lists: present_to_founder / deep_research / radar_watchlist | YES (labeled SYNTHETIC — fixture_category) — **richer than the mock API** |
| 8 | Current API surface | `backend/api/{am,cs,fo,ii}_routes.py` | 7 endpoints; cs mock admits only: q_conditions, dimensions (suitability/opportunity/regime/decay/data_confidence), rule_pack, instrument, liquidity, capital_lockup | Baseline — nothing org/research/artifact exists |
| 9 | Evidence taxonomy (CANONICAL) | `project-definition/EVIDENCE-MODEL.md` §2.1/§2.2 | Record types: Raw Source Record, Observed Fact, Claim (Source Claim / AI Extraction / AI Classification), Normalized Fact, Derived Metric, Statistical Signal, Founder Knowledge Record, Hypothesis, Human Judgment, Approved Decision, Outcome, Lesson | Replaces ChatGPT's ad-hoc EpistemicStatusBadge list |
| 10 | Design system | `design-system/investment-intelligence-platform/MASTER.md` v3.0 + `design/UI_TOKENS.md` + `frontend/src/index.css` | Research Desk visual system: paper canvas, serif display, hairline ledgers, borderless 0–2, provenance chips, staleness banners, honest empty/error states | Constraint for all pages |

**Does NOT exist (verified):** backend org/research endpoints; decision register artifact; model registry; audit center; cross-domain synthesis data (Weekly Brief template is empty); options market data (no options pipeline; template 09 is research-only); quant validation report instances.

---

## 3. Fit-Gap Table (ChatGPT item → Data → Verdict)

| ChatGPT proposal | Data source (verified) | Verdict | Notes |
|---|---|---|---|
| **Research Desk** one main-nav page, 5 views | kanban board + cards | **BUILD** (needs adapter) | Views reconcile to kanban columns (§4) |
| Research row fields (ID, subject, type, analyst, state, approval, monitoring, evidence completeness, data quality, validation, challenge, hold, last change, next action) | card YAML §2#2 + holds | **BUILD** | Every field exists; "evidence completeness" derives from evidence_standard/data_status |
| **Artifact Detail** `/research/:id`, 8 tabs | CIW artifacts + card + holds + challenge files | **BUILD** (needs adapter; tabs 5–6 honest states) | §4.2 |
| **Dashboard → Briefing**, 5 sections | kanban + holds + versioned artifacts | **PARTIAL** — build 4 of 5 | Cross-Domain Intelligence DEFERRED (no data) |
| **CS Product Detail** `/cs-radar/:productId`, 6 tabs | pipeline_result.json §2#7 | **CONDITIONAL** — needs FD to admit CS fields | Options Overlay tab DEFERRED (no data anywhere) |
| 12 shared components | mixed | 10 build / 1 scaffold / 1 redefined | §5 |
| Phase UI-3 (Decision Register, Model Registry, Audit & Exceptions) | no artifacts | **DEFER** (agree with ChatGPT) | Do not build empty screens |
| Agent Team Dashboard / per-agent pages / CoT / rankings / tokens | n/a | **REJECT** (agree) | Violates Constitution; no decision value |
| Navigation: Briefing, Research Desk, AM, CS, FO, II, Weak Signals | n/a | **BUILD** (rename Dashboard → Briefing is Founder choice) | Naming note: "Research Desk" collides with the FD #51 visual-direction name — document the distinction, or pick "Research" / "Work Queue" |

---

## 4. Page Blueprints (text-wireframe level — full blueprints after scope approval)

### 4.1 Research Desk (`/research` — one nav page, 5 views)

**Purpose:** the org-workflow's UI surface — where the work queue, holds, and next actions live. **Primary decision:** "What requires my attention / a decision, and what is blocked?" **Not the purpose:** per-agent productivity, chat transcripts, token stats.

Views reconcile kanban's 11 columns (single source — no parallel state machine):

| ChatGPT view | Kanban columns (KANBAN-CONTRACT §2) | Primary question |
|---|---|---|
| Inbox | Inbox, Triage | What just arrived? |
| Active Research | Scoped, Data Ready, In Research | What is being worked on, by whom? |
| Review Queue | Cross-Review, Validation | What awaits independent review? |
| Founder Review | Founder Review, Blocked | What needs my decision (or is stuck)? |
| Archive | Monitoring, Closed | What was decided / retired? |

Held cards (DATA/VALIDATION/RISK/GOVERNANCE holds) surface inside every view via HoldBanner (never a small badge) + a global "Held / Blocked" filter. **No Progress-72% bars, no composite scores** (design system prohibition).

Row = ResearchArtifactRow: card_id · subject · domain · primary owner · workflow column · approval status · data/validation/risk status · active hold · last change · next action. Sorted by materiality then last_updated. Honest empty states per view ("Inbox is empty — no new research requests", with the intake path).

### 4.2 Research Artifact Detail (`/research/:artifactId` — drill-down, NOT in main nav)

**Purpose:** the complete product of all roles on one subject — evidence, uncertainty, dissent, validation, decision history. **Primary decision:** "Should this advance / be decided / be watched?"

| Tab | Content | Data today |
|---|---|---|
| Executive Summary | core question, current assessment, confidence, what changed, key supporting/contradicting evidence, next decision | MSFT research-result front-matter + dimension summaries (REAL) |
| Research | artifact body (markdown) per domain sections | MSFT v1/v2 (REAL); org briefs as they appear |
| Evidence | reuse EvidencePanel patterns; supporting/contradicting/missing/alternative explanations + provenance + as-of | CIW SRC-xxx refs + source-map (REAL); full register via template 02 as produced |
| Independent Challenge | findings typed: Observed Contradiction / Alternative Explanation / Model Limitation / Data Limitation / Governance Concern / Operational Concern / Generic Risk | challenge-review rounds 1–5 MSFT (REAL) |
| Validation | status, method version, dataset, tests, limitations, dissent | scaffold from template 07 — honest empty (no real reports yet) |
| Data Quality | coverage, freshness, completeness, conflicts, restatements, hold | source-map (REAL) + card data_status |
| Decision History | immutable timeline: created → assigned → evidence → validated → challenged → founder review → approved/rejected/returned | card transitions (git) + founder-review-record (REAL) |
| Audit Trail | artifact versions, corrections, holds, overrides, exceptions | git history per artifact (REAL); audit-finding template as produced |

Immutable timeline rule: corrections render as replacements (version + hash), never deletion — matches PUBLICATION-STANDARD versioning (research-result v1 intact when v2 published).

### 4.3 Briefing (Dashboard `/` — renamed label, same route)

Keep existing: HeroInsight, findings ledger, engine provenance, lifecycle breadth (already a briefing). Add 4 of 5 sections:

| Section | Data | Verdict |
|---|---|---|
| Decisions Required | kanban Founder Review + open_decision_slots (1 real item: ORG-2026-0004) | BUILD — states what decision, not just "review needed" |
| Material Changes Since Last Review | versioned artifacts (MSFT v1→v2 = first real pair) + last_updated | BUILD — compare current vs previous reviewed version |
| Cross-Domain Intelligence | none (Weekly Brief empty) | DEFER — no invented synthesis |
| Holds & Exceptions | holds YAML (2 real) | BUILD — issued by / reason / affected artifact / clearance / age / escalation |
| Research Throughput | kanban ledger | BUILD — ledger counts, never agent rankings |

### 4.4 CS Product Detail (`/cs-radar/:productId` — conditional)

| Tab | Data (verified in pipeline_result.json) | Verdict |
|---|---|---|
| Product Thesis | p1/p2/p3_pass + p1_rationale, discount_type, demand_type, status | NEEDS FD (admit) |
| Commodity Fundamentals | discount_detail (price, avg_aisc, marginal_aisc), demand_detail, L3_cost, L4_supply_demand | NEEDS FD (admit; SYNTHETIC-labeled) |
| Macro Context | L1_macro, L2_policy (signal + note) | NEEDS FD (admit) |
| Close System Assessment | q_conditions/dimensions (already admitted) + conviction, key_risks, layers_aligned/contradicting, recommendation | PARTIAL now; rest NEEDS FD |
| Options Overlay | **none exists** | DEFER — template 09 is research-only; no options pipeline |
| Challenge & Evidence | shared components + key_risks | BUILD with admitted fields |

---

## 5. Component Verdicts (12 proposed)

| Component | Verdict | Grounding |
|---|---|---|
| DecisionRequiredLedger | BUILD | kanban cards + holds |
| ResearchArtifactRow | BUILD | card YAML §2#2 |
| MaterialChangePanel | BUILD | versioned artifacts (v1→v2 pattern) |
| AgentContributionLineage | BUILD | card owners + artifact author/reviewer fields — table, not avatars; Assistant = contributor, never approver |
| HoldBanner | BUILD | holds YAML — full banner, not a badge |
| ReviewGatePanel | BUILD | card data/validation/risk/audit statuses + artifact_state — status rows, no linear progress bar |
| IndependentChallengePanel | BUILD | challenge-review files; reuse FO pattern with typed findings |
| ValidationSummary | SCAFFOLD | template 07 schema; honest empty until real reports |
| DataQualityPanel | BUILD | card data_status + source-map + template 06 |
| DecisionTimeline | BUILD | git history + founder records (immutable by construction) |
| EpistemicStatusBadge | **REDEFINE** | use CANONICAL EVIDENCE-MODEL §2 taxonomy (Raw Source Record / Observed Fact / Claim incl. AI Extraction+Classification / Normalized Fact / Derived Metric / Statistical Signal / Hypothesis / Human Judgment / Approved Decision…) — NOT the ad-hoc list ("AI Interpretation" is not a canonical type) |
| DecisionPacketView | BUILD READ-ONLY | template 10 + ORG-2026-0004 + founder-review-record; options displayed as information — **no UI write-back** (FD #54: only an explicit Founder decision changes canonical state; decisions happen in repo/vault) |

---

## 6. The Missing Piece — Data Layer Gate (the real first decision)

Every page above consumes org-workflow data that IIP's API does not serve. Required: a **read-only file adapter** (new `backend/api/org_routes.py` + artifact registry) reading:

- `GET /org-queue` — kanban cards (columns, statuses, owners, next_action, holds)
- `GET /org-holds` — holds YAML
- `GET /research-artifacts` + `/research-artifacts/{id}` — artifact registry from repo dirs (CIW + org templates instances), front-matter + sections + challenge/founder files
- `GET /cs-radar/{productId}` — from pipeline_result.json (after D2)

Properties: read-only (no writes — git stays the single writer and audit trail), no schema/migration, YAML/markdown/JSON parsing only, provenance labels preserved (kanban = OPERATIONAL; CS = SYNTHETIC; CIW = REAL). Authority: FD #44 requires explicit authorization for new data sources → **D1** (or a named FD covering D1+D2).

---

## 7. Proposed Implementation Phases (revised from ChatGPT's UI-1/2/3)

| Phase | Scope | Gate |
|---|---|---|
| UI-0 | Read-only org adapter + endpoints + locked tests (F3 flow if adapters.py touched) | D1 |
| UI-1 | Briefing sections (Decisions Required, Material Changes, Holds, Throughput) + rename | D3 (scope) |
| UI-2 | `/research` + `/research/:artifactId` + shared components (build-set §5) | D3 |
| UI-3 | CS Product Detail (admit CS pipeline fields first — F3 flow: locked test → adapter → ADAPTER_VERSION bump → registry → suite) | D2 + D3 |
| UI-4 | Deferred: Decision Register, Model Registry, Audit & Exceptions Center | only after real artifacts accumulate (agree with ChatGPT) |

Each phase: browser-first verification, screenshots to `evidence/ui/<task-id>/`, VISUAL_QA.md, borderless audit, design-system compliance (MASTER.md v3.0).

---

## 8. Decisions Required from Founder (one at a time)

- **D1 — Approve the read-only org-workflow adapter (new API surface, no schema/migration, no writes).** Recommended: YES — it is the prerequisite for every page; small, reversible, git remains the single writer.
- **D2 — Approve CS pipeline-field admission** (p1–p3, layers L1–L5, discount/demand details, conviction, key_risks, recommendation) via separate FD + F3 adapter flow. Recommended: YES for thesis/commodity/macro/assessment tabs; Options Overlay stays deferred.
- **D3 — Approve scope/order** (§7 phases UI-0→UI-3; UI-4 deferred).
- **D4 — Page naming:** rename Dashboard label → "Briefing"? New page label "Research Desk" (collides with FD #51 visual-direction name in docs) vs "Research" / "Work Queue"? Recommended: Briefing + Research Desk with a doc note distinguishing direction-name vs nav-destination.

---

*Research Workflow UI Fit-Gap v0.1 — 2026-08-05. Read-only pass; no code changed. All paths verified this session.*
<!-- 2026-08-05 15:47 UTC+7 -->
