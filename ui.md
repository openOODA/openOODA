# ui.md — CLI, TUI, Desktop & Mobile UI + `ootheme` Quick Card (`ooda ui`)

1. **`ootheme` Engine (25 Built-In Themes + Circadian Dark/Light Auto-Switching)**:
   - **6 Classic Presets**: `minimax` (default studio slate), `1982` (retro CRT amber/green phosphor), `nord`, `dracula`, `cyberpunk`, `plain`.
   - **12 Monthly + 7 Holiday Presets** (auto-selected via RTC when `theme = auto` in `~/.openooda/theme.oot`):
     `frost` `amethyst` `thaw` `bloom` `meadow` `solstice` `mirage` `amber` `equinox` `ember` `hearth` `solitude` + `nova` `lantern` `sakura` `sol` `spooky` `harvest` `yule`.
   - **Overrides**: `OODA_THEME=<name>`, `OODA_MODE=dark|light|auto`, `OODA_BORDER=round|sharp|double|ascii`, `NO_COLOR=1`.

2. **34 Canonical Semantic Tokens (Never Hardcode Raw ANSI/Hex in Apps/Tools!)**:
   - **UI (`8`)**: `ui_bg`, `ui_fg`, `ui_surface`, `ui_border`, `ui_border_accent`, `ui_muted`, `ui_dim`, `ui_accent`.
   - **Status (`4`)**: `status_success`, `status_warning`, `status_error`, `status_info`.
   - **Syntax (`9`)**: `syntax_keyword`, `syntax_string`, `syntax_number`, `syntax_type`, `syntax_fn`, `syntax_var`, `syntax_comment`, `syntax_op`, `syntax_punct`.
   - **Diff (`4`) & Match (`4`)**: `diff_added`, `diff_removed`, `diff_context`, `diff_header`, `match_hit`, `match_path`, `match_line_num`, `match_col_num`.
   - **Shell (`5`) & Log (`5`)**: `shell_prompt`, `shell_builtin`, `shell_host_bin`, `shell_nav`, `shell_intent`, `log_trace`, `log_debug`, `log_info`, `log_warn`, `log_error`.

3. **CLI / TUI / Desktop / Mobile / Hardware RGB Surface Rules**:
   - **CLI / TUI (`ootheme`)**: Degrade gracefully from 24-bit TrueColor -> 256 -> 16 -> `NO_COLOR`; support `--json` for machine output; use `ootheme` subcommands (`table`, `dialog`, `prompt`, `progress`, `figure`, `glyph`, `mascot`).
   - **Desktop (`openOODA-DE`) & Mobile Touch**: Require `WindowCap`/`FrameCap`; support responsive layout down to mobile viewports, `oopanel osk` virtual keyboard, `oocomp gesture`/`autorotate`, and `ooportal a11y` accessibility tree.
   - **Hardware RGB Peripheral Sync (`openOODA-tools/oorgb`)**: Syncs RGB keyboards, mice, chassis LEDs, and `/sys/class/leds` (`HidCap` + `UsbCap`) to the active `ootheme` palette (`oorgb sync`, `devices`, `effect static|breathe|wave|reactive|status`, `set <token|hex>`, `brightness`, `off`).
