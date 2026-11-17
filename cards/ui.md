# ui.md — CLI, TUI, Desktop & Mobile UI + `ooda-theme` Quick Card (`ooda ui`)

1. **`ooda-theme` Engine (26 Built-In Themes + Circadian Dark/Light Auto-Switching)**:
   - **7 Classic Presets**: `ooda` (flagship Option-B palette, `ooda-dark` alias), `minimax` (default studio slate), `1982` (retro CRT amber/green phosphor), `nord`, `dracula`, `cyberpunk`, `plain`.
   - **12 Monthly + 7 Holiday Presets** (auto-selected via RTC when `theme = auto` in `~/.openooda/theme.oot`):
     `frost` `amethyst` `thaw` `bloom` `meadow` `solstice` `mirage` `amber` `equinox` `ember` `hearth` `solitude` + `nova` `lantern` `sakura` `sol` `spooky` `harvest` `yule`.
   - **Overrides**: `OODA_THEME=<name>`, `OODA_MODE=dark|light|auto`, `OODA_BORDER=round|sharp|double|ascii`, `NO_COLOR=1`.

2. **43 Canonical Semantic Tokens (Never Hardcode Raw ANSI/Hex in Apps/Tools!)**:
   - **UI (`8`)**: `ui_bg`, `ui_fg`, `ui_surface`, `ui_border`, `ui_border_accent`, `ui_muted`, `ui_dim`, `ui_accent`.
   - **Status (`4`)**: `status_success`, `status_warning`, `status_error`, `status_info`.
   - **Syntax (`9`)**: `syntax_keyword`, `syntax_string`, `syntax_number`, `syntax_type`, `syntax_fn`, `syntax_var`, `syntax_comment`, `syntax_op`, `syntax_punct`.
   - **Diff (`4`) & Match (`4`)**: `diff_added`, `diff_removed`, `diff_context`, `diff_header`, `match_hit`, `match_path`, `match_line_num`, `match_col_num`.
   - **Shell (`5`) & Log (`5`)**: `shell_prompt`, `shell_builtin`, `shell_host_bin`, `shell_nav`, `shell_intent`, `log_trace`, `log_debug`, `log_info`, `log_warn`, `log_error`.
   - **Layer (`4`)**: `layer_root`, `layer_core`, `layer_system`, `layer_apps`.

3. **`ooda-interface` Declarative Scene Tree (1 `.oot` Scene -> 4 Surfaces)**:
   - **Surfaces**: One declarative `.oot` scene tree renders to four backends: `tui` (terminal), `gui` (Wayland desktop), `wui` (wearable), `vui` (vehicle/head-up).
   - **Bit Depth**: Selectable color depth `2/4/8/16/32/64/128/256/512`-bit per surface.
   - **Refresh**: Uncapped VRR rendering at `60/120/144/240/360/512+` Hz; apps declare a floor, the compositor schedules the ceiling.
   - **Accessibility (Mandatory)**: Every scene compiles a semantic accessibility tree bridged to the `ooda-portal a11y` bus, ships colorblind LUTs, and supports motor-assist and audio-radar profiles.

4. **`ooda-engine` Game & Simulation Engine (4 Pipelines + Netlock + Mind Bridge)**:
   - **Pipelines**: `core-vm` (deterministic fixed-point VM), `2d-pixel` (true 2D fixed-point coordinates, parallax tiles, integer AABB hitbox/hurtbox solver), `grid-sim` (cellular/agent simulation), `3d-space`/`3d-voxel` (bounded volumetric scenes).
   - **Procgen**: Seeded procedural generation (`RandCap`) shared by all pipelines; identical seed -> bit-identical world.
   - **Netlock**: 3-tier lock over the `ooda-network` fabric — tier-1 state hash, tier-2 input ledger, tier-3 replay attestation — with `<50us` 8-frame arena rollback and a 4-layer zero-trust anti-cheat stack.
   - **Mind Bridge**: Multimodal AI NPC bridge via `ooda-inference` (local inference), `ooda` (tool-using agents), and `ooda-audio` (digital-audio-workstation voice/MIDI surface).

5. **CLI / TUI / Desktop / Mobile / Hardware RGB Surface Rules**:
   - **CLI / TUI (`ooda-theme`)**: Degrade gracefully from 24-bit TrueColor -> 256 -> 16 -> `NO_COLOR`; support `--json` for machine output; use `ooda-theme` subcommands (`table`, `dialog`, `prompt`, `progress`, `figure`, `glyph`, `mascot`).
   - **Desktop (`@openOODA-system`) & Mobile Touch**: Require `WindowCap`/`FrameCap`; support responsive layout down to mobile viewports, `ooda-panel osk` virtual keyboard (+ agent HUD), `ooda-compositor gesture`/`autorotate`, `ooda-screensaver` (51-scene screensaver & locker), and `ooda-portal a11y` accessibility tree.
   - **Hardware RGB Peripheral Sync (`ooda-hardware`)**: Syncs RGB keyboards, mice, chassis LEDs, and `/sys/class/leds` (`HidCap` + `UsbCap`) to the active `ooda-theme` palette (`ooda-hardware rgb sync`, `devices`, `effect static|breathe|wave|reactive|status`, `set <token|hex>`, `brightness`, `off`).
