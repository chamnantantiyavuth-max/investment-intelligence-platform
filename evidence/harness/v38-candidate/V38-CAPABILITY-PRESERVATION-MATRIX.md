# P5 — v3.7.1 → v3.8 Capability Preservation Matrix

**Purpose:** Classify EVERY meaningful v3.7.1 capability before v3.8 promotion. Prevents silent feature loss in the workflow that has been iterated many rounds.
**Status:** Required pre-Stage-4 review item (P5). v3.8 NOT promoted.
**Date:** 2026-08-12
**Source:** installed `project-workflow` v3.7.1 (hash d296a7af8d604481..., 43,761 bytes, 26 identical copies) + v3.8 candidate (`evidence/harness/v38-candidate/SKILL.md`)

---

## Capability Matrix

| # | v3.7.1 capability | Verdict | v3.8 disposition |
|---|---|---|---|
| 1 | Bible / authoritative-source discipline (Pillar 1) | **KEEP** | §Core Principles #1 — same |
| 2 | SMART-SCOPE (Pillar 2, FD-2026-07-28) | **KEEP** | §Core Principles #2 — same |
| 3 | Domain Guardrail / Spec-before-Answer (Pillar 3) | **RE-SCOPE** | engineering domain drift only; research side owns its own guardrail (research skills) |
| 4 | Identity Card in MEMORY (Layer 1 — ~250 chars domain checksum) | **RETIRE** | Harness §24: domain truth out of MEMORY; AGENTS/specs own it (already partially in AGENTS Domain Index) |
| 5 | Critical / Quick mode selection | **KEEP (re-scoped)** | engineering scope only; Quick/Critical do NOT apply to research |
| 6 | Blacklisted paths (src/auth, broker, ml, migration, calc, schema, audit) | **RE-SCOPE** | project/task-specific risky paths derived from AGENTS + task contract + repo architecture; universal blacklist removed (Harness §24) |
| 7 | Text-Only Quick Mode exception (v3.7.1) | **KEEP** | inherited — text/CSS-only in risky path allowed with `[quick-text-only]` tag |
| 8 | Loop Protocol v3 (session start sequence) | **MOVE** | AGENTS.md owns it (already duplicated there); v3.8 references it for engineering sessions |
| 9 | Session Preflight Check (`session-preflight.sh`) | **KEEP** | engineering sessions; script referenced in v3.8 verification path — **explicitly preserved (P5 focus item)** |
| 10 | Project Truth Map (`PROJECT_TRUTH_MAP.md`) | **KEEP** | engineering projects; **preserved (P5 focus item)** — references/ template stays |
| 11 | §0A Systemic Quality Gates (Root-Cause, Validation Boundary, Deployment Verify, Feature Complete, Batch Atomicity, Verification Evidence Tags) | **KEEP** | merged into v3.8 Verification section (gates 1–6 retained; evidence tags retained) |
| 12 | §0B Automated Gate Enforcement (gate-check.sh, isolation-scan.sh, closeout_status, regression_count, Parent re-verify) | **KEEP** | v3.8 Verification + Rollback sections; scripts project-adapted |
| 13 | §0C LLM Council (Bible/Plan/Milestone/Final gates + Artifact Gate) | **RE-SCOPE** | Engineering Council only (material engineering decisions); research uses CRO/audit chain — separation explicit (Harness §24) |
| 14 | Milestone Council Materiality Rule (v3.7.1) | **KEEP** | engineering milestones only; routine → Parent Evidence QA |
| 15 | Closeout Checklist (8 items) | **RE-SCOPE** | project-level closeout for material sessions/milestones/releases; NOT per-worker (Kanban owns worker continuity) |
| 16 | PROJECT_STATE.md / SESSION_CLOSEOUT.md roles | **RE-SCOPE** | project-level only; Kanban = task state (Harness §24) |
| 17 | Domain Constitution Gate (Phase -1: PROJECT_BIBLE/DOMAIN_MODEL/FORBIDDEN_ACTIONS/ACCEPTANCE_EXAMPLES) | **RE-SCOPE (conditional)** | net-new governed project or material domain redesign only; existing project with authority → read existing, no duplicate creation |
| 18 | Phase Flow (0→-1→1→2→2R→3→4→5→6→7) | **KEEP** | engineering phases unchanged |
| 19 | Phase 2R hostile review (Sol Medium) | **KEEP** | engineering architecture review via approved independent routing (model names not hard-coded) |
| 20 | Regression budget (max 2, 3rd → Founder) | **KEEP** | retained in engineering task contracts |
| 21 | Financial Logic Rule (Parent handles; Sol forbidden) | **RE-SCOPE** | "financial logic" = implementation/calculation/system behavior; NOT investment reasoning (Harness §24 clarification) |
| 22 | Per-task state machine (BACKLOG→QUEUED→IN PROGRESS→DONE + RETRY/BLOCKED/CANCELLED) | **RETIRE** | Hermes Kanban owns durable task state; no parallel machine (Harness §24) |
| 23 | Task Isolation Contract (worktree, owned/forbidden paths, locked_tests, depends_on) | **KEEP** | retained; forbidden_paths per-project |
| 24 | Locked Acceptance Tests (immutable, spec-as-code) | **KEEP** | same |
| 25 | Acceptance Lock Rule (no expected-value change without Bible quote) | **KEEP** | same |
| 26 | Canonical Test Rule (acceptance examples → automated tests) | **KEEP** | same |
| 27 | Evidence QA 10-point checklist | **KEEP** | compressed into v3.8 Verification (all 10 points retained) |
| 28 | Mutation Testing Lite (v3.7.1) | **KEEP** | **preserved (P5 focus item)** — references/mutation-testing-lite.md |
| 29 | Property/Invariant Testing (v3.7.1) | **KEEP** | **preserved (P5 focus item)** — references/property-invariant-testing.md |
| 30 | Escalation Ladder (L1–L4) | **KEEP** | engineering; independent-review routing by runtime config |
| 31 | 3-Tier Model Routing table (Flash/Sol/Luna hard-coded) | **RETIRE (hard-coding)** | routing lives in config/FD; v3.8 references "currently approved independent-review routing" |
| 32 | Config Dependencies block (hard-coded model names) | **RETIRE (hard-coding)** | same as #31 |
| 33 | UI Dashboard Plugin (ui-dashboard-workflow delegation) | **KEEP** | retained — UI implementation routes to ui-dashboard-workflow |
| 34 | Related Skills list (26 companions) | **RE-SCOPE** | pruned to non-overlapping engineering companions; stale refs (project-state-sync, workflow-retrofit, etc.) dropped |
| 35 | Reference scripts (gate-check-template.sh, isolation-scan.sh) | **KEEP** | retained (project-adapted) |
| 36 | Reference files (milestone-evidence-log.md, workflow-cheat-sheet.md, project-truth-map-template.md) | **KEEP** | retained |
| 37 | Close Beta / end-to-end verification | **KEEP** | v3.8 §Verification point 6 (deployment smoke + UI browser) |
| 38 | Golden Project / regression concepts | **KEEP** | Evidence QA point 4 (no regression in critical paths) + locked suite |
| 39 | Security / secret discipline | **KEEP** | §Core Principles #8 — same |
| 40 | Rollback (every material change) | **KEEP** | §Rollback — same |
| 41 | Verification Doctrine link (operational/VERIFICATION-DOCTRINE.md) | **KEEP** | referenced in verification path |
| 42 | Audit Gate (FD-HERMES-007 delegation) | **KEEP** | engineering/governance audits delegate per audit routing (research audits separate) |
| 43 | FINISHING THE JOB rule | **KEEP** | implicit in §Core Principles + verification |

## Summary

| Verdict | Count | Items |
|---|---|---|
| KEEP | 30 | 1,2,5,7,9,10,11,12,14,18,19,20,23,24,25,26,27,28,29,30,33,35,36,37,38,39,40,41,42,43 |
| RE-SCOPE | 8 | 3,6,13,15,16,17,21,34 |
| MOVE | 1 | 8 |
| RETIRE | 4 | 4,22,31,32 |
| **TOTAL** | **43** | (M2 correction: #31/#32 are RETIRE (hard-coding), not RE-SCOPE; nonexistent `26a` removed) |

**P5 focus capabilities — all preserved:** Session Preflight (#9), Project Truth Map (#10), Property/Invariant Testing (#29), Mutation Testing Lite (#28), deterministic hooks (gate-check/isolation-scan #12), Close Beta/E2E (#37), Golden Project/regression (#38), security/secret (#39), rollback (#40), verification doctrine (#41).

**Arithmetic (M2 correction):** 43 rows = **30 KEEP / 8 RE-SCOPE / 1 MOVE / 4 RETIRE**. #31 (hard-coded model routing) + #32 (hard-coded Config Dependencies) are RETIRE — runtime config owns routing; nonexistent `26a` removed.

**Gap found during matrix:** v3.8 candidate §Verification omits explicit mention of `session-preflight.sh` + `PROJECT_TRUTH_MAP.md` + mutation/property testing references — candidate text updated below to carry these references (see v3.8 §Verification Test-Strength Checks + References).

## v3.8 Candidate Addition (from matrix gaps)

Append to v3.8 candidate §Verification:

```
### Preserved v3.7.1 machinery (P5)
- Session Preflight: `references/session-preflight.sh` (template) — run before meaningful engineering work
- Project Truth Map: `references/project-truth-map-template.md` — authoritative-source table per project
- Mutation Testing Lite: `references/mutation-testing-lite.md` — high-value financial/operational logic
- Property/Invariant Testing: `references/property-invariant-testing.md` — generated-input invariants
- Milestone Evidence Log: `references/milestone-evidence-log.md` — per-milestone evidence instrumentation
- Gate check + isolation scan: `references/gate-check-template.sh` + `references/isolation-scan.sh`
```
