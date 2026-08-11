"""Read-only store for research blog reports (FD #62).

Serves the reports/ directory: frontmatter metadata (title/type/category/
subject/date/author/status/summary) + markdown body. Read-only; git is the
single writer and audit trail (same pattern as org_store — no schema, no writes).

Report file contract: see reports/README.md. Frontmatter parsed with PyYAML
(present in the project toolchain). Unknown/invalid files are skipped, never
invented.

Category taxonomy (FD #95 — blog layout structure A, 11 Aug 2026):
  company_weekly           — Weekly กลุ่มบริษัท (new genre, no reports yet)
  deep_research_radar      — 1.2.1 หุ้นที่คัดจากข้อมูลผิดปกติ (Radar, FD #71)
  deep_research_inflection — 1.2.2 Equity Inflection (FD #88/#89, no reports yet)
  deep_research_quality    — 1.2.3 on-demand/cron (Buffett/Pabrai/Li Lu/100 Baggers — WP2)
  cs_product               — 2. Close System products (commodity research)
  weekly                   — org weekly letters (existing genre)
"""
from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = REPO_ROOT / "reports"

# Canonical report types (display order — library filter).
REPORT_TYPES = ["company", "product", "weekly", "quarterly", "theme"]

# Canonical categories (display order — library grouping, FD #95).
REPORT_CATEGORIES = [
    "company_weekly",
    "deep_research_radar",
    "deep_research_inflection",
    "deep_research_quality",
    "cs_product",
    "weekly",
]

CATEGORY_LABELS = {
    "company_weekly": "Company Weekly",
    "deep_research_radar": "Deep Research — Anomaly",
    "deep_research_inflection": "Deep Research — Equity Inflection",
    "deep_research_quality": "Deep Research — Quality & Asymmetry",
    "cs_product": "Close System Products",
    "weekly": "Weekly Intelligence",
}

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
    category = str(meta.get("category") or "")
    # Backward-compatible default: product → cs_product, weekly → weekly,
    # company → deep_research_quality (on-demand). Never invented beyond type.
    if category not in REPORT_CATEGORIES:
        t = str(meta.get("type") or "company")
        category = {
            "product": "cs_product",
            "weekly": "weekly",
            "quarterly": "weekly",
            "theme": "deep_research_quality",
        }.get(t, "deep_research_quality")
    return {
        "slug": slug,
        "title": str(meta.get("title") or slug.replace("-", " ").title()),
        "type": str(meta.get("type") or "company"),
        "category": category,
        "subject": str(meta.get("subject") or ""),
        "date": str(meta.get("date") or ""),
        "author": str(meta.get("author") or ""),
        "status": str(meta.get("status") or "draft"),
        "updated": str(meta.get("updated") or ""),
        "summary": str(meta.get("summary") or ""),
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
    plain .md file inside reports/."""
    if not slug or ".." in slug or "/" in slug or "\\" in slug:
        return None
    path = (REPORTS_DIR / f"{slug}.md").resolve()
    try:
        path.relative_to(REPORTS_DIR.resolve())
    except ValueError:
        return None
    if not path.is_file() or path.suffix != ".md" or path.name == "README.md":
        return None
    return _parse_report(path)
