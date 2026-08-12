# STAGE 6.5 — Model Routing Migration (Sol→Luna) + Gemini Access-Path + v3.8 Pilot #2 CLOSEOUT

**Status:** COMPLETE — recommendation: **v3.8 = PROMOTE (conditional on Founder approval)** · Stage 7 = READY FOR AUTHORIZATION DECISION
**Date:** 2026-08-13
**Branch:** harness/stage2-prep (evidence) + live Hermes configs (iip + 20 profiles)
**Authorization:** Founder Stage 6.5 direction (A–E)

---

## A. Routing Architecture (exact, post-migration)

```
DeepSeek V4 Flash (deepseek) = PRIMARY workforce — routine, research, Radar/Discovery,
  Data Steward, CoS triage, Kanban workers, editorial, self-check
GPT-5.6 Luna High (openai/gpt-5.6-luna via openrouter) = SELECTIVE premium independent reviewer
  — mandatory: material harness/security/arch change, IIP↔IPM authority change,
    schema/destructive review, flagship DR final audit pre-Facts-Locked
  — conditional: CRO on material disagreement, high-uncertainty/Founder-designated, re-review after material correction
Fallback = Luna High (openrouter) for Flash; DeepSeek for Luna (if unavailable)
Gemini DR = external desk (API-key path — see C)
Founder = final authority
```

## B. Exact Config/Profile Diffs (22 files migrated)

| Surface | Before | After |
|---|---|---|
| `delegation.model` (22 configs: global + 21 profiles) | `gpt-5.6-sol` | `openai/gpt-5.6-luna` |
| `delegation.provider` (22 configs) | `openai-codex` | `openrouter` |
| `image_gen.provider` (20 profiles) | (unchanged — restored to `openai-codex`) | `openai-codex` (intact) |
| MoA gpt-5.5 provider (20 profiles) | (unchanged — restored to `openai-codex`) | `openai-codex` (intact) |
| `fallback_providers` | unchanged (already Luna) | `openai/gpt-5.6-luna` (openrouter, high) |
| `profiles/iip/SOUL.md` + 18 profile SOULs | Sol Medium routing (28 refs each) | Luna High routing (28 refs each) |
| `profiles/iip/user.md` | Sol Medium tier | Luna High tier |
| model-routing skill | v3.0 (Flash + Sol + Luna fallback) | **v4.0** (Flash workforce + Luna selective premium + cost guardrail + task-level override doctrine) |
| 13 ACTIVE skills (llm-council, governance-*, prelaunch-close-beta-audit, iip-hermes-workforce, etc.) | Sol Medium policy | Luna High policy (historical changelog preserved) |

## C. Luna Task-Selection Policy (encoded in model-routing v4.0)

- **Mandatory Luna:** material harness/security/arch · IIP↔IPM privacy/authority · schema/destructive/high-blast-radius · flagship DR final audit pre-Facts-Locked · governance/Bible audit · Council gates · pre-launch/close-beta · Phase 2R · L3
- **Conditional Luna:** CRO (material disagreement) · high-uncertainty/Founder-designated · re-review after material correction
- **NEVER Luna:** Radar, Discovery routine, source collection, Data Steward, CoS routine, Pass A/B, normal fundamental analysis, weekly monitoring, editorial, deterministic semantic checks, normal workers, routine self-checks
- **Task-level override preferred** — Luna NOT the base model of org-auditor/org-cro (cost binds to high-EV work, not profiles)

## D. Measured Smoke-Test Results (10/10 + 1 bonus)

V1 delegation= Luna ✅ · V2 session smoke ✅ · V3 Luna direct via OpenRouter ✅ · V4 DeepSeek default ✅ · V5 task override ✅ · V6 no stale ACTIVE sol (configs 0 / SOULs 0 / active skills 0) ✅ · V7 fallback ✅ · V8 rollback (22 backups) ✅ · V9 secret scan 0 ✅ · V10 premium kanban worker → Luna (dispatcher-stamped) ✅ · V10b routine worker → DeepSeek Flash ✅

## E. Luna Usage Estimate (normal monthly)

**3–12 invocations/month** — ~1 Luna premium review per Full Research Mandate (default max); governance/council/audits add 1–3. Cost guardrail: promo-aware policy recorded, architecture viable at normal post-promotion pricing.

## F. Promotion-Expiry / Cost Guard

PROMO-AWARE COST POLICY (recorded in model-routing v4.0 + this closeout):
- Record verified promo expiry when known; re-evaluate routing before expiry.
- Never expand Luna roles solely because promo is cheap.
- If post-promo economics no longer justify a role → downgrade to DeepSeek routine review, preserving Luna for highest-value reviews only.
- Default ≤1 Luna review per Full Research Mandate; 2nd only after material REWORK/correction or explicit Founder decision.

## G. Gemini Production Access-Path Verdict

**VERDICT: Stage 6 pilot = Google AI Studio API-key path (usage-billed, `GOOGLE_API_KEY` in profiles/iip/.env, `deep-research-max-preview-04-2026` via Interactions API) — SEPARATE billing/quota path from the Gemini Pro/Notebook subscription the Founder intends to purchase.** Options: A) keep API path (recommended, proven) · B) Notebook/Pro entitlement integration (engineering task) · C) hybrid. v1.4 workflow unchanged under any option. Full analysis: `STAGE6.5-C-GEMINI-ACCESS-PATH.md`.

## H. v3.8 Pilot #2 Comparison → Recommendation

**PROMOTE v3.8 (conditional on Founder approval).** Two consecutive natural engineering pilots passed (Stage 4 board safety; Stage 6.5 routing migration). v3.8 = engineering/change-control only (research uses IIP skills — verified no contamination in either pilot). Verification discipline (locked acceptance 10/10) + lighter context overhead confirmed vs v3.7.1. No manufactured task was needed.

**Condition:** Founder approval of promotion + (recommended) confirm Stage 7 sequencing after promotion.

## I. Rollback Evidence

- 22 config backups (`*.bak-2026-08-13-stage65`) — restore = copy back (verified sol state restorable)
- SOUL/user backups (iip) — same pattern
- Skills: all changes documented; model-routing v4.0 fully reversible (content restore)
- **Live change now effective** — new sessions/gateway restart pick up Luna delegation; existing long-running processes may hold old config until restart (S4-F2 accepted-latency pattern)

## J. Prohibited-Outcomes Check

| Constraint | Status |
|---|---|
| No Stage 7 production Kanban cutover | ✅ not started |
| No old repo-board deletion | ✅ untouched |
| No /kanban or /org-office rewire | ✅ untouched |
| No Cron migration | ✅ untouched |
| No production IPM activation | ✅ untouched |
| No production SOUL migration (content sync only, same-file pattern) | ✅ content-level sync, no pointer migration |
| No unrelated Discovery remediation implementation | ✅ none |
| No mass conversion of all profiles to Luna | ✅ Luna = delegation (premium reviewer) only; base = DeepSeek everywhere |
| Historical Sol records untouched | ✅ FDs/evidence/changelogs preserved per §23.9 |

## K. Stage 6 D1–D6 Founder Decision Packet

Surfaced verbatim at `STAGE6.5-E-FOUNDER-DECISIONS-D1-D6.md` — 6 decisions with recommendation/default/consequence. **NOT pre-approved.** Founder direction on 5 of 6 already aligned; D1 (A/B writer preference — needs Founder's read of both variants) and D4 (admission wave timing) remain open.

## L. Stage 7 Recommendation

**READY FOR AUTHORIZATION DECISION** (not self-authorizing): board safety closed (9 profiles), governance clean, routing migrated (Luna premium), v3.8 pilot #2 PASS → promote v3.8, then Stage 7 Production Cutover can proceed on Founder GO. Preconditions: D1–D6 decisions + v3.8 promotion approval + Stage 7 scope confirmation.

**STOP — awaiting Founder review.**

---
<!-- 2026-08-13 00:33:39 +0700 — captured via scripts/artifact_timestamp.py (system clock at write) -->
