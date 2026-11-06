#!/usr/bin/env python3
"""Audit .oo import resolution using oodac's resolve_import_path rules.

Mirrors /Projects/openOODA-core/oodac/ast/load_import_parse.oo:
  - sibling prefixes: std/, std-hw/, oodac/
  - fallback: /Projects/openOODA-core/<imp>
  - relative-to-page, parent-walk, sibling-walk probes
"""
import os
import sys

CORE = "/Projects/openOODA-core"
FLEET = ["/Projects/openOODA-OS", "/Projects/openOODA-apps", "/Projects/openOODA-tools",
         "/Projects/openOODA-DE", "/Projects/openOODA-cloud", "/Projects/openOODA-agents",
         "/Projects/openOODA-core", "/Projects/openOODA", "/Projects/idlescreen",
         "/Projects/openOODA-kernel"]


def probe(p):
    return os.path.isfile(p)


def resolve(page_dir, imp):
    is_std = imp.startswith("std/")
    is_std_hw = imp.startswith("std-hw/")
    is_oodac = imp.startswith("oodac/")
    if not (is_std or is_std_hw or is_oodac):
        if probe(os.path.join(page_dir, imp)):
            return os.path.normpath(os.path.join(page_dir, imp))
    else:
        if is_std:
            sub = imp[4:]
        elif is_std_hw:
            sub = imp[7:]
        else:
            sub = imp[6:]
        if probe(sub):
            return os.path.normpath(sub)
    if probe(imp):
        return os.path.normpath(imp)
    # parent walk
    cur = page_dir
    for _ in range(8):
        nxt = os.path.dirname(cur)
        if nxt == cur:
            break
        cur = nxt
        if probe(os.path.join(cur, imp)):
            return os.path.normpath(os.path.join(cur, imp))
    # sibling walk
    cur = page_dir
    for _ in range(8):
        nxt = os.path.dirname(cur)
        if nxt == cur:
            break
        cur = nxt
        for sib in sorted(os.listdir(cur)) if os.path.isdir(cur) else []:
            sibp = os.path.join(cur, sib)
            if os.path.isdir(sibp) and probe(os.path.join(sibp, imp)):
                return os.path.normpath(os.path.join(sibp, imp))
    if is_std or is_std_hw:
        if probe(os.path.join(CORE, imp)):
            return os.path.normpath(os.path.join(CORE, imp))
    return None


def main(root):
    bad = []
    total = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {".git", "bin", "dist", ".ooda-cache", ".blackbox"}]
        for fn in filenames:
            if not fn.endswith(".oo"):
                continue
            p = os.path.join(dirpath, fn)
            for ln in open(p, encoding="utf-8", errors="replace"):
                ln = ln.strip()
                if ln.startswith("import ") and '"' in ln:
                    imp = ln.split('"')[1]
                    total += 1
                    if resolve(dirpath, imp) is None:
                        bad.append((p.replace(root + "/", ""), imp))
    print("== %s : imports=%d unresolved=%d" % (root, total, len(bad)))
    for p, i in sorted(set(bad)):
        print("   UNRESOLVED %s -> %s" % (p, i))


if __name__ == "__main__":
    for r in sys.argv[1:]:
        main(r)
