# Quality & Asymmetry Discovery (WP2 — ChatGPT FIT-GAP)

**Status:** Shadow phase — discovery-side, deterministic, portfolio-blind.
**Authorization:** Founder Option A (11 Aug 2026) — "แก้พวก workflow ที่ ChatGPT เสนอให้เสร็จก่อน" — WP2 of the 4-WP ChatGPT FIT-GAP. All numeric thresholds are **PROPOSED** (FD #53) — no production use until Founder approves validation evidence (same path as FD #88 → #89 for Equity Inflection).

## Purpose

Find exceptional businesses / mispricings that **do not** show up in anomaly
(Radar) or momentum/earnings-breakout (Equity Inflection) discovery:

> A company with high ROIC, long reinvestment runway, strong moat, great capital
> allocation — whose EPS didn't spike this quarter, whose price didn't just leave
> Stage 1, with no anomaly and no news. IIP currently has no systematic way to
> find it. (ChatGPT FIT-GAP, 11 Aug 2026)

## The four archetypes (NOT a score)

| ID | Archetype | Style lineage | Core question |
|----|-----------|---------------|---------------|
| A | Durable Compounder | Buffett / Li Lu | High & stable ROIC, strong FCF conversion, clean balance sheet, capital allocation |
| B | Long-Runway 100-Bagger | Fisher / 100 Baggers | ROIC × reinvestment rate × runway — "if the company generates $1 more cash, how much can it reinvest at high return?" |
| C | Mispriced Quality | Buffett / Li Lu | Great business where the market doubts: temporary problem, underestimated duration/moat, overreaction to a bad quarter |
| D | Asymmetric Value | Pabrai | Limited permanent downside + large upside: special situations, temporary distress, forced selling, holding-company discount, hidden asset, misunderstood cyclicality, big buyback at low valuation |

**Deliberately NOT a score:** Buffett/Li Lu/Fisher/Pabrai/100-Baggers are
different animals. A weighted "Buffett Score" would re-import Platform Disease
(checklist scoring). Archetypes are **lenses** — the engine reports which
signals each lens sees; the Equity Alpha Analyst (role 05) judges
"what deserves investigation?".

## Flow (from ChatGPT FIT-GAP)

```
Shared Equity Universe (WP1 — discovery/equity_universe.py, 98 names)
        │
        ▼
Quantitative candidate generation (archetype engine, shadow)
        │
        ▼
50–100 possible names → evidence reconnaissance (Equity Assistant)
        │
        ▼
15–25 interesting businesses → Equity Alpha Analyst reads / challenges
        │
        ▼
5–10 Task Idea Cards → CoS triage → 1–3 Full Company Deep Research
```

Funnel numbers are illustrative, not hard rules. The bottom half of the funnel
(the research organization: RM → independent first passes → cross-exam → CRO →
audit → FACTS LOCKED → IC Secretary → Founder gate → blog) is UNCHANGED —
WP2 only adds a new way to FIND ideas, it does not add a new research engine.

## Firewall (binding, FD #88 pattern)

The archetype engine output = deterministic evidence block ONLY. It NEVER:
- creates a Task Idea Card, enters CoS triage, or consumes research capacity
- auto-loads into independent research first passes (FD #64 item 7)
- publishes to the blog, or becomes a thesis/conclusion
- sets thresholds to production without Founder approval (FD #53)

CoS triage remains the ONLY entry into research capacity. Radar Scout (role 11)
is not the owner of this stream — **Equity Alpha Analyst (role 05) is the
Principal Owner** (ChatGPT FIT-GAP direction), with Equity Research Assistant +
Quant/Data supporting bulk search.

## Module layout

- `discovery/quality_asymmetry/archetypes.py` — pure deterministic archetype
  engine (no yfinance/numpy at import — runs in pytest venv 3.11). Input:
  already-fetched annual-financial dicts + optional market/recon dicts. Output:
  per-archetype evidence blocks.
- `tests/test_quality_asymmetry_archetypes.py` — 10 locked-style tests
  (contract, determinism, ROIC math, firewall, known cases).
- Fetcher: NOT built in this phase — the engine consumes already-fetched data
  (same architecture as equity_inflection: fetch layer runs under system
  Python 3.14, yfinance + SEC EDGAR companyfacts). Real-data shadow run is a
  future step (validated data pipeline → validation evidence → FD #53 approval).

## Boundaries

- Portfolio-blind (Constitution §23.8.1); advisory identity only.
- No broker connectivity, no allocation, no position sizing, no exit logic.
- No AI-invented rules, thresholds, weights, or fallback (FD #53).
- ADR flag in universe marks non-US domicile (identity only — no judgment).

<!-- 2026-08-11 12:30 UTC+7 -->
