# COUNCIL DECISION

## Gate — UI Visual Review (Phase M, FD #51 Research Desk)

## Verdict — RETEST

## Material Findings — critical only; each: concrete + evidence (file:line or screenshot) + material impact + smallest correction + verify method

1. **The Screener hides approved qualitative truth inside truncated cells.** Evidence: `evidence/ui/redesign-research-desk/02-screener-desktop.png` visibly clips values such as completeness, reliability, freshness, and extension-risk strings; `frontend/src/pages/AMScreenerPage.tsx:68-98` applies `max-w-[110px] truncate` to every matrix value, while `frontend/src/components/StatusBadge.tsx:25-29` provides no full-value disclosure. Material impact: the page promises the “full rule pack” and supports candidate comparison, but the user cannot read material criteria without guessing; this conflicts with `design/PAGE_BLUEPRINTS.md:41-46` and the no-hidden-context direction. Smallest correction: remove value truncation and let cells wrap or size to the full qualitative strings; retain horizontal scrolling for the wide matrix. Verify: browser-check all 10 × 18 populated cells at desktop and compact-laptop widths and confirm no value is clipped or available only by hover.

2. **Several implemented surfaces still use the retired generic Card containment language and exceed the approved 0–2 border budget.** Evidence: `frontend/src/components/EvidencePanel.tsx:18-36` renders three full-perimeter evidence boxes whenever any section has content; `frontend/src/pages/InstitutionalPage.tsx:69-146` renders three KPI Cards plus a fourth Card around the table; `frontend/src/pages/WeakSignalInboxPage.tsx:40-85` renders every anomaly or hypothesis as a Card; and the shared Card itself uses `ring-1` and `rounded-xl` at `frontend/src/components/ui/card.tsx:11-17`. Material impact: these screens revert to a KPI-grid/card-stack visual grammar, exceed the border budget, and break the cross-page Research Desk composition approved in `design/UI_DIRECTION.md:8-15,31-33` and `design/PAGE_BLUEPRINTS.md:6-11,86-88`. Smallest correction: make EvidencePanel sections tonal/open; replace the Institutional KPI Cards with one aligned stats line and unwrap the table into an open ledger; replace Weak Signal Cards with separated ledger rows while preserving the same content and disabled-action honesty. Verify: capture populated Theme Falsification, Institutional, and both Weak Signal tabs; count ordinary full-perimeter content outlines per viewport (target 0, maximum 2) and confirm no `rounded-xl ring-1` Card remains on these page flows.

3. **Close System Radar does not present the approved judgment surface needed to answer its primary decision.** Evidence: `design/USER_DECISION_MAP.md:18` asks “What product should I watch?” and `design/PAGE_BLUEPRINTS.md:48-52` requires a lead product, P1–P3 eligibility, five-layer synthesis, qualitative conviction, and key risks; `frontend/src/pages/CSRadarPage.tsx:31-84` provides only a heading, synthetic banner, and undifferentiated table, including a numeric confidence gauge at lines 75-77. Material impact: the user must synthesize the answer from table columns and cannot see several approved truth dimensions, so the page does not support its intended decision despite truthful SYNTHETIC labeling. Smallest correction: add one dominant lead-product judgment region and the approved eligibility/synthesis/conviction/risk fields using admitted response fields only; where a field is absent, render an explicit unavailable state rather than inventing data. Keep the table as the reference tier. Verify: populated browser review must answer the primary question above the fold and trace every displayed judgment to the CS response while retaining the prominent SYNTHETIC banner.

4. **Login input boundaries are visually undiscoverable in the default state.** Evidence: the live Login browser capture shows labels and entered username but no discernible input rectangles; `frontend/src/components/ui/input.tsx:8-15` uses `border-input bg-transparent`, while `frontend/src/index.css:34-38` maps the input border token to white on the white form surface. Material impact: the authentication workflow’s editable targets—especially the empty password field—are ambiguous, weakening interaction clarity and accessibility on the entry gate. Smallest correction: give inputs a visible functional `border-rule` boundary and an explicit white input background (add/use the approved `bg-input` surface token without using it as the border color). Verify: desktop browser screenshot plus keyboard Tab/focus-visible check; confirm default boundaries are visible and the 2px steel-blue focus treatment remains clear.

## Required Changes — smallest sufficient corrections (numbered)

1. Render every Screener matrix value in full; preserve horizontal scrolling rather than truncating approved qualitative strings.
2. Remove legacy Card containment from Theme evidence, Institutional stats/table, and Weak Signal lists; restore open ledgers/tonal sections and document a 0–2 outline count per reviewed viewport.
3. Recompose CS Radar as lead judgment plus reference table using only admitted truth; expose unavailable approved dimensions honestly.
4. Restore visible functional boundaries for Login inputs and verify default and focus-visible states.
5. After these corrections, run a fresh authenticated Phase M browser retest of Dashboard, AM Queue, Theme Card (Dimensions and Falsification), Screener, CS Radar, Institutional, and Weak Signals; capture fresh Dashboard and Screener screenshots and check the console on the authenticated route set.

## Evidence Gaps — None | list

- Fresh authenticated traversal and new Dashboard/Screener captures could not be completed because the execution guard denied access to the local `.env` credential value. The live Login page and its zero-error console were browser-verified; the current approved Dashboard and Screener screenshots were independently inspected; all protected-route findings above are additionally grounded in HEAD source. This gap must be closed in the retest.
- Mobile 390 × 844 remains `EXTERNAL_NOT_TESTED`, consistent with the implementer packet; no mobile-only finding is asserted here.

## Founder Decisions Required — None | list

- None. The required changes are corrections back to FD #51 direction A and the approved page blueprints; they do not reopen A-01/A-02 or require new scope.

## Minority Warning — None | description

- None.

## Scope Expansion Check — none | rejected | founder approval required

- none

---

## ROUND 2 (2026-08-04, 16:56) — Verdict: RETEST

### Round-1 disposition
- **F1 Screener truncation — FIXED** (zero clipped matrix elements; tables keep overflow-x auto)
- **F2 Legacy Cards — PARTIALLY FIXED** → EvidencePanel still bordered (see finding 1 below)
- **F3 CS Radar lead judgment — FIXED** (JNJ lead from admitted data; honest unavailable P1–P3/5-layer/conviction/risks + FD #46 note)
- **F4 Login input boundary — FIXED** (1px rgb(194,198,203) visible; steel-blue focus ring)

### Material Findings
1. Theme Card Falsification: 3 outlined evidence boxes (EvidencePanel.tsx:20 `border border-border bg-card`) exceed the 0–2 budget.
2. Base UI native-button semantic errors on AM Queue + Theme Card (Button with `render={<Link/>}`).
3. Screener duplicate React keys (`CAND-001` across themes) — reconciliation risk.

### Required Changes
1. EvidencePanel boxes → borderless tonal/open.
2. Link-rendering Buttons → correct Base UI semantics.
3. Screener keys → theme-scoped `${themeId}:${candidateId}`.
4. Repeat authenticated traversal with cleared console → zero errors.

## ROUND 3 disposition (Parent re-verify, 2026-08-04 17:05 — fixes in commit, see below)
- Finding 1 — FIXED: EvidencePanel `border border-border bg-card` → `bg-bg-panel`. Live computed-style scan on Falsification tab: **0 visible full-perimeter content outlines** (only 1 semantic provenance chip + 4 transparent-border tab buttons, both excluded by policy). BROWSER_VERIFIED.
- Finding 2 — FIXED: `nativeButton={false}` on the 3 Link-rendering Buttons. Console after login → Theme Card → Falsification: **0 errors, 0 Base UI warnings**. BROWSER_VERIFIED.
- Finding 3 — FIXED: Screener keys `${themeId}:${candidateId}` (thead + tbody). Console clean on Screener. BROWSER_VERIFIED.
- Required change 4 — DONE: cleared-console traversal (login → AM Queue → Theme Card → Screener → CS Radar → FO → Institutional → Weak Signals), all routes 200, console 0 errors. BROWSER_VERIFIED.
- Suite/build: 304/304, build exit 0. TEST_VERIFIED.

**Final status for Founder presentation: all round-1 + round-2 council findings remediated and independently re-verified. Formal round-3 council PASS available on request.**
