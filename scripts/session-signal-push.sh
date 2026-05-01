#!/bin/zsh
# Session signal push — reads .claude/session-signals.tmp from the current project,
# appends structured lines to shared/session-log.md in the engineering-playbook repo,
# pushes, then clears the tmp file.
# If push fails, writes to shared/pending-signals.tmp for inclusion in the next successful push.

PLAYBOOK_ROOT=~/Developer/engineering-playbook
SESSION_LOG="$PLAYBOOK_ROOT/shared/session-log.md"
RETRO_LOG="$PLAYBOOK_ROOT/shared/retro-log.md"
PENDING="$PLAYBOOK_ROOT/shared/pending-signals.tmp"
PENDING_RETRO="$PLAYBOOK_ROOT/shared/pending-retro.tmp"

# Locate the project root (where .claude/ lives)
# Walk up from cwd until we find a .claude dir or hit home
PROJECT_ROOT="$PWD"
while [[ "$PROJECT_ROOT" != "$HOME" && ! -d "$PROJECT_ROOT/.claude" ]]; do
  PROJECT_ROOT="$(dirname "$PROJECT_ROOT")"
done

SIGNALS_FILE="$PROJECT_ROOT/.claude/session-signals.tmp"
RETRO_FILE="$PROJECT_ROOT/.claude/retro-notes.tmp"

HAS_SIGNALS=false
HAS_RETRO=false
[[ -f "$SIGNALS_FILE" && -s "$SIGNALS_FILE" ]] && HAS_SIGNALS=true
[[ -f "$RETRO_FILE" && -s "$RETRO_FILE" ]] && HAS_RETRO=true

# Nothing to do if neither file has content
[[ "$HAS_SIGNALS" == true || "$HAS_RETRO" == true ]] || exit 0

# ── Session signals ──────────────────────────────────────────────────────────
if [[ "$HAS_SIGNALS" == true ]]; then
  PENDING_CONTENT=""
  if [[ -f "$PENDING" && -s "$PENDING" ]]; then
    PENDING_CONTENT="$(cat "$PENDING")"
  fi
  {
    [[ -n "$PENDING_CONTENT" ]] && echo "$PENDING_CONTENT"
    cat "$SIGNALS_FILE"
  } >> "$SESSION_LOG"
fi

# ── Retro notes ──────────────────────────────────────────────────────────────
if [[ "$HAS_RETRO" == true ]]; then
  PENDING_RETRO_CONTENT=""
  if [[ -f "$PENDING_RETRO" && -s "$PENDING_RETRO" ]]; then
    PENDING_RETRO_CONTENT="$(cat "$PENDING_RETRO")"
  fi
  {
    [[ -n "$PENDING_RETRO_CONTENT" ]] && echo "$PENDING_RETRO_CONTENT"
    cat "$RETRO_FILE"
  } >> "$RETRO_LOG"
fi

# ── Push to remote ───────────────────────────────────────────────────────────
cd "$PLAYBOOK_ROOT" || exit 0
git add shared/session-log.md shared/retro-log.md 2>/dev/null
git commit -m "session signals + retro notes" --no-gpg-sign -q 2>/dev/null
if git push -q 2>/dev/null; then
  # Success — clear all tmp files
  rm -f "$SIGNALS_FILE" "$PENDING"
  rm -f "$RETRO_FILE" "$PENDING_RETRO"
else
  # Push failed — hold in pending files, clear session tmp files
  if [[ "$HAS_SIGNALS" == true ]]; then
    {
      [[ -n "$PENDING_CONTENT" ]] && echo "$PENDING_CONTENT"
      cat "$SIGNALS_FILE"
    } > "$PENDING"
    rm -f "$SIGNALS_FILE"
  fi
  if [[ "$HAS_RETRO" == true ]]; then
    {
      [[ -n "$PENDING_RETRO_CONTENT" ]] && echo "$PENDING_RETRO_CONTENT"
      cat "$RETRO_FILE"
    } > "$PENDING_RETRO"
    rm -f "$RETRO_FILE"
  fi
fi
