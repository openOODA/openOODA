#!/usr/bin/env bash
# # Red Team Continuous Adversarial Pre-Commit Verification Hook (shell)
#
# Logline: Run the 8 Red Team falsification gates fail-closed, then run the
# 9th structural-integrity gate that actually probes the source tree for the
# post-audit invariants. Each .oo test is built with `ooda build` and run
# directly from the produced .bin to bypass the `ooda run` toolchain's
# intermittent stdout-flush issue. A failure on any gate vetoes the hook.
#
# Beats:
#   1. OODA_REPO_ROOT for the repo root; no parent traversal.
#   2. Build + direct .bin run for each .oo gate (no ooda run).
#   3. Real 9th-gate source-lint probes (NOT synthetic ticks).
#   4. Native C Dudect (ns-resolution) gates the 9th gate empirically.
#   5. Master release seal (16 gates) is the structural release lock.

set -e
root="${OODA_REPO_ROOT:-.}"
if [ ! -d "$root/openOODA" ] || [ ! -d "$root/ooda" ]; then
    echo "[ROOT FAIL] missing openOODA or ooda"
    exit 1
fi
cd "$root"
OODA="$root/ooda/bin/ooda"
if [ ! -x "$OODA" ]; then
    echo "ERR redteam $OODA not executable"
    exit 1
fi
export OODA_FS_READDIR="$root"

# Build+run helper: bypasses `ooda run` toolchain by using build + direct .bin
build_run() {
    local src="$1"
    local out="$root/.ooda-cache/redteam/$(echo "$src" | tr '/' '_').bin"
    mkdir -p "$(dirname "$out")" "$root/.ooda-cache/runtime" "$root/.ooda-cache/run"
    "$OODA" build "$src" >/dev/null
    cp "$root/.ooda-cache/run/last.bin" "$out"
    "$out"
}

echo "=== Red Team pre-commit gates ==="

build_run ooda/qa/tests_challenger_1/test_c1_red1_red2_falsification.oo
(cd ooda && "$OODA" run scripts/hip_red1_keyword_trap_smoke.oo)
(cd ooda && "$OODA" run scripts/math_red1_heuristic_smoke.oo)
build_run ooda/qa/tests_challenger_2/test_c2_red3_red4_falsification.oo
(cd ooda && "$OODA" run scripts/std_red3_datapath_smoke.oo)
(cd ooda && "$OODA" run scripts/std_red4_hermetic_smoke.oo)
build_run ooda/qa/tests_challenger_3/test_c3_red5_temporal_saboteur.oo
build_run ooda/qa/tests_challenger_3/test_c3_red6_drag_assassin.oo
build_run ooda/qa/tests_challenger_4/test_c4_red7_semantic_subverter.oo

echo "=== 9th Gate: Structural Integrity (real probes) ==="
build_run ooda/qa/prove/simd_codegen_probe.oo
build_run ooda/qa/prove/ct_primitives_smoke.oo
build_run ooda/qa/prove/dudect_real.oo
build_run ooda/qa/prove/dudect_fraud_detector_smoke.oo
build_run ooda/qa/prove/live_ram_rasp_smoke.oo

echo "--- 9th Gate, sub-test: native C Dudect (ns-resolution CLOCK_MONOTONIC) ---"
gcc -O2 -o /tmp/dudect_c_native "$root/ooda/runtime/dudect_c_native.c" -lm && /tmp/dudect_c_native

build_run ooda/qa/prove/master_release_verifier.oo

echo "redteam_hook: OK"
