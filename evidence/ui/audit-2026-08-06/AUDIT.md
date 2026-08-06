# Full Real-User Audit — Investment Intelligence Platform (6 Aug 2026)

**Trigger:** FD #60 (Founder review — 7 requirements). **Auditor:** Hermes (Parent), walking the app as a real user.
**Method:** logged-in browser walk of all routes at localhost:5173, accessibility-tree + screenshot review per page,
data-layer inspection of pipeline artifacts behind the complaints (verify UI-vs-data root cause).
**Verdict: NOT fit for the intended audience as presented.** The data layer contains real substance in places
(CIW research, 13F signals, FO financials), but the UI buries it under internal governance jargon, thin summaries,
raw markdown, and placeholder/dead states. Every one of the Founder's 7 requirements is confirmed with evidence.

---

## 1. Pages walked

| Route | Evidence | Key issues |
|---|---|---|
| / (login) | snapshot | "§23.8.1" governance symbol on the login page |
| / (Briefing) | 01-briefing.png | Jargon wall: "FD #46/57", "Constitution §14", "ORG_WORKFLOW_KANBAN", "RESEARCH_ARTIFACT_REGISTRY", run IDs; empty FINDING 01 paragraph; provenance stamp uppercase walls |
| /research | snapshot | "KANBAN-CONTRACT §1" label; provenance stamps |
| /research/ciw-pilot-msft/research-result.md | snapshot | **Raw markdown as content**: research_version shows "**proposed v1** (this document; assembled from `research-draft.md` v0.5...)"; "LIFECYCLE §2/§5"; [SRC-001] citation codes as raw text |
| /kanban | accepted earlier | "KANBAN-CONTRACT §1/§6/§10" labels in header (governance jargon) |
| /cs-radar/CS-005 (SLV) | 02-slv-macro-context.png | Header "SYNTHETIC · CLOSE_SYSTEM PIPELINE V0.1"; Macro Context tab = **exactly 2 lines** ("Gold rallying (L1 bullish), silver lags...", "Solar subsidies (IRA, EU, India) → silver demand structural") + "L1 bullish" jargon — verified verbatim vs Founder complaint |
| /fundamental | snapshot | All 8 companies show moat "None Shallow", conviction "Moderate", earnings "MEDIUM" — homogeneous output = zero signal; no company story anywhere |
| /fundamental/AAPL | 03-aapl-moat-tab.png | Moat tab displays "No moat narrative" + **"moat_score removed from the system (FD #53...)" and "spec §3.4.1" as user-facing content**; thesis_summary (data): "Apple Inc. lacks a structural moat" — flatly wrong as an investment statement |
| /cheap-quality | snapshot | **Completely blank page** — no empty state, no explanation |
| /weak-signals | snapshot | "SYNTHETIC / DEMO — NOT LIVE DATA" + "E1–E4" jargon; disabled "Propose Hypothesis"/"Dismiss" buttons = dead UI |
| /institutional | snapshot | Real 13F substance (21 funds, 25,246 signals) but raw CUSIPs instead of tickers, unexplained "BASELINE" action, anomalous values ("$57.8T"), "REAL · sec_edgar_13f · partial_21_51" label |
| /am-queue, /am-screener | (same pattern established; not fully walked) | AM pages carry run-ID + provenance labels; verify in remediation pass |

## 2. Findings mapped to FD #60 requirements

**R1 — Layout hard to read (CONFIRMED, app-wide):** no consistent information hierarchy for a decision-maker;
mixed font/weight systems (serif headlines + mono stamps + uppercase kickers); empty or dead regions (FINDING 01
empty, Cheap & Quality blank, disabled buttons); provenance walls competing with content; no page answers "what
should I look at first". Verdict: reads as an internal dev/audit tool, not a research desk.

**R2 — Macro context too thin (CONFIRMED, data + UI):** SLV Macro Context = 2 sentences. Data-layer cause: CS
pipeline artifact layer notes are 1-line each (synthetic pilot, `close_system/output/pipeline_result.json`
L1_macro/L2_policy/L3_cost notes). UI cause: renders them verbatim as bullet pairs with signal labels. Founder's
question "should I rely on your report?" — honest answer: **no, not on this basis**; the page must either be
enriched (industry-outlook reference layer, FD #58 silver handbook exists) or state its depth limit honestly.

**R3 — Bible § / FD # references in UI (CONFIRMED, widespread):** login "§23.8.1"; Briefing "FD #46/57",
"Constitution §14"; AAPL Moat tab "FD #53", "spec §3.4.1"; artifact detail "LIFECYCLE §2/§5"; Research Desk +
Kanban "KANBAN-CONTRACT §1/§6/§10". All must move out of user-facing content.

**R4 — IDs/Bible numbers as background data (CONFIRMED):** run IDs (AM-V0-20260803-171535), registry names
(RESEARCH_ARTIFACT_REGISTRY), CRR ids, CUSIPs, "partial_21_51" all foreground. They belong in the data layer
(API + tooltips/footnotes), never as page furniture.

**R5 — Fundamental: no story/moat/valuation (CONFIRMED, data layer):** moat classifier returns empty types for
ALL 8 companies (types=[], width None, depth Shallow — homogeneous = broken signal, not analysis); valuation
scenarios are zeros; profit-rate-trend "Insufficient ROIC data". But the package DOES contain unused substance:
financial_quality (margins/ROE/FCF), capital_allocation (GOOD/buybacks), macro_context, industry position,
earnings_trajectory, key_risks — none of it presented as a narrative. The generated thesis ("Apple lacks a
structural moat") is algorithmically wrong as an investment statement and must not be surfaced as fact.

**R6 — Research brief as raw markdown (CONFIRMED):** artifact detail renders markdown source (bold markers,
backticks, [SRC-xxx] codes, lifecycle refs) as content. The CIW research-result contains genuinely strong data
(FY26 revenue $331.8B, Cloud $214.4B, RPO $678B, segment table) — it needs a designed research-note presentation.

**R7 — Hedge-fund presentation standard (CONFIRMED FAIL):** current state = audit-trail tool aesthetic. Target:
a Bridgewater/Two Sigma-style research desk — dense, narrative-led, every claim with evidence depth, zero internal
jargon, calm typography, honest depth states.

## 3. Root-cause classification

| Layer | Issues |
|---|---|
| UI presentation (fixable in frontend) | R1 layout, R3 jargon removal, R4 metadata→background, R6 markdown rendering, R7 standard, provenance wall de-emphasis, blank Cheap&Quality, dead buttons |
| Data content (needs spec-based pipeline work + named FDs) | R2 CS macro depth (enrich or honest-limit), R5 FO moat classifier (empty for all), FO valuation scenarios (zeros), FO narrative layer |

## 4. Remediation plan (proposed — Founder gate)

- **Phase 1 — UI language + metadata hygiene (frontend only, non-material):** strip all §/FD#/CONTRACT/registry
  jargon from user-facing text; provenance → discreet "data: real · as-of" chips; IDs/run-refs → tooltip/background;
  honest empty states everywhere; remove dead buttons. Browser re-audit.
- **Phase 2 — Institutional presentation pass (frontend, non-material→material):** per-page redesign to the
  Ray-Dalio standard: one decision per page, narrative-led hierarchy, dense data-first layout, typography pass.
  Screenshots per page + visual council (material).
- **Phase 3 — Research note rendering (frontend):** CIW artifacts render as designed research notes (thesis,
  evidence, tables, citations as footnotes), never raw markdown.
- **Phase 4 — Content depth (material, pipeline + named FDs):** CS macro enrichment from the industry-outlook
  reference layer (FD #58 silver handbook — with point-in-time caveats) or honest depth-limit states; FO moat
  classifier diagnosis + valuation analysis + narrative layer (spec-based, no invented rules).
- **Phase 5 — Verification:** full re-audit walk, screenshots, visual council, Founder acceptance.

## 5. Evidence

- Screenshots: `evidence/ui/audit-2026-08-06/01-briefing.png`, `02-slv-macro-context.png`, `03-aapl-moat-tab.png`
- Data inspection: `close_system/output/pipeline_result.json` (SLV layers), `fundamental-opportunity-v0/output/pipeline_result.json` (AAPL package)
- FD #60 register: repo item 76 + vault FD-60

<!-- 2026-08-06 13:30 UTC+7 -->
