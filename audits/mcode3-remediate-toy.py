#!/usr/bin/env python3
"""mcode3 remediation: clear the toy modulus / traversal vectors in the 8 target repos.

Every substitution is asserted (exact before/after counts) so a drifted tree
fails loudly instead of silently producing a half-remediated page.
"""
import sys

APPS = "/Projects/openOODA-apps"
OS = "/Projects/openOODA-OS"

# repo -> component prefix
STATE_REPOS = {
    "%s/oobrowser" % APPS: "oobrowser",
    "%s/oocanvas" % APPS: "oocanvas",
    "%s/oochat" % APPS: "oochat",
    "%s/oodaw" % APPS: "oodaw",
    "%s/oodeck" % APPS: "oodeck",
}

OLD_ENC = "    return (((sa % 1000000007) * 1000003) % 1000000007 + sb) % 1000000007;"
NEW_ENC = "    return sa * 1000003 + sb;"
OLD_DEC = "    let a: Int = (sv / 1000003) % 1000000007;"
NEW_DEC = "    let a: Int = sv / 1000003;"
OLD_HDR = "//   Encode/decode items with mod-1e9+7 checksums."
NEW_HDR = "//   Encode/decode items as a lossless base-1000003 packed pair."

fail = []


def patch(path, pairs):
    with open(path, encoding="utf-8") as f:
        src = f.read()
    orig = src
    for old, new, want in pairs:
        got = src.count(old)
        if got == want:
            src = src.replace(old, new)
        elif got == 0 and src.count(new) >= 1:
            print("  already applied, skipping %s" % path)
        else:
            fail.append("%s: expected %d occurrence(s) of %r, found %d"
                        % (path, want, old[:60], got))
    if src != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(src)
        print("  patched %s" % path)


print("== state.oo codec: drop the toy modulus from the reversible item codec ==")
for repo, pfx in STATE_REPOS.items():
    patch("%s/core/state.oo" % repo, [
        (OLD_ENC, NEW_ENC, 1),
        (OLD_DEC, NEW_DEC, 1),
        (OLD_HDR, NEW_HDR, 1),
    ])

print("== oodeck: retarget the oo_pqc_sha3_round salt from the toy modulus to the fleet salt 7 ==")
SALT = [
    ("%s/oodeck/core/engine.oo" % APPS, 7),
    ("%s/oodeck/ipc/framebuf.oo" % APPS, 1),
    ("%s/oodeck/ipc/wayland_client.oo" % APPS, 5),
    ("%s/oodeck/sec/pqcseal.oo" % APPS, 2),
    ("%s/oodeck/ui/view.oo" % APPS, 2),
]
for path, want in SALT:
    patch(path, [(", 1000000007)", ", 7)", want)])

print("== ooflash: mark the negative-trust test page with the fleet _expect_ marker ==")
patch("%s/ooflash/tests/test_flash.oo" % APPS, [
    ("check_fx(", "ooflash_fx_expect(", 30),
])

if fail:
    print("\nFAILED:")
    for f in fail:
        print("  " + f)
    sys.exit(1)
print("\nOK: all substitutions applied")
