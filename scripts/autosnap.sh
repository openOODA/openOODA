#!/usr/bin/env bash
# autosnap.sh - Back up uncommitted work in every openOODA repo to Forgejo.
#
# For each dirty repo, build a snapshot commit from a temporary index (the
# working tree, the real index, and the checked-out branch are never touched)
# and push it to refs/heads/wip/autosnap-<host>. Re-running only pushes when
# the content changed. Repos locked to other servers are skipped.
set -u
host=$(hostname -s)
skip='/openOODA-core/(std|oodar|oodac)$|/openOODA-agents/oohat$'
for g in $(find /Projects/openOODA-* -maxdepth 2 -name .git -type d 2>/dev/null); do
  r=$(dirname "$g")
  [[ "$r" =~ $skip ]] && continue
  [ -z "$(git -C "$r" status --porcelain 2>/dev/null)" ] && continue
  tmp=$(mktemp)
  cp "$g/index" "$tmp" 2>/dev/null
  GIT_INDEX_FILE="$tmp" git -C "$r" add -A 2>/dev/null
  tree=$(GIT_INDEX_FILE="$tmp" git -C "$r" write-tree)
  rm -f "$tmp"
  ref="refs/heads/wip/autosnap-$host"
  prev=$(git -C "$r" ls-remote origin "$ref" 2>/dev/null | cut -f1)
  if [ -n "$prev" ] && [ "$(git -C "$r" rev-parse -q --verify "$prev^{tree}" 2>/dev/null)" = "$tree" ]; then
    echo "same  $r"; continue
  fi
  c=$(git -C "$r" commit-tree "$tree" -p HEAD -m "autosnap $host $(date -Is)")
  if git -C "$r" push -q origin "$c:$ref" -f 2>/dev/null; then echo "SNAP  $r -> $ref ${c:0:7}"; else echo "FAIL  $r"; fi
done
