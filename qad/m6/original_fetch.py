"""Independent HTTP fetch used only as an OriginalSourceVerifier.

The ledger and ``source_bridge`` perform no network I/O. This module is the
verifier those functions call. ``verify_and_admit_source`` mints the trusted
receipt. A caller-built SRC-01 is not a receipt.

A case or report read does not call this module. Fetching runs only when an
ingest command passes ``fetch_sources``. Bytes may be reused inside one
process after a successful live fetch. A test may pass ``opener``; that
opener is not a live fetch, is not cached, and still has to pass the URL
policy for scheme, credentials, and literal blocked addresses.
"""

from __future__ import annotations

import hashlib
import ipaddress
import socket
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse

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
MAX_RESPONSE_BYTES = 8 * 1024 * 1024
MAX_TIMEOUT_SECONDS = 120.0
MAX_REDIRECTS = 5
_CGNAT = ipaddress.ip_network("100.64.0.0/10")
_BLOCKED_HOSTS = frozenset({"localhost", "localhost.localdomain"})


class OutboundUrlRejected(ValueError):
    """The URL is outside the independent fetcher's outbound policy."""


def _address_blocked(text: str) -> bool:
    candidate = str(text or "").split("%", 1)[0].strip()
    if not candidate:
        return False
    try:
        parsed = ipaddress.ip_address(candidate)
    except ValueError:
        return False
    if isinstance(parsed, ipaddress.IPv6Address) and parsed.ipv4_mapped is not None:
        parsed = parsed.ipv4_mapped
    if (
        parsed.is_private
        or parsed.is_loopback
        or parsed.is_link_local
        or parsed.is_multicast
        or parsed.is_reserved
        or parsed.is_unspecified
    ):
        return True
    return isinstance(parsed, ipaddress.IPv4Address) and parsed in _CGNAT


def _dns_resolver(host: str, port: int):
    return socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)


def validate_outbound_url(
    url: str,
    *,
    resolver=None,
    hop: int = 0,
    resolve: bool = True,
) -> str:
    """Reject non-https, credentials, and blocked addresses.

    When ``resolve`` is true, every address returned for the host is checked.
    One blocked address rejects the URL. Redirect callers pass ``hop``.
    """
    if hop > MAX_REDIRECTS:
        raise OutboundUrlRejected("redirect hop cap exceeded")
    parsed = urlparse(" ".join(str(url or "").split()))
    if parsed.scheme != "https":
        raise OutboundUrlRejected("only https URLs are fetched")
    if parsed.username is not None or parsed.password is not None:
        raise OutboundUrlRejected("credentials in the URL are blocked")
    host = parsed.hostname
    if not host:
        raise OutboundUrlRejected("URL has no host")
    if host.lower().rstrip(".") in _BLOCKED_HOSTS:
        raise OutboundUrlRejected("localhost is blocked")
    if _address_blocked(host):
        raise OutboundUrlRejected(f"blocked address {host}")
    if not resolve:
        return url
    port = parsed.port or 443
    lookup = resolver or _dns_resolver
    try:
        infos = lookup(host, port)
    except socket.gaierror as exc:
        raise OutboundUrlRejected(f"DNS resolution failed for {host}") from exc
    if not infos:
        raise OutboundUrlRejected(f"DNS resolution returned no addresses for {host}")
    for info in infos:
        sockaddr = info[4]
        address = sockaddr[0] if sockaddr else ""
        if _address_blocked(address):
            raise OutboundUrlRejected(f"blocked resolved address {address}")
    return url


def _bounded_timeout(timeout: float) -> float:
    try:
        value = float(timeout)
    except (TypeError, ValueError) as exc:
        raise OutboundUrlRejected("timeout is not a number") from exc
    if value <= 0:
        raise OutboundUrlRejected("timeout must be positive")
    return min(value, MAX_TIMEOUT_SECONDS)


def _read_capped(response) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while True:
        block = response.read(64 * 1024)
        if not block:
            break
        total += len(block)
        if total > MAX_RESPONSE_BYTES:
            raise RuntimeError(f"response exceeds {MAX_RESPONSE_BYTES} bytes")
        chunks.append(block)
    raw = b"".join(chunks)
    if not raw:
        raise RuntimeError("HTTP fetch returned an empty body")
    return raw


def next_https_hop(current: str, location: str) -> str:
    """Join a redirect and reject a scheme other than https."""
    nxt = urljoin(current, location)
    if urlparse(nxt).scheme != "https":
        raise OutboundUrlRejected("scheme downgrade is blocked")
    parsed = urlparse(nxt)
    if parsed.username is not None or parsed.password is not None:
        raise OutboundUrlRejected("credentials in the URL are blocked")
    return nxt


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _live_fetch(url: str, *, user_agent: str, timeout: float, resolver) -> bytes:
    current = url
    opener = urllib.request.build_opener(_NoRedirect)
    for hop in range(MAX_REDIRECTS + 1):
        validate_outbound_url(current, resolver=resolver, hop=hop, resolve=True)
        request = urllib.request.Request(
            current,
            headers={
                "User-Agent": user_agent,
                "Accept": "text/html,application/xhtml+xml",
            },
        )
        try:
            with opener.open(request, timeout=timeout) as response:
                return _read_capped(response)
        except urllib.error.HTTPError as exc:
            if exc.code not in {301, 302, 303, 307, 308}:
                raise RuntimeError(f"HTTP fetch failed for {url}: {exc}") from exc
            location = exc.headers.get("Location") if exc.headers else None
            if not location:
                raise RuntimeError(f"redirect from {current} had no Location") from exc
            current = next_https_hop(current, location)
        except urllib.error.URLError as exc:
            raise RuntimeError(f"HTTP fetch failed for {url}: {exc}") from exc
    raise OutboundUrlRejected("redirect hop cap exceeded")


def fetch_url_bytes(
    url: str,
    *,
    user_agent: str = SEC_USER_AGENT,
    timeout: float = 90,
    opener=None,
    resolver=None,
) -> bytes:
    """Return the response body. ``opener`` is a test seam, not a receipt."""
    bounded = _bounded_timeout(timeout)
    if opener is not None:
        validate_outbound_url(url, resolver=resolver, resolve=False)
        raw = opener(url, user_agent, bounded)
        if not isinstance(raw, bytes) or not raw:
            raise ValueError("opener returned no bytes")
        if len(raw) > MAX_RESPONSE_BYTES:
            raise RuntimeError(f"response exceeds {MAX_RESPONSE_BYTES} bytes")
        return raw
    cached = _CACHE.get(url)
    if cached is not None:
        return cached
    raw = _live_fetch(url, user_agent=user_agent, timeout=bounded, resolver=resolver)
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
