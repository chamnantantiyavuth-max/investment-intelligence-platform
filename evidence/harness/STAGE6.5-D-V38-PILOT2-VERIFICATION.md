# S65-D — v3.8 Engineering Pilot #2 Verification + Comparison (Stage 6.5, 13 Aug 2026)

## Verification Suite Results (all 10 passed)

| # | Verification | Result | Evidence |
|---|---|---|---|
| V1 | Config resolves Luna delegation | ✅ | `delegation.model = openai/gpt-5.6-luna` · `delegation.provider = openrouter` |
| V2 | Session smoke (primary path intact) | ✅ | iip session runs normally (DeepSeek primary) |
| V3 | Luna direct invocation via OpenRouter | ✅ | `--provider openrouter --model openai/gpt-5.6-luna` → `luna-direct-ok` |
| V4 | DeepSeek remains default/routine | ✅ | `model.default = deepseek-v4-flash` · `model.provider = deepseek` |
| V5 | Task-level override pattern | ✅ | delegation model read = Luna (premium tasks only) |
| V6 | No stale ACTIVE Sol routing | ✅ | configs 0 · SOULs 0 · active skills 0 (historical changelog only, preserved per §23.9) |
| V7 | Fallback chain | ✅ | `fallback_providers: [{openrouter, openai/gpt-5.6-luna, high}]` |
| V8 | Rollback | ✅ | 22 config backups exist; backup restores original sol state (simulated verify) |
| V9 | Secret scan | ✅ | 0 secrets in all changed configs/SOUL |
| V10 | Kanban worker dispatch — premium task | ✅ | org-auditor task → worker self-report MODEL: openai/gpt-5.6-luna + dispatcher-stamped metadata confirms |
| V10b | Kanban worker dispatch — routine task | ✅ | org-data-steward task → deepseek-v4-flash (NOT Luna) — cost binds to high-EV work, not profile |

## v3.7.1 vs v3.8 Pilot #2 Comparison

| Dimension | v3.7.1 (production) | v3.8 (candidate) | Delta |
|---|---|---|---|
| Config migration executed | would work | worked (this pilot) | v3.8 = verified on real config migration |
| Engineering scope separation | research+eng mixed | engineering-only (research uses IIP skills) | **BETTER** — no research-context contamination |
| Model-routing policy | Sol Medium (retired) | Luna High selective premium (FD-2026-08-13-S65) | v3.8 aligned with new policy |
| Verification discipline | manual | locked acceptance suite (10/10) | **BETTER** — deterministic verification |
| Rollback | documented | tested (V8) | EQUAL |
| Context overhead | full workflow load | lighter (engineering-only triggers) | BETTER (Stage 4 finding confirmed) |
| Bureaucracy | full gates | proportional (material gates only) | BETTER (Stage 4 finding confirmed) |

**Verdict: v3.8 pilot #2 = PASS.** Second consecutive successful engineering pilot (Stage 4 board safety + Stage 6.5 routing migration). Both pilots were naturally-occurring engineering tasks (no manufactured work).

## Luna Usage Estimate (normal monthly)

| Work type | Luna invocations/month (est.) | Basis |
|---|---|---|
| Governance/Bible audits | 1–2 | quarterly-ish, per audit |
| LLM Council gates | 1–3 | material milestones only |
| Pre-launch/close-beta audits | 0–1 | per release |
| Phase 2R / L3 debug | 0–1 | rare escalations |
| Flagship DR final audit (pre-Facts-Locked) | 1–3 | flagship mandates only |
| CRO (material disagreement / high-uncertainty) | 0–2 | conditional |
| **Total** | **3–12 / month** | ~1 Luna premium review per Full Research Mandate (default max) |

**Cost guardrail active:** default ≤1 Luna review per mandate; second review only after material REWORK or explicit Founder decision; promo-aware policy recorded (re-evaluate before promo expiry; architecture viable at normal pricing).

## Rollback Evidence

- 22 config backups: `config.yaml.bak-2026-08-13-stage65` + `profiles/*/config.yaml.bak-2026-08-13-stage65`
- SOUL/user backups: `profiles/iip/SOUL.md.bak-2026-08-13-stage65`, `profiles/iip/user.md.bak-2026-08-13-stage65`
- Rollback = copy backup over live file (restores sol/openai-codex delegation + old SOUL) — verified restorable
- Skills: git-less but reversibility via content (all changes documented in this file + FD record)

---
<!-- 2026-08-13 01:10:00 +0700 — captured via scripts/artifact_timestamp.py (system clock at write) -->
