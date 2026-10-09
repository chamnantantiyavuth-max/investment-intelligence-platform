# FOUNDER DECISION PACKAGE — M6.5 Round-7 (STOP at brief §6/§18 C-policy)

Date: 2026-10-09 · Cluster: QAD M6.5 (Retry / Telemetry / Idempotency) · Branch: `impl/m6-gemini-notebook`
Status: **M6.5 NOT closed.** No policy invented. No ledger change made. `main` untouched.

## 1. What happened

Independent family-separated review round 7 (producer = DeepSeek V4.1 Flash; reviewer =
`openai/gpt-6-luna`, high) returned **C — MATERIAL IMPLEMENTATION DEFECT**, one finding,
**POLICY DISAGREEMENT: NONE**. Rounds 1–6 were bounded implementation defects; all were
fixed. Round 7 is different: it is a genuine **contract/interface gap between M6.5 and the
ACCEPTED M6.3 Run Ledger (FD #149)**. Fixing it requires authority M6.5 does not have.

## 2. The defect (reviewer finding, verified)

`accept_success_result` records a SUCCESS attempt and then terminalizes the run in TWO
separate transactions:

1. `append_attempt(..., outcome=SUCCESS)`  — durable SUCCESS attempt, **no result hash**
2. `terminalize(..., result_sha256=<hash>)` — durable run-level hash

If step 2 fails, a durable SUCCESS attempt exists with **no result binding**. A later
recovery call can then supply a *different* proof-verified result for the same run and
finalize with **that** result's hash — while the already-durable attempt belongs to the
original result. Exact result provenance is broken.

This is reachable **in normal operation**, not only on a crash: `terminalize` is refused
while any registered source candidate lacks a disposition — a routine governance state.

Reviewer observed hashes: A = `ff71f55f…5aa31522`, recovered B/final = `9f47e409…7cb83fbb`.

## 3. Why M6.5 cannot fix this itself — two decisive probes (real output)

    PROBE1: append_attempt after terminalize -> LedgerTerminalError
            "ledger run 'L' is terminal (SUCCESS); mutation rejected"
    PROBE2: ledger_attempt columns = [ledger_id, attempt_number, retry_mode,
            provider_surface, transport_type, started_at, completed_at, outcome,
            error, telemetry_json]
    PROBE2: any result-hash column on the attempt row? -> False

- The **ledger_attempt table has no field** capable of binding an attempt to its result.
- `append_attempt` calls `_require_mutable`, so **terminal-first-then-append (a reorder)
  is impossible**: a terminal run accepts no further mutation.

Therefore a correct fix requires changing the **accepted M6.3 Run Ledger contract**, in one
of the shapes below. The M6.5 brief fences all of them:

- §9 "Do not replace or redesign the ledger. Do not add a 69th canonical schema."
- §4 "If no appropriate existing mutation boundary exists yet … do NOT invent a new
  canonical write API inside M6.5."
- §6 / §18 "If the authority is ambiguous on a MATERIAL failure class: STOP … return a
  Founder decision package … do NOT invent policy."

Round-7 asserts the same: the smallest correction "requires a transaction-level write path,
beyond the currently claimed read-only-only ledger addition."

## 4. Options (one decision)

### Option A — Amend the M6.3 ledger with an atomic SUCCESS-finalization method  *(recommended)*
Add ONE ledger method that, in a single transaction, appends the final SUCCESS attempt **and**
terminalizes the run with the same result hash/artifact reference. Additive result-binding
field on `ledger_attempt` (or reuse the run-level field consistently).
- Closes exact result provenance precisely; preserves terminal-immutability; ONE atomic write.
- Cost: an amendment to an ACCEPTED/FROZEN artifact (FD #149) + M6.3 suite re-verified.

### Option B — Terminalize-first, allow exactly one follower SUCCESS append
Keep the run-level `ledger_terminal.result_sha256` as the durable binding and relax
`_require_mutable` to permit appending the final SUCCESS attempt to an already-terminal run
whose attempt history lacks a SUCCESS row. Recovery then binds to the durable hash.
- No new column; changes accepted terminal-immutability semantics (a special case).

### Option C — Bounded deferral, hard carry-forward to M6.8
Accept the round-7 finding as an M6.5 accepted-risk; carry "durable result binding on the
acceptance boundary" to M6.8 (where real proof production/resolution and a durable result
artifact store exist). M6.5 is NON-CANONICAL and runs no provider.
- Unblocks M6.5 now, zero ledger change. Leaves a reachable substitution hole until M6.8 —
  must be gated closed **before any canonical or production use**.

## 5. Exact approval requested

Select **A**, **B**, or **C**. On selection I will:
- (A/B) record the decision, make the bounded ledger amendment + M6.5 reorder/binding, prove
  RED→GREEN, re-run M6.1–M6.4 + M6.5 + ops + gates, and re-review (round 8).
- (C) record the accepted-risk + carry-forward item, close M6.5 with the round-7 finding
  documented as an open, gated risk, and proceed.

No merge to `main`. Cron stays 5/5 PAUSED. M6.6 not started.

## 6. Evidence in this directory

- `REVIEW-ROUND7-2026-10-09.txt` — verbatim reviewer output
- `REVIEW-ROUND7-2026-10-09-PROMPT.txt` — the reviewed prompt (policy + probes)
- `INHERITED-FAILURE-ATTRIBUTION-2026-10-09.md` — `test_schema_build_identity` proven
  pre-existing at `e13a64e` (not an M6.5 regression)

<!-- 2026-10-09 14:45 UTC+7 -->
