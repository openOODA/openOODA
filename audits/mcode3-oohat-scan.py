#!/usr/bin/env python3
"""Faithful re-implementation of the oohat Purple + Black gates over a repo tree.

Mirrors:
  /Projects/openOODA-agents/oohat/hats/blue.oo   (oohat_orient_scan_tree, oohat_purple_orient)
  /Projects/openOODA-agents/oohat/hats/black.oo  (oohat_black_exec_vectors, oohat_black_data_vectors,
                                                   oohat_black_standards_page, oohat_black_spec_page)
  /Projects/openOODA-agents/oohat/core/metrics.oo (oohat_page_info, oohat_has_academy, oohat_is_banned_name)
  /Projects/openOODA-agents/oohat/core/scan.oo    (oohat_collect / oohat_scan_files / density)
"""
import os
import sys

SKIP_DIRS = {".git", ".github", "bin", "dist", ".ooda-cache", ".blackbox"}
BANNED = {"util.oo", "utils.oo", "helper.oo", "helpers.oo", "common.oo",
          "misc.oo", "shared.oo", "base.oo", "core.oo"}


def is_banned_name(bn):
    if bn in BANNED:
        return True
    if "_ext.oo" in bn or "_part" in bn:
        return True
    return False


def has_academy(src):
    lines = src.split("\n")
    head = "\n".join(lines[:16])
    return ("// # " in head and "// Logline:" in head
            and "// Setup:" in head and "// Beats:" in head)


def is_fn_line(line):
    t = line.strip()
    return t.startswith("pub fn ") or t.startswith("fn ")


def page_info(src):
    lines = src.split("\n")
    fns = 0
    cur = 0
    maxfn = 0
    for ln in lines:
        if is_fn_line(ln):
            fns += 1
            maxfn = max(maxfn, cur)
            cur = 1
        elif cur > 0:
            cur += 1
    maxfn = max(maxfn, cur)
    n2 = len(lines) if len(src) > 0 else 0
    if n2 > 0 and lines[n2 - 1].strip() == "":
        n2 -= 1
    return n2, fns, maxfn, has_academy(src)


def exec_vectors(src):
    sh = dos = trv = mem = 0
    dot2 = "." + "." + "/"
    if ("sh -c" in src or "bash -c" in src or "system(" in src or "popen(" in src):
        sh += 1
    if "process_exit(" in src or "abort()" in src:
        dos += 1
    if (dot2 in src or "/etc/passwd" in src or "/etc/shadow" in src
            or "/proc/self/mem" in src or "/dev/mem" in src):
        if not any(k in src for k in ("path_safe(", "assert_eq(", "_expect_",
                                      "!str_contains", "test_", "selftest")):
            trv += 1
    if any(k in src for k in ("unsafe ", "transmute", "raw_ptr", "dlopen", "LD_PRELOAD")):
        mem += 1
    return sh, dos, trv, mem


def data_vectors(src):
    sec = cls = psn = bnd = 0
    if any(k in src for k in ("PRIVATE_KEY", " api_key", "secret_key", "password =")):
        sec += 1
    if any(k in src for k in ("zebes", "ringmaster", "spotlight",
                              "100.102.186.93", "100.88.249.93", "100.66.54.24")):
        cls += 1
    if any(k in src for k in ("<<<<<<<<", ">>>>>>>>", "1000000007", "// TODO", "// FIXME")):
        psn += 1
    if any(k in src for k in ("unchecked_idx", "unauth_ipc", "gets(", "strcpy(")):
        bnd += 1
    return sec, cls, psn, bnd


def spec_page(src):
    ev = exec_vectors(src)
    dv = data_vectors(src)
    v = sum(ev) + sum(dv)
    if "sovereign" in src or "moonshot" in src:
        v += 1
    if "dogfight" in src or "bootstrap" in src:
        v += 1
    return v


def standards_page(src, path):
    nlines, fns, maxfn, hdr = page_info(src)
    v = 0
    if not hdr:
        v += 1
    if nlines > 256:
        v += 1
    if fns > 0 and nlines < 16:
        v += 1
    if fns > 8:
        v += 1
    if maxfn > 64:
        v += 1
    if is_banned_name(os.path.basename(path)):
        v += 1
    if "\t" in src:
        v += 1
    return v, (nlines, fns, maxfn, hdr)


def collect(root):
    out = []
    def walk(d, depth):
        if depth > 6 or not os.path.isdir(d):
            return
        try:
            entries = sorted(os.listdir(d))
        except OSError:
            return
        for name in entries:
            if name in SKIP_DIRS or name.startswith("."):
                continue
            p = os.path.join(d, name)
            if os.path.isdir(p):
                walk(p, depth + 1)
            elif name.endswith(".oo"):
                out.append(p)
    walk(root, 0)
    return sorted(out)


def main(root):
    files = collect(root)
    # density
    dirs = {}
    for f in files:
        d = os.path.dirname(f)
        dirs[d] = dirs.get(d, 0) + 1
    dens = {d: c for d, c in dirs.items() if c > 8}

    toy = weak = pqc_imps = 0
    std_f = 0
    spec_f = 0
    details = []
    for p in files:
        try:
            src = open(p, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        st, info = standards_page(src, p)
        sp = spec_page(src)
        std_f += st
        spec_f += sp
        if "std/sec/pqc.oo" in src or "std/sec/capreg.oo" in src or "std/core/ooda.oo" in src:
            pqc_imps += 1
        hits = []
        if "1000000007" in src:
            hits.append("TOY_MOD_1000000007")
        if "998244353" in src:
            hits.append("TOY_MOD_998244353")
        for k in ("md5(", "sha1(", "crc32_auth", "fake_hash"):
            if k in src:
                hits.append("WEAK_HASH:" + k)
        if st:
            nlines, fns, maxfn, hdr = info
            if not hdr:
                hits.append("NO_HEADER")
            if nlines > 256:
                hits.append("LINES=%d>256" % nlines)
            if fns > 0 and nlines < 16:
                hits.append("LINES=%d<16" % nlines)
            if fns > 8:
                hits.append("FNS=%d>8" % fns)
            if maxfn > 64:
                hits.append("MAXFN=%d>64" % maxfn)
            if is_banned_name(os.path.basename(p)):
                hits.append("BANNED_NAME")
            if "\t" in src:
                hits.append("TAB")
        if sp:
            ev = exec_vectors(src)
            dv = data_vectors(src)
            names = ["SHELL", "DOS", "TRAVERSAL", "MEMORY"]
            for i, nm in enumerate(names):
                if ev[i]:
                    hits.append(nm + "=%d" % ev[i])
            for i, nm in enumerate(["SECRET", "CLUSTER", "POISON", "BOUNDS"]):
                if dv[i]:
                    hits.append(nm + "=%d" % dv[i])
            if "sovereign" in src or "moonshot" in src:
                hits.append("SPEC_WORD_A")
            if "dogfight" in src or "bootstrap" in src:
                hits.append("SPEC_WORD_B")
        if hits:
            details.append((p, hits))

    print("== repo: %s" % root)
    print("files_scanned=%d pqc_imports=%d toy_mod=%d weak_hash=%d" % (len(files), pqc_imps, toy, weak))
    print("density_violations=%d std_findings=%d spec_findings=%d" % (len(dens), std_f, spec_f))
    for d, c in sorted(dens.items()):
        print("  DENSE %s = %d" % (d, c))
    for p, hits in details:
        print("  %s :: %s" % (p.replace(root + "/", ""), ", ".join(hits)))
    # purple
    purple_ok = pqc_imps > 0 and toy == 0 and weak == 0
    black_ok = (len(dens) == 0) and std_f == 0 and spec_f == 0
    print("PURPLE=%s BLACK=%s" % ("PASS" if purple_ok else "FAIL",
                                  "PASS" if black_ok else "FAIL"))
    print()


if __name__ == "__main__":
    for r in sys.argv[1:]:
        main(r)
