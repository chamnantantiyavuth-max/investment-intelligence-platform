# Project State — Investment Intelligence Platform

> Compact bootstrap state. Source of truth remains the approved project governance documents.
> Build metrics (test counts, commit counts) are tracked HERE — see §Build Metrics below.

## Current state

- **Hermes AI Workforce INTEGRATED (FD #54, 5 Aug 2026):** IIP Hermes Organization Pack v0.1 approved (Q1 as proposed / Q2 Holds org-workflow-only / Q3 Option C pilot) → subordinate operational standard under `operational/hermes-organization/` (AI-ORGANIZATION-OPERATING-STANDARD v0.1, AUTHORITY-MATRIX, DAILY-WEEKLY-WORKFLOW, KANBAN-CONTRACT, ROLE-REGISTRY, 10 Principal + 10 Assistant role contracts, 13 mapped templates, installation docs, repo kanban with 5 pilot cards + holds register). 10 thin Principal profiles INSTALLED + verified (`org-cos`, `org-ic-secretary`, `org-commodity-analyst`, `org-macro-strategist`, `org-equity-analyst`, `org-options-strategist`, `org-cro`, `org-quant-validator`, `org-data-steward`, `org-auditor`; Assistants = bounded delegated subagents, NO 20 profiles; `iip` preserved as bootstrap/control). Runtime verified: sync idempotent, 8 pre-existing profile SOUL hashes UNCHANGED, watchdog 16 cores clean, 0 secrets. Dry-run pilot PASS 8/8 (handoffs, lineage, Holds issued+cleared by issuer, dissent preserved, packet gate fail→re-pass, portfolio-blind, CIW untouched; delegated subagent 5/5 constraint checks PASS — output preserved as *-delegated.md). MERGED to main (0e0370d) + pushed 5 Aug 2026. Follow-ups tracked: R3 source-map licensing backfill, L1 single-writer lock field, L2 delegation-retry clause (optional amendments), C-04/C-05/M-02 unchanged.
- **UI REDESIGN v3 (FD #51, 4 Aug 2026):** direction **SELECTED: A — Research Desk** (light, dense, paper; FT/research-note character; mockup winner at `design/mockups/`; B dark terminal + C editorial report rejected); **IMPLEMENTED all 11 pages + ACCEPTED BY FOUNDER (4 Aug 2026)** — council visual review 2 rounds (R1 RETEST 4 findings → fixed; R2 RETEST 3 findings → fixed) + Parent round-3 re-verify (console 0 errors, 0 visible outlines, 9 routes 200); artifact `evidence/COUNCIL_DECISION-ui-2026-08-04.md`; evidence `evidence/ui/redesign-research-desk/VISUAL_QA.md`; audit fixes C1–C6, M1/M3/M6/M8, C-02 frontend quarantine; backend C2 fix (counter-evidence per-theme scoping, ADAPTER_VERSION v3, +1 locked test → 304/304); commits c4ae919/bd3d7b6/ca96285/a169596. **Remaining (next decisions): A-01 (AM override/history scope), A-02 (FO/II formula approval).** v2.1 light editorial AND FD #49 dark terminal both RETIRED. Prior (FD #49/#50): full frontend redesign — **v2.1 LIGHT EDITORIAL** (Founder-delegated direction: dark terminal retired; off-white canvas #F7F8FA, ink text, tinted tonal panels, hero-insight + findings anatomy, muted accents #178A63/#C2527B/#B07A1E/#4A7BB5, no neon). B1 tokens/shell/primitives, B2 panels, B3 Dashboard+Login, B4 AM Queue+ThemeCard+Screener (new `/am-screener`) all rebuilt + browser-verified. **FD #50:** §11 falsification read-only schema extension live (alternative_explanations / evidence register / unresolved_counter_evidence; ADAPTER_VERSION v2; Theme Card Falsification tab). **Remaining: B5 CS Radar → B6 FO (Queue/Detail/Cheap&Quality) → B7 II + Weak Signals → B8 a11y+responsive pass + full per-directory test sweep.** CS/FO/II/WeakSignal pages still show pre-redesign style until their batch (expected interim state).
- Product phase: `IIP-Phase 10` complete (Institutional Intelligence V1). `IIP-Phase 10.5` complete (Real 13F data via FD #42 amendment). All authorized phases (0–10.5) delivered. **Phase 11 (Deep Research Handoff / CIW): PILOT FIRST SLICE + MONITORING + SECOND SLICE COMPLETE (3 Aug 2026)** — MSFT research published (FD-CIW-012) + monitoring contract + Cron Class A live (FD-CIW-013/014) + **valuation second slice PUBLISHED (FD-CIW-016)**. Full implementation (Cron Class B/C, Obsidian sync, expanded tree, schema) remains deferred.
- Workflow gate: `WF-Phase -1` — Bible Council COMPLETE (CIW proposal): verdict FOUNDER DECISION REQUIRED, 10 Required Changes accepted (Option A), FD-CIW-001..007 approved (all Option A), amendment map drafted. **CIW Spec v0.2 BATCH APPROVED (FD-CIW-008, 2 Aug 2026)** — 7 specs in `project-definition/company-intelligence-workbench/` + amendment map APPROVED + 11 targeted amendments issued (documentation-only; Phase 11 implementation still not opened). **Pilot company selected: MSFT (FD-CIW-009). Pilot first slice COMPLETE (3 Aug 2026):** design v0.3 (2R PASSED) → CRR-2026-0001 approved (Research Gate) → Source Map gate passed (real SEC EDGAR) → bounded research (Modules A–M initial) → Independent Challenge PASS (round 5, after 4 FAIL rounds + rework v0.1→v0.5) → Founder-approved publication (FD-CIW-012): `research-result.md` v1 Published / Current Authoritative.
- Latest FDs: **FD #55 (5 Aug 2026) — Research Workflow UI Phase UI-0 (D1, Option A):** read-only org-workflow adapter LIVE — 4 auth-protected endpoints (`/org-queue`, `/org-holds`, `/research-artifacts`, `/research-artifacts/{id}`) serving kanban cards/holds/CIW artifact registry from committed repo files via new `backend/org_store.py` (adapters.py untouched → no F3); operational tracking only, never domain state; no writes/schema; +8 locked tests → 309/309; live smoke verified; per `design/research-workflow-ui/FIT-GAP-v0.1.md` (ChatGPT IA proposal fit-gap). Prior: **FD #54 (5 Aug 2026) — IIP Hermes AI Workforce Integration (APPROVED + MERGED):** org-pack demoted to subordinate operating standard; canonical state contract (two-axis Theme governance); new org-workflow authority grants (DATA/VALIDATION/RISK/GOVERNANCE Holds + IC Secretary gate + kanban movement, Q2 org-workflow scope only); 10 thin Principal profiles installed (Q1 Option A topology; Assistants = bounded subagents); repo-based kanban; 13 mapped templates (deep-dive paper + theme card rejected); no new cron; Option C dry-run pilot PASS 8/8. Prior: **FD #53 (4 Aug 2026) — FO/II unapproved formulas removed** (moat_score/signal_score deleted, −2σ trigger, trap 4 = MIXED, ADAPTER_VERSION v4) (71 total).
- **Real-Data Production Path COMPLETE + RELEASED (3 Aug 2026, FD #46–48) + II FOLLOW-UP (same day):** AM/FO/II serve real pipeline artifacts (AM REAL EOD hybrid, FO yfinance 8 pkgs, II SEC EDGAR partial_21_51) through auth-protected API with SQLite lineage; CS remains the sole labeled-synthetic surface; provenance labels per component (real/hybrid/synthetic + human_sourced evidence); dashboard CS agreement (2/1) enforced. **II follow-up (commit 3337154/aacaacc):** Institutional Intelligence page (`/institutional` — provenance badge, stats, 50-row table, conviction/action badges) + server-side pagination (`/ii-signals?limit=&offset=`, backward-compatible, `total` added) — closes accepted risk #1 (II API-only) + mitigates #2 (16.7MB artifact); isolation-scan clean-tree false-violation fixed. Gates: 3× Phase 2R (FAIL→folded) + Plan Council Lite (PASS WITH FIXES) + Final Council R1 REWORK (F1–F4 remediated) + R2 PASS WITH FIXES + final production audit (browser + API/oracle + DB lineage + oracle).
- **Pre-Launch Close Beta Audit CLOSED (3 Aug 2026 evening):** split-lane audit (Parent browser 10/10 + Sol Medium API/oracle) → NOT READY → Option A remediation (CS truth agreement + provenance labels) → re-audit verified → **READY WITH ACCEPTED RISKS** (Founder accepted 2 cosmetic Minors). App is release-ready as a **labeled synthetic demo**; FD #44 boundaries unchanged (real-pipeline wiring/persistence/auth deferred). Artifacts: `qa/prelaunch-audit/`.
- Tests: **309/309 all passing** — verified 5 August 2026 (post FD #55: 140 locked (90 logic + 42 real-data-api + 8 org-workflow) + 56 AM + 25 CS + 43 FO + 45 II).

## Build Metrics (single source of truth — v3.3.0)

| Metric | Value | Last verified |
|--------|-------|---------------|
| Python tests | 309/309 (140 locked: 90 logic + 42 real-data-api + 8 org-workflow; 56 AM + 25 CS + 43 FO + 45 II) | 2026-08-05 |
| Frontend build | ✅ passes (`npm run build` exit 0) | 2026-08-04 |
| Frontend lint | 0 errors (oxlint) | 2026-08-04 |
| Commits | 145 on `main` (HEAD `0e0370d` — org-pack integration merged + pushed 5 Aug 2026; +8 vs 137) | 2026-08-05 |
| FDs approved | #1–44 + FD-CIW-001..016 + FD #45..#55 (71 total) | 2026-08-05 |
| closeout_status | **completed** — session closed 5 Aug 2026: FD #54 org-pack INTEGRATED + MERGED (docs-only; no code/schema/domain change); remaining (unchanged): C-04 state reconciliation, C-05 vault register rebuild, M-02 FO spec metadata, A-01 deferred, CIW deferred, org-pack follow-ups R3/L1/L2 optional | 2026-08-05 |

> Stale mirrors to update together: `SESSION_CLOSEOUT.md`, `AGENTS.md` checkpoints, `README.md`, `project-definition/README.md`, vault `fd-register.md`. Audit/council reports live in `evidence/`.

## Open constraints

- No active blockers. **Real-data production path RELEASED (FD #46–48, 3 Aug 2026):** AM/FO/II serve real pipeline artifacts through auth-protected API with SQLite lineage; CS API surface serves labeled synthetic demo data (stays synthetic — no real CS data).
- Deferred items: DR-004 (Legacy Knowledge Salvage), Phase 11 Deep Research Handoff / CIW (concept approved in principle only — FD-CIW-001; implementation/automation/schemas/pilot require a separate named FD superseding FD #44), CIW pilot company selection (FD-CIW-007 — shortlist after specs), AM/CS API-backed workflows, automated challenge/earnings/trap detection, cross-module institutional signal integration, final stack declaration, database/persistence expansion. Templates TPL-* remain deferred.
- No broker connectivity, execution, or portfolio allocation.
- No AI-invented investment rules, thresholds, weights, formulas, lookbacks, or fallback behavior.
- No Legacy/quarantine access without separate named authorization.
- No schema or migration without explicit authorization.
## Next allowed action

**Research Workflow UI (FD #55, 5 Aug 2026) — UI-0 adapter LIVE + MERGED-ready.** Read-only org-workflow
API surface done (8 locked tests, 309/309). **Next decisions (one at a time):** D2 — approve CS
pipeline-field admission (p1–p3/layers/discount_detail/demand_detail/conviction/key_risks — separate FD +
F3 flow) unlocks CS Product Detail (UI-3); D3 — approve UI scope/order (UI-1 Briefing sections →
UI-2 /research + artifact detail); D4 — page naming (Briefing? Research Desk vs Research/Work Queue).
Unchanged: A-01 deferred (FD #52), C-04/C-05/M-02 closeout leftovers (C-05 partially reduced: vault
fd-register FD-54/55 now current), CIW PAUSED (monitoring only; next decision point Q1-FY27 ~Oct 2026),
org-pack follow-ups R3/L1/L2 optional.

## Bootstrap sources

- `AGENTS.md`
- `PROJECT_BIBLE.md` → `01-PROJECT-DNA.md`
- `02-PROJECT-CONSTITUTION.md`
- `operational/FOUNDERS-DECISIONS.md`
- `PROJECT_INDEX.md`
- `evidence/` — audit reports + council decisions

## Lifecycle sync

- Last session: 2026-08-05 (org-pack integration — FD #54): read-only fit-gap + design (previous task) → Founder approval (Q1/Q2/Q3) → branch `org-pack-v0.1` (rollback checkpoint + `_staging/hermes-backup-20260805/`) → operating standard/authority matrix/workflow/kanban contract/role registry/10 role contracts/13 templates/installation docs/repo kanban → FD #54 registered (repo + vault) → 10 thin Principal profiles installed (org-cos..org-auditor; sync-governance.py + watchdog extended with backup; 18 profiles total; 8 pre-existing SOUL hashes UNCHANGED; watchdog 16 cores clean; 0 secrets) → docs greps PASS + ad-hoc temp-script 30/30 → dry-run pilot PASS 8/8 (5-role simulation on `research-result.md` v1; HOLD-DATA-001/HOLD-RISK-001 issued+cleared by issuer; packet gate fail→re-pass; delegated subagent 5/5 constraint checks PASS, output preserved as *-delegated.md; write race = L1 single-writer lesson) → Founder ACCEPTED (A) → merged to main `0e0370d` + pushed. Evidence: `evidence/organization/` (fit-gap, runtime verification, pilot artifacts).
- Prior session: 2026-08-03 evening (AM findings → production readiness → pre-launch close-beta audit) — Loop v3 + governance sync PASS → **FD #45: 3 AM findings resolved** (FSLR yfinance artifact verified; AMD genuine unwind; GAP-006 fixed V0_TICKERS 5→9, re-run AM-V0-20260803-171535, coverage 9/9) → production smoke test (found + fixed vite proxy 8001→8000, `e5f4134`) → UI design audit (sidebar token gap parked) → **Full Pre-Launch Close Beta Audit** (split-lane: Parent browser 10/10 + Sol Medium API/oracle) → NOT READY (`a80c237`: SOL-003/BROWSER-003 CS triple disagreement + provenance Minors) → Option A remediation (`f96f0a5`: single-source CS counts, CSRadarPage→API, data_source everywhere) → re-audit + Founder acceptance (`91982a5` `b038b2f`) → **READY WITH ACCEPTED RISKS** → closeout (MEM-IIP-019/020 + state sync)
- Outcome: FD-CIW-010 (design path) → design v0.3 (Phase 2R PASSED) → FD-CIW-011 (pilot execution authorization) → CRR-2026-0001 approved (Research Gate) → Source Map gate passed → bounded research (Modules A–M, initial, real SEC EDGAR + Microsoft IR sources) → Independent Challenge 5 rounds (FAIL ×4 → PASS, findings F1–F8/N1/N2 all disposed, v0.1→v0.5) → **Founder APPROVED publication (FD-CIW-012) → research-result.md v1 Published / Current Authoritative** → FD-CIW-013/014 (monitoring contract + Cron Class A live) → **FD-CIW-015 (second-slice execution authorization, CRR-2026-0002 v0.4 after Phase 2R 3 rounds) → Source Map 2 gate passed → research-draft-2 v0.1→v0.4 (Independent Challenge 4 rounds: FAIL×3 → PASS) → Founder APPROVED (FD-CIW-016) → research-result-2.md v1 Published / Current Authoritative (supplemental; first-slice v1 intact)**
- Evidence: `docs/ciw-pilot-msft/` — first-slice artifacts (6/6) + second-slice artifacts: CRR-2026-0002-request.md (Approved), source-map-2.md, research-draft-2.md (v0.4 reviewed), challenge-review-2{,-REVIEW,-CONFIRM,-FINAL}.md (rounds 1–4), founder-review-record-2.md, research-result-2.md (Published v1) + `evidence/PHASE-2R-CRR-2026-0002-2026-08-03{,-REVIEW,-CONFIRM}.md` (Phase 2R rounds 1–3)
- Blockers: none
- Next phase: CIW paused — monitoring only until Q1-FY27 (~Oct 2026) or Founder call (third slice / new company / Phase 11 implementation each require named authorization)
- Last verified: 2026-08-04

## Session

| Field | Value |
|-------|-------|
| closeout_status | **completed** — 5 Aug 2026: FD #54 org-pack INTEGRATED + MERGED (docs-only; no code/schema/domain change); remaining unchanged: C-04/C-05/M-02 + A-01 deferred + CIW paused + org-pack follow-ups R3/L1/L2 optional |
| fd_count | #1–53 + FD-CIW-001..016 + FD #54..#55 (71 total) |
| audit_verdict | **Pre-Launch Close Beta Audit CLOSED — READY WITH ACCEPTED RISKS** (split-lane: Parent browser 10/10 + Sol Medium API/oracle; initial NOT READY → Option A remediation `f96f0a5` → re-audit verified → Founder accepted 2 cosmetic Minors `b038b2f`; app release-ready as labeled synthetic demo; FD #44 boundaries unchanged) |

<!-- 2026-08-05 15:56 UTC+7 -->
