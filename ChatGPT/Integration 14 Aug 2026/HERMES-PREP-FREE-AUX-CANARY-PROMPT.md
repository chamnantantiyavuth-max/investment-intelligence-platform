# HERMES — PREPARE FREE AUXILIARY + OPENROUTER INTEGRATION

IMPORTANT: PREPARATION / CANARY ONLY until Stage 7 FINAL + Stage 8 retirement.

Founder target:
- Main: DeepSeek V4 Flash High via OpenRouter
- Premium escalation: GPT-5.6 Luna High via OpenRouter
- Auditor: Gemini 3.6 Flash High via Google subscription / Antigravity CLI
- Free aux candidates:
  - compression: `nvidia/nemotron-3-ultra-550b-a55b:free`
  - general text: `nvidia/nemotron-3-nano-30b-a3b:free`
  - vision: `google/gemma-4-26b-a4b-it:free`
- Emergency fallback after migration: DeepSeek Direct API

HARD HOLD:
Do NOT alter current production routing before the real 17 Aug Weekly Radar Stage-7 proof.
Do NOT touch Live Office, Native Kanban authority, old-board ACL, Stage-8 scope, board `other`, IPM, or research doctrine.

1. Inventory actual current config:
   Main, delegation, fallback_providers, every auxiliary slot, compression,
   provider_routing, Radar Cron, profile overrides.
   Never print secrets.

2. Verify the exact free model slugs/capabilities from live OpenRouter.
   Do not silently substitute a similarly named model.

3. Verify per-model privacy-compatible free endpoints.
   Prepare per-task OpenRouter `extra_body.provider` with
   `data_collection: deny` and `require_parameters: true` where appropriate.
   Test ZDR separately.

4. Run isolated canaries without mutating global production config:
   A) compression fidelity
   B) text auxiliaries
   C) vision

5. Prove fallback behavior.
   Do not assume OpenRouter-free -> OpenRouter-paid task fallback works exactly
   as expected. Verify the installed Hermes runtime.
   Free failure must degrade to a reliable model with no privacy relaxation.

6. Produce PRE-CUTOVER report only:
   - current routing map
   - proposed post-Stage8 map
   - canary results
   - privacy results
   - fallback proof
   - estimated savings
   - exact config diff that WOULD be applied later
   - PASS/HOLD recommendation

STOP. Do not promote anything until Founder confirms after Stage 7 FINAL and Stage 8 retirement.
