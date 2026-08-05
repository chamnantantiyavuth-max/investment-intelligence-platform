# Page Blueprints — Research Workflow UI (UI-1 + UI-2)

**Status:** PROPOSED — FOUNDER REVIEW REQUIRED
**Version:** 0.1 (draft for review — NOT approved, NOT canonical)
**Date:** 2026-08-05
**Author:** IIP profile (Hermes Agent)
**Base:** `design/research-workflow-ui/FIT-GAP-v0.1.md` (D1 approved, FD #55 — data layer LIVE) + design system `MASTER.md` v3.0 (Research Desk direction, FD #51) + `design/UI_TOKENS.md`.
**Scope:** UI-1 (Briefing) + UI-2 (/research + artifact detail) — presentation-layer only. Data comes from the 4 D1 endpoints (`/org-queue`, `/org-holds`, `/research-artifacts`, `/research-artifacts/{id}`). NO new backend work, NO write routes, NO CS Product Detail (UI-3, gated by D2), NO Decision/Model/Audit registers (UI-4 deferred).
**Naming (D4, folded into this review):** Dashboard label → **Briefing**; new nav item **Research Desk** (label collides with the FD #51 visual-direction name in docs — documented here as direction-name vs nav-destination; alternative labels: Research / Work Queue — Founder may veto).
**Authority anchors:** Constitution §1 (search-space reduction, evidence preservation), §8 (provenance), §10 (no composite scores), §21 (Founder-only decisions), §23.4 (epistemic status); EVIDENCE-MODEL §2 (record taxonomy), §9 (data confidence); KANBAN-CONTRACT §1 (operational state ≠ domain state), §2 (columns), §3 (card fields); FD #54 (Holds org-workflow scope only), FD #55 (UI-0).

---

## Page 1 — Briefing (`/` — Dashboard renamed)

### Primary user and decision
Founder, on session start. Primary question: *"What changed, what needs my decision, and what is held?"* Primary decision: which item to open next. NOT the purpose of this page: per-agent activity, token/effort stats, chat transcripts, deep research reading (that is the artifact detail page).

### Bible-to-UI IDs
Existing map (BIBLE_TO_UI_MAP.md, FD #51): dashboard attention-triage rows; new regions trace to Constitution §21 (Founder-only decisions → Decisions Required), §8/§23.4 (provenance → all new panels), KANBAN-CONTRACT §1 (operational ≠ domain state → throughput/holds labels). No new domain semantics introduced — every number derives from admitted org-workflow or pipeline data.

### Reading order
```
Masthead (shared: brand serif · 7-item nav · advisory · portfolio-blind stamp)
Staleness banner (existing, AM/FO/II bounds FD #47 D3)
1  HeroInsight (existing — lead AM insight, unchanged)
2  DECISIONS REQUIRED        [NEW — DecisionRequiredLedger]
3  MATERIAL CHANGES          [NEW — MaterialChangePanel]
4  Findings ledger (existing 4 FindingCards, unchanged)
5  HOLDS & EXCEPTIONS        [NEW — HoldBanner list]
6  RESEARCH THROUGHPUT       [NEW — ledger]
7  Engine provenance (existing, unchanged)
8  Theme lifecycle breadth (existing, unchanged)
ExplainPanel (existing)
AdvisoryFooter (shared, rendered once by Layout)
```

### Text wireframe
```
DECISIONS REQUIRED                         [kicker, small-caps, accent]
(1 item · org_workflow_kanban · as-of 2026-08-05)
  ORG-2026-0004  Founder decision pack — pilot          [mono id · serif subject]
  Decide: approve packet completeness for Founder review (simulated)   [plain-language requested decision]
  Ready · no active holds · 0 dissent · as-of 2026-08-05                [readiness + meta line]
  → open /research/ciw-pilot-msft/…                                     [single action link]
  [empty state: "No items require your decision — new decisions appear here
   when the IC Secretary moves a complete packet into Founder Review."]

MATERIAL CHANGES SINCE LAST REVIEW        [kicker]
  ciw-pilot-msft/research-result-2.md  v2 published (2026-08-03)
  → supersedes nothing; supplements v1 (append-first, FD-CIW-016)      [delta line, no invented diff]
  [empty state: "No versioned artifact changes since your last review."]

HOLDS & EXCEPTIONS                        [kicker]
  No active holds · 2 cleared (HOLD-DATA-001, HOLD-RISK-001)            [honest; cleared collapsed]
  [active hold = full HoldBanner, never a badge]

RESEARCH THROUGHPUT                       [ledger — counts, never rankings]
  New Requests 0 · Active Research 3 · Awaiting Evidence 0 ·
  Awaiting Validation 1 · Founder Review 1 · Held 0 · Published 2
  [derived from kanban columns + artifact statuses]
```

### Primary and secondary actions
Primary: open a decision item → artifact detail. Secondary: filter holds by type; expand cleared holds; refresh. No write actions (decisions happen in repo/vault per FD #54).

### Interaction model
- Decision rows are links (keyboard-focusable); readiness shown as text states, not traffic lights only (color never sole carrier).
- Material changes: one delta line per versioned artifact pair; no speculative diff rendering.
- Throughput: static ledger text — no charts (counts are small and operational).
- No new modals; no hover-only information (critical states inline).

### Required states
Loading (skeleton rows) · API error (scoped: what failed + what's affected + retry — existing pattern) · empty (per section, with reason + next action) · stale (existing banner) · held (HoldBanner) · mobile.

### Responsive transformation
Single column; masthead wraps; run-stamp hidden below md (existing); ledger rows stack (label above value); decisions list full-width.

### Accessibility requirements
Contrast ink-3 ≥4.5:1 (existing token); focus-visible on all links; color+text for readiness; aria-labels on icon buttons (existing sweep pattern); no autoplay/refresh.

### Visual acceptance criteria
Borderless 0–2 full-perimeter outlines (all new sections = open regions + hairline separators only); paper canvas; serif subjects; mono ids/stamps; provenance chips on every data section; no KPI card grid added.

### Surface and containment plan
- Open regions: all 4 new sections (hairline-ledger rows).
- Background zones: tonal `bg-bg-panel` only for hold/error panels.
- Necessary separators: hairline `border-rule` under section headers + ledger rows.
- Full-perimeter bordered surfaces: 0.
- Functional justification: n/a.
- Card containment justification: none — decisions/materials/holds/throughput are lists, not independent action objects.

---

## Page 2 — Research Desk (`/research` — NEW nav item)

### Primary user and decision
Founder + org principals. Primary question: *"What is being worked on, what awaits review, what needs my decision, and what is blocked?"* Primary decision: which item to open / which queue needs attention. NOT the purpose: agent productivity, per-role pages, chat, tokens (rejected by fit-gap — no data, no decision value).

### Bible-to-UI IDs
KANBAN-CONTRACT §2 (columns → views), §3 (card fields → row), §4 (labels), §5 (WIP limits → counts), §6 (movement rights → who may act), §7 (blocked standard), §10 (repo mechanics → provenance stamp); Constitution §21 (Founder Review = decision gate only).

### Reading order
```
Masthead (Research Desk active)
Page header: kicker "Research Workflow" · serif title "Research Desk"
             · mono stamp: org_workflow_kanban · operational · as-of <date>
View selector (segmented): Inbox · Active Research · Review Queue ·
                            Founder Review · Archive        [counts per view]
Toolbar: domain filter · priority filter · Held/Blocked filter · sort
Ledger: ResearchArtifactRow × N (hairline rows, sticky first column)
  [any row with an ACTIVE hold renders HoldBanner inline above its row]
Footer note: "Operational tracking — card state never equals domain state (KANBAN-CONTRACT §1)."
```

### View ↔ column mapping (single source — kanban, no parallel state machine)
| View | Columns (KANBAN-CONTRACT §2) | Default sort |
|---|---|---|
| Inbox | Inbox, Triage | created_at desc |
| Active Research | Scoped, Data Ready, In Research | materiality, last_updated |
| Review Queue | Cross-Review, Validation | materiality, last_updated |
| Founder Review | Founder Review, Blocked | materiality, last_updated |
| Archive | Monitoring, Closed | last_updated desc |

Held/Blocked filter overlays any view (cards with active holds or `blocked_reason` set).

### Text wireframe (row = ResearchArtifactRow)
```
ORG-2026-0004 · Founder decision pack assembly — pilot        [mono id · serif title]
Founder review of the pilot packet (D5 gate)                  [research_question, ink-2]
GOVERNANCE · M2 · IC Secretary (simulated)                    [domain chip · materiality · primary owner]
Founder Review · Draft · DATA READY WITH LIMITATIONS · PENDING · REVIEWED WITH OPEN RISKS
                                                              [workflow col · artifact state · data/validation/risk]
changed 2026-08-05 · next: Founder review (simulated)         [last change · next action]
→ /research/…                                                 [row action]
```

### Primary and secondary actions
Primary: open row → artifact detail (when `expected_artifact`/registry match exists; rows without artifacts show "no artifact yet" and no dead link). Secondary: filter/sort; expand hold banner. No writes (git is single writer).

### Interaction model
- View selector = one ledger re-filtered, NOT tabs-as-process (reading mode, per IA rule).
- Counts per view derived from card `workflow_column` (never domain state).
- Active hold → full banner (issued by / reason / clearance / age), not a badge (fit-gap component verdict).
- Empty states per view, honest: e.g. Inbox empty → "No new research requests — intake happens via template 01 / CRR contract."

### Required states
Loading · error (scoped) · empty per view · all-held view · blocked rows (blocked_reason + owner of resolution, KANBAN-CONTRACT §7) · mobile.

### Responsive transformation
View selector scrolls horizontally (compact); ledger collapses to stacked rows with labels; sticky first column removed below md.

### Accessibility requirements
Segmented control = real buttons/radiogroup with aria-pressed; focus order row→action; color+text for statuses; hold banner = semantic region (role="status" where appropriate).

### Visual acceptance criteria
Borderless 0–2; hairline-ledger rows; no KPI cards; no progress bars (ReviewGatePanel statuses are text rows, never linear); provenance stamp visible; counts never presented as rankings.

### Surface and containment plan
- Open regions: ledger + toolbar + view selector.
- Background zones: tonal panel only for hold banner + blocked rows.
- Necessary separators: hairline rows + header rules.
- Full-perimeter bordered surfaces: 0 (hold banner = tonal, no outline).
- Functional justification: n/a.
- Card containment justification: none — the ledger is a list surface.

---

## Page 3 — Research Artifact Detail (`/research/*` — drill-down, not in nav)

### Primary user and decision
Founder (review) + principals (work). Primary question: *"What does this research actually say, what evidence supports it, what challenges it, and how did it get here?"* Primary decision: approve / return / watch / reject (decision happens in repo — page is read-only display).

### Bible-to-UI IDs
CIW result contract (identity/state), EVIDENCE-MODEL §2/§5/§9 (evidence vs epistemic records, provenance, confidence), §7 (contradicting evidence), Constitution §21 (decision history), PUBLICATION-STANDARD versioning (append-first; v1 intact when v2 published).

### Reading order
```
Masthead (Research Desk active)
Back link → /research
Header: artifact_type chip · serif title · identity stamps (research_id ·
        research_version · research_status · modified) · provenance chip
        (research_artifact_registry · REAL for CIW results)
Section selector (reading modes, not process steps):
  Executive Summary · Research · Evidence · Independent Challenge ·
  Validation · Data Quality · Decision History
  [Audit Trail = deferred to UI-4 — needs git-history endpoint, not in D1 scope]
Body per section (below)
Related artifact family list (drafts · source maps · challenge reviews ·
        founder records for the same research_id/prefix)
Footer note (artifact path + modified; git is the audit trail)
```

### Section contents (data-verified)
| Section | Content | Data today |
|---|---|---|
| Executive Summary | identity table (research_id/version/status/confidence when present) + lead paragraph | REAL (CIW results) |
| Research | rendered markdown body of the artifact | REAL |
| Evidence | evidence refs extracted from the artifact's own citations (SRC-\d+) + linked source-map artifacts; note: full evidence register = template 02 as produced (future) | REAL (MSFT source maps) |
| Independent Challenge | challenge-review artifacts for the same research_id/prefix (rounds), expandable | REAL (MSFT rounds 1–5 + slice-2 rounds 1–4) |
| Validation | from card validation_status/data_status when linkable + honest empty ("no quant validation report published yet — template 07 defines the form") | scaffold |
| Data Quality | from card data_status + source-map coverage rows + honest empty | partial |
| Decision History | version/status transitions documented in founder-review-record artifacts + card fields (created/last_updated/column) | REAL (records) |

Honest-empty rule (DNA-016): every empty section states why it is empty + what produces it — never "no data" without a path.

### Primary and secondary actions
Primary: read + decide (decision actions happen outside the UI per FD #54 — page displays the DecisionPacket options as information when a packet artifact exists: Reject / Return for Research / Watch / Approve for Official Tracking / Approve Research Publication / Defer — labels only, no buttons that write). Secondary: switch sections; open related artifacts; copy artifact path (no clipboard secrets — plain text).

### Interaction model
- Section selector = reading mode (same doctrine as Theme Card tabs).
- Evidence refs render as mono citations; linking out to external sources NOT in scope (no new web layer).
- Related family matched by research_id / filename prefix convention (challenge-review vs challenge-review-2) — documented join, honest limitation.

### Required states
Loading · error · 404 (unknown artifact, with registry link) · artifact without identity table (identity rows hidden, not zeroed) · empty sections (honest) · mobile.

### Responsive transformation
Single column; identity table stacks; section selector scrolls horizontally.

### Accessibility requirements
Landmark regions per section; focus-visible back link + selector; color+text statuses; long markdown body scrolls natively.

### Visual acceptance criteria
Borderless 0–2; serif headlines; mono identity stamps; provenance chip mandatory; no invented composite score; no fake progress.

### Surface and containment plan
- Open regions: all sections (hairline-ledger identity table, open markdown flow).
- Background zones: tonal panel for validation/data-quality empty states.
- Necessary separators: hairline header rules + identity table rows.
- Full-perimeter bordered surfaces: 0.
- Functional justification: n/a.
- Card containment justification: none.

---

## Cross-page rules
1. All three pages consume ONLY the D1 endpoints — no new backend work in UI-1/UI-2.
2. Every data section carries provenance (org_workflow_kanban / org_workflow_holds / research_artifact_registry + as-of) — design-system mandate.
3. No composite scores, no progress bars, no KPI card grids, no per-agent views, no chain-of-thought (fit-gap rejections).
4. Browser-first verification: desktop 1440 + mobile 390 screenshots to `evidence/ui/research-workflow/<task-id>/` + VISUAL_QA.md + ≥1 refinement pass (v4.0.0 Phase L/M).
5. Border budget: 0 full-perimeter outlines on all three pages (tonal panels + hairlines only).
6. Build order within UI-1/UI-2: shared components first (DecisionRequiredLedger, ResearchArtifactRow, MaterialChangePanel, HoldBanner, ReviewGatePanel, AgentContributionLineage, DecisionTimeline) → Briefing → /research → artifact detail → browser refinement → visual council (llm-council, Sol Medium) → Founder acceptance.

## Decisions requested (this review)
- **D4 (folded):** approve labels **Briefing** + **Research Desk** (or name alternatives).
- Approve these 3 blueprints as the build target for UI-1 + UI-2.
- Confirm UI-2 tab scope: 7 sections (Audit Trail deferred to UI-4, needs git-history endpoint).

---

*Page Blueprints UI-1/UI-2 v0.1 — 2026-08-05. Read-only design pass; no code changed.*
<!-- 2026-08-05 16:10 UTC+7 -->
