# openOODA (.oo) Agent Quick Card
1. **Discover & Learn On-Demand** (Zero-bloat ~24-line cards built into `ooda`):
   - `ooda ooda`     -> How to quickly build, adapt, and verify openOODA software
   - `ooda about [x]`-> Explain any layer (`L0`–`L7`), canonical binary, or subcommand
   - `ooda spec`     -> `.oo` syntax, types, structs, `match`, and `oostd` builtins
   - `ooda rules`    -> Power-of-2 Shape Ladder (`1/2/4/8/16/32/64/128/256`) & CLI laws
   - `ooda security` -> Zero-Trust `CapReg64` (`0..31` capabilities), `oosandbox`, `oosign`, `ooprovenance`
   - `ooda privacy`  -> Zero-telemetry, PII/EXIF/SECRET scrubbing (`ooredact`), LED & clipboard TTL gates
   - `ooda defense`  -> Active defense (`oodefense` IDS/canary/honeypot), `oofirewall`, DMA/DRAM/USB guards
2. **Power-of-2 Shape Ladder (`1/2/4/8/16/32/64/128/256`)**:
   - `1`: Link count == 1 (0 symlinks/hardlinks) & max 1 statement/line. `2`: Min 2 tests (functional + negative-trust exit != 0).
   - `4`: Max 4 nesting depth. `8`: Max 8 files/dir, 8 fns/file, 8 params/fn. `16`: Min 16 lines/file.
   - `32`: 32 explicit capabilities (`&FsReadCap`, `&FsWriteCap`, `&NetCap`, `&ProcessCap`, `&EnvCap`), max 32 chars/name (no `*_1.oo` splits), <=32 files/repo.
   - `64`: Max 64 code lines/fn. `128`: Max 128 chars/line. `256`: Max 256 lines/file.
3. **Syntax & Workflow**:
   - Relative string imports only (`import "core/engine.oo";` or `import "oostd/fs/os/fs.oo";`, never `::`). No parens on `if cond { }` / `while cond { }`. No struct trailing commas. Connect all CLI/TUI/GUI output to `ootheme` and expose `<binary> about`.
   - Build & Verify: `ooda build && ooda test && ooda check && ooda audit`.
