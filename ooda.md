# ooda.md — How to Quickly Build & Adapt openOODA Software (`ooda ooda`)

1. **Find Where Code Belongs (Never Duplicate Repos)**:
   - Run `ooda about` (lists all layers `L0`–`L7`) or `ooda search <keyword>` before writing code.
   - Route UI/scene work to `ooui` (`.oot` scene tree -> `tui|gui|wui|vui`), simulation/game work to `ooengine` (4 pipelines + `oomesh` netlock), and original games to the `L5` `@openOODA-apps` titles (`ooemu`, `ooarcade`, `oocommand`, `oostrike`, `oovoxel`).
   - Add new features as clean subcommands inside the canonical domain binary (`<binary> <subcommand>`), never via `--mode`/`--persona` flags or symlinks.

2. **Standard Repository Anatomy (`<= 32` `.oo` Pages, `<= 8` Entries/Dir)**:
   - `main.oo`: Capability-explicit entrypoint (`pub fn main(fs_r: &FsReadCap, ...) -> Result[Int, String]`), routing `--help`, `--version`, `about`, `--mcp`, and subcommands; unknown flags MUST exit `2`.
   - `core/`: Pure deterministic domain logic (`<= 256` lines/file, `<= 64` code lines/fn, `<= 8` fns/file).
   - `render/`: Output formatting wired to **`ootheme`** semantic tokens (`ui_accent`, `status_success`, `status_error`, `diff_added`, etc.) with `NO_COLOR` & `--json` support.
   - `ipc/`: Optional `--mcp` JSON-RPC tool server (`json_unescape`-safe).
   - `tests/`: At least 1 real functional I/O test + 1 negative-trust refusal test (`--unknown-flag-zzz` -> exit `2`, invalid capability -> `Err`).

3. **3-Command Fast OODA Loop**:
   - `ooda build && ooda test` -> Compile (`main.oo -> dist/<bin>`) and run functional + negative-trust tests.
   - `ooda check && ooda audit` -> Verify `1/2/4/8/16/32/64/128/256` shape ladder and 8-hat `oohat cycle` (`quorum_mask=255`).
   - `ooda sync` -> Pull latest GitHub commits across `/Projects/openOODA*` and rebuild changed binaries into `~/.openooda/bin/`.
