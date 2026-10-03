#!/usr/bin/env bash
# ==============================================================================
# openOODA E2E Test Suite Launcher
# Usage:
#   bash openOODA/qa/e2e/run_e2e.sh [--all] [--tier 1|2|3|4] [--domain R1..R5]
# ==============================================================================
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
POLYROOT="$(cd "$HERE/../../.." && pwd)"

export PYTHONPATH="${POLYROOT}:${PYTHONPATH:-}"
export OODA_POLYROOT="${POLYROOT}"

exec python3 "${HERE}/runner.py" "$@"
