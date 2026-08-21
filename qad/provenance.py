"""M5.1 — Provenance and PIT metadata mixins for frozen QAD schemas.

Every runtime schema inherits these to ensure complete provenance tracking
and Point-in-Time enforcement metadata per M4A contract.
"""

from datetime import datetime
from typing import Optional


class ProvenanceMixin:
    """Provenance metadata — every canonical schema must carry these.

    Frozen per M4A provenance fields contract. Individual schemas may add
    additional provenance fields beyond this base set.
    """

    source: str  # origin (e.g. "sec-edgar", "yfinance", "manual-entry")
    retrieval_timestamp: datetime  # when retrieved/created
    data_version: str  # source version identifier

    class Config:
        extra = "forbid"


class PITMixin:
    """Point-in-Time metadata — every schema with PIT enforcement.

    Frozen per M4A PIT fields contract.
    """

    as_of_date: str  # ISO date string; PIT boundary this record is valid within

    class Config:
        extra = "forbid"