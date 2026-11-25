# openOODA Master Roadmap & Goal TODO

> **Mandate:** Harden openOODA (`.oo`) into a sound, zero-theater, zero-external-dependency systems programming language across `@openOODA`, `@openOODA-core`, and `@openOODA-system`. Backwards compatibility is NOT required — every phase executes a clean break. Scientific & mathematical libraries remain inside `ooda-standard` and must be genuinely validated.
>
> **Dual Veto Law:** Every item below requires unanimous **`VERDICT: PASS`** from both read-only adversarial subagents (`integrity-auditor` and `systems-architect`), plus green build/tests/determinism/`ooda-verify cycle`, version bump, annotated tag, and GitHub push before being checked `[x]`.

---

## Phase 0: Governance, Shape Compromise & Veto Subagents (`openOODA`, `ooda-verify`)
- [x] **0.1** Define & activate `integrity-auditor` and `systems-architect` read-only veto subagents.
- [x] **0.2** Update `openOODA/cards/rules.md` and `ooda-verify` (`core/shape/profile.oo`, `core/types/scan.oo`, `core/hats/white.oo`, `Makefile`) with the Power-of-2 compromise (`<= 16` fns/file, `<= 16` entries/dir, `<= 256` L/file kept, mandatory `anchor.oo` exempt from 16L floor).
- [x] **0.3** Add `ooda-verify/core/sec/anti_theater.oo` catching single-line stub exports, `"Int floor"` crypto/ZK toys, and mechanical split boilerplate; bump & release `ooda-verify` `v1.1.0`.
- [x] **0.4** Write formal clean-break `.oo` Language Specification (`openOODA/spec/01..06.md`), align `openOODA/README.md` with verified reality, bump & release `openOODA` `v3.2.0`.

## Phase 1: Clean-Break `.oo` Language Core Upgrade (`ooda-compiler`)
- [x] **1.1** Hex (`0x`), binary (`0b`), octal (`0o`), `_` separators, byte literals (`b'x'`), typed suffixes, raw strings, trailing commas, clean `struct`/`enum`, labeled `break`/`continue`. (`ooda-compiler` v0.18.0)
- [ ] **1.2** `usize`, `isize`, `f32`, explicit `as` casts, and true unsigned arithmetic/shifts/comparisons (`udiv`, `urem`, `lshr`, `icmp ult/ule/ugt/uge`).
- [ ] **1.3** Stack arrays `[T; N]`, slices `&[T]`/`&mut [T]` with SMT bounds elision, and tuples `(A, B)`.
- [ ] **1.4** Full arbitrary-payload sum types (ADTs) + `Box[T]` + tag-dispatched ARC drop + exhaustive `match` (delete legacy `{i64, i64, OoStr}` layout).
- [ ] **1.5** `@repr(C)`/`@repr(packed)`/`@repr(align(N))` + `size_of`/`align_of`/`offset_of` + typed `static`/`static mut` globals.
- [ ] **1.6** Capability-gated `MmioPtr[T]`/`RawPtr[T]` (volatile load/store), explicit `extern "C"` (delete name-prefix heuristics), and capability-gated inline `asm!`.
- [ ] **1.7** Monomorphized user generics (`struct`/`enum`/`fn`) + static-dispatch `trait`/`impl` (`Eq`, `Ord`, `Hash`, `Read`, `Write`, `Drop`).
- [ ] **1.8** First-class function pointers `fn(...) -> ...` and real capture-struct closures.
- [ ] **1.9** **Seed Bump Gate 1:** `S1 == S2` (`OK_FIXED_POINT`) across hosted + `nostd` + `openooda` + `uefi` + `wasm32`; release tagged `ooda-compiler`.

## Phase 2: Typed AST → CFG/SSA MIR Compiler Rewrite (`ooda-compiler`)
- [ ] **2.1** Replace string-tagged AST with real typed recursive AST (`Item`/`Stmt`/`Expr`/`Pat`/`TypeExpr` + `Span`); delete old string AST helpers.
- [ ] **2.2** Replace delimited flat-string symbol/type tables with integer-ID interner + O(1) hash maps.
- [ ] **2.3** Wire `core/mir/` into the real compilation pipeline (`Typed AST -> CFG/SSA MIR`); delete `mir_flush_types_stub`.
- [ ] **2.4** Port Borrow, Move, Capability, `with_cap` Effect, OODA Phase, `SECRET:` Taint, `Send`/`Sync`, and SMT VC checks onto MIR CFG dataflow; delete token-scanning checkers.
- [ ] **2.5** Implement MIR optimization passes (mem2reg, const-fold, copy-prop, DCE, inlining, LICM, bounds-check elision, unified MIR ARC/drop elaboration).
- [ ] **2.6** Multi-error diagnostics with source-span carets + `--error-format=json` + DWARF debug info (`-g`).
- [ ] **2.7** **Seed Bump Gate 2:** Byte-identical `S1 == S2` compiling through Typed AST → MIR under `< 512 MiB` RAM; release tagged `ooda-compiler`.

## Phase 3: Clean-Break Runtime Overhaul, Real OS Concurrency & 234-Stub Purge (`ooda-runtime`)
- [ ] **3.1** Tag static/immortal string literals (1-bit tag) to eliminate `span_has_mt` hash probing on every `oo_str_retain`/`oo_str_release`.
- [ ] **3.2** Compact 16-byte slab headers + 16B/32B/64B slab classes + per-thread slab caches (remove single global lock `rc_lock_off(8)`).
- [ ] **3.3** Rewrite `oo_int_to_str` using stack `[u8; 32]` (delete `rc_lock_off(16)` global spinlock).
- [ ] **3.4** Replace every `rt_bss_ptr(slot, size)` with typed `static` structs.
- [ ] **3.5** Redesign `mem_arena.oo` with typed `Arena` handles, thread-local active arena/scratch stack, and unlimited slots.
- [ ] **3.6** Implement real OS threads (`clone3`/`futex` + native Ring-3 threads), `Mutex[T]`, `RwLock[T]`, `Condvar`, `Atomic*` with memory orderings, and thread-safe blocking `Channel[T]`.
- [ ] **3.7** Complete native Ring-3 `libooda-runtime-openooda.a` ABI (`openooda/*`) and fix Landlock jail flake (delete `OODA_NO_JAIL=1`).
- [ ] **3.8** Purge all **234** single-line stub exports (`stub_export_count == 0` verified automatically), including adding missing `crypto_mldsa65_{keygen,sign,verify}_internal` to `win64/pqc_anchor.oo` (`libooda-runtime-pqc-win64.a`) and fixing the Landlock jail flake.
- [ ] **3.9** Runtime microbenchmark gate proving ARC retain/release, small-alloc, and multi-thread scaling improvements; release tagged `ooda-runtime`.

## Phase 4: Native Multi-Arch Backends, Pure-`.oo` Linker & `PATH=""` Zero-Dependency Self-Host
- [ ] **4.1** Complete shared MIR register allocator (fast linear-scan `-O0`/`-O1` + graph-coloring `-O2`), frame lowering, and ABI tables.
- [ ] **4.2** Native **x86_64** backend (`core/emit/x86_64/`): full instruction selector + encoder (Linux, Win64, UEFI, `nostd`, `openooda`, SSE2/AVX2, atomics, inline `asm!`, `RETGUARD`/CET).
- [ ] **4.3** Native **AArch64** (`core/emit/aarch64/`) and **RISC-V 64** (`core/emit/riscv64/`) backends verified under QEMU user + bare-metal emulation.
- [ ] **4.4** Native **WASM32** (`core/emit/wasm/`) and **GPU PTX/SPIR-V** (`core/emit/gpu/`) backends (zero `nvcc`/`hipcc`).
- [ ] **4.5** Pure-`.oo` **ELF64**, **PE32+/UEFI**, and **WASM32** object emitters, static/PIE/bare-metal linkers, symbol stripper, and `.a` archiver.
- [ ] **4.6** Pure-`.oo` native-threaded `ooda build` / `ooda test` / `ooda det` replacing GNU `make`, `clang`, `lld`, `strip`, `xargs`, `bash`, and coreutils shell-outs across `@openOODA-core`.
- [ ] **4.7** **Zero-Dependency Self-Host Gate (`PATH=""`):** With `PATH=""` (zero non-OODA binaries reachable), compile `ooda-runtime` + `ooda-compiler` `S1 -> S2` and verify byte-identical `OK_FIXED_POINT` + fast compile-time benchmark; release tagged `ooda-compiler` & `ooda`.

## Phase 5: `ooda-standard` Deduplication & Full Core + Scientific Validation
- [ ] **5.1** Remove ~32 duplicate `foo/` vs `foo_grp/` collection groups and empty placeholder stub files (`*_stub.oo`/`*_stubs.oo`); migrate any callers cleanly.
- [ ] **5.2** Implement real generic O(1)/O(log N) collections: `Vec[T]`, `HashMap[K, V]`, `HashSet[K]`, real O(log N) `BTreeMap[K, V]`, `VecDeque[T]`, `BinaryHeap[T]`, `BitSet`.
- [ ] **5.3** Implement real systems I/O: `Bytes`/`ByteBuf`, `Read`/`Write`, `BufReader`/`BufWriter`, UTF-8, `fmt`, event loop I/O.
- [ ] **5.4** Implement real multi-limb `U256`/`U384` Montgomery arithmetic for BN254 & BLS12-381 (eliminating all 64-bit `Int floor` ZK toys) + constant-time audit, zeroization, and NIST/RFC KAT suites across all `sec/` modules.
- [ ] **5.5** Validate every scientific, math, physics, chem, bio, comm, econ, proof, and AI module in `ooda-standard` against analytical ground-truth, numerical accuracy, conservation laws, and finite-difference gradient checks (delete anything that fails real validation).
- [ ] **5.6** Expand `ooda-standard/tests/` with full unit, property, numerical, KAT, and benchmark suites; release tagged `ooda-standard`.

## Phase 6: Toolchain & `@openOODA-system` Native Alignment
- [ ] **6.1** Wire `ooda-language` (LSP) to Phase 2 Typed AST + Symbol Interner; release tagged `ooda-language`.
- [ ] **6.2** Finish `ooda` CLI (`test`, `bench`, `doc`, AST-based `fmt`) and `ooda-package` (SemVer + SHA-256 `ooda.lock` + workspaces); release tagged `ooda` & `ooda-package`.
- [ ] **6.3** Audit & validate `ooda-sign`, `ooda-bridge`, `ooda-interface`, `ooda-version` (real KATs, clean `extern "C"`, zero stubs); release tagged versions.
- [ ] **6.4** Refactor `ooda-kernel`, `ooda-boot`, `ooda-drivers`, `ooda-hardware` onto hex literals, `@repr(C)`/`@repr(packed)` structs, `MmioPtr[T]`, and `asm!` — delete `oo_hw_op` completely; release tagged versions.
- [ ] **6.5** Complete Ring-3 syscall ABI (`0..31`), SMP scheduling, real hardware drivers separated from models, and decouple the 208 `/proc`/`/dev`/`/sys` files across `@openOODA-system` daemons behind `linux`-vs-`openooda` adapters; release tagged versions.
- [ ] **6.6** **Final Native OS Gate:** Pure-OODA (`PATH=""`) build of `ooda-boot` -> `ooda-kernel` -> `ooda-start` -> `ooda-shell` verified in QEMU (`qemu-smoke`) running an interactive command + Ring-3 capability-denial trap with zero Linux kernel underneath; final `openOODA` release tag & catalog sync.
