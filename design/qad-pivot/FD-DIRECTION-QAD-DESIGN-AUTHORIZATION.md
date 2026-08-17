# FD Direction — QAD Design Authorization

> **Status:** 🔴 **SUPERSEDED — HISTORICAL DESIGN ARTIFACT.** Authority moved to FD #130 (QAD Architecture Design Gate, approved 16 Aug 2026), Constitution v0.6, ADR-130, and M5-IMPLEMENTATION-GATE.md. This file is preserved for lineage only — do not use as current authority.

> **This is a single Direction FD — NOT an implementation authorization.**
> FD #130 (proposed — pending Founder review and acceptance)

## Direction

**QAD-M0 audit is accepted with Required Changes.** The QAD-specialized design work for the Investment Intelligence Platform may proceed through M4 (Domain Contracts + Schemas + Evaluation Contract) and through Packs A/B/C design artifacts.

**NOT authorized by this direction:**
- Any production code, pipeline, or database implementation
- Any constitution amendment (amendment text must be presented for explicit review first)
- Any physical file/directory archival or deletion
- Any model-routing changes
- Any workforce profile reframing
- Any PDF renderer selection or font lock
- Any autonomous research selection or publication
- Any CD/broker/execution/allocation changes

## Required Changes (from M0 audit)

1. **Evaluation Contract before M5 coding** — split M4 into M4A (Schemas) + M4B (Evaluation Contract + PIT fixtures + acceptance cases + cost controls)
2. **Capability-level legacy map** — do not supersede/archive by module name; map actual capabilities
3. **Provider-agnostic architecture** — QAD must use `Role → Tier → Routing Policy → Provider`; OpenRouter is NOT a QAD dependency
4. **Role contracts before workforce reframe** — create logical QAD role contracts in Pack A first; workforce migration map second
5. **NotebookLM contracts in M3/M4** — Research Request, Result, Provenance, Source Validation contracts defined before M6 engineering
6. **PDF tech unlocked** — define Publication Contract + Thai Typography Standard + Visual Acceptance Tests; renderer selected at M11 via comparative benchmark
7. **Single direction FD only** — no batch-approving FD #130–137; material Constitution/Plan/Model-Tier FDs presented with actual artifact text
8. **M2 semantic states** — `ACTIVE → FROZEN → SUPERSEDED → VERIFIED_UNUSED → ARCHIVED`; physical moves at M15 only

## Founder Answers to Open Questions

| Q | Decision |
|---|----------|
| Q1: New profile? | **Stay in `iip`** — QAD is the new IIP identity, not a separate project |
| Q2: Reframe org profiles? | **Not yet** — logical contracts first, workforce mapping second |
| Q3: 34 existing reports? | **Preserve all** — historical/pre-QAD artifacts, never rewrite history |
| Q4: CIW? | **Absorb into QAD** — keep lineage: CIW Result Contract + Quality Gates → QAD Research Protocol |
| Q5: NotebookLM production? | **Contracts M3/M4, engineering M6** |

## What This Unlocks

The following design-only workstreams may proceed:
- M1 drafts (Constitutional Pivot text, Manifesto/DNA/Vision/Scope amendments) — **present for review, do not ratify**
- M2 logical boundary map — capability-level, not physical
- M3 QAD Domain Contracts (17 spec documents)
- Pack A — Production Role Contracts (logical QAD roles, not reframed workforce)
- Pack B — Canonical Schemas & State Machines (incl. NotebookLM contracts)
- Pack C — Evaluation Contract + PIT Fixtures + Acceptance Cases + Cost Controls
- M4A — Canonical Schemas & State Machines
- M4B — Pre-Code Evaluation Contract

## Next Gate

**PRE-CODE DESIGN GATE** — after Packs A/B/C complete + independent adversarial review + Founder review:
- Domain Contracts approved?
- Role Contracts approved?
- Schemas approved?
- Evaluation Contract + fixtures approved?
- Cost/runaway controls approved?

Only then may M5 (Autonomous Discovery) production coding begin.

<!-- 2026-08-16 UTC+7 -->