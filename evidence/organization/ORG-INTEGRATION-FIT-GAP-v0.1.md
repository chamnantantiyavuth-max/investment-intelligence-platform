# IIP × Hermes Organization Pack — Integration Fit-Gap Analysis

**Status:** PROPOSED — FOUNDER REVIEW REQUIRED
**Version:** 0.1 (draft for review — NOT approved, NOT canonical)
**Date:** 2026-08-05
**Author:** IIP profile (Hermes Agent), read-only discovery pass
**Source pack:** `C:\Users\Admin\Desktop\Antigravity\_staging\IIP_Hermes_Organization_Pack_v0.1` (34 files, all read)
**Scope:** READ-ONLY. No profiles installed, no local Hermes config modified, no production code/schema/Constitution changed, no pack document promoted. All integration decisions below require explicit Founder approval via the companion FD proposal (`operational/FD-PROPOSAL-IIP-HERMES-WORKFORCE-v0.1.md`).

---

## 1. Executive Summary

The pack is **substantially well-designed as a workforce operating manual** (good alignment with the Blind Portfolio Rule, Two-Tier Autonomy, Unresolved-Decision Protection, dissent preservation, and artifact-based source of truth), but it **cannot be adopted as-is**. It contains one **second-constitution artifact**, one **state-model conflict that collapses the canonical two-axis Theme governance**, one **parallel research state machine** the project explicitly forbids (CIW-LIFECYCLE §1: "reuse approved states, do not create a parallel machine"), and **four new Hold authorities plus an IC administrative gate that are not approved anywhere in the current authority hierarchy**.

**Verdict: integrate selectively as a subordinate operational standard** (`AI-ORGANIZATION-OPERATING-STANDARD-v0.1.md`), after mandatory rewrites of the state model and authority additions, with a **thin-profile topology (Option A) and a repo-based kanban** (the Hermes kanban toolset is disabled in the current profile config). Do NOT create 20 persistent profiles. Do NOT promote the pack's own Constitution.

Findings summary: **4 CRITICAL · 9 HIGH · 6 MEDIUM · 4 LOW** (register in §5).

---

## 2. Startup and Authority Inspection Results (Verify-First)

| Check | Result | Evidence |
|---|---|---|
| Active profile | **iip** (running) | `hermes profile list` — ◆iip, deepseek-v4-flash, running |
| project-workflow skill version | **3.7.1** | skill frontmatter (`version: 3.7.1`), readiness `available` |
| Skill loaded | Yes | skill_view returned full SKILL.md |
| Repository root | `C:\Users\Admin\Desktop\Antigravity\investment-intelligence-platform` | confirmed |
| Source pack | EXISTS, **outside** repo (`_staging\IIP_Hermes_Organization_Pack_v0.1`, 34 files) | find listing |
| Git state | **clean**, branch `main` → `origin/main`, HEAD `be93aff` (137 commits) | git status/log |
| Latest FD | **FD #53** (69 total: #1–53 + FD-CIW-001..016) | `operational/FOUNDERS-DECISIONS.md` |
| Next allowed action | UI redesign (FD #51 Research Desk) COMPLETE/ACCEPTED; A-01 deferred (FD #52); C-04/C-05/M-02 closeout leftovers; CIW paused (Q1-FY27) | `PROJECT_STATE.md` |
| Active Holds | **None** (no Hold mechanism exists in the project today) | PROJECT_STATE "No active blockers"; grep of governance docs |
| Constitution | v0.4 header; amendment records v0.2–v0.5 (Blind Portfolio Rule v0.5) | `02-PROJECT-CONSTITUTION.md` |
| Operating Model | v0.1 + §5.7 CIW (v0.2) — Dual Intelligence paths | `project-definition/INVESTMENT-INTELLIGENCE-OPERATING-MODEL.md` |

### 2.1 Local Hermes runtime facts (inspected, not assumed)

| Fact | Value | Implication for the pack |
|---|---|---|
| Profile root | `C:\Users\Admin\AppData\Local\hermes\profiles\iip\` — **NOT** `~/.hermes/profiles/iip/` (that path holds only `default`) | Startup references in the pack's installation docs must use the real path; the SOUL.md FD-HERMES-008 "CANONICAL: ~/.hermes/shared/SOUL.md" reference is **stale** (actual shared root is `AppData\Local\hermes\shared\`). Pre-existing drift, out of scope, flagged. |
| Profile composition | No inheritance/includes/symlinks. Each profile = flat copy of canonical `shared\SOUL.md` (24.7 KB) + spliced `shared\project-context\<profile>.md`, per `sync-governance.py`; `profile.yaml` is description-only | Thin profiles are copy-composed; a new profile requires a project-context file + addition to the sync script's `PROFILES` list + watchdog coverage. |
| Existing profiles | 8 already exist (iip, capcmd, fxtrading, notebooklm, antigravity-orchestrator, close-system-learning-lab, profirm, default) | Multi-profile runtime is proven; 20 more is feasible but maintenance-heavy. |
| Model routing | One primary (`deepseek-v4-flash`), one delegation model (`gpt-5.6-sol` via openai-codex), fallback luna. `delegate_task` reads ONE `delegation.model` — **no per-call override** | Role "independence" is procedural (prompt/session separation), **not model-based**, for any profile that runs Flash. Governance audits MUST still route to Sol Medium (FD-HERMES-007) — an in-house Flash "Internal Auditor" profile cannot satisfy that rule by itself. |
| Kanban toolset | **DISABLED** (`agent.disabled_toolsets: [..., kanban, project, ...]`; `plugins.disabled: [kanban]`) | The pack's single-board kanban cannot use the Hermes kanban tool without a config change (runtime implication → requires approval). Repo-based markdown board is the zero-config alternative. |
| Memory isolation | Per-profile memories (3,500 chars memory / 2,000 user), per-profile state.db | Real isolation benefit of separate profiles; also the main drift risk (20 stores to reconcile). |
| Delegation/concurrency | max_concurrent_children 10; MOA enabled (gpt-5.5 + deepseek-v4-pro reference models) | 10 principals + subagents fits concurrency ceiling; MOA is an existing multi-agent mechanism (not recommended for first pass). |
| Disabled skills | includes `multi-profile-infrastructure`, `project-state-sync`, `governed-schedule-review`, `founder-review-workflow`, etc. | Any profile-topology or schedule-review implementation skill is currently disabled — a config decision for Founder. |

### 2.2 Pre-existing drift observations (flagged, NOT fixed — read-only task)

1. `~/.hermes/shared/SOUL.md` path in SOUL.md FD-HERMES-008 is stale; real canonical is `AppData\Local\hermes\shared\SOUL.md` (exists; version string check vs v3.7.1 pending — the file references differ from the skill's v3.7.1 text).
2. `~/.hermes/unified-SOUL-v3.1.md` still says "project-workflow v3.6" (stale vs skill 3.7.1).
3. `sync-governance.py` `CUR_VERSION = "Project Workflow v3.7"` (stale vs 3.7.1) and its profile list excludes `profirm`/`default`.
4. Constitution file header says v0.4 while amendment records run through v0.5 (Blind Portfolio Rule).
5. `PROJECT_STATE.md` closeout_status `in_progress` with C-04/C-05/M-02 leftovers — the org-pack workstream must not collide with these (separate path).

---

## 3. Constraint Compliance Check (per task constraints A–I)

| Constraint | Result |
|---|---|
| A. Existing authority unchanged; pack subordinate | ⚠️ Pack must be renamed from "Constitution" and its amendment rule rewritten to reference Constitution §21 (see F-01). |
| B. No second Constitution | ❌ **F-01** — `00-IIP-ORG-CONSTITUTION-v0.1.md` is a parallel constitution (own amendment rule §15, own authority claims). Must be renamed `AI-ORGANIZATION-OPERATING-STANDARD-v0.1.md` and demoted to an operational artifact under `operational/hermes-organization/`. |
| C. Preserve two-axis Theme governance | ❌ **F-02** — pack §5.3 "Governance State" is a flat 5-value axis that collapses Approval Status × Monitoring Status. Direct violation of Constitution §5 + THEME-MODEL §3 + constraint C. |
| D. Roles implement the approved logical Operating Model | ✅ Alignable — every role maps to an existing logical responsibility (ROLE-MAPPING doc); no product-topology redesign needed. |
| E. Runtime topology critical evaluation | ✅ Option A (10 thin Principals + bounded Assistant subagents) recommended; Option B (20 persistent) feasible but not justified; Option C viable for pilot (§7). |
| F. Thin runtime profiles | ✅ Repo stays canonical; profiles hold loader + identity + role reference only. |
| G. Blind Portfolio Rule | ✅ Pack §2 aligns with Constitution §23.8.1. No portfolio data anywhere. |
| H. Template non-duplication | ⚠️ 3 templates REJECT (duplicate/conflicting), 5 REUSE/EXTEND, 4 EXTEND EXISTING, 3 CREATE NEW — see TEMPLATE-DISPOSITION doc. |
| I. Formal authority changes need explicit Founder review | ❌ **F-03/F-04** — Holds + IC gate + card-movement rights are new authorities with zero current approval. All routed to the FD proposal. |

---

## 4. Role-by-Role Mapping (summary — detail in `ROLE-MAPPING-v0.1.md`)

| # | Proposed role | Approved logical responsibility (Operating Model / specs) | Verdict |
|---|---|---|---|
| 1 | Founder Chief of Staff | Research Orchestrator (OM §3); Synthesis & Decision Support coordination; Founder Decision Gate queueing (OM §9) | ALIGN — coordinator only, not approver (pack enforces) |
| 2 | IC Secretary | Founder Decision Gate recordkeeping (OM §9); CIW founder-review-record precedent; FD register custody | ALIGN with rename: no "Investment Committee" decision body exists (F-08) |
| 3 | Commodity Product Analyst | OM §5.3 Product Analysis (ETFs/funds/indices/commodities — V1+ path); Close System product suitability (Constitution §15) | ALIGN — bounded research only; V1+ path, no production inputs today |
| 4 | Global Macro Strategist | OM §5.1 Macro Analysis (V1+); Momentum §6.1 Market Regime; Close System Macro Regime | ALIGN — bounded research; regime methodology not yet approved |
| 5 | Equity Alpha Analyst | OM §5.4 Company + §5.5 Earnings & Change; Momentum §6.3–6.8; FO pipeline (Phase 8); CIW deep research (Phase 11, deferred) | ALIGN — must NOT reopen paused CIW path (F-09) |
| 6 | Options Strategist | Close System Instrument Structure (Constitution §15); OM §5.3 | ALIGN — research-only; no live order authority (pack enforces) |
| 7 | Chief Risk Officer | Independent Challenge (OM §7, both paths); Close System risk dimensions; Phase 8 §4 challenge domains | ALIGN — overlaps existing challenge function; must not duplicate it (F-10) |
| 8 | Quant & Model Validator | Shared Core deterministic verification; VERIFICATION-DOCTRINE; project-workflow Evidence QA + mutation testing | ALIGN — maps to existing verification discipline |
| 9 | Data Steward | Shared Intelligence Core: Evidence Acquisition, Data Validation, source registry, provenance, Data Confidence (Constitution §4; EVIDENCE-MODEL §5/§9) | ALIGN — Shared Core owns the capability; role = human-reviewable operator of it |
| 10 | Internal Auditor / Red Team | Audit discipline: FD-HERMES-007 (Sol Medium delegation), governance-audit skill, LLM Council, Independent Challenge adversarial review | ALIGN WITH CONSTRAINT — same-model profile cannot self-audit; audits route via Sol Medium (F-11) |

---

## 5. Finding Register (severity → disposition)

Legend — severity: **CRITICAL** (blocks adoption), **HIGH** (must be resolved before pilot), **MEDIUM** (resolve before full activation), **LOW** (cosmetic/note). Columns: 1) existing authority source, 2) proposed addition, 3) alignment, 4) conflict/duplication, 5) materiality, 6) required correction, 7) FD required?, 8) constitutional amendment?, 9) recommended location, 10) runtime implication.

### CRITICAL

**F-01 — Second Constitution.** Pack `00-IIP-ORG-CONSTITUTION-v0.1.md` (394 lines) is a self-contained constitution with its own §15 amendment rule and §3 Founder-authority enumeration. Existing authority: Constitution §1–§23 + §21 (sole amendment authority). Conflict: two amendment authorities → ungovernable drift. Materiality: HIGH (governance). Correction: rename to `AI-ORGANIZATION-OPERATING-STANDARD-v0.1.md`; rewrite header/status to "Proposed Operational Standard, subordinate to Constitution + FDs"; replace §15 with a pointer to Constitution §21 + `operational/CHANGE-CONTROL-AND-APPROVAL.md`; remove any clause that implies constitutional standing. FD required: YES (as part of the org-pack FD). Constitutional amendment: NO (it is demoted, not merged). Location: `operational/hermes-organization/AI-ORGANIZATION-OPERATING-STANDARD-v0.1.md`. Runtime: none (docs-only).

**F-02 — Governance-state collapse (two-axis Theme governance).** Pack §5.3 defines flat "Governance State" {Experimental, Proposed, Approved for Official Tracking, Rejected, Archived} used by kanban cards, Theme Hypothesis Card template, and role prompts. Existing authority: Constitution §5 + THEME-MODEL §3 define **two independent axes** — Approval Status {Detected Hypothesis, Experimental, Under Human Review, Approved, Rejected} × Monitoring Status {Not Monitored, Active Monitoring, Dormant, Archived} — plus lifecycle (6 stages), confidence, crowding as separate axes. Conflict: collapsing these axes violates Constitution §5 ("Lifecycle, confidence, crowding, and Approval Status, and Monitoring Status are separate dimensions"), constraint C, and the CIW precedent (CIW-LIFECYCLE §1: reuse approved states, no parallel machine). Materiality: CRITICAL (domain state semantics). Correction: delete pack `governance_state`; kanban/artifact fields carry `approval_status` + `monitoring_status` mapped to canonical values; any transition to Approved = Founder-only (already canonical). FD required: YES (approve the corrected state contract). Constitutional amendment: NO (we restore canonical semantics, not change them). Location: rewrite in AI-ORGANIZATION-OPERATING-STANDARD §5 + KANBAN-CONTRACT §3. Runtime: repo-board fields only.

**F-03 — Four new Hold authorities.** Pack §10 (ORG-CONSTITUTION) + AUTHORITY-MATRIX grant Data Hold / Validation Hold / Risk Hold / Governance Hold with "only issuing profile clears, unless Founder overrides." Existing authority: **no Hold mechanism exists** in Constitution, FDs, or specs; the only "block" precedents are CIW Research Gate (Founder-approved request gates research) and project-workflow escalation/regression budgets. Conflict: new authority to pause promotion/canonical publication + new Founder override path. Materiality: HIGH (authority). Correction: do NOT assume approved (constraint I). Propose as explicit FD authority change scoped to the org workflow: Hold = advisory pause on *org-workflow promotion* (never a veto on domain state); Hold record fields as in pack §10; Founder override recorded per Constitution §21 with accepted residual risk; Hold issuers = the 4 roles; Hold does not erase work. FD required: YES (explicit authority grant). Constitutional amendment: NO if scoped to operational workflow only; YES if Holds ever gate canonical domain state (recommend: keep Holds out of canonical state machine → no amendment). Location: AI-ORGANIZATION-OPERATING-STANDARD §10 + AUTHORITY-MATRIX. Runtime: Hold registers live in repo (e.g., `operational/hermes-organization/holds/`); no code change.

**F-04 — IC Secretary administrative completeness gate + card-movement rights.** Pack AUTHORITY-MATRIX §3.2 + KANBAN §6: IC Secretary alone moves a packet into Founder Review and may reject administratively. Existing authority: no IC entity; Founder review is direct (CIW precedent: `founder-review-record.md` compiled by the executor + Founder approves). Conflict: new workflow gate with real blocking power. Materiality: HIGH (workflow authority). Correction: approve via FD as an org-workflow gate (administrative completeness only, no investment judgment — pack already says this); align packet fields with CIW founder-review-record precedent (exact artifact + version + hash + explicit non-meaning). FD required: YES. Constitutional amendment: NO. Location: AI-ORGANIZATION-OPERATING-STANDARD §D5 + KANBAN-CONTRACT §6.

### HIGH

**F-05 — Parallel "Research Lifecycle State."** Pack §5.2 {Observation, Hypothesis, Draft, Reviewed, Validated, Monitoring, Superseded, Archived} — a second research state machine. Existing authority: Thesis Lifecycle (CANDIDATE §3.3.2), Research State (§3.3), CIW workflow statuses (CIW-LIFECYCLE §2, explicitly mapped), artifact states (CIW-LIFECYCLE §5). Conflict: violates "no competing official state machine" (CIW-LIFECYCLE §1). Correction: delete the parallel model; artifact maturity maps to CIW artifact states (Draft → Reviewed Draft → Founder-Reviewed → Current Authoritative → Superseded/Archived); thesis maturity uses Thesis Lifecycle. FD: YES (state contract). Amendment: NO. Location: AI-ORGANIZATION-OPERATING-STANDARD §5 + TEMPLATE-DISPOSITION. Runtime: none.

**F-06 — Theme Hypothesis Card template conflicts.** `templates/05-THEME-HYPOTHESIS-CARD.md` uses pack governance/lifecycle states (§F-02/F-05) and omits Monitoring Status. Existing: THEME-MODEL §7 Theme Card (why now, evidence, contradicting, missing, alternatives, lifecycle, confidence, crowding, approval, monitoring, leaders/challengers/beneficiaries). Correction: REJECT as duplicate; reuse canonical Theme Card; org card = a thin intake view referencing THEME-MODEL §7 fields with both axes. FD: NO (template disposition via org-pack FD). Location: `operational/hermes-organization/templates/` as intake form only.

**F-07 — Template duplication classes.** 5 pack templates duplicate/conflict with canonical artifacts: 02-EVIDENCE-RECORD (vs EVIDENCE-MODEL taxonomy), 04-DEEP-DIVE-RESEARCH-PAPER (vs CIW-RESULT-CONTRACT + Phase 8 §8 13-section package; Master Paper deferred), 11-FOUNDER-DECISION-RECORD (vs canonical FD register + vault fd-register + CIW founder-review-record), 13-AUDIT-FINDING (vs governance-audit evidence format), 14-CHANGE-REQUEST (vs CHANGE-CONTROL-AND-APPROVAL 12-field proposal). Full disposition: TEMPLATE-DISPOSITION doc. Correction: map each to canonical source; no third decision register. FD: NO (disposition). Location: `operational/hermes-organization/templates/` (mapped, thin).

**F-08 — Misleading role names.** "Investment Committee Secretary" implies a decision committee that does not exist (Founder is the sole decision authority, OM §9; IC precedent is Independent Challenge + cross-functional review, not a voting body). "Chief Risk Officer / Chief of Staff" C-suite titles imply firm authority beyond research organization. Correction: keep working titles but add a definitions clause: IC = advisory review forum (no vote, no quorum, no collective decision); C-suite titles are research-organization labels only; the only approver is the Founder. FD: NO (naming convention, part of standard). Location: AI-ORGANIZATION-OPERATING-STANDARD §1 glossary.

**F-09 — Equity Alpha role adjacency to paused CIW.** The role's deep-research responsibilities overlap CIW (Phase 11, PAUSED; next decision point Q1-FY27). Risk: org-pack activation silently reopens the paused path. Correction: explicit clause — org-pack roles perform **bounded research on published/synthetic/historical artifacts only**; any CIW-path deep research requires a separate named FD superseding FD #44 (same gate as today). FD: YES (boundary clause). Amendment: NO. Location: ROLE-MAPPING (Equity Alpha row) + AI-ORGANIZATION-OPERATING-STANDARD §2.

**F-10 — CRO vs existing Independent Challenge duplication.** Independent Challenge (OM §7, Phase 8 §4, CIW QUALITY-GATES §3) is an approved function with mandatory operational independence (executor ≠ reviewer, Sol Medium for governance audits). A Flash-based CRO profile adds a *second* challenge channel. Correction: CRO = named operator of the existing challenge function for org workflows (artifacts: Risk Challenge Memo maps to Phase 8 challenge domains + Close System risk dimensions); challenge execution for material items still requires separate context/model per QUALITY-GATES §1. FD: YES (role definition). Location: ROLE-MAPPING.

**F-11 — Internal Auditor vs FD-HERMES-007 delegation.** Governance audits MUST delegate to Sol Medium (different model family); an in-house Flash auditor is not an independent auditor by the project's own rule. Correction: Internal Auditor profile = audit **orchestrator** (scope, evidence assembly, remediation tracking); actual governance audit execution routes through `delegate_task` → gpt-5.6-sol (fallback luna) per FD-HERMES-007; pack's GOVERNANCE HOLD stays advisory. FD: YES. Amendment: NO. Location: ROLE-MAPPING + AI-ORGANIZATION-OPERATING-STANDARD §8.

**F-12 — Kanban runtime gap.** Pack assumes a single canonical board; Hermes kanban toolset is disabled in iip config. Correction: repo-based board (markdown + YAML card contract in `operational/hermes-organization/kanban/`) with single-writer discipline (CoS Assistant) and the card fields as in KANBAN-CONTRACT §3 (minus F-02 fixes); optionally enable the Hermes kanban toolset later via config change (separate approval). FD: YES (runtime decision). Amendment: NO. Location: `operational/hermes-organization/kanban/`. Runtime: file-level concurrency — same risk class as existing cron writes; mitigate with writer lock discipline.

**F-13 — Materiality scale M0–M4 vs canonical "material change."** Pack KANBAN §4 introduces M0–M4; CHANGE-CONTROL-AND-APPROVAL defines material change. Correction: define M0–M4 as an operational triage scale subordinate to the canonical material-change definition (any M3/M4 = material → full CHANGE-CONTROL proposal + Founder gate). FD: NO. Location: KANBAN-CONTRACT §4.

### MEDIUM

**F-14 — Same-model independence limits.** All 10 principals would run deepseek-v4-flash (config has one primary model). "Independent challenge/validation" between Flash profiles is weaker than Sol Medium review (correlated errors). Correction: ROLE-MAPPING marks which review steps require Sol Medium (governance audit, Phase 2R, material Independent Challenge per QUALITY-GATES §1); intra-org challenge between Flash roles is advisory-lite until a model-separation FD exists. FD: YES (review-routing contract). Location: ROLE-MAPPING review dependencies column.

**F-15 — Profile sync maintenance.** sync-governance.py composes profile SOULs; 10 new profiles require: 10 project-context files, PROFILES list extension, watchdog coverage (cross-profile-sync-watchdog.py), and per-profile memory/USER.md initialization. Risk: drift if sync script updated incorrectly; `multi-profile-infrastructure` skill disabled. Correction: sync extension is part of Stage 3 activation (INTEGRATION-PLAN), gated behind Founder approval; keep profiles thin so sync surface stays minimal. FD: YES (activation stage). Location: `installation/` docs. Runtime: script edit + watchdog.

**F-16 — Memory/context drift across 20 role stores.** 20 × (3,500-char memory + session DBs) → reconciliation burden; role prompts duplicated across profiles drift from repo. Correction: canonical role content ONLY in repo (`operational/hermes-organization/roles/`); profile SOUL references repo path (startup contract); memories restricted to operational notes, never domain truth (matches DNA-018: structured source of truth in application, not chat/memory). FD: NO. Location: PROFILE-STARTUP-CONTRACT.

**F-17 — Assistant authority leakage vectors.** Mitigated well by pack §9 + Assistant Universal Rules (no approve/certify/sign/clear-hold/governance-change; `ASSISTANT DRAFT — PRINCIPAL REVIEW REQUIRED` label). Residual: label is prose (not mechanically enforced); card movement under "Principal instruction" can be ambiguous; prompt-injection via artifacts (SECURITY-AND-UNTRUSTED-CONTENT). Correction: startup contract mandates the label on every substantive output; Assistant handoff = ASSISTANT-WORKLOG template; Principal review gate is mandatory (pack already); audit samples assistant outputs (Internal Auditor). FD: NO (enforcement clause). Location: PROFILE-STARTUP-CONTRACT + KANBAN-CONTRACT.

**F-18 — Failure/degraded operation undefined per role.** Constitution §23.7 requires failure modes (retry/queue/fallback/incomplete/manual/disable). Pack roles define escalation triggers but not failure behavior. Correction: ROLE-MAPPING adds §23.7 failure contract per role (default: queue + manual review; deterministic recordkeeping unaffected). FD: NO (compliance clause). Location: ROLE-MAPPING.

### LOW

**F-19 — Daily/Weekly cadence vs existing cron.** Pack workflow defines daily/weekly cadence; existing automation = CIW Class A monitor (weekly, approved) + daily-review cron (evidence/DAILY-REVIEW-*). Correction: org cadence runs as scheduled tasks only where each task has its own named authorization (FD-CIW-005 discipline); first pass = manual/ad-hoc cadence during pilot, no new cron. FD: YES (cadence clause) — see INTEGRATION-PLAN Stage 2. Location: AI-ORGANIZATION-OPERATING-STANDARD §workflow.

**F-20 — "Approved for Official Tracking" terminology.** Pack §4.2 uses this phrase; canonical Approval Status value is `Approved` (THEME-MODEL §3.1). Correction: map phrase → `Approved` in the glossary; keep the pack's clarification that approval ≠ buy recommendation (matches Constitution §6). FD: NO. Location: glossary.

**F-21 — WIP limits as new operational policy.** Pack KANBAN §5 (1 M2/M3 per principal, etc.). Reasonable operational policy; no conflict. Adopt with materiality scale fix (F-13). FD: NO. Location: KANBAN-CONTRACT.

**F-22 — Pack master file duplication.** `IIP-HERMES-ORGANIZATION-PACK-v0.1.md` (3,426 lines) is a faithful concatenation of all constituents (verified via heading map + embedded-00 diff). Correction: do NOT copy the combined edition into the repo (single-source discipline); keep modular files only; the combined edition stays in _staging as the source-of-record. FD: NO. Location: n/a. Runtime: n/a.

---

## 6. Risk Register (task-required risk list)

| Risk | Assessment | Mitigation |
|---|---|---|
| Authority conflicts | F-01/F-03/F-04 — second constitution + new Holds/gates | Demote to standard; FD-grant Holds/gates with explicit scope; no amendment unless Holds touch canonical state |
| State-model conflicts | F-02/F-05/F-06 — governance collapse + parallel lifecycle | Rewrite to canonical axes; artifact states per CIW-LIFECYCLE §5 |
| Duplicated templates | F-07 — 5 of 16 | TEMPLATE-DISPOSITION: REUSE/EXTEND canonical; REJECT duplicates |
| Duplicated decision records | F-07 (11-FOUNDER-DECISION-RECORD) | Single canonical FD register + vault fd-register; pack form = intake only |
| Misleading role names | F-08 | Glossary clause: IC advisory-only; titles research-org labels |
| Role overlap | F-09/F-10 — Equity↔CIW; CRO↔Challenge | Boundary clauses; roles = operators of existing functions, not new functions |
| Separation-of-duty weaknesses | F-11/F-14 — same-model audit/challenge | Sol Medium routing for audit + material challenge; Flash-vs-Flash = advisory |
| Assistant authority leakage | F-17 | Label contract + Principal gate + audit sampling |
| Memory/context drift | F-16 | Thin profiles; repo-canonical prompts; restricted memories |
| Profile synchronization risk | F-15 | Sync-script extension gated; watchdog coverage |
| Prompt size / bootstrap cost | LOW | ~25 KB shared SOUL + ~6 KB role prompt per profile; negligible disk; maintenance is the real cost |
| Audit-lineage requirements | MEDIUM | Canonical artifact header per pack §11 + profile identity in lineage (Constitution §23.5) |
| Failure / degraded operation | F-18 | §23.7 failure contract per role |
| Scheduling / concurrency | F-19/F-12 | No new cron without named authorization; repo-board writer discipline; concurrency ≤ delegation ceiling |

---

## 7. Runtime Topology Analysis (Options A/B/C)

| Criterion | A — 10 Principals + bounded Assistant subagents (RECOMMENDED) | B — 20 persistent profiles | C — One orchestrator + role skills/prompts |
|---|---|---|---|
| Governance clarity | High — 10 named authorities, Assistants clearly subordinate | Highest on paper — every role a first-class identity | Lower — roles are prompt-scoped, authority implicit |
| Independence | Procedural (session separation) + Sol Medium for material review | Procedural; same-model caveat applies to all Flash profiles | Weakest — same memory/session space; must force delegate_task for every separation |
| Memory isolation | Principals isolated; Assistants ephemeral (subagent contexts) | Full isolation (20 stores) — but 20 stores to reconcile | None between roles (shared orchestrator memory) |
| Context cost | 10 × (~25 KB SOUL + role prompt) | 20 × same | 1 × SOUL + skills; cheapest |
| Maintenance | Moderate — sync script + 10 project-context files | Highest — 20 profiles, 20 memories, watchdog surface | Lowest — one profile |
| Scheduling | Cron/cadence per Principal; Assistants task-bound | Full parallel cadence possible but unmanageable at 20 | Single-threaded; scheduling via one queue |
| Auditability | Good — Principal artifacts + Assistant worklogs | Best in theory | Weakest — role attribution from one store |
| Drift risk | Medium — controlled by repo-canonical prompts | Highest — 20 copies to drift | Lowest |
| Hermes runtime feasibility | ✅ proven pattern (8 profiles exist; subagents via delegate_task, max 10 concurrent) | ✅ feasible but unjustified — no materially different permissions/memory per Assistant; no per-call model override | ✅ zero new profiles; pilot-ready today |

**Recommendation: Option A.** Rationale: constitution §23.5 + OM §10 require a specialized agent only when materially different evidence/reasoning/permissions/independence justify it — true for 10 Principals (distinct evidence domains, review responsibilities), **false for 10 Assistants** (support work is always Principal-reviewed, task-bound, and ephemeral). 20 persistent profiles would add maintenance without adding isolation value; Hermes also cannot give Assistants different models (single delegation.model). Option C is the correct **pilot** vehicle (zero install), Option A the correct **steady state**.

---

## 8. Open Questions for Founder

1. Hold authority: approve Holds as org-workflow-only (recommended) or as canonical-state gates (would require a constitutional amendment)? (F-03)
2. IC Secretary gate: approve the administrative completeness gate as described? (F-04)
3. Topology: Option A (recommended), B, or C — and is the pilot allowed to run under Option C (zero profiles) before any profile creation? (§7)
4. Kanban: repo-based board (recommended, zero config) vs enabling the disabled Hermes kanban toolset? (F-12)
5. Master Paper / deep-dive paper: keep REJECTED until Phase 11 Master Paper authorization? (F-07)
6. Cadence automation: no new cron during pilot (recommended)? (F-19)

---

*Proposed draft for Founder review. Not approved, not canonical, not committed. All findings verified against the files listed in §2 and the full pack contents.*
<!-- 2026-08-05 14:26 UTC+7 -->
