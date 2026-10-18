"""Content-normalized hash for cross-retrieval agreement.

SEC EDGAR HTML embeds a per-request token in a trailing ``<script>`` element.
Two fetches of the same filing can therefore have different raw sha256 values
while the document bytes are otherwise identical.

``content_hash`` on a receipt stays ``sha256`` of the stored bytes. That pin
is the provenance of the ``.bin`` file. This module's normalized hash is used
only to decide whether two independent fetches agree.

Normalization removes well-formed ``<script>...</script>`` elements and
nothing else:

- the tag name match is case-insensitive and includes attributes up to the
  first ``>``;
- the element body is taken non-greedy through the matching end tag;
- every other byte is kept, including comments, ``<style>``, and text;
- an unclosed ``<script>`` is not an element and is left unchanged, so a
  missing end tag cannot swallow the rest of the document.

The passage check uses the same stripped bytes. A quotation that occurs only
inside a script element does not count.
"""

from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass
from pathlib import Path

_SCRIPT_ELEMENT = re.compile(rb"(?is)<script\b[^>]*>.*?</script\s*>")
_HASH = re.compile(r"^[0-9a-f]{64}$")
_NOTE_TOKEN = re.compile(
    r"\b(normalized_sha256|evidence_lead_raw_sha256|"
    r"evidence_lead_normalized_sha256|passage_sha256)=([0-9a-f]{64})\b"
)
_NOTE_AGREEMENT = re.compile(r"\bagreement=(normalized|mismatch|passage-level)\b")

NORMALIZED_HASH_RULE = (
    "content_hash is sha256 of the stored bytes. "
    "normalized_sha256 removes well-formed <script>...</script> elements and "
    "nothing else, then sha256. It is used only for cross-retrieval agreement."
)

# Local B2.2 attachment directory. A file is accepted only when its raw sha256
# equals the claim's expected_sha256. A missing directory is not an error.
_ATTACHMENT_DIR = Path("/home/ubuntu/.cursor/projects/workspace/uploads")
_MAX_CROSS_CHECK_BYTES = 8 * 1024 * 1024


@dataclass(frozen=True)
class CrossRetrievalAgreement:
    """Result of comparing a receipt to an Evidence-Lead fetch."""

    status: str
    detail: str
    notes: str
    raw_sha256: str
    normalized_sha256: str
    evidence_lead_raw_sha256: str
    evidence_lead_normalized_sha256: str
    passage_sha256: str


def strip_script_elements(raw: bytes) -> bytes:
    """Return ``raw`` with well-formed script elements removed."""
    if not isinstance(raw, bytes):
        raise TypeError("script stripping requires bytes")
    return _SCRIPT_ELEMENT.sub(b"", raw)


def content_normalized_sha256(raw: bytes) -> str:
    """sha256 of ``raw`` after script elements are removed."""
    return hashlib.sha256(strip_script_elements(raw)).hexdigest()


def parse_receipt_notes(notes: str) -> dict[str, str]:
    """Read hash tokens written by :func:`format_receipt_notes`.

    Prose in the notes is ignored. Only ``key=<64 hex>`` tokens and the
    ``agreement=`` marker are returned.
    """
    found: dict[str, str] = {}
    if not isinstance(notes, str) or not notes:
        return found
    for name, value in _NOTE_TOKEN.findall(notes):
        found[name] = value
    marker = _NOTE_AGREEMENT.search(notes)
    if marker:
        found["agreement"] = marker.group(1)
    return found


def format_receipt_notes(agreement: CrossRetrievalAgreement) -> str:
    """One notes string carrying the raw pin, the normalized hash, and the agreement."""
    parts = [
        NORMALIZED_HASH_RULE,
        f"normalized_sha256={agreement.normalized_sha256}",
    ]
    if agreement.evidence_lead_raw_sha256:
        parts.append(f"evidence_lead_raw_sha256={agreement.evidence_lead_raw_sha256}")
    if agreement.evidence_lead_normalized_sha256:
        parts.append(
            f"evidence_lead_normalized_sha256={agreement.evidence_lead_normalized_sha256}"
        )
    if agreement.passage_sha256:
        parts.append(f"passage_sha256={agreement.passage_sha256}")
    if agreement.status in {"normalized", "mismatch", "passage-level"}:
        parts.append(f"agreement={agreement.status}")
    if agreement.detail:
        parts.append(agreement.detail)
    return " ".join(parts)


def default_cross_check_paths() -> list[Path]:
    """Optional local files that may hold an Evidence-Lead fetch.

    ``QAD_EVIDENCE_LEAD_FILE`` points at one file. The B2.2 attachment
    directory is scanned when it exists. Callers still accept a file only
    when its raw sha256 equals the expected digest.
    """
    paths: list[Path] = []
    env = os.environ.get("QAD_EVIDENCE_LEAD_FILE")
    if env:
        paths.append(Path(env))
    if _ATTACHMENT_DIR.is_dir():
        paths.extend(sorted(_ATTACHMENT_DIR.glob("*.htm")))
        paths.extend(sorted(_ATTACHMENT_DIR.glob("*.html")))
    return paths


def load_cross_check_bytes(expected_raw_sha256: str, paths: list[Path]) -> bytes | None:
    """Return the first file whose raw sha256 equals ``expected_raw_sha256``."""
    if not _HASH.fullmatch(expected_raw_sha256 or ""):
        return None
    seen: set[Path] = set()
    for path in paths:
        try:
            resolved = path.resolve()
        except OSError:
            continue
        if resolved in seen or not resolved.is_file():
            continue
        seen.add(resolved)
        try:
            if resolved.stat().st_size > _MAX_CROSS_CHECK_BYTES:
                continue
            raw = resolved.read_bytes()
        except OSError:
            continue
        if hashlib.sha256(raw).hexdigest() == expected_raw_sha256:
            return raw
    return None


def judge_cross_retrieval(
    raw: bytes,
    *,
    expected_raw_sha256: str,
    quotation: str,
    lead_bytes: bytes | None,
    notes: str,
    looked_for_lead: bool,
) -> CrossRetrievalAgreement:
    """Decide whether this receipt agrees with the Evidence-Lead fetch.

    No ``expected_raw_sha256`` means the claim did not ask for a cross-check.
    When it did:

    - lead bytes whose raw sha256 equals the expected digest are compared by
      normalized hash;
    - a receipt note recorded at that comparison is reused when the lead file
      is not loaded (a case read does not fetch and does not need the file);
    - if the lead bytes were sought and are absent, and no note records an
      earlier comparison, the passage-level sha256 of the quotation is the
      comparison and the detail says so.
    """
    ours_raw = hashlib.sha256(raw).hexdigest() if isinstance(raw, bytes) else ""
    ours_norm = content_normalized_sha256(raw) if isinstance(raw, bytes) else ""
    passage = ""
    if isinstance(quotation, str) and quotation.strip():
        passage = hashlib.sha256(quotation.encode("utf-8")).hexdigest()
    expected = (expected_raw_sha256 or "").strip()

    def _build(
        status: str,
        detail: str,
        *,
        lead_raw: str = "",
        lead_norm: str = "",
    ) -> CrossRetrievalAgreement:
        agreement = CrossRetrievalAgreement(
            status=status,
            detail=detail,
            notes="",
            raw_sha256=ours_raw,
            normalized_sha256=ours_norm,
            evidence_lead_raw_sha256=lead_raw,
            evidence_lead_normalized_sha256=lead_norm,
            passage_sha256=passage,
        )
        return CrossRetrievalAgreement(
            status=agreement.status,
            detail=agreement.detail,
            notes=format_receipt_notes(agreement),
            raw_sha256=agreement.raw_sha256,
            normalized_sha256=agreement.normalized_sha256,
            evidence_lead_raw_sha256=agreement.evidence_lead_raw_sha256,
            evidence_lead_normalized_sha256=agreement.evidence_lead_normalized_sha256,
            passage_sha256=agreement.passage_sha256,
        )

    if not expected:
        return _build("not-required", "")
    if not _HASH.fullmatch(expected):
        return _build(
            "mismatch",
            "expected_sha256 is not a 64-character sha256 hex digest",
        )
    if isinstance(lead_bytes, bytes) and lead_bytes:
        lead_raw = hashlib.sha256(lead_bytes).hexdigest()
        if lead_raw == expected:
            lead_norm = content_normalized_sha256(lead_bytes)
            if ours_norm == lead_norm:
                return _build(
                    "normalized",
                    (
                        f"Cross-retrieval agreement is content-normalized sha256 {ours_norm}. "
                        f"Receipt raw sha256 {ours_raw}. "
                        f"Evidence-Lead raw sha256 {expected}. "
                        f"Evidence-Lead normalized sha256 {lead_norm}. "
                        "Normalization removes well-formed <script>...</script> elements only."
                    ),
                    lead_raw=expected,
                    lead_norm=lead_norm,
                )
            return _build(
                "mismatch",
                (
                    f"normalized sha256 {ours_norm} != evidence-lead normalized sha256 {lead_norm}; "
                    f"raw sha256 {ours_raw} != expected {expected}"
                ),
                lead_raw=expected,
                lead_norm=lead_norm,
            )
    recorded = parse_receipt_notes(notes)
    recorded_agreement = recorded.get("agreement")
    if recorded_agreement == "normalized":
        lead_norm = recorded.get("evidence_lead_normalized_sha256", "")
        if (
            recorded.get("normalized_sha256") == ours_norm
            and lead_norm == ours_norm
            and recorded.get("evidence_lead_raw_sha256") == expected
        ):
            return _build(
                "normalized",
                (
                    f"Cross-retrieval agreement is content-normalized sha256 {ours_norm}. "
                    f"Receipt raw sha256 {ours_raw}. "
                    f"Evidence-Lead raw sha256 {expected}. "
                    f"Evidence-Lead normalized sha256 {lead_norm}. "
                    "Normalization removes well-formed <script>...</script> elements only."
                ),
                lead_raw=expected,
                lead_norm=lead_norm,
            )
        return _build(
            "mismatch",
            (
                "recorded normalized agreement does not match the stored bytes "
                f"(receipt normalized sha256 {ours_norm}; "
                f"recorded evidence-lead normalized sha256 {lead_norm or 'absent'})"
            ),
            lead_raw=recorded.get("evidence_lead_raw_sha256", ""),
            lead_norm=lead_norm,
        )
    if recorded_agreement == "mismatch":
        lead_norm = recorded.get("evidence_lead_normalized_sha256", "")
        return _build(
            "mismatch",
            (
                f"normalized sha256 {ours_norm} != evidence-lead normalized sha256 "
                f"{lead_norm or 'absent'}; raw sha256 {ours_raw} != expected {expected}"
            ),
            lead_raw=recorded.get("evidence_lead_raw_sha256", expected),
            lead_norm=lead_norm,
        )
    if (
        recorded_agreement == "passage-level"
        and recorded.get("passage_sha256") == passage
        and recorded.get("evidence_lead_raw_sha256") == expected
        and passage
    ):
        return _build(
            "passage-level",
            (
                f"Evidence-Lead original bytes for raw sha256 {expected} were not available; "
                f"compared passage-level sha256 {passage} instead of a content-normalized document hash. "
                f"Receipt raw sha256 {ours_raw}. Receipt normalized sha256 {ours_norm}."
            ),
            lead_raw=expected,
        )
    if looked_for_lead:
        return _build(
            "passage-level",
            (
                f"Evidence-Lead original bytes for raw sha256 {expected} were not available; "
                f"compared passage-level sha256 {passage} instead of a content-normalized document hash. "
                f"Receipt raw sha256 {ours_raw}. Receipt normalized sha256 {ours_norm}."
            ),
            lead_raw=expected,
        )
    return _build(
        "mismatch",
        (
            "normalized-hash agreement was not recorded on the receipt and the "
            f"Evidence-Lead bytes for raw sha256 {expected} were not loaded; "
            f"passage-level sha256 {passage or 'absent'}"
        ),
        lead_raw=expected,
    )
