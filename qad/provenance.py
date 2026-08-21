"""DEPRECATED — NOT USED BY M5.1 GENERATED MODELS.

M5.1 generated models do NOT inherit from these mixins.
PIT and provenance fields are compiled directly into each schema model
from the frozen M4A contract. See qad/models/ for the generated models.

This file is retained for reference only and will be removed when
all consumers are migrated to the generated models.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional


class ProvenanceMixin:
    """DEPRECATED — Not used by M5.1 generated models.
    Provenance fields are now compiled per-schema from frozen M4A."""
    source: str
    retrieval_timestamp: datetime
    data_version: str


class PITMixin:
    """DEPRECATED — Not used by M5.1 generated models.
    PIT fields are now compiled per-schema from frozen M4A."""
    as_of_date: str