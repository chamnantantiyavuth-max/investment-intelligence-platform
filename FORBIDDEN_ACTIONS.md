# FORBIDDEN_ACTIONS.md — alias

> **This file is a naming alias for project-workflow Phase -1 compliance.**
> The authoritative sources of truth are:

👉 **[AGENTS.md](AGENTS.md)** — Project-specific mandatory rules and current-phase restrictions
👉 **[operational/SCOPE-AND-NON-SCOPE.md](operational/SCOPE-AND-NON-SCOPE.md)** — Scope boundaries
👉 **[operational/SECURITY-AND-UNTRUSTED-CONTENT.md](operational/SECURITY-AND-UNTRUSTED-CONTENT.md)** — Security constraints

## Hard Prohibitions (summary)

- **No broker connectivity, execution, or portfolio allocation** — these belong to Capital Command (external)
- **No AI-invented investment rules**, thresholds, weights, formulas, lookbacks, benchmarks
- **No schema or migration** without explicit authorization
- **No Legacy or quarantine access** without separate named authorization
- **No final stack selection** — current technology is provisional
- **AI may recommend but never approve** — Founder retains final authority for material investment judgment
- **AI may not independently authorize capital allocation**, place or direct trades, alter approved policy
- **Experimental Themes must not alter** official filters, rankings, scores, or approved-strategy alerts
- **Never silently overwrite** evidence or AI-generated records to hide prior error
