# Session — 2026-09-08 (Erratum-002: Correction Cycles C/D + E/F → FOUNDER ACCEPTED)

> **Scope of this file:** factual session record for the 8 Sep 2026 interactive
> session (latest session closeout). Prior closeout (7 Sep) preserved in git +
> PROJECT_STATE.md historical rows.
>
> **✅ Final state:** Erratum-002 = **FOUNDER ACCEPTED / CLOSED / FROZEN**
> (8 Sep 2026, authority FD #137, no new FD — accepted by the independent
> remote audit of commits C/D + E/F with TECHNICAL / ARCHITECTURAL PASS).
> M5.3 **HOLD** unchanged (requires separate Founder implementation
> authorization). S7/S8 **NOT** started. Production / Live Autonomous QAD /
> workforce / cron cutover **NOT** authorized.

## Key outcomes

### Round 1 — Five-anchor LIVE carrier + exact RD authorization (Commit C + D)

Founder audited remote 6d76348 implementation, found two material defects:

1. **Defect B not proven on the five-anchor topology** — `TestLiveUpdateCarrier`
   used a monolithic `seeded_store`; `InMemoryEvidenceRegistry.admit_evidence()`
   could not resolve `EAR-01.update_pit_context_id → PITC-01` stored in the
   separate authoritative `PITContextStore`.
2. **`"Research Director" in str(created_by)` substring authorization** unsafe.

- **Commit C = `05c32a8`** (diagnostic evidence first, explicit-path staging,
  no production change): `tests/qad/persistence/test_erratum002_diagnostic_five_anchor.py`
  — expected-fail proofs: `MissingForeignKey: EAR-01.update_pit_context_id: FK
  reference 'PITC-FA-LIVE' not found in PITC-01.pit_context_id`; `"Fake Research
  Director"` accepted (DID NOT RAISE).
- **Commit D = `089cbe6`** (production + test + doc correction, 9 files):
  - `reference.py`: `InMemoryEvidenceRegistry(pit_context_store=...)` + composite
    `store_contains`/`get_existing` resolvers; FAIL CLOSED when store unavailable.
  - `transaction.py`: `RESEARCH_DIRECTOR_ROLE_TOKEN = "Research Director"` exact
    token check (SM-12); `update_provenance` remains human provenance only.
  - Tests: five-anchor acceptance (16) + RRM narrow (`TransactionFailure` +
    `ValidationFailure`, no broad `Exception`); LIVE PITC `created_by` → exact token.
  - Docs: M5.1 Type Binding Policy (PIT exception + `is_update: bool` + FD #137
    header); M5.2 Boundary Contract narrow RRM reconciliation note; Decision
    Package historical resolution header; Erratum-002 verification truth
    (exact LOCAL counts; GitHub/Vercel ≠ Python CI); RunManifestStore docstrings.
  - Verified: full suite **630/630** (596 + 18 Erratum + 16 five-anchor), QAD
    conformance 105/105, M4A 173/173, M4B 93/93, Item-13 **7/7** (NOT N/A).
  - Founder review of Commit C+D: acceptable portions noted; **NOT accepted** —
    authority-isolation defect + private `_load_raw` + APPEND_ONLY doc regression
    required another correction round.

### Round 2 — PITC authority isolation (Commit E + F)

Founder audit of 089cbe6 found three defects:

1. **Material — local PITC shadow can override authority**: resolvers consulted
   registry-local state first (`self.contains`/`self._load_raw`); `store()`
   blocked EV/EAR/SRC but not PITC-01 → shadow PITC planted locally satisfied FK.
2. **Adapter contract** — `pit_context_store._load_raw(...)` private method not
   in the public `PITContextStore` Protocol.
3. **Doc regression** — M5.1 policy table lost the `APPEND_ONLY` row (descriptor
   still has 9 APPEND_ONLY fields; persistence derives from both policies).

- **Commit E = `5b73fc1`** (diagnostic evidence first, 1 file, explicit-path):
  `test_erratum002_authority_isolation.py` — expected-fail proofs:
  `Failed: DID NOT RAISE TransactionFailure` (authority inversion: authoritative
  PITC SEALED vs local shadow LIVE+RD → LIVE update passed); store(PITC-01) not
  boundary-gated (only FK error surfaced, not `CanonicalBoundaryViolation`).
- **Commit F = `58096cc`** (production + test + doc correction, 3 files):
  - `reference.py`: PITC-01 resolves authoritative PITContextStore ONLY (never
    local); `_composite_get_existing` uses PUBLIC `load()` + KeyError→None (no
    `_load_raw` anywhere); RawSourceArchive fallback also public; `store()` +
    `store_batch()` block PITC-01 with `CanonicalBoundaryViolation`.
  - Tests: 8 acceptance proofs (#1 valid no-shadow PASS; #2 wrong-mode
    authoritative beats shadow; #3 unauthorized authoritative beats RD-shadow;
    #4 authoritative absent fails closed; #5 direct store blocked; #6 batch
    blocked; #7 resolver uses public-only PITContextStore API
    (`_PublicOnlyPITCStore` has no `_load_raw`); #8 valid path creates no shadow).
  - Docs: M5.1 `APPEND_ONLY` row restored (semantics unchanged).
  - Verified: authority-isolation **10/10**, five-anchor **16/16**, RRM **11/11**,
    LIVE **7/7**, Item-13 **7/7**, QAD conformance **105/105**, M4A **173/173**,
    M4B **93/93**, full suite **640/640** (596 + 18 Erratum + 16 five-anchor
    + 10 authority-isolation), LOCAL real runs, NOT independent CI.
  - Pushed: `089cbe6..58096cc main -> main`.

### Founder independent audit — ACCEPTED ✅

8 Sep 2026: remote audit of Commit E `5b73fc1` + Commit F `58096cc` returned
**TECHNICAL / ARCHITECTURAL PASS** — no functional blocker remaining in Defect A
or Defect B. Confirmed accepted: authoritative-only PITC lookup (no local
fallback); registry-local shadow cannot satisfy FK or LIVE authorization;
`store(PITC-01)` + `store_batch(…PITC-01…)` blocked; public `PITContextStore
load()` (no private `_load_raw`); missing authoritative store → fail closed;
exact `"Research Director"` authorization retained; RRM lifecycle no regression;
`APPEND_ONLY` row restored; diagnostic→correction chronology E→F preserved.
**Erratum-002 = FOUNDER ACCEPTED / CLOSED / FROZEN** (authority FD #137; no new
FD — no new decision was taken, this is the acceptance of the already-authorized
repair). Remaining work = docs-only closeout (this file + PROJECT_STATE + the
authoritative erratum record). M5.3 ⛔ HOLD — requires separate Founder
implementation authorization.

### M5.3 — ⛔ HOLD (unchanged)

- **FD #137 register:** "M5.3 remains HOLD until Erratum-002 independent acceptance".
- S7/S8 implementation **NOT** authorized; Production / Live Autonomous QAD /
  workforce cutover / cron cutover **NOT** authorized.
- Closing Erratum-002 does NOT auto-authorize M5.3. Working scope remains:
  S7 PIT Runtime Enforcement + S8 Retry Kernel + minimum PIT-aware query
  substrate. Autonomous Discovery business logic not started; M6/M7 not started.

## Recommended next action

1. ✅ **DONE — Erratum-002 FOUNDER ACCEPTED / CLOSED / FROZEN** (8 Sep 2026,
   independent remote audit of Commit E `5b73fc1` + Commit F `58096cc` =
   TECHNICAL / ARCHITECTURAL PASS; authority FD #137; recorded in the
   authoritative erratum record + PROJECT_STATE + this closeout).
2. **Next: M5.3 Founder Implementation Gate** — the Erratum-002 acceptance
   unblocks the gate but does NOT auto-authorize M5.3. Working scope: S7 PIT
   Runtime Enforcement + S8 Retry Kernel + minimum PIT-aware query substrate.
3. Do NOT create Erratum-003 or hardening work unless a new independently
   demonstrated defect exists (per Founder directive).
4. Alternatives: (A) proceed to the M5.3 implementation authorization decision
   now; (B) remain on HOLD until Founder schedules the gate.

<!-- 2026-09-08 16:43 UTC+7 -->