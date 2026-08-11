# openOODA sprint

## Pin
| Item | Value |
|------|--------|
| Release | `v0.184.0-alpha` (stay alpha) |
| Focus | Monofile line pressure (next power-law >600 batches); true residual only |
| Tip (product `ooda`) | Source `ffb9a03` + host **m181 pure dual-green** (research pure_g10: caret+hello+bitwise_ops_smoke PASSED). Product binary may still be m174 residual on disk if m181 not product-flipped — do not claim product tip-flip beyond proven host research. |
| Pure research | **pure9→pure10** dual-green **FIXED** — caret `^` lex + bc ARROW skip; evidence `issue56_prove.log`, `smoke_pack_m181.log` |
| Beta | **Not claimed** |

## Closed this wave (do not re-open)

| Item | Disposition |
|------|-------------|
| **ZT-1..ZT-6** fail-closed EnvCap/FsCap | **FIXED** — `oo_process_policy_getenv` (OODA_/OO_ only); `verify_human` dual-cap; list/ffi/tls policy getenv; ThreadCap/GpuCap in `is_cap_type`. Evidence: C probe `zt_full.log` fails=0; pure emit dual-cap + manual link refuse/allow `zt_product_path_a.log`. Commit `ooda` `4c208c4`. |
| M176 **#40** soft-pass e2e | **FIXED** — pure soft-pass tier scripts deleted (`qa` `c97b281`) |
| M176 **#41** loose e2e | **FIXED** — fail-closed targets; empty/wrong output fails (`qa` `372c489`) |
| M176 **#42** doc-vs-tree | **FIXED** — 10 honesty `[STATUS:]` tags (`openOODA` `4c0c9d4`) |
| M176 **#43** harness quality | **FIXED** — phase5a jq, expect_fail signature, wasm no soft-pass (`qa` `52a016e`) |
| M177 **#44–#49, #52–#53** honesty/install/runner totals | **FIXED** — profile README, install v0.184, README→PM, Playground→Home, version retag, e2e summary export, drop 100% claim |
| M177 **#50–#51** runner false-pass | **FIXED** — residual exit 77, strip bare ERR, WASM shape, stdlib FAIL if missing (`qa` `f7eb797`) |
| Issue **#15** listed monofiles | **FIXED** — rsa_pss/cell/battery/dispatch/inference/audit shims (`std` `3e2eab7`) |
| Power-law **>600** batch (ckks/bgv/…) | **FIXED** path A — ckks/bgv/gaussian/fusion M172 shims (`std` `2de23fa`) |
| Issue **#7** remainder | **FIXED** earlier — fhe/anneal/aero/behavior shims |
| Issue **#6** remainder + leftover parens | **FIXED** — crypto/cps/fin/bio then quantum/edge/enterprise/gui/grid/robot/3d (`std` `47a93b9`, `3f619f0`) |
| M178 **#56** pure dual-green | **FIXED** — lex caret `^` + bc_emit ARROW consume; pure9→pure10 dual-green (caret run=3, hello green, bitwise_ops_smoke PASSED). Commit `ooda` `ffb9a03`. Evidence: `issue56_prove.log`, `smoke_pack_m181.log`. |
| M178 **#57** top-5 monofiles | **FIXED** — bfv/bulletproofs/pe/navigation/hsm M172 shims (`std` `f345acc`); shims ≤54 lines each |
| M178 **#58** doc honesty | **FIXED** — DESIGN/SPEC residual STATUS tags (`openOODA` `17d686d`, +85 tags cluster) |
| M178 **#59** audit CI | **FIXED** — audit README disk + CI gate (`openOODA` `e939dbd`, `3c49df1`) |
| M178 **#60** leftover-#6 parens | **FIXED** — paren field-access batch leftover domains (`std` `3f619f0`) |

Prior closed: #11–14, #9 single-file, #12 rails, free-name Int mistypes, mtls/waf/wireguard/jwt/spiffe/ids/ztidentity/collision/kinematics.

## M178 closed summary (queue retired)

M178 open queue (#56–#60) is **done**. Pure dual-green gate met at source `ffb9a03` / host m181 pure research. Next highest-E work is **power-law monofile splits** on the remaining ~55 files still >600 lines (next worst: dwarf, tss, orca, tpm, disasm, …). Do not re-open caret/ARROW pure residual — that claim is stale.

## Residual (path A — next model)

| Item | What blocks | Evidence |
|------|-------------|----------|
| **Library files still >600** | **55** monofiles remain after #57 top-5 split. Power-law next batches (≤10 per rotation). | Regenerated inventory below; bfv/bulletproofs/pe/navigation/hsm **dropped** (shimmed) |
| **Issue #9/#10 multi-module** | Absolute LINE; lit_env pollution (xfail same-param-name) | residual |
| **Issue #13 doc honesty remainder** | #58 tagged major DESIGN/SPEC residual clusters; any untagged marketing phrasing is light residual only — not a rewrite mandate | residual-note lightly |
| **250 New Domain Libraries** | Cannot write production-ready code due to compiler alpha limits (missing `List[Struct]` lowering, raw ptr MMIO, `import "C"` FFI gen, native `&str`, async actors). Writing stubs would violate RULES §1.3 (no half-truths). | Catalog of 250 proposed libraries logged; compiler backend depth required first. |
| **Product host vs research** | Host research **m181 pure dual-green** proven; if product-installed binary is still m174, that is install lag only — source tip is `ffb9a03`. Prefer honest pin: source tip + m181 research quality. | pure_g10 dual-green; product residual smokes on pure tip in prove logs |

## Residual named (full DESIGN — once)

Full SMT · free-form multi-code · full HITL interactive harness · actor supervision · real GPU · unrestricted dlopen · native `&str` · nested `List[Struct]` · product `&mut T` · object-cap crypto · SOCK_RAW · full async I/O · OS rlimit heap · Tier C · interactive playground · pkg/LSP/registry · beta **not claimed**.

## Oversized Library Files (>600 lines)

*Regenerated 2026-08-11 from `std/src/ooda` after #57 shims. Count: **55**. Top-5 (bfv, bulletproofs, pe, navigation, hsm) no longer listed.*

* `std/src/ooda/sec/sys/dwarf.oo` (968 lines)
* `std/src/ooda/sec/crypto/tss.oo` (964 lines)
* `std/src/ooda/auto/orca.oo` (952 lines)
* `std/src/ooda/sec/crypto/tpm.oo` (931 lines)
* `std/src/ooda/sec/sys/disasm.oo` (910 lines)
* `std/src/ooda/sec/crypto/kms.oo` (902 lines)
* `std/src/ooda/aero/attitude.oo` (897 lines)
* `std/src/ooda/aero/telemetry.oo` (881 lines)
* `std/src/ooda/grid/loadflow.oo` (869 lines)
* `std/src/ooda/aero/formation.oo` (866 lines)
* `std/src/ooda/crypto/keys.oo` (855 lines)
* `std/src/ooda/sec/crypto/zkstark.oo` (854 lines)
* `std/src/ooda/sec/crypto/kmac.oo` (852 lines)
* `std/src/ooda/sec/sys/ebpf.oo` (831 lines)
* `std/src/ooda/quantum/gates.oo` (831 lines)
* `std/src/ooda/quantum/circuit.oo` (830 lines)
* `std/src/ooda/sec/crypto/secp256k1.oo` (823 lines)
* `std/src/ooda/bio/smiles.oo` (801 lines)
* `std/src/ooda/sec/crypto/shamir.oo` (800 lines)
* `std/src/ooda/sec/sys/elf.oo` (776 lines)
* `std/src/ooda/sec/sys/objcap.oo` (774 lines)
* `std/src/ooda/sec/crypto/zksnark.oo` (769 lines)
* `std/src/ooda/sec/crypto/falcon.oo` (767 lines)
* `std/src/ooda/aero/orbit.oo` (759 lines)
* `std/src/ooda/crypto/zkp.oo` (756 lines)
* `std/src/ooda/physics/fluid.oo` (744 lines)
* `std/src/ooda/sec/crypto/plonk.oo` (742 lines)
* `std/src/ooda/fin/yield.oo` (738 lines)
* `std/src/ooda/sec/sys/landlock.oo` (728 lines)
* `std/src/ooda/robot/motors.oo` (726 lines)
* `std/src/ooda/sec/crypto/ed25519.oo` (723 lines)
* `std/src/ooda/fin/credit.oo` (714 lines)
* `std/src/ooda/sec/crypto/groth16.oo` (709 lines)
* `std/src/ooda/sec/crypto/dilithium.oo` (684 lines)
* `std/src/ooda/sec/crypto/double_ratchet.oo` (677 lines)
* `std/src/ooda/physics/soft.oo` (664 lines)
* `std/src/ooda/robot/slam.oo` (660 lines)
* `std/src/ooda/sec/crypto/sha3.oo` (652 lines)
* `std/src/ooda/auto/mpc.oo` (650 lines)
* `std/src/ooda/physics/raycast.oo` (645 lines)
* `std/src/ooda/auto/occupancy.oo` (644 lines)
* `std/src/ooda/aero/tvc.oo` (638 lines)
* `std/src/ooda/sec/crypto/blake3.oo` (635 lines)
* `std/src/ooda/fin/hft.oo` (633 lines)
* `std/src/ooda/grid/solar.oo` (630 lines)
* `std/src/ooda/grid/wind.oo` (629 lines)
* `std/src/ooda/sec/sys/ima.oo` (618 lines)
* `std/src/ooda/physics/rigid.oo` (614 lines)
* `std/src/ooda/aero/propulsion.oo` (614 lines)
* `std/src/ooda/auto/lanelet.oo` (613 lines)
* `std/src/ooda/bio/protein.oo` (610 lines)
* `std/src/ooda/sec/sys/cfi.oo` (606 lines)
* `std/src/ooda/sec/sys/audit.oo` (606 lines)
* `std/src/ooda/bio/phylo.oo` (602 lines)
* `std/src/ooda/sec/crypto/chacha20.oo` (601 lines)

## Next power-law monofile batches (residual, not open M178 queue)

Pick worst 5–10 by line count per rotation; M172 shim pattern (`*_types` / `*_ops` / `*_engine` / `*_stubs` + thin re-export). Suggested next-5: **dwarf, tss, orca, tpm, disasm**. Keep PRs ≤10 files; re-prove `oodac check` under ambient quota.

## Background hygiene (low priority — do not re-label as M178)

* Workspace debris (log files, ad-hoc fix_*.py, codegen `*.tmp.c`) — cleanup only when touching those paths.
* Harness integrity deeper passes (seed precedence, negative-test exit bands) — residual beyond M177 runner false-pass close.
* Plain-English expansion of remaining acronym-heavy closed tables — optional polish.
