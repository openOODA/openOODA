# 01 — Lexical Grammar & Surface Syntax (`.oo`)

> **Status:** Clean-break specification (`openOODA v3.2.0`). Sections marked `[Target: Phase 1]` become active in Phase 1 of [`ROADMAP.md`](../ROADMAP.md) without backwards-compatibility shims.

## 1. Source Units & Comments
- UTF-8 plain text; **tabs are forbidden** (`0x09` is rejected by `ooda-verify`).
- Line comments: `// ...` to `\n`. Every `.oo` file begins with a 4-element Academy header (`// # Title`, `// Logline:`, `// Setup:`, `// Beats:`) in its top 16 lines.
- Max 256 lines/file (16-line min except `anchor.oo` facades & pure import shims), max 128 chars/line, max 1 statement/line.

## 2. Identifiers & Keywords
- Identifiers: `[A-Za-z_][A-Za-z0-9_]*`, max 32 chars.
- Reserved keywords: `fn`, `pub`, `export`, `let`, `mut`, `const`, `struct`, `enum`, `import`, `extern`, `if`, `else`, `while`, `match`, `return`, `break`, `continue`, `scratch`, `with_cap`, `true`, `false` (`[Target: Phase 1]`: `static`, `trait`, `impl`, `type`, `for`, `in`, `as`, `where`, `requires`, `ensures`, `verify`, `with_domain`, `gpu`).

## 3. Literals
- **Decimal integers:** `[0-9][0-9_]*` `[Target: Phase 1: _ separators & typed suffixes]`
- **Prefixed integers `[Target: Phase 1]`:**
  - Hex: `0[xX][0-9a-fA-F][0-9a-fA-F_]*`
  - Binary: `0[bB][01][01_]*`
  - Octal: `0[oO][0-7][0-7_]*`
  - Optional integer suffix: `i8`, `u8`, `i16`, `u16`, `i32`, `u32`, `i64`, `u64`, `isize`, `usize`.
- **Floats:** `[0-9][0-9_]*\.[0-9][0-9_]*([eE][+-]?[0-9_]+)?` with optional `f32`/`f64` suffix (`f64` default).
- **Strings & Bytes:** `"..."` (C-style escapes `\n`, `\r`, `\t`, `\\`, `\"`, `\0`, `\xHH`), raw strings `r#"..."#` `[Target: Phase 1]`, byte literals `b'x'` `[Target: Phase 1]`.

## 4. Statements, Delimiters & Imports
- Imports are explicit relative paths only (`import "core/foo.oo";` or `import "ooda-standard/..."`), never `::`.
- `if cond { ... }` and `while cond { ... }` forbid redundant outer parentheses around `cond`.
- Trailing commas are permitted in struct definitions/literals, enum variants, function parameter/argument lists, array literals, and `match` arms `[Target: Phase 1]`.
- Labeled loops `'outer: while ... { break 'outer; }` `[Target: Phase 1]`.
