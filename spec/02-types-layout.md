# 02 — Types, Memory Layout & Generics (`.oo`)

> **Status:** Clean-break specification (`openOODA v3.2.0`). Items marked `[Target: Phase 1]` replace legacy compiler restrictions with zero backwards-compatibility shims.

## 1. Primitive Types
- Signed integers: `i8`, `i16`, `i32`, `i64` (alias `Int`), `isize` `[Target: Phase 1]`.
- Unsigned integers: `u8`, `u16`, `u32`, `u64`, `usize` `[Target: Phase 1]`.
- Unsigned operators (`/` `udiv`, `%` `urem`, `>>` `lshr`, `< <= > >=` `ult/ule/ugt/uge`) follow true unsigned LLVM/machine semantics `[Target: Phase 1]`.
- Floating-point & vectors: `f32` `[Target: Phase 1]`, `f64` (alias `Float`), `f32x8`, `f64x4`.
- Logic & Unit: `Bool` (`true`/`false`), `Void`.
- Explicit casts: `expr as TargetType` `[Target: Phase 1]` (no silent narrowing or signed/unsigned mixing).

## 2. Compound Types & Layout Attributes
- **Stack arrays `[T; N]` `[Target: Phase 1]`:** Fixed-size inline value `[N x T]` with zero heap allocation or ARC overhead.
- **Slices `&[T]` / `&mut [T]` `[Target: Phase 1]`:** Two-word fat pointer `{ ptr, usize len }`. Indexing performs bounds checks elidable by the static SMT prover (`smt_prover`).
- **Tuples `(A, B, ...)` `[Target: Phase 1]`** & **`String` (`{ ptr, i64 }` UTF-8 byte slice)** & **`List[T]`**.
- **Structs:** `pub struct Name { pub field: Type, ... }`.
  - `@repr(C)`, `@repr(packed)`, `@repr(align(N))` `[Target: Phase 1]` guarantee deterministic C/hardware field offsets.
  - Compile-time intrinsics `[Target: Phase 1]`: `size_of[T]()`, `align_of[T]()`, `offset_of(T, field)`.
- **Arbitrary-Payload Sum Types (`enum`) & `Box[T]` `[Target: Phase 1]`:**
  - Tagged union `{ i32 tag, [max_payload_bytes x i8] }` supporting structs, arrays, multi-field variants, nested enums, and `Box[T]` heap indirection for recursive AST/IR types.
  - Exhaustive `match` with pattern destructuring and tag-dispatched ARC drop.

## 3. Generics, Traits & Callables `[Target: Phase 1]`
- **Monomorphized Generics:** `struct Map[K, V]`, `enum Result[T, E]`, `fn sort[T: Ord](xs: &mut [T])` instantiate specialized machine code at compile time (zero boxing/vtable cost by default).
- **Static Traits:** `trait` / `impl` blocks for compile-time bounds (`Eq`, `Ord`, `Hash`, `Read`, `Write`, `Drop`).
- **Callables:** First-class function pointers `fn(A, B) -> C` and closures capturing environment values by value/borrow.
