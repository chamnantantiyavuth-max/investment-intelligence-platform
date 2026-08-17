# Capability-Level Legacy Reuse Map

> ⛔ **SUPERSEDED — HISTORICAL DESIGN PREDECESSOR (16 Aug 2026)**
> Canonical capability truth after M2 = **`QAD-M2-LEGACY-CAPABILITY-REGISTRY.md`** + **`QAD-M2-DEPENDENCY-MATRIX.md`**.
> This map was the **M1‑era design predecessor** that informed QAD-M2 capability inventory.
> It is preserved as lineage and design‑stage reference only — **do not use for M3 planning**.
> For authoritative current state and disposition, refer to the M2 registry.

> **NOT module-name-based.** Every capability is audited for actual QAD relevance before supersede/reuse/archive decision.
> **Key principle:** A capability that was part of a "strategy" may still survive as an evidence input or supporting QAD function.

---

## Methodology

Each existing capability was evaluated against:
1. **QAD function** it could serve (if any)
2. **Domain overlap** — does it produce evidence inputs or analytical outputs that QAD needs?
3. **Code/module dependency** — is it self-contained or entangled in legacy strategy?
4. **Data pipeline** — does it produce independently useful data?

---

## Capability Map

### 1. Shared Equity Universe (FD #95)
| Field | Value |
|-------|-------|
| **Status** | ✅ **REUSE DIRECTLY** |
| **QAD function** | Quality Universe seed — 98 CIK-verified names |
| **Why not freeze** | Deterministic, PIT, no strategy logic |
| **Action** | Keep active. QAD Quality Universe = superset of this |

### 2. Equity Inflection Scanner (FD #88/#89)
| Field | Value |
|-------|-------|
| **Status** | 🔄 **ADAPT — keep as QAD discovery input** |
| **QAD function** | Dislocation Radar input — EPS breakout detection |
| **Why not freeze** | Produces valuable candidate signal for QAD selection |
| **Action** | Keep running. Output feeds QAD Dislocation Radar (M5). Freeze as standalone module (no further feature development) |

### 3. Quality & Asymmetry Discovery (FD #95)
| Field | Value |
|-------|-------|
| **Status** | 🔄 **ADAPT — QAD Quality Discovery foundation** |
| **QAD function** | Quality assessment lenses — Durable Compounder / 100-Bagger / Mispriced Quality / Asymmetric Value |
| **Why not freeze** | Directly maps to QAD Quality Discovery open system |
| **Action** | Keep as shadow/evidence-only. QAD-M5 will extend with QAD-specific quality protocol |

### 4. CS Product Discovery (FD #97)
| Field | Value |
|-------|-------|
| **Status** | ❌ **DO NOT MAP to QAD Dislocation** |
| **QAD function** | NONE — commodity-specific (gold/silver/copper/oil) |
| **Why not reuse** | QAD Dislocation is company-specific impairment diagnosis. CS Product Discovery watches commodity macro cycles — different domain, different methodology, different evidence class |
| **Action** | FREEZE with CS. QAD Dislocation Radar (M5) is a NEW design, not an evolution of CS Product Discovery |

### 5. Alpha Momentum Pipeline
| Field | Value |
|-------|-------|
| **Status** | ⏸️ **FREEZE as-is** |
| **QAD function** | NONE — momentum screening, Stage Analysis, theme ranking |
| **Why not reuse** | QAD is fundamental/moat/impairment analysis, not momentum |
| **Action** | FROZEN — read-only API for historical record. No deactivation (tests depend on it for regression) |

### 6. Alpha Momentum Theme Infrastructure
| Field | Value |
|-------|-------|
| **Status** | ⏸️ **FREEZE as-is** |
| **QAD function** | NONE (theme-first philosophy contra QAD) |
| **Why not reuse** | Theme Intelligence demoted from mandatory gateway to supporting capability |
| **Action** | FROZEN. Some supporting capabilities (below) may survive |

### 7. Theme Intelligence — Weak Signal Inbox / Anomaly Detection
| Field | Value |
|-------|-------|
| **Status** | 🔄 **ADAPT — supporting QAD discovery input** |
| **QAD function** | Potential anomaly signal for Dislocation Radar |
| **Why survive** | Anomaly detection is model-agnostic; could signal dislocation candidates |
| **Action** | Keep frozen as module. If QAD-M5 needs anomaly signals, import methodology (not code) |

### 8. Close System Product Radar
| Field | Value |
|-------|-------|
| **Status** | ⏸️ **FREEZE as-is** |
| **QAD function** | NONE — commodity macro products |
| **Why not reuse** | QAD is company-specific equity analysis |
| **Action** | FROZEN. Synthetic labels preserved. Read-only API for historical record |

### 9. Fundamental & Opportunity Pipeline
| Field | Value |
|-------|-------|
| **Status** | ⏸️ **FREEZE as strategy — but REUSE components** |
| **QAD function** | See sub-capabilities below |
| **Why not full freeze** | Individual analytical methods (moat framework, earnings quality, capital allocation) are QAD-relevant |

#### 9a. Moat Classification (6 types + Width/Depth/Trend)
| Status | ⏸️ Frozen as pipeline — methodology available for QAD |
|--------|----------|
| **QAD action** | QAD-M8 Business Quality protocol will inherit the 6-type moat framework (spec §3.4.1) and extend with Moat Mechanism Protocol (QAD §18) |

#### 9b. Earnings Quality (HIGH/MEDIUM/LOW/COSMETIC)
| Status | ⏸️ Frozen as pipeline — methodology available for QAD |
|--------|----------|
| **QAD action** | QAD-M8 Financial Reconstruction will adopt Earnings Quality framework |

#### 9c. Value Trap Detector (5-question)
| Status | ❌ REPLACE — QAD Impairment Diagnosis supersedes |
|--------|----------|
| **QAD action** | QAD-M8 Impairment Diagnosis (Temporary/Mostly/Mixed/Structural/Unresolved) replaces the 5-question binary |

#### 9d. Marx Signals (Profit Rate Trend + Narrative Gap, FD #43)
| Status | ⏸️ FREEZE — keep as informational |
|--------|----------|
| **QAD action** | Not directly needed for QAD (impairment diagnosis is more granular). If useful, import methodology. |

### 10. Institutional Intelligence (13F Pipeline)
| Field | Value |
|-------|-------|
| **Status** | ⏸️ **FREEZE as strategy — but 13F DATA survives as QAD evidence input** |
| **QAD function** | Evidence input: institutional conviction signals can inform Quality assessment |
| **Why not full freeze** | Raw 13F data (conviction, concentration, super-investor activity) is legitimate evidence for QAD Business Quality analysis |
| **Action** | FROZEN as pipeline/API. 13F data accessible as evidence source. QAD Evidence Lead may consume it |

### 11. CIW (Company Intelligence Workbench)
| Field | Value |
|-------|-------|
| **Status** | 🔄 **ABSORB into QAD Research Protocol** |
| **QAD function** | QAD Full Research Protocol evolves from CIW Research Framework (Modules A–Q) |
| **Why absorb** | CIW Result Contract + Quality Gates are directly reusable. CIW lifecycle transforms into QAD Case Lifecycle |
| **Action** | Keep CIW artifacts as lineage record. QAD-M3 Domain Contracts inherit CIW Research Framework, Result Contract, Quality Gates. **Preserve CIW lineage** — QAD Workbench is an evolution, not a replacement |

### 12. Hermes AI Workforce (10 org-* profiles)
| Field | Value |
|-------|-------|
| **Status** | 🔄 **REFRAIN — QAD logical contracts first, workforce mapping second** |
| **QAD function** | Workforce mapping to be determined after Pack A role contracts exist |
| **Action** | No changes to org-* profiles until QAD logical role contracts pass Founder review + WORKFORCE-MIGRATION-MAP created |

| 13 | **Hermes Radar (Weekly + Mid-Week)** |
| Field | Value |
|-------|-------|
| **Status** | 🔄 **TRANSITIONAL — retain as non-authoritative complementary Discovery Scout (M1 correction, 2026-08-17)** |
| **QAD function** | External-discovery lane (Lane C) — regulatory context, competitor/supplier/customer commentary, unusual filing context, industry developments, source-specific anomalies — signals structured sensors find difficult |
| **Why not freeze** | QAD Discovery (M5) may not yet reproduce Radar's contextual recall; no pre-decided retirement (Part D) |
| **Action** | **Keep running during M1–M4B unchanged (authorized crons intact).** M3 defines Radar/Scout as non-authoritative complementary discovery (Signal/Candidate intake only; never classifies Temporary vs Structural, determines Quality, values, writes thesis, approves selection, allocates budget, or recommends trades). After QAD Discovery is operational (M5/M6), run the evidence-based migration decision: **Legacy Radar vs QAD Discovery incremental recall evaluation** — if Radar discovers material candidates QAD misses, absorb/retain the function; freeze only after comparative evidence shows no material incremental value or full reproduction elsewhere. Workforce profile reframe deferred to the Workforce Migration Map |

### 14. Deep Research Standing Contract (tpl 16)
| Field | Value |
|-------|-------|
| **Status** | ✅ **REUSE DIRECTLY — foundation for QAD Research Protocol** |
| **QAD function** | Research workflow skeleton (mandate → evidence → cross-exam → CRO → audit → synthesis → Founder gate) |
| **Action** | Keep active. QAD-M3 will extend into full QAD Research Protocol |

### 15. Blog / Report Infrastructure (/library, /library/:slug, reports/)
| Field | Value |
|-------|-------|
| **Status** | ✅ **REUSE DIRECTLY — QAD report index** |
| **QAD function** | Passive renderer of published QAD research |
| **Action** | Keep as-is. QAD-M11 will add PDF generation alongside markdown |

### 16. Thai Editorial Standard (FD #94)
| Field | Value |
|-------|-------|
| **Status** | ✅ **REUSE DIRECTLY** |
| **QAD function** | QAD publication quality control |
| **Action** | Keep. QAD-M11 extends with long-form PDF standard |

### 17. CAPITAL INTELLIGENCE LIVE OFFICE (FD #108–110)
| Field | Value |
|-------|-------|
| **Status** | ✅ **REUSE DIRECTLY — QAD monitoring dashboard** |
| **QAD function** | Monitoring dashboard for QAD cases |
| **Action** | Keep as FROZEN production baseline. QAD-M12 will define monitoring data sources |

### 18. Research Audit Infrastructure (evidence/audit trails)
| Field | Value |
|-------|-------|
| **Status** | ✅ **REUSE DIRECTLY** |
| **QAD function** | QAD-M10 Audit inherits this infrastructure |
| **Action** | Keep active |

### 19. Equity/Fundamental Discovery Modules (discovery/*)
| Field | Value |
|-------|-------|
| **Status** | ⏸️ **FREEZE as independent modules** |
| **QAD function** | May feed evidence into QAD Discovery |
| **Action** | Keep frozen. QAD-M5 reads output but does not depend on it |

---

## Summary Matrix

| Decision | Count | Capabilities |
|----------|-------|--------------|
| ✅ REUSE DIRECTLY | 8 | Shared Equity Universe, Deep Research Contract (tpl 16), Blog/Reports, Thai Editorial Standard, Live Office, Audit Infrastructure, Evidence Doctrine, Security/Untrusted-Content |
| 🔄 ADAPT | 5 | Equity Inflection Scanner, Quality & Asymmetry Discovery, Theme Anomaly Detection, FO Moat/Earnings components, 13F data as evidence input |
| 🔄 ABSORB (with lineage) | 1 | CIW → QAD Research Protocol |
| 🔄 TRANSITIONAL (non-authoritative complementary, retained pending evidence-based migration decision) | 1 | Hermes Radar (Weekly + Mid-Week) |
| ⏸️ FREEZE | 7 | AM Pipeline, AM Themes, CS Product Radar, FO Pipeline (as strategy), II Pipeline (as strategy), CS Product Discovery, Discovery modules |
| ❌ NOT FOR QAD REUSE | 1 | CS Product Discovery → QAD Dislocation mapping rejected |
| ⏸️ REFRAIN (deferred) | 1 | Hermes AI Workforce (wait for contracts + migration map) |

<!-- 2026-08-16 UTC+7 -->