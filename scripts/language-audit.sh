#!/bin/zsh
# Language audit — flags soft language patterns across all SKILL.md files.
# Curator decides what to harden — this script finds candidates only.
# Wired as a Stop hook on the engineering-playbook to catch regression after every curator session.

PATTERNS="should\|try to\|when possible\|if possible\|consider\|may\|might\|ideally\|where applicable\|as needed"
REPO_ROOT="$(git -C "$(dirname "$0")" rev-parse --show-toplevel 2>/dev/null || echo '.')"
RESULTS=$(grep -rn --include="SKILL.md" -e "should" -e "try to" -e "when possible" -e "if possible" -e "consider" -e "ideally" -e "where applicable" -e "as needed" "$REPO_ROOT/skills/" 2>/dev/null)

if [[ -z "$RESULTS" ]]; then
  echo "✓ Language audit: no soft language patterns found."
else
  COUNT=$(echo "$RESULTS" | wc -l | tr -d ' ')
  echo "⚠️  Language audit: $COUNT soft language candidate(s) for curator review:"
  echo ""
  echo "$RESULTS" | sed 's|'"$REPO_ROOT"'/||'
fi
