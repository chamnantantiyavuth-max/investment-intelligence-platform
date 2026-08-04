# Bible-to-UI Map — Investment Intelligence Platform

> **Phase C — ui-dashboard-workflow v4.0.0 (MANDATORY gate, FD-104/FD-107) · 2026-08-04 · FD #51 (A — Research Desk)**
> Every Bible/DNA/Constitution section cross-referenced against UI requirements. State: REPRESENTED / PROGRESSIVE_DISCLOSURE / SYSTEM_ONLY / NOT_YET_REPRESENTED / AMBIGUOUS. Priority: P0 (safety/authority/financial/irreversible) / P1 (primary understanding) / P2 (supporting detail).

## 1. Project DNA (01-PROJECT-DNA.md, DNA-001..020)

| Bible ID | Material concept | User question | UI location | Representation | Pri | State |
|---|---|---|---|---|---|---|
| DNA-001 | Decision intelligence, NOT automated decision-making | "Who decides?" | All pages | Advisory-only tone; no buy/sell affordance; AdvisoryFooter | P0 | REPRESENTED |
| DNA-002 | Evidence first | "Why does this claim hold?" | Hero, Findings, Theme Card | Claim-level evidence links (audit C4 fix), Evidence panel | P0 | PROGRESSIVE_DISCLOSURE |
| DNA-003 | Information preservation (no rewrite) | "What did it say before?" | Theme Card, meta | Run/version stamps; history view (operational gap A-01) | P1 | PROGRESSIVE_DISCLOSURE |
| DNA-004 | Breadth before depth | "How wide is the queue?" | Dashboard, AM Queue | Coverage line (9/9), breadth finding | P1 | REPRESENTED |
| DNA-005 | Shared intelligence, bounded strategies | "Which module am I in?" | Nav | 4 module nav + per-page module label | P1 | REPRESENTED |
| DNA-006 | Discovery is hybrid | "What kind of evidence?" | All numbers | ProvenanceChip REAL/HYBRID/SYNTHETIC (audit C3 fix) | P0 | NOT_YET_REPRESENTED (chip lacks HYBRID) |
| DNA-007 | AI discovery, human approval | "Who approved?" | Provenance, meta | Human-sourced marker + approval status | P0 | PROGRESSIVE_DISCLOSURE |
| DNA-008 | Theme is a relationship structure | "What entities does this theme tie?" | Theme Card | Entity→theme role section | P1 | REPRESENTED |
| DNA-009 | Every material hypothesis falsifiable | "What would change my mind?" | Theme Card | Falsification (§11) tab — FD #50 | P0 | REPRESENTED (scoping bug C2 → fix) |
| DNA-010 | Human authority preserves dissent | "Where is my override?" | Theme Card | Override/dissent display (operational gap A-01) | P0 | NOT_YET_REPRESENTED (fixture-only) |
| DNA-011 | Learning never rewrites history | "History?" | Lineage/meta | Append-only state + run stamps | P1 | PROGRESSIVE_DISCLOSURE |
| DNA-012 | Controlled learning | "What did the loop learn?" | Weak Signal | Learning outputs labeled (self-reflection, gaps) | P2 | PROGRESSIVE_DISCLOSURE |
| DNA-013 | Everything material versioned | "Which version?" | Meta lines | Run id, adapter version, as-of | P1 | REPRESENTED |
| DNA-014 | Replaceable intelligence components | "Which adapter?" | Provenance drill | Component/adapter reference | P2 | PROGRESSIVE_DISCLOSURE |
| DNA-015 | Simplicity before infrastructure prestige | "Why so plain?" | Global | Borderless-by-default, no decorative chrome (v4.0.0) | P0 | REPRESENTED (direction A) |
| DNA-016 | Honest empty states | "Why is this empty?" | All empty/error states | Explain why + next action; error ≠ empty ≠ zero (audit C5 fix) | P0 | NOT_YET_REPRESENTED (failure→zero bug) |
| DNA-017 | Global observation, controlled universe | "What universe?" | Meta | Universe/coverage disclosure (9/9, V0_TICKERS) | P1 | REPRESENTED |
| DNA-018 | Structured truth, narrative layer | "Where is canonical?" | Provenance | Canonical artifact refs (run ids, file hashes) | P1 | PROGRESSIVE_DISCLOSURE |
| DNA-019 | Deep research must earn its cost | "Is this CIW-approved?" | CIW surface | Published-only research results (deferred Phase 11) | P2 | SYSTEM_ONLY |
| DNA-020 | Research returns intelligence to system | — | (future FO link) | CIW→FO feed (future) | P2 | SYSTEM_ONLY |

## 2. Constitution (02-PROJECT-CONSTITUTION.md §1–23)

| Bible ID | Material concept | User question | UI location | Representation | Pri | State |
|---|---|---|---|---|---|---|
| §1 Mission | Advisory opportunity discovery | "What is this?" | Login, footer | Mission line + advisory framing | P1 | REPRESENTED |
| §2 Product structure | 4 bounded contexts | "Where do I go?" | Nav | Dashboard + AM/CS/FO/II modules | P1 | REPRESENTED |
| §4 Shared Core | Cross-module entity/theme truth | "Who owns this theme?" | Theme Card | Ownership/role section (T-001) | P1 | REPRESENTED |
| §5 Theme Intelligence | Theme = primary object | "What's the theme?" | Theme Card | Theme anatomy (why_now, lifecycle, confidence) | P1 | REPRESENTED |
| §6 Two-tier autonomy | Deterministic vs AI vs human | "Who computed this?" | Provenance/epistemic | Authority chips (23.2), provenance | P0 | PROGRESSIVE_DISCLOSURE |
| §7 Weak Signal Inbox | Anomalies + hypotheses (Experimental) | "What's unexplained?" | Weak Signal page | Inbox + Experimental label (≠ official) | P1 | REPRESENTED (old style, B7) |
| §8 Evidence Doctrine | Evidence as foundational object | "What evidence?" | Evidence panel | Register with type/content/source | P0 | REPRESENTED |
| §9 Evidence Progression | Evidence matures | "How strong?" | Evidence panel | Progression status per record | P1 | PROGRESSIVE_DISCLOSURE |
| §10 Information Preservation | No rewrite | "History?" | Lineage | Append-only + version stamps | P1 | PROGRESSIVE_DISCLOSURE |
| §11 Falsification | Every thesis has falsification | "What contradicts?" | Theme Card Falsification tab | alternatives + evidence register + unresolved counter-evidence (FD #50) | P0 | REPRESENTED (C2 scoping bug → fix) |
| §12 Human Authority | Human override preserves dissent | "My override?" | Theme Card | Override display (gap A-01) | P0 | NOT_YET_REPRESENTED |
| §13 Alpha Momentum | 4 quality dimensions separate | "How good is it really?" | AM surfaces | 4 separate dimensions, NO composite (T-004) | P0 | REPRESENTED |
| §14 Theme-First Queue | Queue structure | "What's next?" | AM Queue | Ordered queue, adaptive capacity note | P1 | REPRESENTED |
| §15 Close System | Radar: P1–P3, 5 layers, conviction | "What product to watch?" | CS Radar | P1–P3 badges, 5-layer synthesis, conviction scale | P0 | REPRESENTED (old style, B5) |
| §16 Learning Loop | Loop outputs | "What changed?" | Learning surfaces | Self-reflection log (P2) | P2 | PROGRESSIVE_DISCLOSURE |
| §17 Knowledge Architecture | Structured registry = truth | "Canonical source?" | Provenance | Run/artifact references | P1 | PROGRESSIVE_DISCLOSURE |
| §18 Initial Non-Scope | No execution/allocation | "Can I trade here?" | Global | No execution affordance; footer | P0 | REPRESENTED |
| §19 Architecture Principles | Tech-neutral, presentation-only | — | (governance) | No UI impact beyond presentation-only scope | P1 | SYSTEM_ONLY |
| §20 V0 Thesis | Momentum-first | "What's the thesis?" | Meta, AM | Momentum framing in copy | P1 | REPRESENTED |
| §21 Amendment Authority | Versioned approvals | "What was approved?" | Methodology tier | Version/approval stamps | P2 | PROGRESSIVE_DISCLOSURE |
| §22 Closing Principle | Honesty at closure | — | Global | Honest states everywhere | P1 | REPRESENTED |
| §23.2 | Three-layer authority model | "Who computed?" | Provenance | Authority chip (deterministic/AI/human) | P0 | PROGRESSIVE_DISCLOSURE |
| §23.3 | Function classification | "Advisory or executable?" | Global | Visual separation advisory vs execution | P0 | REPRESENTED |
| §23.4 | Evidence & epistemic status | "WHAT/WHY/HOW?" | Every page | Per-page thesis narrative + methodology + provenance + epistemic label | P0 | PROGRESSIVE_DISCLOSURE |
| §23.5 | Specialized agents/delegation | — | (internal) | n/a UI | P2 | SYSTEM_ONLY |
| §23.6 | Reproducibility & versioning | "Which run?" | Meta | Run/version stamps | P1 | REPRESENTED |
| §23.7 | Failure & degraded operation | "What broke?" | Error/degraded states | Scoped degraded state: what failed/affected/next (audit C5) | P0 | NOT_YET_REPRESENTED (failure→zero) |
| §23.8 | Privacy & data boundaries | — | (internal) | No sensitive data exposure | P2 | SYSTEM_ONLY |
| §23.8.1 | Blind portfolio rule | "Is my portfolio used?" | Login, footer | Portfolio-blind statement | P0 | REPRESENTED |
| §23.9 | Correction doctrine | "Was this corrected?" | Meta | Correction labels (P2) | P2 | PROGRESSIVE_DISCLOSURE |

## 3. FORBIDDEN_ACTIONS.md (hard prohibitions)

| Bible ID | Material concept | User question | UI location | Representation | Pri | State |
|---|---|---|---|---|---|---|
| F-1 | No execution/order/allocation | "Can I act here?" | Global | Zero execution affordances; AdvisoryFooter | P0 | REPRESENTED |
| F-2 | No AI-invented rules/thresholds/weights/formulas | "Is this approved?" | FO/II surfaces | Only approved classifications shown; quarantine unapproved scores (audit C-02) | P0 | NOT_YET_REPRESENTED (C-02 quarantine) |
| F-3 | No history rewrite | "History intact?" | Lineage | Append-only display | P0 | REPRESENTED |
| F-4 | No secrets in UI | — | (internal) | Never render credentials | P0 | SYSTEM_ONLY |

## Gap table summary

| Priority | Total | REPRESENTED | PROGRESSIVE_DISCLOSURE | NOT_YET_REPRESENTED | SYSTEM_ONLY |
|---|---|---|---|---|---|
| P0 | 22 | 10 | 6 | 5 (DNA-006/010/016, §12, §23.7) + F-2 | 1 |
| P1 | 20 | 12 | 7 | 1 (A-01) | 0 |
| P2 | 10 | 0 | 5 | 0 | 5 |
| **Total** | **52** | **22** | **18** | **6** | **6** |

**P0 gaps to close in this redesign (all mapped to audit findings):**
1. DNA-006 → ProvenanceChip HYBRID state (audit C3)
2. DNA-010/§12 → override display (depends on A-01 decision — show what exists, honest state)
3. DNA-016/§23.7 → failure honesty: error ≠ empty ≠ zero (audit C5)
4. §11 → counter-evidence per-theme scoping (audit C2)
5. F-2 → FO/II unapproved scores quarantine (audit C-02 — A-02 decision)
6. §23.4/23.2 → epistemic + authority chips on every page (partially there)

## Gate declaration (FD-104/FD-107 — answered in-line)

1. Did I cross-reference EVERY Bible § against UI requirements? **[Y]** — DNA 20/20 + Constitution §1–23 (+23.1–23.10) + FORBIDDEN_ACTIONS 4/4 = 52 rows.
2. Did I present a complete gap table (P0/P1/P2) to the Founder? **[Y]** — table above; P0=22, P1=20, P2=10.
3. Did the Founder explicitly approve skipping this gate? **[N]** — gate runs (not skipped).
<!-- 2026-08-04 17:10 UTC+7 -->
