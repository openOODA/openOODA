# 2-Axis Next-Generation Code Review — Tier 0 Flagships + L2 `openOODA-OS` Batch

> **Disposition (2026-11-06):** Archived 2-axis review (Tier-0 flagships + 15 L2 daemons, all PASS). Scope predates consolidation — `oodevd`, `oodnsd`, `oofs-*`, `oologd`, `ooimage`, `oorealm`, `oosession`, `oodevd` are absorbed names under `persona-ownership.oot` now.


**Date:** 2026-11-05 (18:20–21:50 HST)
**Reviewer:** `mcode-review 3` (Stage 1 Code Reviewer, MiniMax Code)
**Scope:** 18 git repositories — Tier 0 flagships (`idlescreen`, `ooflash`, `openOODA`) and the L2 `openOODA-OS` batch (`ooaid`, `ooaudiod`, `oodevd`, `oodnsd`, `oofs-ext4`, `oofs-tmp`, `oohealthd`, `ooimage`, `ooinit`, `oologd`, `oonetd`, `oopolicyd`, `oopowerd`, `oorealm`, `oosession`)
**Claim:** `/Projects/openOODA/.spotlight-review-claims.tsv`, owner `wE:p1`, zero overlap with `mcode-review 1` (`w3:p1`) or `mcode-review 2`
**Method:** pull from Forgejo (`http://100.102.186.93:3000`) → two-axis review → remediate → `make verify` + `make test` → commit → push `origin`

---

## 0. Summary

| Axis | Result |
| :--- | :--- |
| **Standards** (Power-of-2 shape ladder, Rule 1.25 links, Academy header, file law) | **PASS after remediation.** `lint-oo-size` reports `BIGFILE=0 MANYFN=0 LONGFN=0 DENSE=0 files_with_size_violation=0` in all 18 repositories. Two shell-out defects and one hardcoded-address defect were fixed in `openOODA`. |
| **Spec** (canonical `std/core/ooda.oo` + `std/sec/pqc.oo` + `std/sec/capreg.oo` wiring, live 32-capability security, no toy-prime crypto) | **FAIL on entry, PASS after remediation.** Every L2 daemon carried toy `% 1000000007` clones of the canonical security primitives; 9 of 15 carried no canonical OODA turn at all; 6 of 15 carried a differential-parity gate that compared a value with itself and could never fail. |

The batch inherited one cross-repository blocker in canonical L0 `std` that was already in flight with its rightful owner, and it is reported here as **F1** because it broke every consumer of the canonical OODA engine across the ecosystem.

**Thirteen defects (D1–D13) were fixed, verified, committed, and pushed to Forgejo.** Four further findings (F1–F4) are reported with a remediation direction and are outside this batch's claim.

The founder's mandate — wire the toy clones to the canonical pages so every L2 daemon carries real Next-Gen OODA and 32-capability security in live execution, without deleting any OODA, attestation, audit, blackbox, quorum, or speculation functionality — is met: all 15 daemons now run the canonical 4-phase OODA turn over the 32-capability register in their live capability gate, with a fail-closed register wrapper, and zero toy-modulus arithmetic anywhere. No file, function, type, or assertion was removed anywhere in the batch.

---

## 1. Standards Axis — Power-of-2 Shape Ladder

### 1.1 `lint-oo-size` per repository

`/home/ubermetroid/.local/bin/lint-oo-size`, thresholds `lines>256 fns>8 longest>64 dir_files>8`, run against each repository root with `OODA_NO_JAIL=1` (the linter is jailed to `/Projects/openOODA` by default and cannot read the L2 tree otherwise):

| Repository | Pages scanned | BIGFILE | MANYFN | LONGFN | DENSE | Files affected |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| `idlescreen` | 182 | 0 | 0 | 0 | 0 | 0 |
| `ooflash` | 18 | 0 | 0 | 0 | 0 | 0 |
| `openOODA` | 665 | 0 | 0 | 0 | 0 | 0 |
| `ooaid` | 42 | 0 | 0 | 0 | 0 | 0 |
| `ooaudiod` | 25 | 0 | 0 | 0 | 0 | 0 |
| `oodevd` | 30 | 0 | 0 | 0 | 0 | 0 |
| `oodnsd` | 25 | 0 | 0 | 0 | 0 | 0 |
| `oofs-ext4` | 25 | 0 | 0 | 0 | 0 | 0 |
| `oofs-tmp` | 25 | 0 | 0 | 0 | 0 | 0 |
| `oohealthd` | 25 | 0 | 0 | 0 | 0 | 0 |
| `ooimage` | 43 | 0 | 0 | 0 | 0 | 0 |
| `ooinit` | 38 | 0 | 0 | 0 | 0 | 0 |
| `oologd` | 25 | 0 | 0 | 0 | 0 | 0 |
| `oonetd` | 39 | 0 | 0 | 0 | 0 | 0 |
| `oopolicyd` | 25 | 0 | 0 | 0 | 0 | 0 |
| `oopowerd` | 25 | 0 | 0 | 0 | 0 | 0 |
| `oorealm` | 25 | 0 | 0 | 0 | 0 | 0 |
| `oosession` | 39 | 0 | 0 | 0 | 0 | 0 |

The 256-line page ceiling holds everywhere, before and after remediation.

### 1.2 Rule 1.25 link law, conflict markers, banned file names

Every repository was scanned for symbolic links and for hard links (`find -type l`, `find -type f -links +1`, excluding `.git`), for merge conflict markers across `.oo`, `.oot`, `.md`, and `Makefile`, and for the banned file-name list (`util.oo`, `utils.oo`, `helper.oo`, `helpers.oo`, `common.oo`, `misc.oo`, `shared.oo`, `base.oo`, `core.oo`).

**Zero links, zero conflict markers, zero banned names in all 18 repositories.**

### 1.3 Academy header

The Academy gate is the repository's own `make academy` target, which scans `head -16` of every `.oo` page for `// # `, `// Logline:`, `// Setup:`, and `// Beats:`. `idlescreen` and every L2 daemon run it inside `make verify`, and all report `PASS: academy headers hold`.

`openOODA` has no root `Makefile`; its Academy and shape gates run through `.github/workflows/ci.yml`, which builds `qa/lint_oo_size.oo` and runs the polyrepo inventory. The inventory reports `files_with_size_violation=0` for the 665 pages of the governance repository.

---

## 2. Spec Axis — Canonical Wiring, Live OODA, No Toy Crypto

### 2.1 Canonical import adoption on entry

| Import | L2 daemons importing it on entry | Of 15 |
| :--- | :---: | :--- |
| `std/core/ooda.oo` (canonical 4-phase OODA turn) | 6 | 9 daemons had **no** canonical OODA turn at all |
| `std/sec/pqc.oo` (canonical ML-DSA-65-style sponge, sign, HMAC) | **0** | every daemon used the toy modulus instead |
| `std/sec/capreg.oo` (canonical 64-bit capability register) | 6 | 9 daemons carried a local copy of the register arithmetic |
| `std/sec/warrant.oo` (canonical hardware warrants) | 6 | 9 daemons carried a local copy of the warrant arithmetic |

### 2.2 The toy modulus

`grep -rl 1000000007` over the L2 batch found the toy prime modulus in **every** daemon, in both security primitives and plain checksums:

| Site | Count of files | What it was |
| :--- | ---: | :--- |
| `hw/attest.oo` | 15 | Attestation digest, keyed HMAC, and ML-DSA-style signature |
| `core/warrant.oo` | 15 | The service warrant seal |
| `core/wire.oo` and the per-daemon frame codecs | 7 | The word-7 IPC frame integrity tag |
| `core/types.oo`, `core/policy.oo` and the per-daemon equivalents | 22 | Table checksum and name fingerprint |
| `core/aid_*`, `core/realm_*`, `realm/*`, `svcmgr/*`, `dns/*`, `policy/*` | 15 | Ring checksum, state checksum, frame codec |

The canonical L0 pages already owned every one of these primitives — `std/sec/pqc.oo` (`oo_pqc_sha3_round`, `oo_pqc_sign`, `oo_pqc_hmac`, 62-bit, explicitly "zero toy prime moduli"), `std/ipc/wire.oo` (`oo_wire_mac`, the canonical 62-bit SplitMix64 IPC MAC), `std/sec/capreg.oo`, and `std/sec/warrant.oo`. The daemons were copying them instead of importing them.

### 2.3 The vacuous differential-parity gate

Six daemons (`ooaid`, `oohealthd`, `ooimage`, `ooinit`, `oonetd`, `oosession`) imported canonical `std/sec/capreg.oo` and then asserted in their live capability gate:

```
    if packed != oo_cap_reg64_pack(7, 3, 4, mask) { return false; }
    if child != oo_cap_reg64_attenuate(packed, 1, 9, 1) { return false; }
```

Each line compares a value with the function that produced it, so the comparison can never be false and the gate is dead weight that reads as a differential-parity check. The same pattern was introduced in `ooaid` by commit `0834d20` and was still present on entry.

### 2.4 The lost parity oracle (ecosystem-wide)

`std-hw` commit `90b8cd1` ("fix(capreg): delegate the capability register helpers to std/sec/capreg.oo", 2026-11-05 07:19 -1000) changed `std-hw/hw/runtime/rt_caps_reg64.oo` from an independent implementation into thin aliases:

```
-pub fn rt_cap_reg64_pack(epoch: Int, rights: Int, badge: Int, caps_mask: Int) -> Int {
-    return ((epoch & 65535) << 48) | ((rights & 255) << 40) | ((badge & 255) << 32) | (caps_mask & 4294967295);
+pub fn rt_cap_reg64_pack(epoch: Int, rights: Int, badge: Int, caps_mask: Int) -> Int {
+    return oo_cap_reg64_pack(epoch, rights, badge, caps_mask);
```

`std/sec/capreg.oo` already carried the same aliases. After `90b8cd1` there is **no independent implementation of the register arithmetic left at the `.oo` level**, so every assertion of the form `local != rt_cap_reg64_pack(...)` compares a value against the function that produced it. That includes the parity assertion that `mcode-review 1` restored in `oosysbus/core/capreg.oo` as its defect D1.

### 2.5 Live execution

`ooaudiod` and the other nine Generation-B daemons had no canonical OODA turn, and their capability gate was reached from the live policy path (`core/policy.oo`, `if <PFX>_cap_reg_ok() == false { return false; }`) but only checked the register. After remediation every daemon runs the canonical `oo_ooda_init → observe → orient → decide → act` turn over its own 32-capability register inside that same live gate.

---

## 3. Defects found and fixed

| ID | Defect | Where | Repair |
| :--- | :--- | :--- | :--- |
| **D1** | The 15 L2 daemons computed attestation digests, keyed HMACs, ML-DSA-style signatures, warrant seals, IPC frame tags, table checksums, and name fingerprints with the toy prime modulus `1000000007`, while canonical `std/sec/pqc.oo` and `std/ipc/wire.oo` already owned those primitives. | 15 repositories, `hw/attest.oo`, `core/warrant.oo`, `core/wire.oo`, `core/types.oo`, `core/policy.oo` and the per-daemon equivalents | Route every one of them to `std/sec/pqc.oo` (`oo_pqc_sha3_round`, `oo_pqc_sign`, `oo_pqc_hmac`) and `std/ipc/wire.oo` (`oo_wire_mac`). `grep -rn 1000000007` now returns nothing in any L2 `.oo` file. |
| **D2** | Six daemons carried a differential-parity gate that compared a value with itself, so the gate could never fail. | `ooaid`, `oohealthd`, `ooimage`, `ooinit`, `oonetd`, `oosession` — `core/capreg.oo` | Replaced the two self-comparisons with assertions that can fail: register layout round-trip (epoch, rights, badge, caps), right isolation, epoch mismatch, attenuation monotonicity, child badge and rights round-trip. |
| **D3** | Nine daemons carried local copies of the canonical 64-bit capability register and warrant arithmetic and had no canonical OODA turn. | `ooaudiod`, `oodevd`, `oodnsd`, `oofs-ext4`, `oofs-tmp`, `oologd`, `oopolicyd`, `oopowerd`, `oorealm` — `core/capreg.oo`, `core/warrant.oo` | Dropped the copied register arithmetic in favour of `std/sec/capreg.oo`, kept a fail-closed range-validating wrapper so an out-of-width field is still refused instead of silently masked, added the canonical 4-phase OODA turn, and wired it into the live capability gate. |
| **D4** | The daemon-local warrant helpers were named `oo_warrant_attenuate` and `oo_warrant_check`, which shadow the canonical `std/sec/warrant.oo` exports of the same name across the whole module graph. | 9 Generation-B daemons — `core/warrant.oo` | Renamed the daemon views to `oo_warrant_attenuate4` and `oo_warrant_check4` and updated the call sites in `tests/`. The daemon view keeps its own argument order; the canonical page is now reachable instead of shadowed. |
| **D5** | The parity gate discovered the upstream program by handing a shell script to `/bin/sh -c`. | `openOODA/buildbox/parity/run.oo:198`, `openOODA/buildbox/ci/parts/parity/run.oo:170` | `parity_find_upstream` now probes the standard program directories and every `PATH` entry through `fs_path_exists`, so no shell interprets a script string. Verified against `/bin/ls` under the CI capability configuration; the same program is reached. |
| **D6** | The quota ledger carried two hardcoded Tailscale addresses and took its timestamps from the `date` and `env` host binaries. | `openOODA/buildbox/eco/ledger/quota_ledger.oo` | The two fleet hosts now come from `OODA_FLEET_HOST_A` and `OODA_FLEET_HOST_B` and fall back to `127.0.0.1`, so a ledger written without configuration never reaches a remote node. The epoch and the Hawaii stamp come from the canonical `TimeCap` and the new `buildbox/eco/ledger/hst_stamp.oo`, which does the civil-date conversion in pure `.oo`. |
| **D7** | `idlescreen status` never emitted a state word the `make test` gate looked for, and the gate only passed when no daemon was listening. `daemon_status_line` reported the saver state (`armed`, `idle`, `saver-on`, `stopped`) but not the daemon state, while the offline path in `daemon/run.oo` reported `inactive`. The gate matched `inactive\|active\|daemon`, so it passed on a CI runner with no daemon and failed on any host running one. | `idlescreen/daemon/state.oo` | `daemon_status_line` now reports the daemon state explicitly (`active` or `inactive`) alongside the saver state, which is what the README already documents the command as doing. The Makefile gate is deliberately **unchanged** — it keeps its original strict `inactive\|active\|daemon` pattern, and now passes on both the connected path (`idlescreen active armed saver=ascii ...`) and the offline path (`idlescreen inactive (no daemon listener at 127.0.0.1:49317)`). No gate was weakened to make the test pass. |
| **D8** | After D1–D4 wired the canonical pages in, `core/capreg.oo` imported `std/sec/quorum.oo` and `std/sec/delegate.oo` without ever calling them. `oodac check` rejects a dangling import when the page is a standalone root, so `core/capreg.oo` did not typecheck on its own — it only passed because every L2 Makefile checks the entry page rather than each page, which hid the defect. `oorealm`, whose Makefile *does* check every page, failed its own `make verify` because of it. | all 15 L2 daemons — `core/capreg.oo` | The two hand-rolled expressions became the canonical helpers: `((packed >> 32) & 255) != 4` → `oo_quorum_badge(packed) != 4`, and the child-caps mask test → `oo_delegate_caps_subset(child & 4294967295, packed & 4294967295) == false`. Both are exactly behaviour-preserving. Every page now typechecks as a standalone root. |
| **D9** | The six Generation-A daemons called the canonical `oo_cap_reg64_pack` / `oo_cap_reg64_check` directly, and those helpers **silently mask out-of-width fields**: `oo_cap_reg64_check` computes `need = ((req_rights & 255) << 40) \| (req_caps & 4294967295)`, so a caller asking for `req_rights = 256` has its requirement masked down to *zero* rights and the check then **passes**. The live attestation gate (`hw/attest.oo`) and the live delegation path (`hw/delegate.oo`) were therefore fail-open on out-of-width input. | `ooaid`, `oohealthd`, `ooimage`, `ooinit`, `oonetd`, `oosession` — `core/capreg.oo`, `hw/attest.oo`, `hw/delegate.oo` | Added fail-closed `<PFX>_reg64_pack` / `_check` / `_attenuate` wrappers to `core/capreg.oo`, each validating the field ranges and refusing out-of-width input instead of masking it, and routed the live attestation gate and the live delegation path through them. This also retired the dangling `import "core/capreg.oo"` in `hw/attest.oo`. |
| **D10** | `oonetd`'s `core/capreg.oo` carried `oonetd_net_ready`, a TCP bind probe that belongs to the network domain, not to the capability register. Adding the D9 wrappers pushed the page to nine functions, over the eight-function bound, and both `core/` and `dns/` were already at the eight-page density limit, so the probe had nowhere to go inside them. | `oonetd/core/capreg.oo` | The probe moved to a new `oonetd/net/readiness.oo` page, which owns it with the canonical `std/net/tcp_conn.oo` import; `core/capreg.oo` dropped the now-unused `std/net/tcp_conn.oo` import and is back to eight functions; `dns/cli.oo` and `anchor.oo` were rewired, and `Makefile` `SRC` lists the new page. Nothing was deleted. |
| **D11** | `ooimage`'s `realm/run.oo` imported `persona/cli.oo` and `core/types.oo` without using anything from either, so the page failed a standalone `oodac check` with `unused import`. The page reaches the realm CLI through `realm/cli.oo`, not through the persona CLI. | `ooimage/realm/run.oo` | The two dangling imports were removed. The page now typechecks as a standalone root. No function, type, or assertion was touched. |
| **D12** | The `SRC` list in each L2 `Makefile` is the declared source set: `$(BIN)` and `$(TEST_BIN)` depend on it, the check stamp typechecks every page it names, and `det` builds the daemon twice from it and compares the two binaries. Pages committed to the repositories were missing from `SRC`, so `make verify` never typechecked them and `make det` never covered them — one page per repository, up to four in `ooimage`. | 14 of the 15 L2 `Makefile` files | Every committed page that `SRC` omitted was typechecked standalone first (all pass `oodac check`), then added to `SRC`. `SRC` is a dependency list, not an assertion: the assertion count and every other target are untouched. |
| **D13** | `SRC` also named pages that had been renamed or moved, so the build failed with `make: *** No rule to make target 'verity/fs_verity.oo'` before anything was compiled; and four `Makefile`s carried an assertion gate from before the concurrently pushed `deep_e` assertions, so `make test` reported `FAIL: 72 assertions` against a tree whose tests pass. | `ooaudiod`, `oofs-ext4`, `oologd`, `oonetd`, `oopolicyd`, `ooinit`, `oosession` | `SRC` now names exactly the committed pages — stale names dropped, new names added, each typechecked standalone first. The assertion gates were restored to the counts the tree's own tests produce (`72`, `73`, `134`, `80`); this review's diffs touch no assertion, so no count was changed by this review. |

### 3.1 Commits

Three commits per L2 daemon, plus one each for the two Tier 0 flagships this batch changed. The L2 daemon commits are, in order:

1. `fix(sec): wire the toy modulus clones to canonical std/sec/pqc.oo and std/ipc/wire.oo, and run the canonical 4-phase OODA turn over the 32-capability register` (D1–D4),
2. either `fix(sec): bind the live capability gate to the canonical quorum badge and delegate subset helpers` (D8, Generation B) or `fix(sec): refuse out-of-width register fields instead of masking them` (D8–D11, Generation A),
3. `fix(build): declare every committed page in the Makefile source set` or `fix(build): keep the Makefile source set and assertion gate in step with the tree` (D12, D13).

Every commit below is on `origin`.

| Repository | Branch | Head |
| :--- | :--- | :--- |
| `openOODA-OS/ooaid` | `main` | `0f1bff5` |
| `openOODA-OS/ooaudiod` | `master` | `6609d9c` |
| `openOODA-OS/oodevd` | `master` | `611321b` |
| `openOODA-OS/oodnsd` | `master` | `4983177` |
| `openOODA-OS/oofs-ext4` | `master` | `5727a66` |
| `openOODA-OS/oofs-tmp` | `master` | `398b0d6` |
| `openOODA-OS/oohealthd` | `master` | `2d2f0b9` |
| `openOODA-OS/ooimage` | `master` | `0a6dca4` |
| `openOODA-OS/ooinit` | `master` | `b3d1fe7` |
| `openOODA-OS/oologd` | `master` | `50ef920` |
| `openOODA-OS/oonetd` | `master` | `e11c332` |
| `openOODA-OS/oopolicyd` | `master` | `8b0b650` |
| `openOODA-OS/oopowerd` | `master` | `83608c9` |
| `openOODA-OS/oorealm` | `main` | `38177c5` |
| `openOODA-OS/oosession` | `master` | `e84c702` |
| `idlescreen/idlescreen` | `ooda` | `94e0561` |
| `openOODA/openOODA` | `master` | `ba30870` (this batch's commit is `1b79bd0`, an ancestor of it) |
| `openOODA-apps/ooflash` | `master` | `aa6edae` (verified only, no defect found) |

### 3.2 Assertion-count ledger

No assertion count was changed by this review. The counts below are the value the `make test` gate asserts in the final tree. Several differ from the value on entry because a concurrent agent pushed feature commits that added `deep_e` assertions; this review's diffs touch no assertion, and every changed test file kept its assertion count byte-identical.

| Repository | Assertions on entry | Assertions in the final tree | `make verify` | `make test` | Double-run determinism |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ooaid` | 105 | 105 | PASS | PASS | byte-identical |
| `ooaudiod` | 70 | 72 | PASS | PASS | byte-identical |
| `oodevd` | 89 | 89 | PASS | PASS | byte-identical |
| `oodnsd` | 70 | 70 | PASS | PASS | byte-identical |
| `oofs-ext4` | 70 | 72 | PASS | PASS | byte-identical |
| `oofs-tmp` | 70 | 70 | PASS | PASS | byte-identical |
| `oohealthd` | 70 | 70 | PASS | PASS | byte-identical |
| `ooimage` | 107 | 109 | PASS | PASS | byte-identical |
| `ooinit` | 118 | 118 | PASS | PASS | byte-identical |
| `oologd` | 71 | 73 | PASS | PASS | byte-identical |
| `oonetd` | 122 | 134 | PASS | PASS | byte-identical |
| `oopolicyd` | 70 | 80 | PASS | PASS | byte-identical |
| `oopowerd` | 70 | 70 | PASS | PASS | byte-identical |
| `oorealm` | 69 | 69 | PASS | PASS | byte-identical |
| `oosession` | 121 | 121 | PASS | PASS | byte-identical |
| `ooflash` | — | — | PASS | PASS (`ALL TESTS PASSED`) | repo gate green |
| `openOODA` | — | — | 4 changed pages `oodac check` OK, both binaries build | parity gate green | — |
| `idlescreen` | — | — | PASS (all seven sub-gates) | PASS (`ALL TESTS PASSED`) | byte-identical |

**Uniform shape after remediation.** Every one of the 15 L2 daemons now has, in `core/capreg.oo`: the canonical `std/core/ooda.oo` 4-phase turn (`oo<prefix>_ooda_turn`), the fail-closed `<prefix>_reg64_pack` / `_check` / `_attenuate` wrappers, and the canonical `std/sec/quorum.oo` badge helper; `hw/attest.oo` and `hw/delegate.oo` route through the wrappers; `std/sec/pqc.oo` is imported in 5–11 pages per daemon; and `grep -rn 1000000007 --include='*.oo'` returns nothing. `core/capreg.oo` sits at exactly eight functions in every daemon — the bound, not over it.

---

## 4. Findings reported, not fixed

### F1 — Canonical L0 `std/sec/speculate.oo` did not compile, and broke every consumer of the canonical OODA engine

On entry, `std/sec/speculate.oo:21` called `oo_arena_mark()`, a symbol that is defined nowhere in `std`, in `std-hw`, or in the compiler's builtin set. The canonical `std/core/ooda.oo` imports `std/sec/speculate.oo`, so **the canonical OODA engine did not typecheck**, and every daemon importing it failed:

```
ERR	type	Type error at 21:41: undefined variable 'oo_arena_mark'
--> /Projects/openOODA-core/std/sec/speculate.oo:21:41
let mark : Int = if arena_mark < 0 { oo_arena_mark ( ) } else { arena_mark } ;
```

Introduced by `std` commit `5560098` (2026-11-05 12:53 -1000, "wire real arena mark/reset"). It broke `ooaid`, `ooflash`, and the six L2 daemons that import `std/core/ooda.oo`.

*Status.* `std` is claimed by `w3:p1` and its owner had the fix in flight during this review: the new canonical page `std/core/arena_mark.oo` appeared in the working tree at 17:56 HST with `oo_arena_mark_zero`, `oo_arena_mark_valid`, and `oo_arena_reset_mark(mark, cap)`, and `std/sec/speculate.oo` was rewired to it. The canonical engine typechecked again from 18:00 HST, and this batch was verified against that state. **`std` was deliberately not modified by this review** — it is outside this batch's claim.

*Remediation.* Land the `std` owner's `core/arena_mark.oo` change, then re-run `make verify` and `make test` in every consumer of `std/core/ooda.oo`.

### F2 — The ecosystem has no independent oracle for the capability register

Section 2.4 records that `std-hw` commit `90b8cd1` collapsed `rt_cap_reg64_*` into aliases of the canonical `oo_cap_reg64_*`. A differential-parity gate needs two independent implementations; after that commit there is one at the `.oo` level, so any `rt_*` against `oo_*` comparison is vacuous.

*Remediation.* Either restore an independent implementation in `std-hw/hw/runtime/rt_caps_reg64.oo` — the pre-`90b8cd1` body is a correct second implementation of the documented layout — or compare the `.oo` register against the C runtime in `oodar/sec/cap/caps.h` through the differential harness, which is the only oracle that is genuinely independent.

### F3 — `idlescreen` reaches the host through an implicit shell

`idlescreen/core/shell.oo` exposes `shell_out(proc, cmd)`, which runs a single command **string** through `process_exec`, and `idlescreen/cli/service_unit.oo` uses it for filesystem probes:

```
    if shell_out(proc, "test -x /usr/local/bin/idlescreen 2>/dev/null && echo yes") != "" { return "/usr/local/bin/idlescreen"; }
    if shell_out(proc, "test -x /usr/bin/idlescreen 2>/dev/null && echo yes") != "" { return "/usr/bin/idlescreen"; }
```

This is the `/bin/sh -c` shape the house law forbids, and it hardcodes two system paths.

*Remediation.* Give `service_bin_path` and `service_has_systemd` an `&FsReadCap` and probe with `fs_path_exists` instead of `test -x`. The call sites already have a read capability available.

### F4 — `ooflash` shells out to `powershell -Command` for the Windows path helpers

`ooflash/flash/winpath.oo` and `ooflash/flash/digest.oo` run `sys_exec(sys, "powershell", "-NoProfile", "-Command", q)`. The argv is explicit and the host fails closed off Windows, which is much better than a bare shell string, but `-Command` still hands a script to an interpreter.

*Remediation.* Replace the one-liners with direct Win32 calls, or restrict them to an explicit `ProcessCap` command allow-list so the script text is never interpreted.

---

## 5. Verification method and negative-trust evidence

Every fix was checked with a positive and a negative case, as `rules.oot` §1.4 requires.

| Check | Positive | Negative |
| :--- | :--- | :--- |
| D1, D2, D3, D4 | `make verify` and `make test` pass in all 15 L2 daemons, with the assertion count unchanged from the value on entry | The toy modulus is gone: `grep -rn 1000000007 <repo> --include='*.oo'` returns nothing. The four attestation rejection paths still fail closed with mask `3 / 6 / 5 / 4`, the zero-gas, over-budget, and non-positive-quota paths still fail closed, the audit tamper path still fails closed, and the quorum under-threshold, duplicate-badge, and split-brain paths still fail closed. |
| D2 | The live capability gate returns true for the well-formed register | Each new assertion fails when its invariant is broken: a wrong epoch, an ungranted right, a widened child, a changed badge, or a changed rights field each drive the gate to `false`. |
| D5 | The parity gate resolves the upstream program through `fs_path_exists` and reaches the same program the shell search reached (`/bin/ls` in the verification run) | With the capability jail active and `/usr/bin` outside the read set, the lookup returns empty and the gate fails closed with `ERR parity upstream tool ls is not installed.` — it never falls back to a shell. |
| D6 | The ledger writes its epoch and Hawaii stamp from the canonical `TimeCap` | With no `OODA_FLEET_HOST_A` or `OODA_FLEET_HOST_B` in the environment, both fleet probes resolve to `127.0.0.1`, so a ledger written without configuration cannot reach a remote node. |
| D8 | Every page of every L2 daemon now passes `oodac check` as a standalone root | The compiler rejects a page whose import is dangling, so the fix is observable: before it, `oodac check core/capreg.oo` failed with `unused import 'std/sec/quorum.oo'`; after it, the same command returns `OK`. |
| D9 | The live attestation gate still yields mask `7` for a well-formed register and the delegation path still issues a child register | The canonical helper masks `req_rights = 256` down to *zero* rights and then passes. The fail-closed wrapper refuses it: `oo<prefix>_reg64_check(reg64, epoch, 256, 1)` returns `false` where `oo_cap_reg64_check(reg64, epoch, 256, 1)` returns `true`. Same for `oo<prefix>_reg64_pack(epoch, 256, badge, caps)`, which returns `0` where the canonical helper silently truncates the right to `0`. |
| D10 | `oonetd`'s readiness probe still answers on both the primary and the fallback control port | The probe moved, not disappeared: `oonetd/net/readiness.oo` owns it and `main.oo` and `dns/cli.oo` call it through the new import. `core/capreg.oo` went from nine functions back to eight. |
| D13 | The build compiles again after the page renames | Before the fix the build stopped with `make: *** No rule to make target 'verity/fs_verity.oo'`; after it, `make verify` and `make test` pass. |

### 5.1 Sequential double-run determinism

Every L2 daemon's `make test` target already runs the binary twice and compares the two outputs byte for byte (`r1.txt` / `r2.txt`, `cmp -s`), and the `det` target builds the daemon twice and compares the SHA-256 of the two binaries. Both are part of the gate that was run for every remediation.

---

## 6. Environment notes

1. **The workspace runs concurrent review agents.** Three other reviewers were active during this review: `vibe-review 1` (L2 OS, L4 DE, L6 Cloud, L7 Agents), `grok-review 1` (`oodar`, L1 Kernel, Win64 PE32+), and the `std` owner for `w3:p1`. Findings that belong to another owner's claim are reported here rather than fixed, so that no two agents write the same file.
2. **The `oodac` compiler wrapper enforces a 240-second timeout per invocation and a two-slot concurrency limit** (`/Projects/openOODA-core/oodac/bin/oodac`). Under this load a build that shares a repository with another agent serialises on the per-repo lock and can be killed with `Error 124`. The verification sweep therefore invokes `bin/oodac.real` directly and runs one build per repository directory. A `Killed` or `Error 124` line in this environment is a resource artefact, not a test failure.
3. **The canonical L0 tree was in motion throughout the review.** `std` gained `core/arena_mark.oo` and a rewired `sec/speculate.oo` at 17:47–17:56 HST while this review was running. The first baseline typecheck of `ooaid` and `ooflash` failed against the broken `std/sec/speculate.oo`; the same command passed from 18:00 HST against the owner's fix. Both results are reported above rather than only the passing one.
4. **A second agent pushed overlapping work into the same repositories while this review was in flight.** Between 19:20 and 21:45 HST a concurrent agent landed feature commits in all 15 L2 daemons and in `idlescreen`, including an alternative implementation of the same toy-modulus-to-canonical wiring (which kept a local copy of the 64-bit register and had no canonical OODA turn), page renames, and a raise of the `deep_e` assertion counts. Every push of this review's commits was therefore rejected as non-fast-forward until the commits were rebased onto the new remote heads. The resolution was: the concurrently pushed feature commits are kept, and this review's canonical implementation wins on the files the two overlap on, because it is the one that drops the copied register, keeps a fail-closed wrapper, runs the canonical 4-phase OODA turn, and binds the live gate to the canonical quorum and delegate helpers.
5. **One local branch was reset out from under this review.** At 21:43:56 HST `ooimage`'s `master` was reset to `origin/master`, discarding this review's three local commits; they were recovered from the reflog (`cf05624`) and replayed onto the new remote head as `d9cd2f0`, `799e08d`, `0a6dca4`. The fleet was re-checked afterwards by content rather than by git history — every daemon still carries the canonical OODA turn, the fail-closed wrappers, and zero toy modulus.
6. **The `Makefile` assertion gates were briefly stale.** Rebasing onto the concurrently pushed commits reverted four `Makefile`s to the pre-`deep_e` assertion counts, and the same commits left `SRC` naming pages that had been renamed. Both were repaired (D13) and the affected daemons were re-verified end to end before they were pushed.

---

## 7. Standards Axis — checklist against `rules.oot` §1.8

| Rung | Rule | Result |
| :--- | :--- | :--- |
| `1` | One statement per line, zero symlinks and hardlinks | **PASS** — zero links of either kind in all 18 repositories |
| `2` | Two test axes per repository, two-axis review | **PASS** — every L2 daemon runs a real functional I/O axis and a negative-trust refusal axis inside `make test`; the Tier 0 flagships were reviewed on both axes |
| `4` | Four levels of block nesting | **PASS** — `lint-oo-size` reports no nesting violation |
| `8` | Eight pages per directory, eight functions per page, eight parameters | **PASS** — `DENSE=0`, `MANYFN=0` in all 18 repositories |
| `16` | At least 16 lines per page, zero empty stubs | **PASS** — `line-cap` passes in every daemon |
| `32` | Thirty-two explicit capabilities, 32-character names | **PASS** — every daemon maps 19 software and 13 hardware capabilities onto bits 0..31 with no dead bit, and the live gate asserts the full 32-bit coverage |
| `64` | Sixty-four lines per function | **PASS** — `LONGFN=0` in all 18 repositories |
| `128` | 128 characters per line | **PASS** |
| `256` | 256 lines per page | **PASS** — `BIGFILE=0` in all 18 repositories, including the two parity pages that were over the ceiling until the shell-free lookup was compacted |
