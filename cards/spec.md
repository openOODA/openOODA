# spec.md — openOODA (`.oo`) Language Syntax Quick Card (`ooda spec`)

1. **File Header & Imports**:
   - Every `.oo` file starts with 4 header comment lines (`// # Title`, `// Logline:`, `// Setup:`, `// Beats:`).
   - Relative string imports only: `import "core/engine.oo";` or `import "oostd/fs/os/fs.oo";` (NEVER `::` namespaces).

2. **Types, Bindings & Data Structures**:
   - Primitives: `Int` (64-bit signed), `Float` (f64), `Bool` (`true`/`false`), `String`, `List[T]`, `Option[T]`, `Result[T, E]`.
   - Bindings are immutable by default (`let x: Int = 10;`); mutable bindings require `let mut y: Int = 0;`.
   - Structs (NO trailing comma on the final field!):
     `pub struct Item { pub id: Int, pub label: String }`
   - Sum Types (Algebraic Data Types):
     `pub type Verdict = Pass | Fail(String);`

3. **Functions, Control Flow & Pattern Matching**:
   - Functions: `pub fn compute(fs_r: &FsReadCap, n: Int) -> Result[Int, String] { ... }`
   - `if` / `while` (NO outer parentheses around condition!):
     `if n <= 0 { return Err("non-positive"); }`
     `while i < n { i = i + 1; }`
   - Exhaustive `match`:
     `let msg: String = match res { Ok(v) => "ok", Err(e) => e };`

4. **Core Builtins & `oostd` Standard Library Map**:
   - Strings: `bytes_len(s)`, `byte_at(s, i)`, `byte_slice(s, lo, hi)`, `chars_len(s)`, `char_at(s, i)`, `str_slice(s, lo, hi)`.
   - Lists: `list_new()`, `list_len(xs)`, `list_get(xs, i)`, `list_set(xs, i, v)`, `list_push(xs, v)`, `list_slice(xs, lo, hi)`.
   - Always import `oostd` instead of rolling custom math/physics/crypto/collections:
     - Math & Proofs: `oostd/core/math/{exact,geometry,blas,fft,algebra,graph_topology}/...`, `oostd/core/proofs/...`
     - Physics & Science: `oostd/core/science/{phys,chem,bio,comm,econ}/...` (`classical/collision`, `integrators`, `relativistic`, `quantum`)
     - Frontier AI-for-Science & Engine Physics: `oostd/core/app/ai/...` (`algo`, `deep`, `transformer`, `graph_gnn`, `gguf`, `quant`, `multimodal`), `oostd/core/app/ui/game_engine/...` (2D/3D `collision_{aabb,circle,gjk,sat}`, `ecs_*`, `camera_2d`/`camera_3d_follow`)
     - Security & Collections: `oostd/sec/{hash,capability,pqc,symmetric}/...`, `oostd/core/collection/...`, `oostd/core/app/ai/algo/...`
