#!/usr/bin/env bash
# Cursor hook: beforeShellExecution — flag obviously destructive patterns for review.
# Requires: jq on PATH. stdin: JSON with .command

set -euo pipefail

if ! command -v jq >/dev/null 2>&1; then
  echo '{ "permission": "allow" }'
  exit 0
fi

input=$(cat)
command=$(echo "$input" | jq -r '.command // empty')

# Broad patterns — tune for your workflow
if echo "$command" | grep -Eiq 'rm[[:space:]]+-rf|mkfs\.|dd[[:space:]]+if=|:>[[:space:]]*/dev/|curl[[:space:]].*\|[[:space:]]*bash|wget[[:space:]].*\|[[:space:]]*bash'; then
  echo '{
    "permission": "ask",
    "user_message": "This command looks potentially destructive or pipes remote content into a shell. Confirm before running.",
    "agent_message": "guard-destructive hook asked for confirmation."
  }'
  exit 0
fi

echo '{ "permission": "allow" }'
exit 0
