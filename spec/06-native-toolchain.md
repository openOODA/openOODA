# 06 — Zero-Dependency Native Toolchain & Fixed-Point Self-Hosting

> **Status:** Clean-break specification (`openOODA v3.2.0`; native multi-arch backends & `PATH=""` gate targeted in Phase 4 of [`ROADMAP.md`](../ROADMAP.md)).

## 1. Zero-External-Dependency Mandate (`PATH=""`)
The completed `@openOODA-core` toolchain compiles, links, strips, archives, tests, and self-hosts **with zero non-OODA tools** (`PATH=""` — no `clang`, `gcc`, `llvm`, `lld`, `ld`, `as`, `ar`, `strip`, `readelf`, GNU `make`, `xargs`, `bash`, or GNU coreutils).

## 2. Multi-Architecture MIR Codegen Pipeline
- **Frontend:** Lexer → Typed Recursive AST (`Span`) → Integer-ID Type/Symbol Interner → Monomorphizer → CFG/SSA MIR.
- **MIR Safety & Opts:** Borrow/Move/Cap/`with_cap`/OODA-Phase/`SECRET:`/`Send`-`Sync`/SMT checks + mem2reg, DCE, const-fold, copy-prop, inlining, LICM, bounds-check elision, unified ARC drop elaboration.
- **Register Allocation & Instruction Selection:** Shared SSA register allocator (`-O0`/`-O1` linear scan for fast compile speed; `-O2` graph coloring + coalescing) lowering to:
  - **x86_64** (SysV, Win64, UEFI, `nostd`, `openooda`, SSE2/AVX2, atomics, `RETGUARD`/CET)
  - **AArch64** (`aarch64-linux`, `aarch64-none-elf`, NEON, atomics)
  - **RISC-V 64** (`riscv64-linux`, `riscv64-none-elf`, RV64GC + atomics)
  - **WASM32** (`wasm32-unknown-unknown`)
  - **GPU** (PTX + SPIR-V device kernels)

## 3. Native Binary Emitters, Linkers & Build Driver
- Pure-`.oo` `ELF64`, `PE32+`/`UEFI`, and `WASM32` object emitters, static/PIE/freestanding linkers, symbol stripper, and `.a` archiver (`core/binfmt/`).
- Native multi-threaded `ooda build` / `ooda test` / `ooda det` replacing external build systems and subprocess shell-outs.

## 4. Stage-1 / Stage-2 Fixed-Point Invariant
Every compiler release must pass byte-identical Stage-1 / Stage-2 self-compilation from clean caches (`S1 == S2` length, SHA-256, and bytes → `OK_FIXED_POINT`).
