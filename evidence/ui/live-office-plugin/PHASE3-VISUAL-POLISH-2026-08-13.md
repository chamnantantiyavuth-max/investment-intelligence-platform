# PHASE 3 — VISUAL POLISH / LIVING OFFICE (v1.2.0)

> Live Office v1 · Phase 2.1 = **PASS** (Founder, 2026-08-13) → **LOGIC FREEZE**
> Phase 3 scope: visual/interaction/UX ONLY. No state-derivation changes.
> Objective: "เปิดมาแล้วรู้สึกว่ากำลังมองเห็น AI Organization ทำงานอยู่"
> Target: 65–70% operational command center / 30–35% living pixel office.
> Checkpoint: 9 deliverables → STOP for Founder visual review.

## What changed (presentation layer only)

| Area | Delivery |
|---|---|
| Office environment | Pod zones per Founder sketch: FOUNDER OFFICE (focal, glowing) → TRANSITION (IC) → ORCHESTRATION (CoS) → RESEARCH POD (4) + INTELLIGENCE/VALIDATION POD (2) → REVIEW/CONTROL (2) → EXTERNAL SENSING (Radar). Zone-tinted floor, grid texture, lane labels. |
| Agent avatars | Original pixel SVG per role with distinct workstation MOTIF: CoS=coordination hub, IC=doc stack, Commodity=barrel, Macro=globe, Equity=chart, Options=candles, Quant=dual monitors, Data=server rack, CRO=shield, Auditor=magnifier+checklist, Radar=dish. No third-party art. |
| Truthful live behaviour | Per-state visuals on every workstation: screen glow (working green / awaiting pink / error red / blocked / review / done), typing dots, breathing, pulse, doc float — all tied to real presentation states only. |
| Founder Office | Focal panel: emblem + decision count + gate rows (originating desk + abbreviated task). READ-ONLY (no approve/reject). |
| Awaiting Founder direction | Floating `▲ FOUNDER` chip above each awaiting desk (IC + Macro live) — real state-driven, no fake arrows across the floor. |
| Real handoffs | S1 semantics preserved exactly: ACTIVE (visible line + packet on real event), RECENT (faint fading), HISTORICAL (hidden, History toggle). Zero active handoffs → zero lines (quiet office is truthful). Lines now drawn desk-EDGE to desk-EDGE (previously center-to-center hid behind cards). Packet enlarged + glowing. |
| Agent detail drawer | Click any desk → read-only drawer: role, profile, state, current task, open count, worker, last activity, DIAG badge, handoff edges (class-tagged), recent events. |
| Observability rail | Compact collapsible: Recent Activity / Workers-Runs / Handoff history toggle. |
| Top summary strip | Active Agents · Running · Blocked · Awaiting Founder · Recent Event — derived only from existing API truth. |
| Responsive | 1440×900: Founder + IC + CoS + full Research + full Intel visible; Review/Radar below fold (scroll). 1920×1080: +Review visible. Full-page captures included. |

## Backend touches (2, both read-only / genuine-defect fixes)

1. **`/activity?profile=` filter** (additive, read-only) — the drawer's "recent
   relevant events" needs per-desk events; no semantics change.
2. **WS live-tail fix** — genuine liveness defect exposed by visual work: the
   events cursor started at 0 and paged through the full history at 200
   events/2s, delaying real events by minutes. Now starts at `MAX(id)` at
   connect → true live streaming (packet pulse verified firing within ≤1s).

## Checkpoint evidence (9/9)

1. **1440×900 polished** — `p3-1440-clean.png` (+ `-full.png`): Founder visible
   without scroll, 11 desks, pod zones, 0 stale lines, summary strip.
2. **1920×1080** — `p3-1920-clean.png`: same + Review lane visible.
3. **Working state (real)** — `p3-working.png`: Options Strategist **WORKING**
   badge + green glow + typing dots; summary Active Agents 1 / Running 1.
   Real bounded worker run (`[VERIFY] Live Office Working-state display
   check`, sleep-45 goal, run id 86, ~128s real execution) — [TEST] tasks are
   diagnostics by frozen H2/S3 design and can never drive desk state, so the
   Working example uses one genuine verification run; archived after.
4. **Awaiting Founder** — visible in every capture: 2 GATEs (ORG-2026-0004 +
   ORG-2026-0012) + `▲ FOUNDER` chips over IC Secretary and Macro Strategist.
5. **ACTIVE handoff animation** — `p3-active-handoff-3.png`: bright blue
   glowing CoS→Quant line + packet dot mid-flight. Pulse verified in-DOM
   t+1.0s→3.5s (`packet=1 active_line=1`), driven by a real `created` event
   (bounded [TEST] parent/child pair).
6. **Zero-active quiet office** — `p3-1440-clean.png`: 0 line elements, floor
   clean; Handoff history (15) toggle preserves the historical record.
7. **Read-only detail drawer** — `p3-drawer-cos.png` (+ `p3-working-drawer.png`
   during a live run): role/profile/state/task/open/worker/activity/DIAG/
   edges/events; close button; backdrop click closes.
8. **Browser/console QA** — Playwright headless chromium, 0 console errors on
   the final build; 404s/500 observed during dashboard restarts were transient
   (re-verified clean twice).
9. **Regression suite** — `pytest` **229/229 passed** (unchanged from 2.1;
   no logic/semantics modified).

## Frozen invariants (unchanged, re-verified)

Native Kanban authoritative · Office read-only projection · zero write routes ·
no Office DB · no persistent presentation state · Operational vs Diagnostics ·
ACTIVE/RECENT/HISTORICAL semantics · Error precedence · HERMES_HOME profile
resolution · Stage 7 = PASS WITH CONDITIONS · Stage 8 = HOLD. Luna NOT invoked.

## Notes / deviations

- Working-state demo required ONE real (non-[TEST]) verification task because
  [TEST] tasks are diagnostics by design — documented in source map §S3. It
  was archived after capture; board returned to baseline (39 links, 0 running,
  all probe tasks archived as audit trail per Founder's earlier ruling).
- REVIEW/CONTROL + EXTERNAL SENSING sit below the 900px fold (scroll) —
  accepted per "Founder area visible without scrolling … where practical".
- Packet travels +x (horizontal) along the line start — fine for the dominant
  left→right edges; per-edge directional travel deferred to Phase 3 polish+
  (no logic change).

<!-- 2026-08-13 22:36 UTC+7 (system clock) -->
