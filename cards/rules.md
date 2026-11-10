# rules.md — Power-of-2 Shape Ladder & CLI Laws (`ooda rules`)

1. **Canonical Power-of-2 Shape Ladder (`1 / 2 / 4 / 8 / 16 / 32 / 64 / 128 / 256`)**:
   - **`1` (`2^0`)**: Link count == `1` (ZERO symlinks or hardlinks anywhere) & max `1` statement per line.
   - **`2` (`2^1`)**: Lean `2`-file `tests/` suite per repo (`tests/test_functional.oo` + `tests/test_refusal.oo`, zero subdirectories, zero source-file grepping).
   - **`4` (`2^2`)**: Max `4` levels of block nesting depth inside a function (use early returns/guards) & **4-Axis Code Review** (`1. oohat Gate` + `2. Semantic Logic & Spec` + `3. Native Binary & Systems` + `4. Ecosystem & Registry`).
   - **`8` (`2^3`)**: Max `8` entries per directory (`DENSE`), max `8` functions per file (`MANYFN`), max `8` parameters per function, & Canonical `8`-Entry Repo Root (`AGENTS.md`, `README.md`, `Makefile`, `ooda.pkg`, `anchor.oo`, `cli/`, `core/`, `tests/`); the `@openOODA` governance root adds `VERSION` + `cards/` (`10` constitutional entries).
   - **`16` (`2^4`)**: Min `16` lines per `.oo` file (`TINYFILE` — zero empty stub files).
   - **`32` (`2^5`)**: `32` explicit capabilities (`0..31`), max `32` chars per identifier/filename (ban `*_1.oo` / `*_part2.oo` / `*_more.oo` mechanical splits), target `<= 32` `.oo` pages per repo.
   - **`64` (`2^6`)**: Max `64` code lines per function (`LONGFN`, excluding comments and blank lines).
   - **`128` (`2^7`)**: Max `128` characters per line.
   - **`256` (`2^8`)**: Max `256` lines per `.oo` file (`BIGFILE` = 1 Page).

2. **CLI, Theme, `oostd` Reuse & Zero-Trust Laws**:
   - Subcommand dispatch only (`<binary> <subcommand>`); `--persona`, `--mode`, and `--personas` flags are forbidden and must exit `2`.
   - Every canonical binary MUST implement `<binary> about`, connect output to `ootheme`, and refuse unknown flags (`--unknown-flag-zzz`) with exit `2`.
   - **Mandatory `oostd` Standard Library Reuse**: Never hand-roll custom hashing, crypto, fixed-point/interval math, 2D/3D collision/physics/engine wiring, frontier AI-for-science/graph algorithms, or collections when `oostd` provides them (`oostd/core/math/`, `oostd/core/science/phys/`, `oostd/core/app/ai/`, `oostd/core/app/ui/game_engine/`, `oostd/core/collection/`, `oostd/sec/`, `oostd/net/`, `oostd/fs/`).
   - Zero `/usr/bin/*` host shell-out relays; all personas must run native `.oo` engines.
