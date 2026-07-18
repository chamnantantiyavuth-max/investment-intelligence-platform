# Verification Doctrine

## Status

Candidate v0.2 operational policy.

## Principle

Passing tests is necessary but not sufficient when the tests and implementation may share the same mistaken interpretation.

## Required Evidence by Change Type

### Documentation and Product Definition

- contradiction review;
- terminology review;
- authority review;
- scope/non-scope check;
- confirmation that no code, dependency, migration, or final stack was introduced.

### Material Domain Logic

- approved acceptance criteria;
- known-answer or golden fixtures independent of implementation;
- boundary and failure cases;
- point-in-time and lineage checks where applicable;
- independent review of source and diff;
- reproducible commands and outputs.

### Scoring or Ranking Changes

- rule/version change record;
- before/after candidate-impact report;
- changed inclusion/exclusion examples;
- regression fixtures;
- explanation of unexpected movements;
- Founder approval when official behavior changes.

### Data Transformations

- raw-source preservation;
- transformation version;
- reconciliation totals;
- missing/conflict behavior;
- rerun reproducibility;
- downstream invalidation plan.

## Independent Review

A reviewer must not rely solely on the executor’s summary.

The reviewer should inspect the relevant source or diff, run checks, and evaluate the result against approved domain semantics.

For high-impact logic, prefer a separate session, agent, or model when practical.

## Conflict Rule

If tests pass but approved domain semantics appear violated, stop.

Tests do not override the Constitution or approved domain specifications.

## Completion Report

A completion claim must include:

- scope completed;
- files changed;
- commands run;
- tests/checks and results;
- known limitations;
- unresolved risks;
- deviations from plan;
- Git status and diff summary.

Do not claim completion from appearance or narrative confidence.
