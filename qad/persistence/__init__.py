"""QAD Persistence Layer — core interfaces and reference adapter.

This package provides the persistence contracts, enforcement rules,
and an in-memory reference implementation for the QAD canonical data
pipeline (M5.1 scope).

Sub-modules
-----------
- ``errors``: Typed persistence exception classes.
- ``interfaces``: ``Protocol`` classes for every store type.
- ``serialization``: Deterministic canonical serialisation and hashing.
- ``fk_enforcer``: FK existence validation from ``FK_REGISTRY``.
- ``immutability``: Immutability policy enforcement from contract descriptor.
- ``transaction``: Atomic ``Transaction`` boundary with validate/commit phases.
- ``reference``: In-memory dict-backed reference implementations (NON-PRODUCTION).

Quick Start
-----------
::

    from qad.persistence.reference import InMemoryCanonicalRecordStore
    from qad.models import SourceRecord

    store = InMemoryCanonicalRecordStore()
    src = SourceRecord(...)
    ch = store.store(src)
    loaded = store.load("SRC-01", src.source_id)
"""

from __future__ import annotations

# -- Public API ---------------------------------------------------------------

# Re-export all error classes
from qad.persistence.errors import (
    CanonicalBoundaryViolation,
    HashMismatch,
    ImmutabilityViolation,
    IntegrityConflict,
    MissingForeignKey,
    NonCanonicalAdmissionRejected,
    PersistenceError,
    TransactionFailure,
    ValidationFailure,
)

# Re-export protocol interfaces
from qad.persistence.interfaces import (
    BlobStore,
    CanonicalRecordStore,
    EvidenceRegistry,
    FinancialFactStore,
    NonCanonicalResearchArtifactStore,
    PITContextStore,
    RawSourceArchive,
    RunManifestStore,
)

# Re-export core enforcement
from qad.persistence.fk_enforcer import validate_fks, validate_fk_structure
from qad.persistence.immutability import (
    check_field_immutable,
    check_immutability,
    get_immutability_rules_text,
    is_record_immutable,
)

# Re-export serialization
from qad.persistence.serialization import (
    canonical_hash_from_bytes,
    compute_canonical_hash,
    deserialize_from_canonical_bytes,
    serialize_to_canonical_bytes,
    serialize_to_canonical_json,
)

# Re-export transaction
from qad.persistence.transaction import Transaction

# Re-export all reference implementations
from qad.persistence.reference import (
    InMemoryBlobStore,
    InMemoryCanonicalRecordStore,
    InMemoryEvidenceRegistry,
    InMemoryFinancialFactStore,
    InMemoryNonCanonicalResearchArtifactStore,
    InMemoryPITContextStore,
    InMemoryRawSourceArchive,
    InMemoryRunManifestStore,
)

__all__ = [
    # -- Errors --
    "CanonicalBoundaryViolation",
    "HashMismatch",
    "ImmutabilityViolation",
    "IntegrityConflict",
    "MissingForeignKey",
    "NonCanonicalAdmissionRejected",
    "PersistenceError",
    "TransactionFailure",
    "ValidationFailure",
    # -- Interfaces --
    "BlobStore",
    "CanonicalRecordStore",
    "EvidenceRegistry",
    "FinancialFactStore",
    "NonCanonicalResearchArtifactStore",
    "PITContextStore",
    "RawSourceArchive",
    "RunManifestStore",
    # -- FK --",
    "validate_fks",
    "validate_fk_structure",
    # -- Immutability --
    "check_field_immutable",
    "check_immutability",
    "get_immutability_rules_text",
    "is_record_immutable",
    # -- Serialization --
    "canonical_hash_from_bytes",
    "compute_canonical_hash",
    "deserialize_from_canonical_bytes",
    "serialize_to_canonical_bytes",
    "serialize_to_canonical_json",
    # -- Transaction --
    "Transaction",
    # -- Reference implementations --
    "InMemoryBlobStore",
    "InMemoryCanonicalRecordStore",
    "InMemoryEvidenceRegistry",
    "InMemoryFinancialFactStore",
    "InMemoryNonCanonicalResearchArtifactStore",
    "InMemoryPITContextStore",
    "InMemoryRawSourceArchive",
    "InMemoryRunManifestStore",
]