#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# openOODA/qa/lint_oo_size.sh
# .oo Size + Mixed-Domain Lint Probe (read-only burn-down inventory)
# ==============================================================================
# Per .oo file reports: function count, longest function in lines (with
# name), and mixed-domain (capability-substrate) signals. Scans oodac,
# oodar, std, and the governance repo without writing outside stdout.
# Default output is the burn-down inventory: flagged rows only,
# worst offenders first. Pass --all for every scanned file.
# Thresholds (env-overridable): OO_MAX_LINES=256 OO_MAX_FNS=15 OO_MAX_FN=80.
# Exit 0 when no size violation; exit 1 when any BIGFILE/MANYFN/LONGFN
# fires. MIX is an informational signal and never fails the probe.
# Longest-function uses brace-depth matching; braces inside strings or
# comments can skew a row, so treat rows as triage leads, not verdicts.
# ==============================================================================

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GOV="$(cd "$HERE/.." && pwd)"
POLY="${OODA_POLYROOT:-$(cd "$GOV/.." && pwd)}"
MAX_LINES="${OO_MAX_LINES:-256}"
MAX_FNS="${OO_MAX_FNS:-15}"
MAX_FN="${OO_MAX_FN:-80}"
MODE="${1:---flagged}"

export POLY MAX_LINES MAX_FNS MAX_FN MODE

python3 - <<'PY'
import os
import re
import sys

poly = os.environ["POLY"]
max_lines = int(os.environ["MAX_LINES"])
max_fns = int(os.environ["MAX_FNS"])
max_fn = int(os.environ["MAX_FN"])
flagged_only = os.environ.get("MODE", "--flagged") != "--all"

roots = ["oodac", "oodar", "std", "openOODA"]
fnre = re.compile(r"^[ \t]*(?:pub[ \t]+)?fn[ \t]+([A-Za-z_][A-Za-z0-9_]*)")
GROUPS = [
    ("fs", ["fsreadcap", "fswritecap", "fscap"]),
    ("net", ["netcap", "tcpcap", "udpcap", "bindcap"]),
    ("gpu", ["gpucap"]),
    ("thread", ["threadcap"]),
    ("ffi", ["fficap"]),
    ("mem", ["alloccap", "arenacap"]),
    ("env", ["envcap", "processcap", "syscap"]),
    ("time", ["timecap", "randcap", "metricscap", "signcap"]),
]


def scan(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        lines = fh.read().split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    low = "\n".join(lines).lower()
    domains = [g for g, keys in GROUPS if any(k in low for k in keys)]
    starts = [(i, m.group(1)) for i, l in enumerate(lines)
              if (m := fnre.match(l))]
    longest, longest_name = 0, "-"
    for s, name in starts:
        depth, begun, end = 0, False, len(lines) - 1
        for i in range(s, len(lines)):
            for ch in lines[i]:
                if ch == "{":
                    depth += 1
                    begun = True
                elif ch == "}":
                    depth -= 1
            if begun and depth <= 0:
                end = i
                break
        if end - s + 1 > longest:
            longest, longest_name = end - s + 1, name
    flags = []
    if len(lines) > max_lines:
        flags.append("BIGFILE")
    if len(starts) > max_fns:
        flags.append("MANYFN")
    if longest > max_fn:
        flags.append("LONGFN")
    if len(domains) >= 2:
        flags.append("MIX")
    return len(lines), len(starts), longest, longest_name, domains, flags


files = []
for root in roots:
    base = os.path.join(poly, root)
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for fn in sorted(filenames):
            if fn.endswith(".oo"):
                files.append(os.path.join(dirpath, fn))

rows = []
counts = {"BIGFILE": 0, "MANYFN": 0, "LONGFN": 0, "MIX": 0}
for path in sorted(files):
    try:
        nlines, nfns, longest, lname, domains, flags = scan(path)
    except OSError:
        continue
    for f in flags:
        counts[f] += 1
    if flagged_only and not flags:
        continue
    rel = os.path.relpath(path, poly)
    dom = "+".join(domains) if domains else "-"
    flg = ",".join(flags) if flags else "-"
    rows.append((len(flags), longest, nlines, rel, nlines, nfns,
                 longest, lname, dom, flg))

rows.sort(key=lambda r: (-r[0], -r[1], -r[2]))

n_viol = sum(1 for r in rows if "BIGFILE" in r[9] or "MANYFN" in r[9]
               or "LONGFN" in r[9])
print("# .oo size lint inventory")
print(f"# polyroot: {poly}")
print(f"# thresholds: lines>{max_lines} fns>{max_fns} longest>{max_fn}")
print(f"# files_scanned: {len(files)}")
print(f"# rows_listed: {len(rows)}")
print(f"# violations: BIGFILE={counts['BIGFILE']} "
      f"MANYFN={counts['MANYFN']} LONGFN={counts['LONGFN']} "
      f"files_with_size_violation={n_viol}")
print(f"# mix_signals: MIX={counts['MIX']}")
print("file\tlines\tfns\tlongest\tlongest_fn\tdomains\tflags")
for r in rows:
    print(f"{r[3]}\t{r[4]}\t{r[5]}\t{r[6]}\t{r[7]}\t{r[8]}\t{r[9]}")
sys.exit(1 if n_viol else 0)
PY
