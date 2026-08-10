"""Read-only store for research blog reports (FD #62).

Serves the reports/ directory: frontmatter metadata (title/type/subject/date/
author/status/summary) + markdown body. Read-only; git is the single writer
and audit trail (same pattern as org_store — no schema, no writes).

Report file contract: see reports/README.md. Frontmatter parsed with PyYAML
(present in the project toolchain). Unknown/invalid files are skipped, never
invented.
"""
from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = REPO_ROOT / "reports"

# Canonical report types (display order — library filter).
REPORT_TYPES = ["company", "product", "weekly", "quarterly", "theme"]

_FRONTMATTER = r"^---\s*\n(.*?)\n---\s*\n(.*)$"


def _parse_report(path: Path) -> dict | None:
    """Parse frontmatter + body. Returns None for invalid files."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    import re

    m = re.match(_FRONTMATTER, text, re.DOTALL)
    if not m:
        return None
    try:
        meta = yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return None
    if not isinstance(meta, dict):
        return None
    body = m.group(2).strip()
    slug = path.stem
    # Bilingual support (10 Aug 2026): Thai title/summary in frontmatter
    # (title_th / summary_th); Thai body in reports/th/<slug>.md when present.
    title_th = str(meta.get("title_th") or "") or None
    summary_th = str(meta.get("summary_th") or "") or None
    return {
        "slug": slug,
        "title": str(meta.get("title") or slug.replace("-", " ").title()),
        "title_th": title_th,
        "type": str(meta.get("type") or "company"),
        "subject": str(meta.get("subject") or ""),
        "date": str(meta.get("date") or ""),
        "author": str(meta.get("author") or ""),
        "status": str(meta.get("status") or "draft"),
        "updated": str(meta.get("updated") or ""),
        "summary": str(meta.get("summary") or ""),
        "summary_th": summary_th,
        "path": str(path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "content": body,
    }


def list_reports() -> list[dict]:
    """All report files sorted newest-first by date, then slug. No content."""
    reports = []
    if not REPORTS_DIR.is_dir():
        return reports
    for path in sorted(REPORTS_DIR.glob("*.md")):
        if path.name == "README.md":
            continue
        r = _parse_report(path)
        if r:
            r.pop("content", None)
            reports.append(r)
    reports.sort(key=lambda r: (r["date"], r["slug"]), reverse=True)
    return reports


def get_report(slug: str) -> dict | None:
    """Single report with body content. Traversal guard: slug must resolve to a
    plain .md file inside reports/. Thai body (reports/th/<slug>.md) is merged
    as `content_th` when present — the reader can switch languages."""
    if not slug or ".." in slug or "/" in slug or "\\" in slug:
        return None
    path = (REPORTS_DIR / f"{slug}.md").resolve()
    try:
        path.relative_to(REPORTS_DIR.resolve())
    except ValueError:
        return None
    if not path.is_file() or path.suffix != ".md" or path.name == "README.md":
        return None
    report = _parse_report(path)
    if report is None:
        return None
    # Thai body: reports/th/<slug>.md (optional)
    th_path = (REPORTS_DIR / "th" / f"{slug}.md").resolve()
    try:
        th_path.relative_to(REPORTS_DIR.resolve())
    except ValueError:
        th_path = None
    if th_path and th_path.is_file():
        try:
            text = th_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            text = ""
        m = __import__("re").match(_FRONTMATTER, text, __import__("re").DOTALL)
        report["content_th"] = (m.group(2).strip() if m else text.strip()) or None
    else:
        report["content_th"] = None
    return report
