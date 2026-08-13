# Stage 8 preflight baseline — sanitized rollback evidence

This directory contains SANITIZED rollback evidence for the Stage 8 preflight
checkpoint (2026-08-13). The raw runtime database is NOT stored here and MUST
NOT be committed to this public repository.

**Doctrine (P4 A+, 2026-08-13):**
> Public repo rollback evidence = hash + sanitized export + counts.
> Raw runtime DB = private backup only.

Files:
- `kanban-snapshot-manifest.json` — hash, size, counts, classification, restore procedure
- `sanitized-board-summary.json` — public-safe board metadata + status counts
- `board-iip.json.snapshot-2026-08-13` — board metadata JSON (public-safe, retained)

Raw backup location: PRIVATE/LOCAL (outside this repository; exact path not published).
Restore: see manifest.
