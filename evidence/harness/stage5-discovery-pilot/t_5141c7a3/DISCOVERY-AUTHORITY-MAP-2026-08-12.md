# IIP Discovery Recall & Coverage Audit — Child A: Current Discovery & Authority Map

**Date:** 2026-08-12
**Author:** org-data-steward (Data Steward profile, discovery/mapping role)
**Task:** t_5141c7a3 — [DISC][CHILD] A — Current Discovery & Authority Map
**Parent:** t_500dd515 — IIP Discovery Recall & Coverage v1.1 (org-cos synthesis)
**Methodology anchor:** `investment-intelligence-platform/ChatGPT/Integration 12 Aug 2026/IIP_Discovery_Recall_Coverage_Audit_Final_Handoff_v1.1.md` (§32 A/B, §33 consolidate)
**Constraint:** BOUNDED mapping only — NO domain state change, NO new thresholds, NO new canonical states, portfolio-blind. Audit language only (SURFACED_HIGH / SURFACED_MAYBE / NOT_PROMOTED / INSUFFICIENT_DATA).
**Repo root:** `C:/Users/Admin/Desktop/Antigravity/investment-intelligence-platform/`

---

## 1. Current Discovery Pipeline Map (as-built, 12 Aug 2026)

```
UNIVERSE (deterministic denominators)
   ├─ Equity: discovery/equity_universe.py — 98 names (FO-8 core + US large/mid-cap + ADRs),
   │   CIK-verified vs SEC company_tickers.json as-of 2026-08-11, PIT identity (FD #58), FD #95 WP1
   └─ Close System: commodity watch list (gold / silver / copper / oil) — CS Product Discovery v0.1 (FD #97)

DISCOVERY LANES
   E1 Radar Scout (role 11, org-radar-scout) — open-ended anomaly/divergence/filing discovery
      ├─ cron: weekly Mon 08:00 UTC+7 (job 8ba233e88015, FD #78) + mid-week Thu 08:00 (job cda817d17236, FD #80)
      ├─ EDGAR 8-CIK standing scan (FD #81) — AAPL/MSFT/NVDA/GOOGL/AMZN/META/TSLA/JNJ; MSFT = CIW boundary digest-only
      ├─ feedback loop: reads kanban/card-outcomes.md (FD #82 — do-not-reraise / known-gap / refine)
      └─ output: 0–3 Task Idea Cards/pass → kanban Inbox + Radar Digest → kanban/digests/
   E2 Equity Inflection (discovery/equity_inflection/) — deterministic EPS-breakout scanner
      ├─ FD #88 authorized (shadow) → FD #89 STANDING BEHAVIOR + Stage Def v0.1 thresholds = PRODUCTION
      ├─ standing instrument: run_universe_scan.py over full 98-name universe (11 Aug: ABBV/BMY/LLY/VRTX)
      ├─ firewall: deterministic evidence blocks ONLY — never auto-RM/thesis/publication; CoS triage = only entry
      └─ output: evidence blocks → (design: Radar packaging) → Task Idea Cards → CoS triage
   E3 Quality & Asymmetry (discovery/quality_asymmetry/) — 4 archetype lenses (A Durable Compounder /
      B Long-Runway 100-Bagger / C Mispriced Quality / D Asymmetric Value)
      ├─ FD #95 WP2; SHADOW phase — all thresholds PROPOSED (FD #53), role 05 = Principal Owner
      ├─ shadow run 11 Aug: 98 rows scanned / 71 with archetype evidence (FD #97 text says "62 evidence blocks")
      └─ firewall (FD #88 pattern): never cards / never CoS / never publish
   C1 CS Product Discovery (discovery/cs_product/discovery.py) — watch-input collector + spec §5
      pattern matcher (Cyclical Trough / Sentiment Divergence / Dislocation / Inventory / Physical-vs-Paper)
      ├─ FD #97 (un-deferred); SHADOW; PROPOSED thresholds (FD #53); role 03 = Principal Owner
      └─ honest-empty: LBMA silver 404 / tradingeconomics 403 noted, never invented

TASK IDEA CARDS (kanban/cards/ORG-2026-XXXX.yaml, schema KANBAN-CONTRACT §3)
   21 cards on disk (0001–0021). Filed by: Radar Scout cron (0006–0017), Equity Inflection universe
   scan session (0018–0021, FD #97). All enter the kanban Inbox column.

CoS TRIAGE (D1) — Founder Chief of Staff (role 01, org-cos)
   Classify intake (anomaly/theme/product/macro/company/options/data/quant/risk/audit) + assign:
   task ID, research question, decision user, required-by, domain owner, evidence standard,
   expected artifact, dependencies, explicit non-goals (DAILY-WEEKLY-WORKFLOW D1).
   CoS is the ONLY entry into research capacity (FD #88/#89 firewall).
   Precedent: "TRIAGED (Founder A, 6 Aug)" marker; 0013/0014 folded at triage; 0012 DEFERRED with re-test trigger.

RESEARCH MANDATE (RM-####) — scoped by CoS (role 01)
   CoS scopes the mandate + forms the smallest research cell (lead + relevant support, never all 10).
   Mandate files: research/mandates/ (RM-2026-0001 APL moat, 0002 SLV, 0003 JNJ on disk;
   0004 AAPL deep-analysis executed via workspace research/companies/AAPL/deep-analysis-2026-08-09/).

RESEARCH EXECUTION (template 16 — DEEP-RESEARCH-STANDING-CONTRACT, FD #95 WP3)
   anti-anchoring first pass → evidence build → main essay → cross-exam (material claims only) →
   CRO opposing (Sol Medium, FD #73) → audit/re-audit → IC Secretary synthesis → Founder gate → publish.
   Outputs: reports/*.md main + -opposing- companion; research/companies/<TICKER>/ workspaces.
```

## 2. Authority Ownership (per AUTHORITY-MATRIX v0.1 + ROLE-REGISTRY v0.1)

| Stage | Owner | Authority (may) | Boundaries (may not) |
|---|---|---|---|
| Universe membership | Shared layer (WP1) | Deterministic membership criteria documented (FD #53) | No AI-invented thresholds; expansion needs evidence + Founder |
| E1 Radar scanning | Radar Scout (11) | Scan broadly; write Task Idea Cards to Inbox; recommend materiality/domain/owner (advisory); Anomaly Log | No analysis/theses; no assigning work; no moving cards past Inbox; no state change |
| E2 Inflection scan | Standing scanner (FD #89) | Deterministic evidence blocks; standing instrument | Never auto-cards/RM/publish; cron/cards/radar/blog changes need separate FDs |
| E3 Quality & Asymmetry | Equity Alpha (05) Principal Owner | Shadow evidence generation only | Thresholds PROPOSED only; no production use until Founder approves validation |
| C1 CS Product | Commodity (03) Principal Owner | Shadow watch-input + pattern matching | PROPOSED thresholds only; honest-empty required |
| Card filing | Radar (11) + session runs | Cards to Inbox | Never past Inbox |
| Triage (D1) | CoS (01) | Classify, assign owner/artifact/non-goals, scope RMs, form cells, reduce/sequence/pause | No approving conclusions/themes/doctrine; no clearing Holds; no editing conclusions |
| Data readiness (D2) | Data Steward (09) | DATA READY / READY WITH LIMITATIONS / DATA HOLD | No converting limitations into confidence |
| Research (D3) | Domain Principal (03–06) | Frame question, produce artifact, sign conclusion | Assistants never sign |
| Challenge (D4) | CRO (07) / Quant (08) / Data (09) | Risk/validation Holds | Holds = org-workflow pause only; Founder-only override |
| Founder Review gate | IC Secretary (02) | Admin completeness gate; sole mover into Founder Review | Administrative only — not an investment vote |
| Canonical state change | Founder only | approval_status/monitoring/thesis/research/artifact transitions | — |
| Audit | Internal Auditor (10) | Governance Holds; audit orchestration | Execution via Sol Medium (FD-HERMES-007) |

## 3. Funnel (bounded denominators, as of 12 Aug 2026)

- Equity universe: 98 names (deterministic). CS watch universe: 4 commodities.
- Radar passes: 3 digests on disk (2026-08-07 weekly, 2026-08-07 midweek, 2026-08-10 weekly).
- Task Idea Cards: 21 filed (0001–0021). 6 radar cards → published reports (0006–0011, 0013, 0015);
  0014 folded into 0013; 0012 deferred (Blocked, re-test trigger); 0016–0021 in "Research" column
  (6 cards: LBMA vaults, GOOGL raise, ABBV/BMY/LLY/VRTX inflection candidates).
- Research Mandates: RM-2026-0001..0004 (0001/0002/0003 published; 0004 AAPL deep-analysis published FD #87).
- QA shadow: 98 rows scanned, 71 archetype evidence blocks, 0 cards (shadow phase — no promotion).
- CS shadow: v0.1 engine built, 0 cards.
- Published library: ~24 reports (14 research notes after companion nesting, FD #96).

## 4. Authority / Documentation Drift (methodology §2 — report, do not silently reconcile)

| # | Drift | Evidence | Severity |
|---|---|---|---|
| D1 | `workflow_column` vocabulary violates KANBAN-CONTRACT §2: cards 0006–0011/0013/0015 use `Published`, 0016–0021 use `Research` — neither is in §2 column list (Inbox/Triage/Scoped/Data Ready/In Research/Cross-Review/Validation/Founder Review/Monitoring/Blocked/Closed) | cards/*.yaml vs KANBAN-CONTRACT §2 | HIGH (audit/observability) |
| D2 | `kanban/board.md` stale: lists only ORG-2026-0001..0011; 0012–0021 on disk but not on board | board.md (11 rows) vs cards/ (21 files) | MEDIUM |
| D3 | equity_inflection README header still says "Shadow phase (Phase 0) — SHADOW-gated: no standing production behavior until Founder approves validation evidence" — superseded by FD #89 (10 Aug) STANDING BEHAVIOR + production thresholds; body §Stage Definition updated but header + §Boundaries unchanged | README lines 5/26/115 vs FOUNDERS-DECISIONS #89 | HIGH (authority/runtime conflict) |
| D4 | Card filing path drift: FD #88/#89 design = scanner output → Radar Scout packaging → card; actual 0018–0021 filed directly from universe-scan session (FD #97) — radar packaging step not evidenced | FOUNDERS-DECISIONS #88/#89/#97; card YAMLs | MEDIUM |
| D5 | QA shadow count: FD #97 text says "62 evidence blocks"; runtime JSON = 98 rows / 71 with archetypes | FD #97 vs shadow-evidence-2026-08-11.json | LOW |
| D6 | RM-2026-0004 executed + published (FD #87) but no mandate file in research/mandates/ (only 5 files there); record lives in FD register + research/companies/AAPL workspace | research/mandates/ vs FOUNDERS-DECISIONS #87 | LOW |

## 5. Where Recall Can Be Lost — Miss Taxonomy Risk Map (M1–M7)

| Miss | Current evidence | Measured? | Severity | Notes |
|---|---|---|---|---|
| M1 Universe | Equity deterministic lanes bounded by 98-name universe; CS lane = 4 commodities vs approved spec (broad-market/sector ETFs, fixed income, strategic minerals...) | PARTIAL (universe count known; out-of-universe counterfactual NOT run — §11 proposed only) | HIGH | H1/H5 supported: universe breadth is the first-order recall bound |
| M2 Data | Known gaps registered: COMEX deliverable (CME 403), lease rates (no free source), CFTC COT (404), LBMA silver JSON (404), tradingeconomics (403), FRED lag; QA 27/98 rows without archetype evidence | YES (card-outcomes.md known-gap table + retry policy) | MEDIUM | Gaps are tracked with retry policy — good; still produce INSUFFICIENT_DATA class |
| M3 Detector | Inflection: thresholds production (FD #89) but detector bounded (H1/H2 windows, MIN_QUARTERS 9, stage filters); survivorship limitation D1 acknowledged; CS matcher v0.1 = 5 patterns, PROPOSED thresholds; QA archetypes PROPOSED | PARTIAL (validation Phase 1 for inflection only) | MEDIUM | Detector-miss measured only for FO-8 universe, not full 98 |
| M4 Judgment | Radar digests document "deliberately ignored and why" (good); QA 71 evidence blocks → 0 cards, no disposition log for why each was not promoted | NO (no rejected-item register; digest prose only) | **HIGH** | Key Founder concern (H2). Rejected-before-card items have no structured disposition trail |
| M5 Cadence | Radar Mon+Thu cadence; event-driven triggers exist (§4 workflow); filing→triage observed ~1 day (0016/17 filed 10 Aug, triage 11 Aug) | NO (T0–T5 latency not systematically measured) | MEDIUM | No unexplained multi-day blind window observed in sample |
| M6 Triage | 0012 DEFERRED with re-test trigger (do-not-reraise until macro window settles); 0013/0014 folded; card-outcomes register tracks outcomes | PARTIAL (deferral recorded; independent triage re-review NOT done) | MEDIUM-HIGH | H6: CoS is an under-audited second false-negative gate |
| M7 Authority/workflow | Drifts D1–D6 above; M7 = surfaced-but-blocked cases | YES (drift inventory) | MEDIUM | D1/D3 are the material ones |

## 6. Recall Proxies Status (methodology §6 — bounded denominators only)

1. **Historical PIT benchmark:** DONE for Equity Inflection (Phase 1 validation: 21 quarter-ends × FO-8, 0 look-ahead/168, 0 revision flips/48 — FD #89). NOT done for full 98-name universe, QA archetypes, or CS lane.
2. **Rejected-item independent audit:** NOT RUN. Radar ignores recorded in digest prose only; QA 71 evidence blocks have no disposition. This is the largest unmeasured area.
3. **Out-of-universe counterfactual scan:** NOT RUN (methodology §11 — proposed, not executed).
4. **Coverage matrix / blind-spot analysis:** NOT BUILT (CS spec-to-implementation matrix missing; equity archetype white-space map missing).

## 7. Audit-Language Labels for the Bounded Sample (not canonical states)

- Radar: SURFACED_HIGH = filed cards (21); digest-ignored items = NOT_PROMOTED (recorded in prose, e.g., META Form 4 cluster, 13F-HR season, gold continuation, Hormuz, AMZN S-4).
- QA shadow: 71 evidence blocks = SURFACED_MAYBE → NOT_PROMOTED (no cards); 27 rows without archetypes = INSUFFICIENT_DATA.
- CS shadow: no output yet — INSUFFICIENT_DATA (LBMA silver 404, tradingeconomics 403, CME 403).

## 8. Smallest Recommended System Changes (for parent synthesis — NOT implemented)

1. Fix D3 (README shadow→standing) — documentation only, no code.
2. Fix D1 (column vocabulary) — align cards to §2 columns or amend §2; board.md refresh (D2).
3. Add rejected-item disposition capture (audit-only, §9 labels) — cheapest observability fix; supports M4/M6 measurement.
4. Run the 4 recall proxies (PIT benchmark extension, rejected-item audit, out-of-universe scan, coverage matrix) — bounded, per methodology §10–§12, §17.

---
*Child A deliverable — mapping only, no domain state change. Audit language per methodology §9/§26. Parent (org-cos) owns synthesis + Founder-ready packet.*
<!-- 2026-08-12 22:40 UTC+7 -->
