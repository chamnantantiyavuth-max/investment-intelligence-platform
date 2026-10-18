"""Serverless session mode (IIP_STATELESS_SESSIONS=1, set by api/index.py on Vercel).

A login on one function instance must authenticate on another instance whose /tmp
store has no nonce row. Expiry, signature, and logout on the serving instance still reject.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

_SCRIPT = r"""
import json, os, time
from fastapi import Response
from backend import auth, persistence
assert auth.STATELESS_SESSIONS
r = Response()
assert auth.login("founder", "pw-test", r)
token = r.headers["set-cookie"].split("iip_session=", 1)[1].split(";", 1)[0].strip('"').replace('\\054', ',').replace('\\"', '"')
out = {}
persistence.set_active_nonce(None)  # cold instance: no nonce row
out["cold_instance"] = auth.verify_session(token)
persistence.set_active_nonce("someone-else")  # instance that served an older login
out["other_nonce"] = auth.verify_session(token)
out["tampered"] = auth.verify_session(token[:-1] + ("0" if token[-1] != "0" else "1"))
p = json.dumps({"nonce": "n", "issued_at": int(time.time()) - 7200, "expires_at": int(time.time()) - 1}, separators=(",", ":"))
out["expired"] = auth.verify_session(p + "." + auth._sign(p))
auth.logout(Response(), token)
out["after_logout_same_instance"] = auth.verify_session(token)
print(json.dumps(out))
"""


def test_stateless_session_survives_cold_instance_and_logout_revokes_locally():
    env = dict(os.environ)
    tmp = tempfile.mkdtemp(prefix="iip-stateless-")
    env.update({
        "IIP_STATELESS_SESSIONS": "1",
        "IIP_DB_PATH": str(Path(tmp) / "iip.db"),
        "IIP_AUTH_USER": "founder",
        "IIP_AUTH_PASSWORD": "pw-test",
        "IIP_AUTH_SECRET": "s" * 40,
    })
    r = subprocess.run([sys.executable, "-c", _SCRIPT], capture_output=True, text=True,
                       timeout=60, cwd=str(REPO), env=env)
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout.strip().splitlines()[-1])
    assert out == {
        "cold_instance": True,
        "other_nonce": True,
        "tampered": False,
        "expired": False,
        "after_logout_same_instance": False,
    }
