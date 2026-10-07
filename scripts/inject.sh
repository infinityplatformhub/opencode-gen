#!/bin/sh
set -eu
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SOURCE=$(dirname "$SCRIPT_DIR")
mkdir -p "${1:-.}"
TARGET=$(CDPATH= cd -- "${1:-.}" && pwd)
if [ "$SOURCE" = "$TARGET" ]; then
  echo "Choose a target project other than the framework checkout." >&2
  exit 1
fi
command -v python3 >/dev/null 2>&1 || { echo "python3 is required" >&2; exit 1; }
exec python3 "$SCRIPT_DIR/install.py" "$SOURCE" "$TARGET"
