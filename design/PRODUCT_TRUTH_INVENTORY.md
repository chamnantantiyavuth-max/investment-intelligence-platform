# Product Truth Inventory — Investment Intelligence Platform

> **Phase A — ui-dashboard-workflow v4.0.0 (FOUNDATION, FD #51 direction: A — Research Desk)**
> **Date:** 2026-08-04 · **Authority:** approved Bible/specs only — no README/memory/mockup as domain truth
> **Scope:** every material concept the UI must represent, with source, type, criticality, and UI presence.

Types: objective · entity · metric · status · rule · constraint · warning · lifecycle · action · authority · evidence · calculation · history

## 1. Shared Intelligence Core (DOMAIN-ARCHITECTURE.md §1.1, §3–4)

| ID | Source | Concept | Type | Criticality | User relevance | Must appear in UI? |
|---|---|---|---|---|---|---|
| T-001 | DOMAIN-ARCH §1.1 | Shared Core owns canonical Entity–Theme structural roles (DR-006; FD #26) | rule | P0 | Theme-level classification wins over stock-level | Yes — Theme Card shows entity→theme roles |
| T-002 | DOMAIN-ARCH §4.1–4.4 | Information flow: Evidence → Theme → Candidate → Research Queue → Human Review → Learning | lifecycle | P1 | Explains provenance chain per page | Yes — evidence lineage breadcrumb/drill |
| T-003 | DOMAIN-ARCH §5 | Cross-cutting: no AI-invented rules; advisory-only; portfolio-blind | constraint | P0 | Trust boundary communicated to user | Yes — advisory footer everywhere |
| T-004 | CANDIDATE-AND-QUEUE §2.5 | Separation Rule: Theme Quality / Candidate Quality / Entry Readiness / Data Confidence NEVER merged into one composite | rule | P0 | Users see 4 separate dimensions | Yes — 4 distinct dimensions, no composite score |

## 2. Alpha Momentum (ALPHA-MOMENTUM-V0-SPEC.md)

| ID | Source | Concept | Type | Criticality | User relevance | Must appear in UI? |
|---|---|---|---|---|---|---|
| T-010 | AM §1–2 | Momentum-first opportunity discovery; controlled universe (V0_TICKERS 9, coverage 9/9) | objective | P1 | Context for every AM number | Yes — provenance/coverage line |
| T-011 | AM §3 | Controlled themes with approval process + documentation requirements | lifecycle | P0 | Theme Card = primary AM object | Yes — Theme Card page |
| T-012 | AM §4.1–4.2 | 6-stage screening pipeline (S1–S6) with deterministic features | lifecycle | P0 | Stage position explains readiness | Yes — stage indicator on Theme/Candidate |
| T-013 | AM §5.1 | Theme Card: thesis, WHY, evidence lineage, status | entity | P0 | Core reading surface | Yes — Theme Card |
| T-014 | AM §5.2 | Research Queue: ordered, theme-first, adaptive capacity | entity | P1 | Queue page = screening output | Yes — AM Queue page |
| T-015 | AM §5.3 | Evidence Lineage: every claim → evidence records | evidence | P0 | Trust: claims traceable to sources | Yes — Evidence panel + claim links |
| T-016 | AM §5.4 | Historical State preserved (no rewriting history) | history | P0 | Users can see prior states | Yes — history/lineage view (operational gap: AC-8 fixture-only, see T-036) |
| T-017 | AM §5.5 | Human Feedback/Override: record override, preserve original + dissent | action | P0 | Founders may override, dissent preserved | Yes — override display (operational gap: AC-6 fixture-only, see T-036) |
| T-018 | AM §6 | Acceptance criteria AC-1..AC-8 (incl. override AC-6, history AC-8) | constraint | P0 | Governs what "complete" means | Yes — honest status labels (no overclaim) |
| T-019 | AM §7 | V0 Non-Scope: no execution, no allocation, no broker | constraint | P0 | Boundary shown in footer | Yes — advisory footer |

## 3. Close System (CLOSE-SYSTEM-PRODUCT-RADAR.md) — SYNTHETIC DEMO SURFACE (FD #46)

| ID | Source | Concept | Type | Criticality | User relevance | Must appear in UI? |
|---|---|---|---|---|---|---|
| T-020 | CS §2 | Product eligibility P1/P2/P3 (can't-go-zero, discount pricing, structural demand) | rule | P0 | Eligibility = why product is on radar | Yes — P1–P3 badges |
| T-021 | CS §3 | Product taxonomy: commodities/ETFs/structured products radar universe | entity | P1 | Radar scope | Yes — filter/taxonomy |
| T-022 | CS §4 | 5 intelligence layers: macro, policy, cost structure, supply/demand, hidden signals | evidence | P0 | Layer synthesis = insight | Yes — 5-layer synthesis panel |
| T-023 | CS §5.1 | Conviction scale: Low / Moderate / High / Maximum | status | P0 | Decision-relevant | Yes — conviction badge (qualitative only, automation deferred) |
| T-024 | CS §5.2 | Synthesis template (connective reasoning) | evidence | P1 | Explains WHY conviction | Yes — synthesis narrative |
| T-025 | FD #46 | CS = sole labeled synthetic surface; MUST be prominent + honest | warning | P0 | Prevent misreading demo as live | Yes — SYNTHETIC DEMO banner, all CS surfaces |
| T-026 | FD #47 D2 | No synthetic fallback on real endpoints; CS stays synthetic | rule | P0 | Trust boundary | Yes — provenance chip per component |

## 4. Fundamental & Opportunity (FUNDAMENTAL-OPPORTUNITY-INTELLIGENCE.md) — REAL DATA (FD #46)

| ID | Source | Concept | Type | Criticality | User relevance | Must appear in UI? |
|---|---|---|---|---|---|---|
| T-030 | FO §2 | Unified framework: Layers × Domains (5 layers × 6 sub-domains) | objective | P1 | Explains structure of FO surfaces | Yes — methodology tier |
| T-031 | FO §3.4.1 | Moat Classification System (6 types; width/depth/trend) | status | P0 | Moat = primary quality read | Yes — moat classification panel |
| T-032 | FO §3.5.1 | Earnings Quality explicit dimension | status | P0 | Quality signal | Yes — earnings quality panel |
| T-033 | FO §3.6.2 | Value Trap Detector (mandatory) | warning | P0 | Trap detection = decision-critical | Yes — trap verdict + reasons |
| T-034 | FO §3.6.1 | Valuation Priorities (Founder-ordered) | rule | P1 | Explains valuation context | Yes — methodology tier |
| T-035 | Audit C-02 | Unapproved FO derived numbers (moat_score weighted, 30% proxy, trap 4/5→NOT_A_TRAP) — MUST NOT surface until Founder-approved formula FD | constraint | P0 | UI shows approved qualitative classifications only | Yes — hide/omit unapproved scores; show spec classifications |

## 5. Theme, Evidence, Candidate (THEME-MODEL.md, EVIDENCE-MODEL.md, CANDIDATE-AND-QUEUE-MODEL.md)

| ID | Source | Concept | Type | Criticality | User relevance | Must appear in UI? |
|---|---|---|---|---|---|---|
| T-040 | THEME §2 | Theme lifecycle stages + lifecycle properties | lifecycle | P0 | Stage = where thesis stands | Yes — lifecycle badge |
| T-041 | THEME §3 | Approval status + monitoring status (governance) | status | P0 | Official state vs draft | Yes — status badges |
| T-042 | THEME §7 | Theme Card anatomy | entity | P0 | Core surface | Yes — Theme Card |
| T-043 | THEME §8 | Confidence (qualitative) | status | P1 | Readiness context | Yes — confidence label |
| T-044 | THEME §6 | Weak Signal Inbox: unexplained anomalies + theme hypotheses (Experimental) | entity | P1 | Experimental ≠ official | Yes — Weak Signal page, Experimental label |
| T-045 | EVIDENCE §2 | Taxonomy: evidence/observation records vs epistemic/governance records | evidence | P0 | Every claim has a record type | Yes — evidence register (type shown) |
| T-046 | EVIDENCE §5 | Provenance: point-in-time evaluation | evidence | P0 | When a fact was true | Yes — as-of/point-in-time stamp |
| T-047 | EVIDENCE §6 | Aging/staleness: relevance decay, 3-year narrative default, tombstoning | warning | P0 | Stale data honesty | Yes — staleness banner/bound |
| T-048 | EVIDENCE §7 | Contradicting evidence must be scoped per theme/candidate | evidence | P0 | Prevent false associations (audit C2) | Yes — falsification tab, per-theme scoped |
| T-049 | CANDIDATE §1–2 | Candidate identity (entity/issuer/asset) + 4 quality dimensions separate (T-004) | entity | P0 | Candidate rows | Yes — candidate tables/rows |
| T-050 | CANDIDATE §3.3 | Thesis narrative + conviction; lifecycle; entry trigger + watchlist gate | status | P0 | Readiness + why | Yes — thesis panel, gate status |
| T-051 | CANDIDATE §4 | Theme-first research queue (structure, adaptive capacity) | entity | P1 | Queue ordering logic | Yes — queue page |
| T-052 | FD #50 | Falsification read-only panel: alternative_explanations, evidence register, unresolved_counter_evidence | evidence | P0 | Intellectual honesty surface | Yes — Falsification (§11) tab |

## 6. Operating Model + Institutional (INVESTMENT-INTELLIGENCE-OPERATING-MODEL.md, FD #42)

| ID | Source | Concept | Type | Criticality | User relevance | Must appear in UI? |
|---|---|---|---|---|---|---|
| T-060 | OPERATING §5–6 | Dual intelligence paths: Fundamental & Opportunity + Momentum & Market Leadership | objective | P1 | Navigation explains both paths | Yes — nav + per-page path label |
| T-061 | OPERATING §6 | Momentum elements: regime, breadth & leadership, RS, price-volume, breakout readiness | metric | P1 | AM supporting read | Yes — AM theme/queue supporting panels |
| T-062 | OPERATING §7 | Independent Challenge (thesis challenge) | authority | P1 | Shows challenge/verification status | Yes — challenge status line |
| T-063 | FD #42 | Institutional Intelligence: 13F, concentration ratio, conviction signals, super-investor watchlist | entity | P1 | II page content | Yes — Institutional page |
| T-064 | Audit C-02 | II unapproved derived score (0–100 score_signal, ≥20% boundary) — surface only approved FD #42 fields until formula FD | constraint | P0 | Trust: no invented scores | Yes — show action badges per FD #42 only |

## 7. Cross-Cutting Authority & Trust (Constitution, FORBIDDEN_ACTIONS, FD #46–48)

| ID | Source | Concept | Type | Criticality | User relevance | Must appear in UI? |
|---|---|---|---|---|---|---|
| T-070 | CONST §23.4 | Per-page WHAT/WHY/HOW + thesis narrative + evidence provenance + epistemic status | rule | P0 | Every page explains itself | Yes — all pages (hero/lede + methodology + provenance) |
| T-071 | CONST §23.8.1 | Advisory only — NO buy/sell/allocate, no broker connectivity | constraint | P0 | Never conflation advisory/execution | Yes — advisory footer every page |
| T-072 | FORBIDDEN_ACTIONS | No AI-invented thresholds/weights/formulas/lookbacks/fallback | constraint | P0 | UI must not present invented numbers as official | Yes — only approved values shown |
| T-073 | FD #46–48 | Provenance labels per component: real / hybrid / synthetic + human_sourced; AM hybrid must show HYBRID (audit C3) | evidence | P0 | Truthfulness of every number | Yes — ProvenanceChip with REAL/HYBRID/SYNTHETIC states |
| T-074 | FD #46–48 | Real-data path: AM EOD (≤7d), FO yfinance (≤30d), II 13F (≤120d); staleness bounds | warning | P0 | Freshness honesty | Yes — as-of + staleness bound |
| T-075 | FD #51 + audit C1 | Research Desk direction: light, dense, paper; typography-led hierarchy; borderless-by-default (0–2) | rule | P0 | Visual identity | Yes — tokens/MASTER.md v3.0 |
| T-076 | Audit C4 | Narrative claims (hero/findings) require claim-level evidence links — no orphan superlatives | rule | P0 | Trust: every claim traceable | Yes — hero + findings carry evidence refs |
| T-077 | Audit C5 | Failure honesty: request error ≠ empty ≠ zero — scoped degraded states | rule | P0 | No false narrative on API failure | Yes — per-surface error states |
| T-078 | Human Review §2 | Human Override fields/rules — preserve original + dissent | action | P0 | Governance history | Yes — override display; operational workflow pending C-03 decision |

## AMBIGUOUS / OPEN (needs Founder or domain decision — do not invent)

| ID | Item | Why open | Required decision |
|---|---|---|---|
| A-01 | AM Human Override / history: fixture-level only, GET-only API | Audit C-03 — AC-6/AC-8 claimed complete without operational workflow | Founder: fixture demonstration (reclassify) vs authorized operational scope (implement) |
| A-02 | FO/II derived scores (moat_score, trap mapping, II score) | Audit C-02 — code exceeds approved spec; prohibited AI-invented formulas | Founder: approve exact formulas via named FD, or quarantine from surfaces |
| A-03 | FO spec approval metadata (Approved vs TBD) | Audit M-02 — self-contradictory header | Founder: metadata-only amendment |

## Source map (authoritative)

- DOMAIN-ARCHITECTURE.md, ALPHA-MOMENTUM-V0-SPEC.md, CLOSE-SYSTEM-PRODUCT-RADAR.md, FUNDAMENTAL-OPPORTUNITY-INTELLIGENCE.md, THEME-MODEL.md, EVIDENCE-MODEL.md, CANDIDATE-AND-QUEUE-MODEL.md, INVESTMENT-INTELLIGENCE-OPERATING-MODEL.md, HUMAN-REVIEW-AND-LEARNING-MODEL.md (all `project-definition/`, Approved)
- 02-PROJECT-CONSTITUTION.md (§23), FORBIDDEN_ACTIONS.md, operational/FOUNDERS-DECISIONS.md (#40–51, FD-CIW-001..016)
- Audit findings: evidence/FULL-AUDIT-OBJECTIVE-2026-08-04.md, evidence/FULL-AUDIT-UI-2026-08-04.md
<!-- 2026-08-04 16:55 UTC+7 -->
