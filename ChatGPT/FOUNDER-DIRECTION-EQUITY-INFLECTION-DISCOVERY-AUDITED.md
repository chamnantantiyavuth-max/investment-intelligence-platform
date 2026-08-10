# FOUNDER DIRECTION — EQUITY INFLECTION DISCOVERY
## Preserve the AI-Native Research Organization. Do NOT Rebuild the Old IIP Platform.

Repository:  
https://github.com/chamnantantiyavuth-max/investment-intelligence-platform.git

---

## 0. READ THIS AS A DIRECTION REVIEW, NOT AN IMPLEMENTATION REQUEST

Do not modify code, governance, role contracts, prompts, workflows, blog UI, schemas, or existing research artifacts yet.

First inspect the CURRENT authoritative state of the repository and reconcile this direction against:

- AGENTS.md
- PROJECT_STATE.md
- current Founder Decisions
- the research-organization reconstitution
- Radar Scout contracts
- current Equity Alpha Analyst contracts
- current research workflow
- current Research Blog / reports contract
- current O'Neil / Minervini references, if still authoritative
- FD #74 and FD #75 history
- FD #62 onward relating to reports/blog
- FD #63–68 relating to research analytical freedom
- FD #71 Radar Scout
- FD #87 and the latest full-company research pilot
- every Founder Decision, amendment, and current-state update AFTER FD #87, if any

FD #87 is a known checkpoint, not a ceiling. Do not assume it is still the latest decision when this direction is read. Do not guess the next FD number. Resolve the actual current authority chain first.

Because this repository has gone through several architectural reversals, DO NOT infer current behavior from old module names, old pipeline code, old screenshots, or superseded specifications.

Establish CURRENT TRUTH from the authority hierarchy before proposing any change. If current authoritative documents conflict with any historical reference in this direction, report the conflict rather than silently choosing one.

---

## 1. WHY THIS DIRECTION EXISTS

The Founder previously rejected the original IIP platform model.

The failure was not primarily technical.

The failure was intellectual.

The software platform imposed too much structure on the research process:

- fixed fields
- rigid analytical sections
- checklists
- scores
- pass/fail classifications
- dashboards
- predetermined analytical dimensions
- pipeline-driven output

AI researchers gradually optimized for filling fields rather than understanding the investment.

The resulting work looked complete but often lacked:

- original reasoning
- causal explanation
- deep business analysis
- intellectual narrative
- prioritization of what actually matters
- disagreement between specialists
- genuine investment insight

The Founder therefore changed IIP into an:

**AI-Native Investment Research Organization**

whose primary product is:

**deep written research published through the Research Blog**

rather than an investment-analysis dashboard.

The governing doctrine remains:

> **STRUCTURE THE OPERATIONS, NOT THE THINKING.**

We may structure:

- discovery
- task intake
- ownership
- evidence handling
- review
- audit
- provenance
- version history
- publishing
- monitoring

We must NOT structurally dictate how an analyst thinks or writes the research essay.

This principle is non-negotiable.

---

## 2. CURRENT RESEARCH ORGANIZATION — PRESERVE IT

The current research organization is conceptually correct and should NOT be replaced.

The intended research flow is approximately:

```text
Radar Scout / Founder / Material Event
            ↓
       Task Idea Card
            ↓
         CoS Triage
            ↓
      Research Mandate
            ↓
    Small Research Cell
            ↓
  Independent First Passes
       (anti-anchoring)
            ↓
      Evidence Build
            ↓
   Lead Analyst Deep Work
            ↓
     Main Research Essay
            ↓
     Cross Examination
            ↓
      CRO Opposing Thesis
            ↓
           Audit
            ↓
         Re-audit
            ↓
  IC Secretary / Synthesis
            ↓
      Founder Review
            ↓
      Research Blog
```

The exact sequence should follow the latest authoritative repository rules if they differ slightly.

Important:

**Do not rebuild this workflow as a software pipeline.**

The workflow coordinates people/agents and quality control.

It does not prescribe an analytical template.

---

## 3. THE NEW IDEA

The Founder now wants to add a systematic method for discovering interesting EQUITY research candidates.

This is NOT a return to the old Alpha Momentum platform.

It is NOT a new investment platform.

It is NOT a portfolio-management system.

It is NOT a buy/sell engine.

It is a:

### Research Discovery Protocol

working title:

**Equity Inflection Discovery**

Its purpose is:

> Detect companies where underlying earnings power may be changing **before or during the earliest phase of market recognition**, then surface only the most interesting cases for disciplined research intake into the existing free-form research organization.

Conceptually:

```text
BUSINESS INFLECTION
        +
MARKET RECOGNITION
        ↓
RESEARCH CANDIDATE
        ↓
WHY IS THIS HAPPENING?
        ↓
CHANGE-DRIVER / CATALYST RECON
        ↓
FULL COMPANY RESEARCH
```

---

## 4. FOUNDER'S INITIAL EQUITY SPEC

The Founder's initial intuition is:

### A. Earnings Inflection

Find companies where the latest quarterly earnings show an unusually important breakout or acceleration relative to approximately the previous two years.

The original idea was:

> Latest quarterly EPS breaks above the earnings range of the prior two years.

However, do NOT blindly hard-code this literal definition yet.

The design must consider:

- seasonality
- base effects
- buyback-driven EPS growth
- tax effects
- one-off gains
- accounting changes
- acquisition effects
- cyclical peak earnings

The signal should capture genuine **Earnings Power Inflection**, not merely a mechanically higher reported EPS number.

Potential evidence may include:

- quarterly EPS YoY growth acceleration
- TTM / normalized EPS breakout
- revenue confirmation
- gross/operating margin direction
- cash conversion sanity
- guidance change
- estimate revisions

These are candidate design inputs, NOT yet approved production formulas.

#### Separate the signal hypotheses

Do NOT conflate:

1. **EPS-level breakout** — the absolute or normalized earnings level reaches a new multi-period high; and
2. **EPS-growth-rate acceleration** — the rate of year-over-year earnings growth itself accelerates or breaks above its prior range.

They are different hypotheses and may behave differently. Design and validate them separately before deciding whether they should be combined.

#### Earnings-data semantics must be explicit

Before implementation, define what the scanner means by "EPS" and how it handles:

- GAAP diluted EPS vs adjusted/non-GAAP EPS
- fiscal-quarter seasonality
- stock splits and corporate actions
- restatements
- discontinued operations
- acquisitions and divestitures
- large tax items
- share-count changes and buybacks
- low-base and negative-base effects
- industries where EPS is an incomplete primary signal

Do not silently substitute adjusted figures for reported figures. If multiple earnings definitions are used, preserve the source and transformation lineage.

Some company types may require a different economic measure or may need to be excluded from the first version if the signal is not economically meaningful. Do not force one EPS formula across every business model merely to maximize universe coverage.

Do not invent thresholds.

---

### B. Stage Eligibility

The Founder wants only:

- Stage 1
- Early Stage 2

and wants to exclude:

- mature / late Stage 2
- Stage 3
- Stage 4

The intellectual reason is important:

The Founder is NOT simply trying to buy strong stocks.

The objective is to detect the transition:

> **Business Inflection → Pre-Recognition / Early Market Recognition**

before the opportunity becomes widely mature, crowded, or heavily extended.

Interpretation:

- **Stage 1** is primarily a **pre-recognition / watch** state: the business may be changing before price discovery is complete.
- **Early Stage 2** is primarily an **early-recognition / priority-candidate** state: both business evidence and market recognition may be beginning to align.

Stage 1 and Early Stage 2 should NOT necessarily receive the same treatment.

Proposed research-capacity logic:

```text
Earnings Inflection + Stage 1
          ↓
Watch / CoS triage
          ↓
Possible bounded Change-Driver Recon

Earnings Inflection + Early Stage 2
          ↓
Priority CoS triage
          ↓
Bounded Change-Driver Recon
          ↓
Possible Full Deep Research Mandate

Mid/Late Stage 2
          ↓
Normally no new full research mandate

Stage 3 / 4
          ↓
Excluded from this discovery protocol
```

This is proposed logic for review, not authorization to implement.

---

### C. Change-Driver / Catalyst Recon — "What Changed?"

Once a stock survives the discovery screen, the next question must NOT be:

> "Is this a good momentum stock?"

The question should be:

> **What changed in the underlying economics of this company?**

Potential catalysts include:

- new product
- new platform
- new customer
- new capacity
- new market
- pricing power
- market-share shift
- margin inflection
- competitor failure
- regulatory change
- policy change
- supply constraint
- management change
- operating leverage
- distribution change
- analyst estimate revisions
- structural industry change
- emerging Theme

The Change-Driver / Catalyst Recon should determine whether the earnings inflection appears:

- structural
- cyclical
- temporary
- accounting-driven
- financial-engineering-driven
- macro-driven
- genuinely company-specific
- multi-causal / not reducible to one catalyst

**"No identifiable single catalyst" is a valid result.** Never manufacture a catalyst, narrative, or theme merely to complete the workflow.

This recon is a bounded research-intake step, not a miniature Full Company Analysis. It should answer only enough to judge whether scarce deep-research capacity is warranted.

---

### D. Point-in-Time Integrity — Mandatory for Discovery and Validation

The discovery system must be point-in-time honest.

Historical validation and any future production scan must use only information that was actually available at the scan timestamp.

Mandatory protections include:

- use the earnings release / filing availability timestamp, not merely the fiscal period end date
- preserve revision and restatement history where material
- adjust price history for corporate actions with documented methodology
- define a point-in-time investable universe to avoid survivorship bias
- prevent future constituents, future delistings, or future classifications from leaking backward
- prevent revised fundamentals from being used before their publication date
- preserve source, timestamp, transformation, and feature-version lineage for every deterministic signal
- explicitly test for look-ahead bias, survivorship bias, and data-vendor revision leakage

A backtest that cannot prove point-in-time availability is not admissible evidence for calibration.

---

## 5. CRITICAL ARCHITECTURE — THE INTELLECTUAL FIREWALL

This is the most important design requirement.

There must be a hard conceptual boundary between:

### DISCOVERY

and

### RESEARCH

```text
┌──────────────────────────────────────────┐
│       STRUCTURED DISCOVERY SIDE          │
│                                          │
│  deterministic / objective where useful │
│                                          │
│  Earnings Inflection                     │
│  Stage classification                    │
│  data / liquidity sanity                 │
│  optional enrichment signals             │
│                                          │
└───────────────────┬──────────────────────┘
                    │
             Candidate Signal
                    │
                    ▼
               Radar Scout
      signal/provenance sanity only
                    │
                    ▼
              Task Idea Card
                    │
                    ▼
                 CoS Triage
                    │
════════════════════╪══════════════════════
      INTELLECTUAL FIREWALL
════════════════════╪══════════════════════
                    │
                    ▼
       Equity Research Intake Recon
      bounded Change-Driver / Catalyst
                    │
          ┌─────────┴─────────┐
          │                   │
      weak/unclear       material/interesting
          │                   │
     Watch/Archive             ▼
                       Neutral Big Question
                               │
                       Full Research Mandate
                               │
                       Small Research Cell
                               │
                    Independent First Passes
                               │
                         Evidence Build
                               │
                         Deep Analysis
                               │
                       Cross Examination
                               │
                       CRO Opposing Thesis
                               │
                            Audit
                               │
                          Synthesis
                               │
                         Founder Review
```

**Above the firewall: structure is useful.**

**Below the firewall: analytical freedom governs.** A bounded intake recon may exist, but it must not become a fixed company-analysis template or pre-decide the research conclusion.

Never allow scanner fields to become the structure of the final research essay.

---

## 6. O'NEIL / MINERVINI — CORRECT ROLE

The Founder is attracted to O'Neil because O'Neil is not simply technical momentum.

The useful concepts include:

- earnings acceleration
- sales confirmation
- "N" / meaningful new catalyst
- relative strength
- leadership
- institutional accumulation
- price-volume confirmation
- constructive base structure

Minervini contributes particularly useful concepts around:

- stage analysis
- early Stage 2
- avoiding deteriorating stages
- contraction / base quality
- avoiding late or extended entry structures

### Start with a minimal discovery core

Do not recreate a full CAN SLIM checklist by default.

The first design should distinguish:

**Core eligibility candidates**
- Earnings Inflection
- Stage Eligibility
- data / liquidity sanity

**Possible enrichment / prioritization evidence**
- relative strength
- price-volume behavior
- institutional activity
- estimate revisions
- industry leadership
- market regime
- base quality / contraction
- other O'Neil / Minervini observations

An enrichment signal must not silently become a hard gate merely because it exists in a historical methodology. Promote it to a hard gate only after explicit Founder approval supported by evidence.

**Theme context should default to enrichment, not eligibility.** A company may be discovered stock-first before the market has assigned a popular theme or narrative to the change. Theme membership must not become a hidden prerequisite unless separately re-approved.

### Legacy Rule Pack — concepts only, not wholesale inheritance

If the repository still contains the historical O'Neil / Minervini Rule Pack, reuse only concepts, definitions, and deterministic features that remain useful.

Do NOT automatically inherit its:

- historical entry rules
- historical exit rules
- 7–8% stop-loss rules
- position-sizing rules
- market-regime veto
- Approved-Theme gate
- old lifecycle state machine
- old conviction framework
- legacy thresholds
- automated scoring assumptions

unless each item is separately reviewed and re-approved for this new research-discovery purpose.

However:

**O'Neil / Minervini should be a DISCOVERY LENS, not the intellectual constitution of company research.**

The fact that a company entered research through a momentum/inflection signal must NOT create a presumption that:

- the company is good
- the catalyst is durable
- the stock is attractive
- the valuation is reasonable
- the thesis is correct

Momentum provides evidence that:

> "Something may be happening."

Research must independently determine:

> "What is actually happening, why, whether it is durable, who captures the economics, and what could make the thesis wrong?"

---

## 7. VERY IMPORTANT — AVOID RESEARCH ANCHORING

The Research Mandate should remain neutral.

BAD mandate:

> "Explain why XYZ is a great momentum stock after its earnings breakout."

This anchors the research cell toward confirmation.

BETTER mandate:

> "XYZ displayed an unusual earnings inflection while its price structure remained in a base or transitioned into an early advancing stage. What changed in the underlying economics, is the change durable, and does the available market evidence represent genuine recognition of improvement or merely a temporary, cyclical, accounting, or narrative effect?"

Momentum is the reason the company reached the research desk.

It is NOT the research conclusion.

The full research cell should receive a **neutral mandate plus necessary provenance**, not a pre-solved scanner narrative. Do not auto-load a large discovery checklist, ranking score, CAN SLIM scorecard, or historical rule-pack conclusions into independent first passes. Preserve the discovery data in the audit trail, but do not let it pre-structure the analysts' reasoning.

---

## 8. RADAR SCOUT — PRESERVE ROLE BOUNDARY

Do NOT turn the Radar Scout into an Equity Analyst.

The Radar Scout should remain a discovery function.

If this direction is approved, its relationship to equity discovery may be approximately:

```text
Equity Inflection Scanner / data process
              ↓
         Radar Scout
              ↓
signal/provenance sanity + why unusual
              ↓
        Task Idea Card
              ↓
          CoS Triage
              ↓
 Equity Alpha / designated research lead
              ↓
bounded Change-Driver / Catalyst Recon
```

**Radar does not own Catalyst Recon.** Once the work requires explaining company economics, identifying a durable change driver, or evaluating whether an observed signal is structural versus cyclical/accounting-driven, ownership has crossed into research and should move to the Equity Alpha Analyst or another explicitly scoped research lead.

Radar still:

- raises questions
- identifies unusual situations
- preserves source/time provenance
- recommends research questions

Radar must NOT:

- write the investment thesis
- decide whether the company is high quality
- recommend buying
- assign capital
- perform the final company analysis

Consider whether the scanner itself should be deterministic software/data logic rather than LLM reasoning.

Numerical calculations such as:

- EPS growth
- moving averages
- relative strength
- stage-related deterministic features
- volume statistics

should generally not depend on an LLM when they can be reproducibly computed.

AI should interpret, investigate, and form questions around the signals.

The scanner has **no authority** to create a Full Research Mandate, approve a company, or force research capacity consumption. It surfaces candidates. Radar packages the observation. CoS triages. Research ownership begins only after an explicit handoff.

---

## 9. FULL COMPANY DEEP RESEARCH — DO NOT TURN IT INTO A CHECKLIST

Once a candidate is admitted into Full Company Research, the existing Analytical Freedom Doctrine remains fully active.

The analyst must be free to discover the explanatory structure of the company.

Useful analytical lenses may include:

- business model
- industry structure
- competitive advantage / moat
- unit economics
- earnings quality
- balance sheet
- management
- capital allocation
- reinvestment runway
- market-share dynamics
- catalyst durability
- valuation / embedded expectations
- key risks

But:

> **Analytical lenses are not mandatory article headings.**

Example:

If customer concentration is the controlling issue, the analyst may devote much of the essay to it.

If the key insight is an obscure bottleneck in the value chain, follow it.

If valuation is not currently knowable with adequate evidence, say so.

If moat analysis contributes little to the actual question, do not force three pages of moat commentary.

Main research output must remain:

**a coherent analytical essay**

rather than:

**a completed form.**

### Free-form narrative, bounded evidentiary responsibility

Analytical freedom does NOT mean permission to omit a material issue.

The main essay may choose its own structure, emphasis, and causal framing. Reviewer-side QA must still ask whether any material dimension was ignored without justification.

The standard is:

> **Free-form narrative, bounded evidentiary responsibility.**

If a conventional lens is immaterial, the analyst may omit it. If it is material, the analysis must address it somewhere — not necessarily under a mandatory heading.

---

## 10. CHECKLISTS — QA ONLY

Internal checklists are allowed and useful in:

- Data Steward workpapers
- Quant validation
- source/provenance review
- evidence appendices
- audit
- final quality control

They must NOT become the main article structure.

Never produce a Founder-facing company report that looks primarily like:

```text
Earnings: PASS
Moat: HIGH
Management: GOOD
Valuation: MEDIUM
Momentum: STRONG
Risk: MEDIUM
Overall Score: 83/100
```

unless the Founder separately requests such a reference table.

Classification must remain subordinate to explanation.

---

## 11. BLOG — PRESERVE REPORTS-AS-PRODUCT

Do NOT rebuild momentum dashboards or company-analysis screens.

The Blog remains the primary Founder-facing research product.

The preferred content families should eventually support concepts such as:

- Company Research
- Equity Inflection / Discovery
- Products & Commodities
- Themes & Macro
- Intelligence Updates
- Weekly Intelligence

Exact taxonomy is a design decision to review later.

Do NOT implement UI changes yet.

Individual ticker names such as AAPL / NVDA should scale as:

- search
- subject
- company series

rather than permanent top-level navigation items.

Discovery artifacts do not automatically deserve publication. A Task Idea Card, Change-Driver Recon, or rejected candidate may remain an internal workpaper when it lacks standalone research value. Publication is an editorial/research judgment, not a workflow completion requirement.

---

## 12. DO NOT PUBLISH EVERY SCREEN HIT

The Research Blog must remain curated intelligence, not a database dump.

Illustrative funnel:

```text
5,000+ US equities
       ↓
40–60 screen hits
       ↓
10–15 genuinely interesting situations
       ↓
4–8 catalyst-supported candidates
       ↓
1–3 Full Deep Research mandates
       ↓
High-quality published work
```

Numbers above are illustrative only.

Do NOT treat them as approved thresholds.

Screen output could potentially appear as one curated periodic note, for example:

**"Equity Inflection Radar — Week of YYYY-MM-DD"**

rather than dozens of low-value individual articles.

Do not optimize the organization for report count, screen-hit count, conversion rate to publication, or artificial weekly output. Silence and archived candidates are valid outcomes.

---

## 13. COMPANY RESEARCH SERIES

A useful long-term knowledge history might become:

```text
COMPANY XYZ
│
├── Discovery Note
├── Catalyst Investigation
├── Full Company Deep Analysis
├── CRO Opposing Thesis
├── Earnings / Material Change Update
├── Thesis Revision
└── Postmortem / Invalidation
```

Not every step must become a public Blog article. Some steps may remain internal research workpapers. What matters is preserving the evolution of knowledge:

- when we noticed the company
- what triggered attention
- what we initially believed
- what research discovered
- what contradicted the thesis
- what later changed
- what we got wrong

Do not silently rewrite history.

---

## 14. "WHY THIS REACHED OUR DESK"

Momentum/discovery information may appear briefly in the company article.

Example:

> "XYZ reached the research desk after quarterly earnings showed an unusual two-year inflection while price remained in a constructive base or transitioned into an early advancing phase. Revenue and margins broadly supported the signal. The research mandate was to determine whether this reflected a durable change in earnings power or merely a temporary, cyclical, accounting, or financial-engineering effect."

That may be enough.

Do NOT let scanner metrics dominate the research essay.

---

## 15. DO NOT REVIVE THE OLD PLATFORM

Unless explicitly authorized in a later Founder Decision, DO NOT create:

- Momentum Dashboard
- Company Score Dashboard
- CAN SLIM Score
- O'Neil Score
- Moat Score
- weighted investment score
- pass/fail company pipeline
- fixed company-analysis form
- 15 mandatory research sections
- mandatory agent-by-agent report sections
- automated buy/sell recommendation
- broker integration
- allocation logic
- position sizing logic
- portfolio-aware research
- automatic Full Research Mandates triggered solely by a scanner hit
- wholesale inheritance of legacy O'Neil / Minervini entry, exit, stop-loss, Theme-gate, or scoring logic

Do not route the research essay through old Alpha Momentum / FO UI schemas.

Legacy calculation/data code may be reusable as infrastructure if appropriate.

Legacy architecture must not regain authority over research thinking.

---

## 16. RELATIONSHIP TO CLOSE SYSTEM RESEARCH

Preserve the Radar Scout's broad opportunity-discovery mission.

This equity direction should exist alongside, not replace:

- commodity research
- Close System product research
- macro research
- theme research
- options/volatility research
- event-driven research

The Radar Scout is a broad opportunity monitor.

Equity Inflection Discovery is ONE input stream into Radar/research intake.

Do not redefine the entire Radar around equities.

---

## 17. RESEARCH CAPACITY MATTERS

Full-company research is expensive because proper work may involve:

- independent specialist views
- primary filings
- transcripts
- quantitative reconstruction
- competitive research
- industry work
- cross-examination
- CRO opposing thesis
- audit
- rework
- Founder review

Therefore discovery must protect scarce research capacity.

Stage 1 should usually have a higher bar before receiving full research than a well-supported Early Stage 2 inflection.

"Interesting" does not automatically mean "research everything."

---

## 18. REQUIRED FIRST-PASS DELIVERABLE — NO IMPLEMENTATION

Before proposing code changes, produce:

### A. CURRENT-TRUTH RECONCILIATION

Explain the current authoritative IIP model after all recent reversals.

Explicitly identify:

- what is active
- what is frozen
- what is legacy but still present
- what is superseded
- what FD #75 currently prevents
- whether any decision after FD #87 changes this known checkpoint
- current Radar Scout behavior
- current Equity Research behavior
- current full-company research capability
- current Blog architecture

Cite exact repo files / Founder Decisions.

### B. FIT-GAP

Compare this Founder Direction with current behavior.

Classify each item:

- ALREADY EXISTS
- EXISTS BUT INACTIVE
- CONFLICTS WITH CURRENT FD
- SMALL AMENDMENT
- NEW CAPABILITY REQUIRED
- SHOULD NOT BE BUILT

### C. MINIMUM-CHANGE DESIGN

Propose the smallest architecture change necessary to add Equity Inflection Discovery while preserving:

- Analytical Freedom
- Radar boundaries
- existing deep-research workflow
- Reports-as-Product
- Blog architecture
- portfolio blindness
- audit/history

Prefer reuse over architecture expansion.

### D. FOUNDER DECISION DRAFT

Draft a new Founder Decision that explicitly supersedes FD #75 only to the minimum degree necessary.

Do NOT erase or rewrite FD #74/#75 history.

The new FD should establish:

> Equity Inflection Discovery is authorized as a research-intake capability, not as a revival of the old IIP investment platform.

Include explicit Anti-Regression Guardrails against the checklist-platform failure.

### E. EARNINGS-INFLECTION DESIGN OPTIONS

Propose 2–3 alternatives for defining Earnings Inflection.

Compare:

- signal quality
- false positives
- seasonality
- data requirements
- backtestability
- simplicity

Do not choose arbitrary thresholds without evidence.

### F. STAGE DESIGN OPTIONS

Propose how Stage 1 / Early Stage 2 / Late Stage 2 / Stage 3 / Stage 4 could be defined reproducibly.

Explicitly identify which components can be deterministic and which require interpretation.

### G. CHANGE-DRIVER / CATALYST-RECON CONTRACT

Define a bounded Change-Driver / Catalyst Recon output that is enough to decide whether a candidate deserves a Full Research Mandate without becoming a miniature Full Company Analysis.

Explicitly define ownership. Radar may package the signal and research question, but company-economic interpretation should move to Equity Alpha or another scoped research lead.

"No identifiable single catalyst" must be a valid outcome.

### H. RESEARCH-MANDATE CONTRACT

Propose a neutral Big Question format that prevents momentum-origin anchoring.

### I. BLOG IMPACT

Explain what, if anything, eventually needs to change in the Blog taxonomy.

Prefer no UI change unless clearly necessary.

### J. VALIDATION & SHADOW-PILOT PLAN

Before permanent implementation or threshold hardening, propose a bounded validation plan.

It must include:

- point-in-time historical validation using only information available at each historical timestamp
- explicit tests for look-ahead bias, survivorship bias, revision leakage, and corporate-action handling
- separate validation of EPS-level breakout and EPS-growth-rate acceleration hypotheses
- shadow runs on current data before converting provisional rules into standing production behavior
- false-positive review: what kinds of companies/signals repeatedly look interesting but fail deeper investigation?
- missed-opportunity review: what important inflections would the design have failed to surface?
- research-capacity load: how many candidates would reach CoS / Equity Recon per cycle?
- stability/sensitivity: does a small threshold change radically alter the candidate set?
- data-quality failure behavior and honest empty-output behavior

Do NOT judge the discovery protocol solely by forward stock returns after a signal.

Its primary objective is **research-discovery quality**: whether it reliably surfaces a manageable number of genuinely information-rich situations that justify further investigation.

Any return analysis is secondary evidence and must not convert this research-intake system into a trading-system backtest by stealth.

---

## 19. SUCCESS TEST

The redesign succeeds if:

1. We systematically discover companies experiencing meaningful business inflections.
2. We avoid wasting deep-research capacity on thousands of ordinary companies.
3. We use market recognition as evidence, without allowing price action to substitute for company analysis.
4. O'Neil / Minervini improve discovery without controlling the final research conclusion.
5. Research essays remain free-form, causal, opinionated, evidence-grounded, and intellectually independent.
6. CRO can still disagree completely.
7. Auditor can still block unsupported claims.
8. Founder reads an actual investment-research essay — not a checklist.
9. Blog remains the product.
10. No old IIP platform disease returns.
11. A scanner hit never automatically becomes a research mandate, investment thesis, or publication.
12. Historical validation remains point-in-time honest and resistant to survivorship/look-ahead leakage.

---

## 20. FINAL PRINCIPLE

Remember:

> **The scanner surfaces what may deserve attention.**
>
> **Radar packages and recommends; CoS decides what receives research-capacity consideration.**
>
> **The research team decides what it means.**
>
> **The Founder decides what to do with the knowledge.**

And:

> **STRUCTURE THE DISCOVERY.**
>
> **PRESERVE THE THINKING.**
>
> **KEEP DECISION AUTHORITY HUMAN-GATED.**

Start with repository inspection and CURRENT-TRUTH reconciliation.

Do not implement until the Founder reviews the fit-gap, minimum-change design, and new FD draft.
