# AGENTS.md

## Authority

Read and follow, in order:

1. `02-PROJECT-CONSTITUTION.md`
2. `operational/FOUNDERS-DECISIONS.md`
3. Approved domain specifications
4. Approved ADRs
5. Approved implementation plans

AI-generated suggestions do not override approved documents.

## User Context

The Founder is the product and investment-domain owner, not a professional software engineer. Do not treat visible approval as proof of technical correctness.

Use tests, evidence, reproducibility, and explicit acceptance criteria.

## Core Rules

- Plan substantial work before implementation.
- Challenge unsafe, contradictory, or unnecessary requirements.
- Separate facts, assumptions, hypotheses, and decisions.
- Do not invent missing domain rules.
- Do not hide uncertainty or conflicting evidence.
- Do not change official scoring logic without an approved, versioned proposal.
- Do not access the legacy repository unless a task explicitly authorizes a narrow inspection.
- Do not introduce broker connectivity, execution, or portfolio allocation.
- Do not read or expose secrets.
- Use synthetic or sanitized data initially.
- Do not perform broad refactors without a rollback point and approved plan.
- Do not claim completion without verification.
- Keep Theme Quality, Candidate Quality, Entry Readiness, and Data Confidence separate.
- Experimental Themes must not affect official strategy rankings.
- Preserve history, dissent, and evidence lineage.

## Current Project Phase

Constitution and Product Definition.

Do not write application code, select a final technology stack, install dependencies, or create migrations unless explicitly authorized by a later approved phase.

## Working Method

For substantial tasks:

1. Restate the goal.
2. Identify constraints.
3. List assumptions and deferred decisions.
4. Produce a file-by-file or task-by-task plan.
5. Stop at the requested gate.
6. Implement only after approval.
7. Verify independently.
8. Report unresolved issues honestly.
