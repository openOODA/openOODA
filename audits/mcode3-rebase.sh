#!/usr/bin/env bash
# mcode-review 3 -- rebase the review commits onto the concurrently-pushed
# remote head, keeping the canonical implementation.
#
# For every conflicted file the review commit's version wins, because the
# review commit is the one that:
#   * drops the copied 64-bit register in favour of std/sec/capreg.oo,
#   * keeps a fail-closed range-validating wrapper,
#   * runs the canonical 4-phase OODA turn over the 32-capability register,
#   * binds the live gate to std/sec/quorum.oo and std/sec/delegate.oo.
#
# The concurrently pushed commits keep everything the review commit did not
# touch (theme pages, --tui/theme wiring, unrelated platform features).
#
# After each conflict resolution the merged imports are de-duplicated,
# because a clean auto-merge of "add import X" on both sides leaves two
# copies and the compiler rejects the duplicate.
#
# Usage: mcode3-rebase.sh <repo-dir> [<repo-dir> ...]

LOG=/Projects/openOODA/openOODA/audits/mcode3-rebase.log
: > "$LOG"

for repo in "$@"; do
  [ -d "$repo/.git" ] || continue
  br=$(git -C "$repo" symbolic-ref --short HEAD)
  echo "===== $repo ($br) =====" | tee -a "$LOG"

  git -C "$repo" fetch origin "$br" -q 2>/dev/null
  before=$(git -C "$repo" rev-parse HEAD)

  # Loop: a repo can have more than one commit to replay.
  step=0
  while true; do
    step=$((step + 1))
    if [ $step -gt 6 ]; then echo "  ABORT: too many rebase steps" | tee -a "$LOG"; break; fi

    out=$(git -C "$repo" rebase origin/"$br" 2>&1)
    rc=$?
    if [ $rc -eq 0 ]; then
      echo "  rebased cleanly" | tee -a "$LOG"
      break
    fi
    if ! git -C "$repo" rev-parse --verify REBASE_HEAD >/dev/null 2>&1; then
      echo "  REBASE ERROR (not a conflict):" | tee -a "$LOG"
      echo "$out" | tail -5 | tee -a "$LOG"
      break
    fi

    # Collect the conflicted paths.
    conflicted=$(git -C "$repo" diff --name-only --diff-filter=U)
    for f in $conflicted; do
      echo "  conflict: $f -> review version" | tee -a "$LOG"
      git -C "$repo" checkout --theirs -- "$f"
    done

    # De-duplicate imports in every file the replay touched.
    for f in $(git -C "$repo" diff --cached --name-only); do
      [ -f "$repo/$f" ] || continue
      d=$(grep -E '^import ' "$repo/$f" 2>/dev/null | sort | uniq -d)
      if [ -n "$d" ]; then
        echo "  dedup imports: $f ($d)" | tee -a "$LOG"
        python3 - "$repo/$f" <<'PY'
import sys
p = sys.argv[1]
lines = open(p).read().split("\n")
out, seen = [], set()
for ln in lines:
    if ln.startswith("import "):
        if ln in seen:
            continue
        seen.add(ln)
    out.append(ln)
open(p, "w").write("\n".join(out))
PY
      fi
    done

    git -C "$repo" add -A >/dev/null 2>&1
    GIT_EDITOR=true git -C "$repo" rebase --continue >/dev/null 2>&1
  done

  after=$(git -C "$repo" rev-parse HEAD)
  if [ "$before" = "$after" ]; then
    echo "  NO CHANGE (already up to date or rebase skipped)" | tee -a "$LOG"
  else
    echo "  new head: $(git -C "$repo" log --oneline -1)" | tee -a "$LOG"
  fi
  git -C "$repo" status --porcelain | head -5 | tee -a "$LOG"
  echo "" | tee -a "$LOG"
done
echo "REBASE PASS DONE" | tee -a "$LOG"
