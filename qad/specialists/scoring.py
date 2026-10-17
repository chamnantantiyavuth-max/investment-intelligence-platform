"""Deterministic gap scoring from the canonical EIV bands.

QAD-MODERN-SCUTTLEBUTT-PROTOCOL.md §6 defines Expected Information Value as
a qualitative band, not a quantified score:

- PLAUSIBLE_HIGH: likely to resolve a critical question that changes the
  case outcome. Budget priority high.
- PLAUSIBLE_MEDIUM: useful context, unlikely to change the outcome.
- PLAUSIBLE_LOW: not material; may be deferred.

No canonical numeric EIV formula exists. The mapping below uses only the
stored gap fields (importance, resolvability_class, question text) and the
§6 band meanings. It is not a new investment selection policy. Founder
priority, when supplied, is an explicit override recorded beside this rank.
It does not rewrite the band.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

EIV_RANK = {"PLAUSIBLE_HIGH": 3, "PLAUSIBLE_MEDIUM": 2, "PLAUSIBLE_LOW": 1}
IMPORTANCE_RANK = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}

# Words that mark an H1-versus-H2 outcome question in stored gap text.
# They are routing labels for text that already exists, not new hypotheses.
_OUTCOME_MARKERS = (
    "mechanism",
    "temporary",
    "structural",
    "outlook",
    "membership",
    "moat",
    "impairment",
    "recovery",
    "valuation",
    "market share",
)

# First match wins. Order keeps a specific dimension ahead of generic
# financial words such as "margin".
_CLASSIFIER: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("management_capital_allocation", ("outlook", "buyback", "dividend", "capital allocation")),
    ("customer_product_investigator", ("membership", "customer", "churn")),
    ("competitor_investigator", ("competitor", "market share")),
    (
        "industry_economics_capital_cycle",
        ("capital cycle", "industry structure", "rate bridge"),
    ),
    ("supplier_investigator", ("supplier", "input cost")),
    ("distributor_channel_investigator", ("distributor", "sell-through", "destocking")),
    ("employee_organization_investigator", ("talent", "glassdoor", "employee")),
    ("digital_social_investigator", ("web traffic", "app ranking", "social sentiment")),
    ("regulatory_investigator", ("regulatory", "regulation")),
    ("technology_ip_investigator", ("patent", "r&d pipeline")),
    ("scientific_clinical_investigator", ("clinical trial",)),
    ("geographic_investigator", ("geographic", "regional")),
    ("business_quality_moat", ("moat", "switching cost")),
    ("impairment_diagnosis_recovery", ("impairment diagnosis", "recovery model")),
    ("valuation_market_implied_expectations", ("reverse dcf", "valuation")),
    (
        "financial_reconstruction_accounting_quality",
        ("10-q", "10-k", "reserve", "xbrl", "companyfacts", "earnings", "margin", "skeptic"),
    ),
)

_ROUTABLE_STATUS = {"OPEN", "IN_PROGRESS", "UNRESOLVED"}


def _enum(value: object) -> str:
    return getattr(value, "value", value)  # type: ignore[return-value]


def _contains(text: str, phrase: str) -> bool:
    return re.search(rf"\b{re.escape(phrase)}\b", text) is not None


def classify_question(text: str) -> str | None:
    lowered = text.lower()
    for specialist_id, phrases in _CLASSIFIER:
        if any(_contains(lowered, phrase) for phrase in phrases):
            return specialist_id
    return None


def assign_eiv(importance: str, resolvability_class: str, text: str) -> str:
    """Map one gap onto the §6 band. CURRENTLY_UNRESOLVABLE is deferred."""
    if resolvability_class == "CURRENTLY_UNRESOLVABLE":
        return "PLAUSIBLE_LOW"
    outcome = any(_contains(text.lower(), marker) for marker in _OUTCOME_MARKERS)
    if importance == "CRITICAL" and outcome:
        return "PLAUSIBLE_HIGH"
    if importance == "CRITICAL":
        return "PLAUSIBLE_MEDIUM"
    if importance == "HIGH" and outcome:
        return "PLAUSIBLE_HIGH"
    if importance == "HIGH":
        return "PLAUSIBLE_MEDIUM"
    if importance == "MEDIUM" and outcome:
        return "PLAUSIBLE_MEDIUM"
    return "PLAUSIBLE_LOW"


@dataclass(frozen=True)
class RankedGap:
    gap_id: str
    specialist_id: str | None
    eiv: str
    importance: str
    resolvability_class: str
    question: str
    falsifiable_question: str
    operational_status: str

    @property
    def sort_key(self) -> tuple:
        return (
            -EIV_RANK[self.eiv],
            -IMPORTANCE_RANK.get(self.importance, 0),
            self.gap_id,
        )


def rank_gaps(gaps: list) -> list[RankedGap]:
    """Rank routable gaps. Closed and deferred gaps are omitted."""
    ranked: list[RankedGap] = []
    for gap in gaps:
        status = _enum(gap.operational_status)
        if status not in _ROUTABLE_STATUS:
            continue
        question = gap.question or ""
        falsifiable = gap.falsifiable_question or ""
        text = f"{question} {falsifiable}"
        importance = _enum(gap.importance)
        resolvability = _enum(gap.resolvability_class)
        ranked.append(
            RankedGap(
                gap_id=gap.gap_id,
                specialist_id=classify_question(text),
                eiv=assign_eiv(importance, resolvability, text),
                importance=importance,
                resolvability_class=resolvability,
                question=question,
                falsifiable_question=falsifiable,
                operational_status=status,
            )
        )
    ranked.sort(key=lambda item: item.sort_key)
    return ranked


def natural_selection(ranked: list[RankedGap], max_n: int) -> list[RankedGap]:
    """One gap per dimension, in EIV order. Unclassified gaps are not selected."""
    chosen: list[RankedGap] = []
    seen: set[str] = set()
    for item in ranked:
        if not item.specialist_id or item.specialist_id in seen:
            continue
        chosen.append(item)
        seen.add(item.specialist_id)
        if len(chosen) >= max_n:
            break
    return chosen
