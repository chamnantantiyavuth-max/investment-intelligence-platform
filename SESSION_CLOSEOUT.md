# Session — 2026-09-08 (Erratum-002 Independent-Audit Correction Cycles: Commit C/D + E/F)

> **Scope of this file:** factual session record for the 8 Sep 2026 interactive
> session (latest session closeout). Prior closeout (7 Sep) preserved in git +
> PROJECT_STATE.md historical rows.
>
> **✅ NOT claimed in this file:** Erratum-002 **NOT** marked FOUNDER ACCEPTED /
> FROZEN. M5.3 **HOLD** unchanged. S7/S8 **NOT** started. Production/Live QAD
> **NOT** authorized. Final closeout reconciliation deferred until the Founder
> authorizes it after independent audit (correction directive #8).

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
  - Pushed: `089cbe6..58096cc main -> main`; HEAD == origin/main == `58096cc`,
    560 commits, worktree clean.

### M5.3 — ⛔ HOLD (unchanged)

- **FD #137 register:** "M5.3 remains HOLD until Erratum-002 independent acceptance".
- S7/S8 implementation **NOT** authorized; Production / Live Autonomous QAD /
  workforce cutover / cron cutover **NOT** authorized.
- Erratum-002 = **READY FOR FOUNDER INDEPENDENT ACCEPTANCE** of Commit C+D / E+F
  (Founder has not yet reviewed E+F on remote at session end).

## Recommended next action

1. **Founder independent audit of Commit E `5b73fc1` + Commit F `58096cc` on
   remote** (authority-isolation: shadow cannot override, public API only,
   store/batch blocked, APPEND_ONLY restored).
2. If accepted → Founder-authorize the final closeout reconciliation
   (mark Erratum-002 FOUNDER ACCEPTED/FROZEN; update PROJECT_STATE.md /
   SESSION_CLOSEOUT.md current-status rows; AGENTS.md checkpoint F5).
3. Only then → M5.3 implementation authorization gate (S7 PIT Runtime + S8
   Retry Kernel) may reopen.
4. Alternatives: (A) direct closeout now — **not recommended** (audit first per
   your own discipline); (B) additional hardening if remote audit finds anything.

<!-- 2026-09-08 23:55 UTC+7 -->