#!/bin/sh
# POSIX sh only — no bash features
# Copy local skill directories from another framework checkout.
# External pinned skills are maintained through /opencode-gen-sync-skills.
set -eu

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
FRAMEWORK_DIR="$(dirname "$SCRIPT_DIR")"
SOURCE="${1:-$FRAMEWORK_DIR}"

echo "Updating skills from: $SOURCE"

LIBRARY="$SOURCE/skills-library"

if [ ! -d "$LIBRARY" ]; then
  echo "Error: skills-library not found at $LIBRARY"
  echo "Usage: $0 [path-to-framework-repo]"
  exit 1
fi

if [ "$(CDPATH= cd -- "$LIBRARY" && pwd)" = "$(CDPATH= cd -- "$FRAMEWORK_DIR/skills-library" && pwd)" ]; then
  echo "Source is already this library; use /opencode-gen-sync-skills for upstream updates."
  exit 0
fi

UPDATED=0
SKIPPED=0

for skill_dir in "$LIBRARY"/*/; do
  skill_name="$(basename "$skill_dir")"

  # Skip _index.json (it's a file, not a dir)
  [ -d "$skill_dir" ] || continue

  src="$skill_dir/SKILL.md"
  dst="$FRAMEWORK_DIR/skills-library/$skill_name/SKILL.md"

  if [ ! -f "$src" ]; then
    continue
  fi

  if [ -f "$dst" ]; then
    # Compare files — update if different
    if ! cmp -s "$src" "$dst"; then
      cp -R "$skill_dir/." "$(dirname "$dst")/"
      echo "  Updated: $skill_name"
      UPDATED=$((UPDATED + 1))
    else
      # References can change even when SKILL.md does not.
      cp -R "$skill_dir/." "$(dirname "$dst")/"
      SKIPPED=$((SKIPPED + 1))
    fi
  else
    # New skill — copy
    mkdir -p "$FRAMEWORK_DIR/skills-library/$skill_name"
    cp -R "$skill_dir/." "$(dirname "$dst")/"
    echo "  Added: $skill_name"
    UPDATED=$((UPDATED + 1))
  fi
done

# Update _index.json if changed
if [ -f "$LIBRARY/_index.json" ]; then
  if ! cmp -s "$LIBRARY/_index.json" "$FRAMEWORK_DIR/skills-library/_index.json"; then
    cp "$LIBRARY/_index.json" "$FRAMEWORK_DIR/skills-library/_index.json"
    echo "  Updated: _index.json"
  fi
fi

echo ""
echo "Done. Updated: $UPDATED, Up to date: $SKIPPED"
