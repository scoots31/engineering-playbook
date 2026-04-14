#!/usr/bin/env bash
# Build packaging/dist/cursor-work-playbook.zip for transfer to a Cursor-only work machine (no GitHub).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
BUNDLE_SRC="$ROOT/packaging/cursor-work-bundle"
OUT="$ROOT/packaging/dist/cursor-work-playbook"
ZIP="$ROOT/packaging/dist/cursor-work-playbook.zip"

rm -rf "$OUT" "$ZIP"
mkdir -p "$OUT/skills" "$OUT/hooks/examples" "$OUT/templates" "$OUT/mempalace"

echo "==> Copying skills and hook examples"
cp -R "$ROOT/skills/"* "$OUT/skills/"
shopt -s nullglob
for f in "$ROOT/hooks/examples/"*; do
  cp "$f" "$OUT/hooks/examples/"
done
shopt -u nullglob
cp "$ROOT/templates/consumer-cursor-always-apply.mdc" "$OUT/templates/"

echo "==> Transforming shared docs (Cursor-only)"
python3 "$SCRIPT_DIR/cursor_work_bundle_transforms.py" "$ROOT" "$OUT"

echo "==> Overlaying work-bundle static files"
cp -R "$BUNDLE_SRC/." "$OUT/"

echo "==> Zipping"
mkdir -p "$ROOT/packaging/dist"
( cd "$ROOT/packaging/dist" && zip -rq "cursor-work-playbook.zip" "cursor-work-playbook" )

ls -lh "$ZIP"
echo "Done: $ZIP"
