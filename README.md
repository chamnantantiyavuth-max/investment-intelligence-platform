# Investment Intelligence Platform

## What This Is

An investment **opportunity discovery** platform — it narrows the global investment search space while preserving evidence, uncertainty, disagreement, and decision history. It helps answer *"What deserves further investigation?"* — it does **not** autonomously decide what to buy, sell, or allocate.

> **Sacred boundaries:** no broker connectivity, no order execution, no automated allocation, AI advisory only, never rewrite history, Experimental ≠ official.

## Repository Layout

| Path | Contents |
|------|----------|
| `01-PROJECT-DNA.md` · `02-PROJECT-CONSTITUTION.md` | Product DNA + Constitution (v0.4, §23 AI Operating Constitution, Blind Portfolio Rule) |
| `PROJECT_BIBLE.md` / `DOMAIN_MODEL.md` / `FORBIDDEN_ACTIONS.md` / `ACCEPTANCE_EXAMPLES.md` | Phase -1 alias pointers to the authoritative documents |
| `project-definition/` | 10 approved domain specifications |
| `operational/` | FOUNDERS-DECISIONS (#1–44), ROADMAP, OPEN-QUESTIONS, VERIFICATION-DOCTRINE |
| `design/` | Alpha Momentum V0 design artifacts (143 themes, 20 acceptance scenarios, rule packs) |
| `alpha-momentum-v0/` | Strategy 1: momentum screening pipeline (S1–S6) + experimental quarantine |
| `close_system/` | Strategy 2: Close System Product Radar (P1–P3 eligibility) |
| `fundamental-opportunity-v0/` | Fundamental & Opportunity Intelligence (moat, earnings quality, value trap, FD #43 signals) |
| `institutional-intelligence-v0/` | Institutional Intelligence (13F filings, concentration ratio, conviction) |
| `shared/` | Shared templates |
| `backend/` | FastAPI thin API layer (AM/CS/FO routes) |
| `frontend/` | React 19 + Vite + TypeScript + shadcn/ui presentation layer |
| `evidence/` | Audit reports + council decisions (created 2026-08-02) |

## Status (as of 2 August 2026)

- **Phases 0–10.5 complete** (code artifacts delivered; FD #1–44 approved)
- **Phase 11 (Deep Research Handoff) NOT authorized** — deferred
- **Tests:** 262/262 Python tests passing · frontend `npm run build` exit 0
- **Provisional stack only:** Python + pandas + FastAPI + React/shadcn/ui — **not** claimed as final stack selection (SPEC AC-10)
- **Synthetic-data honesty:** FO/II pipeline output carries SYNTHETIC vs REAL watermarks; AM/CS/dashboard surfaces carry explicit SYNTHETIC/DEMO banners until real pipeline wiring is authorized
- **No schema/migration layer, no broker/execution/allocation**

## Quick Start

```bash
# Python tests (all modules)
python -m pytest -q

# Backend API
python -m uvicorn backend.main:app --port 8000

# Frontend (dev)
cd frontend && npm install && npm run dev

# Frontend build (verification)
cd frontend && npm run build
```

## Governance

Read `AGENTS.md` first — it defines authority order, the Domain Guardrail, and workflow governance. Build metrics (test/commit/FD counts) live in `PROJECT_STATE.md` (single source of truth). Audit artifacts live in `evidence/`.

## Foundation History

- Foundation v0.1 — Initial approved Constitution
- CTO Audit v0.1 — Completed
- Foundation v0.2 — Founder-approved governance and agent-safety hardening
- Foundation v0.3 — Theme governance-axis clarification (Approval Status + Monitoring Status)
- v0.4 — AI Operating Constitution (§23) · v0.5 — Blind Portfolio Rule (§23.8.1)

<!-- 2026-08-02 05:20 UTC+7 -->
