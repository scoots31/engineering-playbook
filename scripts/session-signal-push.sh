#!/bin/zsh
# Session signal push — reads .claude/session-signals.tmp from the current project,
# appends structured lines to shared/session-log.md in the engineering-playbook repo,
# pushes, then clears the tmp file.
# If push fails, writes to shared/pending-signals.tmp for inclusion in the next successful push.

PLAYBOOK_ROOT=~/Developer/engineering-playbook
SESSION_LOG="$PLAYBOOK_ROOT/shared/session-log.md"
PENDING="$PLAYBOOK_ROOT/shared/pending-signals.tmp"

# Locate the project root (where .claude/session-signals.tmp lives)
# Walk up from cwd until we find a .claude dir or hit home
PROJECT_ROOT="$PWD"
while [[ "$PROJECT_ROOT" != "$HOME" && ! -d "$PROJECT_ROOT/.claude" ]]; do
  PROJECT_ROOT="$(dirname "$PROJECT_ROOT")"
done

SIGNALS_FILE="$PROJECT_ROOT/.claude/session-signals.tmp"

# Nothing to do if no signals file or it's empty
[[ -f "$SIGNALS_FILE" && -s "$SIGNALS_FILE" ]] || exit 0

# Collect pending signals from prior failed pushes
PENDING_CONTENT=""
if [[ -f "$PENDING" && -s "$PENDING" ]]; then
  PENDING_CONTENT="$(cat "$PENDING")"
fi

# Append pending + current signals to session log
{
  if [[ -n "$PENDING_CONTENT" ]]; then
    echo "$PENDING_CONTENT"
  fi
  cat "$SIGNALS_FILE"
} >> "$SESSION_LOG"

# Push to remote
cd "$PLAYBOOK_ROOT" || exit 0
git add shared/session-log.md 2>/dev/null
git commit -m "session signals" --no-gpg-sign -q 2>/dev/null
if git push -q 2>/dev/null; then
  # Success — clear both files
  rm -f "$SIGNALS_FILE"
  rm -f "$PENDING"
else
  # Push failed — move current signals to pending, clear tmp
  {
    if [[ -n "$PENDING_CONTENT" ]]; then
      echo "$PENDING_CONTENT"
    fi
    cat "$SIGNALS_FILE"
  } > "$PENDING"
  rm -f "$SIGNALS_FILE"
fi
