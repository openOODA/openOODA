#!/usr/bin/env bash
# Strict sequential double-run determinism check: compares the ASSERTION output only
# (build chatter is excluded because run 1 rebuilds and run 2 reuses the cached binary).
set -u
LOGDIR=/Projects/openOODA/openOODA/audits/logs
mkdir -p "$LOGDIR"
export OODA_NO_JAIL=1

REPOS="$*"
for r in $REPOS; do
  n=$(basename "$r")
  cd "$r" || continue
  b=$(git -C "$r" symbolic-ref --short HEAD)
  bin=$(grep -m1 '^BIN :=' Makefile | sed 's/^BIN :=[[:space:]]*//')
  tbin=$(grep -m1 '^TESTBIN :=' Makefile | sed 's/^TESTBIN :=[[:space:]]*//')
  echo "--- $n [$b] bin=$bin testbin=$tbin"
  for i in 1 2; do
    ./"$tbin" > "$LOGDIR/det-$n-$i.txt" 2>&1
    ./"$bin" --json > "$LOGDIR/det-$n-json-$i.txt" 2>&1
  done
  if cmp -s "$LOGDIR/det-$n-1.txt" "$LOGDIR/det-$n-2.txt"; then
    echo "    test-binary output: BYTE-IDENTICAL"
  else
    echo "    test-binary output: DIFFERS"; diff "$LOGDIR/det-$n-1.txt" "$LOGDIR/det-$n-2.txt" | head -10
  fi
  if cmp -s "$LOGDIR/det-$n-json-1.txt" "$LOGDIR/det-$n-json-2.txt"; then
    echo "    --json output:      BYTE-IDENTICAL"
  else
    echo "    --json output:      DIFFERS"; diff "$LOGDIR/det-$n-json-1.txt" "$LOGDIR/det-$n-json-2.txt" | head -10
  fi
done
