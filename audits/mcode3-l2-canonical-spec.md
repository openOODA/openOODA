# L2 openOODA-OS Remediation Spec — canonical std wiring (mcode-review 3)

> **Disposition (2026-11-06):** Archived spec. The L2 `openOODA-OS` canonical-std remediation it prescribes was executed and verified — see `nextgen-2axis-review-mcode3.md` (18/18 PASS). Retained as the transformation reference.


**Status:** reference implementation PROVEN at `/Projects/openOODA-OS/ooaudiod` commit `07fb716`.
`make verify` passes and `make test` reports `PASS: 70/70 assertions` + `ALL TESTS PASSED`.

Read the reference diff first:

```
cd /Projects/openOODA-OS/ooaudiod && git show 07fb716
```

## Founder mandate (do not violate)

> Do NOT delete or strip OODA loop, capability attenuation, attestation, audit, blackbox, quorum, or
> speculation functionality from L2 OS daemons. Instead, replace the toy `% 1000000007` modulus
> clones by wiring their functions to canonical `std/core/ooda.oo`, `std/sec/pqc.oo`,
> `std/sec/capreg.oo`, and `std/sec/warrant.oo` so every L2 daemon has real Next-Gen OODA +
> 32-capability security woven into live execution and passes `make verify` + `make test`.

Keep every existing function, struct, type, and assertion. No file deletions. No test assertion
count changes.

## Canonical primitives (read-only, do NOT edit)

| Path | Exports |
| :--- | :--- |
| `/Projects/openOODA-core/std/sec/pqc.oo` | `oo_pqc_sha3_round(a,b)`, `oo_pqc_sign(digest,sk)`, `oo_pqc_hmac(digest,key)` — 62-bit, always >= 1 |
| `/Projects/openOODA-core/std/ipc/wire.oo` | `oo_wire_mac(words)` — 62-bit SplitMix64 MAC over words[0..6]; **requires >= 7 elements** |
| `/Projects/openOODA-core/std/sec/capreg.oo` | `oo_cap_reg64_pack/check/attenuate`, `oo_cap_bit_index`, `rt_cap_bit_index` |
| `/Projects/openOODA-core/std/core/ooda.oo` | `OodaTurn`, `oo_ooda_init/observe/orient/decide/act` |
| `/Projects/openOODA-core/std/sec/warrant.oo` | `oo_warrant_check(reg64,cur_epoch,req_caps,warrant)`, `oo_warrant_attenuate(parent,child_caps,child_warrants)`, `oo_warrant_is_immutable` |

**Import path form is always the sibling-repo absolute form**: `import "std/sec/pqc.oo";`,
`import "std/ipc/wire.oo";`, `import "std/core/ooda.oo";`, `import "std/sec/capreg.oo";`.
Never `::`, never a relative copy.

## Transformation rules

### T1 — rolling mixer / fingerprint  → canonical sponge

Old shape (any file):

```
    let fv: Int = v % 1000000007;
    let x: Int = if fv < 0 { fv + 1000000007 } else { fv };
    let fa: Int = acc % 1000000007;
    let base: Int = if fa < 0 { fa + 1000000007 } else { fa };
    let prod: Int = (base * 131) % 1000000007;
    return (prod + x) % 1000000007;
```

New:

```
    let h: Int = oo_pqc_sha3_round(acc, v);
    if h <= 0 { return 1; }
    return h;
```

Add `import "std/sec/pqc.oo";` to that file. Same treatment for a string/name hash that folds
`h = ((folded * 33) % 1000000007 + rank) % 1000000007;` → `h = oo_pqc_sha3_round(h, rank);`
and for a state checksum that folds several fields → fold them with `oo_pqc_sha3_round`.

**Semantics**: the old mixer returned values in `[0, 1000000007)` and could return `0`. The
canonical sponge returns a 62-bit value `>= 1`. Any caller that tested `== 0` must be re-read;
in this codebase the checksums are only ever compared for equality against a value produced by
the same function, so equality still holds. Keep a `if h <= 0 { return 1; }` floor.

### T2 — IPC frame integrity tag → canonical MAC

Old shape (`core/wire.oo` and its per-repo equivalents `core/aid_parse.oo`,
`core/realm_parse.oo`, `realm/realm_parse.oo`):

```
    let folded: Int = raw % 1000000007;
    let w: Int = if folded < 0 { folded + 1000000007 } else { folded };
    h = ((h * 31) % 1000000007 + w) % 1000000007;
...
    w = list_push(w, ((h * h) % 1000000007 + h % 97) % 1000000007);
...
    if list_get(wire, 7) != ((h * h) % 1000000007 + h % 97) % 1000000007 { return bad; }
```

New — replace the whole checksum function body with the canonical MAC and use it directly as
the word-7 tag:

```
pub fn <PFX>_frame_checksum(words: List[Int]) -> Int {
    if list_len(words) < 7 { return 0; }
    return oo_wire_mac(words);
}
```

and `w = list_push(w, h);` in encode, `if list_get(wire, 7) != h { return bad; }` in decode.
Add `import "std/ipc/wire.oo";`.

Keep the local frame layout (magic 7951, 32-bit header) exactly as it is — only the tag
algorithm changes.

### T3 — attestation primitives → canonical PQC (`hw/attest.oo` in every repo)

Replace the keccak-sponge body of `<PFX>_attest_shake3` and route hmac/sign through canonical:

```
pub fn <PFX>_attest_shake3(a: Int, b: Int, c: Int) -> Int {
    let h: Int = oo_pqc_sha3_round(oo_pqc_sha3_round(a, b), c);
    if h <= 0 { return 1; }
    return h;
}

pub fn <PFX>_attest_hmac(digest: Int, key: Int) -> Int {
    if digest <= 0 || key <= 0 { return 0; }
    let t: Int = oo_pqc_hmac(digest, key);
    if t <= 0 { return 1; }
    return t;
}

pub fn <PFX>_attest_sign(digest: Int, secret: Int) -> Int {
    if digest <= 0 || secret <= 0 { return 0; }
    let s: Int = oo_pqc_sign(digest, secret);
    if s <= 0 { return 1; }
    return s;
}
```

Add `import "std/sec/pqc.oo";` and drop the now-unused `std/sec/hash/keccak_sponge.oo` import.
`<PFX>_attest_digest`, `_verify`, `_mask`, `_record`, and the `O<PFX>Attest` struct keep their
exact signatures and semantics — the mask must still come out `7` on the good path and
`3 / 6 / 5 / 4` on the four rejection paths.

### T4 — warrant seal → canonical PQC (`core/warrant.oo` in every repo)

```
pub fn oo_warrant_seal(reg64: Int, key: Int) -> Int {
    let r: Int = (reg64 >> 40) & 255;
    if (r & 64) == 0 { return 0; }
    if key <= 0 { return 0; }
    let d: Int = oo_pqc_sha3_round(reg64, key);
    let s: Int = oo_pqc_hmac(d, key);
    if s <= 0 { return 1; }
    return s;
}
```

Add `import "std/sec/pqc.oo";`.

### T5 — canonical 32-capability register + live Next-Gen OODA turn (`core/capreg.oo`)

Two generations exist. Make both land on the same target.

**Generation A** — the file already imports `std/sec/capreg.oo`, `std/core/ooda.oo`,
`std/sec/quorum.oo`, `std/sec/delegate.oo` and already has `<PFX>_ooda_reg()` and
`<PFX>_ooda_turn()`. Its only defect is two **vacuous assertions** in `<PFX>_cap_reg_ok()`:

```
    if packed != oo_cap_reg64_pack(7, 3, 4, mask) { return false; }          // compares a value with itself
    if child != oo_cap_reg64_attenuate(packed, 1, 9, 1) { return false; }     // compares a value with itself
```

Replace exactly those two lines with the real, failing-capable assertions below. Leave the
rest of the file and the existing `<PFX>_ooda_turn` body untouched.

**Generation B** — the file defines its own `oo_cap_reg64_pack/check/attenuate` copies and
imports only `std-hw/hw/runtime/rt_caps_reg64.oo`. Rewrite it to the ooaudiod target:
import `std/sec/capreg.oo` + `std/core/ooda.oo` + `std/sec/quorum.oo` + `std/sec/delegate.oo`,
delete the three copied `oo_cap_reg64_*` functions, add the fail-closed range-validating
wrappers and the canonical OODA turn, exactly as `/Projects/openOODA-OS/ooaudiod/core/capreg.oo`
does after commit `07fb716`. Keep `<PFX>_cap32_soft()` and `<PFX>_cap32_hard()` byte-identical
except for the local prefix, and keep `rt_cap_bit_index("...")` call sites unchanged — the
canonical `std/sec/capreg.oo` also exports `rt_cap_bit_index`.

Target `<PFX>_cap_reg_ok()` body (both generations end up here):

```
pub fn <PFX>_cap_reg_ok() -> Bool {
    let soft: Int = <PFX>_cap32_soft();
    let hard: Int = <PFX>_cap32_hard();
    if (soft | hard) != 4294967295 { return false; }
    if (soft & hard) != 0 { return false; }
    let mask: Int = soft | hard;
    let packed: Int = <PFX>_reg64_pack(7, 3, 4, mask);
    if packed <= 0 { return false; }
    if ((packed >> 48) & 65535) != 7 { return false; }
    if ((packed >> 40) & 255) != 3 { return false; }
    if ((packed >> 32) & 255) != 4 { return false; }
    if (packed & 4294967295) != mask { return false; }
    if <PFX>_reg64_check(packed, 7, 1, 1) == false { return false; }
    if <PFX>_reg64_check(packed, 7, 8, 1) { return false; }
    if <PFX>_reg64_check(packed, 8, 1, 1) { return false; }
    let child: Int = <PFX>_reg64_attenuate(packed, 1, 9, 1);
    if child <= 0 { return false; }
    if ((child & 4294967295) & (4294967295 - (packed & 4294967295))) != 0 { return false; }
    if ((child >> 32) & 255) != 9 { return false; }
    if ((child >> 40) & 255) != 1 { return false; }
    if <PFX>_reg64_check(child, 7, 2, 1) { return false; }
    if <PFX>_reg64_check(child, 7, 1, 1) == false { return false; }
    return <PFX>_ooda_turn(packed, (packed & 255) + 1, ((packed >> 8) & 255) + 1, ((packed >> 40) & 255) + 1, ((packed >> 48) & 255) + 1, true);
}
```

**MANDATORY**: every comparison needs explicit parentheses around the bit-mask expression, e.g.
`if ((packed >> 48) & 65535) != 7 { ... }` — NOT `if (packed >> 48) & 65535 != 7 { ... }`.
The .oo parser binds `!=` tighter than `&`, so the unparenthesised form silently compares the
wrong thing. This exact bug cost one debugging cycle in the reference implementation.

Fail-closed wrappers (Generation B only; Generation A keeps using canonical names directly):

```
pub fn <PFX>_reg64_pack(epoch: Int, rights: Int, badge: Int, caps_mask: Int) -> Int {
    if rights < 0 || rights > 255 { return 0; }
    if badge < 0 || badge > 255 { return 0; }
    if caps_mask < 0 || caps_mask > 4294967295 { return 0; }
    return oo_cap_reg64_pack(epoch, rights, badge, caps_mask);
}

pub fn <PFX>_reg64_check(reg64: Int, cur_epoch: Int, req_rights: Int, req_caps: Int) -> Bool {
    if req_rights < 0 || req_rights > 255 { return false; }
    if req_caps < 0 || req_caps > 4294967295 { return false; }
    return oo_cap_reg64_check(reg64, cur_epoch, req_rights, req_caps);
}

pub fn <PFX>_reg64_attenuate(parent_reg64: Int, child_rights: Int, child_badge: Int, child_caps: Int) -> Int {
    if parent_reg64 <= 0 { return 0; }
    if child_rights < 0 || child_rights > 255 { return 0; }
    if child_badge < 0 || child_badge > 255 { return 0; }
    if child_caps < 0 || child_caps > 4294967295 { return 0; }
    return oo_cap_reg64_attenuate(parent_reg64, child_rights, child_badge, child_caps);
}
```

**IMPORTANT — name collision hazard**: `std/sec/capreg.oo` exports `oo_cap_reg64_pack/check/attenuate`
AND `std/core/ooda.oo` -> `std/sec/warrant.oo` exports `oo_warrant_check` and
`oo_warrant_attenuate`. A locally defined function with the same name shadows the canonical
one for the whole module graph. So the daemon-local warrant helpers MUST use the
non-colliding names `oo_warrant_attenuate4` and `oo_warrant_check4` (this is what
`/Projects/openOODA-OS/ooaudiod/core/warrant.oo` does). Where a repo's `core/warrant.oo`
currently defines `oo_warrant_attenuate` / `oo_warrant_check`, rename them to
`oo_warrant_attenuate4` / `oo_warrant_check4` and update the call sites in `tests/`.

Canonical OODA turn (Generation B only; copy from the reference):

```
pub fn <PFX>_ooda_reg() -> Int {
    return <PFX>_reg64_pack(7, 3, 4, <PFX>_cap32_soft() | <PFX>_cap32_hard());
}

pub fn <PFX>_ooda_turn(reg64: Int, signal: Int, context: Int, intent: Int, effect: Int, act_ok: Bool) -> Bool {
    let ep: Int = (reg64 >> 48) & 65535;
    let rt: Int = (reg64 >> 40) & 255;
    let sk: Int = (reg64 >> 8) & 255;
    let key: Int = (reg64 >> 16) & 255;
    let mut t: OodaTurn = oo_ooda_init(reg64, ep, rt, 1, 100, 64);
    t = oo_ooda_observe(t, signal, 10, sk, key);
    t = oo_ooda_orient(t, context, 10, sk, key);
    t = oo_ooda_decide(t, intent, 10, sk, key);
    t = oo_ooda_act(t, effect, act_ok, sk, key);
    return t.ok && t.committed;
}
```

### T6 — `hw/delegate.oo` and `hw/attest.oo` register calls

Where a `hw/` page calls `oo_cap_reg64_pack` / `oo_cap_reg64_check`, point it at the fail-closed
wrapper `<PFX>_reg64_pack` / `<PFX>_reg64_check` from `core/capreg.oo` (the `hw/` page already
imports `core/capreg.oo`).

### T7 — `core/warrant.oo` structure

Target: import `std/sec/warrant.oo` + `std/sec/pqc.oo`; keep `oo_warrant_phase_epoch`,
`oo_warrant_phase`, `oo_warrant_revoke`, `oo_warrant_seal`, `oo_warrant_seal_ok`; provide
`oo_warrant_attenuate4` (4-arg, keeps the ATTENUATE-right / IMMUTABLE-parent / subset
fail-closed checks, delegates the packing to `oo_cap_reg64_attenuate`) and `oo_warrant_check4`
(4-arg daemon view, delegates to canonical `oo_warrant_check(reg64, cur_epoch, req_caps,
req_rights)` — note the canonical argument order differs from the daemon view).

See `/Projects/openOODA-OS/ooaudiod/core/warrant.oo` after commit `07fb716`.

### T8 — Academy header

Every `.oo` page you touch must keep the 4-element Academy header
(`// # Title`, `// Logline:`, `// Setup:`, `// Beats:`) and stay between 16 and 256 lines with
at most 8 functions. Update the `Setup:` line to mention the canonical pages you now import.

## Verification gate (every repo, mandatory)

```
cd <repo>
rm -f .ooda-cache/check.stamp
make verify          # must print all PASS lines and exit 0
make test            # must print "ALL TESTS PASSED" and exit 0
```

The `make test` target asserts an exact assertion count (e.g. `PASS: 70/70 assertions`). The
count must be UNCHANGED from the repo's current value — you are not adding or removing
assertions. If the count changed, you changed an assertion; fix that instead of editing the
Makefile.

Also run the size linter (must report `files_with_size_violation=0`):

```
OODA_NO_JAIL=1 /home/ubermetroid/.local/bin/lint-oo-size <repo>
```

## Rules

1. Do NOT edit anything under `/Projects/openOODA-core/` (another agent owns it).
2. Do NOT edit `/Projects/openOODA/openOODA` or any repo outside your assigned list.
3. Do NOT delete files. Do NOT delete functions, types, or assertions.
4. Do NOT change the public behaviour of any function other than as specified above.
5. Do NOT `git push`. Commit only (one commit per repo, message starting with
   `fix(sec): wire the toy modulus clones to canonical std/sec/pqc.oo ...`).
6. `git -c user.name='spotlight' -c user.email='spotlight@clownhouse.io' commit`.
7. If `make verify` or `make test` fails, iterate until both pass. If you cannot make it pass,
   revert that repo (`git checkout -- . && git reset --hard HEAD`) and report the exact failure
   and what you tried — a half-finished repo is worse than an untouched one.
8. Report per repo: files changed, the assertion count before/after, `make verify` and
   `make test` results, and the lint-oo-size violation count.

## Report format

One section per repo, in this shape:

```
### <repo>
- files changed: <list>
- assertions: <before> -> <after>
- make verify: PASS/FAIL (<one-line reason>)
- make test: PASS/FAIL (<one-line reason>)
- lint-oo-size: BIGFILE=<n> MANYFN=<n> LONGFN=<n> DENSE=<n>
- commit: <short sha>
```
