#!/usr/bin/env bash
# # Red Team Continuous Adversarial Pre-Commit Verification Hook
#
# Logline: Run the 8 Red Team falsification gates fail-closed, then run the
# 9th structural-integrity gate (5 real probes) that actually probes the
# post-audit invariants:
#   1. simd_codegen_probe        — 15 source-lint invariants
#   2. ct_primitives_smoke      — bit-exact truth table
#   3. dudect_real              — .oo-level Dudect with now_ms timing
#   4. dudect_c_native.c        — native C Dudect with CLOCK_MONOTONIC ns
#   5. master_release_verifier  — 13-gate on-disk audit
#
# The dudect fraud detector in std/sec/ct/ct_dudect.oo now fails closed on
# any synthetic-tick pattern. The red8 sub-test has been retired; the
# real constant-time property is verified by probes 3 and 4 above.
#
# Setup: Reads OODA_REPO_ROOT, defaults to /home/jeryd/Projects/openOODA.

set +e  # explicit exit codes; do not abort on first sub-test failure

root="${OODA_REPO_ROOT:-/home/jeryd/Projects/openOODA}"
if [ ! -d "$root/openOODA" ] || [ ! -d "$root/ooda" ]; then
    echo "[ROOT FAIL] missing openOODA or ooda under $root"
    exit 1
fi
cd "$root"
OODA="$root/ooda/bin/ooda"
if [ ! -x "$OODA" ]; then
    echo "ERR	redteam	$OODA not executable"
    exit 1
fi
export OODA_FS_READDIR="$root"

overall_status=0

run_test() {
    local desc="$1"
    local path="$2"
    echo "  $desc..."
    if "$OODA" run "$path" > /tmp/redteam_gate_out.txt 2>&1; then
        cat /tmp/redteam_gate_out.txt
        echo "  [PASS] $desc"
    else
        local rc=$?
        cat /tmp/redteam_gate_out.txt
        echo "  [FAIL] $desc (exit $rc)"
        overall_status=1
    fi
    rm -f /tmp/redteam_gate_out.txt
}

run_subshell_test() {
    local desc="$1"
    local path="$2"
    echo "  $desc..."
    if (cd "$root/ooda" && "$OODA" run "$path") > /tmp/redteam_gate_out.txt 2>&1; then
        cat /tmp/redteam_gate_out.txt
        echo "  [PASS] $desc"
    else
        local rc=$?
        cat /tmp/redteam_gate_out.txt
        echo "  [FAIL] $desc (exit $rc)"
        overall_status=1
    fi
    rm -f /tmp/redteam_gate_out.txt
}

echo "=== Red Team pre-commit gates ==="
run_test        "Red 1 & 2"                  "ooda/qa/tests_challenger_1/test_c1_red1_red2_falsification.oo"
run_subshell_test "hip_red1"                 "scripts/hip_red1_keyword_trap_smoke.oo"
run_subshell_test "math_red1"                 "scripts/math_red1_heuristic_smoke.oo"
run_test        "Red 3 & 4"                  "ooda/qa/tests_challenger_2/test_c2_red3_red4_falsification.oo"
run_subshell_test "std_red3"                  "scripts/std_red3_datapath_smoke.oo"
run_subshell_test "std_red4"                  "scripts/std_red4_hermetic_smoke.oo"
run_test        "Red 5 Temporal Saboteur"    "ooda/qa/tests_challenger_3/test_c3_red5_temporal_saboteur.oo"
run_test        "Red 6 Drag Assassin"         "ooda/qa/tests_challenger_3/test_c3_red6_drag_assassin.oo"
run_test        "Red 7 Semantic Subverter"   "ooda/qa/tests_challenger_4/test_c4_red7_semantic_subverter.oo"
# Red 8 retired: synthetic-tick Dudect detected by fraud detector
# in std/sec/ct/ct_dudect.oo (dudect_evaluate). Real constant-time
# is verified by 9th-gate probes 3 and 4 below.

echo ""
echo "=== 9th Gate: Structural Integrity (real probes) ==="
run_test        "simd_codegen_probe (15 source-lint invariants)" \
                                            "ooda/qa/prove/simd_codegen_probe.oo"
run_test        "ct_primitives_smoke (bit-exact truth table)" \
                                            "ooda/qa/prove/ct_primitives_smoke.oo"
run_test        "dudect_real (.oo-level now_ms timing)" \
                                            "ooda/qa/prove/dudect_real.oo"

echo "  --- 9th Gate, sub-test: native C Dudect (ns-resolution CLOCK_MONOTONIC) ---"
if gcc -O2 -o /tmp/dudect_c_native "$root/ooda/runtime/dudect_c_native.c" -lm > /tmp/gcc_out.txt 2>&1; then
    if /tmp/dudect_c_native > /tmp/dcn_out.txt 2>&1; then
        cat /tmp/dcn_out.txt
        echo "  [PASS] native C Dudect"
    else
        cat /tmp/dcn_out.txt
        echo "  [FAIL] native C Dudect (runtime)"
        overall_status=1
    fi
else
    cat /tmp/gcc_out.txt
    echo "  [FAIL] native C Dudect (compile)"
    overall_status=1
fi
rm -f /tmp/gcc_out.txt /tmp/dcn_out.txt /tmp/dudect_c_native

run_test        "master_release_verifier (13-gate on-disk audit)" \
                                            "ooda/qa/prove/master_release_verifier.oo"

echo ""
if [ $overall_status -eq 0 ]; then
    echo "redteam_hook: OK"
    exit 0
else
    echo "redteam_hook: VETO"
    exit 1
fi
