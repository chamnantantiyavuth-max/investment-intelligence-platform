# Coverage Gap Detection — Template

**Status:** Operational Template  
**Version:** v0.1  
**Owner:** AI Intelligence Layer (Founder-reviewed)  
**Authority:** THEME-INTELLIGENCE.md §Coverage Gap Detection (FD #25)  

---

## Purpose

After every material pipeline run, the AI shall review the current system state and identify what the Founder may have overlooked — candidates, themes, sectors, or risks that are present in evidence but absent from the Watchlist or active monitoring.

Coverage gap detection is **AI-assisted discovery**, not automated decision-making. Gaps are surfaced for Founder review — never silently acted upon.

---

## Detection Triggers

Coverage gap detection runs:

- [ ] After every material pipeline run
- [ ] When a new Theme is approved (cross-reference against existing Watchlist)
- [ ] When an existing Theme shows strengthening evidence but no corresponding Watchlist additions
- [ ] When a sector or industry shows leadership breadth but the Watchlist has thin or zero coverage

---

## Gap Types

### 1. Theme Coverage Gap
An Approved Theme with strong evidence but zero or thin Candidate coverage in the Watchlist.

**Surface to Founder:** "This theme is strengthening but you have no candidates tracking it."

### 2. Candidate Blind Spot
A Candidate that repeatedly appears in evidence across multiple approved themes but is absent from the Watchlist.

**Surface to Founder:** With evidence summary and thesis prompt.

### 3. Sector Blind Spot
A sector or industry with improving breadth, relative strength, or fundamental momentum but no approved Theme or Watchlist coverage.

**Propose:** New Experimental Theme or prompt Founder review.

### 4. Risk Blind Spot
A risk factor (regulatory, competitive, macro) that appears in evidence across multiple Candidates or Themes but is not tracked in any thesis's key_risks.

**Surface:** Add to relevant theses or surface as a cross-cutting concern.

---

## Report Format

```markdown
# Coverage Gap Report
**Run:** {run_id}
**Date:** {date}
**Pipeline Version:** {version}
**Reviewer:** AI ({model})

## Summary
- Gaps detected: {count}
- Theme Coverage Gaps: {count}
- Candidate Blind Spots: {count}
- Sector Blind Spots: {count}
- Risk Blind Spots: {count}

## Gap Details

### Theme Coverage Gap: {title}
- **Theme:** {theme_id} — {theme_name}
- **Evidence Strength:** {summary}
- **Current Coverage:** {candidates_count} candidates
- **Recommendation:** {what to do}
- **Evidence References:** {list}

### Candidate Blind Spot: {ticker}
- **Candidate:** {ticker} — {name}
- **Appears In Themes:** {list of theme_ids}
- **Why Overlooked:** {why not on watchlist}
- **Evidence Summary:** {what the evidence says}
- **Recommendation:** {add to watchlist / monitor / dismiss}

### Sector Blind Spot: {sector/industry}
- **Sector/Industry:** {name}
- **Signal:** {what's happening}
- **Current Coverage:** {do we have any themes here?}
- **Recommendation:** {propose experimental theme / monitor}

### Risk Blind Spot: {risk factor}
- **Risk:** {description}
- **Affects:** {list of themes/candidates}
- **Current Tracking:** {is this in any key_risks?}
- **Recommendation:** {add to key_risks / surface as cross-cutting concern}

## Founder Decisions Required
- [ ] Decision 1
- [ ] Decision 2

## Disposition
- **Next Review:** {date or trigger}
```
---

## Rules

1. Gaps are surfaced, never silently acted upon.
2. Gap detection must reference specific evidence, not vague impressions.
3. A detected gap does not create an obligation to act — the Founder may consciously choose to leave a gap uncovered.
4. Gap detection results are included in the self-reflection log for traceability (Phase 6).
5. Reports are versioned and stored in `operational/coverage-gaps/`.
6. Approved: Gap reports that led to Founder action. Rejected: Gaps the Founder chose to ignore.
