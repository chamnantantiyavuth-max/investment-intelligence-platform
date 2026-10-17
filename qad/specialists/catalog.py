"""Load specialist configs and refuse any that override role authority.

Display names are the six core capabilities named for this router and the
eleven investigator names in QAD-MODERN-SCUTTLEBUTT-PROTOCOL.md §2.
The expected canonical role for each id is fixed here from
QAD-M3-ROLE-AND-SERVICE-REGISTRY.md §3. A config file that names a
different role does not load.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from qad.specialists.separation import (
    BUSINESS_INDUSTRY,
    ELASTIC,
    FINANCIAL_MANAGEMENT,
    IMPAIRMENT,
    VALUATION,
)

CONFIG_PATH = Path(__file__).with_name("configs") / "dimensions.json"

FORBIDDEN_DESK_CLASSES = frozenset({"L8", "L9", "L10"})

CORE_IDS: tuple[str, ...] = (
    "business_quality_moat",
    "industry_economics_capital_cycle",
    "financial_reconstruction_accounting_quality",
    "management_capital_allocation",
    "impairment_diagnosis_recovery",
    "valuation_market_implied_expectations",
)

INVESTIGATOR_IDS: tuple[str, ...] = (
    "customer_product_investigator",
    "competitor_investigator",
    "supplier_investigator",
    "distributor_channel_investigator",
    "employee_organization_investigator",
    "digital_social_investigator",
    "regulatory_investigator",
    "technology_ip_investigator",
    "scientific_clinical_investigator",
    "geographic_investigator",
    "industry_specialist",
)

EXPECTED_DISPLAY_NAMES: frozenset[str] = frozenset(
    {
        "Business Quality & Moat",
        "Industry Economics & Capital Cycle",
        "Financial Reconstruction & Accounting Quality",
        "Management & Capital Allocation",
        "Impairment Diagnosis & Recovery",
        "Valuation & Market-Implied Expectations",
        "Customer / Product Investigator",
        "Competitor Investigator",
        "Supplier Investigator",
        "Distributor / Channel Investigator",
        "Employee / Organization Investigator",
        "Digital / Social Investigator",
        "Regulatory Investigator",
        "Technology / IP Investigator",
        "Scientific / Clinical Investigator",
        "Geographic Investigator",
        "Industry Specialist",
    }
)

# Registry §3. Configs are checked against this map and cannot replace it.
EXPECTED_ROLE: dict[str, str] = {
    "business_quality_moat": BUSINESS_INDUSTRY,
    "industry_economics_capital_cycle": BUSINESS_INDUSTRY,
    "financial_reconstruction_accounting_quality": FINANCIAL_MANAGEMENT,
    "management_capital_allocation": FINANCIAL_MANAGEMENT,
    "impairment_diagnosis_recovery": IMPAIRMENT,
    "valuation_market_implied_expectations": VALUATION,
    **{specialist_id: ELASTIC for specialist_id in INVESTIGATOR_IDS},
}

EXPECTED_INVESTIGATOR_TYPE: dict[str, str] = {
    "customer_product_investigator": "CUSTOMER",
    "competitor_investigator": "COMPETITOR",
    "supplier_investigator": "SUPPLIER",
    "distributor_channel_investigator": "DISTRIBUTOR",
    "employee_organization_investigator": "EMPLOYEE",
    "digital_social_investigator": "DIGITAL",
    "regulatory_investigator": "REGULATORY",
    "technology_ip_investigator": "TECHNOLOGY",
    "scientific_clinical_investigator": "SCIENTIFIC",
    "geographic_investigator": "GEOGRAPHIC",
    "industry_specialist": "INDUSTRY_SPECIALIST",
    # The industry-economics desk uses the Industry Specialist charter type.
    # The canonical role stays Business & Industry Analyst.
    "industry_economics_capital_cycle": "INDUSTRY_SPECIALIST",
}


class CatalogError(Exception):
    """A specialist config disagrees with the canonical role or name list."""


def _validate(rows: list[dict]) -> dict[str, dict]:
    if len(rows) != len(EXPECTED_DISPLAY_NAMES):
        raise CatalogError(
            f"expected {len(EXPECTED_DISPLAY_NAMES)} configs, found {len(rows)}"
        )
    by_id: dict[str, dict] = {}
    names: list[str] = []
    for row in rows:
        specialist_id = row["specialist_id"]
        if specialist_id in by_id:
            raise CatalogError(f"duplicate specialist_id {specialist_id}")
        if specialist_id not in EXPECTED_ROLE:
            raise CatalogError(f"unknown specialist_id {specialist_id}")
        display = row["display_name"]
        names.append(display)
        if row.get("canonical_role") != EXPECTED_ROLE[specialist_id]:
            raise CatalogError(
                f"{specialist_id} canonical_role {row.get('canonical_role')!r} "
                f"does not match registry role {EXPECTED_ROLE[specialist_id]!r}"
            )
        if row.get("overrides_canonical_authority") is not False:
            raise CatalogError(f"{specialist_id} must not override role authority")
        if row.get("desk_research_only") is not True:
            raise CatalogError(f"{specialist_id} must be desk_research_only")
        expected_type = EXPECTED_INVESTIGATOR_TYPE.get(specialist_id)
        actual_type = row.get("investigator_type")
        if expected_type != actual_type:
            raise CatalogError(
                f"{specialist_id} investigator_type {actual_type!r} "
                f"!= {expected_type!r}"
            )
        forbidden = FORBIDDEN_DESK_CLASSES.intersection(row.get("allowed_source_classes") or [])
        if forbidden:
            raise CatalogError(f"{specialist_id} allows forbidden classes {sorted(forbidden)}")
        by_id[specialist_id] = row
    if set(names) != EXPECTED_DISPLAY_NAMES:
        missing = EXPECTED_DISPLAY_NAMES - set(names)
        extra = set(names) - EXPECTED_DISPLAY_NAMES
        raise CatalogError(f"display names missing={sorted(missing)} extra={sorted(extra)}")
    if set(by_id) != set(EXPECTED_ROLE):
        raise CatalogError("specialist id set does not match the 6+11 map")
    return by_id


@lru_cache(maxsize=1)
def load_catalog() -> dict[str, dict]:
    payload = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return _validate(payload["specialists"])


def get_specialist(specialist_id: str) -> dict:
    catalog = load_catalog()
    try:
        return catalog[specialist_id]
    except KeyError as exc:
        raise CatalogError(specialist_id) from exc
