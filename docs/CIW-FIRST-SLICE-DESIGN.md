# CIW First-Slice Design — Pilot Company: MSFT

**Status:** DRAFT v0.1 — pending Phase 2R independent review (Sol Medium) + Founder approval
**Version:** 0.1
**Date:** 2026-08-03
**Owner:** Founder
**Authority:** FD-CIW-010 (Phase 11 Design Path OPENED — supersedes FD #44 for DESIGN purposes only); CIW-CONCEPT §6 (Pilot Scope); CIW-LIFECYCLE §6 (First-Slice Lifecycle); CIW-REQUEST-CONTRACT; CIW-QUALITY-GATES; CIW-RESULT-CONTRACT; CIW-PUBLICATION-STANDARD; CIW-RESEARCH-FRAMEWORK
**Approval:** Pending — Phase 2R review → Founder approval → FD-CIW-011 (pilot execution authorization)
**Status after approval:** Documentation only. This design does NOT authorize execution; pilot execution requires FD-CIW-011.

---

## 1. Purpose

This document is the **design plan for the CIW first slice** — the bounded pilot that validates the CIW workflow on pilot company **MSFT** per CIW-CONCEPT §6. It maps the six lifecycle steps (CIW-LIFECYCLE §6) to concrete artifacts, actors, gates, and file locations.

**What the pilot validates (and only this):**
- The CIW workflow is feasible end-to-end: Approved Request → Source Map → bounded initial research → Independent Challenge → Founder Review → structured Research Result.
- The workflow completes **without** Cron, a new repository/profile, a database migration, or an earnings-update subsystem (CIW-CONCEPT §6 verification; Required Change #9).

**What the pilot does NOT validate:**
- The economic validity of the research methodology or its valuation assumptions (Council minority warning — RESEARCH-FRAMEWORK §1).
- Any investment conclusion about MSFT. Pilot = workflow validation, **not** stock endorsement.

## 2. Gate Sequence

```
FD-CIW-010 (done — design path opened)
  → [this design] DRAFT v0.1
  → Phase 2R independent review (Sol Medium, hostile reviewer)
  → Founder approval of design
  → FD-CIW-011 (pilot execution authorization — named FD superseding FD #44 for pilot scope)
  → CRR-2026-0001 Research Request draft → Founder approval (Research Gate)
  → Source Map → bounded research → Independent Challenge → Founder Review → structured result
```

No step may be skipped. FD #44 remains in force for everything outside the design path until FD-CIW-011.

## 3. Workflow — Six Steps, Actors, Artifacts

| # | Lifecycle Step (LIFECYCLE §6) | CIW Research Status | Artifact | Actor |
|---|---|---|---|---|
| 1 | Approved Research Request | `Approved for Research` | `docs/ciw-pilot-msft/CRR-2026-0001-request.md` | AI drafts (Class B) → **Founder approves** (Research Gate, REQUEST-CONTRACT §2/§7) |
| 2 | Source Map | `Researching` | `docs/ciw-pilot-msft/source-map.md` | AI executor (source gate; `missing_required` blocks progression) |
| 3 | Bounded Initial Research | `Researching` → `Draft` | `docs/ciw-pilot-msft/research-draft.md` | AI executor (modules A–M, depth=initial) |
| 4 | Independent Challenge | `Independent Review` | `docs/ciw-pilot-msft/challenge-review.md` | **Independent reviewer** (separate context — see §6) |
| 5 | Founder Review | `Founder Review` | `docs/ciw-pilot-msft/founder-review-record.md` | **Founder only** |
| 6 | Structured Research Result | `Published` (Current Authoritative v1) | `docs/ciw-pilot-msft/research-result.md` | Founder publishes; AI assembles per RESULT-CONTRACT |

**Prohibited transitions (LIFECYCLE §7):** AI → Published; Cron → any authoritative state change; Reviewer → Published (reviewer approves pass, Founder publishes). Every transition records audit fields: prior state, new state, actor, reason, evidence reference, timestamp, workflow version.

## 4. File Tree (bounded — no expanded tree)

```
docs/
├── CIW-FIRST-SLICE-DESIGN.md        ← this design (v0.1 draft → v0.1 approved)
└── ciw-pilot-msft/
    ├── CRR-2026-0001-request.md     ← Approved Research Request (Research Gate)
    ├── source-map.md                ← Source Map + source-coverage report
    ├── research-draft.md            ← Bounded initial research (Draft)
    ├── challenge-review.md          ← Independent Challenge artifact
    ├── founder-review-record.md     ← Founder Review record
    └── research-result.md           ← Structured Research Result (Current Authoritative v1)
```

The expanded CIW file tree (papers, earnings-update packages, monitoring state, Obsidian sync) is **deferred** to later slices (CIW-CONCEPT §6). This tree is the pilot floor — six artifacts, one per lifecycle step, plus this design.

## 5. Research Request — CRR-2026-0001 (draft specification)

Per CIW-REQUEST-CONTRACT §3, the request to be drafted (after FD-CIW-011) must carry at minimum:

| Field | Value |
|---|---|
| `request_id` | `CRR-2026-0001` |
| `company_id` | MSFT — Microsoft Corporation (NASDAQ: MSFT); entity identity from Shared Core |
| `universe` | `US-listed common stocks (v0.3)` — per DNA-017 approved text (Required Change #3) |
| `origin` | `source_system: investment-intelligence-platform; trigger_type: founder_commission (pilot per FD-CIW-009/FD-CIW-011); originating_themes: none (portfolio-blind pilot)` |
| `research_question` | **Primary:** "Does Microsoft possess durable business quality and competitive advantage sufficient to support its current enterprise value — assessed at initial depth?" (valuation element answered qualitatively via Modules G/H/M only; no deterministic valuation output) |
| `secondary_questions` | (a) How durable and how wide is the moat, and what is the trend? (b) What does the current price imply about market expectations, and are those expectations demanding? (c) What are the principal permanent-loss mechanisms and their likelihood? |
| `known_evidence` | Existing FO pipeline data for MSFT (Phase 8 classification is canonical and NOT re-derived by CIW — CONCEPT §3.1) |
| `known_counterevidence` | To be stated explicitly at request time (must be visible from the start — REQUEST-CONTRACT §3) |
| `required_depth` | `initial` (first slice) |
| `required_outputs` | `structured_research_result` only (Master Paper deferred) |
| `applicable_modules` | A, B, C, D, E, F, G, H, I, J, K, L, M — all at **initial depth** |
| `justified_omissions` | **N** Valuation: deterministic valuation contracts not approved; advisory ranges deferred to later slice. **O** Margin of Safety: depends on N. **P** Opportunity Cost: depends on N. **Q** Monitoring: monitoring spec deferred to later slice (CIW-CONCEPT §6; Required Change #9) |
| `priority` | Pilot — workflow validation (Theme-first queue discipline, Constitution §14) |
| `founder_constraints` | Time box: single bounded research pass; draft ≤ 1 research session; focus: business quality + moat durability + what price implies; no valuation verdict; no recommendation language |
| `portfolio_blind` | `true` (Constitution §23.8.1) — no holdings, positions, cost basis, or transaction history supplied |
| `approval_status` | `Draft` → `Approved` (Founder, Research Gate) |
| `authority` | `autonomous_investment_decision: false; founder_final_authority: true` |

### Module depth notes (RESEARCH-FRAMEWORK §3 — applicability-based, never a mandatory long-report checklist)

- A–D at full initial depth (business quality + moat are the pilot focus).
- E (management/governance): initial — proxy/compensation statement required by source gate when E in scope (REQUEST-CONTRACT §4.4).
- F (financial forensics): initial — 5+ years where available, real 10-K data.
- G (owner earnings): advisory estimates with explicit assumptions + calculation lineage; **not** an official output.
- J (normalization/stress): initial — mild/severe cases only, no thesis-break determination (that requires predeclared condition or Founder decision — LIFECYCLE §3).
- K (permanent loss): ranked risks only.
- M (variant perception): qualitative — what the price implies; no reverse-DCF valuation output.

## 6. Independent Challenge Mechanism (QUALITY-GATES §1 — MANDATORY separation)

The challenge is a **required** step for pilot publication (QUALITY-GATES §3). Design:

| Property | Design |
|---|---|
| Executor | Parent (DeepSeek V4 Flash) in the main session — produces the Draft |
| Reviewer | **Sol Medium subagent** (`gpt-5.6-sol` via `openai-codex`, delegation model per 3-Tier routing) via `delegate_task` — isolated context, no access to executor's framing |
| Fallback | Sol Medium unavailable → `openai/gpt-5.6-luna` (openrouter, reasoning=high). **No fallback to self-review or no-review** — publication is blocked if no eligible reviewer (QUALITY-GATES §1) |
| Direct source inspection | Reviewer MUST inspect cited sources and calculations directly (SEC EDGAR filings, transcripts); findings cannot be copied solely from the writer's summary |
| Provenance disclosure | Review artifact identifies executor and reviewer identities/contexts and states what was independently verified |
| Challenge questions | RESEARCH-FRAMEWORK §7 final challenge (three assumptions driving value, least-supported assumption, reversing fact, confirmation bias, skeptical short-seller argument, knowledgeable-operator argument, mispricing vs uncertainty vs distress vs optimism, rational private owner, market-closed-10-years, superior expected return) |
| Output | `challenge-review.md` — PASS / FAIL / REVIEW REQUIRED per gate; advisory to Founder; **council/committee agreement is not Founder approval** (QUALITY-GATES §3) |

**Gate result states (QUALITY-GATES §2):** `Pass` → proceeds to Founder Review; `Fail` → returns to executor with findings (bounded rework ≤ 2 cycles, QUALITY-GATES §6); `Review Required` → human review. A gate can never be bypassed by claiming "non-material".

## 7. Quality Gates — Minimum Checks (QUALITY-GATES §2)

Before `Independent Review` → `Founder Review` transition, the research must pass: source-coverage, primary-source, contradiction, unsupported-claim, stale-source (Constitution §8 three-year rule), accounting red-flag, valuation-assumption (explicit/versioned, advisory), deterministic-calculation lineage (where calculations exist), per-share economics, dilution, thesis-falsification (invalidation conditions stated), artifact-lineage, authority (no AI/Cron authoritative transitions), scope (within approved request).

The research draft must carry the **completion standard** (QUALITY-GATES §4): scope completed, sources reviewed, artifacts produced, calculations performed, checks run (list), limitations, unresolved risks, disagreements, deviations from the approved request, **review status** — a completion claim without review status is incomplete.

## 8. Founder Review (PUBLICATION-STANDARD §1, §7)

- Founder reviews the challenged draft + challenge artifact + quality-gate results.
- **Every canonical change requires explicit Founder approval** — thesis status, valuation figures (advisory), confidence, classification impacts (PUBLICATION-STANDARD §1). Approval must identify the exact artifact (Constitution §21); casual agreement is not approval.
- Founder approval → `Published` / Current Authoritative v1 (structured result).
- **Class C (automatic canonical publication) is disabled** during the pilot (PUBLICATION-STANDARD §2). The deterministic-metadata allowlist is empty for the first slice (Founder has not approved any allowlist entry).

## 9. Structured Research Result (RESULT-CONTRACT)

`research-result.md` must carry all RESULT-CONTRACT §2 fields: `research_id`, `company_id` + `universe` + `universe_version`, `as_of_date`, `research_version`, `research_status` (Published only after Founder approval), `investment_classification` (advisory, Founder-decided — never mechanically set), `thesis_status` (approved Thesis Lifecycle value), `confidence` (qualitative, evidence-linked), dimension summaries (business quality, moat, balance sheet, management, owner earnings, valuation context (advisory), permanent-loss mechanisms, monitoring indicators), `unresolved_questions` (explicit — honest empty states), `theme_feedback` (RESEARCH-FRAMEWORK §8), `artifact_references`, `review_status`, `source_map` (per-source status), `claim_lineage` (claim-level evidence references + calculation lineage), `portfolio_blind: true`.

**Source-coverage discipline (RESULT-CONTRACT §3):** any `missing_required` or `failed_retrieval` forces the result to `Incomplete` or `Review Required` — a polished report cannot appear complete despite missing primary sources. Contradictions remain visible; never averaged away. No evidence found ≠ evidence of non-existence.

## 10. Non-Scope (hard constraints — CIW-CONCEPT §6/§7, FD-CIW-001..007)

The first slice **does NOT** include (and FD-CIW-011 must NOT authorize):

- Cron jobs of any class (FD-CIW-005 — implementation still requires separate authorization; this slice runs fully manually).
- Obsidian synchronization (FD-CIW-006 — narrative layer deferred).
- Database migration or schema changes (no `src/database/**`, no migrations).
- New repository or separate Hermes profile (FD-CIW-002).
- Earnings-update / re-underwriting automation.
- Expanded file tree, Master Research Paper, presentations.
- Deterministic valuation calculation contracts (deferred — advisory context only).
- Class C publication, deterministic-metadata allowlist.
- Any change to official Candidate, Thesis, Theme, Moat, Earnings-Quality, Value-Trap, or Investment state — CIW research completion is **not** investment approval (LIFECYCLE §4).
- Any code changes to existing pipeline/frontend modules.

## 11. Verification — Slice Completion Standard

The first slice is complete (CIW-CONCEPT §6 + QUALITY-GATES §5) only when:

1. All six artifacts exist in `docs/ciw-pilot-msft/` (request approved → source map → draft → challenge → founder review → result).
2. Quality gates (§7) all passed with no `Fail` outstanding and no bypass claims.
3. Independent Challenge completed with provenance disclosure; publication-blocked path never triggered.
4. Founder approval recorded for the request (Research Gate), the publication (Publisher), and every canonical change.
5. `research-result.md` reaches `Published` with `portfolio_blind: true` and complete source-coverage report.
6. **Constraint check:** the slice ran with zero Cron jobs, zero DB/schema changes, zero new repos/profiles, zero Obsidian sync, zero earnings automation.
7. Evidence log updated (per v3.7.1 milestone-evidence-log practice) with the verification tags (TEST_VERIFIED / STATIC_OBSERVATION / EXTERNAL_NOT_TESTED / INFERENCE).

**Pilot outcome framing:** a successful slice validates the CIW workflow's feasibility — nothing more. Any inference that the methodology is economically validated, or that MSFT is endorsed, is explicitly rejected (RESEARCH-FRAMEWORK §1 minority warning).

## 12. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Reviewer unavailable → publication blocked | Planned fallback Luna; if both unavailable, slice pauses at Independent Review — no self-review shortcut (QUALITY-GATES §1) |
| Source retrieval failures (paywalls, EDGAR issues) | `justified-absent` / `failed_retrieval` statuses recorded, not hidden; result forced to Incomplete/Review Required (RESULT-CONTRACT §3) |
| Scope drift into full valuation / full paper | Modules N–Q omitted with justification; `founder_constraints` time box; scope gate in quality checks |
| Draft too long (long-report ≠ deep research — DNA-019) | Initial depth only; every module justified by decision value; omissions allowed with reason |
| Conflating pilot success with methodology validity | Minority warning restated in design, result, and closeout |
| Concurrent-session working-tree mutation | Re-check `git status` before/after each commit; anchor patches on unique content |

---

*Draft v0.1 (FD-CIW-010). Sources: CIW-CONCEPT §6, CIW-LIFECYCLE §6–§7, CIW-REQUEST-CONTRACT §2–§7, CIW-QUALITY-GATES §1–§6, CIW-RESULT-CONTRACT §2–§6, CIW-PUBLICATION-STANDARD §1–§3, CIW-RESEARCH-FRAMEWORK §1–§8; FD-CIW-001..010.*
<!-- 2026-08-03 01:16 UTC+7 -->
