# IIP × Gemini Deep Research × Gemini Notebook
## Final Hermes Handoff Brief v1.4

**Status:** Proposal for Hermes design review and Founder approval  
**Purpose:** Integrate Gemini Deep Research and Gemini Notebook into the existing IIP research organization without replacing IIP governance, duplicating existing research contracts, or sacrificing independent thinking.  
**Critical instruction:** This document is self-contained. Do not assume you have seen any earlier v1.0–v1.2 plan.

---

# 0. Founder Intent

The Founder has identified two distinct weaknesses in the current IIP research experience:

1. **Research depth:** Gemini Deep Research often produces broader and deeper source discovery and synthesis than the current Hermes-only research output.
2. **Communication quality:** Even when Hermes research is analytically strong, the final Thai writing can feel translated, mechanical, over-structured, or less natural than Gemini Deep Research. Strong research loses value when it is communicated poorly.

The integration must solve BOTH problems.

The target is not:

> replace Hermes with Gemini

and not:

> copy Gemini output directly into IIP

The target is:

> use each system where it has comparative advantage while keeping IIP as the governed research system.

Desired separation:

- **Hermes** = Research Operating System / Orchestrator / Evidence Controller
- **Gemini Deep Research** = Independent External Research Desk
- **Gemini Notebook** = Active Source-Grounded Research Workspace
- **Gemini Editorial** = Preferred Thai Investment Writing Desk after Facts Locked
- **Hermes Research Team** = Independent analysis, reconciliation, challenge, falsification
- **CRO / Auditor** = Independent truth challenge
- **IC Secretary** = Managing Editor / Publication Controller
- **IIP** = Canonical evidence, lineage, governance, research record
- **Obsidian** = Narrative knowledge / human learning layer only
- **Founder** = Final authority

---

# 1. FIRST ACTION: INSPECT BEFORE DESIGNING

Before proposing any change, inspect the repository and authoritative rules.

At minimum read and reconcile against:

- `AGENTS.md`
- project Constitution / Project DNA
- `operational/FOUNDERS-DECISIONS.md`
- `project-definition/EVIDENCE-MODEL.md`
- CIW specifications, especially:
  - Research Framework
  - Research Request Contract
  - Research Result Contract
  - Quality Gates
  - Lifecycle
- `operational/hermes-organization/templates/16-DEEP-RESEARCH-STANDING-CONTRACT.md`
- `reports/THAI-RESEARCH-EDITORIAL-STANDARD.md`
- relevant security / untrusted-content doctrine
- current role/authority documents for IC Secretary, CRO, Auditor, Data Steward, and research analysts
- current monitoring / Radar / CoS triage contracts where relevant

## Hard rule

Do NOT create:

- a second deep-research workflow;
- a second Evidence Ledger;
- a second source-of-truth system;
- a second monitoring engine;
- a second research lifecycle;
- a second Thai editorial standard;

unless a real gap cannot be satisfied by minimally amending the existing authoritative artifact.

Prefer amendments over parallel frameworks.

---

# 2. DO NOT IMPLEMENT YET

This handoff authorizes **design review only**.

Do NOT:

- modify authoritative files;
- commit code;
- create Cron jobs;
- change automation;
- create schemas;
- change official research state;
- create new Founder Decisions;
- alter publication contracts;
- automate Gemini;
- change browser/login configuration;

until you have:

1. completed a FIT-GAP review;
2. shown the Founder the minimum amendment plan;
3. identified exact artifacts to change;
4. received explicit Founder approval.

End the first response at the Founder decision gate.

---

# 3. Preserve the Existing Deep Research Contract

The existing IIP Deep Research Standing Contract remains the base workflow.

Do not replace its proven sequence:

```text
Research Mandate
→ Anti-Anchoring
→ Evidence Build
→ Main Essay
→ Cross-Examination
→ CRO Opposing Thesis
→ Audit / Re-Audit
→ Correction Propagation
→ Facts Locked
→ Editorial Synthesis
→ Founder Gate
→ Publish
```

Gemini must be inserted INTO this workflow.

It must not become a parallel workflow beside it.

---

# 4. Target Architecture

```text
                     IIP DISCOVERY / RADAR
                              │
                              ▼
                          CoS TRIAGE
                              │
                              ▼
                           RM-####
                              │
                              ▼
                       SOURCE PREFLIGHT
                              │
                              ▼
              CANONICAL IIP SOURCE SNAPSHOTS
                              │
                              ▼
                    GEMINI NOTEBOOK WORKSPACE
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
 Hermes Analyst A       Hermes Analyst B       Gemini Deep Research
    ISOLATED                ISOLATED                ISOLATED
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                       FIRST PASSES FROZEN
                              │
                              ▼
                        RECONCILIATION
                              │
                              ▼
                    GEMINI SOURCE EXPANSION
                              │
                              ▼
                      SOURCE ADMISSION GATE
                              │
                              ▼
                        EVIDENCE BUILD
                              │
                              ▼
                          MAIN ESSAY
                              │
                              ▼
                     CROSS-EXAMINATION
                              │
                              ▼
                    CRO OPPOSING THESIS
                              │
                              ▼
                       AUDIT / RE-AUDIT
                              │
                              ▼
                    CORRECTION PROPAGATION
                              │
                              ▼
                        ═ FACTS LOCKED ═
                              │
                              ▼
                   PUBLICATION FACT PACKET
                              │
                              ▼
                  GEMINI THAI EDITORIAL PASS
                              │
                              ▼
                    IC SECRETARY MANAGING QC
                              │
              ┌───────────────┼────────────────┐
              ▼               ▼                ▼
        Fact Fidelity   Thai Quality      Jargon Firewall
              │               │                │
              └───────────────┼────────────────┘
                              │
                              ▼
                   PUBLICATION QUALITY GATE
                              │
                              ▼
                         FOUNDER GATE
                              │
                              ▼
                           PUBLISH
```

---

# 5. Gemini Notebook Has Three Roles — No More

Gemini Notebook should be used aggressively, but within clear boundaries.

## Role A — Living Source Workspace

Maintain source-grounded context for the company or long-lived research subject.

Suggested naming:

`IIP — <Company> — <Ticker> — Living Research`

Use it to hold useful active research sources.

## Role B — Deep Research Launch / Source Discovery

Gemini Deep Research may be launched through the Notebook environment when appropriate.

Its purpose is to:

- expand the search frontier;
- discover sources Hermes did not find;
- follow material leads;
- identify contradictions;
- expose missing evidence;
- produce an independent research view.

## Role C — Final Editorial Workspace

After Facts Locked, use Gemini again as a Thai investment publication writer using ONLY the approved Publication Fact Packet plus selected supporting primary sources.

---

# 6. Gemini Notebook Is NOT the Audit Archive

This is critical.

Some Notebook sources can change or sync as their upstream document changes.

Therefore Notebook state is not sufficient to reconstruct historical research.

IIP must preserve point-in-time evidence independently.

For every material source entering a research run, use the existing Evidence Model requirements.

Where applicable preserve:

- source identifier;
- publication/public-availability timestamp;
- retrieval/ingestion timestamp;
- effective/as-of period;
- originating URL/reference;
- revision/vintage;
- content hash/source version;
- supersedes/superseded-by relationship;
- raw record reference;
- licensing/retention metadata;
- extraction method/version.

## Rule

```text
Notebook copy / synced source
≠
Canonical IIP Raw Source Record
```

The Notebook may hold the convenient working copy.

IIP must retain the auditable point-in-time record.

Do not silently let an auto-synced source rewrite the evidence state of an old research run.

---

# 7. Source Preflight and Freshness

Every research run begins with:

```text
RESEARCH_AS_OF: YYYY-MM-DD HH:MM timezone
```

Before Deep Research, Hermes checks whether current-required evidence is current as of that timestamp.

For a US-listed company, the existing CIW Source Gate governs.

Examples where applicable:

- latest 10-K / annual filing;
- latest 10-Q / interim filing;
- material recent 8-K;
- earnings release;
- earnings-call transcript;
- latest management guidance;
- DEF 14A when governance/compensation matters;
- historical filings required for normalization;
- relevant regulatory evidence.

## Enrichment sources

Useful but not automatically hard blocking unless the mandate requires them:

- CEO/CFO interviews;
- shareholder letters;
- investor day / capital-markets day;
- conference appearances;
- long-form podcasts;
- customer evidence;
- supplier evidence;
- competitor filings/calls;
- technical documentation;
- industry publications;
- original public YouTube interviews/transcripts.

## Freshness distinction

Do NOT equate "old" with "stale."

Use:

- **CURRENT-REQUIRED** — must be latest available
- **HISTORICAL-RELEVANT** — deliberately old evidence needed for longitudinal analysis
- **SUPERSEDED** — replaced by a newer authoritative version
- **STALE NARRATIVE** — old narrative/intent evidence whose current relevance has decayed

A FY2021 filing can remain highly relevant for five-year margin history.

A current investment conclusion cannot rely on an obsolete earnings quarter as though it were current.

---

# 8. Source Population in Gemini Notebook

Hermes may populate the Notebook with high-information-density sources.

Possible categories:

```text
Regulatory Filings
Financial / Earnings
Management
Products / Customers
Competitors
Industry / Supply Chain
Macro / Regulation
Independent Research
Contradictory / Bear Evidence
Gemini-Discovered Sources
```

Do not invent a second source-tier hierarchy if IIP already has one.

Use the existing IIP source-admission and independence rules.

## Management statement rule

A CEO interview is a primary source for:

> what management said

It is not automatically authoritative for:

> whether management's economic claim is true

Material management claims require independent verification when possible.

## YouTube / interview rule

When Notebook imports only transcript text, preserve the original URL/reference and timestamp context in IIP.

Do not treat transcript import alone as a complete audiovisual audit record.

---

# 9. Anti-Anchoring Must Include Gemini

The Gemini lane must not anchor the Hermes analysts.

The Hermes analysts must not anchor Gemini.

At Stage 2 Anti-Anchoring:

```text
Hermes Analyst A → isolated first pass
Hermes Analyst B → isolated first pass
Gemini Deep Research → isolated first pass
```

Freeze all first-pass artifacts before any cross-exposure.

## Critical extension

Isolation applies not only to current Hermes drafts.

It also applies to prior AI-generated analytical conclusions stored in a Living Notebook.

Gemini's first-pass research should see:

- approved Research Mandate;
- approved preflight evidence;
- known factual context;
- explicitly authorized known counterevidence where the existing contract requires it;

but should NOT automatically see:

- old Gemini conclusions;
- prior Hermes essays;
- old summary narratives;
- obsolete thesis statements;
- rejected hypotheses;
- prior publication prose;

if those artifacts would create avoidable anchoring.

## Implementation-neutral isolation rule

If the current Notebook UI/tooling can guarantee a clean selected-source context, use it.

If it cannot, create a dedicated clean research-run context/notebook or equivalent isolated execution context.

Do not sacrifice anti-anchoring merely to keep one notebook.

---

# 10. When Gemini Deep Research Should Run

Do not run Gemini Deep Research on every minor task.

Preserve the existing principle that deep research must earn its cost.

Gemini Deep Research is most appropriate for:

- Full Company Deep Research;
- major re-underwriting;
- a high-value unresolved evidence gap;
- material regime change;
- complex industry/competitive mapping;
- decision-critical research where broader search coverage has high expected information value.

For a narrow factual update, use the smallest sufficient research method.

The Research Mandate should record whether external Deep Research is:

- `required`
- `preferred`
- `not_needed`

with rationale.

Do not invent an arbitrary numeric threshold unless already authorized.

---

# 11. Gemini Deep Research Prompt Contract

The exact prompt should be generated from the Research Mandate and current evidence state.

Baseline instructions:

```text
RESEARCH AS OF: [exact timestamp]

You are an independent external research desk.

Do not assume the existing investment thesis is correct.

Use the most current information available through the Research-As-Of timestamp.

Prioritize original and primary sources where possible.

Distinguish:
- verified fact
- management claim
- third-party claim
- derived metric
- inference
- estimate
- unresolved / unknown

Actively search for evidence that could invalidate the apparent thesis.

Investigate meaningful contradictions instead of averaging them away.

Follow material new evidence into new questions when necessary.

Look for:
- business economics
- revenue drivers
- unit economics where relevant
- customer economics
- supplier dependence
- competitive structure
- product positioning
- management credibility
- capital allocation
- financial quality
- earnings quality
- dilution
- balance-sheet risk
- industry cycle
- technological disruption
- regulation
- market expectations / valuation context when in scope
- bear case
- thesis killers

Surface important sources that materially expand the evidence base.

State what remains unresolved.

Do NOT issue a buy/sell/position-size recommendation.

Do NOT treat prior AI conclusions as facts.
```

The Research Mandate and existing CIW applicability rules determine the actual scope.

Do not force every module into every research task.

---

# 12. Gemini-Discovered Sources Must Pass IIP Source Admission

Gemini citations are not automatically IIP evidence.

For each material Gemini-discovered source:

```text
Gemini discovers source
→ Hermes opens underlying source
→ verify source identity/date/context
→ evaluate independence / duplication
→ evaluate freshness and incremental information value
→ admit or reject under existing IIP rules
→ create/update canonical IIP evidence lineage
```

## Hard rule

```text
"Gemini said X"
≠
Evidence
```

The underlying source is the evidence.

Do not automatically import all cited and uncited sources into the Notebook.

Prefer information gain over source count.

---

# 13. Reconciliation

After independent first passes are frozen, compare:

- Hermes analyst views;
- Gemini Deep Research findings;
- primary evidence;
- counterevidence.

Focus on disagreement.

For each material disagreement, identify:

- which claim differs;
- which evidence differs;
- which assumption differs;
- which source is stronger;
- whether another research wave can resolve it;
- whether uncertainty must remain visible.

Do not average incompatible conclusions into false consensus.

Then continue the existing IIP contract.

Gemini does NOT replace:

- Evidence Build;
- Cross-Examination;
- CRO Opposing Thesis;
- independent audit;
- correction propagation;
- Founder review.

---

# 14. Research Layer and Publication Layer Are Separate

This is a core design principle.

```text
Research Truth
≠
Communication Quality
```

Analysts optimize for:

- truth;
- evidence;
- causal reasoning;
- contradiction;
- calculation;
- uncertainty.

The publication layer optimizes for:

- clarity;
- natural Thai;
- narrative flow;
- explanation;
- information hierarchy;
- reader usefulness.

Do not require the best researcher to also be the best Thai writer.

---

# 15. Publication Fact Packet — Mandatory Logical Handoff, Not Necessarily a New File

After:
- cross-examination;
- CRO dissent;
- audit/re-audit;
- corrections;
- correction propagation;
- Facts Locked;

the publication writer must receive a structured, Facts-Locked handoff.

Call the logical contract:

`PUBLICATION-FACT-PACKET`

However, do NOT create a new file merely to satisfy the name if an existing IC Secretary / publication-prep artifact can be minimally extended to contain the required fields.

The requirement is the contract, not file proliferation.

This is the ONLY analytical state the final editorial writer may rely on, plus specifically selected supporting primary sources.

Required fields:

## Research Identity
- subject
- scope
- Research-As-Of timestamp
- analytical horizon

## Central Finding
Final verified analytical conclusion.

## Material Claims
Atomic thesis-bearing claims allowed in publication.
Each maps to existing evidence lineage.

## Verified Facts
Facts admitted through IIP evidence rules.

## Verified Calculations
Material calculations plus approved interpretation.

## Causal Chain

```text
cause
→ business mechanism
→ financial manifestation
→ investment relevance
```

## Material Uncertainty
What is unresolved or not provable.

## Management Claims
Statements that remain attributable to management.

## Material Dissent
CRO/challenger positions that must remain visible.

## Rejected / Superseded Claims
Claims the editorial writer MUST NOT resurrect.

## Thesis-Break / Falsification Conditions
What evidence would materially change interpretation.

## Editorial Priority
Which insights matter most to the Founder/reader.

## Facts Locked Registry
- numbers
- dates
- source identifiers
- uncertainty levels
- material dissent
- conclusion boundaries

The Publication Fact Packet is a derived publication handoff.

It does not replace the canonical Research Result / evidence lineage.

---

# 16. Gemini Thai Editorial Role

After Facts Locked, Gemini may be used again in a completely separate role:

**Thai Investment Editorial Desk**

Gemini editorial output is NOT the original Deep Research report.

It is a fresh composition created from the final verified state.

## Baseline editorial prompt

```text
You are the Thai investment publication editor.

Write a professional Thai investment article using ONLY:
1. the approved PUBLICATION-FACT-PACKET, and
2. the specifically selected supporting primary sources.

You are NOT performing new investment analysis.

Do not add any factual, causal, financial, competitive, or investment claim
that is not already authorized by the Publication Fact Packet.

Do not resurrect rejected or superseded claims.

Preserve:
- all material facts
- figures
- dates
- uncertainty
- dissent
- causal conclusions
- thesis-break conditions where relevant

Write as a highly competent Thai investor explaining the case to another
experienced investor.

The article must feel originally written in Thai, not translated from English.

Use natural Thai sentence structure.

Do not over-translate established investment terminology.
Terms such as moat, switching cost, network effect, gross margin, FCF, ROIC,
capex, guidance, pricing power, unit economics, multiple, and reverse DCF may
remain in English when that is more natural for Thai investors.

Do not translate the research draft sentence-by-sentence.

Read the full approved packet, understand the argument, then write a fresh
causal narrative.

Within the opening 10–15% of the article, make clear:
- what is happening;
- why it matters now;
- the central insight;
- the strongest evidence;
- the strongest reason the thesis could be wrong.

Use numbers to explain economics, not to dump statistics.

Every important number should help answer:
- what changed?
- how large is it?
- why does it matter?
- what does it reveal about the business?

Preserve epistemic honesty with natural distinctions such as:
- ข้อมูลยืนยันว่า...
- หลักฐานตอนนี้ชี้ว่า...
- ฝ่ายบริหารระบุว่า...
- เรายังพิสูจน์ไม่ได้ว่า...
- นี่เป็นการประเมิน ไม่ใช่ตัวเลขที่บริษัทเปิดเผย...
- หลักฐานยังไม่พอให้สรุปว่า...

Avoid:
- project / governance jargon
- mandate IDs
- FD/spec references
- workflow language
- AI-sounding transition clichés
- excessive headings
- excessive bullet lists
- repetitive "ไม่ใช่ X แต่คือ Y" rhetoric
- literal English syntax
- unnatural Thai noun stacking
- generic consulting language
- unnecessary dramatic language

The final article must read like a high-quality Thai investment publication,
not an AI research artifact.
```

---

# 17. IC Secretary Role — Managing Editor, Not Forced Primary Writer

Do not remove the IC Secretary.

Refine the role.

The IC Secretary should become the:

**Managing Editor / Publication Controller**

Responsibilities:

- prepare or verify the Publication Fact Packet;
- dispatch the approved editorial writer;
- inspect Thai readability;
- verify no facts or conclusions changed;
- verify uncertainty remains;
- verify dissent remains;
- verify internal jargon is removed;
- return weak prose for another editorial pass;
- control the Founder publication handoff.

There is no architectural requirement that Hermes itself must write the final prose.

Use the strongest approved writer for the job.

---

# 18. Facts Locked Must Be Upgraded: Token Fidelity + Semantic Fidelity

The existing numeric/date/accession token-preservation check is valuable but insufficient.

A writer can preserve every number and still change the meaning.

Example failure:

```text
Research:
"Evidence is insufficient to conclude that switching costs are increasing."

Editorial distortion:
"Switching costs are increasing, although the exact magnitude is uncertain."
```

All numbers could remain unchanged while the conclusion changes.

Therefore publication must pass TWO fidelity checks.

## Gate F1 — Token Fidelity

Existing deterministic checks:

- figures;
- dates;
- accessions;
- required immutable tokens.

## Gate F2 — Semantic Fidelity / No-New-Claims

Extract every material claim from the final article and map it against the Publication Fact Packet.

Classify each material publication claim as:

- `MATCHED`
- `SUPPORTED_REPHRASE`
- `ALTERED_MEANING`
- `NEW_UNAUTHORIZED_CLAIM`
- `OMITTED_MATERIAL_UNCERTAINTY`
- `OMITTED_MATERIAL_DISSENT`

Publication fails if any material claim is:

- `ALTERED_MEANING`
- `NEW_UNAUTHORIZED_CLAIM`
- materially omits required uncertainty/dissent.

The semantic reviewer must not be the same context that wrote the article where operational separation is practical.

For decision-critical research, prefer an independent reviewer/context.

---

# 19. Thai Publication Quality Gate

Correct facts are not sufficient for publication.

A final article must pass:

## P1 — Research Integrity
- final thesis matches Facts Locked state;
- no rejected claim reappears;
- uncertainty preserved;
- material dissent preserved.

## P2 — Fact Fidelity
- token fidelity passes;
- semantic fidelity passes;
- no new unauthorized claim.

## P3 — Natural Thai
- sounds written in Thai, not translated;
- terminology natural for Thai investors;
- no awkward literal calques;
- no excessive noun stacking;
- no unnecessary academic language;
- English finance terms retained where clearer.

## P4 — Causal Narrative
- article explains mechanism, not checklist;
- thesis is easy to locate;
- numbers have "so what?";
- background does not bury the insight.

## P5 — Publication Craft
- headline accurately reflects thesis;
- opening provides information rather than hype;
- paragraph flow is deliberate;
- headings/bullets are used only when helpful;
- no obvious repetitive AI prose patterns;
- no internal IIP governance jargon.

A P3/P4/P5 failure is a real publication failure even if research is correct.

Return for re-edit.

---

# 20. Founder-Approved Thai Writing Benchmark

Do not invent a style benchmark.

Create a mechanism for a small Founder-approved corpus of writing examples.

Preferred source:

- Gemini Deep Research / Gemini editorial outputs the Founder personally considers excellent.

Use the corpus only to learn communication characteristics such as:

- naturalness;
- sentence rhythm;
- explanation density;
- use of English financial terms;
- paragraph length;
- causal flow;
- level of formality;
- handling of uncertainty.

Do NOT copy sentences.

Do NOT treat benchmark articles as factual/analytical authority.

Until the Founder supplies/approves examples, use:

- current `THAI-RESEARCH-EDITORIAL-STANDARD.md`;
- the rules in this handoff;
- existing Founder feedback.

---

# 21. Editorial A/B Validation — Calibration Only

For the first 3–5 suitable research publications after integration:

Create from the SAME Facts-Locked publication handoff:

- Candidate A — Gemini editorial
- Candidate B — Hermes / current IC Secretary editorial

Compare, preferably without writer labels where practical, on:
- natural Thai;
- clarity;
- causal flow;
- concision;
- investment usefulness;
- preservation of uncertainty;
- factual/semantic fidelity.

Founder preference is the decisive communication-quality signal.

If Gemini consistently wins and passes fidelity gates:
- make Gemini the default Thai prose generator;
- STOP routine A/B duplication.

If Hermes consistently wins:
- retain Hermes as default;
- use Gemini selectively.

Do not turn two complete drafts into a permanent tax.

Re-open A/B calibration only when:
- editorial model changes materially;
- Thai quality visibly regresses;
- Founder requests recalibration;
- publication genre changes materially.

Hermes remains orchestrator and publication controller regardless of prose generator.

---

# 22. Gemini / Browser Integration Reliability

The integration must not silently assume the Gemini UI will always be available.

Use the existing authenticated browser/session integration if already working.

## Security boundaries

Hermes must not:

- store or expose Google passwords;
- commit session tokens/cookies;
- bypass CAPTCHA;
- bypass MFA;
- log authentication secrets.

If re-authentication is required:

- pause the affected Gemini step;
- ask for human login/re-authentication;
- resume from recorded workflow state.

## Workflow state

Use a resumable state model, mapped to existing IIP workflow states rather than creating competing official states.

Operational sub-status examples may include:

```text
GEMINI_PREFLIGHT_READY
GEMINI_DR_SUBMITTED
GEMINI_DR_RUNNING
GEMINI_DR_RESULT_CAPTURED
GEMINI_SOURCES_REVIEWED
GEMINI_EDITORIAL_SUBMITTED
GEMINI_EDITORIAL_CAPTURED
GEMINI_FIDELITY_REVIEW
```

These are implementation details, not Candidate/Thesis/Investment states.

Do not create them as official domain states unless existing governance requires it.

---

# 23. Failure / Fallback Semantics

Gemini availability must never be confused with research completeness.

If Gemini fails:

```text
EXTERNAL_DR_UNAVAILABLE
```

or another existing compatible failure status should be recorded.

Do NOT silently continue and claim equivalent coverage.

Possible outcomes:

1. retry within bounded policy;
2. use approved alternative external research desk;
3. continue Hermes-only as a clearly limited / partial research run;
4. route to Founder if Gemini coverage was required by the mandate.

Similarly, if Gemini editorial is unavailable:

- Hermes/IC Secretary may produce a fallback draft;
- it must pass the SAME publication quality gates;
- do not lower the Thai quality standard because the preferred editor is unavailable.

---

# 24. Monitoring Boundary

Gemini integration does not own monitoring.

Existing IIP:

- Radar;
- CIW monitoring;
- Cron;
- CoS triage;
- event-driven workflows;

remain responsible for detecting potential new research needs.

Monitoring may create/propose a research task.

Deep Research begins through the existing authorized research path.

Gemini must not autonomously:

- promote a Candidate;
- change Thesis status;
- change Theme state;
- publish;
- initiate decision-critical research outside approved workflow;
- change investment status.

---

# 25. Obsidian Boundary

Preserve existing IIP doctrine.

Obsidian is the narrative / learning layer.

It may contain:

- research notes;
- learning;
- thesis evolution narratives;
- human memory;
- cross-research synthesis.

It is not the sole canonical evidence/state system.

Gemini Notebook and Obsidian may improve usability and memory.

Neither overrides IIP canonical lineage.

---

# 26. Integration Success Metrics

Do not judge Gemini by:

- report length;
- number of searches;
- number of sources;
- eloquence alone.

Measure incremental research value.

Possible metrics:

## Research Value
- unique material sources discovered;
- unique primary sources discovered;
- material contradictions found;
- material assumptions invalidated;
- unresolved questions resolved;
- factual corrections caused by Gemini evidence;
- useful evidence Hermes did not find;
- duplicate/noise source rate.

## Publication Value
- Founder preference in A/B tests;
- Natural Thai gate pass rate;
- number of editorial rework loops;
- semantic fidelity failures;
- token fidelity failures;
- reading clarity / time-to-thesis;
- amount of internal jargon removed;
- unsupported-claim rate.

## System Value
- auditability preserved;
- point-in-time reconstruction preserved;
- no authority leakage;
- no duplicate canonical systems;
- bounded failure recovery;
- no silent downgrade when Gemini is unavailable.

Do not invent investment-performance attribution from a tiny pilot.

---

# 26A. Research / Engineering Skill Boundary

Investment research tasks must NOT auto-load the software `project-workflow` engineering skill.

Research tasks use:
- IIP Evidence;
- IIP Deep Research;
- Publication;
- Kanban coordination;
- role contracts.

If a research run discovers that code, scanner, schema, UI, config, or harness must change:

```text
research finding
→ separate authorized engineering task
→ project-workflow v3.8
→ implementation / tests / release
```

Do not let software governance anchor or bloat independent research first passes.

Likewise, engineering verification does not replace:
- Cross Examination;
- CRO;
- research audit;
- Facts Locked.

---

# 27. Minimum-Change Design Principle

Before proposing a new file, ask:

> Can this be expressed as a minimal amendment to an existing authoritative contract?

Expected likely amendment targets:

- `operational/hermes-organization/templates/16-DEEP-RESEARCH-STANDING-CONTRACT.md`
  - add isolated Gemini DR lane at Anti-Anchoring
  - add source-admission handoff
  - add Publication Fact Packet logical contract / minimally extend an existing publication-prep artifact
  - add Gemini editorial lane after Facts Locked
  - add semantic fidelity / publication quality gate

- `reports/THAI-RESEARCH-EDITORIAL-STANDARD.md`
  - allow approved best-available prose generator
  - make IC Secretary Managing Editor / Publication Controller
  - add Semantic Fidelity / No-New-Claims
  - add Thai quality benchmark / A-B validation
  - strengthen anti-AI-prose and natural Thai requirements

Potentially:

- one small subordinate Gemini Notebook operating protocol IF existing docs cannot cleanly hold source-workspace/security/runtime details.

Do NOT create a large new parallel document tree by default.

---

# 28. What Hermes Must Deliver to the Founder

Your FIRST response to this handoff must contain a design review only.

Deliver exactly these sections:

## A. Current-State Findings
What IIP already has that solves parts of this plan.

## B. FIT-GAP
For every major requirement in this document:

- already satisfied;
- partially satisfied;
- missing;
- conflicts with existing authority.

## C. Recommended Minimal Architecture
Show the final integration architecture after reconciling with the repo.

## D. Exact Amendment Set
List exact existing files you recommend changing and WHY.

Avoid new files unless necessary.

## E. Governance / Authority Conflicts
Identify anything requiring a named Founder Decision.

## F. Gemini Notebook Operating Boundary
Explain:
- source role;
- anti-anchoring;
- point-in-time snapshot;
- editorial role;
- what remains canonical in IIP.

## G. Thai Publication Quality Plan
Explain:
- Publication Fact Packet;
- Gemini editorial role;
- IC Secretary role;
- token fidelity;
- semantic fidelity;
- Natural Thai gate;
- A/B calibration.

## H. Failure / Security Plan
Explain browser/auth/session failure and fallback behavior.

## I. Validation Plan
Propose a bounded integration validation using an upcoming suitable Research Mandate.

Do NOT select or create a new investment thesis merely to test the integration if an existing suitable mandate can be used.

## J. Founder Decisions Required
Present the smallest possible set of explicit decisions required before implementation.

Then STOP.

Do not implement until the Founder approves the exact plan/amendments.

---

# 29. What NOT to Do

Do not:

- rebuild IIP around Gemini;
- make Gemini the source of truth;
- publish the original Gemini DR report directly;
- let Gemini conclusions anchor all Hermes analysts;
- feed prior AI conclusions into Gemini first-pass by default;
- import every Gemini-discovered source;
- create a duplicate Evidence Ledger;
- create a duplicate financial model without a proven need;
- create a new monitoring system;
- let auto-synced Notebook sources rewrite historical evidence;
- allow editorial prose to introduce new analysis;
- rely only on numeric token checks after editorial;
- force every finance term into Thai;
- make every report long because Deep Research was used;
- lower research or language standards when Gemini is unavailable;
- bypass Founder gates;
- over-engineer the integration.

---

# 30. v1.4 Cross-File Integration Notes

v1.4 adds three constraints:

1. Publication Fact Packet is a mandatory logical contract, not mandatory file proliferation.
2. Editorial A/B testing is bounded calibration, not permanent double-generation.
3. Project Workflow engineering skill is outside normal research execution; code/system changes become separate engineering tasks.

These changes preserve v1.3 research architecture while reducing context load and operational duplication.

---

# 31. Final Design Principle

The desired operating model is:

```text
Hermes protects the process.
IIP protects evidence and authority.
Gemini expands the research frontier.
Gemini Notebook makes the source base usable.
Gemini writes Thai when it is the better communicator.
IC Secretary protects publication quality.
CRO and Auditor protect dissent and truth.
Founder decides.
```

Optimization target:

```text
FINAL RESEARCH VALUE
=
Research Truth
× Evidence Quality
× Independence
× Communication Quality
```

If any multiplier approaches zero, a long and sophisticated report still fails.

The goal is not to prove Hermes or Gemini is superior.

The goal is to build the strongest investment-research organization from their complementary strengths.
