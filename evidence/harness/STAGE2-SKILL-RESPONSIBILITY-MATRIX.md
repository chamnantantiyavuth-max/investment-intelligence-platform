# STAGE 2E — Skill Responsibility Overlap Matrix + Final Architecture Proposal

**Purpose:** Content-level overlap audit of existing skills vs Harness v1.1 §23 target responsibility map. Founder approves RESPONSIBILITIES first — new skill filenames only where a documented gap exists.
**Status:** DRAFT — no skill created/merged/retired in Stage 2. Actions below are recommendations for Stage 3+.
**Date:** 2026-08-12
**Method:** read SKILL.md content of every candidate-existing skill (head + workflow sections), map responsibilities, classify KEEP / EXTEND / MERGE / RETIRE / NEW.

---

## 1. Target Responsibilities (Harness v1.1 §23) vs Existing Skills

| # | Target responsibility | Existing skill (installed, skills-shared) | Coverage (content-level) | Verdict | Action |
|---|---|---|---|---|---|
| R1 | Engineering change-control workflow | `project-workflow` v3.7.1 (26 copies) | full (but universal-scope) | KEEP + RE-SCOPE | v3.8 candidate created (Stage 2D); v3.7.1 stays production until Stage 4 |
| R2 | IIP org workforce operation (11 profiles, holds, role contracts) | `iip-hermes-workforce` v1.0.0 | substantial — owns org topology, FD #54, kanban/holds mechanics, sync scripts | **KEEP NAME + EXTEND** (P7) | **P7 dependency scan (Stage 2.1):** 6 references found — `.usage.json`, `iip-phase-planning/references/reconstitution-direction-workflow-2026-08-06.md`, `research/industry-outlook-reference/SKILL.md`, `iip-ui-design/references/org-office-pixel-mockup-2026-08-07.md`, + its own SKILL.md + own reference file. **Rename to `hermes-harness-admin` REJECTED (migration risk > aesthetics).** Keep name `iip-hermes-workforce`, EXTEND responsibility to include harness-admin duties (profile inventory, config sync, skill governance, Kanban diagnostics, write-approval health). `capital-kanban` remains NEW thin (board policy only) |
| R3 | Kanban org policy (one-board, tenant iip/ipm, privacy, taxonomy) | `iip-hermes-workforce` (partial) + KANBAN-CONTRACT-v0.1.md (repo) | partial — repo contract holds columns/columns semantics; skill holds org mechanics | **NEW (thin)** | `capital-kanban` — org policy only, referencing repo contract + native kanban-worker; do NOT duplicate native lifecycle |
| R4 | Evidence procedure (source admission, PIT, lineage, management claims, correction propagation) | `sec-edgar-research` (retrieval only), `fundamental-company-research` (claim-lineage drafting), Evidence Model (repo spec) | partial across 2 skills + repo spec; no single procedure owner | **NEW (thin) or EXTEND** | `iip-evidence` — thin shared procedure referencing EVIDENCE-MODEL.md + sec-edgar retrieval; OR extend fundamental-company-research. Recommend NEW thin (evidence is cross-cutting: discovery + research + publication) |
| R5 | Deep company research (mandate → anti-anchoring → evidence → essay → cross-exam → CRO → audit → Facts Locked) | `fundamental-company-research` v1.x | substantial — CIW slice workflow + Apple research-cell workflow (Plan A §6) proven | **EXTEND** | extend with Gemini DR lane (v1.4 §4) + source-preflight + reconciliation. No new `iip-deep-research` full skill needed |
| R6 | Publication (Facts Locked → Thai editorial, token + semantic fidelity, IC Secretary managing editor) | `iip-editorial-publication` | substantial — Thai editorial standard, FACTS LOCKED, jargon firewall, category taxonomy (FD #94/96) | **EXTEND** | add Semantic Fidelity Gate F2 (v1.4 §18) + Publication Fact Packet contract (v1.4 §15) + Gemini editorial lane. No new skill |
| R7 | Discovery audit (Recall/Coverage v1.1 method) | none | none — new workstream | **NEW** | `iip-discovery-audit` — encodes v1.1 method (recall proxies, miss taxonomy M1–M7, coverage matrices) |
| R8 | IIP↔IPM handoff (one-way firewall, neutral question transformation, board sanitization) | `simulated-portfolio-office` (IPM-side: ledger/letters/IPM-FD-003) | partial — IPM side exists; IIP-side handoff contract absent | **NEW (thin)** | `iip-ipm-handoff` — IIP-side: what may flow, what never flows, sanitized artifact_ref format. IPM side stays in simulated-portfolio-office (IPM owns its skill) |
| R9 | IPM operating review (weekly review, PM letter, ledger) | `simulated-portfolio-office` | full — IPM-owned, Constitution v0.2, ledger contract | **KEEP** | no `ipm-operating-review` needed — existing skill already owns this. Rename not required |
| R10 | Independent engineering review gates | `llm-council` v1.1.1 + `governed-review-gates` v1.5.1 | full (engineering council) + full (hostile review playbook) | KEEP both | llm-council = council gates; governed-review-gates = hostile re-performance playbook. Non-overlapping with research CRO/audit (v3.8 keeps separation) |

## 2. Other Existing Skills — Classification

| Skill | Verdict | Note |
|---|---|---|
| `iip-functional-verification` | KEEP | functional smoke testing (FD-HERMES-010) — non-overlapping |
| `iip-ui-design` v2.2.0 | KEEP | IIP frontend design system (Research Desk v3.0) — non-overlapping |
| `obsidian-memory` v1.1.0 | KEEP | LTM recall/capture — memory layer, not research procedure |
| `knowledge-management` / `vault-project-notes` | KEEP | vault capture — non-overlapping |
| `fundamental-company-research` | EXTEND (R5) | base for deep-research extension |
| `sec-edgar-research` | KEEP | retrieval toolkit — referenced by iip-evidence, not replaced |
| `governed-scheduled-review` | disabled in config | legacy review cron skill — review before re-enable or retire |
| `iip-phase-planning` | disabled in config | phase planning — superseded by v3.8 scope split; retire or keep disabled |
| `project-workflow-backfill` (26 copies) | MERGE/RETIRE | stub — collapse to 1 shared copy or retire (v3.8 supersedes) |

## 3. Duplication / Shadow Facts (verified Stage 1)

- `project-workflow` SKILL.md: **26 copies** (13 profiles × 2 paths), all hash-identical d296a7af... → no content drift, but architecture-fragile. Consolidate to skills-shared (symlink already used by iip/ipm); org-* physical copies → remove after sync proves shared dir discovery works.
- `project-workflow-backfill`: 13 copies, hash-identical 7f8cb203... → stub; retire to shared if needed.
- org-* profiles: 201 physical skill copies/profile (vs 233 in shared) — snapshot drift risk; converge to symlink like iip.

## 4. Proposed Final Skill Architecture (smallest set)

```
ENGINEERING
  project-workflow v3.8        (candidate ready — Stage 2D)
  llm-council                  (keep)
  governed-review-gates        (keep)

ORGANIZATION / HARNESS
  iip-hermes-workforce         (KEEP NAME + EXTEND responsibility — P7: 6 refs; no rename)
  capital-kanban               (new thin — R3, org policy only)

IIP RESEARCH
  iip-evidence                 (new thin — R4)
  fundamental-company-research (extend — R5)
  iip-editorial-publication    (extend — R6)
  iip-discovery-audit          (new — R7)

BOUNDARY
  iip-ipm-handoff              (new thin — R8)

IPM
  simulated-portfolio-office   (keep — R9, IPM-owned)
```

**Net change vs Harness v1.1 target (8 NEW):**
- NEW actually needed: `capital-kanban`, `iip-evidence`, `iip-discovery-audit`, `iip-ipm-handoff` = **4 new**
- `hermes-harness-admin` = **NOT created** — `iip-hermes-workforce` KEEPS its name (P7: 6 references; rename risk > aesthetics) and is EXTENDED to carry harness-admin responsibilities
- `iip-deep-research` = **NOT needed** (fundamental-company-research extends)
- `iip-publication` = **NOT needed** (iip-editorial-publication extends)
- `ipm-operating-review` = **NOT needed** (simulated-portfolio-office owns)

**Exact diffs for Stage 3** (after Founder approves responsibilities): one diff per skill (extend/reshape), each with content-level change list. No skill is created/edited in Stage 2.
