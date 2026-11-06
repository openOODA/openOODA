#!/usr/bin/env bash
# mcode-review 3 -- rebase a repository onto the current remote head and
# report whether the resulting tree differs from the tree that was verified.
#
# If the tree is identical, the earlier verification still holds and the
# repository can be pushed without re-running the gate. If the tree
# changed, the repository must go back through the verification sweep.
#
# Usage: mcode3-rebase-and-check.sh <repo-dir>

set -u
repo="$1"
br=$(git -C "$repo" symbolic-ref --short HEAD)
tree_before=$(git -C "$repo" rev-parse HEAD^{tree})

git -C "$repo" fetch origin "$br" -q 2>/dev/null
behind=$(git -C "$repo" rev-list --count HEAD..origin/$br)
if [ "$behind" = "0" ]; then
  echo "$repo: up to date with origin/$br"
  exit 0
fi

git -C "$repo" rebase origin/"$br" >/tmp/mc3_rebase.$$ 2>&1
if [ $? -ne 0 ]; then
  echo "$repo: REBASE CONFLICT -- needs manual resolution"
  git -C "$repo" status --porcelain | head -10
  exit 1
fi

tree_after=$(git -C "$repo" rev-parse HEAD^{tree})
if [ "$tree_before" = "$tree_after" ]; then
  echo "$repo: rebased, TREE UNCHANGED -- verification still holds"
else
  echo "$repo: rebased, TREE CHANGED -- must re-verify"
  git -C "$repo" diff --stat "$tree_before" "$tree_after" | tail -15
fi
rm -f /tmp/mc3_rebase.$$
