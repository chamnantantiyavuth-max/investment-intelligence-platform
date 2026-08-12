# STAGE 6.6 — Final Routing & Subscription Alignment CLOSEOUT (R1–R6 + regression)

**Status:** COMPLETE — v3.8 PROMOTED · Stage 7 = READY (awaiting Founder GO; R4 browser approval pending)
**Date:** 2026-08-13
**Authorization:** Founder Stage 6.6 direction (R1–R6 + D1–D6 decisions + Stage 7 HOLD for this bounded cleanup)

---

## R1 — Luna truly selective ✅

`delegation.model` reverted **Luna → deepseek-v4-flash / deepseek** in all **22 configs** (global + 21 profiles). Routine `delegate_task` / helper work now runs on the primary workforce model. Luna = **explicit task-level override only** (`kanban create --model openai/gpt-5.6-luna --provider openrouter`).

| Verify | Result |
|---|---|
| routine `delegate_task` → NOT Luna | ✅ delegation.model = deepseek-v4-flash |
| routine Kanban worker → Flash | ✅ org-data-steward task: session deepseek-v4-flash (t_9055b222) |
| premium audit → Luna | ✅ org-auditor override task: `premium-luna-ok — openai/gpt-5.6-luna` (t_d2f7f1ff) |
| Material Engineering Review → Luna | ✅ `eng-review-luna-ok — running on openai/gpt-5.6-luna via openrouter` (t_b0e0a140) |
| Luna NOT base model of org-auditor/org-cro | ✅ base = deepseek everywhere; override per task only |

## R2 — Luna removed as global routine fallback ✅

`fallback_providers` set to **`[]`** in all configs. Routine DeepSeek failure → **queue/fail safely** (no silent conversion of routine workload into paid Luna workload). Premium tasks retry Luna explicitly per their own contract (task-level override remains the premium invocation).

## R3 — Model names removed from SOUL / USER ✅

- iip SOUL.md Model Routing section rewritten as **generic policy pointer** (no model names, no provider names; loads `model-routing` skill).
- Audit Delegation Rule / LLM Council / Governance Sync Gate sections: model-specific refs → "approved premium reviewer (per model-routing policy)".
- user.md Tech Stack & Model Routing → generic pointer.
- **Synced to all 18 profiles. Final sweep: 0 model-name refs across ALL SOUL+user files.**
- Architectural regression from Stage 6.5 (28 refs × 18 SOULs) **reversed**. Future model changes touch config + FD + skill only — never SOUL/USER.

## R4 — Gemini Notebook Pro integration path (subscription-first) ⚠️ BLOCKER

**CONCRETE TECHNICAL BLOCKER:** browser harness reached Chrome remote-debugging setup — requires one-time Founder approval (tick "Allow remote debugging for this browser instance" + Allow popups). Playwright/Browser-Use infrastructure otherwise ready.
- Rehearsal plan documented (navigate → Deep Research → submit frozen prompt → poll (Pro quota 20/day) → capture report+sources → freeze+provenance → verify anti-anchoring unchanged).
- API-key path remains the fallback (proven Stage 6).
- Full status: `STAGE6.6-R4-GEMINI-NOTEBOOK-REHEARSAL.md`.

## R5 — Promotion status ✅ (no invented expiry)

```
Promotion status: ACTIVE — 50% off ($0.50/M input, $3/M output, OpenRouter model page)
Verified: 2026-08-13
Official expiry: NOT PUBLISHED / NOT VERIFIED — re-check periodically; never invent a date
```
Recorded in model-routing skill v4.0. Post-promo cost guard retained (viable at normal pricing; no role expansion for promo reasons).

## R6 — Luna Council scope ✅

model-routing skill v4.0: **Luna mandatory for MATERIAL milestones only** (Bible, Final, material engineering gates). **Routine Plan-Lite / Test-Charter / Diagnostic-Lite gates do NOT consume Luna** (legacy Council proliferation removed).

## Regression (R7) — all passed

Routine delegation NOT Luna ✅ · routine worker Flash ✅ · premium audit Luna (override) ✅ · material engineering review Luna (override) ✅ · fallback [] ✅ · **Luna leakage = 0** (only the 2 explicit premium override tasks touched Luna) · config final: delegation=deepseek-v4-flash/deepseek, fallback=[], base=deepseek everywhere.

## v3.8 Promotion

**PROMOTED 2026-08-13 (FD #105):** v3.8.0 (engineering/change-control workflow) deployed to **20 profiles** (version header updated candidate→3.8.0, supersedes note added). Two natural engineering pilots passed (Stage 4 board safety + Stage 6.5/6.6 routing migration); regression passed post-cleanup.
- **v3.7.1 rollback preserved:** `evidence/harness/v37-rollback/project-workflow-SKILL-v3.7.1.md` (hash d296a7af8d604481 = production hash) + originals in git history.

## Founder Decisions (Stage 6 D1–D6) — recorded

D1 DEFER (writer default after ≥3 A/B samples) · D2 APPROVE continue calibration · D3 APPROVE minimal amendments · D4 APPROVE bounded G1–G10 admission task (not Stage-7 blocker) · D5 APPROVE Data Steward investigation · D6 APPROVE Apple errata. All recorded for execution queue.

## Prohibited-Outcomes Check

No Stage 7 cutover · no board deletion · no /kanban rewire · no Cron migration · no IPM activation · no mass Luna conversion (Luna = explicit override only) · historical Sol/Luna records preserved (§23.9) · SOUL/USER now model-name-free.

## Stage 7 Recommendation

**GO-READY (2 conditions):** (1) Founder completes R4 browser approval → Notebook rehearsal runs (or explicit accept of API-first fallback); (2) Founder GO on cutover scope. Board safety closed, governance clean, routing architecture consistent (Flash workforce + Luna premium override + fail-safe fallback), v3.8 promoted.

**STOP — awaiting Founder review.**

---
<!-- 2026-08-13 01:09:50 +0700 — captured via scripts/artifact_timestamp.py (system clock at write) -->
