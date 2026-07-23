# Self-Reflection Log — Template

**Status:** Operational Template
**Version:** v0.1
**Owner:** AI Intelligence Layer (Founder-reviewed)
**Authority:** LEARNING-AND-KNOWLEDGE-LOOP.md §Self-Reflection Log (FD #25)

---

## Purpose

After every material pipeline run, assessment cycle, or investment decision, the AI shall produce a self-reflection log — a structured markdown record capturing what was learned, what changed, and what remains uncertain.

The self-reflection log enables **compound learning across runs**. Instead of starting from zero each cycle, the AI reviews its own prior assessments, identifies what was confirmed or contradicted, and surfaces lessons for the Founder.

---

## Required Sections

Every self-reflection log shall include all 7 sections. Sections may be marked "None" or "No changes" when appropriate — but none may be omitted.

### 1. Run Context
Timestamp, pipeline version, data vintage, themes evaluated, candidates assessed, and any special conditions (e.g., first run after model update, after data source change).

### 2. Thesis Status Changes
Which theses were Confirmed, Weakened, or Invalidated by new evidence since the last run. Include specific evidence references. Reference prior self-reflection logs where the thesis was previously assessed.

### 3. Surprises
What the AI or Founder did not expect. What contradicted prior assumptions. What was overlooked in previous assessments. Surprises may be positive (better than expected) or negative (worse than expected).

### 4. Mistakes Identified
What prior assessments were wrong. Why they were wrong (reasoning error, missing evidence, changed conditions). What should have been done differently. Be specific — reference the prior assessment and the new information that revealed the error.

### 5. Lessons
What should be remembered for future runs. What pattern or principle emerged. What the AI now understands that it did not understand before. Lessons may be promoted to formal Lesson entities after Founder review.

### 6. Open Questions
What remains uncertain. What evidence is still missing. What the system is waiting to learn. Open questions should be specific and falsifiable — not vague "we need more data."

### 7. Blind Spots
What themes, candidates, or risks the Founder may have overlooked. What is present in the evidence but absent from the Watchlist. Cross-reference with Coverage Gap Detection reports where applicable.

---

## Rules

1. Self-reflection logs are **AI-generated drafts** — they are not official knowledge until Founder reviews and approves specific lessons.
2. Logs are **cumulative**: each run's log references prior logs so the learning chain is traceable.
3. Logs are **versioned** and never silently overwritten.
4. Approved lessons extracted from self-reflection logs are promoted to the formal Lesson entity in the Learning Loop.
5. Self-reflection logs are part of the **AI Intelligence Layer** — they do not modify deterministic rules, scores, or thresholds without separate Founder approval.
6. Logs reference specific evidence IDs, run IDs, and prior log filenames — not vague recollections.
7. Logs are stored in `operational/self-reflection-logs/` with filename format: `YYYY-MM-DD-run-{run_id}.md`.

---

## Format

```markdown
# Self-Reflection Log
**Run:** {run_id}
**Date:** {date}
**Pipeline Version:** {version}
**Prior Log:** {filename or "None — first run"}

---

## 1. Run Context
...

## 2. Thesis Status Changes
...

## 3. Surprises
...

## 4. Mistakes Identified
...

## 5. Lessons
...

## 6. Open Questions
...

## 7. Blind Spots
...
```
