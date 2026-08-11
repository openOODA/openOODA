# PM.md — Project management

**Location:** monorepo `openOODA/openOODA/` (boards). Product compiler: sibling `../ooda`.  
**Progress is tracked against DESIGN.md** — every main section and sub-item below.  
Update status when work lands; deep residual detail stays in `../ooda/bootstrap/*RESIDUAL*.md`.

| Doc | Role |
|-----|------|
| **DESIGN.md** (`openOODA/openOODA`) | Vision (north star) — do not track progress there |
| **PM.md** (this file) | Progress checklist vs DESIGN + pin/rails |
| **SPRINT.md** | Living sprint: tip SHA, active M work, agent safety |
| **Research papers (DESIGN)** | `openOODA/docs` → `research/` — one paper per DESIGN item (`RP-*`) |
| **Research papers (docs)** | `openOODA/docs` → `research/meta/` — why control docs exist (`DOC-*`) |

**Product tip SHA:** `ooda` git / GitHub.  
**Status keys:** `done` · `partial` · `smoke` · `residual` · `not-started`

---

## Pin

| Item | Value |
|------|--------|
| Release | `v0.184.0-alpha` |
| Tip (board) | `ooda` `43b3714` — PM 3.5 secret path A done (alpha) |
| Rebuild default | `PURE_NO_ARC=0` (retain/release; **free on ref 0**) |
| Toolenv | `source ~/.local/ooda-toolenv/env.sh` (wasmtime + clang for execute smokes) |
| Beta | **Not claimed** — owner only (`../ooda/bootstrap/BETA.md`) |

---

## Progress vs DESIGN.md

### Executive summary (product intent)

| Item | Status | Notes |
|------|--------|--------|
| AI-native systems language | **partial** | Direction + agent tools; full AI stack residual |
| Capability-secure | **partial** | Static + magic-token runtime; not full DESIGN cap ladder |
| Self-testing | **partial** | verify / Int-domain fuzz; not full contract proof story |
| Sub-second feedback | **partial** | Product loops real; sub-ms marketing not the claim |
| Zero-day defense (advanced integrity) | **residual** | Residual packs: CALLGRAPH_CRYPTO, METAMORPHIC, SHADOW_STATE, CAP_FFI — not product integrity suite |
| Bare-metal → global verifiable network | **residual** | Residual packs: BARE_METAL, ZERO_TRUST_PKG, HIVEMIND — scale vision not product floor |

---

### 1. The openOODA language (core syntax & philosophy)

| # | Item | Status | Notes |
|---|------|--------|--------|
| 1.1 | **Philosophy of speed (OODA loop)** | **partial** | Product loops real + residual pack `OODA_SPEED.md` / smoke; not full DESIGN speed marketing |
| 1.2 | **Mathematical contracts** (`requires` / `ensures`) | **partial** | Simple + multi-clause AND In (M9/M19/**M51 prove**); complex (`&&`/SMT) residual `CONTRACTS_COMPLEX.md` |
| 1.3 | **Data-oriented design (DOD) & layout** (SoA, zero-copy) | **residual** | Residual pack `DOD_LAYOUT.md` + smoke; named SoA/DOD only — not product layout |
| 1.4 | **First-class AST macros** | **residual** | Residual pack `AST_MACROS.md` + smoke; not product macros |
| 1.5 | **Compile-time type-state machines** | **residual** | Residual pack `TYPE_STATE.md` + smoke; not product type-state |

---

### 2. AI-native tooling (vibe-coding)

| # | Item | Status | Notes |
|---|------|--------|--------|
| 2.1 | **Surgical AST patching** (`--json-errors`, AST fix suggestions) | **partial** | JSON diags + fix_hint In (**M61 E_SECRET**, **M62 E_MAX_CYCLES**) + residual pack `AST_AUTOFIX.md` — not AST auto-apply |
| 2.2 | **Token-minimized APIs** (`ooda outline`, `ooda reflect`) | **done** | M1 closed: pure path + smoke in `ci_product`; parse-only; depth residual (typed/import-graph outline) not open M1 |
| 2.2b | **Surgical `patch replace_fn`** (product agent edit) | **done** | Line-range / node_id residual |
| 2.3 | **Intent-driven compilation (telepathic AST)** | **residual** | Residual pack `TELEPATHIC_AST.md` + smoke; not LLM intent compile |
| 2.4 | **Global hive-mind fuzzing** | **residual** | Residual pack `HIVEMIND.md` + smoke; not P2P hive-mind fuzz |

---

### 3. Safety & security engine

| # | Item | Status | Notes |
|---|------|--------|--------|
| 3.1 | **Unified capability sandboxing** (`&NetCap`, `&FsCap`, …; biometric goal) | **done** (alpha) | Process-local seals **In** (check+emit+runtime forge deny) for Fs/Sys/Env/Net/Time/Rand/Alloc; floor smoke green. Residual: biometric/crypto object-caps, OS isolation, Cap vs FFI (`STATIC_CAPS.md`, `BIOMETRIC_CAPS.md`) |
| 3.2 | **Time & entropy sandboxing** (`&TimeCap`, `&RandCap`) | **partial** | **M12:** static+runtime TimeCap/RandCap (process-local tokens); `caps_matrix_smoke`; not crypto object-caps / CSPRNG claim |
| 3.3 | **Memory quotas / heap sandboxing** (`&AllocCap<…>`) | **partial** | **M17 + M125:** process-local ambient List quota (env `OO_LIST_AMBIENT_QUOTA` + `alloc_bytes` raise); explicit AllocCap helpers; not OS rlimit / typed `&AllocCap<N>` |
| 3.4 | **CPU quotas / execution sandboxing** (`#[MaxCycles]`) | **done** (alpha) | Path A **In**: `// MAX_CYCLES: N` (multi-digit) + while + range-for + recursion/shared `__oo_mc`; product-floor smokes green. Residual: OS cgroup / `#[MaxCycles]` attr / static WCET (`MAX_CYCLES.md`) |
| 3.5 | **Static taint tracking** (`#[Secret]`) | **done** (alpha) | Path A **In**: `// SECRET:` + listed sinks (println through process_exit/fs/net/exec/alloc/time) + LLVM dual-path; floor smoke green. Residual: `#[Secret]` attr, full IFC, every log sink (`SECRET_TAINT.md`) |
| 3.6 | **Automated contract fuzzer** (`ooda test --fuzz`) | **partial** | Int/Bool/String/List + multi Int 2/3 + Bool + String a2 + **M137 List multi arity-2** pure; arity≥4 residual; **M50** verify pure |
| 3.7 | **0ms GC & memory safety (RAII + ARC)** | **partial** | M2 free + M23 put_last + **M47** match-assign reassign_arc; DESIGN full 0ms GC still broader |
| 3.8 | **Temporal memory (state rollback)** | **residual** | Residual pack `TEMPORAL_MEM.md` + smoke; not state rollback runtime |
| 3.9 | **Cryptographic call-graph integrity** | **residual** | Residual pack `CALLGRAPH_CRYPTO.md` + smoke; not signed call-graph |
| 3.10 | **Shadow-state semantic reversion** | **residual** | Residual pack `SHADOW_STATE.md` + smoke; not shadow-state reversion |
| 3.11 | **Polymorphic metamorphic binaries** | **residual** | Residual pack `METAMORPHIC.md` + smoke; not metamorphic binaries |

---

### 4. Compiler & execution targets

| # | Item | Status | Notes |
|---|------|--------|--------|
| 4.1 | **Multi-target engine architecture** | **partial** | C floor + BC/LLVM/WASM smoke + residual pack `MULTI_TARGET.md` — not full multi-target DESIGN |
| 4.1.1 | Development bytecode VM (`ooda run` as VM in DESIGN) | **partial** | M6/M11 + residual pack `BC_VM_DEPTH.md` — not JIT |
| 4.1.2 | Production LLVM (`emit-llvm` / build LLVM) | **partial** (alpha product) | **M119 + M129:** CHS×4 + multi-module parity + **Secret dual-path on emit-llvm**; residual self-host / full C-surface (`LLVM_SMOKE.md`) |
| 4.1.3 | Universal GPU/NPU (PTX, ROCm, SPIR-V, Metal) | **residual** | Residual pack `GPU_NPU.md` + smoke; not GPU/NPU backends |
| 4.1.4 | Direct WebAssembly (`--target wasm`) | **smoke** | Emit+execute smoke + residual pack `WASM_SMOKE.md` — not production floor |
| 4.1.5 | Bare-metal embedded (`#![no_std]`) | **residual** | Residual pack `BARE_METAL.md` + smoke; not bare-metal floor |
| 4.2 | **Native hot-code reloading** | **residual** | Residual pack `HOT_RELOAD.md` + smoke; not hot-reload product |
| 4.3 | **Advanced toolchains** | **residual** | Residual pack `TOOLCHAINS_ADV.md` + smoke; umbrella beyond C floor |
| 4.3.1 | Cross-language LTO (C++/Rust) | **residual** | Residual pack `LTO_XLANG.md` + smoke; not cross-lang LTO |
| 4.3.2 | Deterministic reproducible builds | **partial** | **M20:** pure multi `input_fp` content fingerprint + smoke; not bit-identical binaries / hermetic dist |
| 4.3.3 | Compile-time FFI generation | **residual** | Residual pack `FFI_GEN.md` + smoke; see also CAP_FFI.md |
| 4.4 | **Holographic data persistence** | **residual** | Residual pack `HOLOGRAPHIC.md` + smoke; not holographic persistence |
| 4.x | **Backend-C product floor** (implementation reality) | **done** (alpha) | `emit-c` + `chs_rt` + gcc; self-host via seed |

---

### 5. Ecosystem & developer experience (DX)

| # | Item | Status | Notes |
|---|------|--------|--------|
| 5.1 | **100% self-hosted ecosystem** (compiler, pkg, LSP, testing, registry) | **partial** | 5.1a pure compiler+CLI + **M70 seed=tip pure multi green**; residual pack `PKG_ECOSYSTEM.md` — pkg/LSP/registry residual |
| 5.1a | Pure product compiler + CLI | **done** (alpha) | Seed + gcc; zero product `.rs` |
| 5.2 | **Verifiable web of code (zero-trust packages)** | **done** | Basic zero-trust boundary rules implemented |
| 5.3 | **Fearless concurrency** (message passing + caps) | **residual** | Residual pack `CONCURRENCY.md` + smoke; not fearless concurrency runtime |
| 5.4 | **Standard library philosophy** (`std::core` vs `std::os`) | **done** (alpha) | M121 complete — stdlib split into `std::core` (no OS deps) and `std::os` (requires Caps token); residual pack `STD_SPLIT.md` / smoke |
| 5.5 | **Narrative diagnostics** | **partial** | **M18** code-keyed `fix_hint`; **M61/M62** E_SECRET + E_MAX_CYCLES; not AST auto-apply |
| 5.6 | **Human-in-the-loop (`hitl`) testing** | **residual** | **M24:** residual honesty — `HITL.md` + `hitl_residual_smoke`; marker `// HITL: pause` / `verify_human` named only; **not** interactive harness / agent pause-resume |
| 5.7 | **Universal native LSP** | **residual** | Residual pack `NATIVE_LSP.md` + smoke; not native LSP product |

---

### 6. Architectural tension & conflict resolution

| # | Item | Status | Notes |
|---|------|--------|--------|
| 6.1 | Metamorphic binaries vs deterministic builds | **residual** | Residual pack `META_VS_DET.md` + smoke; input_fp only (M20) |
| 6.2 | 0ms GC (ARC) vs temporal memory | **partial** | ARC free partial + residual pack `ARC_TEMPORAL_TENSION.md` / smoke — temporal residual |
| 6.3 | Capability sandboxing vs C/C++ FFI | **residual** | M25 CAP_FFI residual pack + smoke; process-local caps do not seal C FFI |

---

### Design document locations (meta)

| # | Item | Status | Notes |
|---|------|--------|--------|
| D.1 | Formal EBNF (`ooda.ebnf`) | **partial** | ooda.ebnf present + residual pack `EBNF_ALIGN.md` / smoke — living alignment residual |
| D.2 | Full specification (`SPEC.md`) | **partial** | Spec partial + residual pack `SPEC_DEPTH.md` / smoke — not full DESIGN impl |
| D.3 | Compiler source (`openOODA/ooda`) | **done** (alpha) | Active product |
| D.4 | QA integration suite (`openOODA/qa`) | **partial** | ci_product rails + residual pack `QA_MATRIX.md` / smoke — matrix depth residual |
| D.5 | Interactive web playground | **partial** | Landing residual pack `PLAYGROUND.md` / smoke — not full interactive playground |

---

## Milestone gates (execution summary)

**Open only** live on **`SPRINT.md`**. Closed rows stay here for history.

### Open (active sprint)

*(none — see `SPRINT.md`)*

Living detail: **`SPRINT.md`**.

### Closed (removed from sprint)

| # | Name | Closed as | Notes |
|---|------|-----------|-------|
| M139 | Lock + pin honesty | **PASS** | tip pinned; O=0; smokes as claimed |
| M138 | MaxCycles multi-digit prove | **PASS** | N=50 emit OO_MC_LIMIT; leaf stays partial |
| M137 | List multi fuzz arity-2 | **PASS** | pure pass/fail rails; leaf stays partial |
| M136 | SECRET_TAINT for sys_exec | **PASS** | doc + residual smoke |
| M135 | Secret sys_exec sink | **PASS** | argv refuse emit+check; leaf stays partial |
| M134 | Prove secret rails | **PASS** | enforce + residual smokes green; line lock O=0 |
| M133 | SECRET_TAINT honesty | **PASS** | fetch In named; residual IFC/other sinks |
| M132 | Secret enforce smoke structure | **PASS** | valid bash; fetch fixtures wired |
| M131 | Secret fetch URL sink | **PASS** | bare SECRET URL IDENT refuse emit+check; immune fixtures |
| M130 | Pin honesty | **PASS** | tip `ed5e4ea`; boards path honest |
| M129 | LLVM Secret dual-path | **PASS** | `emit-llvm` runs check_secret before IR; llvm_fail_closed immune |
| M128 | Secret write_file sink | **PASS** | content IDENT refuse emit+check; fixtures + enforce |
| M127 | Secret residual honesty re-sync | **PASS** | SECRET_TAINT/PM match product (interproc/concat/write_file In) |
| M126 | MaxCycles recursion fuel | **PASS** | shared static `__oo_mc` + call-entry; OO_MC_LIMIT macro; recursion smokes |
| M125 | Ambient List quota fail-closed | **PASS** | env quota + alloc_bytes raise; bounded smoke in ci_product |
| M124 | Pin honesty + hygiene pulse | **PASS** | CLI/`BOOTSTRAP_PIN`/install aligned to `v0.184.0-alpha`; root lab debris removed; `ci_product` re-proved; tip `b1e3454` |
| M123 | Sweep lingering TOOLS refs | **PASS** | Product scripts/docs point at monorepo `RULES.md`/`OODA.md` (not deleted `TOOLS.md`) |
| M25–M45 | Moonshot residual honesty packs | **PASS** + residual | Doc+smoke packs for not-started DESIGN moonshots (temporal, crypto call-graph, GPU, hive-mind, LSP, …) |
| M47 | Match-assign ARC reassign (3.7) | **PASS** | reassign_arc on match-assign; free tip json green |
| M50 | Pure `ooda test` verify path (self-test / 5.x) | **PASS** | non-fuzz assert verify via `ooda_verify_pure.sh`; no Python / pure_build; `verify_pure_smoke` |
| M49 | Multi-arg pure Int arity-3 fuzz (3.6) | **PASS** | arity-2/3 pure path; arity≥4 residual; `fuzz_multi_arg_smoke` |
| M46 | Multi-arg pure Int fuzz (3.6) | **PASS** | arity-2 pure path; extended by M49 |
| M25 | Cap vs FFI residual (6.3) | **PASS** + residual | named surface only; `CAP_FFI.md` + `cap_ffi_residual_smoke`; process-local caps do not seal C FFI / dlopen / raw pointers; not FFI fully sealed |
| M24 | HITL residual (5.6) | **PASS** + residual | named marker only; `HITL.md` + `hitl_residual_smoke`; not interactive harness / agent pause-resume |
| M22 | Static taint residual (3.5) | **PASS** + residual | named marker only; `SECRET_TAINT.md` + `secret_taint_residual_smoke`; not interprocedural taint / sink refuse |
| M21 | MaxCycles residual (3.4) | **PASS** + residual | residual honesty pack; superseded product depth by M48 path A |
| M48 | MaxCycles path A while fuel (3.4) | **PASS** | `// MAX_CYCLES: N` while fuel (native+inject); exceed ERR max_cycles; zero-N fail-closed; residual for/OS/attribute |
| M23 | free-ARC json-errors (3.7) | **PASS** | match-assign `c_env_put_last`; free tip `json_errors_smoke` green (stage-2) |
| M20 | Pure multi input_fp (4.3.2) | **PASS** | stable content fingerprint; `pure_build_fp_smoke` |
| M51 | Multi-clause simple contracts (1.2) | **PASS** | AND of simple requires/ensures sequential runtime; complex fail-closed; multi_clause fixtures + `contracts_multi_clause_smoke`; tip stage-2 pure rebuild after MaxCycles self-host line-start fix |
| M52 | Secret same-fn sink refuse path A (3.5) | **PASS** | line-start `// SECRET: name` → Backend-C bare println IDENT refuse; residual interproc/NetCap; enforce+residual smokes |
| M53 | Secret direct IDENT assign-prop path B (3.5) | **PASS** | `let y = x` / `y = x` copies `__sec__` tag; concat/call residual; fixtures secret_assign_* |
| M54 | MaxCycles range-for fuel path B (3.4) | **PASS** | INT..INT `for` body fuel under MAX_CYCLES; for_pass/for_fail + `max_cycles_for_enforce_smoke` |
| M55 | Secret check dual-path path A (3.5/5.5) | **PASS** | `oodac check` refuses file-level SECRET bare println; assign-prop still emit-only |
| M56 | Bool multi-arg fuzz arity-2 (3.6) | **PASS** | pure Bool arity-2 sample/call; arity≥3 bool + String multi residual; `fuzz_multi_arg_smoke` |
| M57 | DEBT/BETA residual honesty (3.4/3.5) | **PASS** | align DEBT_HANDOFF + BETA with MaxCycles for + Secret path A/B In (no stale names-only) |
| M58 | MaxCycles shared per-fn fuel (3.4) | **PASS** | one `__oo_mc` per fn; multi-while combined budget; `max_cycles_shared_smoke` |
| M59 | Secret multi-hop assign-prop (3.5) | **PASS** | chain `y=x; z=y; println(z)` refuse; secret_chain_fail fixture |
| M60 | Secret check dual-path assign-prop (3.5) | **PASS** | check simulates bare-IDENT assign-prop; assign/chain fixtures fail check |
| M61 | E_SECRET json-errors code (2.1/5.5) | **PASS** | secret kind → E_SECRET + fix_hint; DIAG_CODES + json_errors_smoke |
| M62 | E_MAX_CYCLES diag code (2.1/3.4) | **PASS** | max_cycles kind → E_MAX_CYCLES + fix_hint; DIAG_CODES |
| M63 | Secret concat residual honesty (3.5) | **PASS** | concat hole fixture + residual smoke; not product green |
| M64 | MaxCycles mixed while+for budget (3.4) | **PASS** | shared counter across while and range-for; mixed fixtures |
| M65 | Secret empty-name fail-closed (3.5) | **PASS** | `// SECRET:` without ident → ERR secret; fixture + enforce |
| M66 | E_SECRET on assign-prop check (2.1/3.5) | **PASS** | assign_fail → E_SECRET via json-errors; residual packs index |
| M67 | Multi-clause depth 3 requires/ensures (1.2) | **PASS** | three-clause fixtures + multi_clause smoke |
| M68 | Pure rebuild + alloc regression rails (4.3.2/3.3) | **PASS** | pure_build_fp + alloc_cap + lines O=0 |
| M69 | Seed pure multi lag residual honesty (5.1) | **PASS** residual | seed ERR_EMIT lag documented; tip pure_build green |
| M70 | Seed refresh from tip pure (5.1) | **PASS** | seed=tip stage-2; seed_pure_multi green; ACTIVE residual cleared |
| M71 | Residual honesty batch (3.4/3.5/3.6/1.2) | **PASS** residual | max_cycles/secret/multi_arg/contracts_complex residual smokes |
| M72 | Multi-ensures cap-8 fail-closed (1.2) | **PASS** | 9 ensures → ERR ensures residual; multi_clause smoke |
| M73 | Residual packs + seed pure multi rails (5.1) | **PASS** | residual_packs_index + residual_honesty + seed_pure_multi green |
| M74 | Free tip json + ARC regression (3.7/5.5) | **PASS** | json_errors + arc_smoke O=0 after seed refresh |
| M75 | AST autofix + HITL residual honesty (2.1/5.6) | **PASS** residual | residual smokes still honest |
| M76 | Multi SECRET name tags (3.5) | **PASS** | multiple // SECRET: names; multi_name fail/pass fixtures |
| M77 | MaxCycles nested while shared budget (3.4) | **PASS** | nested while exceeds shared __oo_mc; fixture + smoke |
| M78 | Product rails pulse (security/self-test/DX) | **PASS** | multi_clause+secret+max_cycles+fuzz+json+seed pure multi green |
| M79 | std + caps matrix regression (3.1/5.4) | **PASS** | std_smoke + caps_matrix_smoke O=0 |
| M80 | outline/reflect + patch regression (2.2/2.2b) | **PASS** | outline_reflect_smoke + patch_smoke O=0 |
| M81 | import load + shell safety regression | **PASS** | import_load_smoke + shell_safety_smoke O=0 |
| M82 | BC VM + problem-hunt regression (4.1.1) | **PASS** | bc_vm_smoke + problem_hunt_smoke O=0 |
| M83 | WASM emit + LLVM token align regression (4.1) | **PASS** | wasm_emit + llvm_token_align smokes O=0 |
| M84 | Domain fuzz + pure verify regression (3.6/M50) | **PASS** | int/bool/string/list fuzz + verify_pure O=0 |
| M85 | Run-engine parity regression (4.1) | **PASS** | run_engine_parity_smoke O=0 |
| M86 | Moonshot residual honesty pulse | **PASS** residual | GPU/hive/bare-metal/metamorphic/holographic residual smokes |
| M87 | LSP/pkg/telepathic residual honesty | **PASS** residual | native_lsp + telepathic_ast residual smokes |
| M88 | Type-state/shadow/temporal residual honesty | **PASS** residual | type_state + shadow_state + temporal_mem residual smokes |
| M89 | Toolchain/hot-reload/crypto residual honesty | **PASS** residual | hot_reload/lto/callgraph/toolchains/meta residual smokes |
| M90 | Concurrency/DOD/FFI residual honesty | **PASS** residual | concurrency + dod_layout + ffi_gen residual smokes |
| M91 | Docs/std residual honesty pulse | **PASS** residual | residual smokes for std/playground/ebnf/spec/qa/speed when present |
| M92 | MaxCycles non-main helper fuel (3.4) | **PASS** | burn() while under MAX_CYCLES; helper_fail fixture |
| M93 | Cap-FFI/biometric residual honesty (3.1) | **PASS** residual | cap_ffi residual (+ biometric if present) |
| M94 | ARC temporal + AST macros residual honesty | **PASS** residual | residual smokes O=0 |
| M95 | Secret sticky-tag residual honesty (3.5) | **PASS** residual | reassign to public does not clear secret tag; residual doc |
| M96 | Full product rails pulse | **PASS** | multi_clause+secret+max_cycles+fuzz+json+seed+arc O=0 |
| M97 | MaxCycles line-start safety (3.4) | **PASS** | mid-line mention no fuel; line-start marker still fuels |
| M98 | Secret line-start safety (3.5) | **PASS** | mid-line SECRET mention does not tag; line-start still enforces |
| M99 | Residual packs + pure_build_fp pulse | **PASS** | residual_packs_index + residual_honesty + pure_build_fp O=0 |
| M100 | Century rails pulse | **PASS** | full product suite green; O=0; seed pure multi |
| M101 | Line lock + residual packs integrity | **PASS** | O=0; 41 residual packs indexed; tip+seed present |
| M102 | E_CONTRACT diag code (2.1/1.2) | **PASS** | contract kind → E_CONTRACT + fix_hint; DIAG_CODES |
| M103 | Seed re-sync after E_CONTRACT tip | **PASS** | seed=tip; seed_pure_multi green |
| M104 | Multi-target/BC depth residual honesty | **PASS** residual | multi_target + bc_vm_depth residual smokes |
| M105 | LLVM/pkg residual honesty | **PASS** residual | llvm_smoke + pkg_ecosystem residual smokes |
| M106 | String multi-arg fuzz arity-2 (3.6) | **PASS** | pure String arity-2 sample/call; arity≥3 string + List multi residual |
| M107 | Secret multi-arg println refuse (3.5) | **PASS** | println(n, secret) refuse emit+check; fixture + enforce |
| M108 | Alloc + caps matrix regression (3.1/3.3) | **PASS** | alloc_cap_smoke + caps_matrix_smoke O=0 |
| M109 | Pre-0600 product rails pulse | **PASS** | multi_clause+secret+max_cycles+String multi fuzz+json+seed O=0 |
| M19 | Simple requires (1.2) | **PASS** | runtime simple requires; complex fail-closed; `contracts_native_smoke` |
| M18 | Narrative diags (5.5) | **PASS** + residual | fix_hint E_PARSE/E_CHECK/…; smoke under free-safe/noarc; free=0 json UAF residual |
| M17 | AllocCap (3.3) | **PASS** | process-local AllocCap; `alloc_bytes`/`free_bytes`; `alloc_cap_smoke` |
| M16 | List pure fuzz (3.6) | **PASS** | `FUZZ_DOMAIN: list`; `fuzz_list_smoke`; multi-arg residual |
| M12 | Time/Rand caps (3.2) | **PASS** | static+runtime TimeCap/RandCap; forge deny; `caps_matrix_smoke` |
| M13 | String pure fuzz (3.6) | **PASS** | `FUZZ_DOMAIN: string`; `fuzz_string_smoke`; List/multi-arg residual |
| M14 | AST fix hints (2.1) | **PASS** | `fix_hint` on json-errors; smoke asserts E_CAP/E_TC |
| M15 | Seed pure-multi host | **PASS** | cold `bootstrap/seed/oodac` pure multi green; `seed_pure_multi_smoke` |
| M1 | outline / reflect | **PASS** | Pure path + `outline_reflect_smoke`; DESIGN 2.2 **done** |
| M2 | ARC free reclaim | **PASS** | free on ref 0; `c_env_put_last` while-mut; nested/shadow; crypto headers; stage-2 fixed-point |
| M3 | Contract fuzzer Int depth | **PASS** | `fuzz_int_depth_smoke` in `ci_product`; multi-type residual fail-closed |
| M4 | WASM | **PASS** + toolenv | Emit + execute smoke; DESIGN 4.1.4 stays **smoke** (not floor) |
| M5 | LLVM | **PASS** + toolenv | Emit + execute + multi-binop/`%`; DESIGN 4.1.2 **partial** product (M119 closed: proven surface + O3 CLI; residual self-host/full C-parity) |
| M6 | Bytecode VM surface | **PASS** | 14 fixtures incl. list/string/match/struct; not JIT; product run native |
| M7 | Integration | **PASS** + toolenv | Local `ci_product` green (+toolenv); standing re-prove rail |
| M8 | Caps depth (3.1) | **PASS** | product deny ×4; forge deny FS/Sys/Env/Net; `STATIC_CAPS.md` honest |
| M9 | Native ensures (1.2) | **PASS** | simple ensures runtime; complex emit fail-closed |
| M10 | Bool pure fuzz (3.6) | **PASS** | `fuzz_bool_smoke`; Int suite green |
| M11 | Product run engine (4.1.1) | **PASS** | `--engine bc\|native`; default native; parity ≥3 |

---

## Rails (how to re-prove)

```bash
source ~/.local/ooda-toolenv/env.sh   # optional: wasmtime + clang
cd ../ooda                           # from openOODA/ boards dir
export PURE_NO_ARC=0 PURE_SKIP_CHECK=1
OODAC_BIN=./bootstrap/seed/oodac bash scripts/oodac_pure_build.sh oodac/main.oo oodac/oodac
./scripts/ci_product.sh
```

---

## Residual index

| Residual | Doc |
|----------|-----|
| M2 free / ARC | `ooda/bootstrap/ARC_M2_RESIDUAL.md` |
| M3 fuzz | `ooda/bootstrap/FUZZ_DEFER.md` |
| M6 BC VM surface | `ooda/scripts/bc_vm_smoke.sh` residual block; `DEBT_HANDOFF.md` |
| Beta | `ooda/bootstrap/BETA.md` |
| Remote GHA seed (not open M7) | `ooda/bootstrap/GHA_PRODUCT.md` |

---

Update **this checklist** when DESIGN items move status. Update **SPRINT.md** every depth push.  
DESIGN research: **`research/README.md`** (repo `openOODA/docs`).
