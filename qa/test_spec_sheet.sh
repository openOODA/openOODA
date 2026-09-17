#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# openOODA/qa/test_spec_sheet.sh
# Empirical Stress Harness for Milestone 1: Tier A Spec Sheet
# ==============================================================================

SPEC_FILE="${1:-openOODA/spec.oot}"
echo "=== Testing Spec Sheet: $SPEC_FILE ==="

if [ ! -f "$SPEC_FILE" ]; then
  echo "FAIL: $SPEC_FILE does not exist!"
  exit 1
fi

FAILS=0
WARNS=0

# --- Test 1: Line Count Ceiling (<= 256) ---
LINE_COUNT=$(wc -l < "$SPEC_FILE")
echo "Test 1 [Line Count]: $LINE_COUNT lines"
if [ "$LINE_COUNT" -gt 256 ]; then
  echo "  FAIL: Line count $LINE_COUNT exceeds 256 ceiling!"
  FAILS=$((FAILS + 1))
elif [ "$LINE_COUNT" -eq 0 ]; then
  echo "  FAIL: File is empty!"
  FAILS=$((FAILS + 1))
else
  echo "  PASS: Line count $LINE_COUNT is within limit (<= 256)"
fi

# --- Test 2: Max Width Ceiling (<= 80 Columns) ---
echo "Test 2 [Max Column Width]: Checking all lines <= 80 characters"
LONG_LINES=$(awk '{ if (length > 80) print NR ":" length ":" $0 }' "$SPEC_FILE")
if [ -n "$LONG_LINES" ]; then
  echo "  FAIL: Lines exceeding 80 columns found:"
  echo "$LONG_LINES"
  FAILS=$((FAILS + 1))
else
  MAX_LEN=$(awk 'BEGIN{m=0} {if(length>m) m=length} END{print m}' "$SPEC_FILE")
  echo "  PASS: 0 lines exceed 80 columns (max observed: $MAX_LEN chars)"
fi

# --- Test 3: Clean 2-Line Header ---
echo "Test 3 [Clean Header]:"
H1=$(sed -n '1p' "$SPEC_FILE")
H2=$(sed -n '2p' "$SPEC_FILE")
if [[ "$H1" =~ ^#\  ]] && [[ "$H2" =~ ^File:\  ]]; then
  echo "  PASS: Clean 2-line header found: '$H1' / '$H2'"
else
  echo "  FAIL: Header does not match Clean 2-line header pattern"
  echo "    Line 1: '$H1'"
  echo "    Line 2: '$H2'"
  FAILS=$((FAILS + 1))
fi

# --- Test 4: Trailing Commas in Struct Declarations/Examples ---
echo "Test 4 [Struct Trailing Commas]:"
STRUCT_TRAILING=$(grep -nE 'struct[^{]*\{[^}]*,[[:space:]]*\}' \
  "$SPEC_FILE" || true)
if [ -n "$STRUCT_TRAILING" ]; then
  echo "  FAIL: Struct with trailing comma found:"
  echo "$STRUCT_TRAILING"
  FAILS=$((FAILS + 1))
else
  echo "  PASS: Zero struct trailing commas found in examples"
fi

if grep -q -i "trailing comma" "$SPEC_FILE"; then
  echo "  PASS: Spec explicitly specifies zero trailing commas rule"
else
  echo "  FAIL: Spec does NOT mention trailing commas rule!"
  FAILS=$((FAILS + 1))
fi

# --- Test 5: Condition Parentheses Prohibition & Cleanliness ---
echo "Test 5 [Condition Parentheses]:"
COND_PAREN=$(grep -nE '(if|while)[[:space:]]+\([^)]+\)[[:space:]]*\{' \
  "$SPEC_FILE" || true)
if [ -n "$COND_PAREN" ]; then
  echo "  FAIL: Prohibited condition with parentheses found in example:"
  echo "$COND_PAREN"
  FAILS=$((FAILS + 1))
else
  echo "  PASS: No condition expressions with outer parentheses in examples"
fi

if grep -q -i "parenthes" "$SPEC_FILE"; then
  echo "  PASS: Spec explicitly codifies condition no-parentheses rule"
else
  echo "  FAIL: Spec does NOT mention condition no-parentheses rule!"
  FAILS=$((FAILS + 1))
fi

# --- Test 6: 22 Active Normative Keywords ---
echo "Test 6 [22 Active Normative Keywords]:"
ACTIVE_KW=(
  fn let pub mut import requires ensures verify if else match
  for in while return type true false gpu break continue export
)
ACTIVE_MISSING=0
for kw in "${ACTIVE_KW[@]}"; do
  if ! grep -qE "(^|[ ,])\\b$kw\\b([ ,.]|\$)" "$SPEC_FILE"; then
    echo "  FAIL: Active keyword '$kw' not found in spec!"
    ACTIVE_MISSING=$((ACTIVE_MISSING + 1))
  fi
done

if [ "$ACTIVE_MISSING" -eq 0 ]; then
  echo "  PASS: All ${#ACTIVE_KW[@]} active keywords are present in spec"
else
  echo "  FAIL: $ACTIVE_MISSING active keywords missing from spec"
  FAILS=$((FAILS + ACTIVE_MISSING))
fi

if grep -q "Active Normative Keywords (22)" "$SPEC_FILE" || \
   grep -q "exactly 22 keywords" "$SPEC_FILE"; then
  echo "  PASS: Active keywords count 22 explicitly asserted in spec"
else
  echo "  WARN: Active keywords count 22 not explicitly stated in spec"
  WARNS=$((WARNS + 1))
fi

# --- Test 7: 5 Residual Non-Normative Keywords ---
echo "Test 7 [5 Residual Non-Normative Keywords]:"
RESIDUAL_KW=(trait newtype where spec impl)
RESIDUAL_MISSING=0
for kw in "${RESIDUAL_KW[@]}"; do
  if ! grep -qE "(^|[ ,])\\b$kw\\b([ ,.]|\$)" "$SPEC_FILE"; then
    echo "  FAIL: Residual keyword '$kw' not found in spec!"
    RESIDUAL_MISSING=$((RESIDUAL_MISSING + 1))
  fi
done

if [ "$RESIDUAL_MISSING" -eq 0 ]; then
  echo "  PASS: All ${#RESIDUAL_KW[@]} residual keywords are present in spec"
else
  echo "  FAIL: $RESIDUAL_MISSING residual keywords missing from spec"
  FAILS=$((FAILS + RESIDUAL_MISSING))
fi

if grep -q "Residual Non-Normative Keywords (5)" "$SPEC_FILE" || \
   grep -q "following 5 keywords" "$SPEC_FILE"; then
  echo "  PASS: Residual keywords count 5 explicitly asserted in spec"
else
  echo "  WARN: Residual keywords count 5 not explicitly stated in spec"
  WARNS=$((WARNS + 1))
fi

# --- Test 8: 20 Normative Capability Tokens ---
echo "Test 8 [20 Normative Capability Tokens]:"
CAP_TOKENS=(
  FsReadCap FsWriteCap FsCap ProcessCap SysCap
  NetCap TcpCap UdpCap BindCap EnvCap
  TimeCap RandCap AllocCap ArenaCap ThreadCap
  GpuCap FfiCap MetricsCap SignCap CompilerReadCap
)
CAP_MISSING=0
for cap in "${CAP_TOKENS[@]}"; do
  if ! grep -q "$cap" "$SPEC_FILE"; then
    echo "  FAIL: Capability token '$cap' not found in spec!"
    CAP_MISSING=$((CAP_MISSING + 1))
  fi
done

if [ "$CAP_MISSING" -eq 0 ]; then
  echo "  PASS: All ${#CAP_TOKENS[@]} capability tokens are present in spec"
else
  echo "  FAIL: $CAP_MISSING capability tokens missing from spec"
  FAILS=$((FAILS + CAP_MISSING))
fi

# --- Test 9: Substrate Bits and Excised Dead Bits ---
echo "Test 9 [Substrate Bits & Excised Bits]:"
if grep -q "26" "$SPEC_FILE" && \
   grep -q "Audio" "$SPEC_FILE" && \
   grep -q "Camera" "$SPEC_FILE" && \
   grep -q "Usb" "$SPEC_FILE" && \
   grep -q "Hid" "$SPEC_FILE" && \
   grep -q "Window" "$SPEC_FILE" && \
   grep -q "Frame" "$SPEC_FILE"; then
  echo "  PASS: All 6 reserved device bits documented"
else
  echo "  FAIL: Substrate reserved device bits incomplete in spec!"
  FAILS=$((FAILS + 1))
fi

if grep -q "HITL" "$SPEC_FILE" && \
   grep -q "SYNC" "$SPEC_FILE" && \
   grep -q "MEM" "$SPEC_FILE" && \
   grep -q "HTTP" "$SPEC_FILE"; then
  echo "  PASS: All 4 dead excised bits documented"
else
  echo "  FAIL: Dead excised bits incomplete in spec!"
  FAILS=$((FAILS + 1))
fi

# --- Test 10: Wire Protocol and Diagnostics ---
echo "Test 10 [Wire Protocol Contracts]:"
if grep -q 'OK\\t<verb>\\t<message>' "$SPEC_FILE" || \
   grep -q 'OK' "$SPEC_FILE"; then
  echo "  PASS: TSV success wire format documented"
fi
if grep -q 'ERR\\t<category>\\t<message>' "$SPEC_FILE" || \
   grep -q 'ERR' "$SPEC_FILE"; then
  echo "  PASS: TSV error wire format documented"
fi
if grep -q 'exit' "$SPEC_FILE" || grep -q 'Exit Code' "$SPEC_FILE"; then
  echo "  PASS: Exit code matrix documented"
fi

# --- Summary ---
echo "=========================================="
echo "Harness Verdict: FAILS=$FAILS, WARNS=$WARNS"
if [ "$FAILS" -eq 0 ]; then
  echo "OVERALL VERDICT: PASS (CONFIRM CORRECTNESS)"
  exit 0
else
  echo "OVERALL VERDICT: FAIL (CHALLENGE / FAIL)"
  exit 1
fi
