# M6.7 REVIEW FINDINGS — PARENT INDEPENDENT VERIFICATION + PROVENANCE (FD #151)

Date: 2026-10-14
Purpose: a reviewer verdict is a CLAIM. Before reporting a **C** to the Founder, every material
finding was re-executed by the Parent, and each was then tested against the PREVIOUS ACCEPTED HEAD
`c288aebec523b3d0a9aa73c7802c39d0cdf06cf6` to establish whether M6.7 introduced it or merely exposed
an already-accepted surface.

Harness: two read-only detached-HEAD worktrees (review target `e8fd966`, pre-M6.7 `c288aeb`); all
probe scripts written OUTSIDE the worktrees; external basetemps. Both worktrees verified pristine
after the runs (`git status --porcelain` empty, HEADs unchanged).

---

## FINDING 3 — CONFIRMED and INTRODUCED BY M6.7 (material)

Exact reviewer repro re-run by the Parent:
`m67_create_binding_repro.py` →
```
ledger_id_mismatch_exception= LedgerNotFound: ledger run 'L-WANTED' not found
ledger_id_mismatch_runs= ['L-OTHER']
request_id_mismatch_exception= RetryPolicyError: SUCCESS refused: the result's request_id
    'REQ-BADCREATE' is not bound to the target ledger run 'L-WANTED' (request_id='REQ-WRONG')
request_id_mismatch_state= ('REQ-WRONG', 0, [2 candidates], [2 DEFERRED dispositions], None)
```

Parent's own minimal probe (`parent_verify_finding3.py`) — a NEW run whose caller-supplied
`create_run_kwargs.request_id` disagrees with the request while `ledger_id` agrees:
```
[1] call result
    raised              : RetryPolicyError: SUCCESS refused: the result's request_id 'REQ-R' is not
                          bound to the target ledger run 'L-R' (request_id='REQ-WRONG')
    outcome             : None
[2] durable ledger state AFTER the refusal
    run L-R exists      : True
    record.request_id   : REQ-WRONG      (the request said 'REQ-R')
    is_terminal         : False
    terminal_status     : None
    result_sha256       : None
    attempts            : []
    candidates          : ['SC-9864cce747428189bd4a4c09', 'SC-f1ef4abf72d765f20ce6ad01']
    dispositions        : [('SC-9864…', DEFERRED), ('SC-f1ef…', DEFERRED)]
    events              : [(1,'RUN_CREATED'), (2,'CANDIDATE_REGISTERED'), (3,'CANDIDATE_REGISTERED'),
                           (4,'CANDIDATE_DISPOSED'), (5,'CANDIDATE_DISPOSED')]
[3] HALF-POPULATED NON-TERMINAL RUN PERSISTED: True
[4] control (correctly bound kwargs): outcome=SUCCESS_FINALIZED,
    terminal=SUCCESS, hash=fcc3a0b23768dd3196968c0207f1b7ed9095966e9fd349ee36a451f3097ee2bb
```

**Verified:** the defect is real and it is in the NEW M6.7 entry point. `run_provider_attempt`
creates the run from unvalidated `create_run_kwargs` and then performs durable mutation (candidate
registration + disposition) BEFORE validating the request↔run binding, so a refusal leaves a
non-terminal run populated with candidates and dispositions that can never complete. The
happy path is unaffected (control GREEN, exact result identity).

---

## FINDING 2 — CONFIRMED, but PRE-EXISTING at the accepted HEAD (NOT introduced by M6.7)

Parent probe on the PRE-M6.7 worktree at `c288aeb` (`pre_m67_provenance.py`, ledger API only):
```
has finalize_success_attempt_atomic: True
PRE-M6.7 terminal_status : TerminalStatus.SUCCESS
PRE-M6.7 result_sha256   : ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
PRE-M6.7 artifact_ref    : mock://not-executed/forged
PRE-M6.7 attempts        : [(1, 'SUCCESS')]
fabricated hash accepted with NO result object and NO proof: True
```

**Verified:** the accepted FD #153 low-level writer already accepted a caller-supplied hash +
artifact reference with no result object and no proof, BEFORE any M6.7 code existed. FD #155 then
deliberately routed ALL new supported public SUCCESS writes to exactly this method, and M6.7 calls
it through the accepted M6.5 `accept_success_result` route. The M6.7 change did not widen it.

---

## FINDING 1 — CONFIRMED, but PRE-EXISTING at the accepted HEAD (NOT introduced by M6.7)

Parent probe on the PRE-M6.7 worktree at `c288aeb` (`pre_m67_resolver_provenance.py`, using the
accepted PUBLIC M6.4 builder with the M6.5 fixtures):
```
PRE-M6.7 (c288aeb): public M6.4 builder + a CALLER-SUPPLIED resolver
  control (accepted stub resolver) -> SUCCESS
  liar resolver                    -> SUCCESS
  closed_corpus_enforcement        : ClosedCorpusEnforcement.ENFORCED
  isolation_verification           : IsolationVerification.VERIFIED
  closed_corpus_evidence_ref       : EVID-CORPUS-1
  isolation_evidence_ref           : EVID-ISOLATION-1
  result_sha256                    : ff71f55f2511e947669525e2885205d29fd0218cccf0d2908840c4658aa31522
  UNVERIFIABLE REFS ACCEPTED AS PROOF: True
```
Source provenance on the same revision: `qad/m6/research_contract.py` at `c288aeb` already exposes
`proof_resolver` on the public builder (lines 476, 500, 503, 515, 1654, 1662) —
`resolver = DEFAULT_PROOF_RESOLVER if proof_resolver is None else proof_resolver`.

**Verified:** the trusted-resolver seam IS the accepted FD #152 design (an injected dependency is the
proof authority; the default is deny-all). Any caller able to inject a resolver can lie to it, and
that was true before M6.7. M6.7 merely FORWARDS an already-public, already-accepted injection point
through `run_provider_attempt(..., proof_resolver=...)`.

---

## INTERPRETATION (for the Founder — the reviewer reported all three as material)

| # | Reviewer report | Parent verification | Introduced by M6.7? |
|---|---|---|---|
| 1 | material defect | behaviour reproduced (pre-M6.7 too) | **No** — accepted FD #152 seam trust model |
| 2 | material defect | behaviour reproduced (pre-M6.7 too) | **No** — accepted FD #153 low-level writer |
| 3 | material defect | behaviour reproduced | **YES** — new entry-point ordering defect |

Findings 1 and 2 are properties of the ACCEPTED pre-M6.7 surface. Correcting them would amend
accepted contracts / the trust model (FD #152 seam policy; FD #153 writer signature) and therefore
requires a Founder decision — it is outside M6.7's authorized scope, which explicitly forbids
changing accepted contracts without a genuinely necessary Founder decision. Finding 3 is a real
defect in the delivered M6.7 code and is correctable inside M6.7's own new entry point without
touching any accepted contract.

Per the Founder's stop rule (C → STOP, minimal decision package, no automatic correction loop),
no correction was applied and no second review round was started.
