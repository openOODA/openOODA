#!/bin/sh
# fleettick-parity.sh — cutover binary-parity check (RFC-0013 §4, binary-parity law).
# Rebuilds buildbox/fleettick/sweep_main.oo at the current checkout and compares
# its sha256 against the installed fleettick binary. Check-only: never installs,
# never enables the timer.
#
# Usage: ./fleettick-parity.sh [installed-path] [repo-root]
#   installed-path defaults to ~/.local/bin/fleettick
#   repo-root defaults to the checkout this script ships in
#   OODA_COMPILER env overrides the compiler (default: the fleet oodac.real path)
#
# Exit 0 = PARITY_OK, 1 = PARITY_FAIL, 2 = tool error.
set -eu

INST="${1:-$HOME/.local/bin/fleettick}"
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SRC="${2:-$(CDPATH= cd -- "$HERE/../../.." && pwd)}"
OODAC="${OODA_COMPILER:-/Projects/openOODA-core/oodac/bin/oodac.real}"

[ -f "$INST" ] || { echo "PARITY_ERR installed binary missing: $INST"; exit 2; }
[ -x "$OODAC" ] || { echo "PARITY_ERR compiler missing: $OODAC (set OODA_COMPILER)"; exit 2; }
[ -f "$SRC/buildbox/fleettick/sweep_main.oo" ] || { echo "PARITY_ERR not a fleettick repo: $SRC"; exit 2; }

OUT=$(mktemp /tmp/fleettick-parity.XXXXXX)
trap 'rm -f "$OUT"' EXIT

echo "parity: building $SRC/buildbox/fleettick/sweep_main.oo"
OODA_COMPILER="$OODAC" OODAC_BIN="$OODAC" OODA_NO_JAIL=1 \
    OO_LIST_AMBIENT_QUOTA=8589934592 "$OODAC" build -o "$OUT" "$SRC/buildbox/fleettick/sweep_main.oo" \
    || { echo "PARITY_ERR build failed"; exit 2; }

A=$(sha256sum "$INST" | cut -d' ' -f1)
B=$(sha256sum "$OUT" | cut -d' ' -f1)
if [ "$A" = "$B" ]; then
    echo "PARITY_OK $INST == fresh build ($A)"
    exit 0
fi
echo "PARITY_FAIL installed=$A built=$B"
echo "installed binary predates the current source — rebuild + reinstall at the pinned commit before cutover"
exit 1
