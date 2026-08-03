# Phase 2R — Architecture Review, Round 3 (Real-Data Production Path, FD #46)

> Gate: Phase 2R (final escalation round) · Date: 2026-08-03 · Reviewer: Sol Medium (gpt-5.6-sol, openai-codex) · Duration: 402s
> Subject: `docs/ARCH-REAL-DATA-PRODUCTION.md` v0.3 at commit `53aed9a` · Result: **FAIL** — F3/F7/NF1/NF2/NF3 closed; F1/F2/F4/F5/F6/F8 partial + NF4–NF8 new → revision to v0.4
> Regression: budget 2/2 used + escalation round run (Founder timed out → best judgment) → D4 (verification via implementation gates) presented at Phase 3

## Verdict (round 3)

v0.3 materially improves the design and genuinely closes F3, F7, and NF1–NF3, but F1, F2, F4, F5, F6, and F8 remain only partially closed. Remaining defects — incomplete replay lineage, ambiguous mixed-source provenance, absent database ignore rule, unhandled frontend contract migration — would cause the final production audit to fail.

## Round-2 Item Status (round 3)

| Item | Status | Notes |
|---|---|---|
| F1 | partial | FO flattening (nested→summary extraction) unstated as contract; /am-theme/{id} shape not locked |
| F2 | partial | replay tuple omits endpoint; no executable adapter-by-version; one run_id_fk can't represent composite dashboard; CS has no run |
| F3 | closed | atomic write + single snapshot + WAL/busy_timeout + FK enforcement |
| F4 | partial | theme metadata (why_now/confidence/lifecycle/approval) is human/synthetic layer but gets top-level real provenance; classification doesn't cover source:null / Founder Obsidian Vault / Founder Journal |
| F5 | partial | II as_of not stamped (only generated_at/report_date); dashboard selects "latest" without admission rule |
| F6 | partial | .gitignore *.db rule absent at commit (verified: check-ignore fails); settings schema comment "schema_version ONLY" contradicts active_session_nonce; .env.example absent |
| F7 | closed | D1 correctly flagged Founder decision |
| F8 | partial | no frontend contract/build/browser tests; no dashboard↔CS UI agreement; no auth-client credential test; no unknown-mode test |
| NF1 | closed | PRAGMA every connection + NOT NULL FK + invalid-FK test |
| NF2 | closed | FO envelope locked + legacy-root rejection |
| NF3 | closed | CS dashboard lineage explicit null + backend_static_mock |

## New Material Findings (round 3)

1. **NF4 — Frontend contract migration absent:** amClient expects `ThemeSummary[]`, types require removed synthetic fields, no `credentials: include`, no auth gate/login route → pages render missing values / 401 while backend tests pass.
2. **NF5 — CS triple-agreement regression EXISTS in UI:** `DashboardPage.tsx:61-67` hardcodes 8/3, never calls `/api/dashboard/summary` (SOL-003 survives).
3. **NF6 — Composite/static responses can't use single-run lineage:** dashboard combines AM+FO+II+CS; CS has no pipeline run → need `api_read_runs` relation + static-source descriptor; endpoint must be in replay key.
4. **NF7 — Dashboard admission bypass:** dashboard selects latest per module without mode/freshness checks; current II artifact is SYNTHETIC → synthetic state can re-enter dashboard while direct endpoints 503.
5. **NF8 — No DB/adapter version lifecycle:** no schema_version init/upgrade/reject; adapter_version logged but no immutable code-hash registry.

## Parent verification (2026-08-03)

- DashboardPage.tsx hardcoded 8/3 confirmed (lines 61-67) — NF5 real ✅
- amClient.ts old contract + no credentials: include + types/am.ts synthetic numeric fields confirmed — NF4 real ✅
- Round-3 findings accepted; all folded into v0.4 (F1–F8 + NF1–NF8), verification moved to Phase 4 locked tests (12-point charter incl. frontend build/browser) + Phase 5 QA + Final Council + final production audit.

<!-- 2026-08-03 21:20 UTC+7 -->
