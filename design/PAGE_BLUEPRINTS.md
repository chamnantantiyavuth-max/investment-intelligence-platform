# Page Blueprints — Investment Intelligence Platform

> **Phase G — ui-dashboard-workflow v4.0.0 · 2026-08-04 · FD #51 (A — Research Desk)**
> One dominant focal region per page. Regions in reading order. Bible-to-UI IDs reference `design/BIBLE_TO_UI_MAP.md`.

## Shared shell (all pages)

- Masthead: brand + primary nav (6 items) + as-of/run stamp (mono, right).
- Content tier: lead (claim) → findings/ledger (evidence) → deep-dive reference tier (methodology/evidence) → footer.
- Footer: AdvisoryFooter (no buy/sell/allocate · portfolio-blind · Constitution §23.8.1) + provenance legend.
- Border budget: 0–2 full-perimeter outlines per viewport (masthead rules + table separators excluded; functional exceptions documented).

---

## LOGIN
- **Purpose/decision:** authenticate single user (FD #46).
- **Regions:** (1) masthead brand; (2) centered sign-in form (user + password + submit) — one independent action = allowed outline; (3) advisory line.
- **States:** idle, submitting, invalid credentials, server unavailable.
- **Copy:** user-facing security/context language (audit M6 — no internal "FD #47" jargon in form subtitle).
- **Bible links:** §23.8.1, F-4.

## DASHBOARD
- **Purpose/decision:** attention triage — what needs attention NOW (overview rule: state/boundaries/change/next).
- **Regions:** (1) lead story: HeroInsight — "most interesting setup" + provenance line + claim-level evidence link (C4); (2) Findings ledger (M1/M2 rows: actionable setups, thesis health, leadership concentration) — ledger table with evidence tags; (3) CS Radar summary — SYNTHETIC DEMO banner prominent (T-025); (4) data provenance strip (real/hybrid/synthetic per module); (5) AdvisoryFooter.
- **States:** loading, error (AM fail → scoped degraded, never zero — C5), empty (honest — DNA-016), populated, stale (staleness banner).
- **Responsive:** hero → stacked; ledger → stacked rows.
- **Bible links:** DNA-002/004/006/016, §13/15/23.4/23.7, M1–M3.

## AM QUEUE
- **Purpose/decision:** ordered theme-first queue — what to investigate next (AM §5.2).
- **Regions:** (1) page header (title + coverage 9/9 + run stamp); (2) queue ledger: theme, lifecycle, conviction, gate status, RS, provenance (4 quality dims separate — T-004); (3) row → Theme Card drill; (4) methodology footnote.
- **States:** loading, error, empty (honest zero-result — existing pattern retained), populated.
- **Bible links:** AM §5.2/5.3, §13, DNA-004.

## THEME CARD
- **Purpose/decision:** does this thesis hold? (judgment surface).
- **Regions (tabs = reading modes):** (1) header: theme id, lifecycle, conviction, provenance (HYBRID correct — C3), entity→theme roles (T-001); (2) DIMENSIONS tab: 4 quality dims separate; (3) EVIDENCE tab: evidence register (type/content/source, per-theme scoped — C2); (4) FALSIFICATION (§11) tab: alternative_explanations + evidence register + unresolved_counter_evidence — per-theme scoped, honest empty states (M1: rename to scoped "Falsification" not full §11 until complete); (5) override/dissent display (A-01 honest state); (6) methodology tier.
- **States:** loading, error, empty, populated; candidate rows as ledger rows — NOT Card rings (C6 fix).
- **Bible links:** DNA-008/009/010, §5/11/12, FD #50.

## AM SCREENER
- **Purpose/decision:** which candidates pass approved criteria (FD #49 objective).
- **Regions:** (1) header + criteria scope (spec §4.1–4.3 cited); (2) matrix ledger: candidates × 18 qualitative criteria (7+6+5 — never summed, T-004); (3) story tone applied to text color (M8 fix: tone → class mapping); (4) filters (local).
- **States:** loading, error, empty (zero-result message), populated.
- **Border fix (C6):** matrix as open sections + row separators — no stage boxes, no Card rings (budget 0–2).
- **Bible links:** AM §4, §13, F-2 (no invented criteria).

## CS RADAR
- **Purpose/decision:** what product to watch (CS §2–5).
- **Regions:** (1) prominent SYNTHETIC DEMO banner (T-025); (2) hero: "most interesting product to watch" (commodity/ETF per P2/P3); (3) P1–P3 eligibility badges; (4) 5-layer synthesis (macro/policy/cost/supply-demand/hidden); (5) conviction (Low/Moderate/High/Maximum — qualitative); (6) key risks; (7) advisory footer.
- **States:** loading, error, empty, populated.
- **Bible links:** CS §2/4/5, T-020..026.

## FO QUEUE / COMPANY / CHEAP & QUALITY
- **Purpose/decision:** which companies deserve research; is the moat/trap story sound (FO §3).
- **Regions:** (1) header + real-data provenance (REAL yfinance — FD #46); (2) queue ledger (8 pkgs); (3) COMPANY: moat classification (6 types + width/depth/trend — approved only), earnings quality, valuation context; (4) CHEAP & QUALITY: verdict rows (cheap-quality vs trap) — **approved classifications only; unapproved derived scores hidden (C-02/F-2 quarantine until A-02)**; (5) methodology tier (Valuation Priorities §3.6.1).
- **States:** loading, error, empty, populated; stale banner (FO ≤30d).
- **Bible links:** FO §2/3, T-030..035, F-2.

## INSTITUTIONAL
- **Purpose/decision:** what are large holders doing (FD #42).
- **Regions:** (1) header + REAL · sec_edgar_13f badge + as-of; (2) stats line (not card grid); (3) 13F signal table: conviction/action badges (FD #42 boundaries only — NEW/EXIT, >10% ADD/REDUCE), concentration ratio; (4) server-side pagination (limit/offset); (5) stale bound 120d.
- **States:** loading, error, empty, populated.
- **Bible links:** FD #42, T-063/064, F-2.

## WEAK SIGNALS
- **Purpose/decision:** what is unexplained — promote or park (FD #27).
- **Regions:** (1) EXPERIMENTAL label (≠ official — never alters official filters); (2) unexplained anomalies list; (3) theme hypotheses list; (4) promotion affordance (honest: no official-state change).
- **States:** loading, error, empty, populated.
- **Bible links:** §7, DNA-012, T-044.

## NOT FOUND
- Honest 404 + nav return. (Trivial page; no blueprint depth needed.)

## States matrix (all material pages)

| State | Requirement |
|---|---|
| Loading | skeleton/loading line, no layout jump |
| Empty | why empty + normal? + next action (DNA-016) |
| Error | what failed + what's affected + retry (C5/23.7) — never zero-coercion |
| Stale/partial | staleness banner + bound (AM 7d/FO 30d/II 120d) |
| Populated | ledger/tables per blueprint |
| Mobile | single column, stacked rows, nav compact |

## Border budget (blueprint-level)

Default 0–2 full-perimeter outlines per viewport. Approved exceptions: login form (1 independent action), functional evidence boundaries on Falsification tab if scanning requires (documented in Visual QA), semantic error/staleness/synthetic banners (excluded by policy). Screener/Theme candidates: open sections + row separators (C6).
<!-- 2026-08-04 17:30 UTC+7 -->
