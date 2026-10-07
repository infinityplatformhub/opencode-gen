#!/bin/sh
# Install from this checkout; no remote origin is required.
set -eu
case "${1:-}" in
  -h|--help)
    printf '%s\n' 'Usage: sh install.sh TARGET_PROJECT' 'Install project-local OpenCode Gen from this checkout.'
    exit 0 ;;
esac
[ "$#" -eq 1 ] || { echo 'Usage: sh install.sh TARGET_PROJECT' >&2; exit 1; }
SOURCE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec sh "$SOURCE/scripts/inject.sh" "$1"
