# Project State — Investment Intelligence Platform

> Compact bootstrap state. Source of truth remains the approved project governance documents.
> Build metrics (test counts, commit counts) are tracked HERE — see §Build Metrics below.

## Current state

- Product phase: `IIP-Phase 10` complete (Institutional Intelligence V1). `IIP-Phase 10.5` complete (Real 13F data via FD #42 amendment). All authorized phases (0–10.5) delivered. **Phase 11 (Deep Research Handoff / CIW): PILOT FIRST SLICE + MONITORING + SECOND SLICE COMPLETE (3 Aug 2026)** — MSFT research published (FD-CIW-012) + monitoring contract + Cron Class A live (FD-CIW-013/014) + **valuation second slice PUBLISHED (FD-CIW-016)**. Full implementation (Cron Class B/C, Obsidian sync, expanded tree, schema) remains deferred.
- Workflow gate: `WF-Phase -1` — Bible Council COMPLETE (CIW proposal): verdict FOUNDER DECISION REQUIRED, 10 Required Changes accepted (Option A), FD-CIW-001..007 approved (all Option A), amendment map drafted. **CIW Spec v0.2 BATCH APPROVED (FD-CIW-008, 2 Aug 2026)** — 7 specs in `project-definition/company-intelligence-workbench/` + amendment map APPROVED + 11 targeted amendments issued (documentation-only; Phase 11 implementation still not opened). **Pilot company selected: MSFT (FD-CIW-009). Pilot first slice COMPLETE (3 Aug 2026):** design v0.3 (2R PASSED) → CRR-2026-0001 approved (Research Gate) → Source Map gate passed (real SEC EDGAR) → bounded research (Modules A–M initial) → Independent Challenge PASS (round 5, after 4 FAIL rounds + rework v0.1→v0.5) → Founder-approved publication (FD-CIW-012): `research-result.md` v1 Published / Current Authoritative.
- Latest FDs: **FD #45 (3 Aug 2026 evening) — AM Findings Resolution + GAP-006 Fix** (FSLR P/E anomaly verified as yfinance artifact; AMD −8.8% verified genuine premium unwind; `V0_TICKERS` extended 5→9 → real EOD coverage 9/9). Prior: FD-CIW-015/016 (second slice). Chain: #1–44 + FD-CIW-001..016 + FD #45 (61 total).
- **Pre-Launch Close Beta Audit CLOSED (3 Aug 2026 evening):** split-lane audit (Parent browser 10/10 + Sol Medium API/oracle) → NOT READY → Option A remediation (CS truth agreement + provenance labels) → re-audit verified → **READY WITH ACCEPTED RISKS** (Founder accepted 2 cosmetic Minors). App is release-ready as a **labeled synthetic demo**; FD #44 boundaries unchanged (real-pipeline wiring/persistence/auth deferred). Artifacts: `qa/prelaunch-audit/`.
- Tests: **262/262 all passing** — verified 3 August 2026 (evening, post GAP-006 fix + audit remediation: 90 locked + 56 AM + 42 FO + 25 CS + 49 II).

## Build Metrics (single source of truth — v3.3.0)

| Metric | Value | Last verified |
|--------|-------|---------------|
| Python tests | 262/262 passing | 2026-08-02 |
| Frontend build | ✅ passes (`npm run build` exit 0) | 2026-08-02 |
| Frontend lint | 0 errors, 4 warnings (shadcn/ui fast-refresh advisories) | 2026-08-02 |
| Commits | 89 on `main` | 2026-08-03 |
| FDs approved | #1–44 + FD-CIW-001..016 + FD #45 (61) | 2026-08-03 |
| closeout_status | **completed** (AM findings resolved + GAP-006 fixed FD #45 + pre-launch audit CLOSED READY WITH ACCEPTED RISKS) | 2026-08-03 |

> Stale mirrors to update together: `SESSION_CLOSEOUT.md`, `AGENTS.md` checkpoints, `README.md`, `project-definition/README.md`, vault `fd-register.md`. Audit/council reports live in `evidence/`.

## Open constraints

- No active blockers. AM/CS API surfaces serve labeled synthetic demo data — real pipeline wiring deferred.
- Deferred items: DR-004 (Legacy Knowledge Salvage), Phase 11 Deep Research Handoff / CIW (concept approved in principle only — FD-CIW-001; implementation/automation/schemas/pilot require a separate named FD superseding FD #44), CIW pilot company selection (FD-CIW-007 — shortlist after specs), AM/CS API-backed workflows, automated challenge/earnings/trap detection, cross-module institutional signal integration, final stack declaration, database/persistence expansion. Templates TPL-* remain deferred.
- No broker connectivity, execution, or portfolio allocation.
- No AI-invented investment rules, thresholds, weights, formulas, lookbacks, or fallback behavior.
- No Legacy/quarantine access without separate named authorization.
- No schema or migration without explicit authorization.

## Next allowed action

**CIW PAUSED (session decision, 3 Aug 2026 evening) — no new authoring work this cycle.** Cron Class A job `ciw-msft-class-a-monitor` runs weekly (Mon 09:00) → draft monitoring notes for Founder review; next real data-point run at Q1-FY27 filing (~Oct 2026). Both MSFT results remain Current Authoritative (first slice + valuation supplement). **Next options (each requires named authorization):** (a) MSFT third research slice (e.g., Module C moat depth at customer/competitor level, or Module P comparator returns with primary filings), (b) pilot on another company (FD-CIW-007 shortlist: JNJ/AAPL/META/NVDA), (c) extend Phase 11 implementation (Cron Class B draft analysis, Obsidian sync, expanded tree — separate named FD), (d) keep paused (monitoring runs; Phase 11 expansion stays deferred).

## Bootstrap sources

- `AGENTS.md`
- `PROJECT_BIBLE.md` → `01-PROJECT-DNA.md`
- `02-PROJECT-CONSTITUTION.md`
- `operational/FOUNDERS-DECISIONS.md`
- `PROJECT_INDEX.md`
- `evidence/` — audit reports + council decisions

## Lifecycle sync

- Last session: 2026-08-03 evening (AM findings → production readiness → pre-launch close-beta audit) — Loop v3 + governance sync PASS → **FD #45: 3 AM findings resolved** (FSLR yfinance artifact verified; AMD genuine unwind; GAP-006 fixed V0_TICKERS 5→9, re-run AM-V0-20260803-171535, coverage 9/9) → production smoke test (found + fixed vite proxy 8001→8000, `e5f4134`) → UI design audit (sidebar token gap parked) → **Full Pre-Launch Close Beta Audit** (split-lane: Parent browser 10/10 + Sol Medium API/oracle) → NOT READY (`a80c237`: SOL-003/BROWSER-003 CS triple disagreement + provenance Minors) → Option A remediation (`f96f0a5`: single-source CS counts, CSRadarPage→API, data_source everywhere) → re-audit + Founder acceptance (`91982a5` `b038b2f`) → **READY WITH ACCEPTED RISKS** → closeout (MEM-IIP-019/020 + state sync)
- Outcome: FD-CIW-010 (design path) → design v0.3 (Phase 2R PASSED) → FD-CIW-011 (pilot execution authorization) → CRR-2026-0001 approved (Research Gate) → Source Map gate passed → bounded research (Modules A–M, initial, real SEC EDGAR + Microsoft IR sources) → Independent Challenge 5 rounds (FAIL ×4 → PASS, findings F1–F8/N1/N2 all disposed, v0.1→v0.5) → **Founder APPROVED publication (FD-CIW-012) → research-result.md v1 Published / Current Authoritative** → FD-CIW-013/014 (monitoring contract + Cron Class A live) → **FD-CIW-015 (second-slice execution authorization, CRR-2026-0002 v0.4 after Phase 2R 3 rounds) → Source Map 2 gate passed → research-draft-2 v0.1→v0.4 (Independent Challenge 4 rounds: FAIL×3 → PASS) → Founder APPROVED (FD-CIW-016) → research-result-2.md v1 Published / Current Authoritative (supplemental; first-slice v1 intact)**
- Evidence: `docs/ciw-pilot-msft/` — first-slice artifacts (6/6) + second-slice artifacts: CRR-2026-0002-request.md (Approved), source-map-2.md, research-draft-2.md (v0.4 reviewed), challenge-review-2{,-REVIEW,-CONFIRM,-FINAL}.md (rounds 1–4), founder-review-record-2.md, research-result-2.md (Published v1) + `evidence/PHASE-2R-CRR-2026-0002-2026-08-03{,-REVIEW,-CONFIRM}.md` (Phase 2R rounds 1–3)
- Blockers: none
- Next phase: CIW paused — monitoring only until Q1-FY27 (~Oct 2026) or Founder call (third slice / new company / Phase 11 implementation each require named authorization)
- Last verified: 2026-08-03

## Session

| Field | Value |
|-------|-------|
| closeout_status | completed |
| fd_count | 44 + 16 CIW + FD #45 (61 total) |
| audit_verdict | **Pre-Launch Close Beta Audit CLOSED — READY WITH ACCEPTED RISKS** (split-lane: Parent browser 10/10 + Sol Medium API/oracle; initial NOT READY → Option A remediation `f96f0a5` → re-audit verified → Founder accepted 2 cosmetic Minors `b038b2f`; app release-ready as labeled synthetic demo; FD #44 boundaries unchanged) |

<!-- 2026-08-03 22:40 UTC+7 -->
