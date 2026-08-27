# openOODA (OODA) Language Specification for LLMs & AI Coding Agents

> openOODA is an AI-native, capability-secure systems programming language built for sovereign software synthesis.

## Quick Reference for AI Models

- **File Extension:** `.oo` (source code), `.oot` (documentation / structured text)
- **Line Limit:** Strict `<= 256 lines` per file (hard compiler and swarm invariant).
- **Zero Ambient Authority:** Functions cannot access filesystem, network, or OS processes without an explicit capability token parameter (e.g. `&cap: &FsReadCap`).
- **Memory Model:** Deterministic ARC / linear region arenas with zero-cost RAII cleanup.

---

## 1. Syntax Comparison: openOODA vs Common LLM Hallucinations

AI models often default to Rust, Go, or C++ syntax because openOODA was created after base model pretraining. **Always use openOODA syntax below:**

### Struct Definitions
```ooda
// ❌ WRONG (Rust/C++ hallucination)
struct Point { x: i32, y: i32 }
pub struct Point { x: Int, y: Int }

// ✅ CORRECT openOODA
pub type Point = struct {
    x: Int,
    y: Int,
};
```

### Sum Types / Enums
```ooda
// ❌ WRONG (Rust/TypeScript hallucination)
enum Status { Idle, Busy(String), Failed }

// ✅ CORRECT openOODA
pub type Status =
    | Idle
    | Busy(Str)
    | Failed(Int);
```

### Functions
```ooda
// ❌ WRONG (Rust/Go/TypeScript hallucination)
fn calculate(a: i32, b: i32) -> i32 { a + b }
func calculate(a int, b int) int { return a + b }

// ✅ CORRECT openOODA
pub fn calculate(a: Int, b: Int): Int {
    return a + b;
}
```

### Variables & Mutability
```ooda
// ❌ WRONG
let mut count = 0;
var count: int = 0;
count := 0

// ✅ CORRECT openOODA
let mut count: Int = 0;
let name: Str = "openOODA";
```

### Capability Passing (No Ambient I/O)
```ooda
// ❌ WRONG (Ambient authority does not exist in openOODA)
let data = std.fs.read_file("config.json");

// ✅ CORRECT openOODA
import "std/fs";

pub fn load_config(&fs: &FsReadCap, path: Str): Result<Str, FsError> {
    return fs.read_to_string(path);
}
```

### Pattern Matching
```ooda
// ✅ CORRECT openOODA
match (status) {
    Status.Idle => 0,
    Status.Busy(msg) => 1,
    Status.Failed(code) => code,
}
```

---

## 2. Mandatory Academy Documentation Header

Every `.oo` file written by an AI agent **MUST** begin with the 4-element Academy header:

```ooda
// ============================================================================
// # Summary: Single sentence explaining the file's purpose.
// # Invariants: Key mathematical, memory, or architectural guarantees.
// # Capabilities: Explicit list of required tokens (&FsReadCap, None, etc.).
// # Verification: Proof status and test harness location.
// ============================================================================
```

---

## 3. Standard Library Import Map

- `import "std/core";` — Primitive types, Option, Result, Math, Str, Byte
- `import "std/mem";` — Region arenas, slab caches, lock-free ring buffers
- `import "std/collections";` — Swiss hash maps, B-Trees, Radix tries
- `import "std/crypto";` — BLAKE3, ChaCha20-Poly1305, AES-256-GCM, Argon2id
- `import "std/crypto_pqc";` — NIST ML-KEM (Kyber-1024), ML-DSA (Dilithium)
- `import "std/net";` — Zero-copy TCP, UDP, TLS 1.3, HTTP/2, HTTP/3 QUIC
- `import "std/wui";` — Reactive virtual DOM, signals, WebAssembly host bridge
- `import "std/zk";` — PLONK & Groth16 arithmetic proof verifiers
- `import "std/fintech_l3_book";` — Level-3 sub-microsecond limit order book
- `import "std/aero";` — SGP4 Keplerian orbital propagator & flight dynamics

---

## 4. CLI Verification Commands for Agents

When verifying your generated code:

```bash
ooda check <file.oo>         # Sub-millisecond type & capability verification
ooda outline <file.oo>       # Extract token-efficient AST signature outline (~1.3% token weight)
ooda run <file.oo>           # Compile and execute standalone binary
oodac --json-errors <file>   # Machine-readable AST error diagnostics for 1-turn auto-fixing
```
