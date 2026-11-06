#!/usr/bin/env python3
"""mcode-review 3 -- D9 remediation for the Generation-A L2 daemons.

Defect D9: the Generation-A daemons call the canonical std/sec/capreg.oo
helpers (oo_cap_reg64_pack / _check / _attenuate) directly. Those helpers
silently mask out-of-width fields:

    oo_cap_reg64_pack(epoch, rights, badge, caps)
        -> (rights & 255), (badge & 255), (caps & 4294967295)
    oo_cap_reg64_check(reg64, cur_epoch, req_rights, req_caps)
        -> need = ((req_rights & 255) << 40) | (req_caps & 4294967295)

so a caller that asks for rights = 256 has its requirement masked down to
zero rights, and the check then PASSES. That is a fail-open widening in the
live attestation gate (hw/attest.oo) and the live delegation path
(hw/delegate.oo).

Remediation, mirroring the Generation-B shape that already passed review:
  * add fail-closed <PFX>_reg64_pack / _check / _attenuate wrappers to
    core/capreg.oo; each validates the field ranges and then delegates to
    the canonical helper;
  * route core/capreg.oo's own calls through the wrappers;
  * route hw/attest.oo and hw/delegate.oo through the wrappers.

Side effect: the `import "core/capreg.oo"` in hw/attest.oo stops being a
dangling import, so every page now typechecks standalone.

No file, function, type, or assertion is removed. The assertion count is
unchanged.
"""

import re
import sys

REPOS = {
    "ooaid": "ooaid",
    "oohealthd": "oohealth",
    "ooimage": "ooimage",
    "ooinit": "oo",
    "oonetd": "oo",
    "oosession": "oo",
}

ROOT = "/Projects/openOODA-OS"

WRAPPERS = '''pub fn {p}_reg64_pack(epoch: Int, rights: Int, badge: Int, caps_mask: Int) -> Int {{
    if rights < 0 || rights > 255 {{ return 0; }}
    if badge < 0 || badge > 255 {{ return 0; }}
    if caps_mask < 0 || caps_mask > 4294967295 {{ return 0; }}
    return oo_cap_reg64_pack(epoch, rights, badge, caps_mask);
}}

pub fn {p}_reg64_check(reg64: Int, cur_epoch: Int, req_rights: Int, req_caps: Int) -> Bool {{
    if req_rights < 0 || req_rights > 255 {{ return false; }}
    if req_caps < 0 || req_caps > 4294967295 {{ return false; }}
    return oo_cap_reg64_check(reg64, cur_epoch, req_rights, req_caps);
}}

pub fn {p}_reg64_attenuate(parent_reg64: Int, child_rights: Int, child_badge: Int, child_caps: Int) -> Int {{
    if parent_reg64 <= 0 {{ return 0; }}
    if child_rights < 0 || child_rights > 255 {{ return 0; }}
    if child_badge < 0 || child_badge > 255 {{ return 0; }}
    if child_caps < 0 || child_caps > 4294967295 {{ return 0; }}
    return oo_cap_reg64_attenuate(parent_reg64, child_rights, child_badge, child_caps);
}}

'''


def fail(msg):
    print("FAIL: " + msg)
    sys.exit(1)


def read(path):
    with open(path, "r") as fh:
        return fh.read()


def write(path, text):
    with open(path, "w") as fh:
        fh.write(text)


for repo, pfx in REPOS.items():
    base = f"{ROOT}/{repo}"
    capreg = f"{base}/core/capreg.oo"
    attest = f"{base}/hw/attest.oo"
    delegate = f"{base}/hw/delegate.oo"

    src = read(capreg)

    # The wrapper names must not already exist.
    for name in (f"{pfx}_reg64_pack", f"{pfx}_reg64_check", f"{pfx}_reg64_attenuate"):
        if re.search(r"\b" + name + r"\b", src):
            fail(f"{repo}: {name} already exists in core/capreg.oo")

    # Split off the wrapper block so the call-site rewrite below cannot
    # rewrite the canonical call inside the wrappers themselves.
    body = src
    marker = "pub fn "
    idx = body.index(marker)
    head, tail = body[:idx], body[idx:]

    wrappers = WRAPPERS.format(p=pfx)

    # Rewrite the call sites in the existing body.
    n_pack = len(re.findall(r"\boo_cap_reg64_pack\(", tail))
    n_check = len(re.findall(r"\boo_cap_reg64_check\(", tail))
    n_atten = len(re.findall(r"\boo_cap_reg64_attenuate\(", tail))
    tail = re.sub(r"\boo_cap_reg64_pack\(", f"{pfx}_reg64_pack(", tail)
    tail = re.sub(r"\boo_cap_reg64_check\(", f"{pfx}_reg64_check(", tail)
    tail = re.sub(r"\boo_cap_reg64_attenuate\(", f"{pfx}_reg64_attenuate(", tail)

    # The wrappers themselves must still call the canonical helpers.
    if f"{pfx}_reg64_pack" in tail and "oo_cap_reg64_pack" not in wrappers:
        fail(f"{repo}: wrapper body lost the canonical call")

    out = head + wrappers + tail
    write(capreg, out)

    # hw/attest.oo: route the live mask gate through the fail-closed check.
    a = read(attest)
    cnt = a.count("oo_cap_reg64_check(")
    if cnt != 1:
        fail(f"{repo}: expected exactly 1 canonical check in hw/attest.oo, found {cnt}")
    a = a.replace("oo_cap_reg64_check(", f"{pfx}_reg64_check(")
    write(attest, a)

    # hw/delegate.oo: route the live child-register pack through the
    # fail-closed pack.
    d = read(delegate)
    cnt = d.count("oo_cap_reg64_pack(")
    if cnt != 1:
        fail(f"{repo}: expected exactly 1 canonical pack in hw/delegate.oo, found {cnt}")
    d = d.replace("oo_cap_reg64_pack(", f"{pfx}_reg64_pack(")
    write(delegate, d)

    lines = out.count("\n")
    fns = len(re.findall(r"^\s*(pub )?fn ", out, re.M))
    print(f"{repo:10s} prefix={pfx + '_':10s} "
          f"pack={n_pack} check={n_check} atten={n_atten} "
          f"capreg_lines={lines} capreg_fns={fns}")
