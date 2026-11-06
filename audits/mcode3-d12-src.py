#!/usr/bin/env python3
"""mcode-review 3 -- D12: repair the declared source set (Makefile SRC).

Each L2 Makefile declares the set of pages that make builds and typechecks:

    SRC := main.oo anchor.oo core/... tests/...
    $(BIN): $(SRC) $(CHECK_STAMP)
    $(TEST_BIN): $(SRC) $(CHECK_STAMP)
    det: $(SRC)

Pages committed to a repository but absent from SRC are therefore never
typechecked by `make verify` and never covered by the deterministic-build
comparison in `make det`. The concurrently pushed feature commits added
one page per repository without adding it to SRC, so the declared source
set drifted from the committed page set.

This adds every committed page that SRC omits. The pages were typechecked
standalone first: all of them pass `oodac check`. The assertion count is
untouched -- SRC is a dependency list, not an assertion.
"""

import os
import re
import subprocess
import sys

REPOS = [
    "ooaid", "ooaudiod", "oodevd", "oodnsd", "oofs-ext4", "oofs-tmp",
    "oohealthd", "ooimage", "ooinit", "oologd", "oonetd", "oopolicyd",
    "oopowerd", "oorealm", "oosession",
]
ROOT = "/Projects/openOODA-OS"
SKIP_DIRS = {".git", "bin", "dist", ".ooda-cache", "target", ".github", "tests"}

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
    src = m.group(1)
    present = set(src.split())

    # Every committed page outside the test tree.
    pages = []
    for root, dirs, files in os.walk(d):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in sorted(files):
            if f.endswith(".oo"):
                pages.append(os.path.relpath(os.path.join(root, f), d))

    missing = sorted(p for p in pages if p not in present)
    if not missing:
        print(f"{repo}: SRC complete")
        continue

    new_src = src + " " + " ".join(missing)
    text = text[:m.start(1)] + new_src + text[m.end(1):]
    open(mk, "w").write(text)
    print(f"{repo}: added {len(missing)} -> {' '.join(missing)}")
