#!/usr/bin/env bash
# mcode-review 3 -- push each repository as soon as its verification entry
# completes in the sweep log, so the window in which a concurrently pushed
# remote commit can diverge from the verified tree stays as short as possible.
#
# A repository is pushed when the sweep log shows its header and a
# "TEST RUN2: PASS" line. A rejected push is recorded for a later rebase.
#
# Usage: mcode3-push-on-sweep.sh <sweep-log> <repo> [<repo> ...]

LOG="$1"; shift
OUT=/Projects/openOODA/openOODA/audits/mcode3-push.log
: > "$OUT"

for repo in "$@"; do
  name=$(basename "$repo")
  # Wait for this repository's sweep entry.
  for _ in $(seq 1 720); do
    entry=$(awk -v n="/$name =====" '
      index($0, n) { inb=1; buf=""; next }
      /^===== /{ inb=0 }
      inb { buf = buf $0 "\n" }
      END { printf "%s", buf }' "$LOG")
    if echo "$entry" | grep -q "TEST RUN2: PASS"; then
      break
    fi
    sleep 10
  done

  br=$(git -C "$repo" symbolic-ref --short HEAD)
  git -C "$repo" fetch origin "$br" -q 2>/dev/null
  if git -C "$repo" rev-list --count origin/$br..HEAD | grep -q '^0$'; then
    echo "$name: already on origin" | tee -a "$OUT"
    continue
  fi
  res=$(git -C "$repo" push origin "$br" 2>&1)
  if echo "$res" | grep -q "non-fast-forward"; then
    echo "$name: REJECTED (remote moved) -- needs rebase" | tee -a "$OUT"
  else
    echo "$name: pushed ($br) $(git -C "$repo" rev-parse --short HEAD)" | tee -a "$OUT"
  fi
done
echo "PUSH PASS DONE" | tee -a "$OUT"
