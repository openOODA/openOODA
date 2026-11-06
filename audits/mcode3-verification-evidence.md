# mcode-review 3 — Verification Evidence Log

**Date:** 2026-11-05 (18:20–21:50 HST)
**Scope:** 18 repositories — Tier 0 flagships and the L2 `openOODA-OS` batch.

Every line below was produced by an independent re-verification sweep run after the
remediation commits were in place and after the commits were rebased onto the
concurrently pushed remote heads. The sweep script is
`audits/mcode3-final-sweep.sh`: per repository it runs `lint-oo-size`, then
`make verify`, then `make test` twice, sequentially, and compares the two test
outputs byte for byte after the make build echo is filtered out.

`DETERMINISM: Run_1 == Run_2` means the two sequential `make test` runs produced
byte-identical test output. `ALL TESTS PASSED` is the daemon's own final line.

---

## L2 `openOODA-OS` batch

| Repository | Branch | `lint-oo-size` | `make verify` | `make test` (run 1 / run 2) | Determinism |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ooaid` | `main` | 0 violations | PASS | `PASS: test suite (105 assertions) ALL TESTS PASSED` | Run_1 == Run_2 |
| `ooaudiod` | `master` | 0 violations | PASS | `PASS: 72/72 assertions ALL TESTS PASSED` | Run_1 == Run_2 |
| `oodevd` | `master` | 0 violations | PASS | `PASS: 89 assertions ALL TESTS PASSED` | Run_1 == Run_2 |
| `oodnsd` | `master` | 0 violations | PASS | `PASS: 70/70 assertions ALL TESTS PASSED` | Run_1 == Run_2 |
| `oofs-ext4` | `master` | 0 violations | PASS | `PASS: 72/72 assertions ALL TESTS PASSED` | Run_1 == Run_2 |
| `oofs-tmp` | `master` | 0 violations | PASS | `PASS: 70/70 assertions ALL TESTS PASSED` | Run_1 == Run_2 |
| `oohealthd` | `master` | 0 violations | PASS | `PASS: 70/70 assertions ALL TESTS PASSED` | Run_1 == Run_2 |
| `ooimage` | `master` | 0 violations | PASS | `PASS: 109/109 assertions ALL TESTS PASSED` | Run_1 == Run_2 |
| `ooinit` | `master` | 0 violations | PASS | `PASS: 118 assertions ALL TESTS PASSED` | Run_1 == Run_2 |
| `oologd` | `master` | 0 violations | PASS | `PASS: 73/73 assertions ALL TESTS PASSED` | Run_1 == Run_2 |
| `oonetd` | `master` | 0 violations | PASS | `PASS: 134/134 assertions ALL TESTS PASSED` | Run_1 == Run_2 |
| `oopolicyd` | `master` | 0 violations | PASS | `PASS: 80/80 assertions ALL TESTS PASSED` | Run_1 == Run_2 |
| `oopowerd` | `master` | 0 violations | PASS | `PASS: 70/70 assertions ALL TESTS PASSED` | Run_1 == Run_2 |
| `oorealm` | `main` | 0 violations | PASS | `PASS: test suite (69 assertions) ALL TESTS PASSED` | Run_1 == Run_2 |
| `oosession` | `master` | 0 violations | PASS | `PASS: 121/121 assertions ALL TESTS PASSED` | Run_1 == Run_2 |

`lint-oo-size` reported `# violations: BIGFILE=0 MANYFN=0 LONGFN=0 DENSE=0 files_with_size_violation=0`
for each of the 15.

## Tier 0 flagships

| Repository | Branch | `lint-oo-size` | `make verify` | `make test` | Determinism |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `idlescreen/idlescreen` | `ooda` | 0 violations | PASS (Page Rule, file law, academy, density, vocabulary, shape, `oodac check holds on all .oo files`) | `ALL TESTS PASSED` | Run_1 == Run_2 |
| `openOODA-apps/ooflash` | `master` | 0 violations | PASS | `ALL TESTS PASSED` (including `double-run output determinism`) | repo gate green |
| `openOODA/openOODA` | `master` | 0 violations | 4 changed pages `oodac check` → `OK`; both binaries build `OK_PURE_NATIVE` | parity gate green, see below | — |

`openOODA` has no root `Makefile`; its gate is the parity and ledger binaries.

### `openOODA` parity lookup — positive and negative

```
# positive: the lookup resolves the upstream program without a shell
OODA_NO_JAIL=1 ... parity_find_upstream("ls")  ->  /bin/ls

# negative: with the capability jail active and /usr/bin outside the read set
ERR parity upstream tool ls is not installed.
```

The negative case never falls back to a shell: the lookup probes the standard
program directories and every `PATH` entry through `fs_path_exists`, and when
nothing is found it fails closed.

### `idlescreen` status gate — both paths

```
# connected path
$ ./bin/idlescreen status
idlescreen active armed saver=ascii scene=0 timeout=120s inhibitors=0

# offline path (no daemon listener)
$ ./bin/idlescreen status
idlescreen inactive (no daemon listener at 127.0.0.1:49317)
```

The `make test` gate matches `inactive|active|daemon` — the original strict
pattern, unchanged. It passes on both paths because the daemon now reports its
own liveness.

---

## Fleet-wide content check after the final push

```
repo       ooda_turn wrappers quorum_badge pqc_imp toy_mod  capreg_fns
ooaid       2          3        1            9       0         8
ooaudiod    2          3        1            7       0         8
oodevd      2          3        1            6       0         8
oodnsd      2          3        1            5       0         8
oofs-ext4   2          3        1            7       0         8
oofs-tmp    2          3        1            5       0         8
oohealthd   2          3        1            6       0         8
ooimage     2          3        1            9       0         8
ooinit      2          3        1            9       0         8
oologd      2          3        1            7       0         8
oonetd      2          3        1           11       0         8
oopolicyd   2          3        1            7       0         8
oopowerd    2          3        1            6       0         8
oorealm     2          3        1            7       0         8
oosession   2          3        1            9       0         8
```

* `ooda_turn` — the canonical `std/core/ooda.oo` 4-phase turn is present in `core/capreg.oo`.
* `wrappers` — the fail-closed `<prefix>_reg64_check` / `_reg64_pack` wrappers are used by all three of `core/capreg.oo`, `hw/attest.oo`, `hw/delegate.oo`.
* `quorum_badge` — the live capability gate calls the canonical `std/sec/quorum.oo` badge helper.
* `pqc_imp` — pages importing the canonical `std/sec/pqc.oo`.
* `toy_mod` — occurrences of `1000000007` in any `.oo` file: **0**.
* `capreg_fns` — functions in `core/capreg.oo`: **8**, exactly at the bound.

## Scripts

| Script | Purpose |
| :--- | :--- |
| `mcode3-final-sweep.sh` | the verification sweep: lint, `make verify`, `make test` twice, determinism |
| `mcode3-resolve-sweep.sh` | the same sweep, second log file, for a parallel run |
| `mcode3-rebase.sh` | rebase onto the remote head, keep the canonical implementation, de-duplicate imports |
| `mcode3-rebase-and-check.sh` | rebase one repository and report whether the tree changed |
| `mcode3-sync-src.py` | make the Makefile `SRC` list name exactly the committed pages |
| `mcode3-d9-failclosed.py` | the D9 transformation: fail-closed register wrappers in the Generation-A daemons |
| `mcode3-d12-src.py` | the first pass of the D12 transformation |
| `mcode3-push-on-sweep.sh` | push each repository as its sweep entry completes |
