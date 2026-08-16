# Resolution Matrix — Adversarial Findings → Founder Corrections

> **Round:** Final Pre-Code Resolution
> **Maps:** Every finding from INDEPENDENT-ADVERSARIAL-REVIEW.md to the Founder's corrections

---

| Finding | Severity | Founder Correction | Status | Affected Artifact |
|---------|----------|-------------------|--------|-------------------|
| **F1** Chief Underwriter too many authorities | 🔴 HIGH | Autonomous Selection Engine (policy-driven) + Research Director → Chief Underwriter separation. No standing committee. | ✅ ACCEPTED + MODIFIED | Pack A |
| **F1a** Termination requires Auditor concurrence | — (raised in resolution) | 3-tier termination: Hard-fail auto, Judgment-based (Director+Underwriter), Contested Material (Auditor process check) | ✅ ACCEPTED + REFINED | Pack A |
| **F1b** Budget Override should not involve Auditor | — (raised in resolution) | Research Budget Controller (policy/service, not agent). Auditor verifies logging only. | ✅ ACCEPTED | Pack A, Pack C |
| **F2** NotebookLM provenance not persistent | 🔴 HIGH | Persistent discovery_origin metadata. S6 invariant for unvalidated NotebookLM. Negative tests. | ✅ ACCEPTED + STRENGTHENED | Pack B |
| **F3** No inter-rater reliability | 🟡 MEDIUM | κ ≥ 0.7 rejected for M4B. Simple Reviewer A/B agreement + record disagreement. κ deferred to M14 (30–50+ cases). | ✅ MODIFIED | Pack C |
| **F4** Free-model enforcement absent | 🟡 MEDIUM | Model allowlist at routing config level. Pre-execution validation. | ✅ ACCEPTED | Pack B (Research Run manifest) |
| **F5** No case re-open with new as-of | 🟡 MEDIUM | Case lineage: QAD-2026-0001 v1 → v2. Each Research Run immutable. Change package tracked. | ✅ ACCEPTED | Pack B |
| **F6** Temporary diagnosis anchored before Red Team | 🔴 HIGH | Impairment Analyst produces: Primary + Strongest Competing + Weakest Link + Flip Evidence. Red Team starts from raw evidence graph (not analyst narrative). | ✅ ACCEPTED + MODIFIED | Pack A, Pack B |
| **F7** No false-quality detection gate | 🔴 HIGH | Mandatory QUALITY_VERIFICATION with 4 states (VERIFIED/PROBABLE/UNRESOLVED/FAILED). Only FAILED rejects. | ✅ ACCEPTED | Pack A, Pack B |
| **F8** Look-ahead leakage risk underestimated | 🟡 MEDIUM | 3 evaluation layers: A (Named — workflow only), B (Entity-Masked), C (Synthetic/Counterfactual). Model cutoff alone insufficient. | ✅ ACCEPTED + STRENGTHENED | Pack C |
| **F9** Scuttlebutt cost runaway | 🟡 MEDIUM | Per-case investigator limit (max 3 unless Chief Underwriter approves). Evidence Gap ID required before spawning. | ✅ ACCEPTED | Pack A, Pack C |
| **F10** No concrete model mapping | 🔵 LOW | Pro-forma tier mapping added (example only, not constitutional). | ✅ ACCEPTED | Pack A |
| — | — | **Outcomes must be physically sealed** | ✅ ACCEPTED | Pack C |
| — | — | **Pre-M5 fixtures: 10 minimum** | ✅ ACCEPTED | Pack C |
| — | — | **Constitution technology/language neutral** | ✅ ACCEPTED | Draft Constitution |
| — | — | **~17 specs → 8–10 consolidated specs** | ✅ ACCEPTED | Lean Spec Plan |
| — | — | **Legacy capabilities not unnecessarily prohibited** | ✅ ACCEPTED | Draft Constitution |
| — | — | **Fixture selection must isolate subsystem being tested** | ✅ ACCEPTED | Pack C |

## Summary

| Severity | Total | Resolved |
|----------|-------|----------|
| 🔴 HIGH | 4 | 4 (F1 split into 3 sub-fixes, F2, F6, F7) |
| 🟡 MEDIUM | 4 | 4 (F3, F5, F8, F9) |
| 🔵 LOW | 1 | 1 (F10) |
| Additional | 4 | 4 (sealed outcomes, 10 fixtures, tech-neutral constitution, 8–10 specs) |

**All findings addressed.** No unresolved material finding remains.

---

## Founder Authorization

| Item | Status | Date |
|------|--------|------|
| QAD Architecture Design Gate | ✅ **APPROVED** | 2026-08-16 |
| M1–M4B authorized | ✅ **YES** | 2026-08-16 |
| M5 Implementation Gate | ⏳ **PENDING** | — |
| FD #130 (Direction) | ✅ Recorded | 2026-08-16 |

**Frozen architectural decisions per Founder approval:** 19 decisions as listed in ARCHITECTURE-DESIGN-GATE-FINAL.md.

<!-- 2026-08-16 UTC+7 -->