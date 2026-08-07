# IIP AI Organization — Role Registry

**Status:** PROPOSED OPERATIONAL STANDARD — approved for implementation by FD #54 (2026-08-05)
**Version:** 0.1
**Authority:** Subordinate to the IIP Constitution + `AI-ORGANIZATION-OPERATING-STANDARD-v0.1.md`; detailed contracts in `ROLE-MAPPING-v0.1.md` + `roles/`.

## Registry

| # | Role (Principal) | Hermes profile (installed) | Assistant (bounded subagent) | Approved logical responsibility (source) | Primary artifacts (mapped) |
|---|---|---|---|---|---|
| 1 | Founder Chief of Staff | `org-cos` | Executive Research Coordinator | Research Orchestrator (OM §3); Decision Gate queueing (OM §9) | Daily Work Queue, Founder Action Brief, Weekly Operating Review, Dependency/Blocker Log |
| 2 | Investment Committee Secretary | `org-ic-secretary` | Committee Records Assistant | Founder Decision Gate recordkeeping (OM §9); CIW founder-review-record precedent | IC Decision Pack, Founder Review Pack, Decision/Transition Register |
| 3 | Commodity Product Analyst | `org-commodity-analyst` | Commodity Research Assistant | OM §5.3 Product Analysis (V1+); Close System product suitability (§15) | Product Dossier, Cost-Curve Note, Supply-Demand Balance, Close-System Eligibility Memo |
| 4 | Global Macro Strategist | `org-macro-strategist` | Macro Research Assistant | OM §5.1 Macro Analysis (V1+); Momentum §6.1 Market Regime | Macro Regime Map, Scenario/Trigger Matrix, Transmission Note, Policy/Event Brief |
| 5 | Equity Alpha Analyst | `org-equity-analyst` | Equity Research Assistant | OM §5.4/§5.5; Momentum §6.3–6.8; FO pipeline (Phase 8); CIW bounded-consumption only (F-09) | Company Research Paper (CIW-mapped), Candidate Card, Valuation Assumption Sheet, Earnings Update, Thesis/Falsification Register |
| 6 | Options Strategist | `org-options-strategist` | Options Research Assistant | Close System Instrument Structure (§15); OM §5.3 | Options Strategy Memo, Payoff/Greek Map, IV/Skew/Term Note, Scenario Decision Tree |
| 7 | Chief Risk Officer | `org-cro` | Risk Research Assistant | Independent Challenge (OM §7); Close System risk dimensions (§15); Phase 8 §4 | Risk Challenge Memo, Research Risk Register, Scenario Checklist, Residual Risk Acceptance Request |
| 8 | Quant & Model Validator | `org-quant-validator` | Quant Research Assistant | Shared Core deterministic verification (OM §4); VERIFICATION-DOCTRINE; Evidence QA | Quant Validation Report, Reproduction Log, Model Card, Sensitivity Appendix |
| 9 | Data Steward | `org-data-steward` | Data Quality Assistant | Shared Core: Evidence Acquisition, Data Validation, provenance, Data Confidence (EVIDENCE-MODEL §5/§9) | Dataset Card, Data Quality Report, Lineage Record, Source/Licensing Register |
| 10 | Internal Auditor / Red Team | `org-auditor` | Audit Evidence Assistant | Audit discipline (FD-HERMES-007 Sol Medium execution; governance-audit; LLM Council) | Audit Plan, Audit Finding, Red-Team Memo, Root-Cause Analysis, Remediation Verification |
| 11 | Radar Scout / Opportunity Monitor | `org-radar-scout` | Scanning Assistant | Opportunity discovery: continuous monitor of massive public data for anomalies/divergences/unusual signals → Task Idea Cards to research intake (FD #71 — scout/radar layer, Option B) | Task Idea Card, Radar Digest, Anomaly Log |

## Rules

1. Each role is an **operator of an existing approved logical responsibility** — no role creates domain logic, states, rules, or authorities beyond FD #54 scope.
2. Assistants are **bounded delegated subagents/worker prompts** under their Principal (topology per FD #54 Q1/Q3) — no Assistant profiles are installed.
3. Portfolio-blind (Constitution §23.8.1): no role or Assistant receives holdings/positions/cost basis/transactions/account data.
4. CIW boundary: role 5 consumes published CIW results only; no CIW-path research/automation without a separate named FD (FD #44 discipline).
5. Audit execution (role 10) routes through Sol Medium per FD-HERMES-007.
6. All roles read the Operating Standard + their PRINCIPAL.md at startup (PROFILE-STARTUP-CONTRACT).

---

*Role Registry v0.1 — FD #54.*
**Amended 2026-08-06 (FD #66 R-2 + Plan A v0.3):** all 10 Principal + 10 Assistant contracts reframed to research Principals — Analytical Freedom Doctrine (direction §5), independent first pass (§7.3), 3 minimum artifacts (Main Research Essay / Evidence & Quant Appendix / Opposing Thesis & Audit Note, FD #64 item 6); domain specs/checklists NOT auto-loaded into the first pass (optional lenses / QA references only, FD #64 item 7); legacy pipeline outputs frozen (FD #65). Profiles read their amended PRINCIPAL.md at startup (unchanged mechanism).
**Amended 2026-08-06 (FD #71):** row 11 added — Radar Scout (`org-radar-scout`) — scout/radar layer (Option B, dedicated role). Rows 1–10 unchanged. Same session: cross-examiner material-claims rule + Data Steward first-pass thesis-bar encoded (FD #71).
**Amended 2026-08-07 (FD #73):** role 7 (CRO) — all delegated Risk Research Assistant work routes via Sol Medium (openai-codex, `gpt-5.6-sol`, reasoning=medium pilot) for challenger model diversity; delegation `reasoning_effort` high→medium for iip + org-* profiles + global (FD #73 cost pilot, 2-week measurement; council/audit quality monitored — revert on regression). **Option B (same day):** the Opposing Thesis drafting (CRO's main artifact) also delegates via Sol Medium — full challenger model diversity at the decisive output; Assistant contract amended (first-pass drafting allowed ONLY under Sol Medium execution, never self-finalizing; Principal owns verdict); Principal conversation layer stays Flash high. Rows unchanged.
**Amended 2026-08-07 (FD #74):** row 11 (Radar Scout) — bounded momentum-screen scanning mandate added (Option B — momentum candidates via the existing radar intake path, NO new role; conceptual O'Neil/Minervini signals per FD #39 Rule Pack; no invented thresholds per FD #53; new intake stream — frozen AM list untouched per FD #65). Rows 1–10 unchanged.
**Amended 2026-08-07 (FD #75):** row 11 FD #74 momentum-screen mandate **REVERSED** — momentum screening removed from radar scope (Founder decision: focus fundamental/moat/business evidence; Founder reviews charts directly). Row 11 restored to FD #71 discovery-only scanning. Rows 1–10 unchanged.
**Amended 2026-08-07 (FD #78):** row 11 — **weekly Radar Scan cron AUTHORIZED** (named FD per FD-CIW-005 discipline; job `8ba233e88015`, Mon 08:00 UTC+7, deliver local, digest → `kanban/digests/`); on-demand session/ad-hoc RADAR-#### mandates RETAINED (weekly scan does not replace them). Row content unchanged — discovery-only per FD #75. Rows 1–10 unchanged.
<!-- 2026-08-07 15:30 UTC+7 -->
