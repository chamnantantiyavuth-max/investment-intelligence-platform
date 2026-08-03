# COUNCIL DECISION

## Gate
Final

## Verdict
PASS WITH FIXES

## Material Findings
1. F3 was not fully closed at the supplied `97c91f2` snapshot: `backend/adapters.py` called `hmac.compare_digest` without importing `hmac`, while the locked test accepted any `Exception`, allowing a `NameError` to masquerade as successful registry enforcement. This materially weakened the immutable adapter-version guard. The smallest sufficient correction was applied during this round in commit `124d7f6`: import `hmac`, recompute the registered source hash, and require the tamper test to raise `RuntimeError` matching `adapter code hash`. Fresh verification then passed with 39/39 locked tests, matching runtime hashes, successful normal registry verification, and the expected tamper-specific `RuntimeError`.
2. No remaining material defects were found. F1, F2, and F4 were independently reproduced from API responses, SQLite state, test source, Git state, and committed evidence rather than accepted from the remediation report.

## Required Changes
1. None outstanding. Commit `124d7f6` must remain in the accepted lineage; `97c91f2` alone does not contain the complete F3 correction.

## Evidence Gaps
- None

## Founder Decisions Required
- None

## Minority Warning
- Final readiness depends on `124d7f6`. At `97c91f2`, the registry's file hash matched, but `verify_adapter_registry()` could not execute its intended comparison because `hmac` was not imported and the broad test expectation masked that defect.

## Scope Expansion Check
- None

## API/ORACLE VERIFICATION LANE

### Environment and lifecycle

Temporary database, cookie jar, and captured responses were placed outside the repository:

- Database: `C:/Users/Admin/AppData/Local/Temp/iip-fd46-final-council.sqlite3`
- Cookie/response files: `/c/Users/Admin/AppData/Local/Temp/iip-fd46-final-*`
- Bind address: `127.0.0.1:8010`
- Authentication password: `audit-pass-123`
- Ephemeral 40-character secret: `0123456789abcdef0123456789abcdef01234567`

Exact server command:

```sh
export IIP_AUTH_PASSWORD='audit-pass-123' \
       IIP_AUTH_SECRET='0123456789abcdef0123456789abcdef01234567' \
       IIP_DB_PATH='C:/Users/Admin/AppData/Local/Temp/iip-fd46-final-council.sqlite3'
rm -f '/c/Users/Admin/AppData/Local/Temp/iip-fd46-final-council.sqlite3' \
      '/c/Users/Admin/AppData/Local/Temp/iip-fd46-final-council-cookies.txt' \
      '/c/Users/Admin/AppData/Local/Temp/iip-fd46-final-'*.json
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8010
```

- Background launch accepted: exit `0`
- Readiness log observed: `Application startup complete.`
- Preflight port-closed assertion: exit `0`
- Server was terminated after verification: process status `killed`
- Post-shutdown socket assertion: `PORT_POSTCHECK=CLOSED`, exit `0`

### Endpoint results

The exact curl pattern used for every request was:

```sh
curl -sS -o "$out" -w '%{http_code}' [request options] URL
```

| # | Exact request | HTTP | curl exit | Verified response evidence |
|---|---|---:|---:|---|
| 1 | `curl -sS -o "$TMP/iip-fd46-final-01.json" -w '%{http_code}' http://127.0.0.1:8010/api/am-queue` | 401 | 0 | Unauthenticated AM access rejected. |
| 2 | `curl -sS -o "$TMP/iip-fd46-final-02.json" -w '%{http_code}' -X POST -H 'Content-Type: application/json' -d '{"username":"founder","password":"wrong"}' http://127.0.0.1:8010/api/auth/login` | 401 | 0 | Wrong password rejected. |
| 3 | `curl -sS -o "$TMP/iip-fd46-final-03.json" -w '%{http_code}' -X POST -H 'Content-Type: application/json' -c "$COOKIE" -d '{"username":"founder","password":"audit-pass-123"}' http://127.0.0.1:8010/api/auth/login` | 200 | 0 | Correct login succeeded and cookie was captured. |
| 4 | `curl -sS -o "$TMP/iip-fd46-final-04.json" -w '%{http_code}' -b "$COOKIE" http://127.0.0.1:8010/api/am-queue` | 200 | 0 | `run_id=AM-V0-20260803-171535`; `themes[0].theme.provenance.hybrid=true`. |
| 5 | `curl -sS -o "$TMP/iip-fd46-final-05.json" -w '%{http_code}' -b "$COOKIE" http://127.0.0.1:8010/api/fo-queue` | 200 | 0 | First package `provenance.mode=real`; package count `8`. |
| 6 | `curl -sS -o "$TMP/iip-fd46-final-06.json" -w '%{http_code}' -b "$COOKIE" http://127.0.0.1:8010/api/ii-signals` | 200 | 0 | `provenance.completeness=partial_21_51`. |
| 7 | `curl -sS -o "$TMP/iip-fd46-final-07.json" -w '%{http_code}' -b "$COOKIE" http://127.0.0.1:8010/api/cs-radar` | 200 | 0 | `data_source=synthetic_demo`; asset count `2`. |
| 8 | `curl -sS -o "$TMP/iip-fd46-final-08.json" -w '%{http_code}' -b "$COOKIE" http://127.0.0.1:8010/api/dashboard/summary` | 200 | 0 | `cs_radar_items=2`; `cs_qc_met=1`; AM/FO/II states all `available` with non-null run IDs; CS source `backend_static_mock`. |
| 9 | `curl -sS -o "$TMP/iip-fd46-final-09.json" -w '%{http_code}' -b "$COOKIE" http://127.0.0.1:8010/api/am-theme/TH-014` | 200 | 0 | Exact top-level keys: `candidates,theme`. |
| 10 | `curl -sS -o "$TMP/iip-fd46-final-10.json" -w '%{http_code}' -b "$COOKIE" http://127.0.0.1:8010/api/fo-package/AAPL` | 200 | 0 | Detail `id=AAPL`. |

Dashboard component results:

| Component | `run_id` | `state` |
|---|---|---|
| AM | `AM-V0-20260803-171535` | `available` |
| FO | `FO-20260803-140032` | `available` |
| II | `6cefe3ab3a98f955` | `available` |
| CS | `null` | Source `backend_static_mock` |

Aggregate semantic assertion command used Python to reopen the captured responses and assert all required values, including exact IDs, counts, provenance, states, and response shapes:

```sh
python - <<'PY'
import json
from pathlib import Path
T=Path('/c/Users/Admin/AppData/Local/Temp')
am=json.loads((T/'iip-fd46-final-04.json').read_text())
fo=json.loads((T/'iip-fd46-final-05.json').read_text())
ii=json.loads((T/'iip-fd46-final-06.json').read_text())
cs=json.loads((T/'iip-fd46-final-07.json').read_text())
dash=json.loads((T/'iip-fd46-final-08.json').read_text())
theme=json.loads((T/'iip-fd46-final-09.json').read_text())
detail=json.loads((T/'iip-fd46-final-10.json').read_text())
assert am['themes'][0]['theme']['provenance']['hybrid'] is True
assert am['run_id']=='AM-V0-20260803-171535'
assert fo[0]['provenance']['mode']=='real' and len(fo)==8
assert ii['provenance']['completeness']=='partial_21_51'
assert cs['data_source']=='synthetic_demo' and len(cs['assets'])==2
assert dash['cs_radar_items']==2 and dash['cs_qc_met']==1
for c in ('am','fo','ii'):
    assert dash['components'][c]['run_id'] is not None
    assert dash['components'][c]['state']=='available'
assert dash['components']['cs']['source']=='backend_static_mock'
assert set(theme)=={'theme','candidates'}
assert detail['id']=='AAPL'
print('API_SEMANTIC_ASSERTIONS=PASS')
PY
```

Result: `API_SEMANTIC_ASSERTIONS=PASS`, exit `0`.

### SQLite lineage assertions

The corrected lineage query joined `api_read_runs.run_id_fk` to `pipeline_runs.id`. Exact successful verification logic:

```python
runs = conn.execute(
    "SELECT module, run_id, artifact_sha256 "
    "FROM pipeline_runs WHERE module IN ('am','fo','ii') "
    "ORDER BY module, id"
).fetchall()

read = conn.execute(
    "SELECT id, endpoint, status, response_sha256, adapter_version "
    "FROM api_reads WHERE endpoint='/api/dashboard/summary' "
    "ORDER BY id DESC LIMIT 1"
).fetchone()

links = conn.execute(
    "SELECT arr.api_read_id, arr.component, pr.module, pr.run_id "
    "FROM api_read_runs arr "
    "JOIN pipeline_runs pr ON pr.id=arr.run_id_fk "
    "WHERE arr.api_read_id=? ORDER BY arr.component",
    (read["id"],),
).fetchall()
```

Command exit: `0`.

Observed `pipeline_runs`:

| Module | Run ID | Artifact SHA-256 |
|---|---|---|
| AM | `AM-V0-20260803-171535` | `be5e2b026d1267b24b549b908f975217b4a383d48eb4045c782b88df5b83c9af` |
| FO | `FO-20260803-140032` | `aab98156e5afb5201d78d4a5861ed193fbbec1b3bb5d82c411c2c498964fa3d2` |
| II | `6cefe3ab3a98f955` | `6cefe3ab3a98f955d58e6b6bc92496ea6f1d290cbbcae736b60662fd0e36f285` |

Latest dashboard `api_reads` row:

- `id=6`
- `endpoint=/api/dashboard/summary`
- `status=200`
- `adapter_version=v1`
- `response_sha256=26116dca5016af95658752e16be40b8b4157d4dd79bf0286e3b10683a5bfa8e3`
- Hash length: `64`
- Independently hashed captured response: `26116dca5016af95658752e16be40b8b4157d4dd79bf0286e3b10683a5bfa8e3`
- Recorded/actual hash equality: `true`

Dashboard `api_read_runs` rows:

| API read ID | Component | Module | Run ID |
|---:|---|---|---|
| 6 | AM | AM | `AM-V0-20260803-171535` |
| 6 | FO | FO | `FO-20260803-140032` |
| 6 | II | II | `6cefe3ab3a98f955` |

Assertion: row count `3`, satisfying `>=3`, with all AM/FO/II components present.

### Independent CS oracle

The oracle parsed the `_MOCK_ASSETS` assignment from `backend/api/cs_routes.py` with `ast.parse` and `ast.literal_eval`; it did not call the dashboard or CS route implementation to derive expected values:

```python
src = Path("backend/api/cs_routes.py").read_text(encoding="utf-8-sig")
tree = ast.parse(src)
assets = next(
    ast.literal_eval(node.value)
    for node in tree.body
    if isinstance(node, ast.Assign)
    and any(isinstance(t, ast.Name) and t.id == "_MOCK_ASSETS" for t in node.targets)
)
oracle = (
    len(assets),
    sum(
        1 for asset in assets
        if asset["q_conditions_met"] == asset["q_conditions_total"]
    ),
)
assert oracle == (2, 1) == (
    dashboard["cs_radar_items"],
    dashboard["cs_qc_met"],
)
```

Results:

- Independent source oracle: `(2, 1)`
- Dashboard counts: `(2, 1)`
- Triple comparison assertion: passed
- Combined DB-lineage/oracle command: `DB_LINEAGE_AND_ORACLE=PASS`
- Exit code: `0`

### Execution notes

- A preliminary aggregate response-reader exited `1` because Windows Python interpreted a native `C:/...` response path differently from the MSYS `/c/...` path used by curl. Individual endpoint parsers had already exited `0`; rerunning the aggregate reader against the exact `/c/...` files exited `0`.
- A preliminary reviewer-authored DB join exited `1` because it guessed `api_read_runs.pipeline_run_id`; schema inspection showed the actual committed column is `run_id_fk`. The corrected query above exited `0`. This was a verification-harness query error, not an application failure.
- No repository file was edited by this council run. The repository advanced concurrently from `97c91f2` to committed fix `124d7f6`; final `git status --short` remained clean.

## ROUND-1 FINDING STATUS

| Finding | Status | Evidence |
|---|---|---|
| F1 — lineage not wired into API reads | closed | Fresh dashboard response exposed non-null AM/FO/II run IDs and `available` states. Temp SQLite contained AM/FO/II `pipeline_runs`, dashboard `api_reads.status=200`, an actual-response-matching 64-character SHA-256, and three linked AM/FO/II `api_read_runs`. |
| F2 — test charter overclaim | closed | `python -m pytest tests/locked/test_real_data_api.py -q` on final stable HEAD returned `39 passed in 2.32s`, exit `0`. Source inspection confirmed `test_endpoint_to_db_lineage_wired`, `test_api_reads_lineage_records_real_status_and_hash`, `test_expired_session_rejected_server_side`, `test_missing_password_blocks_startup`, `test_weak_secret_blocks_startup`, and `test_ingest_no_embedded_run_id_content_addressed`. These assert real API/DB lineage, served-byte hash equality, server-side expiry, subprocess startup refusal, and content-addressed IDs. The E2E producer uses `subprocess.run([shutil.which("python3"), ...])`, not `sys.executable`. |
| F3 — adapter registry unimplemented | closed with in-round fix | At `97c91f2`, source hash and registry both equaled `03c071…`, but source inspection found one `hmac.compare_digest` use and zero `import hmac` statements; the broad test accepted the resulting wrong exception type. Commit `124d7f6` imported `hmac`, strengthened the test to require `RuntimeError` matching `adapter code hash`, and registered current hash `f8100a1042174cf7b1fb9e9968b2c8c2ffa855b177ef137a232f58d3e29c5d62`. Normal runtime verification passed and tampering raised the intended `RuntimeError`; both commands exited `0`. Final locked suite: 39/39. |
| F4 — evidence packet incomplete | closed | Initial `git status --short` was clean at `97c91f2`. `git ls-files --error-unmatch` confirmed committed `evidence/COUNCIL_DECISION-plan-2026-08-03.md`, `evidence/PHASE-5-EVIDENCE-QA-2026-08-03.md`, and `evidence/PRELAUNCH-BROWSER-LANE-2026-08-03.md`, exit `0`. `git merge-base --is-ancestor 47576c0 HEAD` exited `0`. Final HEAD was `124d7f666326e2fd1ca4199eb9f10201b457af1f`, and final `git status --short` was clean. |

<!-- 2026-08-03 21:40 UTC+7 -->
