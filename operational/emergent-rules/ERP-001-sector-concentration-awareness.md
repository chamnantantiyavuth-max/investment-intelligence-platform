# Emergent Rule Proposal: Sector Concentration Awareness

**Proposal ID:** ERP-001  
**Status:** Draft — awaiting Founder review  
**Proposed By:** AI (DeepSeek V4 Pro)  
**Date:** 2024-07-23  
**Related Pipeline Runs:** AM-V0-20260720, AM-V0-20260722, AM-V0-20260723  

---

## Proposed Rule

The Research Queue display shall annotate sectors where more than 50% of total candidates originate from a single sector, surfacing a "Sector Concentration Notice" in the queue header. This does not change the queue — it adds awareness metadata.

## Originating Pattern

Across 3 consecutive pipeline runs, the Technology sector consistently contributes 5 of 6 total candidates (83%), with Healthcare contributing the remaining 1. The 5 approved themes are Technology (4) + Healthcare (1) — the sector skew is built into the theme selection, not a pipeline defect.

However, the coverage gap report (2024-07-01) identified that sectors like Financials, Energy, and Industrials have zero coverage. This is a conscious Founder decision (Alpha Momentum V0 scope), but future pipeline runs may benefit from making sector concentration visible rather than implicit.

## Supporting Evidence

- Run AM-V0-20260720: Tech 5/6 (83%), Healthcare 1/6 (17%)
- Run AM-V0-20260722: Tech 5/6 (83%), Healthcare 1/6 (17%)
- Run AM-V0-20260723: Tech 5/6 (83%), Healthcare 1/6 (17%)
- Coverage Gap #4: Financials sector has zero themes, zero candidates
- The 143-theme controlled set spans all 11 GICS sectors — but V0 approved themes are concentrated

## Counter-Evidence

- Alpha Momentum V0 is explicitly a vertical slice — sector concentration is expected and acceptable at this stage.
- The Operating Model reserves Fundamental & Opportunity Intelligence (V1+) for broader sector coverage.
- Adding a concentration warning might create noise without actionable value at V0 scale.
- The Founder may prefer to keep V0 simple and address concentration in V1 theme expansion.

## Scope

- [x] Alpha Momentum V0 only
- [ ] All Momentum & Market Leadership strategies
- [ ] All strategies (Shared Core rule)

## Interaction with Existing Rules

This rule **extends** the display layer only — it does not modify pipeline filtering, scoring, or ranking. It is compatible with DS-508 (Show-all) and DS-509 (Empty queue valid). It adds a metadata annotation that may inform future Phase 5 theme expansion decisions.

## Implementation Impact

- **Files affected:** `display.py` (add sector concentration calculation), `templates/queue.html` (add notice banner if concentration > 50%)
- **Pipeline stage:** None — display layer only
- **Display impact:** Small banner in queue header: "⚠️ Sector Concentration: 83% of candidates from Technology sector"
- **Backward compatibility:** Fully backward compatible — no existing behavior changed

## Founder Decision

- [ ] **Approve** — add concentration notice to queue display
- [ ] **Reject** — concentration is expected at V0, no notice needed
- [ ] **Revise** — request changes: ___________
