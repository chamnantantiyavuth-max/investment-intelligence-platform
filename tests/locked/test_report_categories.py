"""Locked-style tests — report category taxonomy (FD #95 blog layout).

Invariants under test:
  1. Every published report carries a valid category ∈ REPORT_CATEGORIES.
  2. Categories match the Founder-approved structure A mapping:
     - type=product → cs_product (Close System Products)
     - type=weekly → weekly
     - radar-origin company reports → deep_research_radar
     - mandate/on-demand company reports → deep_research_quality
  3. Every main/opposing pair shares the SAME category (companion nesting).
  4. Category labels exist for every canonical category (display contract).
  5. Backward-compat default: report without category field derives from type.
"""
import pytest

from backend.report_store import (
    CATEGORY_LABELS,
    REPORT_CATEGORIES,
    list_reports,
)


def test_all_published_reports_have_valid_category():
    reports = list_reports()
    assert len(reports) >= 24, f"expected >=24 reports, got {len(reports)}"
    for r in reports:
        assert r["category"] in REPORT_CATEGORIES, f"{r['slug']}: bad category {r['category']!r}"


def test_type_product_maps_to_cs_product():
    products = [r for r in list_reports() if r["type"] == "product"]
    assert products, "expected product-type reports"
    for r in products:
        assert r["category"] == "cs_product", f"{r['slug']}: {r['category']}"


def test_weekly_type_maps_to_weekly():
    # org weekly letters (type=weekly, subject contains "organization") → weekly
    weeklies = [r for r in list_reports() if r["type"] == "weekly" and "organization" in (r["subject"] or "").lower()]
    assert len(weeklies) == 3, f"expected 3 org weekly letters (WIL #1/#2/#3), got {len(weeklies)}"
    for r in weeklies:
        assert r["category"] == "weekly"


def test_company_weekly_genre():
    # FD #96 structure 1.1 — company weekly digest → company_weekly category
    cw = [r for r in list_reports() if r["category"] == "company_weekly"]
    assert len(cw) >= 1, "expected at least one company_weekly report (FD #96 genre 1.1)"
    for r in cw:
        assert r["type"] == "weekly", f"{r['slug']}: company_weekly should be type=weekly"


def test_radar_origin_reports_category():
    by_slug = {r["slug"]: r for r in list_reports()}
    for slug in [
        "apple-buyback-mask-test-2026-08-06",
        "apple-services-margin-verification-2026-08-06",
        "jnj-talc-resolution-2026-08-07",
    ]:
        assert by_slug[slug]["category"] == "deep_research_radar", slug


def test_quality_origin_reports_category():
    by_slug = {r["slug"]: r for r in list_reports()}
    for slug in [
        "apple-moat-2026-08-06",
        "apple-deep-analysis-2026-08-09",
        "apple-leadership-transition-2026-08-07",
    ]:
        assert by_slug[slug]["category"] == "deep_research_quality", slug


def test_main_opposing_pairs_share_category():
    by_slug = {r["slug"]: r for r in list_reports()}
    pairs = [
        ("apple-moat-2026-08-06", "apple-moat-opposing-2026-08-06"),
        ("apple-buyback-mask-test-2026-08-06", "apple-buyback-mask-test-opposing-2026-08-06"),
        ("silver-deficit-challenge-2026-08-06", "silver-deficit-challenge-opposing-2026-08-06"),
        ("gold-transmission-regime-2026-08-06", "gold-transmission-regime-opposing-2026-08-06"),
    ]
    for main, opp in pairs:
        assert by_slug[main]["category"] == by_slug[opp]["category"], (
            f"{main} ({by_slug[main]['category']}) != {opp} ({by_slug[opp]['category']})"
        )


def test_category_labels_cover_all_categories():
    for c in REPORT_CATEGORIES:
        assert c in CATEGORY_LABELS, f"missing label for {c}"
        assert CATEGORY_LABELS[c].strip()


def test_backward_compat_default_from_type():
    """A report lacking a category field derives from type (product→cs_product)."""
    from backend.report_store import _parse_report, REPO_ROOT
    from pathlib import Path
    import tempfile

    with tempfile.TemporaryDirectory(dir=str(REPO_ROOT)) as td:
        p = Path(td) / "x.md"
        p.write_text(
            "---\ntitle: Test\ntype: product\nsubject: Test\n---\nbody\n",
            encoding="utf-8",
        )
        parsed = _parse_report(p)
        assert parsed is not None
        assert parsed["category"] == "cs_product"
