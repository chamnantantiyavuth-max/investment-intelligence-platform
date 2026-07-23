# Hermes Handoff
## Dual Intelligence Operating Model — Controlled Work Sequence

**Proposal ID:** `IIP-DUAL-INTELLIGENCE-OPERATING-MODEL-v0.1`  
**Source proposal:** `proposed-amendments/IIP-DUAL-INTELLIGENCE-OPERATING-MODEL-v0.1.md`

---

# Recommended Repository Placement

Place the proposal at:

```text
investment-intelligence-platform/
└── proposed-amendments/
    ├── AI-OPERATING-CONSTITUTION-v0.1.md
    └── IIP-DUAL-INTELLIGENCE-OPERATING-MODEL-v0.1.md
```

After approval, the permanent Project Definition artifact should be:

```text
project-definition/
└── INVESTMENT-INTELLIGENCE-OPERATING-MODEL.md
```

Do not place the permanent logical operating model under `design/`. It defines product/domain responsibilities, not implementation architecture.

Detailed agent topology belongs later under a design area such as:

```text
design/
├── shared-ai/
│   ├── AI-AGENT-OPERATING-MODEL.md
│   ├── AI-WORKFLOW-AND-PROVENANCE-MODEL.md
│   └── AI-APPLICATION-FUNCTION-CONTRACTS.md
└── alpha-momentum-v0/
    └── ...
```

These design files must not be created until the applicable design plan is explicitly approved.

---

# Controlled Sequence

## Gate 0 — Repository Baseline

Hermes performs read-only inspection:

- verify branch, HEAD, tags, and clean/dirty state;
- identify current authority versions;
- read change control;
- identify whether prior unauthorized design drafts remain;
- make no changes.

## Gate 1 — Proposal Assessment

Hermes reads the proposal and reports:

- conflicts;
- materiality;
- exact file changes;
- required approvals;
- V0 impact;
- deferred decisions;
- whether the AI Operating Constitution proposal needs a targeted specialized-agent clause.

No files are modified.

## Gate 2 — Founder Approval of Named Plan

Founder approves the exact Project Definition amendment plan, not implementation.

## Gate 3 — Draft Project Definition Amendment

Hermes drafts or updates only the approved document set:

- `project-definition/INVESTMENT-INTELLIGENCE-OPERATING-MODEL.md`
- `project-definition/README.md`
- `project-definition/DOMAIN-ARCHITECTURE.md`
- minimal traceability update to `project-definition/ALPHA-MOMENTUM-V0-SPEC.md`
- proposed operational synchronization drafts

All changed artifacts remain Draft for Founder Review unless the approval explicitly authorizes promotion.

## Gate 4 — Independent Audit

Audit for:

- authority;
- scope;
- terminology;
- contradiction;
- accidental rule invention;
- V0 scope creep;
- external-system boundary leakage;
- deterministic/AI separation;
- exact O'Neil/Minervini rules remaining deferred.

## Gate 5 — Founder Approval and Controlled Application

Only after audit, apply the approved amendment, authority metadata, Founder Decision, indexes, and roadmap wording.

## Gate 6 — Alpha Momentum V0 Design Integration

Create or amend the approved Alpha Momentum V0 design plan so that it implements only:

- Shared Intelligence Core contracts;
- a logical Momentum Intelligence workflow;
- deterministic feature services;
- challenge;
- synthesis;
- Founder review.

Do not implement the full long-term multi-agent organization in V0.

## Gate 7 — Agent Design Later

After Project Definition and V0 design contracts are stable, define AI function contracts and determine whether each logical role is:

- code;
- deterministic service;
- tool;
- prompt/workflow stage;
- one general agent;
- specialized subagent.

Only then select orchestration and implementation details.

---

# Prompt 1 — Read-Only Assessment

```text
You are working inside the Investment Intelligence Platform repository.

A Founder-proposed Project Definition amendment has been placed at:

`proposed-amendments/IIP-DUAL-INTELLIGENCE-OPERATING-MODEL-v0.1.md`

Related proposed AI amendment:

`proposed-amendments/AI-OPERATING-CONSTITUTION-v0.1.md`

Perform a read-only authority and integration assessment.

Do not modify, create, move, delete, stage, commit, or tag any file.

Read at minimum:

- `AGENTS.md`
- `01-PROJECT-DNA.md`
- `02-PROJECT-CONSTITUTION.md`
- `03-OPERATIONAL-DOCUMENTS-INDEX.md`
- all current project-definition files
- `operational/CHANGE-CONTROL-AND-APPROVAL.md`
- `operational/FOUNDERS-DECISIONS.md`
- `operational/AI-GOVERNANCE.md`
- `operational/ARCHITECTURE-PRINCIPLES.md`
- `operational/DOMAIN-GLOSSARY.md`
- `operational/SCOPE-AND-NON-SCOPE.md`
- `operational/ROADMAP.md`
- `operational/DEFERRED-DECISIONS.md`
- both proposed amendment files above

First verify:

- branch;
- HEAD;
- clean/dirty working tree;
- authoritative Foundation and Project Definition versions;
- current phase;
- whether unapproved or quarantined design drafts remain.

Then report:

1. current authority baseline;
2. whether the proposal conflicts with approved doctrine;
3. whether the proposal is constitutional, Project Definition, operational, design, or mixed;
4. the exact permanent file set that should change;
5. the exact insertion or synchronization location in each file;
6. required version increments and named approval artifacts;
7. current V0 impact;
8. which details must remain deferred;
9. whether the existing AI Operating Constitution proposal should receive a narrow specialized-agent clause;
10. a staged plan that stops before implementation.

Critical constraints:

- Capital Command and Trading / Execution Systems are external, not modules of this project.
- Preserve the current Alpha Momentum V0 boundary.
- Do not invent O'Neil, Minervini, Momentum Masters, valuation, screening, pattern, ranking, threshold, period, benchmark, or scoring rules.
- Do not select models, agent frameworks, APIs, vendors, databases, languages, or UI frameworks.
- Do not claim that each logical role must be a separate agent.
- Do not modify authority files.
- Do not begin design or implementation.

Stop after the assessment and await explicit Founder approval.
```

---

# Prompt 2 — Draft the Approved Project Definition Amendment

Use only after reviewing Hermes's assessment and explicitly approving its exact file plan.

```text
I approve the Project Definition drafting plan for:

`IIP-DUAL-INTELLIGENCE-OPERATING-MODEL-v0.1`

Apply only the approved drafting scope from the read-only assessment.

This authorization is for Project Definition and directly required synchronization drafts only. It does not authorize application code, implementation, technology selection, final agent topology, or investment-rule calibration.

Required outcome:

1. Create:
   - `project-definition/INVESTMENT-INTELLIGENCE-OPERATING-MODEL.md`

2. Update only as required:
   - `project-definition/README.md`
   - `project-definition/DOMAIN-ARCHITECTURE.md`
   - `project-definition/ALPHA-MOMENTUM-V0-SPEC.md`

3. Prepare proposed synchronization wording for:
   - `operational/FOUNDERS-DECISIONS.md`
   - `operational/DOMAIN-GLOSSARY.md`
   - `operational/SCOPE-AND-NON-SCOPE.md`
   - `operational/ROADMAP.md`
   - `operational/DEFERRED-DECISIONS.md`

4. Prepare a targeted proposed addition to:
   - `proposed-amendments/AI-OPERATING-CONSTITUTION-v0.1.md`

The constitutional addition may establish only:

- specialized agents require explicit role, authority, evidence, input/output, provenance, validation, failure, escalation, and approval contracts;
- AI-to-AI delegation does not create authority;
- logical roles do not require separate deployed agents;
- exact agent topology remains a design decision.

Do not place the detailed dual-desk organization in the Constitution.

Required domain outcome:

- Fundamental & Opportunity Intelligence and Momentum & Market Leadership Intelligence are equal product paths.
- Shared Intelligence Core supports both without owning strategy semantics.
- Independent Challenge remains separate.
- Synthesis preserves conflicting evidence and separate quality/readiness views.
- Founder Decision Gate remains final within this platform.
- Valuation is contextual, non-dominant, and not an automatic veto by default.
- Capital Command and Trading / Execution remain outside the project boundary.
- V0 remains a narrow Alpha Momentum vertical slice and does not require the full future multi-agent organization.
- Exact O'Neil/Minervini rules, formulas, periods, thresholds, weights, patterns, benchmarks, model providers, and agent framework remain explicitly deferred.

Authority discipline:

- Mark all new or changed Project Definition content Draft for Founder Review unless the repository's approved change-control procedure and this authorization explicitly allow another status.
- Do not alter unrelated sections.
- Do not create code, schema, dependencies, ADRs, implementation plans, or agent prompts.
- Do not commit or tag.

Verification:

- contradiction review;
- terminology review;
- authority review;
- scope/non-scope review;
- V0 scope-creep review;
- external-boundary review;
- rule-invention review;
- Git diff and status report.

Stop after presenting the complete proposed diff and verification results.
```

---

# Prompt 3 — Plan Alpha Momentum V0 Integration

Use only after the Project Definition amendment has passed independent audit and received Founder approval.

```text
The Dual Intelligence Operating Model has now been approved as Project Definition authority.

Perform a read-only Alpha Momentum V0 design-integration review.

Do not modify files yet.

Determine the smallest changes required to the approved Alpha Momentum V0 design plan so V0 demonstrates:

- Shared Intelligence Core contracts;
- deterministic evidence validation and feature computation;
- one logical Momentum & Market Leadership workflow;
- market-regime context;
- fundamental-momentum context;
- relative-strength context;
- price-volume and setup-readiness context;
- independent momentum challenge;
- synthesis that preserves separate Candidate Quality, Theme Quality, Entry Readiness, and Data Confidence;
- Founder review.

Do not require one subagent per logical role.

Identify which responsibilities should initially be:

- deterministic services;
- workflow stages;
- one general AI research capability;
- an independent challenge capability;
- later specialized agents.

Keep out of V0:

- full Fundamental & Opportunity workbench;
- production multi-agent orchestration;
- live/current feeds;
- AI-driven theme discovery;
- broker, capital-allocation, or execution functionality;
- final O'Neil/Minervini rule packs;
- invented formulas, periods, thresholds, weights, benchmarks, and patterns;
- technology and provider selection.

Return:

1. traceability to approved Project Definition;
2. minimal V0 logical component map;
3. exact design files requiring amendment;
4. proposed drafting tranches;
5. material-change classification per tranche;
6. acceptance and audit plan;
7. explicit deferred items.

Stop before modifying any file.
```
