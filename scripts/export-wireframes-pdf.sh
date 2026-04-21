#!/usr/bin/env bash
# Launcher: run this from engineering-playbook as ./scripts/export-wireframes-pdf.sh
# Delegates to the Fantasy Player Evaluation System repo (wireframes live there).
set -euo pipefail
FPE_ROOT="${FPE_ROOT:-$HOME/Developer/Fantasy Player Evaluation System}"
TARGET="$FPE_ROOT/scripts/export-wireframes-pdf.sh"
if [[ ! -x "$TARGET" ]]; then
  echo "Expected: $TARGET" >&2
  echo "Set FPE_ROOT to your Fantasy Player Evaluation System clone and retry." >&2
  exit 1
fi
exec "$TARGET" "$@"
