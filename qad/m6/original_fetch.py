"""Independent HTTP fetch used only as an OriginalSourceVerifier.

The ledger and ``source_bridge`` perform no network I/O. This module is the
verifier those functions call. ``verify_and_admit_source`` mints the trusted
receipt. A caller-built SRC-01 is not a receipt.

Bytes may be reused inside one process after a successful fetch so a replay
loop does not repeat the same download. A new process fetches again. A test
may pass ``opener``; that opener is not a live fetch and is not cached.
"""

from __future__ import annotations

import hashlib
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, timezone

from qad.ids import deterministic_uuid7
from qad.m6.ledger import DeepResearchRunLedgerStore
from qad.m6.source_bridge import (
    DiscoveredSourceReference,
    OriginalSourceVerification,
    SourceFailureKind,
    SourceVerificationCandidate,
    SourceVerificationRequest,
    register_discovered_candidates,
    verify_and_admit_source,
)
from qad.persistence.reference import InMemoryRawSourceArchive
from research.qad_pilot.unh.case_slice import ANCHOR_TS_MS

FETCH_REASON = "independent HTTP fetch by qad.m6.original_fetch"
SEC_USER_AGENT = "FIRO IIP research chamnan.tantiyavuth@gmail.com"
_LIVE = "LIVE_CASE_UPDATE"
_CACHE: dict[str, bytes] = {}


def fetch_url_bytes(
    url: str,
    *,
    user_agent: str = SEC_USER_AGENT,
    timeout: float = 90,
    opener=None,
) -> bytes:
    """Return the response body. ``opener`` is a test seam, not a receipt."""
    if opener is not None:
        raw = opener(url, user_agent, timeout)
        if not isinstance(raw, bytes) or not raw:
            raise ValueError("opener returned no bytes")
        return raw
    cached = _CACHE.get(url)
    if cached is not None:
        return cached
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
    except urllib.error.URLError as exc:
        raise RuntimeError(f"HTTP fetch failed for {url}: {exc}") from exc
    if not raw:
        raise RuntimeError(f"HTTP fetch returned an empty body for {url}")
    _CACHE[url] = raw
    return raw


class HttpOriginalSourceVerifier:
    """Fetch ``request.reference`` and return an untrusted candidate verdict."""

    def __init__(
        self,
        *,
        opener=None,
        source_tier: str = "L1",
        source_type: str = "SEC_FILING",
        title: str | None = None,
        publication_date: str | None = None,
        timeout: float = 90,
    ) -> None:
        self._opener = opener
        self._source_tier = source_tier
        self._source_type = source_type
        self._title = title
        self._publication_date = publication_date
        self._timeout = timeout

    def verify(self, request: SourceVerificationRequest, /) -> SourceVerificationCandidate:
        url = " ".join(str(request.reference or "").split())
        try:
            raw = fetch_url_bytes(url, timeout=self._timeout, opener=self._opener)
        except Exception as exc:
            return SourceVerificationCandidate(
                verified=False,
                reason=f"independent HTTP fetch failed: {exc}",
                failure_kind=SourceFailureKind.NOT_FOUND,
            )
        digest = hashlib.sha256(raw).hexdigest()
        source_id = str(deterministic_uuid7(f"fetched:{url}:{digest}", ts_ms=ANCHOR_TS_MS))
        retrieved = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        return SourceVerificationCandidate(
            verified=True,
            reason=FETCH_REASON,
            source_id=source_id,
            source_tier=self._source_tier,
            source_type=self._source_type,
            content_hash=digest,
            raw_bytes=raw,
            location=url,
            publication_date=self._publication_date,
            retrieval_date=retrieved,
            title=(self._title or url)[:240],
        )


def mint_http_source(
    url: str,
    *,
    opener=None,
    source_tier: str = "L1",
    source_type: str = "SEC_FILING",
    title: str | None = None,
    publication_date: str | None = None,
    timeout: float = 90,
) -> tuple[OriginalSourceVerification | None, str]:
    """Mint a receipt by fetching ``url`` inside ``verify_and_admit_source``.

    The ledger database and the archive used for minting are temporary. The
    returned verdict carries the fetched bytes. The case archive is unchanged
    until ingest admits those bytes.
    """
    verifier = HttpOriginalSourceVerifier(
        opener=opener,
        source_tier=source_tier,
        source_type=source_type,
        title=title,
        publication_date=publication_date,
        timeout=timeout,
    )
    try:
        with tempfile.TemporaryDirectory(prefix="qad-fetch-") as tmp:
            store = DeepResearchRunLedgerStore(f"{tmp}/ledger.sqlite3")
            digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]
            ledger_id = f"L-fetch-{digest}"
            store.create_run(
                ledger_id=ledger_id,
                research_run_id=f"RR-fetch-{digest}",
                rrm_manifest_id="RRM-fetch",
                case_id="CASE-2026-001",
                case_version="v1",
                evidence_gap_id="EG-fetch",
                request_id=f"REQ-fetch-{digest}",
                idempotency_key=f"idem-fetch-{digest}",
                notebook_identity="original-fetch",
                pit_context_id="PITC-fetch",
                pit_mode=_LIVE,
                as_of="2026-10-17",
                input_snapshot_hash="b" * 64,
                provider_surface="original_fetch",
                transport_type="HTTP",
            )
            registered = register_discovered_candidates(
                store,
                ledger_id=ledger_id,
                references=(DiscoveredSourceReference(index=0, reference=url),),
                discovery_timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            )
            outcome = verify_and_admit_source(
                store,
                ledger_id=ledger_id,
                source_candidate_id=registered[0].source_candidate_id,
                verifier=verifier,
                archive=InMemoryRawSourceArchive(),
            )
    except Exception as exc:
        return None, f"S5/M6 source mint failed: {exc}"
    verification = outcome.verification
    if not isinstance(verification, OriginalSourceVerification) or not verification.verified:
        return None, outcome.reason or "S5/M6 source verification did not succeed"
    if verification.reason != FETCH_REASON:
        return None, "S5/M6 receipt was not minted by the independent HTTP fetch"
    return verification, ""
