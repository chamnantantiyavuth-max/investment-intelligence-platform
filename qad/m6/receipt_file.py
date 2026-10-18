"""Persisted S5/M6 fetch receipts.

A case read loads these files and does not open the network. The files are
written only after ``verify_and_admit_source`` has minted a receipt. A
hand-inserted SRC-01 is not a file of this kind.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

from qad.m6.original_fetch import FETCH_REASON

_KIND = "m6-fetch-receipt"
_HASH = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class PersistedFetchReceipt:
    """Receipt recovered from repo files. Not a newly minted verdict."""

    source_id: str
    content_hash: str
    raw_bytes: bytes
    location: str
    retrieval_date: str
    reason: str
    source_tier: str
    source_type: str
    title: str
    publication_date: str | None


def persist_receipts(receipt_dir: Path, verifications) -> list[Path]:
    """Write one JSON plus the fetched bytes for each minted receipt."""
    written: list[Path] = []
    receipt_dir.mkdir(parents=True, exist_ok=True)
    for verification in verifications or ():
        if getattr(verification, "reason", None) != FETCH_REASON:
            continue
        raw = getattr(verification, "raw_bytes", None)
        digest = str(getattr(verification, "content_hash", "") or "")
        source_id = str(getattr(verification, "source_id", "") or "")
        location = str(getattr(verification, "location", "") or "")
        observed = str(getattr(verification, "retrieval_date", "") or "")
        if not isinstance(raw, bytes) or not raw or not _HASH.fullmatch(digest):
            continue
        if hashlib.sha256(raw).hexdigest() != digest or not source_id or not location or not observed:
            continue
        bytes_name = f"{digest}.bin"
        blob_path = (receipt_dir / bytes_name).resolve()
        blob_path.relative_to(receipt_dir.resolve())
        blob_path.write_bytes(raw)
        payload = {
            "kind": _KIND,
            "reason": FETCH_REASON,
            "source_id": source_id,
            "content_hash": digest,
            "location": location,
            "retrieval_date": observed,
            "publication_date": getattr(verification, "publication_date", None),
            "source_tier": getattr(verification, "source_tier", None),
            "source_type": getattr(verification, "source_type", None),
            "title": getattr(verification, "title", None),
            "bytes_name": bytes_name,
        }
        path = receipt_dir / f"{source_id}.json"
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        _drop_other_locations(receipt_dir, location, source_id)
        written.append(path)
    return written


def _drop_other_locations(receipt_dir: Path, location: str, source_id: str) -> None:
    """Keep one receipt file per URL so a later verify replaces the prior hash."""
    for path in receipt_dir.glob("*.json"):
        if path.stem == source_id:
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(payload, dict) or payload.get("location") != location:
            continue
        bytes_name = str(payload.get("bytes_name") or "")
        path.unlink(missing_ok=True)
        if bytes_name and "/" not in bytes_name and "\\" not in bytes_name:
            blob = receipt_dir / bytes_name
            if blob.is_file():
                blob.unlink()


def load_persisted_receipts(receipt_dir: Path | None) -> list[PersistedFetchReceipt]:
    """Load receipts whose bytes still hash to the recorded sha256.

    A missing directory, a bad file, or a hash mismatch yields nothing for
    that file. It does not fetch.
    """
    if receipt_dir is None or not receipt_dir.is_dir():
        return []
    root = receipt_dir.resolve()
    loaded: list[PersistedFetchReceipt] = []
    for path in sorted(root.glob("*.json")):
        receipt = _load_one(root, path)
        if receipt is not None:
            loaded.append(receipt)
    return loaded


def _load_one(root: Path, path: Path) -> PersistedFetchReceipt | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict) or payload.get("kind") != _KIND:
        return None
    if payload.get("reason") != FETCH_REASON:
        return None
    digest = str(payload.get("content_hash") or "")
    source_id = str(payload.get("source_id") or "").strip()
    location = str(payload.get("location") or "").strip()
    observed = str(payload.get("retrieval_date") or "").strip()
    bytes_name = str(payload.get("bytes_name") or "")
    if not _HASH.fullmatch(digest) or bytes_name != f"{digest}.bin":
        return None
    if not source_id or not location or not observed:
        return None
    blob = (root / bytes_name).resolve()
    try:
        blob.relative_to(root)
    except ValueError:
        return None
    if not blob.is_file():
        return None
    raw = blob.read_bytes()
    if hashlib.sha256(raw).hexdigest() != digest:
        return None
    publication = payload.get("publication_date")
    return PersistedFetchReceipt(
        source_id=source_id,
        content_hash=digest,
        raw_bytes=raw,
        location=location,
        retrieval_date=observed,
        reason=FETCH_REASON,
        source_tier=str(payload.get("source_tier") or "L1"),
        source_type=str(payload.get("source_type") or "SEC_FILING"),
        title=str(payload.get("title") or location)[:240],
        publication_date=str(publication)[:10] if publication else None,
    )
