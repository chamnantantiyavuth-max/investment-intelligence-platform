# Company Intelligence Workbench — Quality Gates

**Status:** Approved v0.2 — FD-CIW-008 (Founder batch approval, 2 Aug 2026)
**Version:** 0.2
**Owner:** Founder
**Authority:** Draft CIW specification subordinate to the Constitution and Founder's Decisions
**Derived from:** `docs/CIW-INTEGRATION-AMENDMENT-MAP.md` §6; `evidence/COUNCIL_DECISION-bible-2026-08-02.md` Required Changes #8, #9; proposal §12.4, §20 (adapted); `FUNDAMENTAL-OPPORTUNITY-INTELLIGENCE.md` §4 (Independent Challenge)
**Approval:** FD-CIW-008 — Founder batch approval, 2 Aug 2026

---

## 1. Principle: Independent Review Is Mandatory and Operationally Independent

Required Change #8: for the pilot, **independent review is mandatory** and must be **operationally independent**:

- **No self-review** — the executor cannot review their own work, in any session or agent context.
- **Separate context** — reviewer runs in a separate session/context from the executor (separate agents, sessions, or models; never the same framing).
- **Direct source inspection** — the reviewer must inspect cited sources and calculations directly; review findings cannot be copied solely from the writer's summary.
- **Independence/provenance disclosure** — the review artifact identifies executor and reviewer identities/contexts and states what was independently verified.
- **Publication blocking** — if an eligible reviewer is unavailable, publication is **blocked** (no fallback to self-review or no-review).

The proposal's "separation when practical" (proposal §20.1) is **not sufficient** for the pilot — separation is mandatory (Required Change #8).

## 2. Minimum Research Quality Gates

Before any publication-ready state (LIFECYCLE: `Independent Review` → `Founder Review`), the research must pass (adapted from proposal §20.2):

| Gate | Checks |
|---|---|
| Source-coverage | Source map complete; no blocking `missing_required` / `failed_retrieval`; limitations visible (RESULT-CONTRACT §3) |
| Primary-source | Primary sources used where available; derived duplicates not counted as independent |
| Contradiction | Contradicting evidence recorded and visible; none averaged away |
| Unsupported-claim | Every material claim has claim-level evidence reference (RESULT-CONTRACT §4) |
| Stale-source | Freshness class and staleness default checked (Constitution §8 three-year rule) |
| Accounting red-flag | Revenue recognition, recurring "one-time" adjustments, SBC, off-balance-sheet items reviewed |
| Valuation-assumption | Valuation assumptions explicit and versioned (advisory only) |
| Deterministic-calculation | Calculations rerunnable from raw sources with lineage |
| Per-share | Per-share economics checked (dilution-adjusted) |
| Dilution | Dilution and share-count effects checked |
| Reverse-DCF | Where applicable — what the price implies |
| Permanent-loss | Permanent-loss mechanisms assessed (Module K) |
| Thesis-falsification | Invalidation conditions stated; minimum-evidence rule for thesis change (LIFECYCLE §3) |
| Artifact-lineage | Prior versions, update packages, and transitions auditable |
| Authority | No AI/Cron authoritative transitions; Founder gates respected |
| Scope | Research stayed within approved request scope and universe |

**Gate result states:** `Pass` → proceeds; `Fail` → returns to executor with findings; `Review Required` → human review; a gate can never be bypassed by claiming "non-material".

## 3. Independent Challenge (Phase 8 §4 alignment)

- CIW executes the **Shared Core Independent Challenge** (Phase 8 spec) with executor/reviewer separation.
- The challenge is a **required step** for pilot publication — not an optional extra.
- Challenge output is advisory to the Founder; **council/committee agreement is not Founder approval** (proposal §20.3).

## 4. Completion Standard

A completion claim must state (proposal §20.4, adopted):

- scope completed;
- sources reviewed;
- artifacts produced;
- calculations performed;
- checks run (list);
- limitations;
- unresolved risks;
- disagreements;
- deviations from the approved request;
- review status.

A completion claim **without** review status is incomplete.

## 5. First-Slice Gate Order (Required Change #9)

```
Approved Request → Source Map gate → bounded initial research → 
quality gates (§2) → Independent Challenge → Founder Review → Published
```

The first slice is complete only when this full chain passes. No earnings automation, recurring scheduling, Obsidian sync, or expanded file tree is required (or permitted) for first-slice completion.

## 6. Failure and Escalation

- Gate failures return findings to the executor; **bounded** rework cycles (retries bounded — no infinite loops).
- Repeated failure creates an **escalation record** to the Founder.
- Material conflicts between sources or between executor and reviewer require **human review** — never silent resolution.

---

*Approved v0.2 (FD-CIW-008). Source: Council verdict Required Changes #8, #9; Amendment Map §6; proposal §12.4/§20 adapted; Phase 8 spec §4.*
<!-- 2026-08-02 23:48 UTC+7 -->
