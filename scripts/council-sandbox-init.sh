#!/usr/bin/env bash
# council-sandbox-init.sh — Generic Council Sandbox lifecycle manager (v2)
# INT-G2.1: Creates isolated execution environment for blind Round-1 review.
#
# WARNING: Do NOT use `icacls /deny "Everyone:(W,D,DC)"` on Windows.
# The Everyone group includes the Admin user — it locks out the running session.
#
# Primary isolation mechanism (Windows):
#   Option A: Docker terminal backend (proven Harness Stage 3, FD #100)
#   Option B: OS-level ACL targeting non-admin accounts only (defense-in-depth)
#   Both: Directory allowlist — NOT path denylist
#
# Usage:
#   bash scripts/council-sandbox-init.sh setup <task-id>
#   bash scripts/council-sandbox-init.sh teardown <task-id>
#   bash scripts/council-sandbox-init.sh status <task-id>
set -u

CORE_ROOT="/c/Users/Admin/Desktop/Antigravity"
STAGING="$CORE_ROOT/_staging/council-sandbox"

ACTION="${1:-}"
TASK_ID="${2:-}"

fail() { echo "[COUNCIL-SANDBOX] FAIL: $*" >&2; exit 1; }
info() { echo "[COUNCIL-SANDBOX] $*"; }

setup() {
  local task="$TASK_ID"
  [ -n "$task" ] || fail "task-id required"
  
  local ws="$STAGING/$task"
  [ -d "$ws" ] && fail "workspace already exists: $ws (teardown first)"
  
  info "Creating sandbox workspace: $ws"
  mkdir -p "$ws/packet" "$ws/sources" "$ws/methodology" "$ws/output" "$ws/logs"
  
  # === ALLOWLIST MODEL ===
  # The sandbox workspace contains ONLY:
  #   /packet      RO → Review packet (parent provides)
  #   /sources     RO → Approved reference materials
  #   /methodology RO → Council procedure rules
  #   /output      RW → Critic's own output only
  #   /logs        RW → Execution trace (critic-owned)
  #
  # System paths (profiles, repo, temp, cache) are NOT present in the sandbox.
  # Enforcement is through:
  #   1. Docker container with only /workspace bound (primary)
  #   2. `pre_tool_call` hooks blocking known production paths (defense-in-depth)
  #   3. Subagent prompt instructing tool scope (hygiene, NOT security)
  #
  # WINDOWS ACL NOTE:
  #   icacls /deny "Everyone" blocks Admin on Windows.
  #   Instead of denying system paths, this script creates an ALLOWLIST
  #   workspace that the subagent operates within.
  
  # Create manifest
  cat > "$ws/MANIFEST.md" <<EOF
# Council Sandbox Manifest — $task
**Created:** $(date '+%Y-%m-%d %H:%M:%S %Z')
**Primary isolation:** Execution context (Docker or tool-scoped)
**Allowlist model:**

| Path | Permission | Content |
|------|-----------|---------|
| /packet | READ ONLY | Review packet |
| /sources | READ ONLY | Approved reference materials |
| /methodology | READ ONLY | Council procedure rules |
| /output | READ-WRITE | Critic output (own only) |
| /logs | READ-WRITE | Execution trace |

**NOT exposed (by design):**
- Hermes profile homes (memory, config, credentials, .env)
- Peer delegation transcripts
- Canonical repository (RW)
- Transitional worktree
- Shared system temp
- Other critic outputs
- Docker socket
- Broad MCP/tool surface

**Rollback:** Delete workspace directory (manifest-driven)
EOF
  
  echo "$ws"
  info "Sandbox ready: $ws"
}

teardown() {
  local task="$TASK_ID"
  [ -n "$task" ] || fail "task-id required"
  local ws="$STAGING/$task"
  [ -d "$ws" ] || fail "workspace not found: $ws"
  
  info "Tearing down sandbox: $ws"
  rm -rf "$ws"
  info "Sandbox teardown complete"
}

status() {
  local task="$TASK_ID"
  [ -n "$task" ] || fail "task-id required"
  local ws="$STAGING/$task"
  if [ -d "$ws" ]; then
    echo "ACTIVE: $ws"
    ls -la "$ws/"
    [ -f "$ws/MANIFEST.md" ] && echo "Manifest: present" || echo "Manifest: MISSING"
  else
    echo "NOT FOUND"
  fi
}

case "$ACTION" in
  setup)    setup ;;
  teardown) teardown ;;
  status)   status ;;
  *)
    echo "Usage: $0 {setup|teardown|status} <task-id>"
    echo ""
    echo "  setup   — Create allowlist sandbox workspace"
    echo "  teardown — Remove sandbox workspace"
    echo "  status  — Check sandbox workspace state"
    exit 1
    ;;
esac