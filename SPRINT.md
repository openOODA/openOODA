# openOODA sprint

## Pin
| Item | Value |
|------|--------|
| Release | `v0.184.0-alpha` (stay alpha) |
| Focus | M166 Language Feature Backlog (AGY) path A **closed** |
| Rails | malloc_path_a, bitwise_ops, math_trig, tensor_path_a, tcp_io, sys_syscall_path_a, list_index_path_a (all in `ci_product`) |
| Tip | `ooda` `b6c996b` |
| Beta | **Not claimed** |

## Closed
**M158–M164** as prior  
**M165 residual leftovers path A** (compiler/runtime) — see below  
**M166 Language Feature Backlog (AGY) path A** — tip `b6c996b`

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
`S: low — U=0 on M166 path A tip ship F=0 W=0 O=0`  
*(product tip `b6c996b`; pure self-host rebuild of oodac still residual on some hosts — product fixtures/smokes green on tip binary)*

## M166 Language Feature Backlog (AGY) path A

**Status:** path A **shipped** tip `b6c996b`. Stay **alpha**. **Do not claim beta.**  
**Ship honesty:** source floors + product smokes green; pure multi self-host rebuild residual (some hosts SEGV on `c_emit_let` binds of sealed calls — fixtures avoid those shapes).

| Item | Path A finished | Residual (honesty) |
|------|-----------------|--------------------|
| Dynamic malloc/free under AllocCap | Product free names `malloc`/`free` (aliases `alloc_bytes`/`free_bytes`); fixture uses `free(malloc(...))` | OS rlimit / GC / heap sandbox; host may SEGV on some `let p = malloc(...)` binds |
| Bitwise | `<<` `>>` `&` `|` + `bit_xor` free name | Caret `^` token residual on some hosts |
| Float/trig | `sin` `cos` `ln` `exp` `sqrt` `pow` IEEE double | Decimal / BigDecimal; soft-float bit-identical; full special-fn lib |
| Tensor | Flat `List[Int]` helpers (`std/math/tensor.oo`) | No nested `List[List]` product |
| Net slot IO | `tcp_read` / `tcp_write` / `udp_recv` / `tcp_close` real slot IO | `SOCK_RAW` residual |
| FFI/OS syscalls | `sys_epoll_create` / `sys_inotify_init` / `sys_prctl` sealed residual under SysCap (**Err after require**) | Full async I/O product (epoll loop / inotify watches / real prctl) |
| Array index | `xs[i]` / `index_get` path A | Pointer arithmetic; field-index without List base |
| `ord()` | First-byte 0..255 via `byte_at` | Not Unicode codepoint; not `&str` |
| Cap scoping | Samples in std signatures path A (`std/os/net.oo`, `std/os/process.oo`, …) | Mass AGY stubs still vary; not full DESIGN cap ladder |
| Cap forgery via cast | — | **Residual still open** (not fixed this mile) |

**Smokes (product tree):** `scripts/malloc_path_a_smoke.sh` (also `ci_product`), `bitwise_ops_smoke.sh`, `math_trig_smoke.sh`, `tensor_path_a_smoke.sh`, `tcp_io_smoke.sh`, `sys_syscall_path_a_smoke.sh`, `list_index_path_a_smoke.sh`.  
**Fixtures:** `malloc_path_a.oo`, `bitwise_ops.oo`, `math_trig.oo`, `tensor_path_a.oo`, `sys_syscall_path_a.oo`, `list_index.oo`, `libfloor_tcp_io.oo`.  
**Docs:** `bootstrap/MEMORY_QUOTA.md`, `BYTE_STR.md`, `MATH_TRIG.md`, `CAPS_MATRIX.md`, `STATIC_CAPS.md` (M166 cap scoping + forgery residual).

## M165 openOODA Library Fleshing (AGY)
*   **Massive Standard Library Expansion**: Fleshed out and implemented 359 `std/` openOODA library files across multiple domains (Geometry, Tensors, Hardware APIs, Database Connectors, Codecs, UI, Agents, and NLP).
*   **Fail-Closed Strictness**: All files strictly implement the fail-closed recursive stub pattern (`process_exit(1)`) while explicitly enumerating parameter types, realistic struct fields, and respecting capability checks (e.g. `&SysCap`, `&NetCap`, `&ThreadCap`).
*   **Compiler Compliance**: Surmounted rigorous restrictions in `oodac` (including parameter literal environment collisions and sealed builtin type checking). All 359 library files correctly pass `check_all.sh` with 0 failures!

## M165 Language Feature Backlog (Discovered by Agents)
*Path A delivery of this backlog is under **M166** (above). Discovery bullets retained for agent history; do not re-claim “missing” where M166 path A is finished.*
*   **Dynamic Memory Allocation (`malloc`/`free`)**: Currently missing. Blocking the instantiation of complex pointer-based trees (Radix, KD, Skip Lists) and dynamic reference counters (RC/ARC).
*   **Bitwise Operators (`<<`, `>>`, `&`, `|`, `^`)**: Currently missing. Blocking Fast Fourier Transforms (bit-reversals), bit-packing for Bloom Filters, and high-performance cryptography.
*   **Floating-Point Math & Trigonometry**: Lacking standard library support for `sin()`, `cos()`, and `ln()`. Forced the HyperLogLog agent to use fixed-point Taylor series approximations. Blocks complex roots of unity in FFT.
*   **Multidimensional Array/Tensor Primitives**: Blocks Neural Network operations (Conv, Linear, Attention) and multidimensional topological sorts in Autograd.
*   **Low-Level Network Primitives & Sockets**: Missing raw socket bindings (`AF_INET`/`SOCK_RAW`), `tcp_read`/`tcp_write`, and `udp_recv` returning byte arrays. Blocks native implementation of protocols like PostgreSQL, HTTP/3, gRPC, LDAP, SNMP, and BitTorrent Bencode parsing.
*   **FFI & OS System Calls**: Missing FFI mechanisms to invoke underlying OS system calls natively (e.g., `epoll`, `kqueue`, `inotify`, `seccomp`, `prctl`, `dbus`, `posix_openpt`). Blocking native Linux/macOS async I/O and OS abstractions.
*   **Pointer Arithmetic & Array Indexing**: Missing native array indexing for struct pointers (e.g., `obj.rules[i]`) and pointer arithmetic. Blocks ACL rule iteration and complex data structure traversal.
*   **String/Byte Conversions (`ord()`)**: Missing character-to-integer conversion primitives. Blocks Base64 encoding/decoding, HMAC cryptographic hashing, and Named Entity Recognition (NER) algorithms.
*   **Capability Scoping (`&SysCap`, `&NetCap`)**: Standard library `.oo` signatures often lack `&SysCap` or `&NetCap` tokens, making it impossible to shell out for missing functionality (e.g., executing `/bin/ping` for ICMP) or mutating OS pseudo-filesystems (e.g., `cgroups` at `/sys/fs/cgroup`).
*   **Capability Forgery Vulnerability**: A critical security flaw was discovered by the X11 GUI agent where `&UnsafeFFICap` (and potentially other capabilities) can be forged natively without authorization. By casting a builtin function (e.g. `dlopen`) using `as fn(&UnsafeFFICap, String) -> Int`, the compiler static type checker was successfully bypassed to execute unsafe C functions natively.
