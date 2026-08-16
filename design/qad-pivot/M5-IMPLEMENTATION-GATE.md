# M5-IMPLEMENTATION-GATE.md

> **Status:** ⏳ **PENDING** — not yet passed
> **Gate type:** Production code gate — clears M5 (Autonomous Discovery) and downstream implementation phases

---

## Prerequisites

| # | Requirement | Status | Artifact |
|---|-------------|--------|----------|
| 1 | Canonical QAD specs materialized (9 core + 1 evaluation) | 🔴 PENDING | `project-definition/qad/` |
| 2 | Implementation-grade JSON schemas | 🔴 PENDING | `schemas/qad/` |
| 3 | Actual 10 PIT fixtures (Named/Masked/Synthetic mix) | 🔴 PENDING | `evaluation/input-fixtures/` |
| 4 | Sealed outcomes directory with access controls | 🔴 PENDING | `evaluation-sealed/outcomes/` |
| 5 | Baseline evaluation run — all three layers demonstrated:
|- ≥1 Named Historical fixture run
|- ≥1 Entity-Masked fixture run (PASSES Mask Recognizability Check)
|- ≥1 Synthetic/Counterfactual fixture run | 🔴 PENDING | `evaluation/baseline/` |
| 6 | Critical negative tests passing:
|- NotebookLM cannot self-promote evidence
|- NotebookLM provenance survives promotion
|- Selection Engine rejects candidate missing required gates
|- Quality FAILED → NOT_QAD_QUALITY termination | 🔴 PENDING | `tests/locked/` |
| 7 | QAD role contracts approved | 🔴 PENDING | `contracts/qad/` |
| 8 | Budget/runaway controls defined and testable | 🔴 PENDING | `evaluation/EVALUATION-CONTRACT.md` |
| 9 | Founder GO | 🔴 PENDING | FD #1xx |

---

## What This Gate Unlocks

| Phase | Scope |
|-------|-------|
| M5 | Autonomous Discovery (Quality Discovery + Dislocation Radar + Selection Engine) |
| M6 | Source Intelligence / NotebookLM engineering |
| M7 | Research Workforce / Scuttlebutt |
| M8 | Analytical Core / Impairment |
| M9–M14 | Downstream implementation phases |

---

## Gate Process

1. All 9 prerequisites verified against acceptance criteria
2. Independent auditor confirms compliance
3. Founder reviews M4B evaluation evidence + implementation plan
4. Founder explicitly approves (FD)
5. Gate transitions: PENDING → PASS

<!-- 2026-08-16 UTC+7 -->