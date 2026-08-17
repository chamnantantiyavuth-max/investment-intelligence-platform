# IIP Discovery Recall & Coverage Audit
## Final Hermes Handoff — v1.1

**Status:** Final proposal after three design-review passes  
**Scope:** Upstream opportunity discovery only — from eligible universe/source scanning through Task Idea Card / CoS triage  
**Explicit non-scope:** Deep Research, Gemini Notebook research integration, research writing, publication, and Blog flow are governed separately by `IIP_Gemini_Deep_Research_Final_Handoff_v1.4.md` and existing IIP contracts.

---

# 0. Founder Concern

The Founder does not want IIP to become excellent at deep research while remaining weak at finding what deserves research.

The core concern is:

> If Hermes itself decides that only something it considers “interesting” gets sent forward, how do we know Hermes is not quietly discarding excellent opportunities?

This concern applies to two major discovery domains:

1. **Equities**
2. **Close System products**

The objective of this audit is NOT to force more ideas into research.

The objective is to determine whether IIP has sufficient:

- discovery breadth;
- opportunity coverage;
- recall;
- source coverage;
- data coverage;
- archetype coverage;
- temporal coverage;
- auditability of rejected ideas;
- protection against LLM judgment false negatives.

A high-quality research organization is useless if the right idea never reaches research intake.

---

# 1. Separation From Gemini / Deep Research v1.4

This audit is a separate workstream.

Do NOT merge it into the Gemini Deep Research v1.4 architecture.

Use this boundary:

```text
UPSTREAM DISCOVERY
==================

Universe
→ Data / Sources
→ Deterministic Scanners
→ Radar / Principal Judgment
→ Task Idea Card
→ CoS Triage

        ↓

BOUNDARY

        ↓

DOWNSTREAM RESEARCH
===================

Research Mandate
→ Anti-Anchoring
→ Hermes + Gemini Deep Research
→ Evidence
→ Challenge / CRO / Audit
→ Facts Locked
→ Gemini Thai Editorial
→ Founder
→ Blog
```

This audit ends at the discovery / triage boundary.

It must NOT redesign:

- Deep Research Standing Contract;
- Gemini Notebook workflow;
- Publication Fact Packet;
- Thai editorial workflow;
- Blog publication;
- Facts Locked;
- research-team topology.

If the audit finds a downstream issue, record it as out-of-scope and reference the appropriate workflow.

---

# 2. FIRST ACTION — Inspect Current State

Before proposing or changing anything, inspect the CURRENT repository and current authority hierarchy.

At minimum read:

- `AGENTS.md`
- Constitution / Project DNA
- `operational/FOUNDERS-DECISIONS.md`
- `project-definition/EVIDENCE-MODEL.md`
- `project-definition/CANDIDATE-AND-QUEUE-MODEL.md`
- `project-definition/CLOSE-SYSTEM-PRODUCT-RADAR.md`
- current discovery directory and code
- `discovery/equity_universe.py`
- `discovery/equity_inflection/`
- `discovery/quality_asymmetry/`
- `discovery/cs_product/`
- Radar Scout:
  - `operational/hermes-organization/roles/11-radar-scout/PRINCIPAL.md`
  - `ASSISTANT.md`
- Founder Chief of Staff role contract
- `operational/hermes-organization/KANBAN-CONTRACT-v0.1.md`
- `operational/hermes-organization/kanban/card-outcomes.md`
- recent Radar Digests
- current Cron / monitoring authorizations that affect discovery

Also inspect recent implementation and decision history because documentation and runtime may have evolved at different speeds.

## Important consistency check

Explicitly check for situations where:

- a README says a scanner is shadow-only;
- a later Founder Decision authorizes broader behavior;
- runtime already performs behavior not reflected in the older document;

or vice versa.

Report authority/runtime/documentation drift.

Do not silently reconcile it yourself.

---

# 3. DESIGN REVIEW ONLY FIRST

The first response to this handoff is an AUDIT DESIGN REVIEW.

Do NOT immediately:

- expand the equity universe;
- change scanner thresholds;
- create new Cron jobs;
- change Radar prompts;
- add new discovery archetypes;
- create a Discovery Reservoir;
- create a second queue;
- change CoS authority;
- change Kanban states;
- modify Close System eligibility;
- promote shadow thresholds;
- create a new model-scoring system;
- implement Gemini as a production discovery gate.

First:

1. inspect;
2. map current discovery;
3. identify measurable gaps;
4. propose a bounded audit;
5. identify Founder decisions required;
6. STOP.

Implementation or remediation begins only after explicit Founder approval.

---

# 4. Current Discovery Streams to Audit

The audit must treat each discovery lane separately before evaluating the system as a whole.

## Equity Lane E1 — Radar Scout

Open-ended discovery.

Typical signals:

- unusual filings;
- events;
- policy changes;
- cross-asset divergences;
- anomalous price/volume behavior;
- unusual capital allocation;
- industry changes;
- unexplained developments;
- source contradictions.

Primary risk:

**LLM judgment false negative**

The Radar can see something and decide it is not “interesting enough.”

---

## Equity Lane E2 — Equity Inflection

Deterministic business/earnings inflection discovery.

Audit:

- universe coverage;
- data coverage;
- point-in-time integrity;
- gate-by-gate exclusions;
- historical positive-case capture;
- historical false positives;
- Stage-filter exclusions;
- revenue-confirmation effect;
- detection latency.

Primary risks:

- universe miss;
- detector miss;
- threshold miss;
- data miss.

Do not change approved thresholds during the audit.

---

## Equity Lane E3 — Quality & Asymmetry Discovery

Current lenses include concepts such as:

- Durable Compounder;
- Long-Runway / 100-Bagger;
- Mispriced Quality;
- Asymmetric Value.

Audit whether this stream can surface companies that:

- have no major news;
- have no dramatic anomaly;
- are not in obvious momentum;
- are boring but economically exceptional;
- compound quietly;
- are temporarily misunderstood;
- possess unusual reinvestment economics.

Primary risks:

- universe miss;
- data availability;
- shadow-threshold uncertainty;
- Principal judgment false negative after evidence generation.

Do NOT convert this into one composite “quality score.”

Preserve separate archetypes/lenses.

---

## Close System Lane C1 — Product Discovery

Audit the difference between:

**Approved Close System Product Radar scope**

and

**currently implemented real discovery scope.**

The approved strategy spans categories such as:

- broad-market ETFs;
- sector/thematic ETFs;
- physical commodities;
- fixed income;
- relevant diversified producer / strategic-resource products where authorized.

The current implementation must be measured honestly against the approved scope.

Audit:

- product universe breadth;
- P1 / P2 / P3 coverage;
- intelligence-layer coverage;
- cost-data coverage;
- inventory-data coverage;
- supply/demand coverage;
- macro coverage;
- policy coverage;
- hidden-signal coverage;
- physical-vs-paper coverage;
- data-source reliability;
- products/commodities that currently cannot be evaluated.

Primary risk:

**Spec coverage is much broader than implementation coverage.**

Do not fix this by inventing data or thresholds.

---

# 5. The Audit Is About Recall AND Precision

Do not optimize only for “more cards.”

Two failure modes exist.

## Failure A — Low Precision

```text
Thousands of routine/noisy observations
→ too many cards
→ research capacity wasted
```

## Failure B — Low Recall

```text
Excellent opportunity appears
→ scanner or Hermes dismisses it
→ no card
→ opportunity disappears
```

IIP needs both:

- strong filtering;
- protection against invisible misses.

The current Radar behavior of honestly producing zero ideas when nothing clears the bar is a desirable behavior and must be preserved.

The audit must not create activity for activity's sake.

---

# 6. Absolute Recall Is Not Directly Knowable

Do NOT claim:

> “IIP has 87% opportunity recall.”

There is no known denominator representing every good opportunity in the world.

Instead use explicit **Recall Proxies**.

Required Recall Proxies:

1. Historical Point-in-Time Benchmark Recall
2. Rejected-Item Independent Audit
3. Out-of-Universe Counterfactual Scan
4. Coverage Matrix / Blind-Spot Analysis

Any percentage must clearly identify its bounded benchmark denominator.

Never generalize benchmark recall into universal opportunity recall.

---

# 7. Miss Taxonomy — Mandatory

Every identified discovery failure must be classified by root cause.

Use at least:

## M1 — Universe Miss

The opportunity was never in the scanned universe.

Example:

```text
Excellent company outside current 98-name universe
→ no scanner ever evaluated it
```

## M2 — Data Miss

The asset was in scope, but necessary data was unavailable, stale, inaccessible, or not wired.

Examples:

- missing primary filing;
- blocked commodity feed;
- missing inventory series;
- unavailable cost curve;
- data extraction failure.

## M3 — Detector Miss

The data existed and the asset was scanned, but deterministic logic did not surface it.

Examples:

- inflection signal definition failed to recognize a valid regime;
- Close System pattern set could not represent the opportunity.

## M4 — Judgment Miss

The evidence was surfaced, but Hermes / Principal considered it not interesting enough.

This is the key Founder concern.

## M5 — Cadence / Latency Miss

The discovery system could have found it, but scanned too late.

Measure:

```text
public availability
→ first system observation
→ first evidence block
→ first card
→ CoS triage
```

Do not confuse research latency with discovery latency.

## M6 — Triage Miss

A valid Task Idea Card reached CoS but was rejected, deferred, narrowed, or deprioritized incorrectly.

CoS is a second judgment gate.

Audit it separately from Radar.

## M7 — Authority / Workflow Miss

The opportunity was surfaced but could not progress because:

- authority was unclear;
- an outdated contract blocked it;
- runtime/docs disagreed;
- the lane lacked an authorized packaging path.

---

# 8. Discovery Pipeline Trace

For each lane, build a funnel showing how many items exist at every stage.

Example only:

```text
Universe
  ↓
Successfully fetched
  ↓
Eligible for detector
  ↓
Evidence blocks
  ↓
Principal reviewed
  ↓
Task Idea Cards
  ↓
CoS approved
  ↓
Research Mandates
```

Do NOT focus only on the bottom number.

Record why items leave the funnel.

For deterministic lanes, calculate gate attribution where possible:

```text
excluded by missing data
excluded by eligibility
excluded by signal
excluded by stage
excluded by liquidity
excluded by Principal judgment
excluded by CoS
```

This is essential for locating false negatives.

---

# 9. Audit-Only Capture — No New Canonical State Machine

To audit rejected ideas, the system must temporarily preserve enough information to inspect them.

However, do NOT immediately create a permanent Discovery Reservoir or new Candidate lifecycle.

For the bounded audit, use an **audit-only capture artifact** or existing evidence/audit mechanism.

Capture:

- observed item;
- source;
- timestamp;
- discovery lane;
- detector output;
- disposition;
- disposition reason;
- actor/model where relevant;
- whether sent to card;
- whether sent through CoS;
- later audit verdict.

Suggested audit labels only:

- `SURFACED_HIGH`
- `SURFACED_MAYBE`
- `NOT_PROMOTED`
- `INSUFFICIENT_DATA`

These are NOT canonical Candidate states.

After the audit, determine whether a minimal persistent `Discovery Disposition Log` is actually justified.

Do not build it before evidence of need.

---

# 10. Historical Point-in-Time Benchmark Audit

Purpose:

Test whether the system WOULD HAVE surfaced historically important opportunities using only information available at that time.

## Rules

- no future information leakage;
- use filing/publication timestamps;
- use then-available prices;
- use historical universe membership where possible;
- do not choose only easy winners;
- include negative / near-miss controls;
- include multiple market regimes.

## Equity benchmark categories

Include cases representing different opportunity types:

- earnings inflection;
- durable compounder;
- long-runway growth;
- mispriced quality;
- temporary controversy;
- deep/asymmetric value;
- quiet quality with no headline;
- false-positive exciting story that later failed.

The exact benchmark names and sample size should be proposed during audit design and approved before execution to reduce cherry-picking.

## Close System benchmark categories

Use historically observable episodes such as:

- commodity near production-cost pressure;
- inventory dislocation;
- policy shock;
- fear-driven ETF discount;
- real-yield / fixed-income dislocation;
- commodity supply shock;
- sentiment/fundamental divergence;
- false discounts caused by structural impairment.

Do NOT use the benchmark to retroactively optimize thresholds until every old winner passes.

The goal is diagnosis, not curve-fitting.

---

# 11. Out-of-Universe Counterfactual Audit — Equities

Current shared equity coverage must be tested against eligible names OUTSIDE the current universe.

Purpose:

Answer:

> Is the universe itself causing us to miss companies before discovery even begins?

Create a bounded, stratified external sample from eligible US-listed common stocks / suitable ADRs outside the current universe.

Stratify where practical by:

- size;
- sector/industry;
- age/listing maturity;
- domestic vs ADR;
- profitability profile;
- growth profile.

Run current deterministic discovery logic on the sample where data availability permits.

Measure:

- how many outside names would have generated meaningful evidence;
- how many would have met current scanner conditions;
- which opportunity archetypes are underrepresented in the current universe;
- which market-cap/sector groups are structurally absent.

Do not expand the official universe during the audit.

Use results to justify or reject future expansion.

---

# 12. Rejected-Item Independent Audit

This is the key test for Hermes judgment.

For a bounded sample of items that were:

- surfaced but not promoted;
- judged “not interesting”;
- dropped below Radar card threshold;
- rejected at Principal review;
- rejected/deferred at CoS triage;

perform independent re-review.

## Independence

Where practical, the reviewer should NOT initially see:

- the original disposition;
- the original “not interesting” rationale;
- downstream outcomes.

Give the reviewer the evidence that was available at the original decision time.

Ask:

> Did this evidence justify spending additional low-cost reconnaissance or research capacity?

Possible audit outcomes:

- original rejection well-founded;
- reasonable disagreement;
- probable judgment miss;
- data insufficient;
- cannot determine.

## Reviewer

Use an approved independent context/model consistent with current audit governance.

Gemini may be used as an **audit challenger** for a sample if authorized, but:

- it does not become a production gate;
- it cannot auto-promote anything;
- disagreement triggers review, not override.

The current Internal Auditor / Red Team independence rules remain authoritative.

---

# 13. CoS Triage Audit

Do not stop auditing at Task Idea Card creation.

The Founder concern exists at TWO judgment gates:

```text
Observation
→ Radar / Principal: “interesting?”
→ Card
→ CoS: “worth research capacity?”
→ RM
```

Audit both.

Questions:

- Are high-value but non-dramatic cards disproportionately rejected?
- Does CoS over-prefer urgent/newsworthy issues?
- Does CoS underweight slow compounding or second-order effects?
- Are deferrals later revisited?
- Do WIP/capacity limits create silent permanent misses?
- Are rejected cards preserved with enough rationale for later review?
- Does “not now” become “never” accidentally?

CoS is allowed to protect research capacity.

It should not create invisible historical erasure.

---

# 14. Radar Scout Coverage Audit

Evaluate the open-ended Radar separately.

## A. Source Coverage

Map intended scan domains to actual sources.

Examples:

- SEC / filings;
- macro releases;
- commodity data;
- policy/regulatory;
- news/events;
- cross-asset data;
- price/volume;
- industry-specific sources.

Identify:

- single-source dependence;
- blocked sources;
- sources with long publication lag;
- areas relying heavily on secondary news;
- missing primary feeds.

## B. Temporal Coverage

Measure detection delay.

Examples:

```text
filing published → scanned
macro release → scanned
commodity data published → scanned
material event → card
```

Assess Monday/Thursday cadence and existing event-driven mechanisms.

Do not assume a faster cadence is automatically better.

This is research discovery, not high-frequency trading.

## C. Judgment Coverage

Review what Radar systematically ignores.

Look for biases such as:

- dramatic-event bias;
- headline bias;
- novelty bias;
- large-company familiarity bias;
- narrative salience;
- underweighting boring structural improvement;
- underweighting slow deterioration;
- underweighting second-order beneficiaries;
- underweighting obscure data;
- over-penalizing an incomplete but potentially valuable clue.

The desired Radar question is:

> Is there enough here to justify a question?

not:

> Can I already prove an investment thesis?

---

# 15. Equity Inflection Audit

Audit current production/shadow authority first.

Check for documentation/runtime drift.

Then evaluate:

## Coverage
- percentage of intended universe successfully fetched;
- missing financial histories;
- missing price histories;
- ADR/data edge cases.

## Gate attribution
- H1;
- revenue confirmation;
- Stage;
- liquidity;
- H2 advisory signal.

## Historical recall proxy
Use point-in-time positive and negative cases.

## Sensitivity
Determine which legitimate opportunity types the current definitions cannot see.

Do NOT change thresholds during audit.

Any threshold change requires separate evidence and approval.

---

# 16. Quality & Asymmetry Audit

The purpose of this lane is specifically to catch opportunities Radar and Inflection may miss.

Audit each archetype independently.

Do NOT blend into one score.

Questions:

### Durable Compounder
Can it find excellent businesses without news or earnings acceleration?

### Long-Runway / 100-Bagger
Can it distinguish:
- high ROIC with no runway
from
- high ROIC with reinvestment runway?

### Mispriced Quality
Can it identify temporary impairment without simply rewarding falling price?

### Asymmetric Value
Can it distinguish:
- temporary distress / forced selling / hidden value
from
- permanent impairment / value trap?

Also audit the human handoff:

```text
evidence blocks
→ Equity Analyst judgment
→ Task Idea Cards
```

If many evidence blocks are generated but rejected items have no disposition trail, recall cannot be evaluated.

---

# 17. Close System Coverage Audit — Highest Priority Gap

The Close System audit must begin with a **Spec-to-Implementation Coverage Matrix**.

Rows:

- product categories;
- underlying assets/products;
- P1;
- P2;
- P3;
- Intelligence Layer 1 Macro;
- Layer 2 Policy;
- Layer 3 Cost;
- Layer 4 Supply/Demand;
- Layer 5 Hidden Signals;
- source availability;
- source freshness;
- detector implementation;
- human interpretation path.

Columns may include every currently approved/scannable product class.

## Questions the matrix must answer

- What does the approved spec say Radar should scan?
- What does real discovery actually scan today?
- Which categories have zero production coverage?
- Which assets have identity coverage but no data?
- Which patterns exist in spec but not code?
- Which patterns exist in code but rely on proposed thresholds?
- Which data sources are missing or blocked?
- Which opportunities could not possibly be detected today?

## Critical principle

Close System discovery should prefer:

```text
systematic eligible-universe scan
→ measurable evidence
→ Hermes interprets meaning
```

rather than:

```text
Hermes browses the web
→ asks itself what feels interesting
```

Where signals are measurable, measurement should surface candidates.

Hermes judgment should decide research value and economic meaning, not whether observable data existed.

---

# 18. Close System Universe Audit

Do not assume gold/silver/copper/oil equals the strategy universe.

Compare implementation against approved product taxonomy.

At minimum evaluate current coverage readiness for categories such as:

- broad market ETFs;
- sector/thematic ETFs;
- physical commodities;
- fixed income;
- agricultural commodities where approved;
- strategic minerals/resources where approved.

Do NOT add products merely to make the matrix look complete.

For every potential addition ask:

- P1 eligible?
- reliable product structure?
- sufficient data?
- source licensing/access?
- historical depth?
- measurable P2 evidence?
- measurable P3 evidence?

Coverage claims must be honest.

An unsupported product should be marked:

`NOT EVALUABLE WITH CURRENT DATA`

not treated as neutral.

---

# 18A. Close System Product / Wrapper Coverage

Close System has two distinct discovery questions:

```text
Is the underlying opportunity attractive?
            ≠
Is the chosen investable product/wrapper structurally suitable?
```

The audit must not collapse them.

For each approved product class where applicable, assess whether the wrapper itself introduces material discovery blind spots such as:

- physical vs synthetic exposure;
- tracking difference / tracking error;
- futures roll structure;
- contango/backwardation drag;
- issuer/counterparty structure;
- liquidity / spread;
- AUM / closure risk;
- collateral structure;
- leverage/inverse decay exclusion;
- tax/product mechanics when materially relevant;
- mismatch between underlying commodity thesis and ETF holdings;
- producer-ETF equity/business risk versus physical underlying risk.

Do NOT invent a new suitability score.

Report each relevant dimension separately.

If the underlying opportunity is measurable but no currently approved wrapper can be evaluated reliably, classify that as a **Product / Wrapper Coverage Gap**, not “no opportunity.”

This is especially important because Close System discovery may correctly identify a structural commodity opportunity while the investable implementation vehicle is poor, incomplete, or materially different from the underlying asset.

---

# 19. Data Coverage and Failure Audit

Discovery quality is bounded by data quality.

Build a source/data gap register for the audit.

Classify:

- available/current;
- available/lagged;
- partial;
- secondary-only;
- blocked;
- missing;
- manual/semi-automated;
- not wired.

Examples in Close System may include:

- exchange inventory;
- vault data;
- cost curves;
- lease rates;
- positioning;
- physical premiums;
- EIA;
- LME;
- futures curves;
- ETF flows.

Do not let:

```text
data missing
```

become:

```text
no opportunity
```

Missing data is a Data Miss / uncertainty.

---

# 20. Cross-Lane Overlap and White-Space Map

For equities, create a map:

```text
Opportunity Archetype
→ Radar?
→ Inflection?
→ Quality & Asymmetry?
→ None?
```

Example conceptual archetypes:

- earnings acceleration;
- quiet compounder;
- special situation;
- temporary scandal;
- cyclic recovery;
- hidden asset;
- capital-allocation change;
- regulatory change;
- new product economics;
- second-order beneficiary;
- industry structure shift;
- management change;
- valuation dislocation with stable quality.

The purpose is NOT to invent a scanner for every archetype.

The purpose is to identify **white space**.

White space must be visible before deciding whether to fill it.

---

# 21. Discovery Latency Audit

Measure time from public information to research intake.

For a sample:

```text
T0 = public availability
T1 = system source retrieval
T2 = detector / Radar observation
T3 = Task Idea Card
T4 = CoS triage
T5 = Research Mandate
```

Report separately:

- source latency;
- scan latency;
- judgment latency;
- triage latency.

Do not optimize latency blindly.

For IIP, a slower but accurate research opportunity signal may be acceptable.

However, unexplained multi-day blind windows should be visible.

---

# 22. Precision / Negative-Control Audit

Recall improvements must not destroy precision.

Include negative controls:

- routine filing;
- ordinary insider sale;
- normal earnings release with no change;
- explained market move;
- fashionable narrative with weak evidence;
- commodity price decline caused by structural demand destruction rather than discount.

The system should correctly avoid creating high-priority research noise.

Measure:

- unnecessary evidence escalation;
- unnecessary cards;
- unnecessary CoS load;
- unnecessary research mandates.

---

# 23. Outcome Feedback Audit

The existing Card Outcomes feedback loop is valuable.

Audit whether it captures:

- published;
- folded;
- blocked;
- dropped;
- deferred;
- disproven;
- known-gap;
- re-test trigger.

Critical question:

> Does IIP learn only from ideas that became cards, while learning nothing from ideas rejected before card creation?

If yes, this is a blind spot.

Do NOT immediately build a new permanent system.

First measure its materiality using audit-only rejected-item samples.

---

# 24. Discovery Challenger — Audit Use Only

An independent model may be used to challenge a SAMPLE of rejected items.

Possible question:

> “Given only evidence available at the decision timestamp, identify any item that may have been prematurely dismissed and explain the information value of one additional research step.”

Use this to detect:

- perspective bias;
- salience bias;
- premature certainty;
- missing second-order reasoning.

Rules:

- challenger does not know the original verdict initially where practical;
- challenger does not auto-promote;
- disagreement is not proof Hermes was wrong;
- disagreement creates an audit finding for human/reviewer review.

This is an AUDIT mechanism.

It is not part of Gemini Deep Research v1.4 and not a new production gate.

---

# 25. No Single LLM Irreversible Gate Principle

The audit should evaluate adoption of this principle:

> AI judgment may allocate scarce research attention, but should not make a potentially valuable observation irretrievable without an audit trail.

This does NOT mean every rejected idea becomes a Candidate.

It means the system can answer later:

- what was seen?
- what was rejected?
- why?
- by whom?
- using what evidence?
- was it later shown to be a miss?

The final implementation method should be the minimum needed to achieve this.

---

# 26. Audit Dimensions — Keep Separate

Do NOT collapse the entire discovery system into one weighted score.

Report dimensions separately:

- Universe Breadth
- Source Breadth
- Data Availability
- Recall Proxy
- Precision / Noise
- Detection Latency
- Judgment Sensitivity
- Triage Sensitivity
- Point-in-Time Integrity
- Auditability
- Independence
- Cost / Operational Burden
- Product / Wrapper Coverage (Close System)

Use qualitative audit judgments if needed:

- Strong
- Adequate
- Partial
- Material Gap
- Not Verified

These labels are audit language only, not canonical domain states.

---

# 27. Audit Hypotheses — Test, Do Not Assume

The following are working hypotheses, NOT predetermined conclusions.

## H1
The current equity universe is too narrow to support high-confidence opportunity recall.

## H2
Radar judgment quality is reasonably high precision, but rejected-item recall is unmeasured.

## H3
Equity Inflection reduces LLM judgment risk but remains bounded by universe and detector definitions.

## H4
Quality & Asymmetry is structurally important because it covers quiet opportunities that Radar/Inflection miss, but its shadow status and Principal handoff make recall uncertain.

## H5
Close System real discovery coverage materially lags the approved strategy specification.

## H6
CoS triage is an under-audited second false-negative gate.

## H7
The current outcome feedback loop learns from promoted cards better than from pre-card rejections.

## H8
Close System can correctly identify an underlying opportunity yet still fail at the investable product/wrapper layer.

The audit may confirm, reject, or refine these hypotheses.

---

# 28. Bounded Audit Execution Plan — To Propose for Founder Approval

After FIT-GAP, Hermes should propose a bounded execution package.

A good package will likely contain:

## Workstream A — Architecture / Authority Reconciliation
- current discovery lanes
- current authority
- doc/runtime drift
- no code change

## Workstream B — Equity Universe Coverage
- current 98-name map
- out-of-universe stratified sample
- counterfactual scans
- white-space report

## Workstream C — Historical Recall Proxy
- bounded point-in-time cases
- positives + negative controls
- no future leakage

## Workstream D — Rejection / Judgment Audit
- Radar rejects
- Principal rejects
- CoS rejects/deferred
- independent blind re-review

## Workstream E — Close System Spec-to-Implementation Audit
- full coverage matrix
- data/source gaps
- detector gaps
- universe gaps

## Workstream F — Latency / Source Reliability
- event-to-observation timing
- source failure classification

## Workstream G — Final Findings / Remediation Options
- findings by miss taxonomy
- minimal remediation choices
- Founder decisions

Do not execute these until the Founder approves the exact bounded plan.

---

# 29. Acceptance Standard for the Audit

The audit is complete only when the Founder can answer:

### Equity
1. What percentage of the current intended equity universe is actually scannable?
2. What meaningful opportunities exist outside the current universe?
3. Which opportunity archetypes are covered by which lane?
4. Which archetypes have no reliable discovery path?
5. How often does independent review disagree with Hermes rejection?
6. Where are the largest false-negative risks?
7. Is CoS triage causing material additional misses?
8. What expansion is justified by evidence rather than intuition?

### Close System
1. What portion of the approved product taxonomy is actually covered today?
2. What can the system measure reliably?
3. What cannot it measure?
4. Which P1/P2/P3 dimensions have real evidence?
5. Which intelligence layers are missing?
6. Which product categories are currently impossible to discover systematically?
7. Which data gaps matter most?
8. What is the smallest path to materially better coverage?
9. Which underlying opportunities lack a reliably suitable/evaluable investable wrapper?

### Organization
1. Can we reconstruct why a potentially interesting item was rejected?
2. Do we learn from false negatives?
3. Can we separate Universe/Data/Detector/Judgment/Cadence/Triage misses?
4. Are discovery improvements likely to increase useful opportunity flow without flooding research capacity?

---

# 30. Remediation Principles — After Audit Only

If remediation is justified, prefer this order:

## First — Fix observability
Know what is being missed and why.

## Second — Fix universe / data coverage
Do not ask a smarter LLM to reason about assets/data it never sees.

## Third — Fix deterministic detectors
Where measurable signals exist, use deterministic candidate generation.

## Fourth — Improve judgment
Improve Radar / Principal / CoS prompts or review methods only after upstream coverage is adequate.

## Fifth — Add independent sampled challenge
Use only where evidence shows material judgment misses.

## Sixth — Consider persistent rejection/disposition history
Only if audit evidence shows ongoing value.

Avoid jumping directly to:

> “use a bigger model.”

A smarter model cannot recover an opportunity outside the universe or behind missing data.

---

# 31. Desired Long-Term Design Direction — Not Pre-Approved Implementation

The audit may support a future direction similar to:

```text
                 BROAD ELIGIBLE UNIVERSE
                          │
             ┌────────────┴────────────┐
             │                         │
          EQUITIES               CLOSE SYSTEM
             │                         │
   ┌─────────┼──────────┐     systematic product
   ▼         ▼          ▼       universe + data
Inflection Quality     Radar             │
           /Asymmetry                    ▼
   └─────────┼──────────┘       measurable evidence
             │                         │
             └────────────┬────────────┘
                          ▼
                  DISCOVERY EVIDENCE
                          │
                          ▼
                 Hermes / Principal
                "worth research capacity?"
                          │
                          ▼
                     Task Idea Card
                          │
                          ▼
                       CoS Triage
                          │
                          ▼
                    Research Mandate
                          │
                          ▼
                    v1.4 DOWNSTREAM
```

Principle:

> Machines surface what is measurable.  
> Hermes decides what is meaningful.  
> Audit protects against what Hermes might miss.

This is a direction to test, not an implementation authorization.

---

# 32. What Hermes Must Deliver in Its FIRST Response

Return exactly these sections:

## A. Current Discovery Map
Show every current discovery lane and actual runtime/authority status.

## B. Authority / Documentation Drift
Identify conflicts between FDs, READMEs, code, Cron, and current behavior.

## C. Equity Coverage FIT-GAP
- universe
- Inflection
- Quality & Asymmetry
- Radar
- source/data
- judgment gates
- CoS

## D. Close System Coverage FIT-GAP
Spec vs current real implementation.

## E. Miss Taxonomy Risk Map
For M1–M7:
- current evidence
- severity
- whether measured or unmeasured.

## F. Recall Measurement Plan
Propose:
- historical PIT benchmark;
- rejected-item audit;
- out-of-universe scan;
- coverage matrices.

## G. Precision Protection Plan
How to avoid flooding research capacity.

## H. Bounded Audit Execution Plan
Exact steps, artifacts, sample design, expected cost/complexity.

## I. Minimal Artifact / File Plan
Use existing audit/evidence structures where possible.

Do not create new state systems unnecessarily.

## J. Founder Decisions Required
List the smallest explicit approvals needed to execute the audit.

Then STOP.

Do not remediate or implement before Founder approval.

---

# 33. Required Final Audit Artifacts — After Approval

Hermes should propose exact paths after inspecting repository conventions.

Conceptually the audit should produce no more than necessary, likely including:

1. Discovery Architecture Map
2. Equity Universe Coverage Report
3. Discovery White-Space Matrix
4. Historical Recall Proxy Report
5. Rejected-Item / Judgment Audit
6. CoS Triage Audit
7. Close System Spec-to-Implementation + Product/Wrapper Coverage Matrix
8. Data / Source Gap Register
9. Discovery Latency Report
10. Final Discovery Recall & Coverage Audit
11. Remediation Options for Founder

Do not create 11 files merely because this list contains 11 concepts.

Consolidate where practical.

The goal is evidence, not document count.

---

# 34. Prohibited Outcomes

The audit must NOT:

- alter Gemini v1.4;
- auto-expand universe;
- auto-promote candidates;
- auto-create research mandates;
- lower the Radar bar merely to increase recall;
- introduce a composite Discovery Score;
- tune thresholds to historical winners;
- use future information in historical tests;
- let an independent challenger auto-override Hermes;
- invent missing commodity data;
- interpret missing data as “no opportunity”;
- create a second Kanban;
- create a competing Candidate state machine;
- make Close System a news-scanning strategy;
- revive momentum scanning inside Radar if current Founder decisions prohibit it;
- infer portfolio relevance;
- introduce execution/allocation logic.

---

# 35. Three-Pass Design Review Record

This final handoff incorporates three prior design reviews.

## Review 1 — Recall / Coverage Integrity

Added:

- explicit miss taxonomy M1–M7;
- historical point-in-time recall benchmark;
- CoS as a second false-negative gate;
- out-of-universe counterfactual scan;
- separation of precision vs recall.

Primary correction:

> “Scan quality looks good” is not evidence that good opportunities are not being missed.

## Review 2 — Governance / Anti-Overengineering

Removed:

- immediate permanent Discovery Reservoir;
- new canonical discovery states;
- parallel queues;
- automatic challenger gate.

Replaced with:

- bounded audit-only capture;
- use existing evidence/audit structures;
- persistent disposition history only if audit proves material value.

Primary correction:

> Measure the miss before building infrastructure to solve it.

## Review 3 — Measurement Validity / Close System

Added:

- explicit statement that absolute opportunity recall is unknowable;
- four recall proxies;
- no universal recall percentage;
- blind independent rejection review;
- spec-to-implementation Close System matrix;
- data/source coverage as a first-class constraint;
- prohibition against fitting all historical winners;
- systematic Close System universe principle.

Primary correction:

> The objective is not to prove IIP finds everything.  
> The objective is to make blind spots measurable, attributable, and reducible.

---

## Review 4 — Cross-File Harness Integration (v1.1)

Added:
- explicit Close System Product / Wrapper Coverage;
- separation between underlying opportunity discovery and investable implementation vehicle;
- alignment with Harness v1.1 and Gemini v1.4 boundaries.

Primary correction:

> Correctly detecting an underlying commodity or sector does not prove the chosen ETF/product is a valid Close System implementation vehicle.

---

# 36. Final Design Principle

IIP discovery should never become:

```text
Hermes saw it
→ Hermes was not excited
→ idea disappears forever
```

Nor should it become:

```text
scanner finds thousands of things
→ everything becomes research
→ organization drowns
```

The desired system is:

```text
Broad enough to see
→ disciplined enough to filter
→ auditable enough to detect misses
→ independent enough to challenge judgment
→ selective enough to protect research depth
```

The downstream v1.4 system can only research what upstream discovery gives it.

Therefore:

> Discovery quality is a first-order constraint on the total intelligence of IIP.
