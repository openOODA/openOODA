#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# openOODA/qa/test_cards.sh
# Empirical Stress Harness for the 8 canonical Quick Cards.
#
# The verbose .oot manuals (spec.oot, rules.oot, requirements.oot,
# roadmap.oot, rfcs/, practices/) were purged upstream and replaced by the
# compact Quick Card set: AGENTS.md plus the 8 `ooda <topic>` cards. This
# harness verifies the live card set instead of the deleted .oot corpus.
# It fails closed: every assertion must hold.
# ==============================================================================

ROOT="${1:-openOODA}"
FAILS=0

fail() { echo "FAIL: $1"; FAILS=$((FAILS + 1)); }
pass() { echo "  PASS: $1"; }

need() {
  # need <file> <fixed-string> <label>
  local f="$ROOT/$1" s="$2" label="$3"
  if [ ! -f "$f" ]; then fail "$1 missing"; return; fi
  if grep -qF -- "$s" "$f"; then pass "$label"; else fail "$1 lacks: $s"; fi
}

echo "=== Testing Quick Cards under: $ROOT ==="

# --- Test 1: the 8 cards exist, are titled canonically, and obey the page law ---
echo "Test 1 [Card Presence & Page Law]:"
CARDS=(ooda.md layers.md spec.md rules.md ui.md security.md privacy.md defense.md)
for c in "${CARDS[@]}"; do
  f="$ROOT/$c"
  if [ ! -f "$f" ]; then fail "missing card $c"; continue; fi
  n=$(wc -l < "$f")
  if [ "$n" -eq 0 ]; then fail "$c is empty"; continue; fi
  if [ "$n" -gt 256 ]; then fail "$c is $n lines (exceeds the 256 page law)"; continue; fi
  if ! head -1 "$f" | grep -q "^# $c "; then fail "$c has no canonical title line"; continue; fi
  pass "$c present and titled ($n lines)"
done

# --- Test 2: rules.md — the Power-of-2 Shape Ladder and the CLI laws ---
echo "Test 2 [rules.md Shape Ladder & CLI Laws]:"
need rules.md 'Power-of-2 Shape Ladder' 'ladder headline'
need rules.md '(`2^0`)' 'ladder rung 1'
need rules.md '(`2^3`)' 'ladder rung 8'
need rules.md '(`2^8`)' 'ladder rung 256'
need rules.md '`<binary> about`' 'about law'
need rules.md 'ootheme' 'theme law'
need rules.md '`--persona`' 'forbidden --persona flag'
need rules.md '`--mode`' 'forbidden --mode flag'
need rules.md '`--personas`' 'forbidden --personas flag'
need rules.md '`--unknown-flag-zzz`' 'unknown flag probe'
need rules.md 'exit `2`' 'exit 2 refusal law'

# --- Test 3: spec.md — the language laws the compiler enforces ---
echo "Test 3 [spec.md Language Laws]:"
need spec.md 'NO trailing comma' 'no trailing comma law'
need spec.md 'NO outer parentheses' 'no condition parentheses law'
need spec.md 'Relative string imports only' 'relative imports law'
need spec.md '4 header comment lines' '4-element header law'
need spec.md '`let mut' 'mutable binding law'

# --- Test 4: security.md — Zero Ambient Authority and the 32-capability lattice ---
echo "Test 4 [security.md Zero-Trust Lattice]:"
need security.md 'Zero Ambient Authority' 'zero ambient authority law'
need security.md 'CapReg64' 'CapReg64 register'
need security.md '`0:NetCap`' 'capability lane 0'
need security.md '`31:TpmCap`' 'capability lane 31'

# --- Test 5: ui.md — ootheme engine, overrides and graceful degradation ---
echo "Test 5 [ui.md Theme Engine]:"
need ui.md '`OODA_THEME=<name>`' 'OODA_THEME override'
need ui.md '`OODA_MODE=dark|light|auto`' 'OODA_MODE override'
need ui.md '`OODA_BORDER=round|sharp|double|ascii`' 'OODA_BORDER override'
need ui.md '`NO_COLOR=1`' 'NO_COLOR override'
need ui.md '24-bit TrueColor -> 256 -> 16 -> `NO_COLOR`' 'colour degradation chain'

# --- Test 6: privacy.md and defense.md carry their headline laws ---
echo "Test 6 [privacy.md & defense.md]:"
need privacy.md 'Zero-Telemetry' 'zero telemetry law'
need privacy.md 'RIGHT_ZERO_TELEMETRY' 'sealed privacy right'
need privacy.md 'ooredact' 'redaction engine'
need defense.md 'oodefense' 'active defense engine'
need defense.md 'oofirewall' 'firewall engine'

# --- Test 7: layers.md maps the 8 layers and layers.md/ooda.md front doors ---
echo "Test 7 [layers.md & ooda.md Front Doors]:"
for l in L0 L1 L2 L3 L4 L5 L6 L7; do
  if grep -q "\`$l\`" "$ROOT/layers.md"; then pass "layers.md maps $l"; else fail "layers.md misses $l"; fi
done
need ooda.md 'ooda about' 'about discovery front door'
need ooda.md '`--mode`/`--persona`' 'forbidden flag front door'

# --- Test 8: AGENTS.md front door names every card ---
echo "Test 8 [AGENTS.md Card Index]:"
for c in "${CARDS[@]}"; do
  if grep -q "$c" "$ROOT/AGENTS.md"; then pass "AGENTS.md names $c"; else fail "AGENTS.md misses $c"; fi
done

# --- Test 9: layers.md fleet census — 39 L3 tools, exact 10 L7 agents, 93/99 totals ---
echo "Test 9 [Fleet Census & Roster]:"
if grep -q '`39` Repos' "$ROOT/layers.md" && grep -q 'oosandbox' "$ROOT/layers.md"; then
  pass "layers.md L3 census is 39 with oosandbox"
else
  fail "layers.md L3 census missing 39/oosandbox"
fi
L7_LINE=$(grep 'L7`:' "$ROOT/layers.md" || true)
L7_OK=1
for r in oobench oocode ooconsensus oofalsify oogovern oohat ooloop oomemory ooquota ooswarm; do
  if ! grep -q "$r" <<< "$L7_LINE"; then L7_OK=0; fi
done
for stale in ooagent oocoder oorag omem ooeval ooevolve; do
  if grep -q "\`$stale\`" <<< "$L7_LINE"; then L7_OK=0; fi
done
if [ "$L7_OK" -eq 1 ]; then pass "layers.md L7 roster is the exact 10 on-disk repos"; else fail "layers.md L7 roster mismatch"; fi
if grep -q '`93` total product binaries' "$ROOT/layers.md" && grep -q '`99` total repos' "$ROOT/layers.md"; then
  pass "layers.md census reads 93 product + 6 governance = 99 repos"
else
  fail "layers.md census counts stale"
fi

echo "=============================================="
if [ "$FAILS" -ne 0 ]; then
  echo "RESULT: FAIL ($FAILS failed assertions)"
  exit 1
fi
echo "RESULT: PASS (all card assertions hold)"
