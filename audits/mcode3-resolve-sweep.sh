#!/usr/bin/env bash
# mcode-review 3 — FINAL independent re-verification sweep (v4).
#
# Per repository:
#   1. lint-oo-size violations summary      (Axis 1, shape ladder)
#   2. make verify                          (Axis 2, repo gates)
#   3. make test, twice, sequentially       (Axis 2, double-run determinism)
#   4. the two runs are compared after the
#      make build echo is filtered out, so
#      the comparison is over test output
#      only, not over "did make rebuild".
#
# Usage: mcode3-verify-sweep-v4.sh <repo> [<repo> ...]

REPOS=("$@")
OUT=/Projects/openOODA/openOODA/audits/mcode3-resolve-sweep.log
: > "$OUT"

export OODA_NO_JAIL=1
export OODA_FS_READDIR=/Projects:/proc:/sys
export OODA_COMPILER=/Projects/openOODA-core/oodac/bin/oodac
export OODAC_BIN=/Projects/openOODA-core/oodac/bin/oodac

# Strip the make build echo: the compiler command line, the compiler's own
# OK markers, and make's "built <target>" line. Everything else is test
# output and must be identical between the two runs.
strip_build_echo() {
  grep -vE '^(OO_LIST_AMBIENT_QUOTA=|OK_PURE_NATIVE$|OK[[:space:]]+build[[:space:]]|built[[:space:]])' "$1"
}

assert_count() {
  grep -oE "PASS: [0-9]+(/[0-9]+)? assertions" "$1" | tail -1
  grep -oE "PASS: test suite \([0-9]+ assertions\)" "$1" | tail -1
  grep -oE "ALL TESTS PASSED" "$1" | tail -1
}

for repo in "${REPOS[@]}"; do
  [ -d "$repo" ] || continue
  echo "===== $repo =====" | tee -a "$OUT"

  /home/ubermetroid/.local/bin/lint-oo-size "$repo" 2>&1 \
    | grep -E '^# (violations|files_scanned):' | tee -a "$OUT"

  cd "$repo" || continue
  rm -f .ooda-cache/check.stamp

  if make verify >/tmp/mc4_v.$$ 2>&1; then
    echo "VERIFY: PASS" | tee -a "$OUT"
  else
    echo "VERIFY: FAIL" | tee -a "$OUT"
    tail -25 /tmp/mc4_v.$$ | tee -a "$OUT"
    rm -f /tmp/mc4_v.$$
    continue
  fi
  rm -f /tmp/mc4_v.$$

  if make test >/tmp/mc4_r1.$$ 2>&1; then
    echo "TEST RUN1: PASS  [$(assert_count /tmp/mc4_r1.$$ | tr '\n' ' ')]" | tee -a "$OUT"
  else
    echo "TEST RUN1: FAIL" | tee -a "$OUT"
    tail -25 /tmp/mc4_r1.$$ | tee -a "$OUT"
    rm -f /tmp/mc4_r1.$$
    continue
  fi

  if make test >/tmp/mc4_r2.$$ 2>&1; then
    echo "TEST RUN2: PASS  [$(assert_count /tmp/mc4_r2.$$ | tr '\n' ' ')]" | tee -a "$OUT"
  else
    echo "TEST RUN2: FAIL" | tee -a "$OUT"
    tail -25 /tmp/mc4_r2.$$ | tee -a "$OUT"
    rm -f /tmp/mc4_r2.$$ /tmp/mc4_r1.$$
    continue
  fi

  strip_build_echo /tmp/mc4_r1.$$ > /tmp/mc4_s1.$$
  strip_build_echo /tmp/mc4_r2.$$ > /tmp/mc4_s2.$$
  if cmp -s /tmp/mc4_s1.$$ /tmp/mc4_s2.$$; then
    echo "DETERMINISM: Run_1 == Run_2 (test output byte-identical)" | tee -a "$OUT"
  else
    echo "DETERMINISM: Run_1 != Run_2 -- DIFF:" | tee -a "$OUT"
    diff /tmp/mc4_s1.$$ /tmp/mc4_s2.$$ | head -20 | tee -a "$OUT"
  fi
  rm -f /tmp/mc4_r1.$$ /tmp/mc4_r2.$$ /tmp/mc4_s1.$$ /tmp/mc4_s2.$$
  echo "" | tee -a "$OUT"
done
echo "FINAL SWEEP DONE" | tee -a "$OUT"
