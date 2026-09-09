# QAD-M5.3 — CORRECTION DECISION PACKAGE (READ-ONLY CONTRACT / IMPLEMENTATION ANALYSIS)

> **Status:** READ-ONLY ANALYSIS — no code/test/contract edits made · no commits
> **Audit baseline:** remote `main` `5d77c135ebfd0dd1046c74ad46df6978e003c297` (M5.3 Commit 4) · HEAD `992b7f6`
> **Verdict (Founder independent audit):** M5.3 = IMPLEMENTATION EXISTS · INDEPENDENT AUDIT FAIL · CONTRACT CORRECTION REQUIRED · NOT ACCEPTED · NOT CLOSED · NOT FROZEN · HOLD
> **Erratum-002:** FOUNDER ACCEPTED / CLOSED / FROZEN — MUST NOT be reopened
> **Production / Live Autonomous QAD:** NOT AUTHORIZED · M6/M7: NOT STARTED
> **MODE:** READ-ONLY CONTRACT / IMPLEMENTATION ANALYSIS ONLY
> **Analyzed by:** Main agent (DeepSeek Flash workforce) per Founder instruction; no premium review substituted — this is a correction decision package, not a governance audit.

---

## 0. Verification basis (what this package actually read)

| # | File | Nature |
|---|------|--------|
| 1 | `project-definition/qad/QAD-OPERATING-MODEL.md` §7 (M3-01) | Frozen reliability authority |
| 2 | `design/qad-pivot/QAD-M3-SERVICE-CONTRACTS.md` S7/S8 | Frozen service contracts |
| 3 | `design/qad-pivot/m4a/QAD-M4A-CANONICAL-SCHEMAS.md` RR-01/SI-01/RSR-01/SRC-01/EV-01/RRM-01 | Frozen canonical schemas |
| 4 | `design/qad-pivot/m4a/QAD-M4A-SCHEMA-TRACEABILITY.md` | RR-01 derivation note |
| 5 | `design/qad-pivot/m4a/QAD-M4A-STATE-MACHINES.md` | Frozen state machines (SM-*) |
| 6 | `design/qad-pivot/m4a/QAD-M4A-SCHEMA-ERRATUM-002.md` + `QAD-ERRATUM-002-DECISION-PACKAGE.md` | Frozen Erratum-002 authority |
| 7 | `design/qad-pivot/m4b/pit-leakage-proof.py` TEST 7 | Frozen M4B seal proof |
| 8 | `design/qad-pivot/m4b/QAD-M4B-EVALUATION-CONTRACT.md` §2.1/§3.4 | Frozen Seal Contract |
| 9 | `design/qad-pivot/m5/QAD-M5.2-PERSISTENCE-BOUNDARY-CONTRACT.md` §7/§11 | Frozen M5.2 persistence contract |
| 10 | `qad/m53/retry_kernel.py` | M5.3 S8 implementation |
| 11 | `qad/m53/pit_enforcement.py` | M5.3 S7 implementation |
| 12 | `tests/qad/m53/test_retry_kernel.py` · `test_pit_enforcement.py` | M5.3 tests |
| 13 | `qad/models/family_i.py` · `family_b.py` · `family_c.py` | Runtime models |
| 14 | `qad/persistence/reference.py` · `interfaces.py` | Persistence substrate |
| 15 | `design/qad-pivot/m5/QAD-M5.3-IMPLEMENTATION-MAP.md` · `QAD-M5.3-CLOSEOUT.md` · `SESSION_CLOSEOUT.md` (8 Sep) | Implementation docs + GO record |

Local re-run: `tests/qad/m53/` → **28/28 PASS** (matches closeout). `No .github/workflows` in repo — **no independent Python CI** (only Vercel on GitHub combined status). A local green suite is not contract-conformance evidence.

---

## 1. RETRY BUDGET — "3 RETRIES" VS "3 ATTEMPTS"

**Frozen authority (verbatim):**
- M3-01 §7 (QAD-OPERATING-MODEL.md line 179): "**Bounded retries:** Max 3 retries per stage; budget exhaustion → `INCOMPLETE`"
- M3-SERVICES S8 failure_behavior (line 210): "Stage FAILED → **max 3 retries**. After 3 → stage marked `FAILED`."
- M3-SERVICES S8 retry_behavior (line 211): "Bounded retries per stage (max 3). Retry from last checkpoint; previous stage output preserved."
- M4A RR-01 validation_rules (CANONICAL-SCHEMAS line 1349): "**Max 3 retries per stage. After 3 → FAILED.**"
- M4A RR-01 failure_semantics (line 1350): "After 3 retries → FAILED."
- M4A RR-01 purpose (line 1340): "Record of **retry attempts for a failed operation**."
- M4A traceability (line 563): "M3 specifies **max 3 retries per stage** but not the retry record data model. M4A derives the schema (invocation_id link, attempt_number, ESCALATED status) … to satisfy **bounded-retry accounting**."

**Implementation (retry_kernel.py):** `RetryPolicy(max_attempts=3)` (line 67), loop `range(next_attempt, max_attempts + 1)` (line 184) → **3 stage() calls total**, third retryable failure → FAILED. Test `test_retry_exhaustion_is_failed` asserts `calls["n"] == 3` and 3 RR-01 records.

**Analysis:**
- **A. "max 3 retries" = initial execution + up to THREE subsequent retries = up to 4 stage executions.** "Retry" is by definition a RE-execution after failure. No frozen line ever says the initial execution counts as retry #1 / attempt #1.
- **B. No frozen authority supports "3 total attempts."** Search across M3-01 §7, M3-SERVICES S8, M4A RR-01, M4A traceability, M5.2 §11.2 returned no "attempts" counting definition. The word is consistently **retries**.
- RR-01 purpose ("retry attempts for **a failed operation**") additionally implies RR-01 records exist only once an operation has failed — a first-run SUCCESS must produce **zero** RR-01 records. Current kernel writes `SUCCEEDED attempt #1` on a clean first run (`test_duplicate_retry_produces_no_duplicate_canonical_record` proves 1 RR-01 record exists after a first-call success).

**Answer:** **A** under the package's framing (initial + up to 3 retries). No frozen authority supports `max_attempts=3` total.

**Classification: A — IMPLEMENTATION BUG (contract drift).** The frozen contract is clear; the code + its tests encode a reinterpretation. The RR-01-on-first-success behaviour is part of the same drift.

**Minimum correction (existing surfaces only, no frozen change):** initial execution = SI-01 invocation (frozen enums SUCCESS/FAILURE/PARTIAL/TIMEOUT); RR-01 records retries only (RETRYING → SUCCEEDED/FAILED), max 3 RR-01 per stage; and the serialized SI-01 status stays honest. The state/event sequence is given in §3.

---

## 2. RR-01 ID CONTRACT

**Frozen authority:** M4A RR-01 IDs (line 1346): "`retry_id: UUID v7`". SI-01 (line 1330): "`invocation_id: UUID v7`".

**Implementation (retry_kernel.py line 284):** `rid = retry_id or f"RR-{invocation.invocation_id}-{attempt_number}"` → **not UUID v7**. Tests use `SI-M53-001`, `RR-CONFLICT-1`, `RR-SI-M53-001-1` (test_retry_kernel.py lines 67/285/387); S7 tests use `EV-M53-PRE`, `EAR-M53-PRE`, `PITC-M53-SEAL` (test_pit_enforcement.py lines 173-202).

**Findings:**
- **No existing repository UUID-v7 generator exists** (grep `uuid` across `qad/` + `tests/` found only a docstring). There is no generator to "prefer."
- **No runtime enforcement either:** `qad/validator.py`, M4A validator (`validate-m4a-contracts.py`), and contract-conformance tests contain no UUID-format check. The documented "UUID v7" is contract-as-doc only today.
- The M5.3 fixtures additionally violate UUID v7 on SI-01, EV-01, EAR-01, PITC-01 — i.e., the new tests instantiate non-compliant canonical IDs across the board.

**Classification: A — IMPLEMENTATION BUG (canonical ID drift).** The documented contract says UUID v7; M5.3 code + fixtures do not comply, and nothing enforces it.

**Minimum correction (no new ID standard):** add a small, testable RFC-9562 UUID v7 generator in `qad/` (product code, not a new standard) and use it for generated `retry_id` (and any product-generated SI-01 / PITC-01 / EV-01 / EAR-01 IDs); align or explicitly waive fixture IDs under a documented convention decision for the Founder. If the Founder prefers human-readable IDs (readability argument Winner used elsewhere), that requires a documented contract-derivation decision — it cannot be a silent code choice.

---

## 3. RR-01 ROLE IN THE EXECUTION LIFECYCLE

**Frozen pieces:**
- M3-SERVICES S8: failure_behavior (initial FAILED → retries), retry_behavior (retry from last checkpoint, previous stage output preserved), idempotency ("Same stage + same case version → same execution"), logging `{case_id, stage, attempt, status, checkpoint, duration, error}`, provenance "Stage execution record, checkpoint references".
- M4A SI-01: purpose "Record of a service invocation"; status SUCCESS/FAILURE/PARTIAL/TIMEOUT; optional `retry_count`; every service invocation recorded.
- M4A RR-01: purpose "retry attempts for **a failed operation**"; attempt_number required.
- M4A RSR-01 (lines 398-411): ResearchStageRecord — stage_id, case_id, `stage_name` (18-stage enum), `stage_state` (NOT_STARTED/IN_PROGRESS/COMPLETE/FAILED/INCOMPLETE/SKIPPED), `checkpoint_ref` (optional), `output_ids[]`, `retry_count`, `failure_reason`; revision_rules "Restart from last checkpoint preserves previous output"; failure_semantics "Max 3 retries → FAILED".
- M5.2 §11.2: "Retry state machine (RETRYING → SUCCEEDED / FAILED / ESCALATED) · Idempotency guarantees for retried writes · Integration with the Run Manifest (RRM-01)."

**Current kernel relationship:** `execute(invocation, stage, …, manifest_id, retry_id)` drives 1..max attempts over RR-01 only; SI-01 is a required FK precondition; RSR-01 is entirely unused; nothing binds stage identity or case version.

**Deterministic state/event sequence that reconciles the frozen sources:**

```text
S8 receives stage-execution request
  1. origin: SI-01 invocation written (every invocation recorded)        [SI-01]
  2. stage executes (initial run, NOT an RR-01 yet)                      [RSR-01 stage_state]
     ├─ success            → SI-01=SUCCESS; RSR-01=COMPLETE; done (0 RR-01)
     └─ FAILED (transient) → SI-01=FAILURE/TIMEOUT; RSR-01=FAILED
  3. retry #1..max 3       → each retry = one RR-01 (RETRYING → …)       [RR-01]
     ├─ retry succeeds     → RR-01=SUCCEEDED; RSR-01=COMPLETE; done
     └─ 3rd retry fails    → RR-01=FAILED; stage marked FAILED
                             (case continues with documented failure)   [M3 S8]
  4. rerun after FAILED    → replay from last RSR-01 checkpoint having a
                             terminal outcome; do NOT re-execute         [idempotency]
```

**Boundary:** whether attempt_number should number the retries only (1..3) or count the initial as #1 is *unresolved in the frozen text* — M4A derived `attempt_number` without defining its base. Under the RR-01 purpose ("retry attempts"), retries-only numbering (SI-01 = the initial) is the consistent reading; this is a small point to confirm with the Founder in the correction GO.

**Classification: A (structure is implementable on existing surfaces) with one C sub-point (attempt_number base) for Founder confirmation.**

---

## 4. ESCALATED SEMANTICS

**Frozen authority search for a legal transition to RR-01=ESCALATED:**
- M4A RR-01 enum (line 1345): `status: RETRYING / SUCCEEDED / FAILED / ESCALATED` — enum exists, **no transition rule in RR-01 itself**.
- M4A state machines: line 80 "Retry exhausted → escalated to operator attention" appears inside the **Selection error** state (candidate lifecycle), not RR-01; line 149 "Stage fails → retry (max 3) → succeeds → COMPLETE" — no ESCALATED leg; line 159 (impairment) is a different domain.
- M3-SERVICES S8: "After 3 → stage marked `FAILED`" — the only defined exhaustion outcome.
- M4A traceability line 563: ESCALATED status is **"field-level NEW_M4A_DERIVATION"** — the enum was added at M4A without a machine-readable transition.

**Implementation:** on budget exhaustion with `escalated_to` supplied → RR-01=ESCALATED (+`escalated_to`); without → FAILED (lines 197-202). This transition is **invented**, not derived from frozen authority.

**Classification: C — CONTRACT AMBIGUITY (unresolved contract semantic).** No frozen rule defines when RR-01=ESCALATED is legal. Per the audit instruction: do NOT invent it — the founder decision package must resolve it (options: (i) RR-01 stays FAILED exactly as M3/M4A say and ESCALATED is removed from M5.3 scope; (ii) a named Founder decision derives a documented ESCALATED transition (e.g., explicit human-escalation request with `escalated_to` recorded and a written failure_semantics); (iii) leave ESCALATED deferred). Escalation for candidate selection (SM-1) is a different state machine and does not justify RR-01=ESCALATED.

---

## 5. CHECKPOINT REPLAY IS NOT MATERIALIZED

**Frozen requirement** (M3-SERVICES S8 lines 211-214; M3-01 §7 line 180): retry from last checkpoint; previous stage output preserved; **same stage + same case version → same execution (checkpoint replay)**; logging includes `checkpoint`; provenance includes "checkpoint references".

**Current implementation:** resume position = `len(existing RR-01 records)+1` (line 174); replay idempotency keyed by **invocation_id only** (lines 161-171). There is no machine-readable stage identity, case_version binding, checkpoint identity, checkpoint payload, or previous-stage-output reference in the kernel. The closeout claim "resume from last recorded checkpoint" exceeds the implementation.

**Existing canonical surfaces sufficient to implement it (NO new schema required — verified):**
- **RSR-01** (frozen, runtime model exists `qad/models/family_c.py` line 247): `stage_id`, `stage_name` (enum), `checkpoint_ref`, `output_ids[]`, `retry_count`, `failure_reason`, revision "restart from last checkpoint preserves previous output" → this IS the frozen stage/checkpoint record.
- **RRM-01** (frozen): `case_version` required → the case-version binding.
- **CASE-01 / CLK-01**: case_version available.
- **M5.2 §7.4**: write fails pre/mid-commit → zero partial state, retry safe (per-store).

**Exact binding:** idempotency key = (RSR-01.stage_name, RRM-01.case_version); replay reads the terminal RSR-01 outcome for that (stage, case_version) and returns it instead of re-running; checkpoint state = RSR-01.checkpoint_ref + output_ids[]; RR-01 stays the retry attempt log. All fields already frozen — no new canonical field/schema.

**Classification: A — IMPLEMENTATION BUG (requirement not implemented), NOT a stop condition** (existing RSR-01/RRM-01 surfaces carry the contract; the kernel simply does not use them).

---

## 6. TRUE RETRIED-WRITE IDEMPOTENCY

**Frozen requirement:** M5.2 §11.2: "Idempotency guarantees for retried writes." Also §7.4: "Write fails pre-commit → No partial state. Retry is safe"; "Write fails mid-commit → Snapshot restored — zero partial state. Retry is safe." Canonical identity semantics (same id + same content → idempotent; same id + different content → IntegrityConflict) are the persistence substrate.

**Current implementation:** `stage: Callable[[], None]` receives **no idempotency key, no execution identity, no transaction handle, no checkpoint**. The kernel's tests prove only: RR-01 records themselves don't duplicate (idempotent logging) and immutable-identity collisions raise IntegrityConflict. They do **not** prove that the WORK a retried stage performs cannot duplicate canonical state (e.g., a stage that admits an EV-01 on attempt 1, then fails after the write and is re-run: nothing in the kernel prevents a second admission attempt or defines the correct conflict handling).

**What the persistence layer already offers:** per-store atomic store/store_batch (M5.2 §7.1), admit_evidence/admit_source atomic admission (reference.py), IntegrityConflict on identity collision. With RSR-01 checkpoint/output binding (§5), a retried stage can be made idempotent by: (a) deterministic write identities keyed by (stage, case_version, checkpoint); (b) the store failing closed on conflicting re-writes instead of duplicating; (c) admit-gates rejecting duplicates atomically. This is implementable on existing contracts — the kernel must thread the execution identity into the stage and the tests must prove the actual write-level property.

**Classification: A — IMPLEMENTATION BUG (the §11.2 requirement is not delivered; tests prove log idempotency, not write idempotency).**

---

## 7. RETRY-HISTORY READ FAILURE IS FAIL-OPEN

**Implementation (retry_kernel.py lines 245-250):**
```python
try:
    all_records = self._store.list_all("RR-01")
except Exception:
    return []
```
Store/read failure → "no retry history" → stage may execute again → **duplicate execution risk**. This inverts M3-01 §7 reliability (deterministic, no silent duplicate state) and the project's fail-closed doctrine.

**Narrow correction (typed errors exist):** `PersistenceError` hierarchy (ValidationFailure/IntegrityConflict/ImmutabilityViolation/MissingForeignKey/TransactionFailure/…) is already the store's contract surface. `_attempts_for()` must re-raise typed persistence errors (or wrap in a deterministic `PersistenceError` subtype) so a read failure BLOCKS stage execution. Do not distinguish "truly empty" from "cannot establish" by swallowing broad `Exception`.

**Classification: A — IMPLEMENTATION BUG (fail-open on retry-history read).**

---

## 8. RR-01 + RRM-01 ATOMICITY

**Frozen authority:** M5.2 §7.1: "Batch write (same store): must succeed or fail atomically. **Partial success is not permitted.**" Both RR-01 and RRM-01 are **RunManifestStore schemas** (M5.2 §12.2: RunManifestStore = RRM-01, SI-01, RR-01, BU-01, MOD-01, PROV-01) → **same store** → a single `store_batch([rr_record, updated_manifest])` is the existing atomic boundary. Erratum-002/FD #137 governs RRM-01 lifecycle (RUNNING enrichment allowed, terminal immutable).

**Current implementation:** `_write_attempt` does `self._store.store(rec)` (RR-01) **then** `_attach_*_to_manifest` (RRM-01) via two separate stores (lines 294-300). If the manifest is missing / terminal / update fails, the RR-01 is already committed → **partial canonical state**, and `test_missing_manifest_fails_closed` explicitly asserts RR is written before the attach fails (test lines 352-357). This accepts the exact partial-state window the Founder flagged.

**Analysis of options (per instructions):**
- **A. Manifest validation can be performed BEFORE stage execution / RR write** — yes: load RRM-01, verify RUNNING, before calling `stage()`. Cheap, removes the missing/terminal-manifest window entirely.
- **B. RR-01 + RRM-01 update as one atomic boundary** — yes: same-store `store_batch` (existing mechanism, M5.2 §7.1, store_batch on CanonicalRecordStore interface line 167 / reference implementations). One batch = atomic single-store write.

**Recommendation:** both — preflight the manifest before execution (fail fast, zero writes on bad manifest) AND persist the RR-01 + enriched manifest in one `store_batch`. No persistence redesign required.

**Classification: A — IMPLEMENTATION BUG (partial-state window violates M5.2 §7.1 and the zero-partial-state requirement; test-suite acceptance of it is a test bug).**

---

## 9. S7 PUBLIC AUTHORITY BYPASS

**Frozen authority:** M4A PITC-01 (line 1290ish): "Failure semantics: PIT service unavailable → queries blocked (fail closed)." Erratum-002 / FD #137: authority isolation — PITC/EAR must resolve through the **authoritative five-anchor stores**, no registry-local shadows (`58096cc` closed this for Erratum-002 Defect B).

**Implementation (pit_enforcement.py lines 108-158):**
```python
def adjudicate(self, evidence: EvidenceRecord, pitc: PITContext,
               ear: EvidenceAdmissionRecord | None = None) -> PITVerdict:
```
- `pitc` is used directly (lines 123, 127, 142-143, 151-153) — **no verification** that it is the authoritative PITContextStore record (no `pitc_store.contains/load` on the passed object, no canonical-hash check).
- `ear` — when supplied by the caller it is used **directly** (line 140) without resolving the authoritative EAR-01; only when omitted does the service scan EvidenceRegistry (`_resolve_ear`).
- `query()`/`access()` load the PITC from the store first, so they are the safe paths; the leak is the **public `adjudicate()` surface**.

A forged `PITContext` (e.g., mode=REPLAY_EXCEPTION, created_by="FOUNDER", exception_reason="x") or a forged `EAR-01` object could authorize LIVE post-AS_OF access if a caller reaches `adjudicate()` directly — exactly the authority-isolation discipline closed under Erratum-002.

**Preferred public shape:** public callers supply IDs (e.g., `adjudicate(evidence_id, pitc_id) → service resolves authoritative PITC-01/EV-01/EAR-01 itself via the five anchors and returns PITVerdict`). If object-level adjudication is retained internally, it must be private (`_adjudicate(...)`), or every supplied object must be proven against the authoritative store hash before use.

**Classification: A — IMPLEMENTATION BUG (public adjudicate trusts caller-supplied authority objects; weakens Erratum-002 authority isolation).**

---

## 10. S7 QUERY FAILURE MUST FAIL CLOSED

**Frozen authority:** M3-SERVICES S7 failure_behavior "PIT service unavailable → queries blocked (fail closed). No PIT-unchecked evidence access." M4A PITC-01 same.

**Implementation (pit_enforcement.py lines 170-173):**
```python
try:
    candidates = self._evidence_registry.list_all("EV-01")
except Exception:
    candidates = []
```
→ EvidenceRegistry failure becomes a **legitimate empty context**; consumers cannot distinguish "zero valid evidence" from "evidence store down". Silent failure-substitution, violates fail-closed.

**Other broad-exception swallows in S7/S8 inspected (same class audit):**
- `_verify_integrity` (lines 231-240): `except KeyError: return False` + `except Exception: return False` → store/hash failure turns into SEAL_INVALIDATED. **Direction is SAFE (fail-closed: BLOCKED) but semantically dishonest** — "tamper" vs "cannot verify" are conflated. Should raise typed persistence error or return a distinct "unverifiable" state.
- `_resolve_ear` (lines 252-255): `except Exception: return None` → store failure becomes "no carrier" → in LIVE mode outcome is BLOCKED (fail-closed by coincidence), but the error is swallowed and the reason recorded would be misleading (`live_update_without_valid_erratum002_carrier`).
- retry `_attempts_for` (§7 above): fail-open — the dangerous one.

**Required semantics:** distinguish "zero valid evidence" from "unable to establish PIT-valid evidence because an authority/store failed" — raise a deterministic PIT/infrastructure block (typed `PersistenceError` or `PITBlockError`) on store failure; never return `[]` pretending absence.

**Classification: A — IMPLEMENTATION BUG (silent empty on store failure; broad-swallow pattern also in `_verify_integrity`/`_resolve_ear`).**

---

## 11. SOURCE-TIMESTAMP PIT SEMANTICS

**Frozen authority:** M3-SERVICES S7 inputs: "Case AS_OF_DATE, evidence timestamps, **source timestamps**, evaluation mode." SRC-01 PIT fields: `retrieval_date` (required), `publication_date` (optional) (CANONICAL-SCHEMAS lines 175-180). EV-01 PIT fields: `as_of`, `validation_timestamp` (line 203).

**Current implementation:** S7 adjudicates only `EV-01.as_of <= PITC-01.as_of_date` (line 123). `source_archive` is injected (constructor line 99) but **never used** for adjudication. Evidence admission verifies source existence/FK + AI-method gate only (reference.py `admit_evidence` 1151-1180) — no temporal binding EV.as_of ↔ SRC.publication_date/retrieval_date.

**Future-leak vulnerability (real, demonstrable):** source genuinely published post-AS_OF; EV.as_of backdated to pre-AS_OF; S7 sees only EV.as_of → ALLOWED. The RawSourceArchive is present but unused, so the S7 architecture does not even attempt to close this by construction.

**Which source timestamp is authoritative for PIT?** The frozen contract does not resolve this: `publication_date` is explicitly optional; `retrieval_date` is the only guaranteed field yet is a retrieval artifact (not publication truth). The M4B Seal Contract (§3.4) does require "source publication dates — publication date for every source, verified ≤ AS_OF_DATE" — but that is a **fixture-sealing requirement (pre-production)**, not a runtime S7 binding.

**Behavior when the timestamp is absent:** **not defined in frozen authority.** The audit instruction is explicit: do NOT invent a rule for missing `publication_date`.

**Verdict:** exact current vulnerability = confirmed above; authoritative timestamp = unresolved by frozen docs (needs Founder decision: e.g., require publication_date for material sources at admission vs. bind EV.as_of ≤ min(publication_date, retrieval_date) vs. defer runtime source-time enforcement to the fixture-sealing gate); missing-timestamp behavior = undefined → **STOP / FOUNDER DECISION REQUIRED.** This intersects the GO's stop condition (frozen-authority gap discovered) — the correction decision package must name it explicitly before the next implementation round.

**Classification: C — CONTRACT AMBIGUITY (frozen authority does not determine the required behavior) — Founder decision required; not silently implementable.**

---

## 12. SEALED CORPUS / M4B TEST 7 SEMANTICS

**Frozen M4B TEST 7 (pit-leakage-proof.py lines 185-194):** `tampered_sources` set (different source-set content) → `seal.verify(sealed_sources)` recomputes `sha256(sorted(sources))` vs stored `corpus_hash` → `SEAL_INVALIDATED`. This is a **sealed source-set / corpus-level hash proof**.

**M4B Seal Contract (EVALUATION-CONTRACT §3.4, lines 151-176):** fixture_id, immutable source IDs, **source content hashes**, publication dates ≤ AS_OF, allowed corpus manifest, corpus_hash, label_hash, **seal_hash** (hash of the entire sealed fixture document), plus adjudicator identity/method/timestamp, alternative interpretations, ambiguity notes.

**M5.3 substitution (test_pit_enforcement.py `test_tampered_sealed_evidence_invalidated`, lines 193-212):** a caller forges the EV-01 canonical record's content; `_verify_integrity` compares stored canonical hash vs recompute → SEAL_INVALIDATED. This is **EV record canonical-integrity checking — a security/defense-in-depth check, NOT the sealed corpus hash proof**.

**Surface inspection for the M4B fixture seal:** PITC-01 carries **no** seal/corpus hash fields. EHR-01 (EvaluationHarnessRun, lines 1435-1459) has `corpus_version`, `pit_snapshot`, `policy_version` — a version reference, not the seal hashes (`corpus_hash`/`label_hash`/`seal_hash` absent). No existing canonical surface carries the M4B fixture seal document.

**Which statement is correct:** **B.** Sealed-fixture corpus creation is explicitly a `POST_IMPLEMENTATION_PRE_PRODUCTION` gate (M5 closeout §6: "fixture sealing / cost calibration / final production stack — NOT AUTHORIZED"; M4B state: DRAFT_UNSEALED → … → SEALED happens at fixture sealing). M5.3 S7 supplies the PIT **temporal runtime primitive**; the full corpus-seal verification is legitimately deferred **with fixture sealing**. The EV canonical-hash check is retained as defense-in-depth.

**BUT the closeout/map/test claims must stop calling the EV-hash test "the frozen M4B TEST-7 seal proof."** Closeout line 31 ("canonical-hash tamper → SEAL_INVALIDATED" as KEY SEMANTICS), map line 191 ("S7 integrity/seal | M4B pit-leakage-proof TEST 7"), and the test docstring ("TEST 7 — canonical-hash tamper...") all overstate equivalence. Fix = relabel as EV-record integrity (defense-in-depth), and record "full sealed-corpus verification = deferred to fixture-sealing pre-production gate" explicitly.

**Classification: B — DOCUMENTATION / TEST CLAIM BUG** (runtime EV-hash behavior is fine as defense-in-depth; the closure claim that it is the M4B TEST-7 seal proof is false). Option A (verify full seal now) would require a new canonical carrier → STOP; not recommended since fixture sealing is a named later gate.

---

## 13. DOCUMENT / CODE DRIFT (list, no fixes)

| # | Map/closeout claim | Actual code | Drift |
|---|--------------------|-------------|-------|
| 1 | MAP §B interface: `execute(invocation, stage, *, payload: dict | None = None, …)` (MAP line 136) | `execute(invocation, stage, *, escalated_to, manifest_id, retry_id)` (retry_kernel.py line 115) | Yes — `payload` parameter does not exist; `retry_id` exists and is undocumented in the map |
| 2 | MAP §B semantics: "appends the retry_id reference into RRM-01.failures (existing list field — integration point)" (MAP line ~143) | Final code splits: RETRYING → `retries`, FAILED/ESCALATED → `failures` (lines 296-299) | Yes — map predates the retries/failures split |
| 3 | Closeout §2: "resume from last recorded checkpoint" (line 40) & kernel docstring line 30 | Resume = `len(RR records)+1` (line 174); no checkpoint identity exists | Yes — claim exceeds implementation (see §5) |
| 4 | Closeout §2: "max 3 attempts per stage" (line 34) and "each attempt writes exactly ONE immutable RR-01" | Frozen says "max 3 retries"; kernel writes RR-01 for the initial attempt incl. first-run success | Yes — the S8 core drift, propagated into closeout |
| 5 | Closeout §2 line 31 / map line 191: "canonical-hash tamper → SEAL_INVALIDATED" = M4B TEST 7 | M4B TEST 7 is the sealed source-set hash proof; EV-hash is defense-in-depth | Yes — mislabeled equivalence (see §12) |
| 6 | Closeout stop-condition table (lines 94-99): "Frozen state machine changed? ❌ none" | RR-01=ESCALATED transition invented in code (lines 197-202) without frozen rule | Yes — an un-flagged semantic choice (see §4) |
| 7 | Closeout §3 table lists 105/105 conformance etc. as verification evidence | Conformance validators do not check UUID v7, retry-budget semantics, RR-01 lifecycle role, or S7 fail-closed-on-store-failure | Partial — the cited suites pass yet do not test the drifted contracts (see §14) |

---

## 14. TEST-GAP ANALYSIS (668/668 ≠ closure)

Missing adversarial tests required to prove the frozen contract:

**S7:**
1. Forged caller-supplied PITC (never in store) cannot authorize access via `adjudicate()`.
2. Forged caller-supplied EAR (never in store / different evidence) cannot authorize LIVE evidence.
3. EvidenceRegistry `list_all` failure → query/access **BLOCKS** (typed error), never returns `[]` / never looks like valid empty.
4. Post-AS_OF authoritative source + backdated EV (as_of ≤ PITC) → leak attempt — must be blocked per the Founder decision in §11.
5. Source publication_date missing → behavior per frozen authority / Founder decision (§11) — currently undefined → test blocked until decision.
6. True corpus/seal behavior per §12 decision (deferred) OR explicit defense-in-depth relabel test.

**S8:**
7. Initial stage execution vs retry #1 semantics (initial = SI-01; retries = RR-01 only).
8. Initial success → **zero** RR-01 records (fake-retry prohibition).
9. Full "initial + 3 retries" budget semantics (4 executions max; 3rd retry fail → FAILED).
10. UUID-v7 retry IDs (product-generated) + fixture IDs.
11. Retry-history store failure → stage execution BLOCKED (typed error, not `[]`).
12. Same invocation_id with different stage/case-version cannot false-idempotently reuse a prior terminal outcome (execution key = stage × case_version per §5).
13. Checkpoint replay is real (RSR-01 terminal outcome replay), not attempt-count replay.
14. Retried canonical write produces no duplicate (stage-level, via deterministric write identity + store fail-closed).
15. Transient failure after a canonical write → retry does not duplicate that write (M5.2 §7.4 proof at the write level).
16. RR/RRM integration failure leaves zero partial state (preflight + store_batch per §8).
17. ESCALATED transition only if frozen authority / Founder decision permits it (else removed).

---

## 15. CLASSIFICATION SUMMARY

| # | Issue | Class | Key authority |
|---|-------|-------|----------------|
| 1 | Retry budget 3-retries→3-attempts (+ RR-01 on first success) | **A** IMPLEMENTATION BUG | M3-01 §7, M3 S8, M4A RR-01 (retries wording) |
| 2 | retry_id (and M5.3 fixture IDs) not UUID v7 | **A** IMPLEMENTATION BUG (doc-driven; no runtime enforcement exists) | M4A RR-01/SI-01 IDs |
| 3 | RR-01 lifecycle role (initial = SI-01; RR-01 = retries only; attempt_number base) | **A** (with **C** sub-point on attempt_number base) | M4A RR-01 purpose, SI-01 purpose |
| 4 | ESCALATED transition invented | **C** CONTRACT AMBIGUITY — Founder decision required | M3/M4A say FAILED; no RR-01 ESCALATED rule |
| 5 | Checkpoint replay not materialized | **A** IMPLEMENTATION BUG (implementable on existing RSR-01/RRM-01 — NOT a stop condition) | M3 S8 idempotency, RSR-01 schema |
| 6 | Retried-write idempotency not proven | **A** IMPLEMENTATION BUG | M5.2 §11.2, §7.4 |
| 7 | `_attempts_for()` fail-open on store read | **A** IMPLEMENTATION BUG | M3-01 §7, fail-closed doctrine |
| 8 | RR-01 + RRM-01 partial-state window | **A** IMPLEMENTATION BUG (+ test-bug accepting it) | M5.2 §7.1 same-store batch atomicity |
| 9 | Public `adjudicate()` trusts caller PITC/EAR | **A** IMPLEMENTATION BUG | Erratum-002 authority isolation |
| 10 | `query()` silent empty on store failure (+ broad swallows) | **A** IMPLEMENTATION BUG | M3 S7 fail-closed |
| 11 | Source-timestamp PIT semantics unresolved | **C** CONTRACT AMBIGUITY — **STOP / FOUNDER DECISION REQUIRED** | M3 S7 inputs; SRC-01 optional publication_date; M4B §3.4 sealing-scope |
| 12 | EV-hash test mislabeled as M4B TEST-7 seal proof | **B** DOCUMENTATION/TEST CLAIM BUG | M4B TEST 7 + Seal Contract §3.4 |
| 13 | Map/closeout/code drift (payload, RRM split, checkpoint claim, ESCALATED stop-check) | **B** DOCUMENTATION BUG (items 1,2,3,5,6) + **A** (items 4 core drift) | §13 table |
| 14 | 668/668 insufficient as conformance evidence; missing adversarial tests | **B** TEST-CLAIM BUG | §14 list |

None of the A/B issues requires a new canonical schema or a frozen-state-machine change. Issues 4 and 11 require **Founder decisions** before further implementation. No issue requires inventing a new canonical ID standard (a UUID v7 generator is an implementation detail, not a standard).

---

## 16. FINAL GATE RESULT

**M5.3 CORRECTION — READY FOR FOUNDER DECISION** ✅

(Not "NEW CONTRACT DEFECT / CANONICAL-SURFACE REQUIREMENT": no mechanically required new canonical surface was found — RSR-01/RRM-01/SI-01 already carry checkpoint, case-version, and invocation; RR-01+RRM-01 share a store with `store_batch`; the fail-closed corrections use the existing typed `PersistenceError` hierarchy; seal verification is deferred by the named pre-production fixture-sealing gate.)

**Required Founder decisions before any correction implementation:**
1. **Retry budget (drive parity with frozen wording):** confirm "max 3 retries" = initial execution + up to 3 retries (4 executions max), initial recorded by SI-01, RR-01 = retries only. (Option A in the audit package; the alternative — treating initial as attempt #1 — has NO frozen authority.)
2. **ESCALATED:** remove RR-01=ESCALATED from M5.3 scope (strict FAILED per M3/M4A), OR authorize a documented ESCALATED transition with a written failure_semantics.
3. **Source-timestamp PIT semantics (§11):** which source timestamp is authoritative for PIT; behavior when `publication_date` absent; or defer runtime source-time enforcement to the fixture-sealing pre-production gate (documented).
4. **UUID-v7 scope:** enforce product-generated canonical IDs with a small RFC-9562 UUID v7 generator (preferred), or explicitly waive with a documented convention decision; fixture IDs aligned accordingly.
5. **Correction GO scope (if accepted):** bounded correction round on existing surfaces only — no schema changes, no production adapter, no M6/M7; tests expanded per §14; docs relabeled per §12/§13 — presented for Founder approval before code.

**Status confirmations:**
- M5.3: NOT ACCEPTED / NOT CLOSED / NOT FROZEN — HOLD maintained.
- Erratum-002: FOUNDER ACCEPTED / CLOSED / FROZEN — NOT reopened.
- Production / Live Autonomous QAD: NOT AUTHORIZED. M6/M7: NOT STARTED.
- No code, test, or frozen-contract file was modified to produce this package.
- GitHub combined status: only Vercel; **no independent Python CI** (no `.github/workflows`) — a correction round should consider whether CI is a named requirement in the next GO.

---

## 17. FOUNDER DECISIONS — M5.3 CORRECTION ROUND (9 Sep 2026)

> **Authority:** Founder independent audit review + Correction GO (9 Sep 2026).
> Registered as **FD #138 — QAD M5.3 Correction Round GO + Founder Decisions**.
> Baseline: `5d77c135ebfd0dd1046c74ad46df6978e003c297` (functional M5.3 baseline;
> later remote `main` commits are docs-only). Erratum-002 remains FROZEN — not reopened.
>
> **Erratum to this package (Founder, 9 Sep 2026):** the classification-A summary
> count is **NINE** issues (#1, #2, #3, #5, #6, #7, #8, #9, #10), not ten. The
> §15 table above is correct; this note records the Founder's arithmetic fix.

### 17.1 Retry budget (resolves §1)
- **"max 3 retries" = INITIAL execution + up to THREE subsequent retries (max 4 stage executions).**
- The initial execution is NOT retry #1 and is NOT an RR-01.
- retry #3 fails → **FAILED** always.

### 17.2 SI-01 vs RR-01 lifecycle (resolves §3)
- SI-01 = initial service invocation. RR-01 = retry attempts for a failed operation (M4A purpose).
- Clean first-run success → **zero RR-01 records**.

### 17.3 ESCALATED (resolves §4)
- **REMOVED from M5.3 scope.** After retry #3 fails → FAILED (frozen rule: "After 3 retries → FAILED").
- The RR-01 ESCALATED enum stays untouched/reserved. `escalated_to` is NOT populated
  by the M5.3 automatic retry lifecycle. Any future FAILED→escalation workflow
  requires separate authority.

### 17.4 Execution identity / checkpoint (resolves §5)
- Use existing **RSR-01** (ResearchStageRecord): `stage_name`, `stage_state`,
  `checkpoint_ref`, `output_ids[]`, `retry_count` + frozen revision rule
  "Restart from last checkpoint preserves previous output".
- Logical execution identity = **case_id + authoritative case_version + stage_name**.
  case_version resolved from the authoritative RRM-01 run context.
- Kernel MUST establish identity BEFORE executing; if case version / stage identity /
  authoritative RSR state cannot be established → **FAIL CLOSED, do not execute**.
- Retry resume uses RSR-01.checkpoint_ref and preserves RSR-01.output_ids[] —
  **NOT** `len(RR records) + 1`.
- No new canonical schema.

### 17.5 True retried-write idempotency (resolves §6)
- Prove: same (case_id, case_version, stage_name) + same checkpoint + same canonical
  payload → no duplicate canonical state; conflicting payload → fail closed;
  transient failure after a canonical write → replay does not duplicate.
- S8 API may gain a bounded NONCANONICAL execution-context / idempotency interface.
- No canonical field/schema addition. Real canonical-write retry test required.

### 17.6 Fail-closed retry history (resolves §7)
- `list_all("RR-01")` failure MUST NOT become "no retry history" → stage MUST NOT
  execute; propagate/convert to a typed deterministic failure.

### 17.7 RR-01 + RRM-01 atomicity (resolves §8)
- Same RunManifestStore → use existing M5.2 same-store atomic batch boundary
  (`store_batch`). RR write + required RRM provenance → all succeed OR none.
- Preflight manifest (exists + RUNNING) BEFORE stage execution when manifest
  integration is requested; missing/terminal → fail before execution.

### 17.8 UUID v7 — NO WAIVER (resolves §2)
- M4A says UUID v7 → M5.3-generated canonical IDs MUST comply (retry_id, stage_id,
  and any M5.3-created invocation/PITC/EV/EAR/SRC/RRM ids).
- Implement or reuse a narrow RFC-9562 UUID v7 utility; M5.3 conformance-test
  fixtures must use valid UUID v7 for schemas whose frozen contracts require it.
- NO repository-wide ID retrofit.

### 17.9 S7 public authority boundary (resolves §9)
- Public PIT decisions take IDs/query intent → service resolves authoritative
  PITC/EV/EAR from canonical stores. Object-level adjudicator private/internal.
- Erratum-002 authority isolation frozen — not weakened.

### 17.10 S7 store failure → fail closed (resolves §10)
- Evidence-store failure ≠ legitimate empty set. Authority unavailable → typed
  PIT/infrastructure error. No silent empty context. Inspect `_resolve_ear`,
  `_verify_integrity`, `_load_pitc`, `query`, `access` for broad exception
  swallowing; differentiate not-found from unavailable.

### 17.11 Source-time PIT — Founder decision (resolves §11)
- S7 evaluates BOTH EV-01.as_of AND authoritative SRC-01 source-availability time.
- `effective_pit_time = MAX(EV-01.as_of, authoritative_source_available_at)`.
- **SEALED_HISTORICAL_EVALUATION:** SRC-01.publication_date REQUIRED; missing →
  **PIT BLOCK** (not eligible for SEALED). Do NOT substitute retrieval_date.
  authoritative_source_available_at = publication_date.
- **LIVE_CASE_UPDATE / REPLAY_EXCEPTION:** publication_date if present, else
  SRC-01.retrieval_date (conservative availability evidence).
- Source metadata unresolvable / timestamp uninterpretable → **FAIL CLOSED**.
- Prevents leak: financial period pre-AS_OF but filing published post-AS_OF.

### 17.12 M4B TEST 7 / sealed corpus (resolves §12)
- **Option B:** full corpus-seal verification DEFERRED to the fixture-sealing
  POST_IMPLEMENTATION_PRE_PRODUCTION gate.
- EV canonical-hash check retained as defense-in-depth, renamed/labelled
  **canonical evidence-record integrity / tamper detection** — NOT the M4B
  TEST-7 sealed-corpus proof. No new canonical seal carrier in M5.3.

### 17.13 Correction round scope — AUTHORIZED / NOT AUTHORIZED
- **Authorized:** S7 correction, S8 correction, RSR-01 checkpoint integration
  (existing surface), true retried-write idempotency proof, same-store RR/RRM
  atomicity (existing boundary), UUID-v7 compliance for M5.3 IDs, source-time PIT
  (existing SRC-01 fields), direct adversarial tests, M5.3 map/closeout correction.
- **Not authorized:** new canonical schema, frozen schema/state-machine change,
  Erratum-003, reopening Erratum-002, full §11.3 Query API, production adapter
  selection, M6, M7, Production Release, Live Autonomous QAD, workforce/cron
  cutover, full fixture sealing.

### 17.14 Final state (resolves GO §19)
- After correction: **M5.3 — CORRECTION IMPLEMENTED / READY FOR FOUNDER
  INDEPENDENT RE-AUDIT** — NOT CLOSED / NOT FROZEN.
- Erratum-002: FOUNDER ACCEPTED / CLOSED / FROZEN.
- Production / Live Autonomous QAD: NOT AUTHORIZED. M6/M7: NOT STARTED.

<!-- 2026-09-09 12:00 UTC+7 -->