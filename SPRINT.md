# openOODA sprint

## Pin
| Item | Value |
|------|--------|
| Release | `v0.184.0-alpha` (stay alpha) |
| Focus | Second-gen pure dual-green + caret on pure tip; remaining >600 library splits |
| Tip (product `ooda`) | `4317efb` source + **host binary m174** (product residual smokes green, including caret `^`) |
| Pure research | **m180** = first pure multi link green from m178 free-name host (`OK_PURE_MULTI`); not product tip (caret lex fail; 2nd pure rebuild 8 Result/OoStr errs) |
| Beta | **Not claimed** |

## Closed this wave (do not re-open)

| Item | Disposition |
|------|-------------|
| Pure multi **first** rebuild | **path A progress** — `oodac_pure_build.sh` with m178 host → executable pure binary (SCRATCH/m180). Re-emit core modules exit 0. |
| Issue **#7** listed remainder | **FIXED** — fhe, anneal, aerodynamics, behavior → shims ≤256 + modules check green (`std` commits f92567f, c24ad78) |
| Issue **#15** priority batch | **FIXED** — watermark, redteam, aml, attestation, prompt_filter split (`std` ff539c5) |
| Issue **#6** remainder batch | **FIXED** path A — +48 files (~1234 sites) sec/crypto, sec/cps, fin, bio (`std` 47a93b9); prior 41 in perf/sec/sys |

Prior closed: #11–14, #9 single-file, #12 rails, free-name Int mistypes, mtls/waf/wireguard/jwt/spiffe/ids/ztidentity/collision/kinematics.

## Open work (path A)

### 1. Pure multi dual-green (remaining gaps)
| Fact | Detail |
|------|--------|
| First pure link | Green (m178 → pure binary m180) |
| Second pure | **Fail** — 8 gcc: `OoStr` used as Result (`.ok`); pure tip emit quality residual |
| Caret on pure tip | **Fail** — `ERRlex Unexpected character '^'` (product m174 still green) |
| Done when | pure rebuild twice without rewrite; caret product green; m169 pack green on pure tip; install as product host |

### 2. Library files still >600 lines
New inventory (post-split wave) — still need M172-style shims, e.g.:
- `sec/crypto/{ckks,bgv,bfv,bulletproofs,hsm,tss,tpm,kms}.oo` (900–1300)
- `3d/gaussian.oo` (~1223)
- `auto/{fusion,orca}.oo` (~1100/952)
- `sec/sys/{pe,dwarf,disasm}.oo` (~900–990)
- `aero/{navigation,attitude,telemetry,formation}.oo` (~866–971)
- `grid/loadflow.oo` (~869)

### 3. Issue #15 remaining (300–600)
rsa_pss, cell, battery, dispatch, inference, audit (and any peers still monofile).

### 4. Issue #6 remainder domains
Still open domains outside closed batches (e.g. quantum, edge, enterprise, gui, grid, robot leftovers, 3d, …).

### 5. Issue #9/#10 multi-module residual
Multi-import absolute LINE; lit_env pollution (xfail same-param-name).

### 6. Issue #13 remaining doc honesty
~57 DESIGN/SPEC gaps beyond the 5 critical tags.

## Residual named (full DESIGN)
Full SMT · free-form multi-code · full HITL · actor supervision · real GPU · unrestricted dlopen · native `&str` · nested `List[Struct]` · product `&mut T` · object-cap crypto · SOCK_RAW · full async I/O · OS rlimit heap · Tier C · beta not claimed.

## Smokes (product tip m174)
- m169 residual closeout, typecheck rails, typecheck line — re-run on m174 after tip restore
- Pure tip: agy/cap_forge/m167/bitwise/malloc green; m169/caret not green

## M176 audit round 4 (3 subagents in parallel) — Grok follow-on

Three subagents in parallel audited: (a) weakest e2e tier scripts, (b) top 10 doc-vs-tree gaps, (c) test corpus quality. Findings below.

> **Provenance note:** these audits ran in this session's subagent context, not on the file system. The subagents read files directly. Where a subagent cited a specific file path, I have not re-verified that path exists at this exact commit. Findings are based on the subagent's reading; the file-system state at the time the subagents ran was the current main (post-Grok work).

### Issue #40 — 10 weakest e2e tier scripts are pure soft-pass (HIGH)
- **Severity:** HIGH (RULES §1.6 immune test violation — pass+fail proof required)
- **Files (top 10 structural always-pass):**
  1. `qa/e2e/01_tier1_feature_coverage/t1_f05_01_scope_drop_block_exit.sh` — empty target, baseline swallows anything, `else echo "PASS"` fallback. **Delete.**
  2. `qa/e2e/01_tier1_feature_coverage/t1_f05_02_scope_drop_fn_return.sh` — same pattern. **Delete.**
  3. `qa/e2e/01_tier1_feature_coverage/t1_f05_03_scope_drop_reassign.sh` — same. **Delete.**
  4. `qa/e2e/01_tier1_feature_coverage/t1_f05_04_scope_drop_str_list.sh` — same. **Delete.**
  5. `qa/e2e/01_tier1_feature_coverage/t1_f05_05_scope_drop_nested_blocks.sh` — same. **Delete.**
  6. `qa/e2e/01_tier1_feature_coverage/01_tier1_coverage.sh:40` — `run_e2e_cmd_dual "T1-F13-01" 0 "" ""` (empty target + empty baseline). **Tighten target to `"greet|Hello|world"` or delete.**
  7. `qa/e2e/02_tier2_boundary_corner/t2_f11_01_llvm_codegen_syntax_val.sh` — external `opt` missing, fallback `echo PASS`. **Delete or assert `opt rc==0` via `e2e_assert_exit_code`.**
  8. `qa/e2e/02_tier2_boundary_corner/t2_f09_05_wasm_codegen_validator.sh` — same pattern with `wasm-validate` missing. **Delete or assert `wasm-validate rc==0`.**
  9. `qa/e2e/03_tier3_pairwise_combinations/t3_11_jit_vm_scope_drop.sh` — empty target + baseline `residual|ERR|unknown command` swallows anything. **Delete.**
  10. `qa/e2e/03_tier3_pairwise_combinations/t3_14_ast_outline_jit_vm.sh` — same pattern. **Delete.**
- **Fix path:** delete rows 1–10 first. Zero signal, max noise. Then strip `|^$` and `|OK` from every `t2_f13_*` and `t2_f14_*` baseline. Then collapse OR'd target regexes in rows 11, 17–22, 24, 25 to their single meaningful clause.

### Issue #41 — 15 more e2e scripts have loose or-joined assertions (MEDIUM)
- **Severity:** MEDIUM (RULES §1.6 — pass+fail proof weakened but not absent)
- **Files (sample of 15):**
  - `qa/e2e/01_tier1_feature_coverage/t1_f13_05_vm_run_exit_code.sh:15` — target_rc=42 with empty target; baseline regex matches literal "42" and "rc=0" so any rc passes. **Tighten target to "42" only; remove baseline.**
  - `qa/e2e/02_tier2_boundary_corner/t2_f13_01_vm_run_no_gcc.sh:12` — `PATH="/usr/bin:/bin"` soft-fails on broken gcc; baseline `^$` swallows empty output. **Shadow gcc with stub; tighten target to "Hello World" only.**
  - `qa/e2e/02_tier2_boundary_corner/t2_f13_02_vm_run_div_zero_trap.sh:19` — OR-joined target `"ERR.*vm.*division by zero\|division by zero\|trap"`; baseline `usage\|OK\|^$`. **Tighten target to "division by zero"; remove `OK\|^$` from baseline.**
  - `qa/e2e/02_tier2_boundary_corner/t2_f13_03_vm_run_stack_overflow.sh:16` — same pattern. **Tighten to "stack overflow".**
  - `qa/e2e/02_tier2_boundary_corner/t2_f13_04_vm_run_missing_main.sh:15` — same. **Tighten to "missing main".**
  - `qa/e2e/02_tier2_boundary_corner/t2_f13_05_vm_run_syntax_error.sh:13` — baseline `error\|incompatible\|usage\|^$` matches any "error" substring. **Tighten target to "parse".**
  - `qa/e2e/02_tier2_boundary_corner/t2_f14_01_self_hosting_isolated_temp.sh:12` — `^$\|passed\|0 failures\|SUCCESS\|ok` matches empty output. **Tighten to "passed" only; remove `^$`.**
  - `qa/e2e/02_tier2_boundary_corner/t2_f14_04_self_hosting_fd_limit.sh:12` — `^$\|OK\|greet\|measured\|0` plus `\|\| true` masks actual check exit. **Delete or replace with `e2e_assert_exit_code`.**
  - `qa/e2e/02_tier2_boundary_corner/t2_f14_03_self_hosting_product_purity.sh:11` — `RS_COUNT=0\|PASSED` baseline swallows ERRs. **Tighten to only "RS_COUNT=0".**
  - `qa/e2e/02_tier2_boundary_corner/t2_f14_05_self_hosting_hash_verify.sh:11` — `echo 'FIXED-POINT BOOTSTRAP IDENTICAL'` always prints literal substring. **Delete.**
  - `qa/e2e/01_tier1_feature_coverage/t1_f14_03_ci_product_rail.sh:10` — `OK\|PASSED` matches anything. **Tighten to "RS_COUNT=0\|ci_product: PASSED".**
  - `qa/e2e/04_tier4_real_world_scenarios/t4_07_self_hosting_bootstrap_workflow.sh:8` — same loose pattern. **Tighten to "RS_COUNT=0".**
  - `qa/e2e/02_tier2_boundary_corner/t2_f14_02_self_hosting_line_limit.sh:12` — `echo "PASS: T2-F14-02"` fallback when script missing. **Delete fallback echo; wrap in `e2e_assert_exit_code`.**
  - `qa/e2e/02_tier2_boundary_corner/t2_f05_05_scope_drop_ret_retained.sh:19`, `t2_f05_01_scope_drop_early_ret_if.sh:22` — `"Native executable\|OK\|build\|oo_str_release\|main"` — `OK\|build` matches anything. **Tighten target to "oo_str_release" only.**
- **Fix path:** per-file tightening per the recommendations above. The t2_f13 cluster (5 files) and t2_f14 cluster (5 files) should be done as a batch.

### Issue #42 — Top 10 doc-vs-tree gaps remaining (HIGH)
- **Severity:** HIGH (RULES §1.7 — would cause a new agent to act on false claims)
- **Per RULES §1.10 (plain English), the highest-priority gaps a new agent or owner would actually trip on:**
  1. **SPEC.md:51** — claims `requires`/`ensures` enable the compiler to **auto-synthesize property-based tests**. Tree state: SPRINT.md:54 "Full SMT … residual"; PM.md row 1.2 "Residual: SMT/quantifiers" — synthesis is NOT a working product path. **Add `[STATUS: residual — simple runtime only; auto-synthesis not shipped]`.**
  2. **DESIGN.md:8 / SPEC.md:15** — "global, verifiable compute network"; "Compiler, LSP, test runner, package manager, formatter, and linter bundled in a **single binary**". Tree state: PM.md row 5.1 "pkg/LSP/registry residual"; row 5.1a "Pure product compiler + CLI … done (alpha)" — pkg/LSP are not shipped. **Replace "single binary" list with "compiler + CLI shipped; pkg/LSP/registry residual" or tag each sub-item.**
  3. **SPEC.md:84** — "**Compile-Time Code Execution (`comptime`)** … Type generation, schema validation, and meta-programming". Tree state: PM.md row 1.4 "`macro_expand`/`ast_macro` free-name refuse. Residual: real macro product" — comptime is not a working feature. **Tag with `[STATUS: residual]`.**
  4. **SPEC.md:147-148** — "Ships with an official `ooda.gbnf` grammar file. LLM samplers … can use this grammar file". Tree state: `ooda.gbnf` exists at `openOODA/ooda/ooda.gbnf` but PM.md and SPRINT.md never mention gbnf sampling/grammar-constrained decoding path. **Add `[STATUS: file present; sampler integration not shipped]`.**
  5. **DESIGN.md:25** — "**Global Hive-Mind Fuzzing:** … connecting to a global peer-to-peer network of idle openOODA compilers … collaboratively generates AI-driven semantic mutations … mathematically proving or breaking your contracts overnight". Tree state: PM.md row 2.4 "Path A In: `hive_fuzz`/`hivemind_join` free-name refuse. Residual: P2P hive-mind"; SPRINT.md:54 "Global Hive-Mind Fuzzing … residual" — feature is a free-name refuse, not a working network. **Add `[STATUS: residual / path-A refuse; not a shipped P2P network]`.**
  6. **SPEC.md:11** — "**Sub-second iteration loops**". Tree state: PM.md row 1.1 "Residual pack `OODA_SPEED.md` / smoke — not full DESIGN speed marketing" — "sub-second" on real builds is not proven. **Soften SPEC.md:11 to match honest "product check/build/run loops real".**
  7. **SPEC.md:191** — "`ooda patch` … AI agents emit surgical AST node patches … **cutting output tokens by 90%**". Tree state: PM.md row 2.2b "Product patch path In; line-range / node_id residual"; no measured 90% claim in product; aspiration only. **Drop "90%" or tag `[STATUS: aspirational; node-id patches residual]`.**
  8. **SPEC.md:135** — "OODA's compiler can read `.h` files directly at compile time via `comptime` to **auto-generate OODA type signatures on the fly**". Tree state: PM.md row 4.3.3 "Path A In: `ffi_gen`/`import_c` free-name refuse + Cap vs FFI (6.3). Residual: full `import "C"` gen" — auto-gen from `.h` is not shipped. **Add `[STATUS: residual; `import_c` is refuse-stub, no header reading]`.**
  9. **DESIGN.md:8** — "designed for sub-second development feedback, zero-day defense, and **bare-metal native execution**". Tree state: PM.md row 4.1.5 "Path A In: `bare_metal_init` free-name refuse. Residual: real `#![no_std]` floor" — bare-metal is a refuse-stub, not a working target. **Add `[STATUS: residual; bare-metal target is refuse-stub]`.**
  10. **SPEC.md:129** — "import python::torch" (already M175-fix #3 with `[STATUS: residual / fail-closed stub]`). Re-flagged here for awareness: confirm the tag is intact and not lost in any future doc edit.**
- **Fix path:** Apply all 10 edits in one PR. The two highest-leverage are SPEC.md §7 (drop or `[STATUS]` the single-binary toolchain list) and DESIGN.md §2.4 (tag hive-mind), because a new agent reading either line will wire up code against non-existent paths.

### Issue #43 — Test corpus has 10 quality issues (MEDIUM)
- **Severity:** MEDIUM (false-pass risk; missing real coverage)
- **Issues:**
  1. `qa/qa_phase5a.sh:35-58` — Phase 5d json-errors probe has weak assertion. **HIGH.** Require `jq -e '.kind == "CapabilitySecurityViolation"'` on stdout; assert `--json-errors` flag appears in stderr with `-h` parse.
  2. `qa/tests_high_value/ai_rec_03.oo` — unused fixture, header admits "Runner expects PASS … Real undefined-fn trap lives in typecheck unit tests + Phase 5d JSON probe" — meaning this file does not test the typecheck undefined-fn pattern. **HIGH.** Add a sibling `ai_rec_03_undefined_trap.oo` and route through `qa_phase1_4.sh` Phase 4c expecting TRAP.
  3. `qa/tests_high_value/sec_pen_0[1-5].oo` — 5 byte-identical duplicate files, only the URL path differs. Each is `let _ = fetch("https://evil.example/pen/N");`. **HIGH.** Add `verify` block asserting `error_class == "Capability"` or capture stderr and grep for `sealed|CapabilitySecurityViolation`.
  4. `qa/tests_behavior/beh_01_crypto_sha256.oo`, `beh_02_json_parser.oo`, `beh_06_async_task_join.oo`, `beh_08_old_state.oo` — `verify` blocks assert value but `main()` never re-checks (just `println` without `assert_eq!`). **MEDIUM.** Add `assert_eq!` to `main` of each `*.oo` in Phase 1.
  5. `qa/qa_harness_common.sh:46-84` (`run_phase` helper) — for `expect_fail` without `require_msg`, any non-zero rc passes including 127 (command not found) and SIGSEGV (139). **HIGH.** Combine with `set -o pipefail` and require stderr to match `[Ee]rror|[Cc]apability|[Tt]rap|[Pp]recondition`.
  6. `qa/qa_runner.sh` does not invoke `qa_module_check.py` (file does not exist). **MEDIUM.** Either remove from docs or implement and add `python3 qa/qa_module_check.py` to Phase 8.
  7. `qa/qa_phase6_8.sh:23-29` (Phase 7 WASM probe) — `[ "$wasm_rc" -eq 0 ] || [ "$wasm_rc" -eq 2 ]` accepts BOTH success AND a hardcoded exit-code 2. A regression that emits garbage .wat but exits 2 passes silently. **HIGH.** Drop the `|| [ rc -eq 2 ]` fallback or assert the produced `.wat` file contains `(module` and a non-empty `func` table.
  8. `qa/qa_phase6_8.sh:90-101` (Phase 7c CHS native probe) — hardcodes `"$OODA_SRC_ROOT/../std"` and `"$OODA_SRC_ROOT/../openooda-std"` for STDLIB_BIN (line 166-170); on a fork that uses `vendor/` or a different layout, Phase 7e silently skips — 0 tests, exit 0, no warning. **MEDIUM.** Use `git config --get remote.origin.url` or `OODA_STD` env override; FAIL Phase 7e when STDLIB_BIN is empty.
  9. `qa/e2e/e2e_harness_common.sh:144-148` (`run_e2e_cmd_dual` baseline fallback) — default `effective_baseline` regex is `unknown command\|residual\|ERR\|usage\|ERR_MISSING\|ERR_NO_OUTLINE_HELPER`. `ERR` matches essentially any stderr containing the substring "err". **HIGH.** Tighten to `^(residual|--fuzz residual|TODO residual)` and require exit code in {77, baseline-ranges}.
  10. `qa/tests/type_system/01_file_extension.oo`, `02_immutability.oo`, `tests/high_value/math_edge_03.oo` — `01_file_extension.oo` just returns string `"extension_ok"` (tests nothing about file extension parsing); `02_immutability.oo` doesn't mutate anything; `math_edge_03.oo` may not match its claim. **LOW.** Rename or rewrite to actually exercise the feature, or delete.

## M176 audit round 4 summary (plain English)

Three subagents in parallel. 33 quality issues surfaced. Most are weak assertions in test scripts that pass on empty output or wrong-target regex — immune test violations per RULES §1.6. The doc-vs-tree gaps are about moonshot features the docs claim but the tree refuses at compile time (auto-synthesized tests, hive-mind, comptime, .h-import, bare-metal).

Recommended Grok order:
1. **Issue #40** (HIGH, 10 pure soft-pass e2e scripts) — delete in one PR. Zero signal, max noise.
2. **Issue #42** (HIGH, 10 doc-vs-tree gaps) — one PR to add `[STATUS: residual]` tags. Single-binary / hive-mind / comptime / bare-metal are the highest-priority because they would mislead a new agent wiring up code.
3. **Issue #41** (MEDIUM, 15 loose-assertion e2e scripts) — tighten target regexes, remove `|^$` from baselines.
4. **Issue #43** (MEDIUM, 10 test-corpus quality) — `qa_phase5a.sh:35-58` `jq` assertion, `sec_pen_0[1-5].oo` verify blocks, `qa_harness_common.sh:46-84` `require_msg`, `qa_phase6_8.sh:23-29` drop `rc==2` fallback.
5. **Issue #39** (from M175 round) — `pkg.oo` is dead code; `rm` it.

Total round 4: 10 weakest e2e + 15 loose e2e + 10 doc-vs-tree + 10 test-corpus = **45 new issues** to put in front of Grok.

Per RULES §1.5 (reverse entropy) and §1.7 (claims match tree), this is the longest-tail audit work — the typecheck / cache / install / RP work Grok is doing is the load-bearing fix; this is the long tail of weak tests and overclaimed docs that would surface later as a "tests were always green" surprise.
