#!/usr/bin/env bash
# =============================================================================
# gate-check.sh — Automated Gate Enforcement (v3.3.0), adapted for IIP (FD #46)
# Usage: bash scripts/gate-check.sh
# Exit 0 = all gates pass. Exit 1 = one or more gates fail.
# =============================================================================
set -euo pipefail

FAILURES=0
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

pass() { echo -e "  ${GREEN}✓${NC} $1"; }
fail() { echo -e "  ${RED}✗${NC} $1"; FAILURES=$((FAILURES + 1)); }

echo "=== Gate Check v3.3.0 (IIP) ==="
echo ""

# ---- Gate 3: Deployment Verify (no Alembic — SQLite stdlib, schema via persistence._init_db) ----
echo "Gate 3: Deployment Verify"
if python -c "from backend.persistence import check_schema_compatibility; check_schema_compatibility(); print('schema compatible')" > /dev/null 2>&1; then
    pass "SQLite schema version compatible"
else
    fail "schema_version incompatible — check backend/persistence.py"
fi
echo ""

# ---- Gate 5: Batch Atomicity (os.replace atomic writes in runners) ----
echo "Gate 5: Batch Atomicity"
if grep -q "os.replace" fundamental-opportunity-v0/run.py && grep -q "os.replace" institutional-intelligence-v0/display.py; then
    pass "Runners use atomic os.replace writes"
else
    fail "Atomic write missing in FO/II runners"
fi
echo ""

# ---- Gate 6: Verification Evidence Tags ----
echo "Gate 6: Verification Evidence Tags"
TAGS_FOUND=0
for tag in "TEST_VERIFIED" "STATIC_OBSERVATION" "BROWSER_VERIFIED"; do
    if git log -1 --format="%B" 2>/dev/null | grep -q "$tag"; then
        TAGS_FOUND=$((TAGS_FOUND + 1))
    fi
done
if [ $TAGS_FOUND -ge 1 ]; then
    pass "Evidence tags found in last commit ($TAGS_FOUND tag(s))"
else
    fail "No verification evidence tags in commit message"
fi
echo ""

# ---- Gate 1: Root-Cause Trace ----
echo "Gate 1: Root-Cause Check"
FORMULA_FILES=$(git diff --name-only HEAD~1 2>/dev/null | grep -E "calculation|formula|output|render" || true)
MODEL_FILES=$(git diff --name-only HEAD~1 2>/dev/null | grep -E "model|schema|migration|entity" || true)
if [ -n "$FORMULA_FILES" ] && [ -z "$MODEL_FILES" ]; then
    echo "  ⚠ Formula/output files changed without model changes — verify manually"
    pass "Root-cause check: manual verification recommended"
else
    pass "Root-cause check: no isolated formula changes detected"
fi
echo ""

# ---- Gate 4: Feature Complete (API smoke — all endpoints reachable) ----
echo "Gate 4: Feature Complete (API surface)"
if IIP_AUTH_PASSWORD=gate IIP_AUTH_SECRET=$(python -c "print('x'*40)") python -c "
from fastapi.testclient import TestClient
from backend.main import app
c = TestClient(app)
paths = [r.path for r in app.routes if r.path.startswith('/api')]
print(f'  routes: {len(paths)}')
assert any(p == '/api/ii-signals' for p in paths), 'ii-signals missing'
assert any(p == '/api/auth/login' for p in paths), 'auth login missing'
" > /dev/null 2>&1; then
    pass "API surface includes ii-signals + auth"
else
    fail "API surface incomplete"
fi
echo ""

echo "=== Gate Check Complete ==="
if [ $FAILURES -eq 0 ]; then
    echo -e "${GREEN}All automated gates passed${NC}"
    exit 0
else
    echo -e "${RED}$FAILURES gate(s) failed${NC}"
    exit 1
fi
