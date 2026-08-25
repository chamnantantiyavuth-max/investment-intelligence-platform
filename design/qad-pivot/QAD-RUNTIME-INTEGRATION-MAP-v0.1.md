# QAD Runtime Integration Map v0.1

> **⚠ NON-AUTHORITATIVE MAPPING INDEX — DOES NOT CREATE OR RENAME MILESTONES**
>
> This document is a cross-reference index only. It maps historical workstreams, experiments, and infrastructure to their canonical QAD Master Roadmap milestone. It does not create new milestones, rename existing ones, or grant implementation authority.
>
> Canonical master plan: `REVISED-QAD-MASTER-PLAN.md` (M0 → M15)
> Engineering harness: `project-workflow v3.8`
>
> All authority flows from approved Founder Decisions and frozen M1–M4 contracts.

---

## Mapping Index

| Historical artifact / workstream | Canonical QAD milestone | Role in current roadmap |
|---|---|---|
| **Harness Stage 6 — Gemini Deep Research** | M6 — Source Intelligence | Design evidence; adapter pattern requires M5 stores before production integration |
| **Gemini Notebook subscription / browser pilot** | M6 — Source Intelligence | Design evidence; same M5-store dependency |
| **INT-G0 / G0.1 / G1 / G1.1 — Bot integration gates** | M7 — Research Workforce / Modern Scuttlebutt | Historical test evidence and prior art; M7 will reuse findings |
| **INT-G2 — Bot integration pilot** | M7 — Research Workforce / Modern Scuttlebutt | Authorized but incomplete execution; M7 will reconcile and complete |
| **Hermes Capital Intelligence Board (existing org-* workforce)** | M7 — Research Workforce / Modern Scuttlebutt | Migration input; runtime profile changes are NOT authorized until M7 gate |
| **Council / Red Team pilot experiments** | M10 — Independent Assurance | Design evidence and process learning |
| **Reports-as-product / magazine blog / `/library`** | M11 — Thai Research PDF (precursor) | LEGACY / FROZEN per FD #62; preserved as frozen UI; M11 will produce PDF as primary Founder output |
| **Bot Founder Discussion / group chat concepts** | M7 + M11 interaction layer | Conceptual only; no implementation |
| **RQ on-demand research protocol** | M6 / M7 / M11 runtime protocol | Conceptual only |
| **Gold watch-item / CIW monitoring** | M12 — Thesis Monitoring | DEFERRED; no system design or cron automation |
| **Obsidian integration / learning loop / memory** | M13 — Knowledge Compounding | DEFERRED; learning-loop cron exists but M13 scope not started |
| **Original web platform (frontend)** | LEGACY / FROZEN | Frozen per FD #62; no deletion, not active development |
| **project-workflow v3.8** | ENGINEERING HARNESS | Active; unchanged boundary per AGENTS.md |
| **Harness Stages 1→7 (cutover complete)** | M5–M7 supporting evidence | Preserved as implementation evidence |

---

## What this map does NOT do

1. **Does not create new milestones.** All milestones are defined in the canonical Master Plan only.
2. **Does not rename milestones.** M5 = Autonomous Discovery, M7 = Research Workforce / Modern Scuttlebutt remain unchanged.
3. **Does not grant implementation authority.** Each milestone requires its own Founder gate.
4. **Does not resurrect historical plans.** INT-G, Harness, and Gemini workstreams are not parallel master roadmaps.

## What this map IS for

- Preventing future sessions from treating historical workstreams as competing master plans
- Providing a quick reference for "where does X belong?"
- Preserving design and test evidence without reviving old governance

---

## Current execution lane (as of 25 Aug 2026)

| Layer | Status |
|---|---|
| M5.2 correction (items 1–3) | ✅ DONE + PUSHED |
| M5.2 correction (items 4–14) | ⚠ IN PROGRESS — NEXT |
| M5.3 PIT Runtime Enforcement | ⏳ HOLD |
| Remaining M5 foundations (retry, cost, fixtures) | ⏳ HOLD |
| M5 Autonomous Discovery capability delivery | ⏳ HOLD |
| M6 — M7 — M8 — M9 — M10 — M11 — M12 — M13 — M14 — M15 | ⏳ NOT STARTED |

**Boundaries:**
- M5 implementation is **AUTHORIZED** (FD #135)
- Production Release / Live Autonomous QAD / workforce cutover / cron cutover = **NOT AUTHORIZED**
- Bot Mode, Gemini Notebook/DR engineering, monitoring automation = **NOT STARTED**

<!-- 2026-08-25 00:00 UTC+7 -->