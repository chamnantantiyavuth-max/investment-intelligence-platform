# IIP AI Organization — Kanban Board

**Status:** PROPOSED OPERATIONAL — FD #54 (2026-08-05). Repo-based single board (KANBAN-CONTRACT §10). Operational tracking only — card state never equals domain state.

## Columns

Inbox → Triage → Scoped → Data Ready → In Research → Cross-Review → Validation → Founder Review → Monitoring → Blocked → Closed

## Active Cards (pilot 2026-08-05)

| Card | Title | Column | Owner | Status |
|---|---|---|---|---|
| ORG-2026-0001 | Pilot: bounded review of research-result.md v1 (MSFT) | In Research | Equity Alpha (simulated) | open |
| ORG-2026-0002 | Pilot: data readiness of source map (8 sources) | In Research | Data Steward (simulated) | open |
| ORG-2026-0003 | Pilot: risk challenge of equity memo | Cross-Review | CRO (simulated) | open |
| ORG-2026-0004 | Pilot: Founder decision pack assembly | Founder Review | IC Secretary (simulated) | open |
| ORG-2026-0005 | Pilot: governance/lineage verification | Triage | Internal Auditor (simulated) | open |

## Rules

- Single writer at a time (CoS Assistant under instruction); git history = audit trail.
- WIP limits: 1 M2/M3 per Principal in In Research; Cross-Review ≤ 5; Founder Review ≤ 3 material.
- Only the IC Secretary moves a complete packet into Founder Review.
- Only an explicit Founder decision changes canonical governance state.
- Cards: `cards/<card_id>.yaml` (schema KANBAN-CONTRACT §3). Holds: `holds/<hold_id>.yaml`.
<!-- 2026-08-05 14:55 UTC+7 -->
