# STAGE 2 — Harness Preparation & Staging Closeout Report

**Status:** Stage 2 COMPLETE (bounded scope) — awaiting Founder review before Stage 3
**Date:** 2026-08-12
**Authorization:** FD-98 (Stage 1.1 accepted; Stage 2 bounded preparation only)
**Location:** clean migration worktree `C:/Users/Admin/Desktop/Antigravity/iip-harness-prep` (branch `harness/stage2-prep`, HEAD 9967459) — main dirty tree UNTOUCHED

---

## 1. Exact Diffs (what changed, and where)

### 2A — Governance drift correction (LIVE change, the only production mutation)

**File:** `C:\Users\Admin\AppData\Local\hermes\config.yaml`
```diff
 delegation:
   max_concurrent_children: 10
   max_iterations: 50
-  model: gpt-5.6-sol-medium
+  model: gpt-5.6-sol
   provider: openai-codex
   reasoning_effort: high
```
- **Backup:** `config.yaml.bak-2026-08-12-stage2a` (8,527 bytes)
- **Scope:** global config ONLY. No profile config touched. IPM model untouched (O-IPM-MODEL deferred).

### 2B — Clean migration worktree (NEW, no production effect)

- Created branch `harness/stage2-prep` from HEAD `9967459` at `C:/Users/Admin/Desktop/Antigravity/iip-harness-prep`
- Main working tree (`investment-intelligence-platform`, branch `main`) — **untouched**: 3 deleted ChatGPT files, PROJECT_STATE/SESSION_CLOSEOUT modified, untracked integration folder + CIW draft all still exactly as found
- No stash, no commit, no delete of dirty work

### 2C–2F — Artifacts (NEW files in worktree only, no production skill/SOUL/memory touched)

| File | Purpose |
|---|---|
| `evidence/harness/STAGE2-SOUL-MIGRATION-MATRIX.md` | 21-clause SOUL matrix + 0-loss proof method + pilot plan |
| `evidence/harness/soul-candidates/SOUL-iip-research-candidate.md` | Shared IIP Research SOUL candidate (Harness §18, ~1.1KB) |
| `evidence/harness/v38-candidate/SKILL.md` | project-workflow v3.8 CANDIDATE (engineering-only) |
| `evidence/harness/STAGE2-SKILL-RESPONSIBILITY-MATRIX.md` | content-level overlap matrix + final architecture |
| `evidence/harness/STAGE2-MEMORY-AUDIT.md` | memory/user.md audit + limit method + write-approval test plan |

## 2. Verification Evidence

| Check | Result |
|---|---|
| Global delegation model (runtime) | `hermes config get delegation.model` → **gpt-5.6-sol** ✓ |
| Global reasoning | `hermes config get delegation.reasoning_effort` → **high** ✓ |
| All 20 profiles delegation model | all `gpt-5.6-sol` (17 explicit + 3 inherit → now inherit correct value) ✓ |
| ipm profile | NO delegation section (inherits global — now correct `gpt-5.6-sol`/high) ✓ |
| Residual `gpt-5.6-sol-medium` scan | **0 residual** across global + all profiles ✓ |
| project-workflow v3.7.1 untouched | hash `d296a7af8d604481...` unchanged ✓ (production copy intact) |
| v3.8 candidate isolated | at `evidence/harness/v38-candidate/` — NOT installed to skills-shared ✓ |
| Worktree clean | only `evidence/harness/` untracked artifacts ✓ |
| Main tree untouched | `git status` identical to pre-Stage-2 snapshot ✓ |
| SOUL/IPM/memory untouched | no profile SOUL, no IPM SOUL, no MEMORY/USER.md, no sync script edited ✓ |

## 3. Rollback Evidence

| Change | Rollback |
|---|---|
| 2A global config | restore `config.yaml.bak-2026-08-12-stage2a` → `config.yaml` (one command) |
| 2B worktree | `git worktree remove C:/Users/Admin/Desktop/Antigravity/iip-harness-prep` + `git branch -D harness/stage2-prep` — main tree unaffected |
| 2C–2F artifacts | delete worktree files (or keep — no production effect) |
| Production v3.7.1 | untouched — zero rollback needed |
| Production profiles/kanban/cron/UI | untouched — zero rollback needed |

## 4. Final Skill Responsibility Map (approved responsibilities, not filenames)

```
ENGINEERING
  project-workflow v3.8        (candidate ready — promote after Stage 4)
  llm-council                  (keep — engineering council)
  governed-review-gates        (keep — hostile review playbook)

ORGANIZATION / HARNESS
  hermes-harness-admin         (RESHAPE from iip-hermes-workforce — no new)
  capital-kanban               (NEW thin — org policy only)

IIP RESEARCH
  iip-evidence                 (NEW thin — cross-cutting evidence procedure)
  fundamental-company-research (EXTEND — Gemini DR lane; no iip-deep-research)
  iip-editorial-publication    (EXTEND — semantic fidelity + Fact Packet; no iip-publication)
  iip-discovery-audit          (NEW — v1.1 method)

BOUNDARY
  iip-ipm-handoff              (NEW thin — one-way firewall)

IPM
  simulated-portfolio-office   (KEEP — IPM-owned; no ipm-operating-review)
```

**Net new skills: 4 (capital-kanban, iip-evidence, iip-discovery-audit, iip-ipm-handoff).** Not 8. Exact per-skill diffs deferred to Stage 3 after Founder approves this map.

## 5. SOUL Migration Proof (summary — full in STAGE2-SOUL-MIGRATION-MATRIX.md)

- 21 canonical SOUL clauses mapped 1:1 to destinations (SOUL/AGENTS/PRINCIPAL/skills/config-FD/USER/retire)
- 0-binding-loss proof method defined (clause inventory → destination verify → compose test → hash check)
- Candidate Research SOUL created (~1.1KB vs 26KB — identity/temperament/communication only)
- Pilot scope locked: iip + org-cos + org-data-steward only; IPM SOUL (2.6KB) preserved
- sync-governance.py implication flagged (needs org-radar-scout in PROFILES + per-project SOUL selection) — NOT edited in Stage 2

## 6. Proposed IPM Model Options (O-IPM-MODEL — Founder decision deferred to end of Stage 2)

Context: ipm profile has NO model config today; inherits global. IPM = independent decision layer — should NOT auto-copy IIP's `deepseek-v4-flash`. Available provider paths in this v0.20.0 install:

| Option | Model / provider | Independence from IIP | Quality | Cost path | Notes |
|---|---|---|---|---|---|
| **A** | `deepseek-v4-flash` (deepseek) — copy IIP | ✗ same as IIP primary | high (proven) | existing subscription | simplest, but same-family as IIP → weakest independence |
| **B** | `gpt-5.6-luna` (openrouter) — existing fallback | ✓ different family | high | openrouter key already configured | already wired as fallback; independent review family |
| **C** | `gpt-5.6-sol` (openai-codex) — same as audit delegation | ✓ different family | very high | codex subscription already used | strongest independent judgment; reuse existing delegation path; reasoning=high per FD #93 |
| **D** | defer (set explicit `deepseek-v4-flash` temporarily, revisit) | — | — | — | keeps IPM runnable without choosing |

**Recommendation: C (gpt-5.6-sol via openai-codex, reasoning=high)** — IPM is a decision layer; strongest independence from IIP's Flash research primary, existing subscription path, FD #93-consistent. Alternative B if cost sensitivity. **Founder decides before Stage 3 IPM pilot.**

## 7. Exact Stage 3 Pilot Plan (non-canonical, technical only)

**Pre-conditions (Founder gate):** approve this closeout + O-IPM-MODEL + skill responsibility map.

1. **Enable kanban toolset on pilot profiles only** (progressive, per FD-98):
   - iip → org-cos → org-data-steward → ipm (4 profiles; NOT all 13)
   - Each: remove `kanban` from `disabled_toolsets` + `plugins.disabled`, add `kanban` to `platform_toolsets.cli`
2. **Switch current board** `other` → `iip` (`hermes kanban boards switch iip`)
3. **Board hygiene:** rename display name → "Capital Intelligence" (`hermes kanban boards rename iip "Capital Intelligence"`, slug unchanged); clear board-level `default_workdir` (`set-default-workdir` — verify empty/clear semantics)
4. **Kanban config** (verified v0.20.0 keys only):
   ```yaml
   kanban:
     auto_decompose: false
     auto_decompose_per_tick: 3
     max_in_progress_per_profile: 1
     orchestrator_profile: ""
     default_assignee: ""
     dispatch_in_gateway: true
     failure_limit: 2
   ```
   (max_in_progress/auto_promote_children flagged stale — NOT set)
5. **Pilot tasks** (explicit `PILOT-NONCANONICAL` label):
   - One simple IIP multi-profile task (e.g. source-preflight rehearsal via org-data-steward)
   - One sanitized IPM task (no portfolio data — e.g. "review published IIP report X, return sanitized summary")
6. **Test matrix:** create → assign → dispatch → worker → heartbeat → block → unblock → comment → dependency → complete → restart durability → failure limit
7. **Filesystem isolation feasibility test** (per O3): docker backend availability (`hermes setup terminal`), WSL2/container mount design, restricted backend, OS ACL — produce VERDICT (A hard / B logical-only + quantified residual risk)
8. **Board `other` spot-check** (O5): sample full task bodies/comments for non-test content → then Founder deletion decision
9. **Privacy scan** after pilot: board content + attachments scan for portfolio-sensitive patterns
10. **Write-approval benign test** (2F §5) on a throwaway profile, NOT production
11. **Deliverables:** FILESYSTEM ISOLATION VERDICT, pilot verification evidence, privacy scan, board-other provenance spot-check → Founder gate → Stage 4

**Stage 3 prohibitions carried:** no old-board migration, no /kanban rewire, no cron migration, no v3.8 promotion, no production IPM task, no Discovery Audit, no Gemini DR production.

---

## Gate Status

```
Stage 0  (baseline)      : PARTIAL — backups at each stage start
Stage 1  (design review) : COMPLETE (approved with amendments)
Stage 1.1 (amendments)   : COMPLETE (accepted)
Stage 2  (preparation)   : COMPLETE ← current position (this report)
Stage 3  (technical pilot): NOT AUTHORIZED — awaiting Founder review of this report
Stages 4–9: NOT AUTHORIZED
```
