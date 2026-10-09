# FOUNDER DECISION PACKAGE — M6.5 Round-8 (STOP at brief §14 "C requiring another material contract/policy change")

Date: 2026-10-09 · Cluster: QAD M6.5 (+ FD #153 amendment) · Branch: `impl/m6-gemini-notebook`
Status: **M6.5 NOT closed.** No code changed for this finding. `main` untouched. Cron 5/5 PAUSED.

## 1. What round 8 found (and did NOT find)

Independent family-separated review round 8 (producer = DeepSeek V4.1 Flash; reviewer =
`openai/gpt-6-luna`, high) returned **C — one material finding**. **POLICY DISAGREEMENT:
None.**

Everything the FD #153 amendment was authorized to do is VERIFIED:
- probe 1 (atomic boundary itself, incl. a **two-process race**) — the atomic path is
  atomic; exactly one SUCCESS attempt + matching terminal binding + one event pair.
- probes 2–5 — undisposed-candidate rollback; injection after the attempt insert; injection
  before COMMIT; injection on either audit event → **all roll back completely**.
- probe 6 — result B cannot replace finalized result A.
- probe 7 — a constructed orphan SUCCESS is refused without mutation and without acquiring a
  caller-supplied hash.
- probe 8 — post-terminal mutation (append / terminalize / new candidate / atomic method)
  all refused.
- probe 9 — all five identity mismatches refused with no mutation.
- probe 10 — proof gate ordering, forged/tampered refusal, exact-hash retention,
  non-canonical status.
- probe 11 — Mode A/B, truthful labels, retry limits, fail-closed outcomes, contiguous
  history, idempotency/re-entry.
- probe 14 — created SQLite schema has exactly the declared tables/columns; no
  attempt-level result-hash column; no unexpected table/column. **No schema migration.**
- probe 15 — no provider/Gemini/browser/network imports; no M6.6+ symbols.
- probes 12/13 were marked NOT VERIFIED **only because the disposable review copy has no
  `.git`** (a harness limitation, not a defect): independently re-confirmed here with git
  present — the M6.3 suite is 52/52 unchanged, canonical schema count is 68, RRM-01
  unchanged, and `research_contract.py` is untouched.

## 2. The one finding

**Public low-level ledger writes still bypass the atomic invariant.**

The generic accepted APIs still permit BOTH halves of the FD #153 equivalence to exist
alone — the reviewer reproduced both:
- `append_attempt(..., outcome=SUCCESS)` → a durable **orphan SUCCESS attempt** with no
  terminal record (e.g. if terminalization is then blocked by an undisposed candidate);
- `terminalize(..., terminal_status=SUCCESS)` → a **SUCCESS terminal record with ZERO SUCCESS
  attempts**.

The new atomic finalizer does not close those other paths; the invariant is enforced only at
the atomic boundary and on every M6.5 SUCCESS write path.

Reviewer's proposed smallest correction: reject standalone SUCCESS on the generic
`append_attempt` / `terminalize` paths (keeping fail-closed reads of existing orphan
records). The reviewer explicitly flags: *"Because standalone append semantics are accepted
under FD #149, confirm that narrow guard is within the authorized scope before closeout."*

## 3. Why this is a policy decision, not a bounded bug fix (decisive evidence)

The proposed guard **changes semantics that FD #153 §5 explicitly preserved**:

> "**EXISTING APIs PRESERVED:** `append_attempt()` stays append-only; `terminalize()`
> retains its existing semantics … Do not create competing terminalization semantics."

And those standalone writes are **accepted, tested FD #149 behavior**. Real grep of the
ACCEPTED M6.3 suite (`tests/qad/m6/test_m63_run_ledger.py`):

    line 212:  ... outcome=TerminalStatus.SUCCESS)          # direct SUCCESS append
    line 365, 368, 415, 437, 447, 456, 471, 618, 663, 807:
               store.terminalize("L-001", terminal_status=TerminalStatus.SUCCESS, ...)
    count: 15 occurrences of TerminalStatus.SUCCESS

Implementing the guard would therefore (a) break currently-accepted M6.3 tests and (b)
re-open the FD #149 semantics FD #153 said to preserve. That is a **new contract change**,
which M6.5 brief §14/§18 directs me to STOP and escalate rather than fix-loop.

Scope note (honest): FD #153 scopes its invariant "through this boundary" and to states
arising "because of a partial SUCCESS-finalization failure". The reviewer's case is neither —
it is direct use of an accepted generic API. Part of the trigger is my own round-8 prompt
asking to try "ANY path", which is broader than the Founder's ruling. No M6.5 code writes
SUCCESS through either generic path (only the atomic finalizer; `terminalize` is used solely
for RESEARCH_UNAVAILABLE).

## 4. Options (one decision)

### Option A — Accept M6.5 as correct at the authorized boundary; carry the raw-API limitation forward *(recommended)*
Close M6.5: the FD #153 invariant is enforced wherever M6.5 can write SUCCESS, and the
atomic boundary is verified (including a two-process race). Record the raw generic-API
half-state as an explicit bounded carry-forward with a NAMED gate:
**must be closed before M6.7/M6.8 introduce any new SUCCESS-writing caller** (or as a
separate small M6.3-hardening FD).
- Cost: lowest; no frozen artifact reopened; no accepted test edited.
- Risk: the invariant is not universal — a future caller could bypass the orchestration
  layer. Mitigated by the explicit gate.

### Option B — Extend the amendment now: reject standalone SUCCESS on the generic paths
Add the narrow guard to `append_attempt(outcome=SUCCESS)` and `terminalize(SUCCESS)` (with
fail-closed reads of existing orphan records preserved).
- Cost: re-opens FD #149 semantics a second time in one session and requires updating
  accepted M6.3 tests (or rewriting them to use the new boundary).
- Benefit: the invariant becomes universal at the ledger API.

### Option C — Defer entirely
Treat the raw-API path as out of scope for M6.5 and for now; record as a known limitation
with no named gate.
- Cost: lowest; Risk: highest — no trigger forces the closure.

## 5. Exact approval requested

Select **A**, **B**, or **C**. On selection I will:
- (A) record the decision + the gated carry-forward, then produce the facts-only M6.5
  closeout with the target status
  `M6.5 RETRY / TELEMETRY / IDEMPOTENCY GREEN / ATOMIC SUCCESS FINALIZATION VERIFIED / DETERMINISTIC ATTEMPT LIFECYCLE VERIFIED / READY FOR M6.6`.
- (B) implement the guard, prove RED→GREEN, re-run M6.1–M6.5 + accepted M6.3 suite (updating
  only the tests the guard legitimately invalidates), full regression + gates, then
  re-review (round 9).
- (C) record the limitation and close M6.5 with it noted.

No merge to `main`. Cron stays 5/5 PAUSED. M6.6 not started.

## 6. Evidence in this directory

- `REVIEW-ROUND8-2026-10-09.txt` — verbatim reviewer output
- `REVIEW-ROUND8-2026-10-09-PROMPT.txt` — the reviewed prompt (FD #153 ruling + 15 attacks)
- `REVIEW-ROUND8-2026-10-09-ROUTING.txt` — family-independence guard output

<!-- 2026-10-09 16:40 UTC+7 -->
