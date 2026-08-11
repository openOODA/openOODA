# OODA Programming Language: Feature Specification & Blueprint
**openOODA Project** — `github.com/openOODA`

**OODA** (Observe, Orient, Decide, Act) is a modern, systems-oriented, guard-rail-first programming language designed from the ground up for high reliability, capability security, zero-day defense, self-verification, and rapid AI co-authoring ("vibe coding").

---

## 1. Core Vision & Design Philosophy

* **File Extension**: `.oo` (e.g. `main.oo`, `auth.oo`).
* **The OODA Loop (Rapid Feedback Velocity)**: Sub-second iteration loops between observing code state, orienting diagnostics, deciding edits, and acting on tests.
* **Safety Without Friction**: Make incorrect code impossible to compile without burdening the developer with unnecessary ceremony.
* **Self-Testing Code**: Every function carries its own contracts and executable tests as first-class language constructs.
* **AI Vibe-Coding Native**: Machine-readable AST diff diagnostics, strict contracts, and instant toolchain feedback.
* **Zero-Dependency Ecosystem Standard**: Compiler, LSP, test runner, package manager, formatter, and linter bundled in a single binary (`ooda`).

---

## 2. Type System & Expressiveness

* **Immutability by Default**: Variables are immutable (`let`) unless explicitly declared mutable (`let mut`).
* **Algebraic Data Types & Exhaustive Matching**: No `null` or `undefined`. Optionality and errors use `Option[T]` and `Result[T, E]`. Exhaustive pattern matching is strictly enforced by the compiler.
* **Strong Static Typing with Local Inference**: Inferred types keep syntax clean while maintaining 100% type safety.
* **Traits & Composition over Inheritance**: Interfaces/traits define decoupled behaviors without class hierarchy trees.
* **Refinement Types**: Value bounds verified at compile-time or upon construction:
  ```ooda
  type Port = Int where 1..=65535
  type NonEmptyString = String where self.len() > 0
  ```
* **Strong Newtypes**: Prevent accidental mixing of underlying primitive types:
  ```ooda
  type UserId = newtype u64
  type PostId = newtype u64
  ```

---

## 3. Built-in Guard Rails & Security

* **Capability-Based Security (Effect System)**: Functions must explicitly take capability parameters (`NetCap`, `FsCap`) to perform I/O, preventing unauthorized disk/network access by untrusted packages or AI code:
  ```ooda
  fn fetch_user(net: &NetCap, url: String) -> Result[User, Error]
  ```
* **Must-Use Enforcement**: Unhandled `Result`, `Option`, or resource instances trigger hard compiler errors.
* **No Null/Wild Pointers**: All references are checked; scope-based cleanup ensures zero leaks.

---

## 4. Self-Testing & Executable Contracts

* **Design by Contract (`requires` / `ensures`)**: Preconditions and postconditions run during development and enable the compiler to auto-synthesize property-based tests:
  ```ooda
  fn divide(a: Float, b: Float) -> Float
      requires b != 0.0
      ensures result * b == a
  {
      return a / b
  }
  ```
* **Executable Doc-Tests (`@example`)**: Examples inside function documentation are compiled as mandatory unit tests.
* **Inline `verify` Blocks**: Co-located tests declared right next to function bodies:
  ```ooda
  fn parse_user_id(raw: String) -> Result[UserId, ParseError] { ... }

  verify parse_user_id {
      assert_eq!(parse_user_id("  123 "), Ok(UserId(123)))
  }
  ```
* **Automated Fuzzing (`#[auto_fuzz]`)**: Built-in test runner automatically stress-tests functions against boundary inputs (null bytes, `MAX_INT`, empty arrays, etc.).

---

## 5. Memory & Concurrency Model

* **Deterministic Scope Management (RAII + Region Arenas)**: No global Stop-The-World garbage collection pauses. Automatic memory and resource cleanup at block boundaries.
* **Structured Concurrency**: Async background tasks are strictly bound to parent scope trees—child tasks can never leak or outlive their parent execution block.
* **Zero Data Races**: Thread-shared data must be immutable (`Shared[T]`) or transferred via isolated message channels.

---

## 6. AI & Tooling Integration ("Vibe-Coding Guard Rails")

* **Machine-Readable Diagnostics (`--json-errors`)**: Compiler emits structured JSON errors containing line locations, error codes, and **AST diff patches** for AI agents to auto-fix code instantly.
* **Compile-Time Code Execution (`comptime`)**: Type generation, schema validation, and meta-programming executed using standard language logic at build time (no macro black magic).

---

## 7. Unified Developer Toolchain

Single binary (`ooda`) providing out of the box:
* `ooda build` / `ooda run` — Compiler & runner
* `ooda test` — Integrated unit, contract, doc, and fuzz test runner
* `ooda fmt` — Zero-config code formatter
* `ooda lint` — Static analysis & rule enforcement
* `ooda lsp` — **[STATUS: residual]** Language Server Protocol goal for IDEs (not a shipping daemon on alpha pin)
* `ooda pkg` — Built-in dependency manager

---

## 8. Syntax & Grammar Design

* **Syntax Style**: Hybrid brace-based syntax (`{}`) with clean expression-oriented bodies (similar to TypeScript readability combined with Rust safety).
* **Expression-Based Statements**: `if`, `match`, and blocks return values directly, eliminating temporary mutable accumulator variables:
  ```ooda
  let rating = if score > 90 { "S" } else { "A" };
  ```
* **Explicit Function Contracts**: Keywords `requires`, `ensures`, and `spec` are built-in grammar tokens right above or inside function headers.

---

## 9. Compilation Target Architecture

* **LLVM IR Backend**: Compiles directly to low-level LLVM Intermediate Representation, generating optimized native machine code (x86_64, ARM64/Apple Silicon, RISC-V) comparable to Rust and C++.
* **WebAssembly (WASM) Target**: Compiles to WASM/WASI natively, allowing OODA code to execute securely inside browsers, Cloudflare Workers, or edge runtimes.
* **Instant JIT Mode (`ooda run`)**: Includes a fast JIT/Interpreter frontend for instant execution during rapid AI development and testing iterations, switching to LLVM for release builds.

---

## 10. Multi-Ecosystem Interoperability (FFI & Bridges)

A modern language cannot succeed in isolation. OODA is built to seamlessly talk to existing software ecosystems:

1. **Zero-Cost C-ABI FFI (C / C++ / Rust)**:
   * Direct, zero-overhead import of native `.so`, `.dylib`, or `.dll` libraries without wrapper boilerplate:
   ```ooda
   extern "C" fn sqlite3_open(filename: *const char, db: **sqlite3) -> i32
   ```
2. **Python AI Ecosystem Bridge (`embed "python"`)** — **[STATUS: residual / fail-closed stub]**:
   * Goal: in-process type-safe calls into PyTorch / HuggingFace / NumPy. Alpha product: Python surface may exist as residual stubs; `load_model` / torch import is **not** a working loaded-model path (see `std/os/python.oo` honesty comments). Do not treat sample imports as product-ready:
   ```ooda
   // residual — not a shipping ML embed floor
   // import python::torch
   ```
3. **C-Header Auto-Import**:
   * OODA's compiler can read `.h` files directly at compile time via `comptime` to auto-generate OODA type signatures on the fly.

---

## 11. Zero-Shot AI Adaptability & LLM Memory Optimization

Because OODA is a new language, LLMs will have zero pre-training examples in their training corpus. OODA solves this using **Zero-Shot AI Adaptability**:

1. **Ultra-Compact Grammar Specification (`ooda.grammar`)**:
   * The complete syntax and core grammar can be expressed in an EBNF grammar file under **2,000 tokens (~4 pages of text)**.
   * Any AI agent can ingest the entire language grammar in its system prompt without overloading context memory.

2. **Grammar-Constrained Decoding Support**:
   * Ships with an official `ooda.gbnf` grammar file. LLM samplers (like Gemini, llama.cpp, vLLM) can use this grammar file to force the LLM to output 100% syntactically valid OODA code on the first attempt.

3. **High Orthogonality (Logical Uniformity)**:
   * No special-case syntax rules or obscure syntactic sugar. One way to express each concept (e.g. every control flow construct is an expression, every error is a `Result`).

4. **Compiler-As-Teacher Feedback Loop**:
   * If an LLM makes a mistake, the compiler's JSON diagnostic doesn't just report an error—it explains the rule:
     ```json
     {
       "error": "InvalidKeyword",
       "found": "def",
       "expected": "fn",
       "explanation": "OODA uses 'fn' for function declarations. Example: fn add(a: Int, b: Int) -> Int"
     }
     ```

5. **Self-Describing Standard Library API (`ooda reflect`)**:
   * AI agents can run `ooda reflect <module>` to get concise, token-optimized API signatures and contract specifications directly from the standard library in real time.

---

## 12. Architectural Constraints for LLM Context Optimization

Inspired by real-world AI pair-programming best practices (such as keeping files under 256 lines), OODA bakes file-size modularity directly into the language design:

1. **Zero-Boilerplate File-System Modules**:
   * Drop any `.oo` file into a directory and it is automatically a module (e.g. `src/auth/jwt.oo` -> `auth::jwt`). No manual `mod jwt;` declaration trees needed.

2. **Compiler Modular-Size Lints (`max_file_lines`)**:
   * Built-in linter warns when a single source file exceeds ~256–300 lines.
   * Encourages AI agents and developers to split code at clean, functional boundaries automatically.

3. **Isolated Functional Units**:
   * Each small file encapsulates its types, logic, capability requirements, and co-located `verify` tests in a single, tight context block that fits comfortably inside an LLM's prompt window.

4. **Granular Symbol Reflection**:
   * AI agents can request just a single function's context (`ooda context src/auth/jwt.oo#verify_token`) rather than feeding an entire large repository into the prompt.

5. **Module Type Outlines (`ooda outline`) — 90% Token Reduction**:
   * When an AI agent needs to understand a dependency or sibling file, `ooda outline src/user.oo` returns **only type signatures, contracts, and public APIs**, stripping function bodies completely.
   * Reduces token consumption by **80-90%** when referencing codebase APIs.

6. **Incremental AST Diff Edits (`ooda patch`)**:
   * Instead of generating an entire 256-line file to update 3 lines, AI agents emit surgical AST node patches or diffs (`ooda patch <node_id>`), cutting output tokens by **90%**.

7. **Token-Optimized Diagnostics (`--json-minimal`)**:
   * Compiler errors are formatted into compact, token-dense JSON (stripping boilerplate formatting) so agents process error feedback using minimal tokens.

---

## 13. Comprehensive Security Architecture

OODA implements a multi-layered, zero-trust security model across memory, supply chain, input validation, and AI execution:

1. **Capability-Based Sandboxing (Supply Chain & Dependency Security)**:
   * Third-party packages and imported modules **cannot access disk, network, environment variables, or spawn processes by default**.
   * Access to system resources requires explicit capability tokens passed down from `main()`:
     ```ooda
     // This function CANNOT make network calls or touch disk
     fn parse_jwt(token: String) -> Result[Claims, Error]

     // Requires explicit NetCap handle to make network requests
     fn send_webhook(net: &NetCap, url: String, data: String)
     ```
   * If a malicious package tries to steal `~/.ssh/id_rsa` or env secrets, the compiler rejects it because no `FsCap` or `EnvCap` token was passed to it.

2. **Memory Safety (Eliminating Exploits)**:
   * **No Null Pointers**: Eliminates NullPointerDereference vulnerability class.
   * **Scope-Based RAII & Automatic Bounds Checking**: Array indexing is bounds-checked at compile-time or runtime. Memory is managed deterministically, eliminating Use-After-Free, Double-Free, and Buffer Overflow attacks.

3. **Injection Prevention (SQLi & Command Injection)**:
   * Structured system execution APIs require string arrays rather than raw command strings, blocking shell injection by design:
     ```ooda
     // SAFE: Command and arguments are explicitly separated
     process::exec(sys_cap, "git", ["clone", user_input])
     ```

4. **AI Code Containment (Prompt Injection Defense)**:
   * If an AI model is prompt-injected or hallucinates malicious code, OODA's static capability system and sandboxed JIT runtime trap the execution before it can read system files or execute rogue network calls.

5. **Zero-Day Vulnerability Defense Architecture**:
   * **Default-Deny Capability Trapping**: Even if a 3rd-party dependency contains an unpatched zero-day exploit, the attacker **cannot access disk, network, environment secrets, or shell commands** unless the top-level `main()` function explicitly passed capability handles (`&FsCap`, `&NetCap`) to that specific module. The zero-day is neutralized inside a capability-less sandbox.
   * **[STATUS: residual goal]** **Memory-corruption class defense**: Industry research (Google/Microsoft) attributes a large share of severe zero-days to memory corruption (buffer overflow, UAF, double-free, null deref). openOODA aims to shrink that class via RAII/ARC, bounds checks, and capability defaults — **not** a proven compile-time elimination of ~70% of zero-days on this alpha. Path-A product floors ship; full heap sandbox / dual-green self-host residual. See `PM.md` and `bootstrap/*RESIDUAL*.md`.
   * **Task-Isolated Blast Radius**: Memory is partitioned into isolated task scopes. If a zero-day exploit causes an unrecoverable fault inside a worker task, the supervisor tree kills the isolated task scope without leaking global state or compromising sibling tasks.

---

## 14. High-Performance Engine Architecture

OODA is designed to achieve **C / C++ / Rust level execution speeds** while keeping development ergonomic:

1. **Zero Garbage Collection (0ms Pause Times)**:
   * Uses scope-based RAII and **Region Arena Allocations**. Memory allocated during an HTTP request or game frame is deallocated all at once in a single `O(1)` pointer reset, eliminating Stop-The-World latency spikes.

2. **LLVM IR Optimizer & Bare-Metal Compilation**:
   * Production builds (`ooda build --release`) compile to LLVM IR, leveraging industrial-grade Link-Time Optimization (LTO), dead-code elimination, and auto-vectorization (SIMD / AVX-512 / ARM Neon).

3. **Monomorphized Generics & Value Types**:
   * Structs and primitives are contiguous value types on the stack or memory arena. No pointer chasing or heap boxing (`java.lang.Integer` style overhead). Generics generate specialized native code per type.

4. **Zero-Cost Abstractions & Strippable Contracts**:
   * Higher-order functions (`map`, `filter`), traits, and pattern matching compile down to direct machine jumps and raw loops.
   * `requires` and `ensures` contracts run as inline assertions in debug/test builds, and are optimized out in maximum performance production builds.

5. **Dual-Engine Execution**:
   * **Development (`ooda run`)**: Instant JIT interpreter for sub-second edit/test loops during AI vibe coding.
   * **Production (`ooda build --release`)**: Fully optimized native binary with zero runtime overhead.

---

## 15. Built-in Telemetry, Logging & Debugging Subsystem

OODA integrates structured logging, telemetry, and debugging directly into the core language runtime and toolchain:

1. **Zero-Config Structured Logging & Spans**:
   * Built-in `log::info!`, `log::warn!`, and `log::error!` macros emit structured telemetry (JSON or terminal pretty-print) with zero external dependencies.
   * Async tasks automatically track **tracing spans**, reporting function execution duration, active capability tokens, and parent/child task IDs.

2. **AI-Enriched Stack Traces**:
   * Failures emit clear, structured stack traces containing:
     * Clickable source line URIs (`file:///path/to/file.oo:42`).
     * Exact function argument values passed at the time of failure.
     * Active capability permissions (`FsCap`, `NetCap`).
     * Machine-readable AST diff fix suggestions.

3. **Time-Travel Replay Debugging (`ooda replay`)**:
   * In dev/test mode, OODA can record input streams and scope executions. If a test or contract fails, running `ooda replay <test_id>` replays the exact execution step-by-step deterministically for instant root-cause analysis.

4. **Zero-Overhead Production Probes**:
   * `log::debug!` statements and tracing hooks are compiled out completely in `--release` builds unless explicitly enabled via telemetry feature flags.

5. **Built-in Performance Profiler (`ooda profile`)**:
   * Single command (`ooda profile my_app`) generates CPU flamegraphs, memory allocation heatmaps, and function latency reports without requiring external tools like `perf` or `valgrind`.

---

## 16. First Principles Foundation

OODA was designed by deconstructing programming language design down to fundamental physical and cognitive truths:

### 1. Code, Contracts, and Tests Are One Unified Truth
* **Axiom**: Bugs occur when code, intent, documentation, and tests drift apart into separate tools and files.
* **First Principle**: Functions, preconditions (`requires`), postconditions (`ensures`), doc-examples (`@example`), and unit tests (`verify`) are declared together as a single atomic unit.

### 2. Cognition & LLM Context Are Structurally Finite
* **Axiom**: Both human working memory and LLM prompt windows degrade as context size increases.
* **First Principle**: The language grammar must fit in <2,000 tokens, and source files are naturally soft-capped at ~256 lines with zero-boilerplate file-system module routing.

### 3. Security Is an Invariant of Capabilities, Not Input Sanitization
* **Axiom**: You cannot secure code by trying to sanitize every string; you secure code by denying unauthorized capabilities at the type level.
* **First Principle**: Zero I/O access by default. Functions must explicitly request capability handles (`FsCap`, `NetCap`) from `main()`.

### 4. Memory Lifecycles Follow Execution Scopes
* **Axiom**: Most application memory belongs to a request, a task, or a function block. Garbage collectors waste CPU trying to discover lifecycle patterns that execution scopes already define.
* **First Principle**: Scope-based RAII + Region Arenas achieve $O(1)$ instant deallocation with 0ms GC pause spikes and C-level performance.

### 5. Feedback Velocity Dictates Engineering Quality
* **Axiom**: The shorter the loop between writing code, running tests, and receiving actionable diagnostics, the higher the software quality.
* **First Principle**: Dual JIT/LLVM engines + machine-readable AST diff diagnostics + a zero-config single binary toolchain (`ooda`).

---

## 17. Pre-1.0 Governance, Ecosystem & Release Strategy

1. **Repository visibility**:
   * **[STATUS: alpha pin]** Product is **public** (install pulls GitHub release assets). Governance may keep some boards private; do not claim all repos stay private while alpha ships publicly.

2. **Pre-1.0 Branching & Versioning Pipeline**:
   * Primary development branch: `main` (active pre-release).
   * **Actual pin (PM.md / SPRINT.md):** `v0.184.0-alpha`. **Beta is not claimed.** Historical ladder below is aspirational, not a completed track:
   * `v0.1.0-alpha` — grammar / parser / run path (partial history).
   * `v0.5.0-beta` — **[STATUS: not claimed]** AI diagnostics / verify / fmt goals.
   * `v0.9.0-rc` — **[STATUS: not claimed]** full LLVM + capability verifier goals.
   * `v1.0.0-stable` — future public stable goal.

3. **Batteries-Included Standard Library (`std`)**:
   * **Core Core**: HTTP/Web server, JSON/MessagePack, Cryptography, UTF-8 String, Async Task Runtime, File System, and Math primitives built-in. No need for 50 micro-dependencies just to start a web server.

4. **Decentralized & Lockfile Package Governance (`ooda.lock`)**:
   * Cryptographically hashed lockfiles (`ooda.lock`) guarantee reproducible builds.
   * Supports Git repositories, IPFS, or central registries with strict capability auditing during package installation.

5. **Process Resilience & Actor Supervisor Trees**:
   * Inspired by Erlang/BEAM: Isolated task scopes act as micro-actors. If a child task encounters an unrecoverable failure, supervisor strategies (`one_for_one`, `rest_for_one`) restart only the affected task without bringing down the entire server process.

6. **Automated Migration & Editions (`ooda migrate`)** — **[STATUS: disabled residual]**:
   * Goal: Rust-style edition codemods. **Alpha:** `ooda migrate` is **fail-closed disabled** (SPRINT Issue #14). A prior `sed` that rewrote every `let x =` into `let mut x =` was unsafe and is removed. Do not run migrate expecting a safe codemod until an AST-based tool ships.
