# IIP AI Organization — Kanban Board

**Status:** PROPOSED OPERATIONAL — FD #54 (2026-08-05). Repo-based single board (KANBAN-CONTRACT §10). Operational tracking only — card state never equals domain state.

## Columns

Inbox → Triage → Scoped → Data Ready → In Research → Cross-Review → Validation → Founder Review → Monitoring → Blocked → Closed

## Active Cards (pilot 2026-08-05)

| Card | Title | Column | Owner | Status |
|---|---|---|---|---|
| ORG-2026-0001 | Pilot: bounded review of research-result.md v1 (MSFT) | Closed (pilot complete) | Equity Alpha (simulated) | PILOT PASS |
| ORG-2026-0002 | Pilot: data readiness of source map (8 sources) | Closed (pilot complete) | Data Steward (simulated) | PILOT PASS |
| ORG-2026-0003 | Pilot: risk challenge of equity memo | Closed (pilot complete) | CRO (simulated) | PILOT PASS |
| ORG-2026-0004 | Pilot: Founder decision pack assembly | Founder Review (simulated) | IC Secretary (simulated) | READY FOR FOUNDER REVIEW |
| ORG-2026-0005 | Pilot: governance/lineage verification | Closed (pilot complete) | Internal Auditor (simulated) | PILOT PASS |
| ORG-2026-0006 | Radar (RADAR-001): Silver deficit changes character | Published | Commodity Analyst | PUBLISHED (gate A, 6 Aug) — silver-deficit-challenge + CRO companion |
| ORG-2026-0007 | Radar (RADAR-001): Apple repurchases lag operating acceleration | Published | Equity Analyst | PUBLISHED (gate A, 6 Aug) — apple-buyback-mask-test + CRO companion |
| ORG-2026-0008 | Radar (RADAR-001): Hawkish Fed, resilient gold | Published | Macro Strategist | PUBLISHED (gate A, 7 Aug) — gold-transmission-regime + CRO companion |
| ORG-2026-0009 | Radar (R2): London silver vault holdings rise to series high | Published | Commodity Analyst | PUBLISHED (gate A, 7 Aug) — london-silver-vaults-watch + CRO companion |
| ORG-2026-0010 | Radar (R2): Apple Services margin now directly testable | Published | Equity Analyst | PUBLISHED (gate A, 7 Aug) — apple-services-margin-verification + CRO companion |
| ORG-2026-0011 | Radar (R2): Apple share-count contraction persists | Published | Equity Analyst | PUBLISHED VIA 0010 (gate A, 7 Aug) — share-count evidence inside 0010 report |

## Rules

- Single writer at a time (CoS Assistant under instruction); git history = audit trail.
- WIP limits: 1 M2/M3 per Principal in In Research; Cross-Review ≤ 5; Founder Review ≤ 3 material.
- Only the IC Secretary moves a complete packet into Founder Review.
- Only an explicit Founder decision changes canonical governance state.
- Cards: `cards/<card_id>.yaml` (schema KANBAN-CONTRACT §3). Holds: `holds/<hold_id>.yaml`.
<!-- 2026-08-05 14:55 UTC+7 -->
