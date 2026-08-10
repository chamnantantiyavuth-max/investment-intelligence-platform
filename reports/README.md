# Reports — Research Blog Content (FD #62)

The research blog's content. Each report is a markdown SOURCE file (agents write in markdown —
git, evidence, review workflow); the blog renders it as a professionally typeset article. The
reader never sees raw markdown.

## File contract

- Location: `reports/<slug>.md`
- Frontmatter (YAML between `---` markers), parsed by the backend:

```yaml
---
title: "Report title"
type: company | product | weekly | quarterly | theme
subject: "AAPL" | "Silver (SLV)" | ...
date: 2026-08-06
author: "org-role (e.g., Commodity Analyst)"
status: draft | review | published
updated: 2026-08-06
summary: "One-line thesis for the library index"
---
```

- Body: free-form analytical markdown. Quality bar (FD #62): depth to the mechanism, real point
  of view, informative, reliable (every material figure date-stamped + sourced; point-in-time
  rule FD #58 applies — stale figures flagged).
- Status flow: draft → review (IC Secretary) → published (Founder approval). Only `published`
  reports appear on the library front page (draft/review visible via status filter for the owner).

## Content language

Research content is written in **Thai** (FD #92, 10 Aug 2026) — plain, easy-to-understand Thai,
composed fresh from the evidence (never a word-for-word translation of the English original).
Figures, accessions, dates, and point-in-time stamps are preserved exactly (FD #58);
financial/legal terms keep the English term in parentheses where needed (moat, CRO, ADEQUATE).
English originals survive only in git history + `evidence/` + `research/` workspaces
(evidence lineage — Constitution §23.9).

**Editorial layer (FD #94, 11 Aug 2026):** published articles are editorially synthesized by the
IC Secretary under `THAI-RESEARCH-EDITORIAL-STANDARD.md` — the article body is a clean
Founder-facing investment article (no mandate IDs, FD refs, spec sections, audit status,
workspace paths, or pipeline jargon); the internal governance layer lives in git history /
`research/` / `evidence/` / Audit Center. Weekly letters (`type: weekly`) are organizational
genre and keep internal references. Facts Locked: editorial edits never change figures, accessions,
dates, uncertainty, material dissent, or conclusions (token-preservation check enforced).

## Series

Reports about the same `subject` form a series (e.g., Silver — first note, updates, what changed).
The article page links the previous/next report in the series so history reads as a narrative.
