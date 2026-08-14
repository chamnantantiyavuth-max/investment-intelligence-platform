# HERMES FREE-AUXILIARY INTEGRATION PLAN

## Objective
Reduce recurring LLM cost without lowering quality at decision boundaries.

Target:
- DeepSeek V4 Flash High / OpenRouter = Main
- Free OpenRouter models = low-risk side jobs
- GPT-5.6 Luna High = premium escalation
- Gemini 3.6 Flash High = independent Auditor
- NotebookLM / Gemini DR = independent Deep Research

## Phase A — preparation only
Do not mutate production before the 17 Aug Radar proof.

Inventory:
- Main provider/model/reasoning
- delegation route
- fallback chain
- all auxiliary slots
- compression settings
- provider routing
- Radar Cron route
- profile-specific overrides

Record baseline:
- auxiliary calls
- token/cost analytics
- failures/retries

Verify current free slugs:
- `nvidia/nemotron-3-ultra-550b-a55b:free`
- `nvidia/nemotron-3-nano-30b-a3b:free`
- `google/gemma-4-26b-a4b-it:free`

## Phase B — isolated canary

### Compression
Test Nemotron Ultra free against historical non-sensitive long context.
Must preserve:
- Founder decisions
- gates / HOLD
- blockers
- unresolved dissent
- current state
- provenance / file references
- dates
- negations such as NOT APPROVED / DISABLED

Any invented decision or dropped gate = FAIL.

### General text auxiliaries
Test Nemotron Nano on:
- 10 titles
- 10 profile descriptions
- 10 web extracts
- TTS tags if used

### Vision
Test Gemma 4 on 10 representative screenshots/document images.

## Phase C — Main provider migration after Stage 8
Target Main:
DeepSeek V4 Flash High -> OpenRouter

Provider-routing goals:
- price-efficient compatible endpoint
- require_parameters = true
- data_collection = deny
- verify actual provider slug before excluding any specific DeepSeek-hosted endpoint

Emergency fallback:
DeepSeek Direct API

Luna and Gemini do not enter automatic fallback.

## Phase D — Tier-0 rollout
Promote:
- compression -> Nemotron 3 Ultra free
- title_generation -> Nemotron 3 Nano free
- profile_describer -> Nemotron 3 Nano free
- tts_audio_tags -> Nemotron 3 Nano free
- web_extract -> Nemotron 3 Nano free
- vision -> Gemma 4 26B A4B free

Keep DeepSeek paid:
- approval
- kanban_decomposer
- curator/background review
- governance-sensitive classifiers

Every OpenRouter auxiliary gets its own privacy routing in `extra_body`.

Important: prove fallback behavior rather than assuming free OpenRouter -> paid OpenRouter works as a task-specific fallback.

## Phase E — real-usage observation
Observe for ~3 days:
- free calls attempted / succeeded
- paid fallback count
- auxiliary errors
- compression-fidelity incidents
- latency
- paid auxiliary cost before/after

PASS requires zero critical-state loss and graceful fallback.

## Phase F — optional Tier 1
One slot at a time:
- triage_specifier
- skills_hub
- mcp

No automatic mass rollout.

## Non-goals
- no free Main
- no free Auditor
- no free Founder Gate
- no free final research synthesis
- no free security/privacy decision
- no random `openrouter/free` production router
- no Live Office changes
- no Kanban architecture changes
