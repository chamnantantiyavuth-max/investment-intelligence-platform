# M6.7 — FOUNDER DECISION PACKAGE (independent review returned C)

Date: 2026-10-14
Branch: `impl/m6-gemini-notebook`
Delivered commit under review: `e8fd9663aa2506a8c3143541bf5ce285088484bc` (LOCAL; nothing pushed)
Previous accepted HEAD: `c288aebec523b3d0a9aa73c7802c39d0cdf06cf6`
Independent review: ONE family-independent round — **verdict C** (`evidence/m6.7/REVIEW-ROUND1-FD151-M67-2026-10-14.md`)
Parent verification + provenance: `evidence/m6.7/PARENT-VERIFICATION-AND-PROVENANCE-2026-10-14.md`

Per the Founder's rule for M6.7 — *"C requires STOP and a concise defect/reproduction report. No
automatic review-correction loop."* — the session STOPPED: no correction was applied, no second
review round was started, M6.7 was NOT closed, and nothing was pushed.

## What the review proved (all three findings reproduced by the Parent)

| # | Finding | Verified | Introduced by M6.7? | Correctable inside M6.7 scope? |
|---|---|---|---|---|
| 1 | A caller-supplied resolver can mint proof and a durable SUCCESS | YES | **No** (accepted FD #152 seam) | No — amends the accepted trust model |
| 2 | The public atomic writer accepts a fabricated hash/ref | YES | **No** (accepted FD #153 writer) | No — amends an accepted M6.3 contract |
| 3 | A new run is created + populated BEFORE request↔run binding is validated, leaving a durable HALF-POPULATED NON-TERMINAL run (candidates + dispositions, no attempt, no terminal record) | YES | **YES** | **Yes** — inside the new entry point |

What the review also confirmed as SOUND: the end-to-end mock path, the durable atomic SUCCESS with
the exact result identity, candidate settlement before terminalization, fresh-instance read-back,
retry/exhaustion/idempotent re-entry, the PIT/SEALED boundary, the FD #155 generic SUCCESS guards
(0 attempts / 0 audit events on refusal), the FD #153 exclusivity of the atomic writer, the diff
provenance (protected files untouched), 68 canonical schemas / no migration, no egress or credential
surface, and no ledger mutation from the adapter/transport.

## Options

**A — BOUNDED SELF-CORRECTION OF FINDING 3 + ONE CLOSURE-FOCUSED RE-REVIEW  ⟵ RECOMMENDED**
Correct only the M6.7-introduced defect: preflight every request-bound `create_run_kwargs` field
BEFORE any mutation, validate the resolved/created record against the request before the provider or
the source bridge runs, and add negative regression tests (mismatched ledger_id / request_id /
snapshot hash / run id must be refused with ZERO run, candidates, dispositions, attempts, terminal or
events). Findings 1–2 remain recorded as REVIEWED PRE-EXISTING SURFACE PROPERTIES, not silently
dropped. Then ONE family-independent closure-focused review of the corrected commit. Smallest change
that restores a defensible artifact; keeps the accepted contracts untouched; matches the treatment
used for the earlier M6.4/M6.6 rounds.

**B — CORRECT FINDING 3, CLOSE ON PARENT EVIDENCE (no further review round)**
Same correction, then close M6.7 on the Parent's re-executed evidence without a second independent
round. Faster, but the corrected artifact would carry no independent verdict — inconsistent with the
project's review discipline.

**C — ACCEPT FINDING 3 AS A BOUNDED LIMITATION AND CLOSE OUT AS-IS**
Record the half-state path as a known limitation of the new entry point and close M6.7 on the
A/B-closeout rule by Founder waiver. Not recommended: it leaves a durable partial-state path in
brand-new code that the next milestone (M6.8/M6.9) would build on.

**D — WIDEN THE CORRECTION TO FINDINGS 1–2**
Also address the resolver-authority and low-level-writer issues, e.g. restrict resolver injection to
an approved capability and make the atomic writer accept only a proof-bound result object. This
amends accepted contracts (FD #152 trust model; FD #153 writer signature) and is OUTSIDE M6.7's
authorized scope; it needs its own Founder decision and its own bounded scope.

## Recommendation

**A.** It fixes the only defect M6.7 actually introduced, touches no accepted contract, is provable
with negative regression tests, and can be independently confirmed in one bounded round.
Findings 1–2 should be scheduled as a SEPARATE decision if the Founder wants the resolver-authority
and writer-identity questions tightened — they are pre-existing, accepted, and orthogonal to M6.7.

## State at the moment of this package (verified)

- Implementation commit `e8fd966` is LOCAL only; `origin/impl/m6-gemini-notebook` is still
  `c288aeb`; **nothing pushed**; no merge to `main`.
- `main` = `5bf107774b29e5a5fe4dcec5846800b9b48361ba` unchanged.
- **5/5 cron PAUSED.**
- 68 canonical schemas; no migration; `ledger.py` / `source_bridge.py` / `research_contract.py`
  untouched by `e8fd966`.
- **M6.7 NOT CLOSED. M6.8 NOT STARTED.** No live/provider/browser/cron execution occurred.
- Two read-only frozen worktrees remain (review target `e8fd966`, pre-M6.7 `c288aeb`) — both
  pristine; the pre-M6.7 worktree is disposable once this package is decided.
