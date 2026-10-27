# QAD Challenge, Audit, Underwriting, Publication, Monitoring, Knowledge & Evaluation Contract

> **Contract:** M3-09 (M3 Domain Contract Set — combines M3-09 and M3-10 from lean spec)
> **Status:** M3 FINAL — FROZEN FOR M4 DERIVATION
> **Authority:** FD #130; Constitution §23 (AI Operating Constitution); CAP-009 (CIW ABSORB: Cross-Exam, audit); CAP-016 (REUSE: Audit Infrastructure); CAP-014 (REUSE: Thai Editorial Standard); FD #94 (Publication Firewall); FD #96 (Category/Library structure)
> **Traceability:** CONSTITUTION-§23 · CAP-009 (CIW: Cross-Exam/CRO) · CAP-014 (REUSE: Thai Editorial) · CAP-015 (REUSE: Live Office monitoring) · CAP-016 (REUSE: Audit Infrastructure) · CAP-017 (REUSE: Evidence Doctrine) · FD #94 · FD #96 · EVIDENCE-DOCTRINE · NEW_M3_DERIVATION (Red Team charter, Underwriting verdict states, Monitoring protocol, Evaluation typology)

---

## 1. Four Separate Functions

```text
STRUCTURAL RED TEAM     — Assume the thesis is wrong. Construct the strongest value-trap case.
INDEPENDENT AUDITOR     — Verify source/citation/PIT/calculation integrity. May block FOUNDER_READY.
CHIEF UNDERWRITER       — Synthesize all analysis into a research verdict.
PUBLICATION             — Transform research into Thai long-form journalism.
```

No function may be combined with another in the same logical role (Separation of Duties).

---

## 2. Structural Red Team

### 2.1 Mission

> **Assume the QAD thesis is wrong and the market may be correct.**

The Structural Red Team constructs the strongest structural/value-trap case against the primary thesis. It does NOT attempt to be "fair" or "balanced" — it argues the opposing side as forcefully as the evidence allows.

### 2.2 Charter

| Field | Value |
|-------|-------|
| **Assumption** | QAD thesis is WRONG |
| **Default Position** | Impairment is STRUCTURAL, not temporary |
| **Burden** | Construct the case that quality is absent, impairment is permanent, or valuation is already fair |
| **No Veto** | Red Team findings cannot veto the thesis — they are carried forward to Underwriting |
| **Final Outcome** | `ACCEPTED` / `PARTIALLY_ACCEPTED` / `REJECTED_WITH_EVIDENCE` / `UNRESOLVED` |

### 2.3 Required Analysis

The Red Team must address at minimum:

1. **Against Quality** — Is quality assumption wrong? Moat absent? Returns not durable?
2. **Against Temporary** — Why is the impairment structural, not temporary?
3. **Against Recovery** — What makes recovery unlikely even if impairment is temporary?
4. **Against Management** — What management failures make recovery improbable?
5. **Against Valuation** — Why is the current price fair or cheap for a reason?
6. **For Market Correctness** — What does the market see that the thesis misses?
7. **Hidden Risks** — Unknown unknowns, balance-sheet risks, regulatory, legal, technological
8. **Cost of Being Wrong** — What is the permanent loss if the Red Team is right?

### 2.4 Red Team Independence

- Red Team must have NO prior involvement in the research or thesis creation
- Red Team must not have participated in evidence gathering for this case
- Red Team's output is preserved verbatim alongside the final underwriting verdict
- The Research Director cannot dismiss or suppress Red Team findings

---

## 3. Independent Audit

### 3.1 Mission

Verify the integrity of the research record. The auditor checks what EXISTS, not whether it is correct.

### 3.2 Audit Checklist

| Check | What Is Verified | Pass/Fail |
|-------|------------------|-----------|
| Source Existence | Every cited source exists and is accessible | |
| Original-Source Inspection | Every material fact is traced to original source (not secondary) | |
| Citation Correctness | Every citation points to the correct source, page, and context | |
| PIT Integrity | As-of dates are correct; no post-AS_OF_DATE evidence used without tagging | |
| Calculation Reproducibility | Every derived calculation can be independently reproduced | |
| Contradiction Preservation | All contradictory evidence is preserved, not suppressed | |
| Model Provenance | AI model, version, provider recorded for every AI-generated output | |
| Self-Review Separation | No person/role reviewed their own work | |
| Publication Gates | Required gates (Red Team, Audit) completed before FOUNDER_READY | |

### 3.3 Audit Authority

| Authority | Detail |
|-----------|--------|
| **May block FOUNDER_READY** | If audit fails, case cannot reach Founder |
| **Does not decide the thesis** | Audit checks process, not substance |
| **May call for recalculation** | If calculation cannot be reproduced |
| **May call for source verification** | If source cannot be found |
| **Records all findings** | Audit report is part of the permanent case record |

### 3.4 Audit Outcomes

| Outcome | Meaning | Next Action |
|---------|---------|-------------|
| **PASS** | All checks pass with no material findings | Case proceeds to Founder |
| **PASS_WITH_FINDINGS** | Pass with minor, non-blocking findings | Findings recorded; case proceeds |
| **FAIL** | One or more blocking findings | Case blocked; must be resolved before FOUNDER_READY |

---

## 4. Chief Underwriter

### 4.1 Mission

Synthesize all analytical work, challenge, and audit into a final research verdict.

The Chief Underwriter reads and weighs:
- Quality Analysis (M3-06)
- Industry Economics (M3-06)
- Financial Reconstruction (M3-08)
- Management Assessment (M3-06)
- Dislocation Reconstruction (M3-07)
- Impairment Diagnosis (M3-07)
- Recovery Model (M3-07)
- Normalized Economics (M3-08)
- Valuation / Reverse DCF (M3-08)
- Structural Red Team findings (§2)
- Independent Audit report (§3)

### 4.2 Research Verdict States

| State | Meaning |
|-------|---------|
| **QAD_CONFIRMED** | All four propositions (Quality + Dislocation + Impairment + Valuation) are supported by evidence. High confidence in temporary impairment. |
| **QAD_PROBABLE** | Most evidence supports QAD thesis but material uncertainty remains. |
| **QAD_UNRESOLVED** | Cannot reach verdict — material evidence gaps or the diagnosis is genuinely ambiguous. |
| **NOT_QAD_STRUCTURAL** | Impairment is structural, not temporary. The business or industry is permanently damaged. |
| **NOT_QAD_QUALITY** | Quality assumption is wrong — the business was never high-quality. |
| **NOT_QAD_VALUATION** | The price already reflects the impairment (fair or unattractive even at this level). |

### 4.3 Chief Underwriter Forbidden Actions

| Forbidden | Why |
|-----------|-----|
| Choose its own cases | Selection Engine maintains separation |
| Allocate capital | Portfolio management is external |
| Size positions | No investment authority |
| Execute trades | No broker connectivity |
| Overrule Red Team findings | Red Team findings are preserved, not vetoed |
| Ignore contradictory evidence | All evidence must be weighed |

### 4.4 Underwriting Output

The full underwriting output includes:

1. Research Verdict (one of six states)
2. Synthesis narrative (why this verdict over alternatives)
3. Scenario weightings (subjective assessment of each scenario's likelihood)
4. Key uncertainties ranked by materiality
5. Thesis-specific monitoring indicators
6. Recommendation to Founder (advisory — does not equal endorsement)

---

## 5. Publication

### 5.1 Mission

Transform the research record into one coherent, **free-form Thai Google Doc**, stored in the case's private IIP/QAD Google Drive folder. **The old `/library`/blog destination is retired for new QAD reports by the Founder's 2026-10-18 instruction.** The Editor chooses narrative arrangement based on evidence; do not mandate a template. This affects the presentation/delivery channel only, not underlying QAD evidence, Red Team, audit, underwriting or Founder decisions.

### 5.2 Publication States

| State | Meaning |
|-------|---------|
| **RESEARCH_COMPLETE** | Research is done; publication not yet written |
| **FOUNDER_READY** | Publication written, Red Team completed, Audit passed — ready for Founder review |
| **FOUNDER_ENDORSED** | Founder explicitly agrees with thesis (recorded as FD) |
| **FOUNDER_DISAGREES** | Founder disagrees with thesis (recorded as FD) |
| **FOUNDER_REJECTS** | Founder rejects thesis entirely (recorded as FD) |

**Never** `FOUNDER_ENDORSED` unless Founder explicitly acts. The system does not self-declare endorsement.

### 5.3 Publication Rules (per FD #94 Thai Editorial Standard)

- Thai language (per FD #92 — Thai research content unless Founder specifies English)
- No internal governance jargon (RM/ORG/FD/spec/§/workspace/audit-status/portfolio-blind) in reader-facing content (FD #94)
- The strongest opposing thesis remains equally accessible in the main free-form Doc or a linked companion Google Doc; no forced article slug/category/frontmatter
- Deliver the Doc in a stable PRIVATE Google Drive case folder, with a private case-to-Doc link
- PDF is optional export when requested, not canonical truth or a prerequisite to Founder reading

### 5.3.1 IIP Thai Writing & Editorial Standard — Organization-Wide, Founder-Adopted (2026-10-18)

**Status: STANDING EDITORIAL STANDARD, effective for every future Founder-facing Thai narrative deliverable.** This is not a UNH-specific rewrite and not another report-format template. Applies to all 26 IIP Research Bots whenever they write Founder-facing Thai analytical prose, including QAD essays, summaries, valuation explanations, opposing theses, updates and Google Docs. It also applies to the Thai Editor's synthesis of their work. It does **not** change canonical schemas, source quotations, machine-readable outputs, direct technical handoffs or internal test artifacts.

**Desired reading experience:** Precise institutional research explained with the clarity, conceptual progression and natural language of an excellent Thai nonfiction book: *readers understand the argument without having to decode machine-translated jargon, an audit log, or a list of specialist outputs*. The Founder's positive benchmark is the **explanatory clarity** of a prior Thai summary of *The Selfish Gene*, **not its fixed structure or an instruction to imitate a particular author's prose**.

**Binding writing principles (quality of thought, not mandatory report headings):**

1. **Think in Thai; do not translate sentence by sentence from English.** Use idiomatic, contemporary, professional Thai in connected paragraphs. Avoid unnatural loan-translation, vague buzzwords, stiff bureaucratic language, metaphorical filler, sales language and habitual repetition. Write directly and respectfully, never patronizingly.
2. **Reason before listing.** Explain the real question, what happened, why it matters, the economic or causal mechanism, what the evidence does and does not show, and where the argument might fail. This is a reasoning expectation, **not** a mandatory paragraph order, chapter checklist or 6-section formula.
3. **Guide the reader from familiar to difficult.** Introduce an unfamiliar analytical term through its meaning and economic consequence before using an acronym. Keep the original English in parentheses once when it improves accuracy; use a consistent natural Thai expression afterward. Do not force ambiguous translations (for example, translating financial `underwriting` into a literal insurance-related phrase) when a short contextual explanation is clearer.
4. **Use numbers as evidence, not prose substitutes.** Lead with the implication; show only decision-relevant numbers and denominators in the main argument, explain period, basis and comparator, and then interpret what they mean. Put long peer comparisons, formulas, raw figures, method details and traceability in meaningful tables, links or appendices. **Never discard or alter important values, model assumptions or caveats to improve readability.**
5. **One coherent authorial voice.** Integrate specialist findings into an original, flowing explanation, with natural transitions and proportionate paragraph length. Do not publish stitched Bot notes, one-heading-per-agent sections, a chain of status labels, dozens of microheadings, or machine-generated scorecard prose. Use bullets/tables only when they improve comprehension.
6. **Calibrated certainty without a visible audit log.** Keep `VERIFIED`, `UNVERIFIED`, unresolved hypotheses, unsupported inferences and material conflicts truthful in canonical IIP records. A verified quotation proves only that the text was stated, not that the issuer's explanation is correct. In Founder-facing prose, use at most a **brief DRAFT/as-of status line** plus plain-language disclosure of any material limitation; flag a specific uncertain assumption or unresolved contradiction **where it changes the thesis**. Do not front-load assurance-process explanations, flood prose with status labels, repeat raw verification counts, or require a catalogue of methods and hashes. Cite material claims concisely and accurately; full source/PIT/claim/audit lineage stays accessible in the internal research records, not mandatory reading for the Founder.
7. **Present the strongest contrary interpretation fairly.** Do not bury adverse evidence, uncertainties, assumptions, flaws or thesis killers. Write the objection in intelligible Thai, show why it matters and how it might change the conclusion. Avoid false certainty or invented symmetry.
8. **Analytical freedom is preserved.** The writer may choose emphasis, order, narrative approach, headings, length, examples and voice according to the case. No fixed 42-heading outline, mandated word count, standard introduction, fixed scorecard, article slug/frontmatter or imposed "house template." Short and penetrating is preferable to long and repetitive; deep work is still deep when brevity fits the evidence.
9. **Keep presentation separate from authority.** The Editor can restructure, reword, eliminate repetition, move data to appendices and clarify implications **without inventing research, changing facts, changing underwriting judgments or promoting evidence**. New material analysis goes back to its authorized research owner; actual contradictions or numerical mismatch remain visible. Preserve the existing Red Team, Audit, Underwriting and Founder decisions.
10. **Write for the iPhone reader as well as the serious investor.** Use spacious but restrained native Google Docs typography and fluent Thai narrative. The **Master Plan § "Founder reading comfort & narrative rhythm — 2026-10-27"** supplies adaptable starting defaults (Thai-friendly 12 pt body, ~145% line spacing, ~8 pt paragraph spacing, proportionate heading whitespace). These are practical layout defaults, **not content quotas or a new approval gate**. Separate genuine shifts of thought into readable paragraphs without turning every sentence into a disconnected line. Improve comfort with whitespace **instead of filler prose**, generic intros, repeated explanations or decorative headings. Use simple, useful headings/tables; preserve substantive analytical depth and actual caveats. PDF is optional, and native Google Docs remains the reading source.

**Reader Understanding Contract (all companies, all sectors; Founder amendment 2026-10-19) — define the reader's understanding, NEVER report headings.** Assume the Founder is an intelligent investor **who has never encountered this particular company or its industry**. The report must build the minimum correct mental model **before** relying on specialized figures or arguing over a narrow impairment. For a substantive company investment case, an unfamiliar reader should be able to explain, in their own words:

- **What the business actually does and how money moves:** real products/services and buyers, who pays whom, relevant company/subsidiary/segment relationships, how revenue turns into cash and economic profit, the important costs and incentives, and what operating metrics mean. Where useful, one simple economic example can be more informative than many acronyms.
- **Why it has (or lacks) quality and a moat:** the actual mechanism of advantage, evidence that customers/suppliers/competitors cannot easily erode it, industry structure and the situations in which the purported moat would fail. Never assume a famous name is a quality business.
- **How the business arrived at today's dislocation:** its operating and capital-allocation history, normalized performance versus the recent deterioration, relevant events and the plausible competing causes. Establish a chronology only when it materially helps distinguish cyclical/temporary problems from permanent impairment.
- **What the evidence implies for durable earning power:** segment/unit economics, material risks and dependencies, what could recover, what may be permanently lost, what is fact versus management claim, assumption or inference, and which observations would disprove the preferred thesis.
- **What matters to an investor at the current price:** the key valuation drivers, expectations already priced in, credible upside/downside and uncertainty, including the strongest contrary case, with decision-relevant numbers interpreted rather than dumped.

These are **five comprehension outcomes, NOT a five-part table of contents, checklist, minimum page count or required sequence**. The author is free to teach the company through a story, a business walkthrough, historical case, customer economics, opposing arguments or another coherent structure. Industry-specific mechanisms determine emphasis: e.g. healthcare reimbursement/provider networks; software retention and switching costs; banks' funding/credit; commodities' cost curves. Omit immaterial details and avoid encyclopedic company profiles. **Depth is proportional to scope:** a rapid-discovery/watchlist note need only supply enough business orientation to justify screening and clearly name what remains unresearched; a substantive Full QAD thesis must support the outcomes above where material. Never invent missing explanations to manufacture completeness.

**Research-to-editor ownership:** Research Director ensures that the minimum company/industry economics required to understand the *specific thesis* are researched with original-source support. Relevant Business/Moat, Industry and Financial Specialists supply missing factual context using the existing Evidence Gap flow **only where decision-relevant**. Thai Editor owns the reader's comprehension, transitions, meaningful analogies and integrated narrative, but **cannot add unsupported business facts, infer unsupported causal links or change research decisions**. If essential context is missing, request one bounded targeted research task (or clearly disclose the unknown); do not stop the entire workflow for a decorative background section.

**Living research narrative, not an append-only essay:** Keep immutable source/case/evidence history in the canonical IIP store. In the editable free-form Google Doc, new material findings must update the **current main explanation and affected valuation/uncertainty passages**, not merely accumulate timestamped addenda while old conclusions, stale 'to investigate' statements or outdated data remain in the main storyline. Preserve superseded source-backed work in the existing private case history/working records or a clearly linked archive when needed; **do not automatically reproduce the full historical research log as a giant appendix in the Founder-facing Doc**. Reconcile only passages **actually affected** by new evidence; do not rewrite the entire report at every update. When substantive information conflicts, expose the remaining disagreement rather than smoothing it away.

**Founder reading-experience standard (2026-10-27; ALL companies and all Founder-facing IIP narratives):** The **main deliverable is an investment research explanation, not the institution's internal evidence or governance report**. Spend reader attention primarily on the company, its economics, history, moat, dislocation, sustainable earning power, the strongest countercase, and valuation at a clearly dated price. Every substantial paragraph should help the Founder understand the business or make an investment judgment. Explain source or method details in the narrative **only if essential to interpret a significant figure or limitation**. Use selective, accurate source links on material claims; keep raw IDs, sha256, source-by-source audit ledgers, repetitive `VERIFIED/UNVERIFIED` labels, Bot handoffs, review chronology, lengthy governance glossaries, and obsolete drafts in internal records or opt-in supporting material rather than the primary report. Keep a concise truthful DRAFT/as-of notice and plainly disclose **material** unverified assumptions, uncertainty and unresolved objections; **never conceal caveats or imply verification/approval that did not occur**. Readers must be able to follow the thesis without opening footnotes, yet independently trace material evidence when needed. Keep supporting tables/appendices only if they earn their place by illuminating economics or the investment decision. Preserve the existing original-source, point-in-time, evidence-verification, Red Team, Independent Audit, Underwriting and Founder authorization requirements **in the workflow**. This is an editorial separation of audiences, not a relaxation of standards. Do not create a new publication gate, fixed report template, review package, mandatory footnote density, or mass retrospective rewrite.

**Zero-extra-gate comprehension check:** As part of the Thai Editor's already-required single editorial read, ask: *Can a smart first-time reader explain how this company earns money, why it may be advantaged, what broke, what can recover, and why valuation does or does not compensate for the risk?* If not, repair the smallest missing explanatory bridge using already-supported evidence or flag a material research gap. This check is **editorial work inside the existing handoff**, not a scoring rubric, approval layer, mandatory research re-run or an additional reviewer.

**Lightweight editorial self-check — not a new approval layer:** Before delivery, the Thai Editor reads at least the opening, one dense analytical passage and the conclusion as uninterrupted Thai prose. Fix obvious calques/awkward transitions, explain technical terms, connect data to its significance and ensure source/uncertainty references remain truthful. Re-read additional passages only if the same problem recurs. Do not demand a language score, automatic word-count/heading thresholds, a second editorial committee or iterative review loops. An already-reviewed research report **does not** require new research merely because its Thai prose is polished.

**Example of tone, not a reusable template:** Replace `UNH ไม่ได้ถอยพื้นที่อย่างผิดสัดส่วนตาม plan-county pairs แต่เบี้ยโดดเด่น` with `ข้อมูลเบื้องต้นไม่ได้ชี้ว่า UnitedHealth ถอนตัวจากพื้นที่มากกว่าคู่แข่งอย่างชัดเจน แต่บริษัทกลับขึ้นเบี้ยประกันในสัดส่วนของแผนที่สูงกว่ารายอื่น สิ่งที่ต้องหาคำตอบต่อจึงไม่ใช่เพียงว่าบริษัทลดขนาดลงเท่าไร แต่เหตุใดลูกค้าจึงตอบสนองต่อการปรับราคาแตกต่างจากคู่แข่ง`. Preserve appropriate citations and uncertainty qualification where this example is used with actual data.

### 5.4 Companion Publication

For every main QAD thesis, a companion publication should be produced representing the strongest opposing case. The companion should be:

- Explicitly labeled as the opposing interpretation, with material disagreements fairly retained
- Included in the primary Google Doc or visibly linked to a companion Doc in the same private case folder
- Readable alongside the main research argument whenever delivery is authorized; no blog slug or `/library` gate

---

## 6. Thesis Monitoring

### 6.1 Mission

Monitor thesis-specific indicators, not generic news flow. Monitoring follows the thesis wherever it leads — it does not passively watch the company.

### 6.2 Monitoring Indicators

Indicators are defined during underwriting (Chief Underwriter defines what would confirm or refute the thesis):

- **Recovery indicators** — evidence that recovery is occurring as modeled
- **Warning indicators** — signs that recovery is off track
- **Thesis-killer indicators** — specific conditions that would invalidate the thesis

### 6.3 Monitoring States

| State | Meaning |
|-------|---------|
| **RECOVERY_CONFIRMING** | Thesis indicators tracking as expected; recovery on track |
| **ON_TRACK** | Mixed signals but overall thesis direction holds |
| **UNCERTAIN** | Evidence ambiguous; cannot determine direction |
| **WEAKENING** | Evidence points away from thesis; thesis becoming less probable |
| **BROKEN** | Thesis is no longer supported by evidence; should be abandoned |

### 6.4 Monitoring Protocol

- Monitoring is indicator-specific, not company-generic
- No monitoring update = no material change (valid outcome)
- State transitions require evidence, not time
- BROKEN state triggers notification to Founder
- Monitoring does NOT create new research mandates automatically

---

## 7. Knowledge Compounding

### 7.1 Knowledge Admission

```text
Research Finding
    → Candidate Lesson
    → Cross-Case Validation (3+ independent cases)
    → Independent Review (not original researcher)
    → APPROVED KNOWLEDGE
    → Industry Playbook (if industry-specific)
```

A single research case does NOT automatically become institutional knowledge.

### 7.2 Knowledge States

| State | Criteria |
|-------|----------|
| **Research Finding** | Observation from a single case |
| **Candidate Lesson** | Consistent pattern in 2+ cases |
| **Cross-Case Validated** | 3+ independent cases confirm pattern |
| **Independently Reviewed** | Reviewed by different role |
| **APPROVED KNOWLEDGE** | Cross-case + review + Chief Underwriter approval |

---

## 8. Evaluation

### 8.1 Two Separate Questions

```text
Type A — Did we research the discovered company correctly?
    (Research Quality — existing evaluation framework)
    
Type B — Did we fail to discover a material candidate?
    (Discovery Recall — NEW, first-class metric for QAD)
```

### 8.2 Type A — Research Quality Evaluation

Metrics:
- Decision-Changing Evidence Recall — did the research capture evidence that would change the verdict?
- Thesis-killer detection rate
- Contradiction coverage rate
- Citation correctness rate
- PIT correctness rate
- Temporary vs Structural calibration accuracy
- Report factual-error rate

### 8.3 Type B — Discovery Recall Evaluation

Metrics:
- Universe Coverage Rate
- Data-Ready Coverage
- Known-Opportunity Recall
- Quality Candidate Recall
- Dislocation Detection Rate
- Signal-to-Candidate Conversion Rate
- Candidate-to-Research Conversion Rate
- Discovery Cost per New Candidate
- False Positive Rate (Material)
- **Decision-Changing Candidate Recall** (headline metric — how often did we discover candidates that change portfolio-relevant decisions?)

### 8.4 Evaluation Protocol

- Evaluation requires a sealed outcome corpus (hidden until evaluation run)
- Historical evaluation must use point-in-time data only (as-of = evaluation date, not today)
- Pre-AS_OF_DATE evidence only — no forward-looking information
- Separate runs for Type A and Type B may use different PIT snapshots

### 8.5 Threshold Calibration

Quantitative pass/fail thresholds are NOT defined in this contract. They belong in M4B (Evaluation Contract — Part 7), where they are derived from historical data and Founder-approved calibration runs.

**Thresholds invented in M3 are void.**

<!-- 2026-08-19 13:30 UTC+7 -->