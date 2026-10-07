#!/bin/sh
# Install from a checkout or directly via curl | sh.
set -eu
case "${1:-}" in
  -h|--help)
    printf '%s\n' 'Usage: sh install.sh [TARGET_PROJECT]' 'Defaults to the current project. Downloads the official master archive when run via curl | sh.'
    exit 0 ;;
esac
[ "$#" -le 1 ] || { echo 'Usage: sh install.sh [TARGET_PROJECT]' >&2; exit 1; }
TARGET=${1:-.}
command -v python3 >/dev/null 2>&1 || { echo 'python3 is required' >&2; exit 1; }
# Only trust a source location when actually invoked as a script file.
if [ -f "$0" ]; then
  SOURCE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
  if [ -f "$SOURCE/scripts/install.py" ]; then
    exec sh "$SOURCE/scripts/inject.sh" "$TARGET"
  fi
fi
command -v curl >/dev/null 2>&1 || { echo 'curl is required' >&2; exit 1; }
command -v tar >/dev/null 2>&1 || { echo 'tar is required' >&2; exit 1; }
BASE=${TMPDIR:-/tmp}
[ ! -d /tmp/opencode ] || BASE=/tmp/opencode
TEMP=$(mktemp -d "$BASE/opencode-gen-install.XXXXXX")
trap 'rm -rf "$TEMP"' 0
trap 'exit 1' 1 2 15
curl -fsSL https://codeload.github.com/infinityplatformhub/opencode-gen/tar.gz/refs/heads/master -o "$TEMP/source.tar.gz"
tar -xzf "$TEMP/source.tar.gz" -C "$TEMP"
OPENCODE_GEN_EPHEMERAL_SOURCE=1 sh "$TEMP/opencode-gen-master/scripts/inject.sh" "$TARGET"
