"""Typed persistence errors for the QAD persistence layer.

Every persistence operation uses typed, catchable exception classes
so callers can handle specific failure modes without string matching.
"""

from __future__ import annotations


class PersistenceError(Exception):
    """Base class for all persistence-layer errors."""

    def __init__(self, message: str, *, schema_id: str | None = None,
                 record_id: str | None = None):
        self.schema_id = schema_id
        self.record_id = record_id
        super().__init__(message)


class ValidationFailure(PersistenceError):
    """Raised when a schema instance fails contract validation."""

    def __init__(self, message: str, *, schema_id: str | None = None,
                 record_id: str | None = None, violations: list[str] | None = None):
        self.violations = violations or []
        super().__init__(message, schema_id=schema_id, record_id=record_id)


class CanonicalBoundaryViolation(PersistenceError):
    """Raised when a non-canonical schema is written to a canonical store."""

    def __init__(self, message: str, *, schema_id: str | None = None,
                 record_id: str | None = None):
        super().__init__(message, schema_id=schema_id, record_id=record_id)


class IntegrityConflict(PersistenceError):
    """Raised when the same record ID exists with a different payload.

    Same ID + same payload is a safe, idempotent no-op.
    Same ID + different payload is an integrity violation.
    """

    def __init__(self, message: str, *, schema_id: str | None = None,
                 record_id: str | None = None, existing_hash: str | None = None,
                 incoming_hash: str | None = None):
        self.existing_hash = existing_hash
        self.incoming_hash = incoming_hash
        super().__init__(message, schema_id=schema_id, record_id=record_id)


class MissingForeignKey(PersistenceError):
    """Raised when a foreign-key reference cannot be resolved.

    The 'field' attribute identifies which FK field failed and 'target_ids'
    lists the specific IDs that were not found in the target store.
    """

    def __init__(self, message: str, *, schema_id: str | None = None,
                 record_id: str | None = None, field: str | None = None,
                 target_schema: str | None = None,
                 target_ids: list[str] | None = None):
        self.field = field
        self.target_schema = target_schema
        self.target_ids = target_ids or []
        super().__init__(message, schema_id=schema_id, record_id=record_id)


class ImmutabilityViolation(PersistenceError):
    """Raised when an update attempts to modify an immutable record or field."""

    def __init__(self, message: str, *, schema_id: str | None = None,
                 record_id: str | None = None,
                 violated_fields: list[str] | None = None):
        self.violated_fields = violated_fields or []
        super().__init__(message, schema_id=schema_id, record_id=record_id)


class HashMismatch(PersistenceError):
    """Raised when a content-addressed blob's hash does not match its key."""

    def __init__(self, message: str, *, schema_id: str | None = None,
                 record_id: str | None = None,
                 expected_hash: str | None = None,
                 actual_hash: str | None = None):
        self.expected_hash = expected_hash
        self.actual_hash = actual_hash
        super().__init__(message, schema_id=schema_id, record_id=record_id)


class TransactionFailure(PersistenceError):
    """Raised when a batch transaction fails before commit.

    Carries the list of individual errors that caused the rollback.
    Guarantees: ZERO records were committed.
    """

    def __init__(self, message: str, *, errors: list[PersistenceError] | None = None,
                 phase: str | None = None):
        self.errors = errors or []
        self.phase = phase  # 'validate' or 'commit'
        super().__init__(message)


class NonCanonicalAdmissionRejected(PersistenceError):
    """Raised by RawSourceArchive when non-canonical content is submitted.

    The raw source archive requires an explicit admission workflow for
    content that has not yet passed the canonical boundary check.
    """

    def __init__(self, message: str, *, schema_id: str | None = None,
                 record_id: str | None = None):
        super().__init__(message, schema_id=schema_id, record_id=record_id)