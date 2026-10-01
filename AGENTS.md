# openOODA: House Laws & Agent Engineering Standards (v1)

This document is the **single canonical source of truth** for all code, architecture, and system integration standards across the `openOODA` organization. Every human contributor and AI agent must strictly follow these rules without exception.

---

## 1. The Page Rule (Code Layout & Sizing)

A **page** is one committed `.oo` or `.oot` file. Every page holds one idea, fits in one head, and carries its own weight.

### Hard Sizing Invariants
- **16–256 Lines**: Every committed `.oo` source file must be between **16 and 256 lines**, counted as exact line breaks (blank lines and comments count).
- **Shim Exemption (Floor Only)**: A file is a shim when every non-comment line is an import or re-export (`import "..."`). Shims skip the 16-line floor. The **256-line ceiling still strictly applies**.
- **Directory Density ($\le 8$ pages)**: At most **8 `.oo` pages per directory**, tests included. Crowded directories must split into functional subdirectories grouped by domain, linked via an `anchor.oo` shim.
- **Banned File Names (Name the function, not the drawer)**:
  `util.oo`, `utils.oo`, `helper.oo`, `helpers.oo`, `common.oo`, `misc.oo`, `shared.oo`, `base.oo`, `core.oo`.

### Splitting, Folding, and Naming
- **Over 256 lines**: Split along functional boundaries into a new subdirectory with an `anchor.oo` shim. One page = one verb or one wholly owned noun.
- **Under 16 lines (and not a shim)**: Fold into its closest sibling or caller. Never pad lines with artificial whitespace or comments to reach 16.
- **Action pages lead with a verb**: `render_prompt.oo`, `dispatch_intent.oo`, `emit_llvm.oo`.
- **State pages name what they own**: `session_state.oo`, `symbol_table.oo`.
- **Boundary pages speak trust verbs**: `verify_token.oo`, `admit_binary.oo`, `enforce_sandbox.oo`.

---

## 2. The 4-Element Academy Header (Mandatory on Every Page)

Every committed `.oo` file must begin with the standard 4-element Academy docstring:

```oo
// # Component Name - Subtitle
//
// Logline: Single-sentence imperative summary of functional responsibility.
//
// Setup: Preconditions, wired capability tokens, imported contracts.
//
// Beats:
//   1. First sequential phase of execution.
//   2. Next phase.
//   3. Final phase / exit state.
```

- **ASD-STE100 Compliance**: Clear, concise technical English. No marketing fluff or ambiguous verbs.
- **Imports**: All imports must be relative string literals (e.g. `import "std/fs/path.oo";`). Never use `::` namespaces.

---

## 3. openOODA Capability & Security Discipline

openOODA operates strictly on the Object-Capability (OCap) security model:

### Unforgeable Capability Tokens
- **Zero Ambient Authority**: Privileged operations (spawning processes, reading files, opening network sockets, modifying environment) require explicit, unforgeable capability tokens passed as arguments (`&ProcessCap`, `&FsReadCap`, `&FsWriteCap`, `&EnvCap`, `&NetCap`, `&SysCap`, `&TimeCap`, `&AllocCap`, `&ThreadCap`).
- **Landlock & Sandboxing**: All runtime execution and untrusted evaluation must execute within isolated Landlock sandboxes via `oodar`.
- **Subprocess Safety**: Never invoke `/bin/sh -c` or `/bin/bash -c` blindly. Direct binary execution must use explicit argv arrays via `ProcessCap`. Clean environment variables of child processes to prevent leakage of credentials or internal state.

---

## 4. Per-Page Performance Scorecard & Invariants

Performance is verified continuously across the ecosystem:
- **`lines`**: Source line count (16–256).
- **`ir_lines`**: Number of LLVM IR lines emitted by `oodac emit-ir`.
- **`check_time_ms`**: Duration to typecheck with `oodac check`.
- **`rss_kb`**: Compiler peak memory during module check.
- **The Performance Invariant**: **A change may not grow a page's binary weight, emitted IR line count, or compiler memory overhead without written justification in the commit message.**

---

## 5. Universal QA & Negative-Trust Verification

Before any commit or release is certified, the codebase must pass the verification gate:

1. **Sovereign Test Driver (`cli qa`)**: Run tests locally with `cli qa` or polyrepo suites with `cli qa --all`.
2. **Negative-Trust Edge Falsification**: Prohibit single-sided happy-path suites. Releases require fail-closed validation on boundary inputs (0-byte files, oversized inputs, malformed envelopes, invalid tokens).
3. **Sequential Double-Run Determinism Filter**: Every verification probe must execute twice sequentially in fresh processes (`Run_1 == Run_2`). Double-run is a determinism filter ensuring zero state leakage across invocations.
4. **Binary Parity Law**: Release certification must run against the bit-identical binary installed for the user (`sha256sum ~/.openooda/bin/<tool> == sha256sum dist/<tool>`).

---

## 6. Ecosystem Directory Roles & Decoupled Architecture

The N-Binary ecosystem strictly separates domains:
- **`oodac`**: Direct LLVM IR compiler (AST, mem2reg, IR emission).
- **`oodar`**: C runtime substrate, Landlock sandboxing, and OCap primitives.
- **`cli`**: Sovereign developer driver (`build`, `run`, `test`, `fmt`, `install`, `qa`, `fix`).
- **`ooda`**: Back-compat command router forwarding to `cli`, `opm`, `lsp`, `mcp`, `tui`.
- **`mcp`**: Model Context Protocol server, flight recording, telemetry, and fold protocol.
- **`tui`**: Terminal interface and motor-reflex interactive shell ($\le 2\text{ms}$ keystroke SLA).
- **`opm`**: Package manager and template code generator.
- **`lsp`**: Language Server Protocol engine.
- **`std`**: Standard library across 8 functional domains.
