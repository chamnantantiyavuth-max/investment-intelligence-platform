# STAGE 2C — SOUL Instruction Migration Matrix

**Purpose:** Map every binding instruction in the current composed SOULs (shared/SOUL.md 25.7KB + per-profile project-context splice, composed by sync-governance.py) to exactly one destination. Prove 0 binding instructions lost BEFORE any profile SOUL converges.
**Status (P4 correction, Stage 2.1):** This matrix is an **approved ARCHITECTURAL MAP** — it is NOT yet a completed zero-binding-loss proof. The actual normative-clause inventory (~45–55 clauses) must be extracted and 100% mapped/verified before any production SOUL convergence. **Stage 3 Kanban pilot continues using current production SOULs** — no candidate SOUL activation without independent completion + separate Founder approval of the proof.
**Date:** 2026-08-12
**Evidence:** shared/SOUL.md (3,244 words, 21 sections), shared/project-context/<profile>.md (18 files), profiles/iip/SOUL.md + org-cos/SOUL.md (composed samples, verified identical except splice + 2 minor line diffs)

---

## 1. Architecture of current SOUL (verified)

```
shared/SOUL.md (canonical, contains <!-- PROFILE_CONTEXT_BEGIN/END --> markers)
        │  sync-governance.py compose_soul() splices:
        │  shared/project-context/<profile>.md  → between markers
        ▼
profiles/<p>/SOUL.md   (per-profile composed file, ~26KB each)
```

- All 21 profile SOULs are composed from ONE canonical + per-profile context splice.
- iip vs org-cos SOUL diff = ONLY 3 lines: (1) model-routing pilot note wording, (2) Sol reasoning line (medium→high — now stale after FD #93 fix), (3) the spliced project-context block. No other divergence → convergence is low-risk.
- **v0.20.0 has NO SOUL inheritance/pointer mechanism** — convergence means same content composed per profile, not a filesystem pointer (matches Founder constraint).

## 2. Instruction Migration Matrix (clause-by-clause)

| # | Existing SOUL clause (shared/SOUL.md) | Type | Destination | Preserved verbatim? |
|---|---|---|---|---|
| 1 | Base identity intro (Hermes Agent, Nous Research) | Identity | **new shared IIP Research SOUL** (keep base identity line) | Yes (rewritten concise) |
| 2 | Verify-First Rule (FD-HERMES-003) | Project rule | **AGENTS.md** (already present, §Verify-First Rule) | Yes — already duplicated in AGENTS |
| 3 | Audit Delegation Rule (FD-HERMES-007) | Project rule | **AGENTS.md** (already present) | Yes — already duplicated |
| 4 | Production-Ready Audit Gate (FD-HERMES-010) | Project rule | **AGENTS.md** (already present) | Yes — already duplicated |
| 5 | LLM Council Gate (FD-2026-08-01-LLM-COUNCIL v3.7.1) | Procedure | **project-workflow v3.8** (engineering Council only) + `llm-council` skill | Yes (re-scoped engineering) |
| 6 | Founder Context | Identity/user | **SOUL** (keep) + USER.md | Yes |
| 7 | Communication Style | Identity | **SOUL** (keep) | Yes |
| 8 | Governance Sync Gate (FD-HERMES-008) | Procedure | **hermes-harness-admin skill** (Stage 2E) + AGENTS | Yes |
| 9 | Obsidian Memory Recall Rule (FD-HERMES-009) | Procedure | **obsidian-memory skill** (already owns this) | Yes |
| 10 | Obsidian Memory Capture Rule (FD-HERMES-010) | Procedure | **obsidian-memory skill** (already owns this) | Yes |
| 11 | Session Protocol (Loop Protocol v3) | Procedure | **AGENTS.md** (already present, Complete Loop Protocol) | Yes — already duplicated |
| 12 | PROJECT_STATE.md Single Source + Closeout Gate | Project rule | **AGENTS.md** + project-workflow v3.8 (project-level closeout) | Yes |
| 13 | Workflow Rules (Bible-first, Domain Guardrail, Pre-Implementation Gate, Closeout Checklist) | Project rule | **AGENTS.md** (already present) | Yes — already duplicated |
| 14 | Core Principle: Work Smart (FD-2026-07-28-SMART-SCOPE) | Project rule | **AGENTS.md** + project-workflow v3.8 | Yes |
| 15 | Automated Gate Enforcement (v3.3) | Procedure | **project-workflow v3.8** (engineering gate-check/isolation-scan only) | Yes (re-scoped) |
| 16 | Model Routing (3-Tier) — Flash/Sol/Luna table + fallback | Config/FD | **config.yaml + FOUNDERS-DECISIONS (FD #93)** — runtime routing, NOT in SOUL | Yes (content moved to config; SOUL holds one pointer line) |
| 17 | UI/Design Rules (borderless, browser-first, fonts) | Procedure | **ui-dashboard-workflow skill** + design-system/MASTER.md | Yes |
| 18 | Documentation Rules (Thai PDF Cordia etc.) | Procedure | **ui-dashboard-workflow skill** / iip-ui-design skill | Yes |
| 19 | Project Context (PROFILE_CONTEXT_BEGIN/END splice) | Role identity | **profile description (profile.yaml)** + **PRINCIPAL.md** (canonical role contracts in repo) | Yes — splice moves to description/PRINCIPAL |
| 20 | Central Knowledge Base (vault pointer) | Reference | **AGENTS.md** (pointer line) | Yes |
| 21 | Vault Brain (FD-INFRA-032) | Procedure | **knowledge-management skill** + AGENTS pointer | Yes |

**Per-profile splice destinations:**

| project-context file | Destination |
|---|---|
| iip.md (IIP identity/purpose/SACRED) | iip profile description + PRINCIPAL (control) |
| org-cos..org-radar-scout (11 role identities + SACRED) | respective profile descriptions + `operational/hermes-organization/roles/0X/PRINCIPAL.md` (repo, canonical) |
| other projects (capcmd, fxtrading, notebooklm etc.) | their own profile descriptions — NOT part of IIP convergence |

## 3. Zero-Binding-Loss Proof Method

1. **Extract** every normative sentence from shared/SOUL.md (verbs: MUST/MUST NOT/ห้าม/ต้อง/never/always + rule tables) → clause inventory (target ~45–55 clauses from 21 sections).
2. **Map** each clause to its destination (matrix above) — 1:1, no merge that drops wording.
3. **Verify** each destination file already contains the clause (AGENTS.md duplicates confirmed for #2,3,4,11,13 — grep-verified) OR the candidate file (new SOUL/v3.8/skill) carries it.
4. **Compose test:** after candidate SOUL + destination edits, run a script that greps the union of (candidate SOUL + AGENTS + v3.8 + skills + config pointers) for every clause keyword → missing = binding instruction lost → FAIL.
5. **Hash check:** candidate composed SOUL for iip/org-cos/org-data-steward must be byte-identical across the 3 pilots except the spliced identity block.

## 4. Candidate — Shared IIP Research SOUL (from Harness v1.1 §18)

```markdown
You are a rigorous investment research professional serving the Founder.

Truth is more important than agreement.
Evidence is more important than narrative confidence.
A clear "unknown" is better than a polished guess.

Think independently before reading other analysts' conclusions when the workflow
requires anti-anchoring.

Distinguish fact, source claim, inference, estimate, uncertainty, and judgment.

Actively look for evidence that could disprove the current interpretation.

Do not create artificial consensus.
Preserve material dissent.
Do not infer Founder approval from silence or prior discussion.

Communicate naturally and directly.
When writing for the Founder in Thai, use clear natural Thai rather than literal
translation or generic AI prose.

Project authority and operating rules come from the active workspace's AGENTS.md,
approved repository artifacts, role contract, and task-loaded skills.

Do not treat memory, chat history, model output, or Kanban comments as canonical truth.
```

- **Size:** ~1,100 chars (vs 26KB composed) — >90% reduction.
- **Carries:** identity, intellectual temperament, communication style, uncertainty/disagreement relationship. NOTHING else (per Harness §17 SOUL doctrine).
- **Role identity** comes from profile description + PRINCIPAL.md + task skills (Harness §18).

## 5. Pilot Profiles (iip, org-cos, org-data-steward) — Staged Proof

Stage 2 constraint: **no production switch.** Proof in staging worktree (`iip-harness-prep`):

1. Write candidate to `evidence/harness/soul-candidates/SOUL-iip-research-candidate.md` (this section).
2. Simulate compose: candidate + existing project-context splice → confirm per-profile identity preserved.
3. Diff old composed SOUL vs (candidate + destinations) — every clause accounted.
4. IPM SOUL (2.6KB, separate identity) — **untouched, preserved** (verify hash unchanged).

**Stage 3 (after approval):** switch only the 3 pilot profiles → boot test (SOUL loads, AGENTS loads, project context loads, role identity intact) → then expand.

## 6. Sync-governance.py Implication (must fix in Stage 3, not now)

- `sync-governance.py` composes SOUL from shared/SOUL.md — the canonical must become the NEW research SOUL (or the script learns per-project SOUL selection).
- Script PROFILES list must gain `org-radar-scout` (currently missing — Stage 1.1 finding) before any sync run that touches org profiles.
- **Stage 2 does NOT edit sync-governance.py** (would mutate production sync behavior) — flagged for Stage 3.

---
<!-- 2026-08-12 19:10:33 +0700 — M1: captured via scripts/artifact_timestamp.py (system clock at correction; agent-guessed timestamps rejected) -->
