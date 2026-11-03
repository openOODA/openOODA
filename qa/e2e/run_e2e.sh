#!/usr/bin/env bash
# ==============================================================================
# openOODA E2E Test Suite Launcher (Pure .oo)
# Usage:
#   bash openOODA/qa/e2e/run_e2e.sh
# ==============================================================================
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
POLYROOT="$(cd "$HERE/../../.." && pwd)"
OODAC="${OODA_COMPILER:-/Projects/openOODA-core/oodac/bin/oodac}"

export OODA_NO_JAIL=1
export OODA_FS_READDIR="/Projects:/var/lib/ooda-buildbox:/tmp"
export OODA_FS_WRITEDIR="/Projects:/tmp"
export OODA_COMPILER="${OODAC}"

cd "${POLYROOT}"
TMP_BIN="/tmp/ooda_e2e_runner_$$.bin"
trap 'rm -f "${TMP_BIN}"' EXIT
"${OODAC}" build "${HERE}/runner.oo" -o "${TMP_BIN}" >/dev/null
"${TMP_BIN}" "$@"
