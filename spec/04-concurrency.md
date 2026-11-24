# 04 — Concurrency, Threads & Synchronization

> **Status:** Clean-break specification (`openOODA v3.2.0`; target implementation in Phase 2 MIR + Phase 3 `ooda-runtime`).

## 1. Capability-Gated OS Threads
- Spawning or joining OS threads requires an explicit `&ThreadCap` token (`oo_thread_spawn` / `oo_thread_join`).
- Hosted Linux backend uses `clone3` + `futex`; native openOODA OS uses kernel Ring-3 thread syscalls (`libooda-runtime-openooda.a`).
- Structured concurrency scopes (`with_domain`) drain and join owned actors/channels cleanly before leaving lexical scope.

## 2. Static Data-Race Prevention (`Send` / `Sync`) `[Target: Phase 2–3]`
- Types crossing thread or channel boundaries must satisfy compile-time `Send` (safe to transfer ownership across threads) and `Sync` (safe to share `&T` across threads) enforced in the MIR checker.
- Non-atomic interior-mutable cells and thread-local `Arena` handles are `!Send` / `!Sync`.
- Biased reference counts (`rc_biased.oo`) atomically promote shared payloads (`PROMOTED` bit) before cross-thread transfer.

## 3. Synchronization & Lock-Free Primitives `[Target: Phase 3]`
- **`Mutex[T]` & `RwLock[T]`:** Futex-backed mutual exclusion and reader-writer guards owning the protected `T` (data cannot be accessed without holding the lock guard).
- **`Condvar`:** Condition variable paired with `Mutex[T]` without busy-waiting.
- **`Channel[T]`:** Bounded, thread-safe MPSC/MPMC blocking ring channels (`send`/`recv`/`try_recv`/`close`).
- **`AtomicI64` / `AtomicU64` / `AtomicU32` / `AtomicBool`:** Explicit memory orderings (`Relaxed`, `Acquire`, `Release`, `AcqRel`, `SeqCst`) lowered to native CPU atomic instructions (`lock xadd`/`cmpxchg` on x86_64, `ldaxr`/`stlxr` on AArch64, `amo*`/`lr`/`sc` on RISC-V 64).
