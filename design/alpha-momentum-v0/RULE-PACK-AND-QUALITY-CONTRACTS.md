# Rule Pack and Quality Contracts

Status: Accepted Gate A Decision-Slot Artifact
Version: 0.1
Owner: Founder
Authority: Structurally approved Gate A decision-slot artifact; individual decision-slot content gains authority only through its own named Founder approval
Derived from: Constitution v0.3, Project Definition v0.1, and Approved Stable Design Plan v0.1
Drafting Authorization: AM-V0-GATE-A-DRAFTING-v0.1
Structural Acceptance: AM-V0-GATE-A-STRUCTURAL-ACCEPTANCE-v0.1
Supersedes: v0.1-draft (DS-001–DS-028, RC-001 — see Slot Supersession Map §6)

---

## 1. Inherited Approved Semantics

This section faithfully restates approved semantics that govern Candidate Quality, Theme Quality, Entry Readiness, and Alpha Momentum strategy-owned feature and rule semantics. No expansion or reinterpretation is intended.

### 1.1 Constitution v0.3

- **§10 Information Preservation:** The platform must keep Theme Quality, Candidate Quality, Entry Readiness, and Data Confidence separate. Important trade-offs must not disappear into one opaque score.
- **§13 Alpha Momentum:** Alpha Momentum separates Candidate Quality (fundamentals, growth, liquidity, relative strength, trend quality, accumulation, industry leadership, and other approved rule-pack dimensions), Theme Quality (lifecycle, breadth, leadership, evidence progression, market confirmation, fundamental confirmation, crowding, and confidence), Entry Readiness (price structure, base quality, breakout proximity, volume behavior, volatility contraction, and extension risk), and Data Confidence (freshness, completeness, reliability, conflicts, and missing data).
- **§13 Alpha Momentum — Candidate classification within a Theme:** Confirmed Leader, Emerging Challenger, Direct Beneficiary, Enabler, Bottleneck Owner, Second-order Beneficiary, Watchlist Member, Former Leader, Deteriorating Member.

### 1.2 Candidate and Queue Model (Approved Domain Specification v0.1)

- **§2.1 Candidate Quality:** Measures the quality of the company or asset itself, independent of entry timing. Domains: Fundamentals, Growth, Liquidity, Relative Strength, Trend Quality, Accumulation, Industry Leadership. Owned by Alpha Momentum strategy. Domains are deferred for finalization (OPEN-QUESTIONS.md).
- **§2.2 Theme Quality:** Measures the strength, health, and evidence backing of the Candidate's related Theme(s). Domains: Lifecycle stage, Breadth, Leadership, Evidence progression, Market confirmation, Fundamental confirmation, Crowding, Confidence. Owned by Shared Core (Theme Intelligence). Domains are deferred for finalization.
- **§2.3 Entry Readiness:** Measures whether the Candidate presents a favorable entry opportunity at this moment. Domains: Price structure, Base quality, Breakout proximity, Volume behavior, Volatility contraction, Extension risk. Owned by Alpha Momentum strategy. Domains are deferred for finalization.
- **§2.5 Separation Rule:** Four quality dimensions are presented separately. No weighted sum, composite score, or single ranking may silently absorb trade-offs. A Candidate may score well on Candidate Quality and poorly on Entry Readiness, or vice versa.
- **§3 Three Candidate Axes:** Theme Relationship Role, Leadership State, and Research State are three independent axes with distinct scope and cardinality — not one enum or global Candidate property.

### 1.3 Domain Architecture (Approved Domain Specification v0.1)

- **§1.2 Alpha Momentum Owns:** Eligibility, Filtering (whether and how Theme relationships act as filters, enrichment, or ranking inputs), Prioritization and ranking, Strategy relevance (how Candidate Quality, Entry Readiness, and Theme Quality are presented together in Alpha Momentum's context), Candidate Quality dimensions/weights/feature definitions/scoring, Entry Readiness dimensions/weights/feature definitions/scoring, Research Queue prioritization and ordering, Alpha Momentum-specific rule packs, Alpha Momentum-specific screening pipeline and stage definitions.
- **§1.2 Alpha Momentum Consumes from Shared Core:** Canonical Theme data, Evidence and source data, Entity and asset identity, Normalized data, Feature computation infrastructure, Audit infrastructure.
- **§6 What Does NOT Belong in Shared Core:** Strategy-specific scoring weights or thresholds, strategy-specific ranking or prioritization logic, strategy-specific rule packs, strategy-specific feature definitions, Entry Readiness models specific to Alpha Momentum, Candidate Quality dimensions specific to Alpha Momentum, strategy-specific eligibility/filtering/screening pipeline definitions.

### 1.4 Alpha Momentum V0 Specification (Approved Domain Specification v0.1)

- **§4.1–4.2 Pipeline Stages:** Universe Definition → Theme Context / Theme-linked Selection → Candidate Quality Assessment → Entry Readiness Assessment → Data Confidence Assessment → Research Queue Assembly. The Theme-linked pipeline demonstrated in V0 is a demonstration boundary, not the permanent Alpha Momentum pipeline architecture (§4.4).
- **§4.3 Deterministic Features:** All feature computations must be deterministic. Exact feature formulas, weights, and thresholds are deferred.
- **§4.4 Theme Context Boundary:** Future Alpha Momentum versions must preserve the ability to discover candidates through stock-first screening independent of Theme membership, enrich stock-first candidates with Theme context after discovery, and combine Theme-linked and stock-first discovery paths.

### 1.5 Theme Model (Approved Domain Specification v0.1)

- **§2 Lifecycle:** "no stage is inherently higher quality than another." Lifecycle is a separate axis from Approval Status, Monitoring Status, confidence, crowding, and evidence progression.
- **§8 Confidence:** Confidence is a separate axis. Exact measurement deferred.

### 1.6 Design Plan (Approved Stable Design Plan v0.1)

- **§7 Materiality Policy:** A decision is material if it changes or establishes domain definitions/invariants, strategy eligibility, filtering, ranking, queue behavior, thresholds, weights, formulas, evidence semantics, point-in-time behavior, missing-data behavior, human-review visibility, override semantics, or Shared Platform vs. strategy ownership.
- **§11 Rule-Authority Requirements:** Four permitted Rule Content Authorities: Founder-provided rule, existing approved Constitution or Domain Specification (only for exact rule content it explicitly specifies), approved external doctrine explicitly adopted by the Founder, explicitly approved V0 experiment assumption.

---

## 2. Active Unresolved Decision Slots

---

### Decision Slot: DS-301 — V0 Candidate Quality Domain Set

- **Identifier:** DS-301
- **Topic:** Which of the seven deferred Candidate Quality domains (Fundamentals, Growth, Liquidity, Relative Strength, Trend Quality, Accumulation, Industry Leadership) are selected for V0 scope, and in what grouping or priority
- **Decision Obligation Source:** Constitution §13 lists Candidate Quality domains. CANDIDATE-AND-QUEUE-MODEL §2.1 lists the same domains with "Domains are deferred for finalization (OPEN-QUESTIONS.md)." DOMAIN-ARCHITECTURE §1.2 assigns Alpha Momentum ownership of Candidate Quality dimensions
- **Inherited Approved Semantics:** The seven domains are a deferred menu from the approved specifications. No V0 domain set is approved. The Constitution requires Candidate Quality assessment; which sub-dimensions are included in V0 is a separate selection decision
- **Rule Content Authority:** Founder-provided rule — this decision
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision:**
  - **V0 Candidate Quality Domain Set:** Relative Strength, Accumulation, Liquidity, Growth, Trend Quality
  - **Domains deferred beyond V0:** Fundamentals, Industry Leadership
  - **Founder Intent:** Focus on momentum-aligned quality signals. Exclude Fundamentals and Industry Leadership from V0 scope. The selection reflects a Stage 2 (Mark Minervini) orientation — seeking stocks in confirmed uptrends with institutional accumulation, sufficient liquidity, earnings growth, and healthy trend structure, while excluding deteriorating (Stage 4) stocks. Late-stage and market-confirmation signals are not desired at the Candidate Quality level.
- **Affected Artifact(s):** RULE-PACK-AND-QUALITY-CONTRACTS.md; Candidate Quality assessment output; conditional domain measurement templates (TPL-RP-CANDIDATE-DOMAIN — instantiated for each of the 5 selected domains)
- **Decision Category:** Eligibility (domain scope)
- **Materiality:** Material — determines which aspects of Candidate Quality the V0 pipeline assesses
- **Status:** Approved
- **Resolution:** RESOLVED — 5 domains selected; 2 deferred
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** Domain list from approved specifications; V0 scope constraints; fixture data availability per domain
- **Required Output States:** An explicit V0 Candidate Quality domain set: Relative Strength, Accumulation, Liquidity, Growth, Trend Quality. Each selected domain maps to a measurement contract instantiated from TPL-RP-CANDIDATE-DOMAIN. Fundamentals and Industry Leadership deferred to later versions.
- **Required Explainability:** Which domains were selected (5), which were deferred (2 — Fundamentals, Industry Leadership), rationale, and the rule version
- **Missing-Data Question:** Not applicable at domain-selection level
- **Conflicting-Evidence Question:** Not applicable
- **Point-in-Time Question:** Not applicable at domain-selection level
- **Dependencies:** None blocking
- **Alternatives to Evaluate:** Evaluated by Founder
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-FIRST-DECISION-GROUP-v0.1
- **Verification Evidence:** Founder explicitly selected 5 domains in session; rationale recorded above

---

### Decision Slot: DS-302 — V0 Entry Readiness Domain Set

- **Identifier:** DS-302
- **Topic:** Which of the six deferred Entry Readiness domains (Price Structure, Base Quality, Breakout Proximity, Volume Behavior, Volatility Contraction, Extension Risk) are selected for V0 scope
- **Decision Obligation Source:** Constitution §13 lists Entry Readiness domains. CANDIDATE-AND-QUEUE-MODEL §2.3 lists the same domains with "Domains are deferred for finalization." DOMAIN-ARCHITECTURE §1.2 assigns Alpha Momentum ownership of Entry Readiness dimensions
- **Inherited Approved Semantics:** The six domains are a deferred menu from the approved specifications. No V0 domain set is approved
- **Rule Content Authority:** Founder-provided rule — this decision
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision:**
  - **V0 Entry Readiness Domain Set:** Base Quality, Volatility Contraction, Extension Risk, Breakout Proximity
  - **Domains deferred beyond V0:** Price Structure, Volume Behavior
  - **Founder Intent:** Focus on the core entry-timing signals that matter for momentum entries — quality of the consolidation base, volatility contraction patterns (VCP), extension risk (don't chase extended stocks), and breakout proximity (how close to the pivot). Price Structure and Volume Behavior are deferred to later versions.
- **Affected Artifact(s):** RULE-PACK-AND-QUALITY-CONTRACTS.md; Entry Readiness assessment output; conditional domain measurement templates (TPL-RP-ENTRY-DOMAIN — instantiated for each of the 4 selected domains)
- **Decision Category:** Eligibility (domain scope)
- **Materiality:** Material — determines which aspects of Entry Readiness the V0 pipeline assesses
- **Status:** Approved
- **Resolution:** RESOLVED — 4 domains selected; 2 deferred
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** Domain list from approved specifications; V0 scope constraints; fixture data availability
- **Required Output States:** An explicit V0 Entry Readiness domain set: Base Quality, Volatility Contraction, Extension Risk, Breakout Proximity. Each selected domain maps to a measurement contract instantiated from TPL-RP-ENTRY-DOMAIN. Price Structure and Volume Behavior deferred to later versions.
- **Required Explainability:** Which domains were selected (4), which were deferred (2 — Price Structure, Volume Behavior), rationale, and the rule version
- **Missing-Data Question:** Not applicable
- **Conflicting-Evidence Question:** Not applicable
- **Point-in-Time Question:** Not applicable
- **Dependencies:** None blocking
- **Alternatives to Evaluate:** Evaluated by Founder
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-FIRST-DECISION-GROUP-v0.1
- **Verification Evidence:** Founder explicitly selected 4 domains in session; rationale recorded above

---

### Decision Slot: DS-303 — V0 Theme Quality Consumption Contract

- **Identifier:** DS-303
- **Topic:** Which already approved Shared-Core Theme Quality outputs Alpha Momentum consumes in V0; how Alpha Momentum presents and uses those outputs in strategy context; how lifecycle, Theme Confidence, crowding, and evidence progression remain separately visible; and preventing silent collapse of separate Theme axes
- **Decision Obligation Source:** Constitution §13 requires Alpha Momentum to assess Theme Quality. CANDIDATE-AND-QUEUE-MODEL §2.2 lists Theme Quality domains owned by Shared Core. DOMAIN-ARCHITECTURE §1.2: Alpha Momentum consumes canonical Theme data from Shared Core. THEME-MODEL §2: lifecycle is separate from quality ranking; "no stage is inherently higher quality than another." THEME-MODEL §8: confidence is a separate axis
- **Inherited Approved Semantics:** Shared Core owns Theme Quality definitions (DOMAIN-ARCHITECTURE §1.1). Alpha Momentum consumes Shared-Core outputs for strategy context (DOMAIN-ARCHITECTURE §1.2). Lifecycle, confidence, crowding, and evidence progression are separate axes within Theme Intelligence (THEME-MODEL §2, §8). No stage is inherently higher quality than another. This decision must not define Shared-Core Theme Quality dimensions, add or remove Theme Quality dimensions, define how lifecycle/confidence/crowding/evidence progression compose Theme Quality, or assign lifecycle an inherent quality value. If approved Shared-Core definitions are insufficient for Alpha Momentum consumption, UPSTREAM AMENDMENT REQUIRED — stop that decision path
- **Rule Content Authority:** Founder-provided rule — this decision
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision:**
  - **Consumed Axes (all Shared-Core Theme Quality outputs):**
    1. Lifecycle Stage (6 stages: Weak Signal → Deterioration)
    2. Breadth (sectors, entities, geographical scope)
    3. Leadership (which entities are leaders/challengers — canonical per DR-006)
    4. Evidence Progression (Structural → Operational → Fundamental → Market → Crowding)
    5. Market Confirmation (market price action confirming the theme)
    6. Fundamental Confirmation (earnings/fundamentals confirming the theme)
    7. Crowding (how crowded the theme is)
    8. Confidence (overall confidence in the theme assessment)
  - **Presentation Rule:** All axes are displayed individually — never collapsed into a single composite score. Each axis retains its own label and value. Market Confirmation is consumed and displayed to the Founder but is NOT used as a filter or gating signal within Alpha Momentum's pipeline.
  - **Founder Intent:** Complete visibility into Shared-Core Theme Quality with all axes kept separate. Market Confirmation is an informational axis shown to the Founder but does not gate or filter Candidates. This aligns with the principle that Alpha Momentum should not rely on late-stage market confirmation to make stock-level decisions.
- **Affected Artifact(s):** RULE-PACK-AND-QUALITY-CONTRACTS.md; Theme Card presentation (future Gate C); Alpha Momentum strategy output
- **Decision Category:** Eligibility (consumption scope)
- **Materiality:** Material — determines what Theme information informs Alpha Momentum's strategy context
- **Status:** Approved
- **Resolution:** RESOLVED — all 8 axes consumed; all displayed individually; Market Confirmation is display-only (not a filter)
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** Shared-Core Theme Quality output specification; separate-axes requirements from THEME-MODEL
- **Required Output States:** A consumption contract covering all 8 axes. Each axis displayed individually. Market Confirmation flagged as display-only (non-gating). The contract must not alter Shared-Core definitions.
- **Required Explainability:** Which Theme Quality outputs are consumed (all 8), how they are presented (individually), which axes are display-only vs. gating, and the rule version
- **Missing-Data Question:** When a consumed Shared-Core output is unavailable or not yet assessed for a Theme, the axis is displayed as "Not Assessed" with the reason
- **Conflicting-Evidence Question:** When separate axes point in different strategic directions (e.g., early Lifecycle + high Crowding), all axes are displayed individually — no synthetic reconciliation. The Founder interprets the combined picture.
- **Point-in-Time Question:** Theme Quality outputs are assessed at the evaluation timestamp of the pipeline run
- **Dependencies:** Shared-Core Theme Quality output definitions; DS-306 (Theme Quality Output and Summary Policy)
- **Alternatives to Evaluate:** Evaluated by Founder — all-axes with Market Confirmation display-only was selected over excluding Market Confirmation entirely
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-FIRST-DECISION-GROUP-v0.1
- **Verification Evidence:** Founder explicitly approved consumption of all axes with separate display and Market Confirmation as display-only in session

---

### Decision Slot: DS-304 — Candidate Quality Output and Summary Policy

- **Identifier:** DS-304
- **Topic:** How Candidate Quality sub-dimension results (for domains selected by DS-301) are presented and summarized; "no summary" is a valid outcome
- **Decision Obligation Source:** Constitution §10 requires keeping quality dimensions separate. CANDIDATE-AND-QUEUE-MODEL §2.5 prohibits a single ranking silently absorbing trade-offs. The exact presentation method for sub-dimensions within Candidate Quality is not supplied
- **Inherited Approved Semantics:** The four quality dimensions must remain separate and individually visible. Within Candidate Quality, sub-dimensions may be presented individually or summarized — but no opaque composite score may hide dimension-level trade-offs
- **Rule Content Authority:** Founder-provided rule — this decision
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (Approach B: Individual + Grouped):**
  - All 5 Candidate Quality domains are displayed. No domain is hidden or collapsed.
  - Grouping:
    | Group | Domains |
    |---|---|
    | **Trend & Participation** | Relative Strength, Trend Quality, Accumulation |
    | **Tradeability & Growth** | Liquidity, Growth |
  - Each domain within a group displays its own individual result. Groups provide organizational context — they do not combine, average, or synthesize domain results. No per-group score.
  - No single composite score for Candidate Quality overall.
- **Affected Artifact(s):** RULE-PACK-AND-QUALITY-CONTRACTS.md; Candidate Quality assessment output; Research Queue presentation
- **Decision Category:** Other (Output Policy)
- **Materiality:** Material — determines how Candidate Quality information reaches the Founder
- **Status:** Approved
- **Resolution:** RESOLVED — Approach B: Individual results grouped into Trend & Participation and Tradeability & Growth
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** DS-301 domain selection; per-domain measurement outputs; separation-rule constraints
- **Required Output States:** A deterministic output policy: all 5 domains displayed individually, organized in 2 groups. No composite scores. No hidden domains.
- **Required Explainability:** Which dimensions contributed, their individual assessments, their group placement, and the rule version
- **Missing-Data Question:** When a domain cannot be assessed, it is displayed as "Not Assessed" with the reason, within its group
- **Conflicting-Evidence Question:** Conflicting sub-dimension signals are displayed as-is within their groups — no automatic reconciliation
- **Point-in-Time Question:** All sub-dimension outputs share the same evaluation timestamp as the pipeline run
- **Dependencies:** DS-301 (domain selection — resolved)
- **Alternatives to Evaluate:** Evaluated by Founder — Approach B (grouped) selected over A (flat) and C (traffic light)
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-2-OUTPUT-POLICIES-v0.1
- **Verification Evidence:** Founder explicitly approved Approach B with 2 groups for Candidate Quality in session

---

### Decision Slot: DS-305 — Entry Readiness Output and Summary Policy

- **Identifier:** DS-305
- **Topic:** How Entry Readiness sub-dimension results (for domains selected by DS-302) are presented and summarized
- **Decision Obligation Source:** Constitution §10; CANDIDATE-AND-QUEUE-MODEL §2.5 separation rule. The exact presentation method within Entry Readiness is not supplied
- **Inherited Approved Semantics:** Same separation constraint as DS-304, applied to Entry Readiness
- **Rule Content Authority:** Founder-provided rule — this decision
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (Approach B: Individual + Grouped):**
  - All 4 Entry Readiness domains are displayed. No domain is hidden or collapsed.
  - Grouping:
    | Group | Domains |
    |---|---|
    | **Pattern Quality** | Base Quality, Volatility Contraction |
    | **Entry Timing** | Breakout Proximity, Extension Risk |
  - Each domain within a group displays its own individual result. Groups provide organizational context — they do not combine, average, or synthesize domain results. No per-group score.
  - No single composite score for Entry Readiness overall.
- **Affected Artifact(s):** RULE-PACK-AND-QUALITY-CONTRACTS.md; Entry Readiness assessment output; Research Queue presentation
- **Decision Category:** Other (Output Policy)
- **Materiality:** Material
- **Status:** Approved
- **Resolution:** RESOLVED — Approach B: Individual results grouped into Pattern Quality and Entry Timing
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** DS-302 domain selection; per-domain measurement outputs
- **Required Output States:** A deterministic output policy: all 4 domains displayed individually, organized in 2 groups. No composite scores. No hidden domains.
- **Required Explainability:** Which dimensions contributed, their individual assessments, their group placement, and the rule version
- **Missing-Data Question:** When a domain cannot be assessed, it is displayed as "Not Assessed" with the reason, within its group
- **Conflicting-Evidence Question:** Conflicting sub-dimension signals are displayed as-is within their groups — no automatic reconciliation
- **Point-in-Time Question:** All sub-dimension outputs share the same evaluation timestamp as the pipeline run
- **Dependencies:** DS-302 (domain selection — resolved)
- **Alternatives to Evaluate:** Evaluated by Founder — Approach B (grouped) selected over A (flat) and C (traffic light)
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-2-OUTPUT-POLICIES-v0.1
- **Verification Evidence:** Founder explicitly approved Approach B with 2 groups for Entry Readiness in session

---

### Decision Slot: DS-306 — Theme Quality Output and Summary Policy (Alpha Momentum Consumption)

- **Identifier:** DS-306
- **Topic:** How Theme Quality outputs consumed by Alpha Momentum (per DS-303) are presented and summarized in Alpha Momentum's strategy context; covers Alpha Momentum consumption presentation only, not canonical Shared-Core Theme Quality output design
- **Decision Obligation Source:** Constitution §10; CANDIDATE-AND-QUEUE-MODEL §2.5 separation rule. DOMAIN-ARCHITECTURE §1.2: Alpha Momentum owns strategy relevance presentation. Shared Core owns Theme Quality output design
- **Inherited Approved Semantics:** Shared Core defines canonical Theme Quality output. Alpha Momentum decides how to present consumed outputs in strategy context. This slot addresses Alpha Momentum's consumption presentation, not Shared-Core output design
- **Rule Content Authority:** Founder-provided rule — this decision
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (Approach B: Individual + Grouped):**
  - All 8 Theme Quality axes are displayed. No axis is hidden or collapsed.
  - Grouping:
    | Group | Axes |
    |---|---|
    | **Theme Structure** | Lifecycle, Breadth, Leadership |
    | **Evidence & Confirmation** | Evidence Progression, Market Confirmation, Fundamental Confirmation |
    | **Risk & Meta** | Crowding, Confidence |
  - Each axis within a group displays its own individual value. Groups provide organizational context — they do not combine, average, or synthesize axis values. No per-group score.
  - Market Confirmation remains display-only (non-gating per DS-303) — this is an informational label on the axis, not a filter.
  - No single composite score for Theme Quality overall.
- **Affected Artifact(s):** RULE-PACK-AND-QUALITY-CONTRACTS.md; Alpha Momentum strategy output
- **Decision Category:** Other (Output Policy)
- **Materiality:** Material
- **Status:** Approved
- **Resolution:** RESOLVED — Approach B: Individual axes grouped into Theme Structure, Evidence & Confirmation, and Risk & Meta
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** DS-303 consumption contract; Shared-Core Theme Quality output specification
- **Required Output States:** A deterministic consumption-presentation policy: all 8 axes displayed individually, organized in 3 groups. No composite scores. Market Confirmation flagged display-only. Must not alter Shared-Core output design.
- **Required Explainability:** Which Theme Quality outputs are shown, their group placement, which are display-only vs. gating, and the rule version
- **Missing-Data Question:** When a consumed Shared-Core output is unavailable, the axis is displayed as "Not Assessed" with the reason, within its group
- **Conflicting-Evidence Question:** Conflicting Theme Quality signals are displayed as-is within their groups — no synthetic reconciliation. The Founder interprets the combined picture.
- **Point-in-Time Question:** Theme Quality outputs are assessed at the evaluation timestamp of the pipeline run
- **Dependencies:** DS-303 (consumption contract — resolved); Shared-Core Theme Quality output definitions
- **Alternatives to Evaluate:** Evaluated by Founder — Approach B (grouped) selected over A (flat) and C (traffic light)
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-2-OUTPUT-POLICIES-v0.1
- **Verification Evidence:** Founder explicitly approved Approach B with 3 groups for Theme Quality in session

---

### Decision Slot: DS-307 — Strategy-Relevance Policy While Preserving Separate Dimensions

- **Identifier:** DS-307
- **Topic:** How Candidate Quality, Entry Readiness, Theme Quality, and Data Confidence are presented together in Alpha Momentum's context without collapsing into one opaque score
- **Decision Obligation Source:** DOMAIN-ARCHITECTURE §1.2: Alpha Momentum owns "Strategy relevance: how Candidate Quality, Entry Readiness, and Theme Quality combine in Alpha Momentum's context." Constitution §10: must keep them separate. CANDIDATE-AND-QUEUE-MODEL §2.5: no single ranking may silently absorb trade-offs
- **Inherited Approved Semantics:** The four quality dimensions (including Data Confidence) must remain separate, visible, and individually assessable. Alpha Momentum determines the strategic presentation relationship. No opaque composite score is permitted
- **Rule Content Authority:** Founder-provided rule — this decision, grounded in previously approved DS-304, DS-305, DS-306, and DS-412
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (Four Dimensions Side by Side, No Synthesis):**
  - **หลักการ:** ทั้ง 4 มิติใหญ่ (Theme Quality, Candidate Quality, Entry Readiness, Data Confidence) ปรากฏอยู่ด้วยกันในหน้าจอ Candidate — แต่ไม่มีสูตรไหนที่ยุบรวมมันเป็นตัวเลขหรือคะแนนเดียว
  - **ลำดับการแสดงผล:** TQ → CQ → ER → DC — เรียงจากมุมกว้างสุด (Theme) ไปหาแคบสุด (timing + confidence):
    1. **Theme Quality** — 8 แกน จัด 3 กลุ่ม (Theme Structure, Evidence & Confirmation, Risk & Meta) — ตาม DS-306
    2. **Candidate Quality** — 5 domains จัด 2 กลุ่ม (Trend & Participation, Tradeability & Growth) — ตาม DS-304
    3. **Entry Readiness** — 4 domains จัด 2 กลุ่ม (Pattern Quality, Entry Timing) — ตาม DS-305
    4. **Data Confidence** — แสดงในระดับ Candidate (per DS-412) — 6 dimensions แยกกัน ไม่ roll-up
  - **สิ่งที่ไม่มี:** ไม่มี composite score, ไม่มี star rating, ไม่มี "overall score", ไม่มี weighted average, ไม่มี traffic light รวม — เพราะทุกการยุบรวมซ่อน trade-off (Constitution §10)
  - **เวลามิติใดมิติหนึ่งขัดแย้งกัน (เช่น CQ สูง แต่ ER ต่ำ):** แสดงตามจริงทั้งคู่ — Founder เป็นคนตีความเอง ไม่ใช่ระบบ
  - **ชื่อหน้าจอนี้:** "Candidate Strategy View" — แสดงทุกมิติแยกกัน แต่ในหน้าเดียว
- **Affected Artifact(s):** RULE-PACK-AND-QUALITY-CONTRACTS.md; Research Queue prioritization; Alpha Momentum strategy output
- **Decision Category:** Other (Strategy Policy)
- **Materiality:** Material — determines the fundamental evaluation architecture for how Alpha Momentum presents Candidates
- **Status:** Approved
- **Resolution:** RESOLVED — 4 มิติแยกกัน เรียง TQ→CQ→ER→DC; ไม่มี composite score
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** Candidate Quality outputs (DS-304); Entry Readiness outputs (DS-305); Theme Quality outputs (DS-306); Data Confidence outputs (DS-412)
- **Required Output States:** "Candidate Strategy View" แสดงทั้ง 4 มิติแยกกันตามลำดับที่กำหนด — แต่ละมิติคงรูปแบบ grouped (Approach B) จาก Wave 2
- **Required Explainability:** แต่ละมิติแสดงผลอย่างไร, ทำไมเรียงแบบนี้, และ rule version
- **Missing-Data Question:** มิติที่ประเมินไม่ได้ → แสดง "Not Assessed" พร้อมเหตุผล — ไม่ซ่อน ไม่ข้าม
- **Conflicting-Evidence Question:** มิติที่ให้สัญญาณขัดแย้งกัน → แสดงตามจริง — Founder เป็นคนตีความ
- **Point-in-Time Question:** ทั้ง 4 มิติใช้ evaluation timestamp เดียวกันจาก pipeline run
- **Dependencies:** DS-304, DS-305, DS-306, DS-412 (all resolved)
- **Alternatives to Evaluate:** Evaluated by Founder — 4 dimensions side-by-side chosen to preserve separation per Constitution §10
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-4-ARCHITECTURE-v0.1
- **Verification Evidence:** Founder approved 4-dimension side-by-side strategy view with TQ→CQ→ER→DC ordering in session

---

### Decision Slot: DS-308 — Theme Context Operational Classification

- **Identifier:** DS-308
- **Topic:** Whether Candidate–Theme relationships in the Alpha Momentum pipeline act as a filter, enrichment, ranking input, or combination. This is the canonical decision; the Pipeline artifact references this identifier
- **Decision Obligation Source:** ALPHA-MOMENTUM-V0-SPEC §4.2: "Alpha Momentum decides whether they act as filter, enrichment, or ranking input." DOMAIN-ARCHITECTURE §1.2 assigns Filtering to Alpha Momentum
- **Inherited Approved Semantics:** Shared Core supplies Approved Theme relationships. Alpha Momentum decides their operational role. The V0 pipeline is a demonstration boundary per §4.4
- **Rule Content Authority:** Founder-provided rule — this decision
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (Filter — Theme-Gated Pipeline Entry):**
  - **การตัดสินใจ:** Candidate ต้องมี Theme อย่างน้อย 1 Theme ถึงจะเข้า Alpha Momentum pipeline ได้ — หุ้นที่ไม่มี Theme relationship ใดๆ เลยจะถูกคัดออกตั้งแต่ stage แรก
  - **เหตุผล:** Fundflow ไหลไปตาม Theme — เงินลงทุนสถาบัน (smart money) เคลื่อนย้ายตาม theme/กลุ่ม ไม่ใช่รายตัว — การซื้อหุ้นโดยไม่เข้าใจว่า theme อะไรดันอยู่คือการว่ายทวนน้ำ ผิดหลัก momentum
  - **นี่คือ filter ไม่ใช่ enrichment:** Theme Context stage ทำหน้าที่เป็นประตู — Candidate ต้องผ่านประตูนี้ถึงจะได้ถูกประเมิน CQ, ER, DC ต่อ
  - **ผลกระทบต่อ pipeline:**
    - Stage 1 (Universe Definition) → รายชื่อหุ้นทั้งหมดใน universe
    - Stage 2 (Theme Context) → **กรอง:** เหลือเฉพาะหุ้นที่มี Candidate–Theme relationship กับ Approved Themes
    - Stage 3+ (CQ, ER, DC, Queue) → ดำเนินการต่อเฉพาะหุ้นที่ผ่านกรอง
  - **หุ้นที่มีหลาย Theme:** ผ่าน filter ได้ตามปกติ — ข้อมูลจากทุก Theme จะถูกใช้ใน assessment (ตาม DR-006: canonical roles จาก Shared Core เป็นหลัก)
  - **V0 เป็น Theme-linked demo:** นี่คือ demonstration boundary — ใน V1+ จะเพิ่ม stock-first discovery path (ตาม DS-511)
- **Affected Artifact(s):** RULE-PACK-AND-QUALITY-CONTRACTS.md (canonical); PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md (references via DS-502); Alpha Momentum pipeline Theme Context stage
- **Decision Category:** Filter, Eligibility
- **Materiality:** Material — determines which Candidates enter the pipeline; directly defines the V0 demonstration boundary
- **Status:** Approved
- **Resolution:** RESOLVED — Filter; Candidate ต้องมี Theme อย่างน้อย 1 Theme; หุ้นไม่มี Theme = ไม่เข้า pipeline
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** Candidate–Theme relationship data; Approved Theme list; pipeline design constraints for stock-first path preservation
- **Required Output States:** Theme Context stage กรอง Candidate ตาม Theme membership — เฉพาะ Candidate ที่มี Theme relationship ≥ 1 ผ่านเข้า stage ถัดไป
- **Required Explainability:** Candidate แต่ละตัว: มี Theme อะไรบ้าง, ผ่าน/ไม่ผ่าน filter, และ rule version
- **Missing-Data Question:** Candidate ที่ไม่มี Candidate–Theme relationship data → ถือว่าไม่มี Theme → ไม่ผ่าน filter
- **Conflicting-Evidence Question:** Candidate ที่โยงกับหลาย Theme คุณภาพต่างกัน → ผ่าน filter (เข้าได้) — ข้อมูลทุก Theme ถูกเก็บไว้ใช้ต่อใน assessment
- **Point-in-Time Question:** Candidate–Theme relationships ถูกประเมิน ณ evaluation timestamp — Theme membership อาจเปลี่ยนตามเวลา (Theme lifecycle)
- **Dependencies:** DS-512 (Pipeline stage contracts — operationalizes this classification)
- **Alternatives to Evaluate:** Evaluated by Founder — Filter chosen over Enrichment based on principle that fundflow follows themes
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-4-ARCHITECTURE-v0.1
- **Verification Evidence:** Founder explicitly chose Filter: "ต้องมี Theme ครับ ผมเชื่อว่า fundflow มันไหลไปตาม theme"

---

### Decision Slot: DS-309 — Operational V0 Universe Boundary

- **Identifier:** DS-309
- **Topic:** Operational meaning of "US-listed common stock," ADR suitability definition, listing/de-listing point-in-time handling, duplicate listings and share classes, and public identifier requirements
- **Decision Obligation Source:** Constitution §13: "Alpha Momentum screens US-listed common stocks and suitable ADRs in V0." ALPHA-MOMENTUM-V0-SPEC §2.1: controlled subset via synthetic fixtures or approved historical snapshots
- **Inherited Approved Semantics:** The V0 universe is US-listed common stocks and suitable ADRs. V0 uses controlled fixtures. The Constitution does not supply specific exchange lists, ADR criteria, or operational boundary rules. This slot does not introduce price, liquidity, market-cap, float, or exchange filters — those require separate material eligibility decisions
- **Rule Content Authority:** Founder-provided rule — this decision
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (Fixture-Defined V0 Universe):**
  - **V0 universe ประกอบด้วย:** หุ้นสามัญที่ซื้อขายใน NYSE และ NASDAQ เท่านั้น — ไม่รวม OTC, pink sheets, หุ้นต่างประเทศที่ไม่ได้ซื้อขายผ่าน ADR
  - **ADR:** รวมเฉพาะ ADR ที่มีสภาพคล่องเพียงพอ — ใน V0 fixture creator เป็นคนเลือก ADR ที่จะรวม
  - **วิธีดำเนินการใน V0:** เราใช้ synthetic data → universe คือหุ้นที่เราใส่ใน fixture — ไม่มี real-time exchange feed — เราแค่ต้องแน่ใจว่าหุ้นใน fixture ทั้งหมดอยู่ใน NYSE/NASDAQ จริงตามสมมติ
  - **Edge cases ที่จัดการใน fixture:**
    - Delisting: fixture ระบุวันที่ delist → universe membership สิ้นสุดวันที่นั้น
    - หุ้นที่มีหลาย share class (เช่น GOOGL vs GOOG): fixture เลือก share class ที่มีสภาพคล่องที่สุด — รวมแค่หนึ่ง class ต่อบริษัท
    - identifier: ใช้ ticker symbol เป็น primary identifier ใน V0
  - **เลื่อนไป V0.5:** real exchange feed integration, automated listing/delisting detection, automated ADR suitability scoring, multi-class handling rules. ทั้งหมดนี้ต้องรอข้อมูลจริง
- **Affected Artifact(s):** RULE-PACK-AND-QUALITY-CONTRACTS.md; PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md (references via DS-501); Universe Definition pipeline stage
- **Decision Category:** Eligibility
- **Materiality:** Material — determines the operational boundary of the V0 universe
- **Status:** Approved
- **Resolution:** RESOLVED — NYSE + NASDAQ + suitable ADRs; fixture-defined; ticker as primary identifier; one class per company
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** Listing venue data; ADR classification data; corporate action data for listing/delisting events
- **Required Output States:** V0 universe = fixture-defined set of NYSE/NASDAQ stocks + ADRs; edge cases handled per fixture data
- **Required Explainability:** Which assets are included/excluded by the boundary definition, under what rules, and the rule version
- **Missing-Data Question:** Fixture ต้องมี listing venue + ADR classification ครบ — ถ้าขาด → flag "Not Assessable"
- **Conflicting-Evidence Question:** เราใช้ synthetic data → ไม่มี source conflict ใน V0
- **Point-in-Time Question:** Universe membership เปลี่ยนตาม listing/delisting dates ใน fixture
- **Dependencies:** None blocking
- **Alternatives to Evaluate:** Evaluated by Founder — fixture-defined universe chosen for V0 simplicity
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-5-STAGES-v0.1
- **Verification Evidence:** Founder approved NYSE+NASDAQ+ADRs fixture-defined universe in session

---

### Decision Slot: DS-310 — Additional Alpha Momentum Eligibility Criteria

- **Identifier:** DS-310
- **Topic:** Any eligibility rules beyond the Constitutional universe (US-listed common stocks and suitable ADRs), if any. Each additional criterion is a separate material decision
- **Decision Obligation Source:** DOMAIN-ARCHITECTURE §1.2 assigns Alpha Momentum ownership of Eligibility. Any criterion beyond the Constitutional universe is not approved and requires explicit Founder decision
- **Inherited Approved Semantics:** The Constitutional universe is the baseline. No additional eligibility rules are approved. This slot is the decision point for whether any additional criteria exist, not a proposal that they should
- **Rule Content Authority:** Founder-provided rule — this decision
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (No Additional Eligibility Criteria for V0):**
  - **การตัดสินใจ:** ไม่มี eligibility filter เพิ่มเติมนอกจาก universe boundary ที่กำหนดใน DS-309 (NYSE + NASDAQ + ADRs) — Constitutional universe คือ eligibility set ทั้งหมดสำหรับ V0
  - **ไม่มี:** price filter, market cap filter, liquidity filter, float filter, sector filter — เกณฑ์พวกนี้ถ้าต้องการในอนาคตต้องขอแยกเป็น material decision ใหม่
  - **V0 ใช้ synthetic data:** universe = หุ้นที่เราใส่ใน fixture → เราไม่ต้อง filter เพิ่มเพราะเราเลือกหุ้นเองอยู่แล้ว
  - **ถ้าในอนาคตต้องการเพิ่มเกณฑ์ (เช่น V0.5+):** แต่ละเกณฑ์ต้องเป็น material decision แยก — ต้องมี DS identifier ใหม่ — DS-310 นี้แค่ตอบว่า "V0 ไม่มีเกณฑ์เสริม"
- **Affected Artifact(s):** RULE-PACK-AND-QUALITY-CONTRACTS.md; Alpha Momentum eligibility rules; Universe Definition pipeline stage
- **Decision Category:** Eligibility, Threshold, Filter
- **Materiality:** Material if any additional criterion is adopted; this slot itself is the decision that none are adopted for V0
- **Status:** Approved
- **Resolution:** RESOLVED — ไม่มีเกณฑ์เสริม; Constitutional universe (NYSE+NASDAQ+ADR) คือ eligibility set ทั้งหมดของ V0
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** V0 scope constraints; fixture data characteristics; Founder preferences
- **Required Output States:** Eligibility = DS-309 universe boundary only; no additional filters
- **Required Explainability:** ไม่มีเกณฑ์เสริม; universe boundary (DS-309) คือเกณฑ์เดียวที่ใช้
- **Missing-Data Question:** Not applicable
- **Conflicting-Evidence Question:** Not applicable
- **Point-in-Time Question:** Universe boundary handles time-dependent membership; no additional time-dependent criteria
- **Dependencies:** DS-309 (universe boundary — resolved)
- **Alternatives to Evaluate:** Evaluated by Founder — no additional criteria chosen for V0 simplicity
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-5-STAGES-v0.1
- **Verification Evidence:** Founder approved no additional eligibility criteria for V0 in session

---

## 3. Conditional Templates

Templates are not active decisions. They carry TPL- identifiers and are instantiated with unique DS identifiers only when a domain-selection or ordering-form decision triggers them.

### Template: TPL-RP-CANDIDATE-DOMAIN — Candidate Quality Domain Measurement Contract

- **Template ID:** TPL-RP-CANDIDATE-DOMAIN
- **Purpose:** Conditional measurement contract for each Candidate Quality domain selected by DS-301. Defines the required fields, measurement method, feature contract reference, and output format for a single domain
- **Instantiation trigger:** DS-301 includes the domain in V0 scope
- **Instantiation method:** A new unique DS identifier is created through a later named authorization
- **Required fields per instantiation:** Measurement method; feature definitions (instantiated from TPL-RP-FEATURE-CONTRACT); output type and format; missing-data behavior; conflicting-evidence behavior; point-in-time requirements; explainability contract
- **Status:** Template — not an active decision

### Template: TPL-RP-ENTRY-DOMAIN — Entry Readiness Domain Measurement Contract

- **Template ID:** TPL-RP-ENTRY-DOMAIN
- **Purpose:** Conditional measurement contract for each Entry Readiness domain selected by DS-302
- **Instantiation trigger:** DS-302 includes the domain in V0 scope
- **Instantiation method:** New unique DS identifier through later named authorization
- **Required fields per instantiation:** Same structure as TPL-RP-CANDIDATE-DOMAIN
- **Status:** Template — not an active decision

### Template: TPL-RP-THEME-CONSUMPTION — Theme Quality Consumption Contract (Per-Dimension)

- **Template ID:** TPL-RP-THEME-CONSUMPTION
- **Purpose:** Conditional consumption contract for each Theme Quality dimension consumed under DS-303. Defines how Alpha Momentum consumes and presents a single Shared-Core Theme Quality output
- **Instantiation trigger:** DS-303 identifies the dimension for Alpha Momentum consumption
- **Instantiation method:** New unique DS identifier through later named authorization
- **Required fields per instantiation:** Shared-Core output reference; consumption method; presentation method within Alpha Momentum context; how the dimension remains separately visible
- **Status:** Template — not an active decision

### Template: TPL-RP-FEATURE-CONTRACT — Feature Definition Contract

- **Template ID:** TPL-RP-FEATURE-CONTRACT
- **Purpose:** Feature definition contract template. Each selected V0 domain may instantiate feature-definition decisions with unique DS identifiers through later named authorizations. Replaces the former single catch-all "Alpha Momentum Feature Definitions" slot
- **Instantiation trigger:** A domain is selected and its measurement contract requires feature definitions
- **Required fields per instantiation:** Exact formula or computation specification; input data references; parameters; version; deterministic execution guarantee; output type; missing-input behavior; point-in-time input requirements; computation lineage metadata
- **Status:** Template — not an active decision

### Template: TPL-REFERENCE-COHORT — Reference Cohort Contract Template

- **Template ID:** TPL-REFERENCE-COHORT
- **Purpose:** Template for a Reference Cohort Contract. A real RC identifier is created only after an approved relative rule requires a cohort. No active cohort exists
- **Required fields when instantiated:** Cohort or universe definition; evaluation timestamp; public-availability cutoff; minimum valid sample size; tie behavior; missing-value behavior; universe-change behavior; survivorship treatment; revision or vintage behavior
- **Status:** Template — not an active decision. Replaces former RC-001 which was an active identifier without an approved relative rule

---

## 4. Inherited Controls

The following are inherited approved governance controls from higher-authority documents. They are not unresolved decision slots.

### Higher-Authority Escalation

- **Source:** DESIGN-PLAN.md §13; AGENTS.md authority hierarchy
- **Rule:** When a proposed design decision would change, narrow, contradict, or extend the Constitution, Founder's Decisions, or an Approved Domain Specification: stop that decision path and record UPSTREAM AMENDMENT REQUIRED. The change cannot be approved merely through Gate A, B, C, or D. It requires the applicable material-change and authority-amendment process first
- **Status:** Inherited approved governance control — not an unresolved slot

### Contradiction Visibility (Presentation Layer)

- **Source:** EVIDENCE-MODEL §7: "Contradicting evidence remains visible and is never averaged away for presentation simplicity." Constitution §10: keep dimensions separate
- **Rule:** Contradictions must remain visible in all presentations. No computation may silently compress, net, or erase contradictory evidence. This is approved rule content, not an unresolved slot. Human-facing contradiction presentation display belongs to Gate C (no identifier assigned)
- **Status:** Inherited approved rule — not an unresolved slot

---

## 5. Deferred and Future-Gate Topics

No topics deferred or moved to future gates from this artifact. All active slots (DS-301–DS-310) are Gate A.

---

## 6. Slot Supersession Map

This artifact's v0.1-draft contained 28 decision slots (DS-001–DS-028) and 1 reference cohort contract (RC-001). The following map records their dispositions in the normalized v0.2-draft. Full cross-artifact supersession details are in TRACEABILITY-AND-DECISION-REGISTER.md.

| Old ID | Disposition | Reference |
|---|---|---|
| DS-001 – DS-007 | Superseded by template | TPL-RP-CANDIDATE-DOMAIN (conditional on DS-301) |
| DS-008 | Superseded by | DS-303 (V0 Theme Quality Consumption Contract) |
| DS-009 – DS-015 | Superseded by template | TPL-RP-THEME-CONSUMPTION (conditional on DS-303) |
| DS-016 – DS-021 | Superseded by template | TPL-RP-ENTRY-DOMAIN (conditional on DS-302) |
| DS-022 | Superseded by | DS-304 (Candidate Quality Output and Summary Policy) |
| DS-023 | Superseded by | DS-305 (Entry Readiness Output and Summary Policy) |
| DS-024 | Superseded by | DS-306 (Theme Quality Output and Summary Policy) |
| DS-025 | Superseded by | DS-307 (Strategy-Relevance Policy While Preserving Separate Dimensions) |
| DS-026 | Merged into | DS-308 (Theme Context Operational Classification — canonical) |
| DS-027 | Split and superseded by | DS-309 + DS-310 (Universe Boundary + Additional Eligibility) |
| DS-028 | Superseded by template | TPL-RP-FEATURE-CONTRACT |
| RC-001 | Removed; replaced by template | TPL-REFERENCE-COHORT |

---

## 7. Verification Requirements

Per DESIGN-PLAN.md §15 and VERIFICATION-DOCTRINE.md, Gate A verification requires:

- All 10 active slots are Approved. Rule Pack artifact: 10/10 complete.
- No slot proposes an investment-rule answer, threshold, weight, formula, lookback, benchmark, taxonomy, cohort, ordering, tie-breaker, eligibility rule, aggregation, or fallback (applies to all slots — resolved and unresolved)
- DS-303 limits scope to Alpha Momentum consumption; does not define Shared-Core Theme Quality (verified per approved resolution)
- Every slot carries Decision Obligation Source, Inherited Approved Semantics, Rule Content Authority, and Unresolved Operational Question
- Templates carry TPL- identifiers and are not counted as active decisions
- Old identifiers preserved in the Slot Supersession Map
- DR-003 remains Approved; DR-009 remains Approved (Gate A structural acceptance)
- Approved slots carry explicit Founder-decided resolutions with rationale and approval references
