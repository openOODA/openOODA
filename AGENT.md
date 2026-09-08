# Agent Instructions for openOODA

You are operating within the openOODA polyrepo ecosystem. Your execution must be rigorous, deeply skeptical, and strictly bound by the repository's governance laws (`RULES.oot` and `FLOOR.oo`).

## 1. Zero Trust & The Double-Run Law
- **Falsify, never confirm:** Assume every unverified file, test, and claim is defective until a hostile probe proves otherwise. Static analysis is not verification.
- **Double-Run QA:** A test that always passes provides no proof. Hostile negative-trust tests must be run TWICE in fresh processes and produce identical results to be considered verified. 

## 2. Services for Speed (No Shortcuts)
- **Do not blindly `grep` the tree** or read raw files as a substitute for semantic understanding.
- **You MUST use native services:**
  - `mcp` (for orientation and process boards)
  - `lsp` (for resolving definitions and types)
  - `blackbox` (for execution flight recording and crash autopsies)

## 3. Strict Repository Compliance
- **Pure Files:** Only `.oo` and `.oot` files are permitted for logic (no Python, Bash, etc.).
- **Line Limits:** Absolute maximum of 256 lines per file.
- **Academy Headers:** All `.oo` files must begin with the exact 4-element Academy header (`// # Title`, `// Logline:`, `// Setup:`, `// Beats:`).
- **Subtractive Design:** Fix the base before the tower. Delete what earns nothing. Subtraction always beats addition (Boyd's E-M Invariant).

## 4. Commit Hygiene
- **One Repo, One Commit:** Never bundle changes across multiple repositories in a single commit.
- **Docs in the Same Commit:** Any behavioral change must be accompanied by the corresponding `docs/` or task list update in the very same commit. A change without documentation is incomplete.
