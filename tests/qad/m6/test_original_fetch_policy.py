"""Outbound URL policy for the independent source fetcher. No live network."""

from __future__ import annotations

import hashlib
import json

import pytest

from qad.m6.original_fetch import (
    MAX_REDIRECTS,
    MAX_RESPONSE_BYTES,
    MAX_TIMEOUT_SECONDS,
    OutboundUrlRejected,
    fetch_url_bytes,
    next_https_hop,
    validate_outbound_url,
)
from qad.m6.receipt_file import load_persisted_receipts, persist_receipts


def _public(host, port):
    return [(socket_family(), socket_type(), 0, "", ("8.8.8.8", port))]


def socket_family():
    import socket

    return socket.AF_INET


def socket_type():
    import socket

    return socket.SOCK_STREAM


def _resolves(address):
    def resolver(host, port):
        return [(socket_family(), socket_type(), 0, "", (address, port))]

    return resolver


def test_http_and_credentials_and_missing_host_are_rejected():
    with pytest.raises(OutboundUrlRejected, match="https"):
        validate_outbound_url("http://example.com/a", resolver=_public, resolve=True)
    with pytest.raises(OutboundUrlRejected, match="credentials"):
        validate_outbound_url("https://user:pass@example.com/a", resolver=_public, resolve=False)
    with pytest.raises(OutboundUrlRejected, match="host"):
        validate_outbound_url("https:///no-host", resolver=_public, resolve=False)


def test_localhost_and_literal_blocked_addresses_are_rejected_without_dns():
    blocked = [
        "https://localhost/x",
        "https://127.0.0.1/x",
        "https://10.1.2.3/x",
        "https://192.168.1.9/x",
        "https://172.16.0.4/x",
        "https://169.254.1.1/x",
        "https://100.64.1.1/x",
        "https://224.0.0.1/x",
        "https://240.0.0.1/x",
        "https://0.0.0.0/x",
        "https://[::1]/x",
        "https://[fc00::1]/x",
        "https://[fe80::1]/x",
        "https://[ff02::1]/x",
        "https://[::ffff:127.0.0.1]/x",
    ]
    for url in blocked:
        with pytest.raises(OutboundUrlRejected):
            validate_outbound_url(url, resolver=_public, resolve=False)


def test_dns_answers_are_checked_and_one_blocked_address_rejects():
    with pytest.raises(OutboundUrlRejected, match="resolved"):
        validate_outbound_url(
            "https://example.com/filing",
            resolver=_resolves("10.0.0.8"),
            resolve=True,
        )
    with pytest.raises(OutboundUrlRejected, match="resolved"):
        validate_outbound_url(
            "https://example.com/filing",
            resolver=_resolves("100.64.0.8"),
            resolve=True,
        )
    with pytest.raises(OutboundUrlRejected, match="resolved"):
        validate_outbound_url(
            "https://example.com/filing",
            resolver=_resolves("fd00::1"),
            resolve=True,
        )

    def mixed(host, port):
        return [
            (socket_family(), socket_type(), 0, "", ("8.8.8.8", port)),
            (socket_family(), socket_type(), 0, "", ("127.0.0.1", port)),
        ]

    with pytest.raises(OutboundUrlRejected, match="resolved"):
        validate_outbound_url("https://example.com/filing", resolver=mixed, resolve=True)
    assert validate_outbound_url(
        "https://example.com/filing", resolver=_public, resolve=True
    ).startswith("https://")


def test_dns_failure_and_hop_cap_fail_closed():
    def broken(host, port):
        import socket

        raise socket.gaierror("no such host")

    with pytest.raises(OutboundUrlRejected, match="DNS"):
        validate_outbound_url("https://example.com/x", resolver=broken, resolve=True)

    def empty(host, port):
        return []

    with pytest.raises(OutboundUrlRejected, match="no addresses"):
        validate_outbound_url("https://example.com/x", resolver=empty, resolve=True)
    with pytest.raises(OutboundUrlRejected, match="hop cap"):
        validate_outbound_url(
            "https://example.com/x",
            resolver=_public,
            hop=MAX_REDIRECTS + 1,
            resolve=True,
        )


def test_scheme_downgrade_and_credentialed_redirect_are_blocked():
    with pytest.raises(OutboundUrlRejected, match="scheme downgrade"):
        next_https_hop("https://example.com/a", "http://example.com/a")
    with pytest.raises(OutboundUrlRejected, match="credentials"):
        next_https_hop("https://example.com/a", "https://user:secret@example.com/a")
    assert next_https_hop("https://example.com/a", "https://example.com/b") == "https://example.com/b"


def test_opener_still_enforces_policy_size_and_timeout_cap():
    seen = {}

    def opener(url, user_agent, timeout):
        seen["timeout"] = timeout
        seen["url"] = url
        return b"ok"

    with pytest.raises(OutboundUrlRejected):
        fetch_url_bytes("http://example.com/a", opener=opener)
    assert "url" not in seen
    with pytest.raises(OutboundUrlRejected):
        fetch_url_bytes("https://127.0.0.1/a", opener=opener)
    with pytest.raises(OutboundUrlRejected, match="positive"):
        fetch_url_bytes("https://example.com/a", timeout=0, opener=opener)
    assert fetch_url_bytes("https://example.com/a", timeout=9999, opener=opener) == b"ok"
    assert seen["timeout"] == MAX_TIMEOUT_SECONDS

    def huge(url, user_agent, timeout):
        return b"x" * (MAX_RESPONSE_BYTES + 1)

    with pytest.raises(RuntimeError, match="exceeds"):
        fetch_url_bytes("https://example.com/a", opener=huge)


def test_hand_written_receipt_file_does_not_load(tmp_path):
    digest = hashlib.sha256(b"not-a-fetch").hexdigest()
    (tmp_path / f"{digest}.bin").write_bytes(b"not-a-fetch")
    (tmp_path / "forged.json").write_text(
        json.dumps(
            {
                "kind": "m6-fetch-receipt",
                "reason": "hand-inserted archived source",
                "source_id": "src-forged",
                "content_hash": digest,
                "location": "https://example.com/a",
                "retrieval_date": "2026-10-18T00:00:00Z",
                "bytes_name": f"{digest}.bin",
            }
        ),
        encoding="utf-8",
    )
    assert load_persisted_receipts(tmp_path) == []

    class Minted:
        reason = "independent HTTP fetch by qad.m6.original_fetch"
        raw_bytes = b"sec-bytes"
        content_hash = hashlib.sha256(b"sec-bytes").hexdigest()
        source_id = "src-real"
        location = "https://www.sec.gov/Archives/example"
        retrieval_date = "2026-10-18T01:02:03Z"
        publication_date = "2026-03-31"
        source_tier = "L1"
        source_type = "SEC_FILING"
        title = "example"

    written = persist_receipts(tmp_path, [Minted()])
    loaded = load_persisted_receipts(tmp_path)
    assert len(written) == 1
    assert len(loaded) == 1
    assert loaded[0].content_hash == Minted.content_hash
    assert loaded[0].raw_bytes == b"sec-bytes"
    tampered = tmp_path / f"{Minted.content_hash}.bin"
    tampered.write_bytes(b"tampered")
    assert load_persisted_receipts(tmp_path) == []
