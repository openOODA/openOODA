#!/usr/bin/env bash
# mcode3 verification sweep: lint + make verify + make test (x2 for determinism) + oohat cycle.
set -u
LOGDIR=/Projects/openOODA/openOODA/audits/logs
mkdir -p "$LOGDIR"
export OODA_NO_JAIL=1
export OODA_FS_READDIR=/Projects
export OODA_FS_WRITEDIR=/tmp
export OODA_COMPILER=/Projects/openOODA-core/oodac/bin/oodac.real
export OODAC_BIN=/Projects/openOODA-core/oodac/bin/oodac.real

REPOS="$*"
for r in $REPOS; do
  n=$(basename "$r")
  echo "######## $n ########"
  cd "$r" || { echo "cd failed"; continue; }

  echo "-- lint-oo-size"
  /home/ubermetroid/.local/bin/lint-oo-size "$r" > "$LOGDIR/mcode3-$n-lint.txt" 2>&1
  echo "   lint rc=$? :: $(grep -E 'files_with_size_violation|BIGFILE|MANYFN|LONGFN|DENSE' "$LOGDIR/mcode3-$n-lint.txt" | tr '\n' ' ')"

  rm -f .ooda-cache/check.stamp
  echo "-- make verify"
  make verify > "$LOGDIR/mcode3-$n-verify.txt" 2>&1
  vrc=$?
  echo "   verify rc=$vrc"
  [ $vrc -ne 0 ] && tail -15 "$LOGDIR/mcode3-$n-verify.txt"

  echo "-- make test (run 1)"
  make test > "$LOGDIR/mcode3-$n-test1.txt" 2>&1
  trc=$?
  echo "   test1 rc=$trc :: $(grep -E 'ALL TESTS PASSED|FAIL|assertions' "$LOGDIR/mcode3-$n-test1.txt" | tr '\n' ' ')"

  echo "-- make test (run 2, determinism)"
  make test > "$LOGDIR/mcode3-$n-test2.txt" 2>&1
  trc2=$?
  echo "   test2 rc=$trc2"
  if diff -q "$LOGDIR/mcode3-$n-test1.txt" "$LOGDIR/mcode3-$n-test2.txt" > /dev/null; then
    echo "   DETERMINISM: byte-identical"
  else
    echo "   DETERMINISM: DIFFERS"
    diff "$LOGDIR/mcode3-$n-test1.txt" "$LOGDIR/mcode3-$n-test2.txt" | head -20
  fi
  echo
done
