"""Locked tests: Close System Product Radar V0 — 6-Stage Pipeline
All 5 synthetic fixtures — NOT LIVE DATA.
Pattern: same as Alpha Momentum V0 / FO / II locked suites.
"""
import sys
import os

# Use explicit path addition with cleanup to avoid cross-module fixture collision.
# Import close_system modules by full path to prevent polluting sys.modules['fixtures'].
_cs_dir = os.path.join(os.path.dirname(__file__), "..")
if _cs_dir not in sys.path:
    sys.path.insert(0, _cs_dir)

# Clear any previously cached 'fixtures' that might be from another module
_fixture_key = "fixtures"
if _fixture_key in sys.modules:
    cached = sys.modules[_fixture_key]
    if "close_system" not in getattr(cached, "__file__", ""):
        del sys.modules[_fixture_key]

import importlib
_fixtures = importlib.import_module("fixtures")
PRODUCTS = _fixtures.PRODUCTS
PIPELINE_CONFIG = _fixtures.PIPELINE_CONFIG

_pipeline = importlib.import_module("pipeline")
run_pipeline = _pipeline.run_pipeline
stage_universe = _pipeline.stage_universe
stage_p1_eligibility = _pipeline.stage_p1_eligibility
stage_p2_discount = _pipeline.stage_p2_discount
stage_p3_demand = _pipeline.stage_p3_demand
stage_synthesis = _pipeline.stage_synthesis
stage_radar = _pipeline.stage_radar
RUN_ID = _pipeline.RUN_ID
PIPELINE_VERSION = _pipeline.PIPELINE_VERSION

# Clean up sys.modules to prevent cross-module fixture collision.
# After importing close_system fixtures/pipeline, remove them so other
# modules (FO, II) can import their own fixtures without collision.
for _mod in ["fixtures", "pipeline"]:
    if _mod in sys.modules:
        del sys.modules[_mod]

# ── Fixture counts ──
TOTAL_PRODUCTS = 5
PRODUCT_IDS = ["CS-001", "CS-002", "CS-003", "CS-004", "CS-005"]


class TestFixtureIntegrity:
    """Verify synthetic fixture data is consistent and complete."""

    def test_5_products_total(self):
        assert len(PRODUCTS) == TOTAL_PRODUCTS

    def test_all_have_required_ids(self):
        ids = [p["id"] for p in PRODUCTS]
        assert ids == PRODUCT_IDS

    def test_all_p1_eligible(self):
        """All V0 fixtures must satisfy P1 (cannot go to zero)."""
        for p in PRODUCTS:
            assert p.get("p1_eligible", False), f"{p['id']} should be p1_eligible"

    def test_copper_not_at_discount(self):
        """CS-004 (COPPER) is explicitly NOT at discount — tests P2 rejection."""
        copper = [p for p in PRODUCTS if p["id"] == "CS-004"][0]
        assert copper["p2_discount"] is False
        assert copper["discount_depth"] == "None"

    def test_copper_has_target_entry(self):
        copper = [p for p in PRODUCTS if p["id"] == "CS-004"][0]
        assert "target_discount_entry" in copper["discount_detail"]
        assert copper["discount_detail"]["target_discount_entry"] is not None


class TestPipelineStructure:
    """Verify run_pipeline returns correct top-level structure."""

    def test_returns_run_id(self):
        result = run_pipeline()
        assert result["run_id"].startswith("CS-V0-")

    def test_has_pipeline_metadata(self):
        result = run_pipeline()
        assert result["pipeline_version"] == "v0.1.0"
        assert result["pipeline_name"] == "Close System Product Radar V0"
        assert result["strategy"] == "Close System"
        assert "SYNTHETIC" in result["fixture_category"]

    def test_has_6_stages(self):
        result = run_pipeline()
        stages = result["stages"]
        assert len(stages) == 6
        stage_ids = [s["stage_id"] for s in stages]
        assert stage_ids == ["S1", "S2", "S3", "S4", "S5", "S6"]

    def test_has_synthesized_and_radar(self):
        result = run_pipeline()
        assert "synthesized" in result
        assert "radar" in result
        assert len(result["synthesized"]) == TOTAL_PRODUCTS

    def test_pipeline_deterministic(self):
        """Same input = same output (no random/noise)."""
        r1 = run_pipeline()
        r2 = run_pipeline()
        # Compare synthesized packages (ignore run_id / timestamp)
        for i in range(TOTAL_PRODUCTS):
            s1 = dict(r1["synthesized"][i])
            s2 = dict(r2["synthesized"][i])
            s1.pop("run_id", None); s2.pop("run_id", None)
            assert s1 == s2, f"Synthesized item {i} differs between runs"


class TestS1Universe:
    """Stage 1: Universe Definition."""

    def test_selects_all_5(self):
        s1, selected = stage_universe(PRODUCTS)
        assert s1["total_products"] == TOTAL_PRODUCTS
        assert s1["selected_count"] == TOTAL_PRODUCTS
        assert len(selected) == TOTAL_PRODUCTS


class TestS2P1Eligibility:
    """Stage 2: P1 — Cannot Go to Zero."""

    def test_all_5_pass_p1(self):
        s2, eligible = stage_p1_eligibility(PRODUCTS)
        assert s2["passed_count"] == TOTAL_PRODUCTS
        assert s2["rejected_count"] == 0

    def test_p1_returns_product_dicts(self):
        _, eligible = stage_p1_eligibility(PRODUCTS)
        for p in eligible:
            assert "id" in p
            assert "ticker" in p


class TestS3P2Discount:
    """Stage 3: P2 — Discount Pricing."""

    def test_discount_count(self):
        s3, results = stage_p2_discount(PRODUCTS)
        # 4 products at discount (CS-001, CS-002, CS-003, CS-005)
        assert s3["at_discount"] == 4

    def test_copper_not_at_discount(self):
        _, results = stage_p2_discount(PRODUCTS)
        copper = [r for r in results if r["id"] == "CS-004"][0]
        assert copper["discount"] is False
        assert copper["discount_depth"] == "None"

    def test_discount_depth_breakdown(self):
        s3, _ = stage_p2_discount(PRODUCTS)
        bd = s3["discount_breakdown"]
        assert bd["Maximum"] == 1  # CS-003 TLT
        assert bd["Strong"] == 2   # CS-002 XLE, CS-005 SLV
        assert bd["Moderate"] == 1  # CS-001 GDX
        assert bd["None"] == 1      # CS-004 COPPER


class TestS4P3Demand:
    """Stage 4: P3 — Structural Demand."""

    def test_all_have_demand(self):
        s4, results = stage_p3_demand(PRODUCTS)
        assert s4["with_structural_demand"] == TOTAL_PRODUCTS

    def test_demand_types_present(self):
        s4, _ = stage_p3_demand(PRODUCTS)
        types = s4["demand_types"]
        assert any("Industrial Consumption" in t for t in types)
        assert any("Monetary" in t for t in types)


class TestS5Synthesis:
    """Stage 5: Cross-Layer Synthesis."""

    def test_copper_ineligible_p2(self):
        """CS-004 fails P2 → synthesized has p2_pass=False, eligible=False."""
        _, p2r = stage_p2_discount(PRODUCTS)
        _, p3r = stage_p3_demand(PRODUCTS)
        s5, synthesized = stage_synthesis(PRODUCTS, p2r, p3r)
        copper = [s for s in synthesized if s["id"] == "CS-004"][0]
        assert copper["p1_pass"] is True
        assert copper["p2_pass"] is False
        assert copper["p3_pass"] is True
        assert copper["eligible"] is False
        assert "Ineligible (P2" in copper["status"]

    def test_tlt_fully_eligible(self):
        """CS-003 TLT passes all P1-P3."""
        _, p2r = stage_p2_discount(PRODUCTS)
        _, p3r = stage_p3_demand(PRODUCTS)
        _, synthesized = stage_synthesis(PRODUCTS, p2r, p3r)
        tlt = [s for s in synthesized if s["id"] == "CS-003"][0]
        assert tlt["eligible"] is True
        assert tlt["p1_pass"] is True
        assert tlt["p2_pass"] is True
        assert tlt["p3_pass"] is True

    def test_eligible_sorted_first(self):
        """Eligible products sort before ineligible."""
        _, p2r = stage_p2_discount(PRODUCTS)
        _, p3r = stage_p3_demand(PRODUCTS)
        _, synthesized = stage_synthesis(PRODUCTS, p2r, p3r)
        eligible = [s for s in synthesized if s["eligible"]]
        ineligible = [s for s in synthesized if not s["eligible"]]
        # All eligible must appear before first ineligible
        last_eligible_idx = max(synthesized.index(e) for e in eligible)
        first_ineligible_idx = min(synthesized.index(i) for i in ineligible)
        assert last_eligible_idx < first_ineligible_idx

    def test_conviction_breakdown(self):
        s5, _ = stage_synthesis(PRODUCTS,
            stage_p2_discount(PRODUCTS)[1],
            stage_p3_demand(PRODUCTS)[1])
        cb = s5["conviction_breakdown"]
        # Breakdown must account for every input product (spec §5.1 4-level scale)
        assert sum(cb.values()) == s5["input_count"]
        assert cb["Maximum"] == 1  # SLV — 5/5 layers + hidden corroboration + discount confirmed
        assert cb["High"] >= 1    # TLT
        assert cb["Moderate"] >= 2  # GDX, XLE
        assert cb["Low"] >= 1      # COPPER

    def test_conviction_priority_order(self):
        # Maximum must sort ahead of High in the prioritized eligible bucket (spec §5.1)
        s5, synthesized = stage_synthesis(PRODUCTS,
            stage_p2_discount(PRODUCTS)[1],
            stage_p3_demand(PRODUCTS)[1])
        eligible = [s for s in synthesized if s["eligible"]]
        slv_idx = next(i for i, s in enumerate(eligible) if s["ticker"] == "SLV")
        tlt_idx = next(i for i, s in enumerate(eligible) if s["ticker"] == "TLT")
        assert eligible[slv_idx]["conviction"] == "Maximum"
        assert slv_idx < tlt_idx


class TestS6Radar:
    """Stage 6: Radar Assembly."""

    def test_radar_buckets(self):
        _, s2r = stage_p1_eligibility(PRODUCTS)
        _, p2r = stage_p2_discount(s2r)
        _, p3r = stage_p3_demand(s2r)
        _, synthesized = stage_synthesis(s2r, p2r, p3r)
        s6, radar = stage_radar(synthesized)
        assert s6["present_to_founder"] >= 1
        assert s6["deep_research"] >= 1
        assert s6["radar_watchlist"] >= 1
        assert s6["monitor"] >= 1
        assert s6["ineligible"] >= 1

    def test_tlt_slv_present_to_founder(self):
        _, s2r = stage_p1_eligibility(PRODUCTS)
        _, p2r = stage_p2_discount(s2r)
        _, p3r = stage_p3_demand(s2r)
        _, synthesized = stage_synthesis(s2r, p2r, p3r)
        _, radar = stage_radar(synthesized)
        ptf_ids = [s["id"] for s in radar["present_to_founder"]]
        assert "CS-003" in ptf_ids  # TLT
        assert "CS-005" in ptf_ids  # SLV

    def test_copper_in_monitor(self):
        _, s2r = stage_p1_eligibility(PRODUCTS)
        _, p2r = stage_p2_discount(s2r)
        _, p3r = stage_p3_demand(s2r)
        _, synthesized = stage_synthesis(s2r, p2r, p3r)
        _, radar = stage_radar(synthesized)
        monitor_ids = [s["id"] for s in radar["monitor"]]
        assert "CS-004" in monitor_ids  # COPPER → wait for better price
