# S65-C — Gemini Access-Path Alignment (Stage 6.5, 13 Aug 2026)

## GEMINI PRODUCTION ACCESS-PATH VERDICT

**VERDICT: Stage 6 pilot path = Google AI Studio **API-key path** (usage-billed) — SEPARATE from the Gemini Pro / Notebook Deep Research subscription entitlement the Founder intends to purchase. NOT the same billing/quota path.**

## Evidence (from Stage 6 execution + Hermes source)

| Item | Stage 6 pilot (as-run) | Production intended (Founder) |
|---|---|---|
| Mechanism | `dispatch_gemini.py` → `google.genai` client → Gemini API **Interactions API background job** | Gemini Pro / Notebook Deep Research subscription entitlement |
| Auth | **API key** (`GOOGLE_API_KEY` in `profiles/iip/.env`) — `auth.py` ProviderConfig `gemini`: `auth_type="api_key"`, `api_key_env_vars=("GOOGLE_API_KEY","GEMINI_API_KEY")` | Google One AI Pro / NotebookLM Plus subscription (OAuth/entitlement-based) |
| Billing | Pay-per-token usage via Google AI Studio | Fixed subscription (included quota) |
| Model | `deep-research-max-preview-04-2026` via API | Deep Research / Notebook feature set |
| Provenance | S4-PROVENANCE.json: `"external_tool": "Gemini Deep Research agent (Google Gemini API, Interactions API, background job)"` — job `v1_ChdhNUo…`, prompt SHA-256 `94d476c9…` | TBD — requires integration work |

## Implication (why this matters)

Purchasing Gemini Pro / Notebook does NOT automatically reroute Hermes to it:
- Hermes' Gemini native adapter is **API-key based** (`gemini_native_adapter.py` — "Google Gemini rejected this API key's type — you do NOT need OAuth"; the 401 fix is "mint a new Gemini API key in AI Studio").
- The subscription path (OAuth/entitlement) is a **different integration** — not yet wired into the DR lane.

## Production recommendation (do NOT change v1.4 workflow — only access path)

| Option | Path | Cost model | Action |
|---|---|---|---|
| **A (recommended — keep as-is)** | Continue using the API-key Interactions path for the DR lane; treat Pro subscription as an ALTERNATE fallback/investigation track | Usage (already proven, 11.5-min job, 44,501 chars) | No change; record billing under Google AI Studio |
| **B** | Investigate Notebook/Pro entitlement integration for the DR lane | Subscription | Requires OAuth/entitlement adapter — engineering task (NOT Stage 6.5 scope) |
| **C** | Hybrid: API for the isolated lane, subscription for human-facing Notebook research | Both | Complex; deferred |

**Decision needed from Founder: A / B / C.** Default = A (proven, workflow unchanged, no new integration). The v1.4 analytical workflow (dispatch prompt + provenance + raw/frozen capture) is access-path-agnostic — unchanged under any option.

## Guardrails preserved
- No billing/quota path is assumed shared between API-key and subscription.
- No integration change made in Stage 6.5 (audit only — per Founder: "Do not alter the approved Gemini Deep Research v1.4 analytical workflow").
- `GOOGLE_API_KEY` value NOT logged/printed anywhere in this session.

---
<!-- 2026-08-13 00:50:00 +0700 — captured via scripts/artifact_timestamp.py (system clock at write) -->
