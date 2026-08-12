#!/usr/bin/env bash
# board-safety-hook.sh — pre_tool_call fail-closed guard for IIP board safety (Stage 4, S3-F1 v2)
# stdin: {"hook_event_name":"pre_tool_call","tool_name":"...","tool_input":{...},...}
# stdout: {"action":"block","message":"..."} to block; empty/other to allow.
# fail_closed:true in config makes hook failure/absence block by default.
set -u
EXPECTED_BOARD="iip"
KANBAN_ROOT="/c/Users/Admin/AppData/Local/hermes"
EXPECTED_DB="$KANBAN_ROOT/kanban/boards/iip/kanban.db"

INPUT=$(cat 2>/dev/null || echo "{}")

TOOL=$(printf '%s' "$INPUT" | python -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null)

BOARD_ARG=""
DB_ARG=""
CMD=""

guard_kanban() {
  # $1 = effective board (may be empty), $2 = effective db (may be empty)
  local eb="$1" edb="$2"
  # explicit tool board arg override (F4: in-agent tools expose board input)
  local resolved="${eb:-${HERMES_KANBAN_BOARD:-}}"
  if [ -z "$resolved" ]; then
    resolved="$(tr -d '[:space:]' < "$KANBAN_ROOT/kanban/current" 2>/dev/null)"
  fi
  # HERMES_KANBAN_DB pins the DB path directly and takes precedence (F4).
  # Compare NORMALIZED paths: the live env carries Windows form (C:\...) while
  # EXPECTED_DB is MSYS form (/c/...) — a raw string compare false-blocks every
  # call. cygpath -m maps both to C:/... (forward slashes), then lowercase.
  local db="${edb:-${HERMES_KANBAN_DB:-}}"
  if [ -n "$db" ]; then
    local db_norm expected_norm
    db_norm="$(norm_path "$db")"
    expected_norm="$(norm_path "$EXPECTED_DB")"
    if [ "$db_norm" != "$expected_norm" ]; then
      echo "{\"action\":\"block\",\"message\":\"Board safety: HERMES_KANBAN_DB=$db targets a DB other than the IIP board DB ($EXPECTED_DB)\"}"
      return 0
    fi
  fi
  if [ "$resolved" != "$EXPECTED_BOARD" ]; then
    echo "{\"action\":\"block\",\"message\":\"Board safety: resolved board '$resolved' != expected '$EXPECTED_BOARD' — refusing kanban mutation\"}"
    return 0
  fi
  return 0  # allow (empty output)
}

# Normalize a filesystem path for comparison: cygpath -m yields C:/... form;
# fall back to a manual backslash->slash conversion if cygpath is unavailable.
norm_path() {
  local p="$1" out
  out="$(cygpath -m "$p" 2>/dev/null)" || out=""
  if [ -z "$out" ]; then
    out="$(printf '%s' "$p" | tr '\\' '/')"
  fi
  printf '%s' "$out" | tr 'A-Z' 'a-z'
}

case "$TOOL" in
  kanban_*)
    # in-agent kanban tool: parse explicit board/db inputs (F4)
    BOARD_ARG=$(printf '%s' "$INPUT" | python -c "
import sys,json
try:
    d=json.load(sys.stdin); ti=d.get('tool_input') or {}
    print(ti.get('board') or '')
except Exception: print('')" 2>/dev/null)
    DB_ARG=$(printf '%s' "$INPUT" | python -c "
import sys,json
try:
    d=json.load(sys.stdin); ti=d.get('tool_input') or {}
    print(ti.get('db') or ti.get('db_path') or '')
except Exception: print('')" 2>/dev/null)
    guard_kanban "$BOARD_ARG" "$DB_ARG"
    ;;
  terminal)
    CMD=$(printf '%s' "$INPUT" | python -c "
import sys,json
try:
    d=json.load(sys.stdin); ti=d.get('tool_input') or {}
    print(ti.get('command') or '')
except Exception: print('')" 2>/dev/null)
    case "$CMD" in
      *"hermes kanban"*)
        # CLI kanban mutation from within agent terminal (F1: CLI path must be guarded)
        case "$CMD" in
          *create*|*assign*|*complete*|*block*|*unblock*|*comment*|*link*|*archive*|*move*|*promote*|*dispatch*)
            BOARD_ARG=$(printf '%s' "$CMD" | grep -oE '\-\-board [a-z0-9-]+' | head -1 | awk '{print $2}')
            # R-ADD-2: inline env assignment overrides the hook process env —
            # detect HERMES_KANBAN_BOARD=<x> inside the command string.
            INLINE_BOARD=$(printf '%s' "$CMD" | grep -oE 'HERMES_KANBAN_BOARD=[a-z0-9_-]+' | head -1 | cut -d= -f2)
            if [ -n "$INLINE_BOARD" ]; then
              guard_kanban "$INLINE_BOARD" ""
            else
              guard_kanban "$BOARD_ARG" ""
            fi
            ;;
          *) exit 0 ;;  # read-only kanban cmd (list/show/runs) — allow
        esac
        ;;
      *) exit 0 ;;  # non-kanban terminal command
    esac
    ;;
  *) exit 0 ;;  # non-kanban tool — allow
esac
exit 0
