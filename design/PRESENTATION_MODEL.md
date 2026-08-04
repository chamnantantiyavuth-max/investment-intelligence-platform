# Presentation Model — Investment Intelligence Platform

> **Phase F — ui-dashboard-workflow v4.0.0 · 2026-08-04 · FD #51 (A — Research Desk)**

## Representation by information need

| Information need | Preferred representation | IIP application |
|---|---|---|
| Current state | compact status / summary line | Theme lifecycle badge, conviction badge, surface status |
| Attention triage | ordered list + one dominant lead | Dashboard hero (single lead setup) + Findings ledger |
| Comparison | aligned table / delta / small multiples | Screener matrix; Cheap & Quality rows; II table |
| Change over time | time series / event timeline | (deferred — no chart-heavy surface in V0 UI; RS/price shown as numbers) |
| Distribution | histogram / percentile bands | Queue breadth finding (narrative), not chart |
| Composition | allocation table (no pie unless few stable parts) | Leadership concentration (ledger row) |
| Obligation / queue | ordered list / queue | AM Queue |
| Risk | severity + affected amount + cause + action | CS conviction + risks; Value Trap verdict + reasons |
| Decision | decision panel with context/options/evidence | Theme Card (thesis → falsification → judgment) |
| Detailed truth | dense table / ledger / expandable | Evidence register; falsification §11; methodology tier |
| Process | stepper only for linear progression | 6-stage AM pipeline shown as stage indicator (not a stepper UI) |
| Relationship | matrix / network only when relationship is the decision | Entity→theme roles on Theme Card |
| Empty state | explanation + valid next action | DNA-016: why empty, normal?, next step |
| Error/degraded | what failed / what's affected / what to do | C5: scoped error state, never coerce to zero |

## Chart integrity rules (for any future chart)

- Chart answers a user question, not "looks modern"; aligned number beats chart when clearer.
- No truncated axes, consistent units/time ranges/baselines; derived metrics explained; uncertainty shown when estimated; never color alone for meaning; no 3D/decorative gauges/chrome.
- V0 UI: **ledgers and tables carry the data**; charts only where the decision needs a shape (deferred).

## Anti-patterns rejected (with reason)

| Anti-pattern | Reject because |
|---|---|
| KPI card grid | Generic dashboard; metrics feed hero + ledger (METRIC_MODEL anti-pattern note) |
| Pie charts everywhere | Composition rarely the decision in V0 |
| Gauge/status-dial widgets | Decorative; a badge or number is clearer |
| Icon-in-colored-square tiles | Generic AI aesthetic; no meaning added |
| Green/red without explicit meaning | Colors always paired with text labels (mint/positive, pink/negative) |
| "AI insights" panel without evidence | Narrative claims must carry evidence links (C4) |
<!-- 2026-08-04 17:24 UTC+7 -->
