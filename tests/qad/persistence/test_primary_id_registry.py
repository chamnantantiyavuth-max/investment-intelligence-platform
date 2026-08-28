"""Independent test oracle for the primary-id registry.

Parses the frozen M4A markdown separately from the production code and
verifies that every entry in ``primary_id_registry.json`` matches the
canonical M4A ``IDs / foreign keys`` declarations.

This is an INDEPENDENT oracle — it does NOT import or use
``qad.persistence.reference._schema_identity_field`` or any production
identity-resolution code.  It reads the same M4A source and generates its
own mapping, then cross-checks the production artifact.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

# ── Paths ──────────────────────────────────────────────────────────────────

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_M4A_PATH = (
    _REPO_ROOT
    / "design" / "qad-pivot" / "m4a" / "QAD-M4A-CANONICAL-SCHEMAS.md"
)
_REGISTRY_PATH = (
    _REPO_ROOT / "qad" / "contract" / "primary_id_registry.json"
)


# ── Oracle parser (independent of production code) ─────────────────────────


def _parse_m4a_identities() -> dict[str, str]:
    """Parse the frozen M4A markdown and return ``{schema_id: primary_id_field}``.

    This function is an independent re-implementation — it does NOT call any
    ``qad.persistence`` code, ensuring the test oracle is structurally
    separate from the production identity resolver.
    """
    with open(_M4A_PATH, encoding="utf-8") as f:
        text = f.read()

    result: dict[str, str] = {}

    # Step 1: Primary path — read ``IDs / foreign keys`` line for non-FK declaration
    pattern = re.compile(
        r'\|\s*\*\*schema_id\*\*\s*\|\s*([A-Z]+-\d+)\s*\|\n'
        r'(?:.*\n)*?'
        r'\|\s*\*\*IDs\s*/\s*foreign\s*keys\*\*\s*\|\s*(.*?)\s*\|',
        re.IGNORECASE,
    )

    for m in pattern.finditer(text):
        sid = m.group(1)
        ids_line = m.group(2)

        parts = re.findall(r'`([^`]+)`', ids_line)

        primary = None
        for part in parts:
            if "\u2192" not in part:  # not a FK reference
                field_name = part.split(":")[0].strip()
                primary = field_name
                break

        if primary:
            result[sid] = primary

    # Step 2: FK-only schemas (primary identity is same as FK, e.g. entity_id)
    all_sids = re.findall(
        r'\|\s*\*\*schema_id\*\*\s*\|\s*([A-Z]+-\d+)\s*\|', text
    )
    for sid in all_sids:
        if sid in result:
            continue
        idx = text.find(f"**schema_id** | {sid} |")
        if idx < 0:
            continue
        block_end = text.find("\n---\n", idx)
        if block_end < 0:
            block_end = text.find("\n###", idx) if "\n###" in text[idx:] else idx + 500
        block = text[idx:block_end] if block_end > idx else text[idx : idx + 500]

        req_m = re.search(r"\*\*required_fields\*\*\s*\|\s*`([^`]+)`", block)
        if req_m:
            id_field = req_m.group(1).split(",")[0].strip()
            if id_field.endswith("_id"):
                result[sid] = id_field

    return result


# ── Fixtures ───────────────────────────────────────────────────────────────


@pytest.fixture(scope="module")
def production_registry() -> dict[str, str]:
    with open(_REGISTRY_PATH) as f:
        return json.load(f)["PRIMARY_ID_FIELDS"]


@pytest.fixture(scope="module")
def oracle_registry() -> dict[str, str]:
    return _parse_m4a_identities()


# ── Tests ──────────────────────────────────────────────────────────────────


class TestPrimaryIdRegistryCount:
    """The registry must contain exactly 68 entries — one per M4A schema."""

    def test_production_has_68_schemas(self, production_registry):
        assert len(production_registry) == 68, (
            f"Expected 68 schemas in primary_id_registry.json, "
            f"got {len(production_registry)}"
        )

    def test_oracle_has_68_schemas(self, oracle_registry):
        assert len(oracle_registry) == 68, (
            f"Expected 68 schemas from M4A oracle parser, "
            f"got {len(oracle_registry)}"
        )

    def test_no_extra_schemas(self, production_registry, oracle_registry):
        """Production must not have schemas the M4A doesn't."""
        extra = set(production_registry) - set(oracle_registry)
        assert not extra, (
            f"Production registry has schemas not in M4A: {extra}"
        )

    def test_no_missing_schemas(self, production_registry, oracle_registry):
        """Production must not miss schemas the M4A has."""
        missing = set(oracle_registry) - set(production_registry)
        assert not missing, (
            f"Production registry is missing M4A schemas: {missing}"
        )


class TestPrimaryIdRegistryValues:
    """Every production registry entry must match the M4A oracle exactly."""

    def test_all_identities_match(self, production_registry, oracle_registry):
        mismatches = {}
        for sid, expected_pk in oracle_registry.items():
            actual_pk = production_registry.get(sid)
            if actual_pk != expected_pk:
                mismatches[sid] = (expected_pk, actual_pk)

        assert not mismatches, (
            f"Primary identity mismatches (M4A oracle vs production registry):\n"
            + "\n".join(
                f"  {sid}: M4A says {exp}, registry has {act}"
                for sid, (exp, act) in sorted(mismatches.items())
            )
        )


# ── Known correction verification (regression guard) ───────────────────────


class TestKnownCorrections:
    """The four explicit corrections from FD #135 must be correct."""

    @pytest.mark.parametrize(
        "schema_id, expected_pk",
        [
            ("NFF-01", "normalized_fact_id"),
            ("CALC-01", "calculation_id"),
            ("RM-01", "recovery_id"),
            ("FE-01", "flip_evidence_id"),
        ],
    )
    def test_correction(
        self, schema_id: str, expected_pk: str, production_registry
    ):
        actual = production_registry.get(schema_id)
        assert actual == expected_pk, (
            f"{schema_id}: expected PK={expected_pk!r}, "
            f"got {actual!r}"
        )

# ====================================================================
# Item 11 — Negative tests: wrong/missing PK → FAIL
# ====================================================================


class TestNegativePrimaryIdRejection:
    """Item 11: wrong/missing primary-ID mapping must fail deterministically."""

    def test_wrong_pk_mapping_does_not_store(self, production_registry):
        """Injecting a record with a wrong PK field name fails closed."""
        from qad.persistence.reference import InMemoryCanonicalRecordStore
        from qad.persistence.errors import TransactionFailure
        from pydantic import BaseModel

        class _WrongPkModel(BaseModel):
            schema_id: str = "SM-01"
            wrong_key: str = "val"

        store = InMemoryCanonicalRecordStore()
        with pytest.raises((ValueError, TypeError, TransactionFailure)):
            store.store(_WrongPkModel())

    def test_missing_pk_field_raises(self):
        """An instance with unresolvable schema_id must be rejected."""
        from qad.persistence.reference import InMemoryCanonicalRecordStore
        from qad.persistence.errors import TransactionFailure
        from pydantic import BaseModel

        store = InMemoryCanonicalRecordStore()

        class _UnknownSchemaModel(BaseModel):
            schema_id: str = "UNKNOWN-99"
            data: str = "test"

        with pytest.raises((ValueError, TypeError, TransactionFailure)):
            store.store(_UnknownSchemaModel())
