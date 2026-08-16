# Final Independent Adversarial Re-Review

> **Round:** Resolution — re-testing corrected areas F1/F2/F5/F6/F7/F8 only.
> **Method:** Verify each corrected area is genuinely resolved. Do not reopen already-resolved architecture.

---

## F1 — Chief Underwriter Authority Separation

**Original finding:** 5 authorities concentrated in one role (gatekeeper + terminator + publisher + judge + budget-overrider).

**Resolution applied:**
- Autonomous Selection Engine (policy-driven, deterministic) — independent of Underwriter
- Research Director (Role 1a) — execution management, proposes termination
- Chief Underwriter (Role 1b) — synthesis, adjudication, confirms termination
- 3-tier termination (Hard auto / Judgment-based / Contested material)
- Research Budget Controller (policy/service, not agent) — budget management
- Auditor removed from budget role

**Re-review verdict:** ✅ **RESOLVED.** Selection is policy-driven (model-free, deterministic). Underwriter has no influence on case intake. Termination tiers prevent unnecessary Auditor involvement. Budget Controller is a service, not a role.

---

## F2 — NotebookLM Provenance

**Original finding:** NotebookLM findings can enter canonical registry without persistent provenance tag.

**Resolution applied:**
- Persistent `discovery_origin` metadata (type, notebook_id, request_id, synthesis_excerpt, discovered_url)
- `validation` sub-object (original_source_retrieved, hash, validator, status)
- Source authority (S1–S6) and discovery route are SEPARATE axes — both survive forever
- Hard invariant: NotebookLM without source validation = S6_UNVERIFIED_LEAD
- Negative tests: `NotebookLM_cannot_self_promote`, `NotebookLM_provenance_survives_promotion`

**Re-review verdict:** ✅ **RESOLVED.** Persistence is schema-enforced. S6 default is unconditional. Two-axis concept prevents provenance loss on promotion.

---

## F5 — Case Re-Open / New As-Of

**Original finding:** No path to update case when new information arrives.

**Resolution applied:**
- Case versioning: `QAD-2026-0001 v1 (as-of 2026-08-16)` → `v2 (as-of 2026-11-10)`
- Each Research Run immutable
- Prior Evidence/Claims retrievable
- Change package records what changed and why
- CASE_UPDATE state added to state machine

**Re-review verdict:** ✅ **RESOLVED.** Versioned append-only with lineage preserves history. Monitoring may trigger update. No silent backfill.

---

## F6 — Temporary Diagnosis Anchoring

**Original finding:** Single impairment classification before Red Team creates anchoring bias.

**Resolution applied:**
- Impairment Analyst produces: Primary Diagnosis + Strongest Competing Explanation + Why Primary Dominates + Weakest Link + Flip Evidence
- Red Team starts from: Research Charter + raw Evidence Graph + financial facts + original sources (NOT full analyst narrative)
- Red Team independently builds strongest Structural case

**Re-review verdict:** ✅ **RESOLVED.** Dual/completing output + raw-evidence start for Red Team effectively prevents anchoring. The analyst's narrative is preserved for comparison AFTER Red Team finishes.

---

## F7 — False Quality Gate

**Original finding:** No mandatory gate to detect false-quality cases before Full Research.

**Resolution applied:**
- Mandatory QUALITY_VERIFICATION state between EVIDENCE_BUILDING and ANALYSIS
- Role 6 (Business Analyst) must perform: What created historical economics? Durable mechanism? Transient factors? Customer/competitor evidence? Financial manifestation?
- Quality states: VERIFIED | PROBABLE | UNRESOLVED | FAILED
- Only FAILED → NOT_QAD_QUALITY termination
- UNRESOLVED may trigger targeted evidence acquisition
- False-quality hypothesis is mandatory alternative: "Company was never genuinely high quality"

**Re-review verdict:** ✅ **RESOLVED.** State machine explicitly enforces this gate. UNRESOLVED does not prematurely terminate. FAILED is evidence-grounded.

---

## F8 — Look-Ahead Leakage

**Original finding:** Model cutoff date tracking is insufficient to prevent outcome leakage.

**Resolution applied:**
- 3 evaluation layers: A (Named — workflow only), B (Entity-Masked), C (Synthetic/Counterfactual)
- Famous cases (Kodak, Blockbuster) classified as workflow-only, not core calibration
- Synthetic Layer C for cleanest test of causal impairment reasoning
- Entity-masked Layer B for reduced-leakage real-economics testing
- Sealed outcomes (separate directory, no agent access)

**Re-review verdict:** ✅ **RESOLVED.** 3-layer approach correctly separates workflow testing from predictive calibration. Famous-case leakage explicitly documented. Synthetic layer provides ground-truth causal testing.

---

## Remaining Verifications

| Original Finding | Status | Notes |
|------------------|--------|-------|
| F3 — Inter-rater reliability | ✅ RESOLVED | Simple agreement only for M4B. κ deferred to M14 (30–50+ cases) |
| F4 — Free model enforcement | ✅ RESOLVED | Model allowlist + pre-execution validation in Research Run manifest |
| F9 — Scuttlebutt cost runaway | ✅ RESOLVED | Max 3 investigators unless Chief Underwriter approves. Evidence Gap ID required. |
| F10 — Concrete model mapping | ✅ RESOLVED | Pro-forma tier mapping (example only, not constitutional) |

---

## Final Verdict

**All 10 adversarial findings from the original review are resolved.**

No material finding remains unresolved.

The corrected design package is internally consistent and ready for the PRE-CODE DESIGN GATE.

<!-- 2026-08-16 UTC+7 -->