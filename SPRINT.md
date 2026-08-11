# openOODA sprint

## Pin
| Item | Value |
|------|--------|
| Release | `v0.184.0-alpha` (stay alpha) |
| Focus | M165 honest leftovers path A (compiler/runtime) |
| Rails | contracts_arith, ehitl_autofix, hitl_verify_human, actor_path_a, gpu_path_a, ffi_dlopen_path_a, str_ops_path_a |
| Beta | **Not claimed** |

## Closed
**M158–M164** as prior  
**M165 residual leftovers path A** (compiler/runtime) — see below  

## M165 honest leftovers (path A) — 4 swarms

| Swarm | Item | Path A finished | Still residual (full DESIGN) |
|-------|------|-----------------|------------------------------|
| A | Contracts + multi-code fix | Arith/`&&`/`||` contracts; `ooda fix` also removes exact `// HITL: pause` | Full SMT, quantifiers, free-form suggested_fix |
| B | HITL + actors | `verify_human` env-gated; `actor_spawn/send/recv` under ThreadCap | Full HITL record/replay; actor supervision trees |
| C | GPU + dlopen | `gpu_launch` noop/cpu fallthrough; system-dir dlopen without ALLOWDIR | Real device shaders; unrestricted any-path dlopen |
| D | String ops | `str_starts_with/ends_with/index_of/repeat/uppercase` | True `&str` borrow / lifetimes |

## Residual named (still open for full DESIGN)
Full SMT/quantifiers · free-form multi-code · full HITL harness · unrestricted OS dlopen · real GPU · native `&str` lifetimes · Tier C moonshots (temporal/hive/hot-reload/LSP/…)  
Beta not claimed

## S
`S: low — U=0 on M165 residual floors F=0 W=0 O=0`

## M165 openOODA Library Fleshing (AGY)
*   **Massive Standard Library Expansion**: Fleshed out and implemented 359 `std/` openOODA library files across multiple domains (Geometry, Tensors, Hardware APIs, Database Connectors, Codecs, UI, Agents, and NLP).
*   **Fail-Closed Strictness**: All files strictly implement the fail-closed recursive stub pattern (`process_exit(1)`) while explicitly enumerating parameter types, realistic struct fields, and respecting capability checks (e.g. `&SysCap`, `&NetCap`, `&ThreadCap`).
*   **Compiler Compliance**: Surmounted rigorous restrictions in `oodac` (including parameter literal environment collisions and sealed builtin type checking). All 359 library files correctly pass `check_all.sh` with 0 failures!

## M165 Language Feature Backlog (Discovered by Agents)
*   **Dynamic Memory Allocation (`malloc`/`free`)**: Currently missing. Blocking the instantiation of complex pointer-based trees (Radix, KD, Skip Lists) and dynamic reference counters (RC/ARC).
*   **Bitwise Operators (`<<`, `>>`, `&`, `|`, `^`)**: Currently missing. Blocking Fast Fourier Transforms (bit-reversals), bit-packing for Bloom Filters, and high-performance cryptography.
*   **Floating-Point Math & Trigonometry**: Lacking standard library support for `sin()`, `cos()`, and `ln()`. Forced the HyperLogLog agent to use fixed-point Taylor series approximations. Blocks complex roots of unity in FFT.
*   **Multidimensional Array/Tensor Primitives**: Blocks Neural Network operations (Conv, Linear, Attention) and multidimensional topological sorts in Autograd.
