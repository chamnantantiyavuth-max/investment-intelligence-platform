# FOUNDER DIRECTION RECORD — QAD M6.6 OPTION A+

**Cluster:** QAD M6.6 — Noncanonical Source Discovery + Admission Bridge (FD #151)
**Branch:** `impl/m6-gemini-notebook` · **Reviewed commit:** `38dcd9f` (structural refactor)
**Baseline:** `main` = `5bf107774b29e5a5fe4dcec5846800b9b48361ba` (unchanged)
**Date:** 2026-10-12 · 5/5 IIP cron jobs PAUSED · M6.7 NOT started

---

## 1. The choice, recorded accurately

The Founder selected **OPTION A+** — explicitly **not** Option B (freeze now at `88e61ce`
with no independent A/B verdict) and **not** unlimited Option C (keep iterating fix+review).

Option A+ authorizes exactly:

1. **ONE** bounded **structural** refactor of the M6.6 evidence-admission / reconciliation /
   disposition failure-handling boundary.
2. Focused RED→GREEN regression tests proving the refactored classifier itself.
3. **ONE** family-independent **Round-14** confirmation review on the new refactor commit.
4. M6.6 closeout **ONLY** if Round 14 returns **A or B** with genuinely non-blocking findings.

**Stricter closeout condition than Option A (the "+"):** if Round 14 returns **C**, the Parent
must **STOP** — then preserve the reviewer output verbatim, classify the finding and affected
boundary, record whether it is a new material class or a regression introduced by the refactor,
prepare the minimal next Founder decision package, and return. It must **NOT**:

- automatically freeze M6.6 as accepted risk (which is what plain Option A would have allowed);
- claim an independent PASS;
- silently add another fix/re-review cycle;
- carry an unaccepted material finding into M6.7.

Founder decides the next action from the actual evidence.

## 2. Why A+ and not the alternatives

Rounds 9–13 each returned **C** with real material findings, and **every one of rounds 11–13
was a different escape route into the same nested `try` block** in
`process_discovered_sources` whose broad `except Exception` downgraded an integrity/governance
failure into an ordinary partial evidence-admission outcome. Round 12 and Round 13 defects were
introduced by the fix chain itself. That is a *structural* smell, so the correction had to be
structural — but with the closeout discipline tightened so that a structural refactor cannot
become a way to close the cluster without a genuine independent verdict.

## 3. Authorization basis

- **FD #151** already authorizes bounded M6.6 implementation corrections.
- This direction authorizes the ONE structural correction described in it; **no new FD was
  created**, and none was needed — the refactor uncovered no new policy/contract decision.
  It changes *structure*, not domain semantics: the accepted canonical gates, the accepted PIT
  authority, the accepted ledger semantics and the accepted proof boundary are all unchanged.

## 4. Baseline verification (independently checked before any edit)

| Fact | Value |
|---|---|
| `origin/main` | `5bf107774b29e5a5fe4dcec5846800b9b48361ba` |
| `origin/impl/m6-gemini-notebook` (start) | `1a5002e5caf6be3aba86f968ea1654e0694a4952` |
| Linear descendant of `main` | **YES** (`git merge-base --is-ancestor`) |
| `main` ahead / branch ahead | `0 / 65` |
| Governed worktrees clean | YES (`main`, `impl/*`, `ops/automation`, `fix/m6.2-*`); `harness/stage2-prep` carries a pre-existing unrelated modification to `scripts/board-safety-hook.sh` — untouched |
| Last branch movement | `1a5002e` — a **facts-only state/closeout update**, not a new M6.6 implementation or review verdict |

No reset, rebase, merge or force-push was performed; no stale SHA was matched.

<!-- 2026-10-12 13:05 UTC+7 -->
