# Hermes Master Integration Prompt v1.1
## Safe Integration Order for IIP + IPM Harness Reconstitution

I am attaching THREE Founder design handoffs:

1. `IIP_Hermes_Harness_Reconstitution_Single_Kanban_Final_v1.1.md`
2. `IIP_Discovery_Recall_Coverage_Audit_Final_Handoff_v1.1.md`
3. `IIP_Gemini_Deep_Research_Final_Handoff_v1.4.md`

You also currently have an installed `project-workflow` skill that claims v3.7.1.

Read all three handoffs in full.

Then inspect the ACTUAL installed Hermes runtime, the ACTUAL installed project-workflow skill, the current IIP repository, and the current IPM project.

Do not assume that:
- the installed Hermes version matches old repository documentation;
- the string `v3.7.1` uniquely identifies one project-workflow content;
- the attached plans know local paths/config better than the live machine.

The live runtime + current approved project authority are the evidence base.

---

# Founder Direction

This is a major Harness reconstitution.

The intended final system is:

```text
ONE Hermes Kanban board
        │
        ├── tenant=iip
        │      Discovery → Research → Publication
        │
        └── tenant=ipm
               Portfolio Office
```

There must be ONE operational work-state truth for IIP Research + IPM after cutover.

The old repo-based IIP Kanban must eventually be retired and deleted from the active working tree after verified migration.

Do NOT create:
- a second Hermes board for IPM;
- a parallel archive board;
- a second work-state database behind `/kanban`;
- another Candidate/domain state machine.

Git history + one migration evidence record preserve the old-board history.

---

# Critical Boundary

IIP stays portfolio-blind.

Published IIP research may flow:

```text
IIP → IPM
```

Portfolio-sensitive information must NEVER flow:

```text
IPM → IIP
```

Because a tenant inside one Hermes board is NOT a hard ACL, do not put any of the following into shared Kanban task titles, bodies, metadata, comments, results, or attachments:

- holdings;
- position size;
- cost basis;
- account cash/value;
- P&L;
- transaction history;
- live orders;
- broker/account identifiers;
- private portfolio sizing rationale;
- sensitive PM Letters or portfolio reports.

IPM-sensitive artifacts remain inside the authorized IPM workspace.

The shared board stores only sanitized operational references.

---

# The Three Workstreams Must Stay Separate

## Workstream 1 — Discovery Recall v1.1

Owns:

```text
Universe
→ Sources/Data
→ Discovery scanners/Radar
→ Task Idea
→ CoS Triage
```

Purpose:
How do we know IIP is not missing good opportunities?

Do not change its analytical methodology merely to fit Kanban.

## Workstream 2 — Gemini Deep Research v1.4

Owns:

```text
Research Mandate
→ Anti-Anchoring
→ Hermes + Gemini DR
→ Evidence
→ Cross-Exam
→ CRO
→ Audit
→ Facts Locked
→ Thai Editorial
→ Founder
→ Blog
```

Purpose:
Once something deserves research, how do we research and communicate it at the highest quality?

Do not change its analytical methodology merely to fit the Harness.

## Workstream 3 — Harness v1.1

Owns:

- profiles;
- profile descriptions;
- SOUL;
- AGENTS/context;
- Skills;
- Memory;
- toolsets;
- model-routing boundaries;
- ONE Kanban;
- workspaces;
- security;
- Cron-to-task handoff;
- `/kanban`;
- `/org-office`;
- IIP↔IPM operating firewall;
- Project Workflow disposition.

Harness coordinates Workstreams 1 and 2.
Harness does not redefine their research truth.

---

# Project Workflow v3.7.1 Is a First-Class Migration Item

Do NOT delete project-workflow.

Do NOT assume the version string is enough.

Locate the EXACT installed skill and report:

- path;
- content hash;
- declared version;
- reference-directory hash;
- companion skills/scripts;
- same-name/same-version duplicates;
- profile-local shadows;
- AGENTS/SOUL files that reference or auto-load it.

Compare its actual responsibilities against the new Harness.

The intended direction is:

```text
project-workflow v3.7.1
        ↓
versioned candidate v3.8
        ↓
Engineering / System Change Workflow ONLY
```

It should remain strong for:
- code;
- architecture;
- schema;
- API;
- UI implementation;
- data pipeline implementation;
- deterministic financial calculation implementation;
- config/profile changes;
- SOUL/AGENTS/skills/memory-system changes;
- Kanban integration;
- Cron/automation;
- release/deployment.

It should NOT auto-load for:
- Radar;
- investment research;
- filings analysis;
- Gemini Deep Research;
- evidence research;
- CRO;
- research audit;
- Thai editorial;
- IPM investment reasoning.

Evaluate specifically whether v3.8 should:
- remove hard-coded model/provider routing;
- remove universal Parent/Sol organizational topology;
- use Hermes Kanban instead of its own per-task state machine;
- narrow PROJECT_STATE / SESSION_CLOSEOUT to project-level milestones;
- keep Bible-first, SMART-SCOPE, locked tests, Evidence QA, root-cause, rollback, end-to-end verification;
- separate engineering Council from investment-research CRO/audit;
- move domain Identity Cards out of MEMORY;
- make Constitution/Bible creation conditional for new projects rather than duplicate existing IIP governance;
- replace universal risky-path blacklists with project/task-specific paths;
- reconcile stale companion skill references.

Do not overwrite the installed v3.7.1 in place before Founder approval and backup.

---

# SOUL / Context Target

For IIP:

```text
ONE shared IIP Research SOUL
```

Role differences should come from:

```text
Profile Description
+ PRINCIPAL.md
+ current Kanban task
+ task-scoped Skills
```

Do not maintain 10+ near-duplicate SOULs unless a genuine identity difference requires it.

IPM intentionally receives its own SOUL because its portfolio authority/context differs.

SOUL:
- identity;
- intellectual temperament;
- communication style.

AGENTS:
- project authority;
- project rules;
- source-of-truth hierarchy;
- security;
- task routing.

Do not hard-code IIP AGENTS to inherit another profile's SOUL path.

Audit whether a legacy top-level `user.md` duplicates `memories/USER.md`.
Retire duplicate user-profile mechanisms only after proving what the installed runtime actually loads.

---

# Skills Target

Inventory FIRST.

Do not create new skills from names alone.

Target responsibility map:

```text
ENGINEERING
project-workflow v3.8

ORGANIZATION
capital-kanban
hermes-harness-admin

IIP RESEARCH
iip-discovery-audit
iip-evidence
iip-deep-research
iip-publication

BOUNDARY
iip-ipm-handoff

IPM
ipm-operating-review
```

Existing high-quality specialist/UI/testing skills may remain if responsibility is non-overlapping.

Prefer:
- reuse;
- merge;
- retire;
- thin wrappers/references

over skill proliferation.

Critical shared skills must not be silently mutable by ordinary workers.

Remember:
`skills.external_dirs` is not a read-only security boundary by itself.

Evaluate:
- filesystem read-only strategy;
- trusted Harness Admin writer;
- `skills.write_approval`;
- `skills.guard_agent_created`;
- skill-shadow scan.

If write approval is enabled, verify the pending/approve/reject workflow actually works on the installed Hermes version and on the interface the Founder uses.

---

# Memory Target

Built-in memory is small operational memory.

Do not use it as:
- investment thesis;
- evidence store;
- Founder decision register;
- task tracker;
- portfolio state;
- Gemini result archive.

Target:

```text
SOUL            = identity
AGENTS/repo     = project rules
Skills          = reusable procedure
Kanban          = current work
MEMORY.md       = tiny operational sticky facts
USER.md         = stable Founder preferences
Session Search  = on-demand prior chat retrieval
Gemini Notebook = active research workspace
Obsidian        = narrative learning
IIP Repo        = research/evidence authority
IPM Repo        = portfolio authority
```

Do not enable a shared external memory provider by default.
If you recommend one, make it a later isolated pilot.

---

# Single-Board Security Gates

Before production IPM tasks are allowed on the shared board, provide:

`FILESYSTEM ISOLATION VERDICT`

Choose:

## A — Hard isolation
For example:
- sandbox/container mounts;
- OS ACL;
- restricted backend.

or

## B — Logical-only isolation
If hard isolation is impractical, quantify residual risk and request explicit Founder acceptance.

Workspace selection alone is not proof of hard isolation.

Also verify:
- no IPM-sensitive attachments on board;
- board content leak scan;
- IIP memory leak scan;
- dashboard localhost-only;
- no `0.0.0.0` exposure unless a separate secured remote design is approved.

---

# Kanban Initial Operating Mode

Use the INSTALLED Hermes schema.

Preferred initial policy:

```text
Manual orchestration first.
```

Expected intent:

```yaml
kanban:
  auto_decompose: false
  auto_promote_children: false
  max_in_progress: 3
  max_in_progress_per_profile: 1
  dispatch_in_gateway: true
  failure_limit: 2

  # Intentionally no default_workdir.
  # Every IIP/IPM task supplies explicit workspace.
```

Do not blindly copy these keys if the installed version differs.

Do not configure a default assignee/orchestrator until the pilot proves the safest behavior for a board shared by IIP and IPM.

Preserve the native Hermes Kanban worker lifecycle.
Do not replace native `kanban-worker` behavior with `capital-kanban`.

`capital-kanban` owns only IIP/IPM organizational policy.

---

# REQUIRED INTEGRATION ORDER

Do NOT reorder these stages without explaining why and getting Founder approval.

## Stage 0 — Baseline / Backup

No behavioral change.

Capture:
- Hermes version;
- all profiles/configs/descriptions;
- all SOUL hashes;
- USER/MEMORY hashes;
- skills/hashes;
- exact project-workflow v3.7.1;
- boards/tasks;
- Cron;
- IIP/IPM repo HEADs;
- old repo-board snapshot;
- Kanban DB backup if present;
- rollback points.

## Stage 1 — Read-Only Design/FIT-GAP

This is the ONLY stage authorized by this prompt.

Return the A–O report below.

Then STOP.

Founder reviews.

## Stage 2 — Staged Context + Skill Governance

ONLY after explicit Founder approval.

Use migration branch/staging profile.

Prepare:
- profile descriptions;
- shared IIP Research SOUL candidate;
- IPM SOUL candidate;
- AGENTS cleanup candidate;
- universal project-workflow autoload removal;
- canonical skill ownership/permissions;
- write-approval benign smoke test if approved;
- project-workflow v3.8 candidate;
- skill-shadow scan.

Do not switch production yet.

Founder gate.

## Stage 3 — Non-Canonical Single-Board Technical Pilot

Use ONE Hermes board, but PILOT TASKS ONLY.

Do NOT mirror live production tasks.

Test:
- IIP multi-profile task;
- sanitized IPM task;
- workspaces;
- block/unblock;
- comments;
- dependencies;
- restart durability;
- failure handling;
- worker lifecycle;
- privacy scan;
- localhost dashboard;
- filesystem isolation verdict.

Old repo board remains authoritative for production during this stage.

Founder gate.

## Stage 4 — Project Workflow v3.8 Engineering Pilot

Run v3.8 candidate on ONE bounded engineering task.

Verify:
- engineering-only scope;
- no ALL-task autoload;
- Kanban owns task state;
- model routing not hard-coded;
- project closeout narrowed;
- Council separated from research audit;
- locked tests/Evidence QA remain strong.

Rollback to v3.7.1 if quality regresses.

Founder gate.

## Stage 5 — Discovery Recall v1.1 Kanban Pilot

Run a bounded non-canonical Discovery Audit graph or Founder-approved slice.

Do not mirror a live repo-board task.

Verify:
- child ownership;
- recall proxies;
- rejected-item audit;
- Close System underlying + wrapper coverage;
- no research-capacity flood;
- no domain-state mutation.

Founder gate.

## Stage 6 — Gemini Deep Research v1.4 Kanban Pilot

Use:
- a Founder-designated suitable live Research Mandate; OR
- a bounded rehearsal using an already-published case.

Do not dual-track the same live mandate across two board systems.

Verify:
- anti-anchoring;
- isolated Gemini lane;
- source admission;
- Facts Locked;
- logical Publication Fact Packet/equivalent;
- Thai editorial;
- semantic fidelity;
- bounded A/B calibration;
- browser/auth failure behavior.

Founder gate.

## Stage 7 — Production Cutover

Only after Stages 0–6 PASS.

Then:
- freeze old repo-board writes;
- migrate live work;
- move durable non-board history;
- relocate formal Hold artifacts;
- supersede old repo-board governance/11-column references;
- rewire `/kanban` using governed engineering workflow and Hermes-native task states;
- rewire `/org-office`;
- verify both views use same Hermes DB/API;
- migrate approved Cron jobs to idempotent task triggers where beneficial;
- reconcile old/new live work.

Founder cutover gate.

## Stage 8 — Delete Old Repo Board

Only after independent migration reconciliation passes.

Delete:
- old board state files;
- cards;
- writer/parser;
- old adapter;
- obsolete board-specific tests/UI state logic.

Keep:
- git history;
- ONE migration evidence artifact.

Do not leave an archive board in the working tree.

## Stage 9 — Post-Cutover Observation / Audit

Monitor:
- worker failures;
- backlog;
- board privacy;
- skill/memory pending queues;
- skill shadows;
- handoff quality;
- IIP/IPM leakage;
- context/token load;
- research quality;
- Cron duplication;
- UI consistency.

Do not enable broad auto-decomposition until this observation period passes.

---

# Your FIRST RESPONSE — EXACT STRUCTURE

This prompt authorizes STAGE 1 ONLY.

Return:

## A. Runtime Reality
- Hermes version;
- profile inventory;
- board inventory;
- config/toolsets;
- gateway/dispatcher;
- dashboard bind;
- approvals;
- Cron;
- IIP/IPM paths.

## B. Current Harness FIT-GAP
Compare current reality against Harness v1.1.

## C. Single-Board Migration Plan
Exact:
- migrate;
- move;
- delete;
- retain;
- legacy ID handling;
- governance-contract supersession;
- retirement of old 11-column UI semantics;
- rollback.

## D. IIP/IPM Privacy + Filesystem Isolation Review
Include:
- tenant limitation;
- workspace isolation;
- attachments;
- board leak surface;
- dashboard exposure;
- hard isolation feasibility;
- residual risk.

## E. Profile Plan
For every relevant profile:
- keep/retire/create;
- description;
- SOUL;
- model/toolsets;
- workspace;
- tenant;
- memory.

## F. Context Plan
- one shared IIP Research SOUL;
- IPM SOUL;
- AGENTS cleanup;
- PRINCIPAL role contracts;
- `.hermes.md` conflicts;
- legacy `user.md`.

## G. Project Workflow v3.7.1 Disposition
Report:
- exact path/hash;
- duplicates/shadows;
- companion skills/scripts;
- current autoload paths;
- responsibility overlap;
- KEEP / RE-SCOPE / SPLIT / RENAME / RETIRE verdict;
- proposed v3.8 architecture/diff;
- state/Council/model/session changes.

## H. Skills Plan
Inventory current skills and map to target responsibilities.
List:
- keep;
- merge;
- retire;
- create;
- shadow conflicts;
- write permissions;
- write-approval smoke test.

## I. Memory Plan
- USER;
- MEMORY;
- duplicate cleanup;
- write approval;
- Session Search;
- Obsidian;
- Gemini Notebook;
- external memory provider recommendation.

## J. Kanban Config
Give exact installed-version keys and recommended initial values.
Flag any key in the handoff that is stale or invalid.

## K. UI / Org Office Plan
How `/kanban` and `/org-office` become views of ONE Hermes work-state source.

## L. Cron / Automation Plan
Which current jobs should later create idempotent Kanban tasks and which should stay unchanged.

## M. Companion Workstream Mapping
Show exactly how:
- Discovery Recall v1.1;
- Gemini Deep Research v1.4;
run through the new Harness without analytical modification.

## N. Safe Integration Plan
Translate Stages 0–9 above into exact local actions, evidence, tests, rollback points, and Founder gates.

## O. Founder Decisions Required
Smallest explicit decisions needed to authorize Stage 2.

Then STOP.

---

# Prohibited in This First Response

Do NOT:
- edit repo;
- edit config;
- edit profiles;
- change SOUL;
- change AGENTS;
- write/approve memory;
- edit skills;
- create v3.8;
- mutate Kanban;
- migrate old cards;
- change Cron;
- rewire UI;
- delete anything;
- implement Discovery changes;
- start Gemini Deep Research.

This round is evidence-based design review only.

The objective is a safe, reversible integration plan before the largest Hermes Harness upgrade in this project.
