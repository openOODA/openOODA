#!/usr/bin/env python3
"""mcode-review 3 -- make the Makefile SRC list match the committed page set.

SRC is the declared source set: $(BIN) and $(TEST_BIN) depend on it, the
check stamp typechecks every page it names, and det builds the daemon twice
from it and compares the two binaries.

Two ways it drifts:

  * a page is committed but missing from SRC -- then make verify never
    typechecks it and det never covers it;
  * SRC names a page that no longer exists -- then the build fails with
    "No rule to make target" before anything is compiled.

This rewrites the SRC line so that it lists exactly the committed pages:
every page that exists is named, and every name that no longer exists is
dropped. Nothing else on the line is touched, so the assertion gate stays
whatever the tree's own tests say.
"""

import os
import re
import sys

REPOS = [
    "ooaid", "ooaudiod", "oodevd", "oodnsd", "oofs-ext4", "oofs-tmp",
    "oohealthd", "ooimage", "ooinit", "oologd", "oonetd", "oopolicyd",
    "oopowerd", "oorealm", "oosession",
]
ROOT = "/Projects/openOODA-OS"
SKIP = {".git", "bin", "dist", ".ooda-cache", "target", ".github"}


def pages_of(d):
    out = []
    for root, dirs, files in os.walk(d):
        dirs[:] = [x for x in dirs if x not in SKIP]
        for f in sorted(files):
            if f.endswith(".oo"):
                out.append(os.path.relpath(os.path.join(root, f), d))
    return sorted(out)


for repo in REPOS:
    d = os.path.join(ROOT, repo)
    mk = os.path.join(d, "Makefile")
    if not os.path.exists(mk):
        print(f"{repo}: no Makefile")
        continue
    text = open(mk).read()
    m = re.search(r"^SRC := (.*)$", text, re.M)
    if not m:
        print(f"{repo}: no SRC line")
        continue

    current = m.group(1).split()
    # Keep only names that exist on disk, then add every committed page.
    keep = [p for p in current if os.path.exists(os.path.join(d, p))]
    dropped = [p for p in current if p not in keep]
    committed = pages_of(d)
    missing = [p for p in committed if p not in keep]

    if not dropped and not missing:
        print(f"{repo}: SRC already matches the committed page set")
        continue

    new_src = " ".join(keep + missing)
    text = text[:m.start(1)] + new_src + text[m.end(1):]
    open(mk, "w").write(text)
    parts = []
    if dropped:
        parts.append("dropped stale " + " ".join(dropped))
    if missing:
        parts.append("added " + " ".join(missing))
    print(f"{repo}: " + "; ".join(parts))
