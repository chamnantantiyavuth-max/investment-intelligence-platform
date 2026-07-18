# Change Control and Approval

## Status

Candidate v0.2 operational policy.

## Material Change

A change is material when it affects one or more of:

- constitutional meaning or Founder’s Decisions;
- domain definitions, invariants, or lifecycle transitions;
- strategy eligibility, filters, scores, weights, thresholds, rankings, or official outputs;
- evidence lineage, source independence, point-in-time correctness, or reproducibility;
- AI model, prompt, or workflow used to produce official classifications or rankings;
- security, privacy, retention, deletion, access, or secrets;
- schemas, migrations, destructive operations, or irreversible data transformations;
- external data-source contracts or public APIs;
- module boundaries, major dependencies, or deployment topology;
- human approval, override, or audit behavior.

## Required Material Change Proposal

Before implementation, provide:

1. change title and identifier;
2. problem statement;
3. affected authoritative documents;
4. proposed behavior;
5. alternatives considered;
6. domain and user impact;
7. data and migration impact;
8. security and privacy impact;
9. verification plan;
10. rollback or recovery plan;
11. unresolved risks;
12. exact approval requested.

## Approval

Approval must identify the proposal, plan, artifact, or transition being approved.

Casual agreement to a discussion is not approval of unnamed material work.

## Implementation

After approval:

- create a Git checkpoint;
- implement only the approved scope;
- run the verification plan;
- report deviations;
- inspect the final diff;
- update version and decision history.

## Emergency Rule

No emergency exception exists during the initial project phases. Stop and ask.
