#!/usr/bin/env bash
# Fail-closed board assertion for IIP/IPM organizational Kanban work (C1, Stage 3.2).
#
# Root cause of S3-F1: hermes_cli/main.py `_pin_kanban_board_env()` pins
# HERMES_KANBAN_BOARD=<current board> at chat-session boot. The session that ran
# Stage 3 started while the board file still said "other", so every shell/CLI
# spawned from that session inherited the stale env value (env > board file in
# get_current_board() precedence). `hermes kanban boards switch iip` fixed the
# file, but not the inherited env.
#
# Guard rule (fail-closed):
#   expected_board = iip (IIP/IPM shared board slug)
#   resolved_board  = effective board for this shell
#   if resolved_board != iip -> EXIT 1, DO NOT create/dispatch the task.
#
# Usage:
#   bash scripts/board-guard.sh            # standalone check (exit 0/1)
#   bash scripts/board-guard.sh --force    # export override then verify
set -u

EXPECTED_BOARD="iip"
KANBAN_ROOT="${KANBAN_ROOT:-/c/Users/Admin/AppData/Local/hermes}"

_resolve_board_value() {
  # 1) explicit env pin (what in-process tools + shelled CLI actually use)
  local env_b="${HERMES_KANBAN_BOARD:-}"
  if [ -n "$env_b" ]; then
    echo "$env_b"
    return
  fi
  # 2) persisted current-board file
  local cur_file="$KANBAN_ROOT/kanban/current"
  if [ -f "$cur_file" ]; then
    tr -d '[:space:]' < "$cur_file"
    return
  fi
  echo ""
}

if [ "${1:-}" = "--force" ]; then
  export HERMES_KANBAN_BOARD="$EXPECTED_BOARD"
  echo "[board-guard] forced HERMES_KANBAN_BOARD=$EXPECTED_BOARD (explicit pin override)"
fi

resolved="$(_resolve_board_value)"
echo "[board-guard] resolved board: '${resolved:-<unset>}' | expected: '$EXPECTED_BOARD'"

if [ "$resolved" != "$EXPECTED_BOARD" ]; then
  echo "[board-guard] FAIL-CLOSED: resolved board is '${resolved:-<unset>}', expected '$EXPECTED_BOARD'." >&2
  echo "[board-guard] DO NOT create or dispatch any organizational task." >&2
  echo "[board-guard] Fix: run 'hermes kanban boards switch iip' AND ensure HERMES_KANBAN_BOARD=iip in this shell (or use --force)." >&2
  exit 1
fi

echo "[board-guard] PASS: board = $EXPECTED_BOARD (fail-closed assertion satisfied)"
export BOARD_OK=1
exit 0
