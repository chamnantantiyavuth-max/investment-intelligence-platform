# STAGE 2.1 — Pre-Flight Closure Report (P1–P7)

**Status:** Stage 2 = PASS WITH PRE-STAGE-3 FIXES → P1–P7 COMPLETE. Stage 3 NOT started (awaiting Founder confirmation after this report).
**Date:** 2026-08-12
**Branch:** `harness/stage2-prep` (worktree `C:/Users/Admin/Desktop/Antigravity/iip-harness-prep`)

---

## P1 — Canonical Founder Decision Lineage ✅

- **Vault register:** FD-98 added (12 Aug row; verified present — M3 corrected from "11 Aug")
- **Repo register:** FD-98 added to `operational/FOUNDERS-DECISIONS.md` **item 114** on the clean `harness/stage2-prep` branch (main dirty tree untouched) — exact same Stage 2 scope as vault entry
- Both registers now carry the identical authorization text. Stage 3 authorization will be recorded through the same dual-register mechanism.

## P2 — Clock / Timezone Integrity ✅ (root cause found — no system fault)

| Source | Value |
|---|---|
| Windows system time | 2026-08-12 19:00:08 +07:00 (SE Asia Standard Time, UTC+7 Bangkok) |
| UTC | 2026-08-12 12:00:08 |
| Python datetime (local/utc/bangkok) | 19:00:08 / 12:00:08 / 19:00:08+07:00 — all consistent |
| TZ env | empty (Windows-native timezone used) |
| Timezone registry | `SE Asia Standard Time (UTC+07:00) Bangkok, Hanoi, Jakarta` — correct |

**Root cause of the anomaly:** NOT clock skew, NOT timezone bug. The `2026-08-12 20:30 UTC+7` value was an **agent hard-coded fixed timestamp** written into file footers by me (Hermes) during Stage 1/2 artifact creation, instead of reading the system clock. System time was consistently 19:00 UTC+7.

**Correction applied:**
- Corrected footers: vault fd-register FD-98 row + `evidence/harness/STAGE1-REPORT-2026-08-12.md` → `19:10 UTC+7` with annotation
- **Process rule (standing):** artifact timestamps MUST be read from the system clock (`date`/Python datetime) at write time — never hard-coded by the agent. No PIT research/audit workflow may use agent-generated timestamps as evidence of write time.

## P3 — Stage 2 Artifacts Preserved ✅ (commit below)

- Commit of all Stage 2 artifacts + P1 FD-98 repo entry to `harness/stage2-prep` — see commit SHA in Git record (section at bottom).
- NO merge to main. Rollback = delete worktree + branch.
- Immutable checkpoint BEFORE any Stage 3 mutation.

## P4 — SOUL Zero-Loss Status Correction ✅

- `STAGE2-SOUL-MIGRATION-MATRIX.md` status updated: **approved ARCHITECTURAL MAP, NOT a completed zero-binding-loss proof**.
- Actual normative-clause inventory (~45–55 clauses) → extract + map 100% + verify destinations + prove zero loss → **required before any production SOUL convergence** (separate Founder approval).
- **Stage 3 Kanban pilot uses current production SOULs — no candidate SOUL activation.**

## P5 — v3.8 Candidate Consistency ✅

- **Stale skill references corrected:** `iip-deep-research` → `fundamental-company-research`, `iip-publication` → `iip-editorial-publication`, `ipm-operating-review` → `simulated-portfolio-office`, `hermes-harness-admin` → `iip-hermes-workforce` (P7).
- **Capability Preservation Matrix created:** `evidence/harness/v38-candidate/V38-CAPABILITY-PRESERVATION-MATRIX.md` — 43 v3.7.1 capabilities classified: **30 KEEP / 10 RE-SCOPE / 1 MOVE / 2 RETIRE**.
  - P5 focus items ALL preserved: Session Preflight (#9), Project Truth Map (#10), Property/Invariant Testing (#29), Mutation Testing Lite (#28), deterministic hooks (#12), Close Beta/E2E (#37), Golden Project/regression (#38), security/secret (#39), rollback (#40), verification doctrine (#41).
  - RETIRE only: Identity Card in MEMORY (#4 — Harness §24: domain truth out of memory), per-task state machine (#22 — Kanban owns task state).
  - Gap found & fixed: v3.8 candidate now carries explicit "Preserved v3.7.1 machinery" section referencing all preserved reference files.
- **v3.8 NOT promoted** — remains candidate beside v3.7.1.

## P6 — Memory Audit Correction ✅

- `STAGE2-MEMORY-AUDIT.md` revised:
  - **REMOVE from hot memory (P6):** model routing facts (DeepSeek primary / Luna fallback / Codex-Sol path) → runtime config is authoritative; **"secret scan PASS"** → converted to procedure ("run secret scan before release/commit" in engineering workflow), not a durable fact.
  - Cleaned-memory estimate revised down: **~400–800 chars** (stable paths/tools only).
- **No production MEMORY mutation in Stage 3** except the separately approved benign write-approval test on a throwaway profile.

## P7 — `iip-hermes-workforce` Rename Gate ✅

- **Dependency scan:** 6 references — `.usage.json`, `iip-phase-planning/references/reconstitution-direction-workflow-2026-08-06.md`, `research/industry-outlook-reference/SKILL.md`, `iip-ui-design/references/org-office-pixel-mockup-2026-08-07.md`, + its own SKILL.md + own reference.
- **Decision (per Founder preference): KEEP NAME + EXTEND RESPONSIBILITY.** No rename to `hermes-harness-admin`. Skill matrix + v3.8 candidate updated accordingly.

---

## IPM Model Decision (recorded)

**Stage 3 PILOT model (temporary, non-production):** `gpt-5.6-sol` / provider `openai-codex` / reasoning `high` — approved for the sanitized technical pilot ONLY.
- NOT the permanent IPM production model (deferred until after Harness/Kanban validation).
- Rationale for pilot: independent from IIP's Flash research primary; existing subscription path; FD #93-consistent.
- Caveat recorded: Sol is also IIP's challenger/auditor family — production correlation/independence must be re-examined before permanent selection.

---

## Stage 3 Constraints Acknowledged (24 — from Founder direction)

1. Use existing Hermes board `iip` · 2. No old-board delete/migrate · 3. Backup board DB/config before mutation · 4. Clear board-level `default_workdir` before IPM pilot · 5. `auto_decompose=false` · 6. No global/default assignee · 7. Progressive enablement: iip → org-cos → org-data-steward → ipm · 8. Full lifecycle validation per enablement (create→assign→dispatch→heartbeat→comment→block/unblock→complete→restart) · 9. PILOT-NONCANONICAL only · 10. No mirroring real repo-board tasks · 11. No canonical investment/research state changes · 12. Synthetic IPM pilot workspace with ZERO real portfolio data · 13. Do NOT point IPM pilot at real IPM repo · 14. No IPM-sensitive attachments · 15. Dashboard localhost-only · 16. Filesystem-isolation feasibility tests → FILESYSTEM ISOLATION VERDICT · 17. Shared-board privacy/leak scan (title/body/metadata/comments/results/attachments) · 18. Failure-limit/orphan/worker-recovery tests · 19. No /kanban or /org-office rewire · 20. No Cron migration · 21. No v3.8 promotion · 22. No production SOUL switch · 23. No production IIP MEMORY/USER modification · 24. No board `other` deletion.

**Stage 3 closeout deliverables:** exact config diffs · task graph · worker/run evidence · restart/durability evidence · privacy scan · filesystem isolation result · failure/recovery evidence · rollback proof · unresolved defects list · PASS / PASS WITH CONDITIONS / FAIL recommendation for Stage 4.

---

## Git Record (P3 checkpoint)

```
Branch: harness/stage2-prep (from main 9967459)
Commit: 765b24a621faa61c295dc3c1620adc23e83d99cc
Files: operational/FOUNDERS-DECISIONS.md (FD-98 item 114)
       evidence/harness/STAGE2-CLOSEOUT-2026-08-12.md
       evidence/harness/STAGE2-SOUL-MIGRATION-MATRIX.md
       evidence/harness/STAGE2-SKILL-RESPONSIBILITY-MATRIX.md
       evidence/harness/STAGE2-MEMORY-AUDIT.md
       evidence/harness/soul-candidates/SOUL-iip-research-candidate.md
       evidence/harness/v38-candidate/SKILL.md
       evidence/harness/v38-candidate/V38-CAPABILITY-PRESERVATION-MATRIX.md
Not merged to main. Rollback: git worktree remove + branch -D.
```

---

## Gate Status

```
Stage 1 / 1.1 : COMPLETE
Stage 2       : PASS WITH PRE-STAGE-3 FIXES (this closure)
Stage 2.1     : P1–P7 COMPLETE ← current position
Stage 3       : AUTHORIZED (per Founder direction) — awaiting explicit GO after this report
Stages 4–9    : NOT AUTHORIZED
```

---
<!-- 2026-08-12 19:10:33 +0700 — M1: captured via scripts/artifact_timestamp.py (system clock at correction; agent-guessed timestamps rejected) -->
