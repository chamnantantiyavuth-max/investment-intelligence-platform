"""Auth — single-user, stdlib HMAC session (arch v0.4 §5, plan T3).

Env-only secrets (IIP_AUTH_USER / IIP_AUTH_PASSWORD / IIP_AUTH_SECRET). Server-side
expiry + nonce revocation on logout. Loopback Host enforcement via middleware.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
import time
from datetime import datetime, timezone

from fastapi import Cookie, HTTPException, Request, Response

from backend import persistence

SESSION_COOKIE = "iip_session"
SESSION_TTL_SECONDS = 12 * 3600  # 12h advisory; server enforces expires_at

USERNAME = os.environ.get("IIP_AUTH_USER", "founder")
PASSWORD = os.environ.get("IIP_AUTH_PASSWORD", "")
SECRET = os.environ.get("IIP_AUTH_SECRET", "")

# Startup guards (fail fast, F6) — checked at import; ENV_CHECKED lets tests assert the guard ran.
ENV_CHECKED = False


def _check_env() -> None:
    global ENV_CHECKED
    if not PASSWORD:
        raise RuntimeError("IIP_AUTH_PASSWORD must be set (non-empty) before boot — refusing to start")
    if len(SECRET) < 32:
        raise RuntimeError("IIP_AUTH_SECRET must be >= 32 chars before boot — refusing to start")
    ENV_CHECKED = True


_check_env()


def _sign(payload: str) -> str:
    return hmac.new(SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()


def _issue_token(nonce: str) -> str:
    now = int(time.time())
    payload = json.dumps({"nonce": nonce, "issued_at": now, "expires_at": now + SESSION_TTL_SECONDS},
                         separators=(",", ":"))
    return f"{payload}.{_sign(payload)}"


def _verify_token(token: str) -> dict | None:
    """Return payload dict if signature + nonce + expiry all valid, else None."""
    try:
        payload_b64, sig = token.rsplit(".", 1)
    except ValueError:
        return None
    if not hmac.compare_digest(sig, _sign(payload_b64)):
        return None
    try:
        payload = json.loads(payload_b64)
    except json.JSONDecodeError:
        return None
    # server-side expiry (F6)
    if int(payload.get("expires_at", 0)) < int(time.time()):
        return None
    # server-side nonce (revocation on logout)
    active = persistence.get_active_nonce()
    if active is None or not hmac.compare_digest(str(payload.get("nonce", "")), active):
        return None
    return payload


def verify_session(cookie_value: str | None) -> bool:
    if not cookie_value:
        return False
    return _verify_token(cookie_value) is not None


def login(username: str, password: str, response: Response) -> bool:
    if not hmac.compare_digest(username, USERNAME) or not hmac.compare_digest(password, PASSWORD):
        return False
    nonce = secrets.token_hex(16)
    persistence.set_active_nonce(nonce)
    token = _issue_token(nonce)
    response.set_cookie(
        SESSION_COOKIE, token, httponly=True, samesite="lax", max_age=SESSION_TTL_SECONDS)
    return True


def logout(response: Response) -> None:
    persistence.set_active_nonce(None)  # revoke server-side — copied tokens die (F6)
    response.delete_cookie(SESSION_COOKIE)


def require_auth(request: Request) -> None:
    cookie = request.cookies.get(SESSION_COOKIE)
    if not verify_session(cookie):
        raise HTTPException(status_code=401, detail="Not authenticated")
