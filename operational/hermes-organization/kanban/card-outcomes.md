# Card Outcomes Register — Radar Feedback Loop (FD #82)

> **Purpose:** closes the radar feedback loop — records what happened to every Task Idea Card after it left the Inbox, so the radar's standing watchlist is refined by research outcomes instead of staying static. The radar RAISES questions; this register records what the research team did with them and what the radar should watch (or stop re-raising) next.
> **Owners:** IC Secretary / session closeouts update this register when cards reach research outcomes (triage, publish, drop). **Radar cron jobs (FD #78/#80/#81) READ it only** — read-only input, never written by the scan.
> **Rule:** a card marked `do-not-reraise` must not be re-filed by the radar (same question, same evidence base). A `known-gap` watch item is retried only when a new source, season, or event appears — not every pass.
> **Created:** 2026-08-07 (FD #82, radar gap (c)). Backfilled from RADAR-001 outcomes (published reports, 6–7 Aug 2026).

## Outcomes

| card_id | domain | status | verdict / outcome (sourced) | watchlist implication | do-not-reraise / known-gap |
|---------|--------|--------|-----------------------------|----------------------|---------------------------|
| ORG-2026-0006 | COMMODITY | PUBLISHED | Silver deficit persists without demand growth (World Silver Survey 2026: 40.3Moz 2025 / 46.3Moz 2026 f); demand-growth framing refuted; inventory-liquidity replacement hypothesis = working, not concluded (`silver-deficit-challenge-2026-08-06.md` + CRO) | refine → inventory/liquidity watch items (vaults, COMEX, lease rates) → led to 0009/0013/0014 | — |
| ORG-2026-0007 | EQUITY | PUBLISHED | Apple buyback: 9M cash paid −12.0% YoY in a +16.4% rev quarter; ASR settlement timing = leading hypothesis; durable deceleration UNRESOLVED (`apple-buyback-mask-test-2026-08-06.md` + CRO) | refine → Q3 10-Q authorization usage + share-count continuation → folded 0011 into 0010 | — |
| ORG-2026-0008 | CROSS-ASSET | PUBLISHED | Gold +24.6% YoY vs 47bp real-yield rise: flow-dominance hypothesis consistent, NOT established; no permanent break (`gold-transmission-regime-2026-08-06.md` + CRO) | refine → gold behavior on further real-yield moves / FOMC → led to 0012 | — |
| ORG-2026-0009 | COMMODITY | PUBLISHED | London vaults 902.843 Moz (Jun 26, +18.04% YoY) materially weaken the visible-inventory depletion proxy; available-stock + liquidity normalization UNRESOLVED (`london-silver-vaults-watch-2026-08-06.md` + CRO) | refine → available-stock/free-float + COMEX deliverable + lease rates → led to 0013/0014 | — |
| ORG-2026-0010 | EQUITY | PUBLISHED | Apple Q3 FY26 Services GM 75.62% substantiated from filed 10-Q lines; dissent ~75.6% level source-cleared; trend + tariff-refund segment allocation UNRESOLVED (`apple-services-margin-verification-2026-08-06.md` + CRO) | refine → tariff-refund allocation; Ternus-era capital-allocation signal at Q4 FY26 (~Oct 2026) | — |
| ORG-2026-0011 | EQUITY | FOLDED → 0010 | Share-count continuation delivered inside 0010 (14,594,180,000 sh 2026-07-17 vs 14,608,963,000 2026-06-27) | n/a (folded) | — |
| ORG-2026-0013 | COMMODITY | PUBLISHED (7 Aug) | RM-2026-0002 COMPLETE + PUBLISHED (Founder gate A) — main `reports/silver-squeeze-repricing-test-2026-08-07.md` (verdict: visible data points away from scarcity — vaults series-high, COMEX registered rising, SLV flat → consistent with reflation beta, squeeze not established; audit 20/20 PASS incl. beta 1.4× fix) + CRO `-opposing-` (gross ≠ free float, lease-rate false-negative, ratio compression = thesis's own transmission mechanism — verdict outruns evidence). ORG-2026-0014 folded in (COMEX input) | refine → monitoring conditions updated (lease rates, COMEX drawdown, LBMA July, physical premium, ETF flows); series 0006→0009→0013 converged on 'no visible scarcity signal as of 7 Aug' | — |
| ORG-2026-0014 | COMMODITY | CLOSED (7 Aug) | FOLDED INTO 0013 (Founder triage A) — COMEX registered 99.8 Moz (+6.8 Moz/30d, 2026-08-06, metalcharts) becomes key evidence input for RM-2026-0002; CME-primary confirmation still gapped | n/a (folded) | — |
| ORG-2026-0015 | EQUITY | INBOX (7 Aug) | pending — next research pass after RM-2026-0002 (Founder triage A order) | pending | — |
| ORG-2026-0012 | MACRO | BLOCKED (7 Aug) | DEFERRED per Founder triage A — re-test at a settled macro window (Hormuz live, jobs-report day); gold watch-item monitoring continues via weekly radar | pending (re-test later) | do-not-reraise until macro window settles |

## Known data gaps (retry policy)

| Gap | Retries so far | Status | Retry trigger |
|-----|---------------|--------|--------------|
| COMEX deliverable silver stocks (CME primary) | 2 (0009 pass, mid-week 7 Aug) | KNOWN-GAP (third-party used: metalcharts 99.8 Moz registered 2026-08-06 → card 0014) | CME unblocks / Data Steward D2 confirmation |
| Silver lease rates (free verifiable source) | 2 (0009 pass, mid-week 7 Aug) | KNOWN-GAP | new free source appears (OTC market; LBMA does not publish a free current series) |
| LBMA vault July 2026 | 1 (mid-week 7 Aug — not yet published) | ACTIVE (monthly cadence) | next pass after publication (retry automatically; June 2026 = latest) |
| FRED DFII10 8/6+ observations | 2 | KNOWN-GAP (FRED lag) | FRED CSV catches up (retry each pass; latest 2.41% 8/5) |

<!-- 2026-08-07 17:10 UTC+7 -->
