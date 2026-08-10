# Thai Research Editorial Standard — IIP Published Articles

**Contract:** FD #94 (Publication Firewall + Thai Editorial Standard, 11 Aug 2026) · supersedes the
plain-language clause of FD #92 with an enforceable editorial layer · complements `reports/README.md`
(file contract) — this file governs **how published articles read**, not what they analyze.

## Purpose

The blog is the product. Every published article must read like an investment article a
professional can follow **without knowing IIP exists** — never like a project log.

## Scope

- **Applies to:** research articles (`type: company | product | theme`) — all analysis published on
  /library.
- **Does NOT apply to:** `type: weekly` letters — those are organizational intelligence for the
  Founder (genre: internal status letter), where internal references (FDs, cards) are appropriate.

## The firewall: two layers, one gate

```
Lead analyst draft → CRO / audit → ═══ FACTS LOCKED ═══ → IC Secretary (editor) → readability check → publish
```

- **Internal layer (never shown in the article body):** mandate IDs (RM-2026-XXXX), decision refs
  (FD #NN), card IDs (ORG-2026-XXXX), spec sections (§3.x.x), audit status (MAJOR / CLEAN WITH
  MINORS / re-audit / item N), workspace paths, pipeline/API identifiers, portfolio-blind doctrine,
  corrections records (SILVER-CORR-xxx), agent-dispatch notes. These live in: git history,
  `research/` workspaces, `evidence/`, Audit Center.
- **Facts Locked (the editor may NOT change):** every figure, accession, date, point-in-time stamp,
  uncertainty level, material dissent, and conclusion. Verifiable by the token-preservation check
  (numbers/accessions/dates must be identical before and after editorial edits).

## Editorial rules

1. Write like a Thai analyst explaining to an experienced investor — plain, flowing Thai.
2. Thai prose first; English term in parentheses only on first use when needed (moat, CRO).
3. Never translate a research draft sentence-by-sentence — read the full package, close the draft,
   rewrite from the argument and evidence (fresh composition).
4. One central idea per paragraph; thesis must read as a causal narrative, not a list.
5. Every material figure carries its period/source without breaking the flow.
6. Classifications (HIGH / MEDIUM / INCONCLUSIVE / ADEQUATE) used only where they carry meaning.
7. No project governance terminology in the body — the reader never sees internal IDs.
8. No invented rules, thresholds, or interpretations (FD #53 discipline carries into prose).
9. Uncertainty and dissent are preserved, never softened for readability.
10. A reader who has never heard of IIP must understand the article 100% on first read.

## Editor authority

The IC Secretary is the editor (existing role — no new agent). The editor may: rewrite, reorder,
shorten, merge paragraphs, explain terms, change the headline, smooth the narrative. The editor may
NOT: change facts, change figures, reduce uncertainty, remove material dissent, change conclusions,
or introduce new analysis.

## Verification

Every editorial pass over a published article MUST re-run the token-preservation check
(`evidence/qa/fd92-token-preservation.py` pattern — numeric/accession/date tokens vs the committed
baseline) and a Thai-readability spot check. A clean article must pass with 0 missing tokens.

---
*Governance encoding: amendment pattern — FD #94 registered in FOUNDERS-DECISIONS item 110, fd_count 110.*
<!-- 2026-08-11 03:30 UTC+7 -->
