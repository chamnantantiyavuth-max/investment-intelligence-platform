# Metric Model — Investment Intelligence Platform (Phase B)

> **ui-dashboard-workflow v4.0.0 · Phase B · 2026-08-04 · FD #51 (A — Research Desk)**
> Decision-first: metrics exist to support the Founder's discovery decision, not to fill cards.

## Primary user & decision

- **Primary user:** Founder (Chamnan) — solo operator, momentum-first opportunity discovery
- **Primary question:** "What deserves my attention NOW, and what would change my mind?"
- **Primary decision:** which theme/candidate to read next (and whether the current thesis still holds)

## Primary metrics (3)

| ID | Metric | Type | Meaning | Source fields | Representation (NOT KPI cards) |
|---|---|---|---|---|---|
| M1 | **Actionable setups** — themes with entry-readiness gate satisfied / near-satisfied | outcome | What is actionable now | AM candidate gate status, RS rank, lifecycle | Ledger rows in Findings; hero states the single strongest setup |
| M2 | **Thesis health mix** — lifecycle/conviction distribution (confirming / watching / challenged) | outcome | What is healthy vs at risk | Theme lifecycle, conviction, falsification open items | Findings narrative + Theme Card badges; no aggregate score |
| M3 | **Surface truthfulness** — provenance per surface + staleness status | guardrail | What can I trust | data_source (real/hybrid/synthetic), point_in_time vs staleness bound | ProvenanceChip per component, as-of stamps, staleness banner |

## Drivers (per primary metric)

- **M1 ←** entry-readiness gate pass rate · breakout proximity (RS/price structure) · queue breadth (coverage)
- **M2 ←** conviction trend (qualitative) · lifecycle stage · open falsification items (FD #50 fields)
- **M3 ←** data_source mode · artifact age vs bound (AM 7d / FO 30d / II 120d — FD #47 D3) · run id

## Guardrails (1–2, hard)

- **G1 — Provenance honesty:** every number carries real/hybrid/synthetic label; CS always SYNTHETIC DEMO prominent; AM hybrid never flattened to REAL (audit C3 fix).
- **G2 — No invented authority:** no composite quality scores, no derived FO/II scores (audit C-02 quarantine until formula FD), no AI-invented thresholds. Advisory-only footer on every page.

## Anti-pattern note

Dashboard must NOT render a KPI-card grid (M1–M3 feed the hero + findings ledger + provenance rail — not cards). Research Desk direction: typography + ledger tables carry the metrics.

## Non-metrics (explicitly not dashboard KPIs)

- Portfolio value / P&L / performance (out of scope — no portfolio data, FD #46)
- Model accuracy claims (not a trained model product)
- Raw counts of everything (SMART-SCOPE — only decision-relevant numbers)
<!-- 2026-08-04 17:05 UTC+7 -->
