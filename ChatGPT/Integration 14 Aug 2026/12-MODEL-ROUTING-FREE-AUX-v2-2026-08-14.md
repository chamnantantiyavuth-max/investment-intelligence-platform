# 12 — IIP MODEL ROUTING + FREE AUXILIARY INTEGRATION v2
## Founder-side Knowledge Delta — 2026-08-14

This file supersedes older model-routing statements, including file #11 if present.
It does not supersede IIP/IPM separation, Founder authority, evidence doctrine, Harness stage status, or Live Office freeze.

## Target routing
- Main: **DeepSeek V4 Flash High via OpenRouter**
- Premium escalation: **GPT-5.6 Luna High via OpenRouter**
- Independent Auditor: **Gemini 3.6 Flash High via Google subscription / Antigravity CLI**
- Deep Research: **NotebookLM / Gemini Deep Research**
- Emergency cross-provider fallback: **DeepSeek Direct API**
- Founder: final authority

## Free Auxiliary Layer
Free models are opportunistic capacity for low-blast-radius side jobs only.

### Tier 0
- Compression: `nvidia/nemotron-3-ultra-550b-a55b:free`
- General text aux: `nvidia/nemotron-3-nano-30b-a3b:free`
- Vision: `google/gemma-4-26b-a4b-it:free`

Initial text slots:
- title_generation
- profile_describer
- tts_audio_tags
- web_extract

### Keep paid/reliable initially
Do not put free models in:
- approval / dangerous-command classifier
- kanban_decomposer
- curator / governance review
- Founder Gates
- research conclusion
- security/privacy judgment
- Stage transition judgment

### Tier 1 after evidence
Only after Tier 0 proves stable, test:
- triage_specifier
- skills_hub
- mcp
with the free text auxiliary model.

## Privacy rule
Every free OpenRouter auxiliary task must explicitly enforce privacy routing because auxiliary tasks do not automatically inherit Main provider routing:
- `data_collection: deny`
- `require_parameters: true` where appropriate
- test ZDR availability separately
If no compliant free endpoint exists, use the paid reliable model.

## Free-capacity rule
FREE AUX -> unavailable / rate-limited / privacy-incompatible -> RELIABLE PAID MODEL

Do not use `openrouter/free` random routing in IIP production.
Pin named free models.

## Rollout order
1. Do not modify production routing before the 17 Aug Weekly Radar Stage-7 proof.
2. Prepare isolated canaries only.
3. Run the Radar proof on the existing proven route.
4. If clean: Stage 7 FINAL PASS.
5. Complete Stage 8 old-board retirement.
6. Migrate Main from DeepSeek Direct to DeepSeek V4 Flash High via OpenRouter.
7. Canary and promote Tier-0 free auxiliaries.
8. Observe real usage for several days.
9. Promote Tier-1 one slot at a time only if evidence supports it.

## Success definition
- no organizational regression
- no Kanban authority change
- no Live Office semantic change
- no portfolio leakage
- no free model can approve dangerous actions
- compression preserves all critical state
- privacy enforced per auxiliary request
- free failures degrade gracefully
- paid auxiliary spend falls materially
- DeepSeek remains Main
- Luna remains premium escalation
- Gemini remains independent Auditor
