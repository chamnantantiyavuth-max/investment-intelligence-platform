# Pipeline and Research Queue Design

Status: Accepted Gate A Decision-Slot Artifact
Version: 0.1
Owner: Founder
Authority: Structurally approved Gate A decision-slot artifact; individual decision-slot content gains authority only through its own named Founder approval
Derived from: Constitution v0.3, Project Definition v0.1, and Approved Stable Design Plan v0.1
Drafting Authorization: AM-V0-GATE-A-DRAFTING-v0.1
Structural Acceptance: AM-V0-GATE-A-STRUCTURAL-ACCEPTANCE-v0.1
Supersedes: v0.1-draft (DS-201–DS-218 — see Slot Supersession Map §7)

---

## 1. Inherited Approved Semantics

This section faithfully restates approved semantics that govern the Alpha Momentum screening pipeline stages, Research Queue structure, and related domain rules. No expansion or reinterpretation is intended.

### 1.1 Constitution v0.3

- **§14 Theme-First Research Queue:** The research queue is organized by Theme Card before individual stock ranking. Queue capacity is adaptive. It must not fill a quota with weak candidates. It may return zero high-priority candidates.

### 1.2 Alpha Momentum V0 Specification (Approved Domain Specification v0.1)

- **§4.1–4.2 Pipeline Stages:** Six conceptual stages: Universe Definition → Theme Context / Theme-linked Selection → Candidate Quality Assessment → Entry Readiness Assessment → Data Confidence Assessment → Research Queue Assembly. Ownership assigned per stage.
- **§4.3 Deterministic Features:** All feature computations must be deterministic. Reproducibility is required.
- **§4.4 Theme Context Boundary:** The Theme-linked pipeline is a demonstration boundary. Future versions must preserve stock-first discovery, Theme context enrichment, and combined discovery paths.
- **§5.2 Research Queue:** Theme-first, groups Candidates by Theme, presents four separated quality dimensions, supports adaptive capacity, may return zero high-priority candidates, provides human-readable explanations for prioritization.

### 1.3 Candidate and Queue Model (Approved Domain Specification v0.1)

- **§4.1 Structure:** Research Queue organized by Theme Card first, then Candidates within each Theme. Within a Theme, Candidates ordered by strategy-owned prioritization.
- **§4.2 Adaptive Capacity:** Queue capacity is adaptive. Not a fixed quota. May return zero, a small number, or a larger number. Capacity is quality-driven, not target-driven.
- **§4.3 Infrastructure vs. Semantics:** Shared Core may provide queue infrastructure. Each strategy owns its prioritization, ranking, ordering, and filtering semantics.

### 1.4 Domain Architecture (Approved Domain Specification v0.1)

- **§1.2 Alpha Momentum Owns:** Prioritization and ranking, Research Queue prioritization and ordering, Alpha Momentum-specific screening pipeline and stage definitions.
- **§1.1 Shared Core — Research Queue:** Infrastructure may be shared; semantics are strategy-owned.

### 1.5 Founder's Decisions

- **#8:** Research Queue is Theme-first.
- **#9:** Queue capacity is adaptive and may return zero candidates.

### 1.6 Design Plan (Approved Stable Design Plan v0.1)

- **§6 Gate A must not:** Populate eligibility gates, sort keys, tie-breakers, thresholds, ranking rules, or fallback behavior.
- **§7 Materiality Policy:** Material decisions include filtering, ranking, queue behavior, and missing-data behavior.

---

## 2. Active Unresolved Decision Slots

---

### Decision Slot: DS-501 — Operational V0 Universe Boundary in Pipeline Context

- **Identifier:** DS-501
- **Topic:** How the universe boundary (defined by DS-309 in RULE-PACK-AND-QUALITY-CONTRACTS.md) is operationally applied at the Universe Definition pipeline stage — what the stage consumes, what it emits, and how boundary-edge cases are handled
- **Decision Obligation Source:** ALPHA-MOMENTUM-V0-SPEC §4.2 defines Universe Definition stage. DS-309 defines the boundary. This slot addresses pipeline-specific operationalization
- **Inherited Approved Semantics:** The Universe Definition stage exists. The universe boundary is defined by DS-309. The stage must operate deterministically
- **Rule Content Authority:** Founder-provided rule — this decision, operationalizing DS-309 (resolved) and DS-310 (resolved)
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (Simple Pass-Through with Boundary Filter):**
  - **Stage 1 รับเข้า:** รายชื่อ assets ทั้งหมดใน fixture (ทุก ticker ที่มีข้อมูล)
  - **ทำอะไร:** ตรวจสอบแต่ละ asset — อยู่ใน NYSE/NASDAQ? เป็น ADR ที่เข้าเกณฑ์? มี listing date และยังไม่ delist ณ evaluation date?
  - **Stage 1 ส่งออก:** รายชื่อ Candidate ที่ผ่านเกณฑ์ universe (ตาม DS-309) พร้อม ticker, listing venue, ADR status, listing/delisting dates — **Universe stage ต้องไม่รู้จัก Theme (per DS-511)**
  - **Edge cases:** delisted → ไม่อยู่ใน universe หลังวันที่ delist; หลาย share class → เอาแค่ class ที่มีสภาพคล่องสูงสุด (per DS-309)
  - **ไม่มี eligibility filter เพิ่ม (per DS-310):** universe boundary อย่างเดียว — ไม่ filter ด้วย price, market cap, liquidity
- **Affected Artifact(s):** PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md; Universe Definition stage implementation
- **Decision Category:** Filter, Eligibility
- **Materiality:** Material — determines which assets proceed to subsequent stages
- **Status:** Approved
- **Resolution:** RESOLVED — Universe stage รับ asset list → กรองด้วย DS-309 universe rules → ส่ง candidate list; ไม่รู้จัก Theme (DS-511)
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** DS-309 boundary definition; asset inventory data
- **Required Output States:** Candidate list — เฉพาะ NYSE/NASDAQ/ADR; พร้อม metadata (venue, ADR status, dates)
- **Required Explainability:** Candidate ผ่าน/ไม่ผ่าน เพราะอะไร — "ไม่อยู่ใน NYSE/NASDAQ", "ADR ไม่มีสภาพคล่อง", "delisted"
- **Missing-Data Question:** ถ้า asset ขาด listing venue data → flag "Not Assessable" และคัดออก
- **Conflicting-Evidence Question:** Synthetic data → ไม่มี conflict ใน V0
- **Point-in-Time Question:** Universe membership ประเมิน ณ evaluation timestamp
- **Dependencies:** DS-309 (universe boundary definition — resolved); DS-310 (additional eligibility — resolved as none); DS-512 (stage contracts — resolved)
- **Alternatives to Evaluate:** Evaluated by Founder — simple pass-through with boundary filter
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-5-STAGES-v0.1
- **Verification Evidence:** Founder approved Universe stage operationalization in session

---

### Decision Slot: DS-502 — Theme Context Stage Behavior

- **Identifier:** DS-502
- **Topic:** Pipeline-specific operational behavior of the Theme Context stage, referencing canonical DS-308 for the filter/enrichment/ranking classification
- **Decision Obligation Source:** ALPHA-MOMENTUM-V0-SPEC §4.2 defines Theme Context stage. DS-308 defines the classification. This slot addresses pipeline-specific operationalization
- **Inherited Approved Semantics:** The Theme Context stage exists. Its classification (filter/enrichment/ranking) is determined by DS-308. The V0 pipeline is a Theme-linked demonstration boundary per §4.4
- **Rule Content Authority:** Founder-provided rule — this decision, operationalizing DS-308 (resolved as Filter)
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (Theme-Gated Filter Stage):**
  - **Stage 2 รับเข้า:** รายชื่อ Candidate จาก Stage 1 (Universe) + Candidate–Theme relationship data + Approved Theme list
  - **ทำอะไร:** ตรวจสอบ Candidate แต่ละตัว — มี Candidate–Theme relationship กับ Approved Theme อย่างน้อย 1 Theme หรือไม่?
  - **Stage 2 ส่งออก:** เฉพาะ Candidate ที่มี Theme ≥ 1 — พร้อมโยง Theme context ไว้ (ทุก Theme ที่ Candidate สังกัด ตาม DR-006)
  - **หุ้นมีหลาย Theme →** ผ่าน filter ได้ตามปกติ — ข้อมูลจากทุก Theme ถูกเก็บไว้ใช้ต่อใน assessment
  - **หุ้นไม่มี Theme →** ถูกคัดออก — ไม่เข้า Stage 3+
  - **นี่คือ filter — ไม่ใช่ enrichment:** หุ้นไม่มี Theme = หยุดที่นี่ (ตาม DS-308)
- **Affected Artifact(s):** PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md; Theme Context stage implementation
- **Decision Category:** Filter, Rank
- **Materiality:** Material — determines how Theme context affects Candidate flow
- **Status:** Approved
- **Resolution:** RESOLVED — Theme Context stage กรอง Candidate: ต้องมี Theme ≥ 1; หุ้นไม่มี Theme = ออก
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** DS-308 classification (resolved as Filter); Candidate–Theme relationship data; Approved Theme list
- **Required Output States:** Candidate list — เฉพาะผู้ที่มี Theme; แต่ละ Candidate โยงกับ Theme context
- **Required Explainability:** Candidate ผ่าน/ไม่ผ่าน — "มี Theme: AI Data Center", "ไม่มี Approved Theme"
- **Missing-Data Question:** Candidate ที่ไม่มี relationship data → ถือว่าไม่มี Theme → ไม่ผ่าน filter
- **Conflicting-Evidence Question:** หลาย Theme คุณภาพต่างกัน → ผ่านได้; ข้อมูลทุก Theme ส่งต่อ
- **Point-in-Time Question:** Theme membership ประเมิน ณ evaluation timestamp
- **Dependencies:** DS-308 (Theme Context classification — resolved as Filter); DS-512 (stage contracts — resolved)
- **Alternatives to Evaluate:** Evaluated by Founder — Filter operationalization per DS-308
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-5-STAGES-v0.1
- **Verification Evidence:** Founder approved Theme Context filter stage behavior in session

---

### Decision Slot: DS-503 — Candidate Quality Assessment — Gate/Rank/Enrichment Effects

- **Identifier:** DS-503
- **Topic:** Whether Candidate Quality output (as defined by DS-304 in RULE-PACK-AND-QUALITY-CONTRACTS.md) acts as a gate, ranking input, enrichment label, or combination in the pipeline flow
- **Decision Obligation Source:** ALPHA-MOMENTUM-V0-SPEC §4.2 defines Candidate Quality Assessment stage. DOMAIN-ARCHITECTURE §1.2 assigns Alpha Momentum ownership of prioritization and ranking
- **Inherited Approved Semantics:** The Candidate Quality Assessment stage exists. Its output format is determined by DS-304. This slot decides how the pipeline uses that output
- **Rule Content Authority:** Founder-provided rule — this decision
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (Enrichment — เพิ่มข้อมูล ไม่กรอง):**
  - CQ เป็น enrichment — ไม่ใช่ gate — เพราะ Theme filter (Stage 2) กรองมาแล้ว
  - **Stage 3 รับเข้า:** Candidate list จาก Stage 2
  - **ทำอะไร:** ประเมิน Candidate แต่ละตัวด้วย 5 domains (RS, Accumulation, Liquidity, Growth, Trend Quality) — ตาม DS-301/DS-304
  - **Stage 3 ส่งออก:** Candidate list เดิม — ทุกตัวผ่านหมด — แต่ละตัวมี CQ assessment เพิ่ม (grouped output ตาม DS-304)
  - **ทำไมไม่ gate:** V0 มี universe หุ้นแคบอยู่แล้ว + Theme filter → ไม่ต้อง filter ซ้ำด้วย CQ — CQ แค่บอกว่า "หุ้นนี้คุณภาพเป็นยังไง"
  - **ถ้าประเมินไม่ได้:** แสดง "Not Assessed" — Candidate ยังผ่านต่อไป (ไม่ถูกคัดออก)
- **Affected Artifact(s):** PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md; Candidate Quality Assessment stage implementation
- **Decision Category:** Filter, Rank
- **Materiality:** Material — determines whether Candidate Quality gates Candidates out or merely contributes to ordering
- **Status:** Approved
- **Resolution:** RESOLVED — Enrichment; CQ เพิ่มข้อมูล ไม่กรอง Candidate ออก
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** DS-304 output policy (resolved); Candidate Quality assessment outputs
- **Required Output States:** Candidate list + CQ assessment per Candidate; ทุก Candidate ผ่าน
- **Required Explainability:** CQ result per Candidate per domain per group
- **Missing-Data Question:** ประเมินไม่ได้ → "Not Assessed" → Candidate ยังผ่าน
- **Conflicting-Evidence Question:** Mixed sub-dimension results → แสดงตามจริง
- **Point-in-Time Question:** CQ ประเมิน ณ evaluation timestamp
- **Dependencies:** DS-304 (CQ output policy — resolved); DS-301 (domain selection — resolved)
- **Alternatives to Evaluate:** Evaluated by Founder — enrichment chosen for V0
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-5-STAGES-v0.1
- **Verification Evidence:** Founder approved CQ as enrichment in session

---

### Decision Slot: DS-504 — Entry Readiness Assessment — Gate/Rank/Enrichment Effects

- **Identifier:** DS-504
- **Topic:** Whether Entry Readiness output (as defined by DS-305) acts as a gate, ranking input, enrichment label, or combination in the pipeline flow
- **Decision Obligation Source:** ALPHA-MOMENTUM-V0-SPEC §4.2 defines Entry Readiness Assessment stage. DOMAIN-ARCHITECTURE §1.2 assigns Alpha Momentum ownership
- **Inherited Approved Semantics:** The Entry Readiness Assessment stage exists. Its output format is determined by DS-305
- **Rule Content Authority:** Founder-provided rule — this decision
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (Enrichment — เพิ่มข้อมูล ไม่กรอง):**
  - ER เป็น enrichment — ไม่ใช่ gate — เช่นเดียวกับ CQ
  - **Stage 4 รับเข้า:** Candidate list จาก Stage 3 (พร้อม CQ)
  - **ทำอะไร:** ประเมิน Candidate แต่ละตัวด้วย 4 domains (Base Quality, VCP, Extension Risk, Breakout Proximity) — ตาม DS-302/DS-305
  - **Stage 4 ส่งออก:** Candidate list เดิม — ทุกตัวผ่านหมด — แต่ละตัวมี ER assessment เพิ่ม (grouped output ตาม DS-305)
  - **ทำไมไม่ gate:** ER บอก "จังหวะเข้า" — แต่เราไม่อยากกรองหุ้นที่มี entry timing ไม่ดีออก เพราะตลาดเปลี่ยนได้ — ER แค่บอกข้อมูลให้ Founder ตัดสินใจ
  - **ถ้าประเมินไม่ได้:** แสดง "Not Assessed" — Candidate ยังผ่านต่อไป
- **Affected Artifact(s):** PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md; Entry Readiness Assessment stage implementation
- **Decision Category:** Filter, Rank
- **Materiality:** Material
- **Status:** Approved
- **Resolution:** RESOLVED — Enrichment; ER เพิ่มข้อมูล ไม่กรอง Candidate ออก
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** DS-305 output policy (resolved); Entry Readiness assessment outputs
- **Required Output States:** Candidate list + ER assessment per Candidate; ทุก Candidate ผ่าน
- **Required Explainability:** ER result per Candidate per domain per group
- **Missing-Data Question:** ประเมินไม่ได้ → "Not Assessed" → Candidate ยังผ่าน
- **Conflicting-Evidence Question:** Mixed sub-dimension signals → แสดงตามจริง
- **Point-in-Time Question:** ER ประเมิน ณ evaluation timestamp
- **Dependencies:** DS-305 (ER output policy — resolved); DS-302 (domain selection — resolved)
- **Alternatives to Evaluate:** Evaluated by Founder — enrichment chosen for V0
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-5-STAGES-v0.1
- **Verification Evidence:** Founder approved ER as enrichment in session

---

### Decision Slot: DS-505 — Data Confidence Assessment — Gate/Warning Effects

- **Identifier:** DS-505
- **Topic:** Whether Data Confidence output (as defined by DS-412 in DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md) acts as a gate, advisory warning, enrichment, or purely informational in the Alpha Momentum pipeline
- **Decision Obligation Source:** ALPHA-MOMENTUM-V0-SPEC §4.2 defines Data Confidence Assessment stage with Shared Core ownership. Alpha Momentum decides how the pipeline uses the output
- **Inherited Approved Semantics:** The Data Confidence Assessment stage exists. Shared Core owns the assessment. Alpha Momentum decides how the pipeline uses it
- **Rule Content Authority:** Founder-provided rule — this decision
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (Warning — เตือน ไม่กันออก):**
  - DC เป็น warning — ไม่ใช่ gate — DC เตือนว่า "ข้อมูลที่ใช้ประเมิน Candidate นี้อาจไม่น่าเชื่อถือ" แต่ไม่กัน Candidate ออก
  - **Stage 5 รับเข้า:** Candidate list จาก Stage 4 (พร้อม CQ + ER)
  - **ทำอะไร:** ประเมิน Data Confidence ในระดับ Candidate (ตาม DS-412) — แสดง 6 dimensions แยกกัน ไม่ roll-up
  - **Stage 5 ส่งออก:** Candidate list เดิม — ทุกตัวผ่านหมด — แต่ละตัวมี DC assessment เพิ่ม
  - **ทำไมไม่ gate:** DC เป็น metadata — บอกคุณภาพของข้อมูล ไม่ใช่คุณภาพของหุ้น — การกันหุ้นออกเพราะข้อมูลไม่ดีคือการทิ้งโอกาสเพราะปัญหา data quality ไม่ใช่เพราะหุ้นไม่ดี
  - **DC แสดงเป็นคำเตือน:** ถ้า DC ต่ำ (เช่น reliability ต่ำ, มี conflict, freshness stale) → เตือนให้ Founder รู้ แต่ไม่กัน Candidate
  - **ถ้าประเมินไม่ได้:** แสดง "Not Assessed" — Candidate ยังผ่านต่อไป
- **Affected Artifact(s):** PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md; Data Confidence Assessment stage pipeline behavior
- **Decision Category:** Filter, Rank
- **Materiality:** Material — determines whether low Data Confidence excludes Candidates or merely informs
- **Status:** Approved
- **Resolution:** RESOLVED — Warning; DC เตือน ไม่กัน Candidate ออก
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** DS-412 output format (resolved); Data Confidence assessment outputs
- **Required Output States:** Candidate list + DC assessment per Candidate; ทุก Candidate ผ่าน; DC dimensions แยกกัน
- **Required Explainability:** DC result per Candidate — 6 dimensions individually
- **Missing-Data Question:** DC ประเมินไม่ได้ → "Not Assessed" → Candidate ยังผ่าน
- **Conflicting-Evidence Question:** DC แสดง conflicts ตาม DS-405/DS-412 — ไม่ยุบรวม
- **Point-in-Time Question:** DC ประเมิน ณ evaluation timestamp
- **Dependencies:** DS-412 (DC scope levels — resolved); all Data Confidence dimension slots (resolved)
- **Alternatives to Evaluate:** Evaluated by Founder — warning chosen for V0
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-5-STAGES-v0.1
- **Verification Evidence:** Founder approved DC as warning (not gate) in session

---

### Decision Slot: DS-506 — Theme-First Queue Assembly

- **Identifier:** DS-506
- **Topic:** Structural rules for assembling the queue by Theme first, then Candidates; what the stage produces and how prior stage outputs are consumed
- **Decision Obligation Source:** ALPHA-MOMENTUM-V0-SPEC §4.2: "Order by Theme, then by strategy-owned prioritization within each Theme." Constitution §14: Theme-first. CANDIDATE-AND-QUEUE-MODEL §4.1: Theme-first structure
- **Inherited Approved Semantics:** Queue is Theme-first. Within-Theme ordering is strategy-owned. The structural assembly rules (how Themes are grouped, how Candidates are placed) are not fully supplied. The V0 pipeline is a Theme-linked demonstration boundary per §4.4
- **Rule Content Authority:** Founder-provided rule — this decision
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (Theme-First Grouping, No Within-Theme Ordering):**
  - **Stage 6 รับเข้า:** Candidate list จาก Stage 5 พร้อม assessments ครบ 4 มิติ (TQ, CQ, ER, DC)
  - **ทำอะไร:** จับกลุ่ม Candidate ตาม Theme — แต่ละ Theme เป็น "Theme Card" ที่มีรายชื่อ Candidate ภายใต้ Theme นั้น
  - **Stage 6 ส่งออก:** Research Queue — เรียงตาม Theme (Theme Card 1, Theme Card 2, ...), ภายในแต่ละ Theme เป็นกลุ่ม Candidate (ยังไม่เรียงลำดับ — per DS-507: unordered)
  - **Candidate ที่มีหลาย Theme:** ปรากฏในทุก Theme ที่สังกัด — ไม่ duplicate assessment data — แต่ visibility ในแต่ละ Theme context อาจเน้นคนละมุม
  - **Theme ที่ไม่มี Candidate ผ่าน filter:** ไม่ปรากฏในคิว (หรือแสดงเป็น "Theme มีอยู่ แต่ไม่มี Candidate ผ่านคุณสมบัติ")
- **Affected Artifact(s):** PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md; Research Queue Assembly stage implementation
- **Decision Category:** Rank
- **Materiality:** Material — determines the structure of the final queue output
- **Status:** Approved
- **Resolution:** RESOLVED — Theme-first grouping; ไม่เรียงลำดับภายใน Theme (รอ DS-507)
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** Outputs from all prior pipeline stages; Candidate–Theme relationship data
- **Required Output States:** Research Queue จัดกลุ่มตาม Theme — แต่ละ Theme มี Candidate list; ทุก Candidate ที่ผ่าน pipeline ปรากฏในคิว
- **Required Explainability:** Why each Theme appears, which Candidates belong to each Theme
- **Missing-Data Question:** Candidate มี Theme Quality data แต่ไม่มี CQ/ER/DC → ยังปรากฏในคิว — dimensions ที่ขาดแสดง "Not Assessed"
- **Conflicting-Evidence Question:** Candidate อยู่หลาย Theme → ปรากฏในทุก Theme — assessment data แชร์กัน
- **Point-in-Time Question:** Queue assembled ณ evaluation timestamp
- **Dependencies:** DS-307 (Strategy-Relevance — resolved); DS-308 (Theme Context — resolved); DS-503–DS-505 (stage effects — resolved)
- **Alternatives to Evaluate:** Evaluated by Founder — Theme-first grouping without within-Theme ordering for V0
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-6-QUEUE-v0.1
- **Verification Evidence:** Founder approved Theme-first queue assembly in session

---

### Decision Slot: DS-507 — V0 Prioritization Output Form

- **Identifier:** DS-507
- **Topic:** Whether V0 requires ordered, tiered/grouped, unordered, or no Theme/Candidate prioritization output. This is the parent decision; within-Theme ordering, Theme-level ordering, and tie behavior are conditional and become active only when an ordering-dependent form is selected
- **Decision Obligation Source:** Constitution §14: Research Queue is Theme-first. No prioritization output form is mandated. DESIGN-PLAN.md §6: Gate A must not decide queue ordering
- **Inherited Approved Semantics:** The queue exists and is Theme-first. The output form (ordered, tiered, unordered, none) is not specified
- **Rule Content Authority:** Founder-provided rule — this decision
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (Unordered — กลุ่มอย่างเดียว ไม่เรียงลำดับ):**
  - **V0 output form:** Unordered — Candidate ถูกจัดกลุ่มตาม Theme แต่ไม่เรียงลำดับภายในกลุ่ม
  - **ไม่มี:** ภายใน-Theme ordering (ไม่มี template TPL-PIPELINE-WITHIN-THEME-ORDERING), ระหว่าง-Theme ordering (ไม่มี template TPL-PIPELINE-THEME-LEVEL-ORDERING), tie-breaker rules (ไม่มี template TPL-PIPELINE-TIE-BEHAVIOR)
  - **เหตุผล:** การเรียงลำดับ = material decision ที่ต้องกำหนด weights, relative importance, tie-breakers — defer ไปถึง V1+ เมื่อเรามี real data และประสบการณ์ใช้ระบบ V0 จริง
  - **ผลต่อ templates:** templates ทั้ง 3 ตัว (TPL-PIPELINE-WITHIN-THEME-ORDERING, TPL-PIPELINE-THEME-LEVEL-ORDERING, TPL-PIPELINE-TIE-BEHAVIOR) ยังไม่ถูก activate — ยังเป็น conditional templates
- **Affected Artifact(s):** PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md; Research Queue Assembly output; conditional ordering templates
- **Decision Category:** Rank
- **Materiality:** Material — determines whether and how the queue communicates priority to the Founder
- **Status:** Approved
- **Resolution:** RESOLVED — Unordered; จัดกลุ่มตาม Theme ไม่เรียงลำดับ; ordering templates remain inactive
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** V0 scope and objectives; Founder review workflow expectations
- **Required Output States:** Queue output = Theme-first groupings, no within-group ordering
- **Required Explainability:** Output form: unordered groupings
- **Missing-Data Question:** Not applicable
- **Conflicting-Evidence Question:** Not applicable
- **Point-in-Time Question:** Not applicable at form-selection level
- **Dependencies:** DS-506 (Queue Assembly — resolved)
- **Alternatives to Evaluate:** Evaluated by Founder — unordered chosen to defer ordering complexity to V1+
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-6-QUEUE-v0.1
- **Verification Evidence:** Founder approved unordered queue output form in session

---

### Decision Slot: DS-508 — Adaptive-Capacity Decision Policy

- **Identifier:** DS-508
- **Topic:** The decision policy governing how many Candidates appear in the queue: quality-driven inclusion rules, no fixed quota, and valid empty-queue outcome. The decision policy may or may not use thresholds — "policy" does not presume "thresholds"
- **Decision Obligation Source:** Constitution §14: "Queue capacity is adaptive. It must not fill a quota with weak candidates. It may return zero high-priority candidates." Founder's Decision #9. CANDIDATE-AND-QUEUE-MODEL §4.2: "Capacity is determined by the number of candidates that meet the strategy's quality thresholds, not by a target count"
- **Inherited Approved Semantics:** Queue capacity is adaptive. It must not fill a quota. It may return zero Candidates. Capacity is quality-driven, not target-driven. The phrase "quality thresholds" in CANDIDATE-AND-QUEUE-MODEL §4.2 describes the conceptual principle — it does not mandate numeric thresholds as the implementation method
- **Rule Content Authority:** Founder-provided rule — this decision
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (Show All — No Quality Threshold in V0):**
  - **V0 capacity policy:** Candidates ทุกตัวที่ผ่าน pipeline (Stage 1+2 filters) ปรากฏในคิวทั้งหมด — ไม่มี quality threshold มากรองเพิ่ม
  - **"Adaptive" หมายความว่า:** จำนวน Candidate ในคิว = จำนวนที่ผ่าน filter — ไม่ใช่ quota ตายตัว — ถ้าผ่านน้อยคิวก็เล็ก, ถ้าผ่านมากคิวก็ใหญ่, ถ้าไม่มีใครผ่านเลยคิวก็ว่าง (DS-509)
  - **ไม่มีการเติม quota:** ถ้าผ่านแค่ 3 ตัว → คิวมี 3 ตัว — ไม่พยายามเติมให้ถึง 10
  - **Quality thresholds defer ไป V1+:** ยังไม่มีเกณฑ์คุณภาพขั้นต่ำ — เพราะทุกเกณฑ์คือ material decision ที่ต้องกำหนด thresholds → defer จนกว่าเรามีประสบการณ์ใช้ระบบ V0
- **Affected Artifact(s):** PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md; Research Queue Assembly; Research Queue output
- **Decision Category:** Threshold, Filter
- **Materiality:** Material — determines which Candidates appear in the queue and how many
- **Status:** Approved
- **Resolution:** RESOLVED — Show all Candidates that pass pipeline filters; no quality threshold; adaptive = no quota
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** Candidate assessments from all prior pipeline stages; quality dimension outputs
- **Required Output States:** Queue contains all Candidates passing Stage 1+2; count is adaptive; zero is valid
- **Required Explainability:** Total Candidates passing, why N Candidates
- **Missing-Data Question:** Candidate ที่ผ่าน filter แต่ assessment ไม่ครบ → ยังอยู่ในคิว
- **Conflicting-Evidence Question:** No per-dimension threshold → no conflict in inclusion decision
- **Point-in-Time Question:** Policy evaluated ณ evaluation timestamp
- **Dependencies:** DS-307 (Strategy-Relevance — resolved); DS-503–DS-505 (stage effects — resolved)
- **Alternatives to Evaluate:** Evaluated by Founder — show-all policy for V0
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-6-QUEUE-v0.1
- **Verification Evidence:** Founder approved show-all adaptive capacity in session

---

### Decision Slot: DS-509 — Queue Empty-State Operational Contract

- **Identifier:** DS-509
- **Topic:** Gate A operational contract for the empty-queue state: zero Candidates is a valid output; operational output state and required reason/audit categories; lineage to the rules and inputs producing the empty state; downstream contract behavior
- **Decision Obligation Source:** Constitution §14: may return zero. CANDIDATE-AND-QUEUE-MODEL §4.2: "Zero high-priority candidates (DNA-016: Honest Empty States)"
- **Inherited Approved Semantics:** The queue may return zero Candidates. The system must not fabricate Candidates. Gate A scope is limited to operational contract: output state, reason/audit categories, lineage, and downstream behavior. Human-facing presentation (UI wording, page layout, visual prominence, near-miss display, display order) belongs to Gate C (no identifier assigned)
- **Rule Content Authority:** Founder-provided rule — this decision
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (Empty Queue = Valid, Honest Output):**
  - **คิวว่างเปล่าเป็น output ที่ถูกต้อง** — ไม่ใช่ error — เกิดขึ้นได้เมื่อไม่มี Candidate ผ่าน Stage 1+2 filters
  - **สาเหตุที่คิวว่างได้:** (1) ไม่มีหุ้นใน universe ที่มี Approved Theme, (2) ทุกหุ้นที่มี Theme ถูก delist ก่อน evaluation date, (3) universe fixture ไม่มีข้อมูลในช่วงเวลานั้น
  - **สิ่งที่ระบบต้องบันทึกเมื่อคิวว่าง:** (a) evaluation timestamp, (b) จำนวน Candidate ที่เข้า Stage 1, (c) จำนวนที่ถูก filter ออกแต่ละ stage และเหตุผล, (d) rule versions ที่ใช้
  - **สิ่งที่ระบบห้ามทำ:** ห้ามลดมาตรฐานเพื่อให้มี Candidate, ห้ามสร้าง Candidate ปลอม, ห้ามเปลี่ยน filter rules อัตโนมัติ
  - **Human-facing display (Gate C):** หน้าจอว่างจะแสดงอะไร — เป็นเรื่องของ Gate C
- **Affected Artifact(s):** PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md; Research Queue Assembly; downstream consumers of queue output
- **Decision Category:** Fallback
- **Materiality:** Material — determines how the system communicates absence of opportunities
- **Status:** Approved
- **Resolution:** RESOLVED — Empty queue = valid, honest output; ต้องบันทึก audit trail; ห้าม fabrication
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** Queue assembly output (empty); pipeline stage outputs showing exclusion reasons
- **Required Output States:** Empty queue output contract: zero Candidates, reason categories, audit lineage
- **Required Explainability:** Why queue is empty, which rules/filters produced the empty state, lineage
- **Missing-Data Question:** แยกสาเหตุได้ว่า "ไม่มีข้อมูล" vs "มีข้อมูลแต่ไม่ผ่าน" — ต้องบันทึกต่างกัน
- **Conflicting-Evidence Question:** Not directly applicable
- **Point-in-Time Question:** Empty-state output carries evaluation timestamp
- **Dependencies:** DS-508 (Adaptive-Capacity — resolved); DS-506 (Queue Assembly — resolved); DS-510 (Explainability — pending)
- **Alternatives to Evaluate:** Evaluated by Founder — honest empty state as constitutional requirement
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-6-QUEUE-v0.1
- **Verification Evidence:** Founder approved honest empty-state contract in session

---

### Decision Slot: DS-510 — Explainability, Audit, and Rule-Result Lineage Contract

- **Identifier:** DS-510
- **Topic:** Logical minimum content required for deterministic explanation, audit, rule-result lineage, rule version linkage, input and evidence references, evaluation timestamp, and reproducibility. Gate A owns the logical minimum content; Gate C owns human-facing presentation, layout, wording, visual hierarchy, and display ordering (no Gate C identifier assigned)
- **Decision Obligation Source:** ALPHA-MOMENTUM-V0-SPEC §5.2: "human-readable explanations for prioritization." §5.3: evidence lineage traceability. §5.4: historical state queryability. Constitution §19: explainability, reproducibility. DOMAIN-ARCHITECTURE §5: audit trail for material transitions
- **Inherited Approved Semantics:** The queue must provide human-readable explanations. Evidence lineage must be traceable. Historical state must be queryable. Audit infrastructure exists. Reproducibility is required. The logical minimum content for these requirements is not supplied. Human-facing presentation belongs to Gate C
- **Rule Content Authority:** Founder-provided rule — this decision
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (Per-Run Audit Record + Per-Candidate Explanation):**
  - **ทุกครั้งที่ pipeline run — บันทึก audit record ที่ประกอบด้วย:**
    1. `run_id` — unique identifier ของการ run ครั้งนี้
    2. `evaluation_timestamp` — วันที่/เวลาที่ประเมิน
    3. `rule_versions` — ทุกกฎที่ใช้ในการ run นี้ (rule ID + version + effective date)
    4. `stage_results` — แต่ละ stage: input count → output count → exclusion reasons (ถ้ามี)
    5. `evidence_references` — evidence records ที่ถูกใช้ในการประเมิน
  - **ทุก Candidate ใน queue — บันทึก explanation ที่ประกอบด้วย:**
    1. `candidate_id` — ticker
    2. `theme_membership` — อยู่ใน Theme อะไรบ้าง
    3. `stage_trajectory` — ผ่าน/ไม่ผ่าน แต่ละ stage + เหตุผล
    4. `assessment_summary` — CQ, ER, DC results (dimensions แยกกัน)
    5. `rule_lineage` — กฎ version ไหนที่ใช้กับ Candidate นี้
  - **Reproducibility:** input เดิม + rule versions เดิม = output เดิมเสมอ — audit record พิสูจน์ได้
- **Affected Artifact(s):** PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md; All pipeline stages; Audit infrastructure
- **Decision Category:** Other (Explainability, Audit)
- **Materiality:** Material — determines whether pipeline outputs are independently verifiable
- **Status:** Approved
- **Resolution:** RESOLVED — per-run audit record + per-Candidate explanation; reproducibility guaranteed
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** Pipeline run metadata; stage inputs and outputs; rule versions; evidence references
- **Required Output States:** Audit record per run; explanation per Candidate; traceability from output → rule → evidence
- **Required Explainability:** Contract นี้กำหนดว่า explainability ต้องมีอะไร — ทุก queue decision trace ได้
- **Missing-Data Question:** Stage ที่ run ไม่ได้เพราะ missing data → audit record บันทึกเหตุผล
- **Conflicting-Evidence Question:** Audit record แยก conflict จาก absent data
- **Point-in-Time Question:** Audit record บันทึก evaluation timestamp + rule versions
- **Dependencies:** DS-513 (Rule Lifecycle — pending, for rule version linkage); all pipeline stage slots
- **Alternatives to Evaluate:** Evaluated by Founder — minimum audit + explanation contract for V0
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-6-QUEUE-v0.1
- **Verification Evidence:** Founder approved explainability and audit contract in session

---

### Decision Slot: DS-511 — Stock-First Discovery Path Preservation

- **Identifier:** DS-511
- **Topic:** Design constraints the V0 pipeline must satisfy to avoid precluding future stock-first discovery (screening Candidates independent of Theme membership), per §4.4
- **Decision Obligation Source:** ALPHA-MOMENTUM-V0-SPEC §4.4: "Future Alpha Momentum versions must preserve the ability to: discover candidates through stock-first screening independent of Theme membership; enrich stock-first candidates with Theme context after discovery; combine Theme-linked and stock-first discovery paths"
- **Inherited Approved Semantics:** Future versions must preserve stock-first discovery capability. V0 is a Theme-linked demonstration boundary, not the permanent architecture. This requirement is explicit approved rule content
- **Rule Content Authority:** ALPHA-MOMENTUM-V0-SPEC §4.4 — for the requirement to preserve future stock-first capability. Founder-provided rule — for the V0 architectural constraints
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (Extension Point, Not Dual Path in V0):**
  - **V0 ตอนนี้:** Pipeline เป็น Theme-linked — Candidate ต้องมี Theme ถึงเข้าได้ (DS-308: Filter) นี่คือ demonstration boundary ตาม §4.4
  - **สิ่งที่ต้องทำเพื่อไม่ให้ V0 ปิดประตู V1+:**
    1. **Stage 1 (Universe Definition) ต้องทำงานแยกจาก Theme โดยสมบูรณ์** — Universe stage ต้องไม่รู้ว่า Theme คืออะไร, ไม่ query Theme, ไม่ filter ด้วย Theme — มันแค่คืนรายชื่อหุ้นทั้งหมดใน universe (ตาม DS-309/DS-310) ไม่ว่า หุ้นพวกนั้นจะมี Theme หรือไม่
    2. **Stage 2 (Theme Context) เป็นจุดเดียวที่ filter ด้วย Theme** — ใน V1+ เราสามารถเพิ่มเส้นทางขนานที่ข้าม Stage 2 หรือใช้ Stage 2 แบบ enrichment แทน filter ได้ โดยไม่ต้องรื้อ Stage 1, 3, 4, 5, 6
    3. **Stage 3–6 (CQ, ER, DC, Queue) ต้องทำงานได้โดยไม่ขึ้นกับ Theme** — stages พวกนี้ใช้ข้อมูล Candidate โดยตรง — ถ้าใน V1+ Candidate ไม่มี Theme, stages พวกนี้ยังทำงานได้ตามปกติ (แค่ส่วน TQ ใน Candidate Strategy View จะแสดง "No Theme")
  - **สรุป:** V0 pipeline architecture มี "extension point" ก่อน Stage 2 — จุดที่ stock-first path จะเสียบเข้าในอนาคตได้ โดย architecture ของ stages อื่นไม่ต้องเปลี่ยน
  - **นี่ไม่ใช่ investment rule — เป็น architectural constraint** เพื่อให้เป็นไปตาม §4.4
- **Affected Artifact(s):** PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md; Alpha Momentum pipeline architecture; future V1+ pipeline design
- **Decision Category:** Other (Architecture Constraint)
- **Materiality:** Material — determines whether V0 design closes off required future capability
- **Status:** Approved
- **Resolution:** RESOLVED — Universe stage แยกจาก Theme โดยสมบูรณ์; Theme filter อยู่ที่ Stage 2 เท่านั้น; Stage 3–6 ทำงานได้โดยไม่ต้องมี Theme
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** Current V0 pipeline stage design; DS-308 (Theme Context classification); understanding of stock-first screening requirements
- **Required Output States:** 3 architectural constraints: (1) Universe stage must operate independently of Theme, (2) Theme filtering isolated to Stage 2, (3) downstream stages must function without Theme context
- **Required Explainability:** How each V0 pipeline decision preserves or constrains the stock-first path
- **Missing-Data Question:** Not directly applicable
- **Conflicting-Evidence Question:** Not directly applicable
- **Point-in-Time Question:** The stock-first path must also support point-in-time evaluation
- **Dependencies:** DS-502 (Theme Context stage behavior); DS-308 (Theme Context classification — resolved as Filter)
- **Alternatives to Evaluate:** Evaluated by Founder — extension-point approach chosen as simplest way to satisfy §4.4 without building dual-path in V0
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-4-ARCHITECTURE-v0.1
- **Verification Evidence:** Founder approved extension-point architectural constraint in session

---

### Decision Slot: DS-512 — Logical Stage Dependencies and Input/Output Contracts

- **Identifier:** DS-512
- **Topic:** What each pipeline stage requires and produces; logical dependencies between stages; deterministic evaluation requirements; how missing or empty inputs propagate. Covers what were previously separate stage contract (DS-217), intermediate empty-state (DS-216), and execution concerns
- **Decision Obligation Source:** ALPHA-MOMENTUM-V0-SPEC §4.1 defines stages and their logical sequence. DESIGN-PLAN.md §7 identifies stage contracts as material. Physical execution parallelism is deferred to architecture/implementation planning
- **Inherited Approved Semantics:** The six pipeline stages exist in a defined logical sequence. Each has a described purpose. Deterministic execution is required. This slot addresses logical dependencies and deterministic evaluation requirements, not physical runtime scheduling
- **Rule Content Authority:** Founder-provided rule — this decision
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (Linear Pipeline with Explicit I/O Contracts):**
  - **6 stages เรียงตามลำดับ — แต่ละ stage รับ output จาก stage ก่อนหน้า, ส่ง output ให้ stage ถัดไป:**
    ```
    [Universe] → [Theme Context] → [Candidate Quality] → [Entry Readiness] → [Data Confidence] → [Queue Assembly]
    ```
  - **Contract แต่ละ Stage:**
    1. **Universe Definition (Stage 1):** 
       - **รับเข้า:** Asset inventory, DS-309 universe rules, DS-310 eligibility criteria
       - **ส่งออก:** รายชื่อ Candidate ทั้งหมดใน universe (ยังไม่กรองด้วย Theme)
       - **กฎ:** Universe stage ต้องไม่รู้จัก Theme (per DS-511 — preservation constraint)
    2. **Theme Context (Stage 2):**
       - **รับเข้า:** รายชื่อ Candidate จาก Stage 1, Candidate–Theme relationship data, Approved Theme list
       - **ส่งออก:** รายชื่อ Candidate ที่มี Theme ≥ 1 (DS-308: Filter) พร้อม Theme context ที่โยงไว้
       - **กฎ:** Candidate ไม่มี Theme → ถูกคัดออก; หลาย Theme → เก็บทุก Theme
    3. **Candidate Quality (Stage 3):**
       - **รับเข้า:** รายชื่อ Candidate จาก Stage 2, CQ dimension data (5 domains จาก DS-301)
       - **ส่งออก:** Candidate แต่ละตัวพร้อม CQ assessment (ตาม DS-304 grouped output)
       - **กฎ:** ประเมินทุก Candidate ที่ผ่าน Stage 2; ถ้าประเมินไม่ได้ → "Not Assessed"
    4. **Entry Readiness (Stage 4):**
       - **รับเข้า:** รายชื่อ Candidate จาก Stage 3, ER dimension data (4 domains จาก DS-302)
       - **ส่งออก:** Candidate แต่ละตัวพร้อม ER assessment (ตาม DS-305 grouped output)
       - **กฎ:** เหมือน Stage 3 — ประเมินทุกตัว; ไม่ได้ → "Not Assessed"
    5. **Data Confidence (Stage 5):**
       - **รับเข้า:** รายชื่อ Candidate จาก Stage 4, DC assessment data (DS-401–DS-412)
       - **ส่งออก:** Candidate แต่ละตัวพร้อม DC assessment ระดับ Candidate (per DS-412)
       - **กฎ:** แสดง DC dimensions แยกกัน ไม่ roll-up; ไม่มี gate — DC เป็นข้อมูล ไม่ใช่ filter
    6. **Queue Assembly (Stage 6):**
       - **รับเข้า:** Candidate ทั้งหมดจาก Stage 5 พร้อม assessments ครบทั้ง 4 มิติ
       - **ส่งออก:** Research Queue — Theme-first (กลุ่มตาม Theme), ภายใน Theme เรียงตาม... (DS-507 ยัง unresolved)
       - **กฎ:** Adaptive capacity (DS-508 — unresolved), อาจ return empty queue (DS-509 — unresolved)
  - **Missing/Empty Input Propagation:** ถ้า stage ก่อนหน้าส่ง empty list มา → stage ถัดไปส่ง empty list ต่อไป — ไม่พัง, ไม่ generate ข้อมูลปลอม
  - **Deterministic:** ทุก stage ต้องทำงานแบบ deterministic — input เดิม + rule version เดิม = output เดิมเสมอ
- **Affected Artifact(s):** PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md; All pipeline stage implementations
- **Decision Category:** Other (Data Contract)
- **Materiality:** Material — determines what data flows between stages
- **Status:** Approved
- **Resolution:** RESOLVED — linear 6-stage pipeline; explicit I/O contract per stage; empty input propagates as empty output
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** Resolved stage classification decisions; quality dimension output specifications
- **Required Output States:** I/O contract per stage per specification above; empty/missing input → propagate flag
- **Required Explainability:** Contract documented; traceable per pipeline run
- **Missing-Data Question:** Stage ได้ input ที่มี missing data → assess เท่าที่ทำได้, flag สิ่งที่ missing → ส่งต่อให้ stage ถัดไป
- **Conflicting-Evidence Question:** Stage ได้ input ที่มี conflicting data (e.g., DC conflict records) → preserve conflicts, ส่งต่อ
- **Point-in-Time Question:** ทุก stage output มี evaluation timestamp + rule version กำกับ
- **Dependencies:** DS-501–DS-506 (stage-specific operational decisions — still unresolved; contracts reference expected future resolutions); RULE-PACK and DATA-CONFIDENCE output specifications (resolved)
- **Alternatives to Evaluate:** Evaluated by Founder — linear contract approach chosen for V0 simplicity
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-4-ARCHITECTURE-v0.1
- **Verification Evidence:** Founder approved 6-stage linear pipeline I/O contracts in session

---

### Decision Slot: DS-513 — Rule Lifecycle, Version, Authority, and Effective-Date Contract

- **Identifier:** DS-513
- **Topic:** Canonical cross-cutting contract for rule lifecycle, versioning, authority, and effective-date semantics. Canonical owner: Pipeline artifact. All other Gate A artifacts reference this slot rather than creating duplicate lifecycle/version decisions
- **Decision Obligation Source:** DESIGN-PLAN.md §8 requires stable artifacts with versioned amendment processes. DESIGN-PLAN.md §11 requires every rule to trace to its Rule Content Authority. DOMAIN-ARCHITECTURE §5 requires versioning for material transformations. No operational rule-lifecycle contract is supplied
- **Inherited Approved Semantics:** Material rules must be versioned. Amendments require named approvals. Rule authority must be traceable. The operational contract for rule identifiers, version semantics, effective dates, supersession, retirement, and evaluation-time rule-version selection is not supplied
- **Rule Content Authority:** Founder-provided rule — this decision
- **Unresolved Operational Question:** RESOLVED — see Resolution below
- **Resolution — Founder Decision (Every Rule Has Identity + Version):**
  - **ทุกกฎในระบบต้องมี metadata ต่อไปนี้:**
    1. `rule_id` — unique identifier (เช่น DS-301, DS-407)
    2. `version` — version string (เช่น `v0.1`, `v1.2`)
    3. `authority` — Rule Content Authority (Founder, Constitution §X, EVIDENCE-MODEL §Y, etc.)
    4. `approval_reference` — named approval (เช่น `AM-V0-FIRST-DECISION-GROUP-v0.1`)
    5. `effective_from` — วันที่กฎนี้เริ่มมีผล
    6. `supersedes` — ถ้าเป็น version ใหม่ → ชี้ไป version เก่า
    7. `status` — `active`, `superseded`, `retired`
  - **เวลา pipeline run — ใช้กฎ version ที่ active ณ evaluation timestamp:**
    - Pipeline run วันที่ 15 มิ.ย. 2025 → ใช้กฎที่ `effective_from <= 2025-06-15` และยังไม่ superseded ณ วันนั้น
    - ถ้ามีกฎ version ใหม่ effective 1 ก.ค. 2025 → run วันที่ 15 มิ.ย. ไม่ใช้ version ใหม่
  - **Version numbering:** ใช้ format `v{major}.{minor}` — major เปลี่ยนเมื่อ material, minor เปลี่ยนเมื่อ clarification
  - **ห้าม:** เปลี่ยนกฎโดยไม่เปลี่ยน version, ใช้กฎที่ยังไม่ approved, ลบกฎเก่าโดยไม่มี tombstone
- **Affected Artifact(s):** PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md (canonical owner); referenced by all Gate A artifacts; all rule outputs
- **Decision Category:** Other (Governance Contract)
- **Materiality:** Material — determines whether rules have deterministic version identity and traceable authority
- **Status:** Approved
- **Resolution:** RESOLVED — ทุกกฎมี rule_id, version, authority, effective_from; evaluation-time version selection
- **Founder Decision Required:** Yes — completed
- **Required Inputs:** Existing versioning requirements from DESIGN-PLAN.md and DOMAIN-ARCHITECTURE; rule-authority hierarchy
- **Required Output States:** Rule lifecycle contract: identity, versioning, authority tracing, effective-date semantics
- **Required Explainability:** For any rule output: rule_id, version, authority reference, effective status, contract version
- **Missing-Data Question:** Rule output ที่อ้างอิงกฎที่ retired → audit record บันทึกเป็น "rule retired — output may be stale"
- **Conflicting-Evidence Question:** กรณีมีกฎ 2 versions active พร้อมกัน (ผิดปกติ) → flag conflict, ใช้ version ล่าสุด
- **Point-in-Time Question:** Evaluation-time rule-version selection is this slot's core concern
- **Dependencies:** DS-510 (Explainability — resolved)
- **Alternatives to Evaluate:** Evaluated by Founder — simple identity + version contract for V0
- **Known Risks if Deferred:** No longer applicable — resolved
- **Approval Reference:** AM-V0-WAVE-6-QUEUE-v0.1
- **Verification Evidence:** Founder approved rule lifecycle and versioning contract in session

---

## 3. Conditional Templates

Templates are not active decisions. They carry TPL- identifiers and are instantiated with unique DS identifiers only when DS-507 selects an ordering-dependent output form.

### Template: TPL-PIPELINE-WITHIN-THEME-ORDERING — Within-Theme Candidate Ordering Policy

- **Template ID:** TPL-PIPELINE-WITHIN-THEME-ORDERING
- **Purpose:** Conditional contract for within-Theme Candidate ordering. Instantiated with a unique DS identifier through later named authorization only if DS-507 selects an ordering-dependent output form
- **Required fields per instantiation:** Ordering policy (what dimensions inform ordering, without proposing concrete sort keys); tie-behavior reference; explainability requirements
- **Status:** Template — not an active decision

### Template: TPL-PIPELINE-THEME-LEVEL-ORDERING — Theme-Level Ordering Policy

- **Template ID:** TPL-PIPELINE-THEME-LEVEL-ORDERING
- **Purpose:** Conditional contract for Theme-level ordering. Instantiated only if DS-507 selects an ordering-dependent output form requiring Theme ordering
- **Required fields per instantiation:** Ordering policy (what dimensions inform Theme ordering); tie-behavior reference
- **Status:** Template — not an active decision

### Template: TPL-PIPELINE-TIE-BEHAVIOR — Tie Behavior Policy

- **Template ID:** TPL-PIPELINE-TIE-BEHAVIOR
- **Purpose:** Conditional contract for tie behavior. Instantiated only if DS-507 selects an ordering form that creates tie cases
- **Required fields per instantiation:** Tie resolution policy (without proposing concrete tie-breaker rules); fallback behavior when all resolution methods are exhausted
- **Status:** Template — not an active decision

---

## 4. Inherited Controls

### Higher-Authority Escalation

- **Source:** DESIGN-PLAN.md §13; AGENTS.md authority hierarchy
- **Rule:** Same as documented in RULE-PACK-AND-QUALITY-CONTRACTS.md §4. Applicable to any pipeline decision that would change or narrow higher authority
- **Status:** Inherited approved governance control

### Contradiction Visibility (Presentation Layer)

- **Source:** EVIDENCE-MODEL §7
- **Rule:** Contradictions must remain visible. Human-facing presentation belongs to Gate C
- **Status:** Inherited approved rule

---

## 5. Deferred and Future-Gate Topics

### Deferred Beyond Gate A

| Topic | Old ID | Rationale |
|---|---|---|
| Stage Execution Order and Parallelism | DS-215 (old) | Physical execution parallelism is a runtime scheduling concern. Deferred to architecture/implementation planning after Gate D. Gate A addresses logical dependencies and deterministic evaluation requirements only (DS-512) |

### Moved to Future Gate C (No Identifier Assigned)

| Topic | Old ID | Rationale |
|---|---|---|
| Theme Card and Research Queue Relationship | DS-218 (old) | Presentation/human-review-flow decision. Natural owner is Gate C artifact THEME-CARD-AND-HUMAN-REVIEW-FLOW.md per DESIGN-PLAN.md §4. No Gate C identifier assigned — requires separate Gate C drafting authorization |
| Human-Facing Empty-State Presentation | — (split from old DS-208) | UI wording, page layout, visual prominence, near-miss display, display order. Gate A operational contract (DS-509) covers output state, reason categories, lineage, and downstream behavior. Presentation belongs to Gate C |
| Human-Facing Contradiction Visibility and Display | — (split from old DS-113) | Gate A data-layer detection and preservation is DS-405. Human-facing display and presentation belongs to Gate C |

---

## 6. Slot Supersession Map

This artifact's v0.1-draft contained 18 decision slots (DS-201–DS-218). Full cross-artifact supersession details are in TRACEABILITY-AND-DECISION-REGISTER.md.

| Old ID | Disposition | Reference |
|---|---|---|
| DS-201 | Merged and superseded by | DS-501 (references DS-309 for boundary) |
| DS-202 | Merged into | DS-308 (canonical — in Rule-Pack artifact; this artifact references DS-308 via DS-502) |
| DS-203 | Superseded by | DS-503 |
| DS-204 | Superseded by | DS-504 |
| DS-205 | Superseded by | DS-505 |
| DS-206 | Superseded by | DS-506 |
| DS-207 | Superseded by | DS-508 |
| DS-208 | Superseded by | DS-509 (operational contract); human-facing presentation split to Gate C |
| DS-209 | Superseded by template | TPL-PIPELINE-WITHIN-THEME-ORDERING (conditional on DS-507) |
| DS-210 | Superseded by template | TPL-PIPELINE-THEME-LEVEL-ORDERING (conditional on DS-507) |
| DS-211 | Superseded by template | TPL-PIPELINE-TIE-BEHAVIOR (conditional on DS-507) |
| DS-212 | Merged into | DS-510 |
| DS-213 | Merged into | DS-510 |
| DS-214 | Superseded by | DS-511 |
| DS-215 | Deferred beyond Gate A | Architecture/implementation planning (no identifier) |
| DS-216 | Absorbed into | DS-512 (stage contracts handle empty-output propagation) |
| DS-217 | Absorbed into | DS-512 (merged into logical stage dependencies and contracts) |
| DS-218 | Moved to Gate C | No identifier assigned |

---

## 7. Verification Requirements

- All 13 active slots are Approved. Pipeline artifact: 13/13 complete. 🎉 GATE A COMPLETE.
- No slot proposes prohibited content
- Every slot carries Decision Obligation Source, Inherited Approved Semantics, Rule Content Authority, and Unresolved Operational Question
- DS-509 limits scope to operational contract; human-facing presentation belongs to Gate C
- DS-510 separates logical explainability/audit content from Gate C presentation
- DS-513 is the only canonical Rule Lifecycle/Version/Authority/Effective-Date decision
- No DS identifiers reused from old range
- No Gate C identifiers assigned
- Templates are conditional on DS-507 and carry TPL- identifiers
