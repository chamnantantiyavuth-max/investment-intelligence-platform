#!/usr/bin/env bash
# council-sandbox-hook.sh — pre_tool_call allowlist enforcer for Council sandbox
# INT-G2.1: Blocks file tools from accessing paths outside the sandbox allowlist.
#
# Install in profile config.yaml:
#   hooks:
#     pre_tool_call:
#       - command: "bash .../scripts/council-sandbox-hook.sh"
#         timeout: 5
#         fail_closed: true
#
# stdin: {"tool_name":"read_file","tool_input":{"path":"..."},...}
# stdout: {"action":"block","message":"..."} to block; empty to allow.
set -u

# === SANDBOX ALLOWLIST ===
# Only paths under these roots are allowed for file tools.
ALLOWED_ROOTS=(
  "C:/Users/Admin/Desktop/Antigravity/_staging/council-sandbox"
)

# File tools that read or write paths
FILE_TOOLS="read_file|write_file|patch|search_files"

INPUT=$(cat 2>/dev/null || echo "{}")

TOOL=$(printf '%s' "$INPUT" | python -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('tool_name', ''))
except:
    print('')" 2>/dev/null)

TOOL_INPUT_PATH=$(printf '%s' "$INPUT" | python -c "
import sys, json
try:
    data = json.load(sys.stdin)
    inp = data.get('tool_input', {})
    if isinstance(inp, dict):
        print(inp.get('path', inp.get('pattern', '')))
    else:
        print(inp)
except:
    print('')" 2>/dev/null)

# Only enforce for file tools
if echo "$TOOL" | grep -qiE "^($FILE_TOOLS)$" 2>/dev/null && [ -n "$TOOL_INPUT_PATH" ]; then
  ALLOWED=false
  for root in "${ALLOWED_ROOTS[@]}"; do
    # Normalize: convert both to forward-slash, lowercase
    root_norm=$(echo "$root" | sed 's|\\|/|g' | tr '[:upper:]' '[:lower:]')
    path_norm=$(echo "$TOOL_INPUT_PATH" | sed 's|\\|/|g' | tr '[:upper:]' '[:lower:]')
    if echo "$path_norm" | grep -q "^$root_norm"; then
      ALLOWED=true
      break
    fi
  done
  
  if [ "$ALLOWED" = "false" ]; then
    echo "{\"action\":\"block\",\"message\":\"Council sandbox: path '$TOOL_INPUT_PATH' is outside the sandbox allowlist. Allowed roots: ${ALLOWED_ROOTS[*]}\"}"
    exit 0
  fi
fi

# Allow (empty output)
exit 0