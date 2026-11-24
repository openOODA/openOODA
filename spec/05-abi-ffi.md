# 05 — Calling Conventions, C FFI & Native OS ABI

> **Status:** Clean-break specification (`openOODA v3.2.0`).

## 1. Explicit Foreign Function Interface (`extern "C"`) `[Target: Phase 1]`
- Foreign symbols are declared explicitly with `extern "C" fn name(arg: Type, ...) -> Ret;` and require `&FfiCap` to call (unless internal runtime substrate).
- Calling convention lowering is driven by target triple and explicit `extern "C"` linkage — never by symbol name prefixes.
- Types crossing `extern "C"` boundaries must be scalar, pointer, or `@repr(C)` / `@repr(packed)` structs.

## 2. Target Triples & Calling Conventions
| Target Triple | Binary Format | Calling Convention | Runtime Archive |
| :--- | :--- | :--- | :--- |
| `x86_64-unknown-linux` | `ELF64` PIE/RELRO/CET | System V AMD64 | `libooda-runtime-core.a` |
| `x86_64-openooda` | `ELF64` (`.ooda.abi`) | System V AMD64 + 32-syscall ABI (`0..31`) | `libooda-runtime-openooda.a` |
| `x86_64-w64-mingw32` | `PE32+` | Microsoft x64 (`sret` aggregates) | `libooda-runtime-core-win64.a` |
| `x86_64-unknown-uefi` | `PE32+` EFI | Microsoft x64 (0 OS syscalls) | `libooda-runtime-uefi.a` |
| `x86_64-none-elf` / `aarch64-none-elf` / `riscv64-none-elf` | Freestanding `ELF64` | Arch bare-metal ABI (0 OS syscalls) | `libooda-runtime-nostd*.a` |
| `wasm32-unknown-unknown` | `WASM32` | WebAssembly MVP + JS scratch | `libooda-runtime-wasm32.a` |

## 3. Native `x86_64-openooda` Syscall ABI (Ring-3 <-> Ring-0) `[Kernel ABI + Phase 6 Userspace Cutover]`
- `0..31` capability-checked syscalls via `syscall` instruction (`ooda-kernel/core/cspace/`, `[Target: Phase 6]` for full Linux-free userspace cutover): `rax` = syscall number, `rdi/rsi/rdx/r10/r8/r9` = arguments, `rax` = signed return (`< 0` negative errno).
- Every capability-gated syscall verifies the caller's `CapReg64` slot inside kernel `CSpace` (`ooda-kernel/core/cspace/`).
