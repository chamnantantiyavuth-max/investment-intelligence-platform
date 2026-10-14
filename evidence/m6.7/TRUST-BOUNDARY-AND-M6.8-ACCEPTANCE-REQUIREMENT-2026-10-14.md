# M6.7 TRUST-BOUNDARY RECORD + M6.8 ACCEPTANCE REQUIREMENT (FD #151)

Date: 2026-10-14
Source: independent Round-1 review findings 1 and 2 (verdict C), re-executed and
provenance-established by the Parent in
`evidence/m6.7/PARENT-VERIFICATION-AND-PROVENANCE-2026-10-14.md`.

The Founder's Round-1 ruling: findings 1–2 are CONFIRMED PRE-EXISTING behaviours at
`c288aeb`; the accepted FD #152 / FD #153 contracts are NOT to be modified by this M6.7
correction; findings 1–2 must NOT be treated as universally harmless merely because they
predate M6.7; their reproduction evidence is preserved and the accepted trust assumptions
are documented below and recorded as a concrete M6.8 security/integration acceptance
requirement.

## 1. Preserved reproduction evidence (both PRE-EXISTING at `c288aeb`)

**Finding 1 — resolver authority.** On a read-only `c288aeb` worktree, the accepted PUBLIC
M6.4 builder accepted a CALLER-SUPPLIED resolver and returned a SUCCESS result claiming
`ClosedCorpusEnforcement.ENFORCED` / `IsolationVerification.VERIFIED` for evidence
references no evidence store knows about:
```
control (accepted stub resolver) -> SUCCESS
liar resolver                    -> SUCCESS
closed_corpus_enforcement        : ClosedCorpusEnforcement.ENFORCED
isolation_verification           : IsolationVerification.VERIFIED
closed_corpus_evidence_ref       : EVID-CORPUS-1
isolation_evidence_ref           : EVID-ISOLATION-1
```
Source provenance at the same revision: `qad/m6/research_contract.py` already exposed
`proof_resolver` on the public builder (`resolver = DEFAULT_PROOF_RESOLVER if
proof_resolver is None else proof_resolver`).

**Finding 2 — low-level writer identity.** On the same `c288aeb` worktree, the accepted
FD #153 writer already persisted a durable SUCCESS from a caller-supplied hash/ref with no
result object and no proof:
```
PRE-M6.7 terminal_status : TerminalStatus.SUCCESS
PRE-M6.7 result_sha256   : ffffffff…ffffffff
PRE-M6.7 artifact_ref    : mock://not-executed/forged
fabricated hash accepted with NO result object and NO proof: True
```
This is the accepted FD #154 disposition class: the universal ledger-level
`SUCCESS attempt ⇔ SUCCESS terminal result binding` is guaranteed for the AUTHORIZED
orchestration route, not for arbitrary direct low-level callers.

## 2. Accepted trust assumptions (documented, NOT re-litigated here)

1. **A proof resolver is a TRUSTED ORCHESTRATION DEPENDENCY, not an arbitrary
   provider-supplied object.** The M6.4 seam (FD #152) is an injected dependency: the
   component that INJECTS it is responsible for its trustworthiness. The default
   (`DEFAULT_PROOF_RESOLVER`) is deny-all, so absent an explicit trusted injection SUCCESS
   fails closed, and a provider transport's self-reported assertions are never treated as
   proof.
2. **The low-level atomic finalizer is TRUSTED PERSISTENCE MACHINERY, not a
   general-purpose proof-verification API.** `finalize_success_attempt_atomic(...)` gives
   ATOMICITY (attempt + terminal binding + audit events in one transaction, full rollback);
   it does not and was never authorized to RE-VERIFY a proof. It must only ever be reached
   through an orchestration route that has already verified the result.
3. **M6.7 obtains SUCCESS only through the existing proof-verified
   `accept_success_result()` route.** The M6.7 entry point never calls the low-level atomic
   writer itself and never calls the FD #155-restricted generic SUCCESS APIs — verified by
   the Round-1 reviewer's AST call scan (`static_calls.provider.py=[]`,
   `static_calls.mock_transport.py=[]`; orchestration calls the accepted M6.5 services).
4. **The accepted in-process trust boundary is unchanged**: hostile same-process
   introspection / `object.__new__` / monkeypatching of module internals and deliberate raw
   SQLite mutation are OUT of scope and are not findings.

## 3. NAMED M6.8 ACCEPTANCE REQUIREMENT

> **`M6.8-TRUST-BOUNDARY-ACCEPTANCE`** — the real (non-mock) M6.8 provider integration
> MUST demonstrate, with executable evidence, that **untrusted transport output cannot
> inject an unauthorized proof resolver and cannot use the low-level atomic writer as an
> alternate SUCCESS acceptance path**.
>
> Minimum demonstration for M6.8 closeout:
> 1. the production/default resolver remains deny-all unless a TRUSTED component injects a
>    resolver, and no provider-supplied field, header, payload, artifact or transcript can
>    select or substitute the resolver (probe: hostile transport output attempting to
>    influence resolver selection → SUCCESS still refused, fail closed);
> 2. no provider-derived code path reaches `finalize_success_attempt_atomic(...)` or the
>    FD #155-restricted generic SUCCESS APIs — every M6.8 SUCCESS must arrive through the
>    proof-verified `accept_success_result()` route (probe: AST/call-site scan plus a
>    behavioural hostile-transport run);
> 3. the M6.7 mock resolver is NOT installed as any production default (probe: production
>    configuration contains no injected mock resolver; `MOCK_PROOF_RESOLVER_IS_TEST_ONLY`
>    stays test-only);
> 4. credential/egress isolation is retained (no credential in transport, logs, artifacts
>    or the ledger).

This requirement is carried forward as an M6.8 acceptance condition and is recorded here
rather than as a new production gate or governance layer (no such layer is needed now).
