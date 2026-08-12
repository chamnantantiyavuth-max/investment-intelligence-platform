# Stage 4 — v3.7.1 vs v3.8 Pilot Comparison Matrix

**Date:** 2026-08-12
**Pilot:** S3-F1 Board Safety Root Fix (executed under project-workflow v3.8 CANDIDATE)
**Question answered:** Did removing v3.7.1's bureaucracy degrade engineering quality?

| Dimension | v3.7.1 (production, unchanged) | v3.8 Pilot (candidate) | Verdict |
|---|---|---|---|
| **Root-cause quality** | Full-phase: Discovery→Constitution→Spike→2R→Plan→Implement→Evidence QA | Condensed but intact: reproduce → root-cause confirm → alternatives → Engineering Review (2R-equivalent) → implement → locked tests | **EQUAL** — root cause (`_pin_kanban_board_env` session-boot pin + env precedence + F4 DB bypass) found and confirmed with evidence |
| **Scope control** | Phase gates + task contracts + acceptance lock | ONE bounded task (S3-F1) with explicit prohibitions list; no scope creep into core patch (per Founder: don't touch main.py) | **EQUAL/BETTER** — bounded tighter than v3.7.1 norms; zero forbidden surfaces touched |
| **Architecture quality** | Formal 2R hostile review | Independent Engineering Council (Sol Medium) review — caught F1–F6 incl. two real bypasses (board input override, HERMES_KANBAN_DB) that the original design missed | **EQUAL** — review was materially effective; design v2 is stronger than v1 |
| **Independent review** | Mandated 2R + Council gates | Delegated to Sol Medium via approved independent-review routing (FD-HERMES-007); verdict REWORK → incorporated | **EQUAL** — real independence (different model family, caught design flaws) |
| **Test strength** | Locked acceptance + mutation/property testing | Locked acceptance (10 criteria) + 6 hook unit cases (2 allow + 4 negative incl. bypasses) + live E2E (create→iip, restart→survive, worker re-dispatch→done) + negative DB-delta check | **EQUAL** — all acceptance criteria covered; negative cases stronger than v3.7.1 norms |
| **Evidence quality** | Evidence QA with verification tags | Full evidence trail: reproduction (task t_029e72a0 on other), hook test outputs, doctor output, DB reads, run trails, timestamps via deterministic helper (VERIFY PASS) | **EQUAL** — every claim backed by runtime output |
| **Regression protection** | Regression budget + isolation scan | Unrelated boards untouched (verified: capcmd/notebooklm/robot-trading no hook, no iip forcing); iip profile config backup; rollback = remove hooks block | **EQUAL** |
| **Context/token overhead** | Heavy: full Bible reading, phase docs, multiple gates | Light: design doc (6KB) + review + hook script (3KB) + acceptance script; no Bible re-read needed for harness-only change | **BETTER** — materially lower overhead for engineering-scope work |
| **Unnecessary bureaucracy** | Per-task state machine, mandatory closeout per worker, council on every milestone | None of that: no per-task state machine (Kanban is task state), no worker closeout ceremony, Engineering Council only at the material gate | **BETTER** — the specific things FD #100 targeted are gone |
| **Overall engineering confidence** | High but heavy | High — same quality gates where they matter, lower friction | **EQUAL** (confidence) + **BETTER** (efficiency) |

## Key v3.8 candidate strengths observed in pilot

1. **Engineering-only scope held** — the pilot never drifted into research/council/domain territory.
2. **Review value preserved** — the REWORK verdict caught two real bypass vectors (F4) that would have shipped in design v1.
3. **Bureaucracy actually removed** — no Phase -1 Bible ceremony for a config-level fix; authority read + preflight sufficed.
4. **Verification discipline intact** — locked acceptance executed as tests, not prose.

## Residual concerns (for v3.8 promotion decision)

- **S4-F2 (new finding):** gateway restart kills in-flight worker; claim held until `claim_expires` (~15 min) before dispatcher reconciles. Operator can force re-dispatch via block/unblock (proven). Not a board-safety issue; a durability-latency note for production cutover planning.
- **HERMES_DELEGATED_CHILD_CONTEXT=1:** this session is itself a delegate-task child context (kanban mutation blocked unless unset). Harness operators must know this env quirk.
- v3.8 candidate tested on ONE engineering pilot only — promotion should follow ≥1 more engineering task (per v3.7.1 §5 rule: evidence from 2–3 projects before further governance change).

## Recommendation

**REVISE v3.8 — CONDITIONAL** (promote after one more bounded engineering task + S4-F2 noted as accepted operational latency, not a defect). The pilot proves the v3.8 shape preserves engineering quality while removing the targeted bureaucracy; one more data point is prudent before replacing production v3.7.1.

<!-- 2026-08-12 20:38:20 +0700 — captured via scripts/artifact_timestamp.py (system clock at write) -->
