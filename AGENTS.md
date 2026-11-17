# openOODA (openOODA) — Constitutional Specification, Quick Cards & Ecosystem Root

Canonical governance root of the openOODA capability-secured computing stack (zero ambient
authority, single-cycle 64-bit `CapReg64` hardware/software capabilities). This repository is
the constitution: it holds the 8 canonical Quick Cards (`cards/`), the docs semver (`VERSION`),
the consolidated 4-organization ecosystem census, and a native `.oo` self-verification surface
(`bin/openooda`) that proves every card and invariant without stubs.

## Constitutional Root (10 Entries)

`AGENTS.md` `README.md` `VERSION` `Makefile` `ooda.pkg` `anchor.oo` `cards/` `cli/` `core/` `tests/`
= the canonical 8-entry product blueprint (`AGENTS.md`, `README.md`, `Makefile`, `ooda.pkg`,
`anchor.oo`, `cli/`, `core/`, `tests/`) **plus** `VERSION` + `cards/` (governance-only).

## The 8 Canonical Quick Cards (`cards/`)

Zero-bloat (8..64-line) cards served live by the `ooda` master CLI (`ooda <verb>`):

| Card | Verb | Scope |
| :--- | :--- | :--- |
| `cards/ooda.md` | `ooda ooda` | How to rapidly build, test, and adapt openOODA software |
| `cards/layers.md` | `ooda layers` | The 4-Organization Architecture Map across Desktop, Server & Mobile |
| `cards/spec.md` | `ooda spec` | `.oo` syntax, types, structs, `match`, and `ooda-standard` builtins |
| `cards/rules.md` | `ooda rules` | Power-of-2 Shape Ladder `1/2/4/8/16/32/64/128/256` & CLI laws |
| `cards/ui.md` | `ooda ui` | CLI, TUI, Desktop & Mobile UI + `ooda-theme` 26 presets & 43 tokens |
| `cards/security.md` | `ooda security` | Zero-Trust `CapReg64` `0..31` caps, `ooda-sandbox`, `ooda-sign`, `ooda-provenance`, `ooda-vault` |
| `cards/privacy.md` | `ooda privacy` | Zero-telemetry, PII/EXIF/SECRET scrubbing `ooda-vault`, LED & clipboard TTL gates |
| `cards/defense.md` | `ooda defense` | Active defense `ooda-firewall` IDS/canary/honeypot, DMA/DRAM/USB guards |

## The Canonical 4-Organization Ecosystem (78 Repos)

| Organization | Packages | Repos | Members |
| :--- | :---: | :---: | :--- |
| **Umbrella** `@openOODA` | `4` + `1` | `5` | `openOODA`, `catalog`, `install`, `website` + `.github` |
| **Core** `@openOODA-core` | `15` | `16` | `ooda`, `ooda-binary`, `ooda-bridge`, `ooda-build`, `ooda-compiler`, `ooda-engine`, `ooda-format`, `ooda-interface`, `ooda-language`, `ooda-package`, `ooda-provenance`, `ooda-runtime`, `ooda-sign`, `ooda-standard`, `ooda-verify` + `.github` |
| **System** `@openOODA-system` | `37` | `38` | Base (`10`): `ooda-archive`, `ooda-boot`, `ooda-container`, `ooda-data`, `ooda-drivers`, `ooda-files`, `ooda-hardware`, `ooda-health`, `ooda-kernel`, `ooda-machine`; Services (`11`): `ooda-authority`, `ooda-bus`, `ooda-connect`, `ooda-database`, `ooda-firewall`, `ooda-inference`, `ooda-modem`, `ooda-network`, `ooda-sandbox`, `ooda-shell`, `ooda-vault`; Shell & Tools (`16`): `ooda-compositor`, `ooda-disk`, `ooda-edit`, `ooda-filesystem`, `ooda-list`, `ooda-panel`, `ooda-portal`, `ooda-read`, `ooda-screensaver`, `ooda-settings`, `ooda-start`, `ooda-terminal`, `ooda-text`, `ooda-theme`, `ooda-version`, `ooda-web` + `.github` |
| **Apps** `@openOODA-apps` | `18` | `19` | `ooda-arcade`, `ooda-audio`, `ooda-browser`, `ooda-calculator`, `ooda-camera`, `ooda-canvas`, `ooda-chat`, `ooda-commander`, `ooda-emulator`, `ooda-flasher`, `ooda-office`, `ooda-passwords`, `ooda-player`, `ooda-remote`, `ooda-store`, `ooda-strike`, `ooda-studio`, `ooda-voxel` + `.github` |

**Fleet Census**: `70` product packages (`15` core + `37` system + `18` apps) + `4` `@openOODA`
umbrella repos = `74` product+platform repos; plus `4` `.github` org-profile repos = `78` total
repos across the 4 canonical organizations.

## Power-of-2 Shape Ladder (`1/2/4/8/16/32/64/128/256`)

- `1`: Link count == 1 (0 symlinks/hardlinks) & max 1 statement/line.
- `2`: Lean 2-file `tests/` suite (`test_functional.oo` + `test_refusal.oo`, 0 source-grepping).
- `4`: Max 4 nesting depth & 4-Axis Code Review (`ooda-verify Gate` + `Semantic & Spec` + `Native Binary & Systems` + `Ecosystem & Registry`).
- `8`: Max 8 entries/dir, 8 fns/file, 8 params/fn, 8-entry product repo root.
- `16`: Min 16 lines/file. `32`: 32 explicit capabilities (`0..31`), max 32 chars/name, <=32 `.oo` pages/repo.
- `64`: Max 64 code lines/fn. `128`: Max 128 chars/line. `256`: Max 256 lines/file.

## CLI Laws & Self-Verification Surface

- `bin/openooda` verbs: `check`/`audit`/`status`/`verify` (card + ladder + census + law verdicts),
  `cards`, `about`, `theme <name>`, `--self-test`, `--help`, `--version`, additive `--json`.
- Subcommand dispatch only (`<binary> <subcommand>`); `--persona`, `--mode`, `--personas` flags are
  forbidden and every unknown argument or `..` traversal operand refuses with exit `2`.
- Every canonical binary implements `<binary> about`, connects output to `ooda-theme`, supports
  `NO_COLOR` + `--json`, and refuses unknown flags (`--unknown-flag-zzz`) with exit `2`.
- `core/card_check.oo` proves: all 8 cards exist with markdown titles and real content, `rules.md`
  documents all nine ladder rungs, `VERSION` parses as semver digits, and `layers.md` carries the
  exact census (`70`/`74`/`78`, `15`/`37`/`18` packages, all 4 organizations, `ooda-verify`).
- `core/card_law.oo` proves: the constitutional 10-entry root exists, `AGENTS.md` opens with the
  canonical constitutional title, and `README.md` links all eight cards.

## Syntax, Mandatory `ooda-standard` Reuse & Workflow

- Relative string imports only (`import "core/engine.oo";` or `import "ooda-standard/fs/os/fs.oo";`, never `::`).
  No parens on `if cond { }` / `while cond { }`. No struct trailing commas. Academy headers on every page.
- **Always import `ooda-standard`** for math (`ooda-standard/core/math/exact/...`, `geometry/...`),
  2D/3D physics & collision (`ooda-standard/core/science/phys/classical/...`, `gnc/...`,
  `relativistic/...`, `ooda-standard/core/app/ui/game_engine/...`), frontier AI-for-science &
  graphs (`ooda-standard/core/app/ai/...`), collections (`ooda-standard/core/collection/...`),
  and crypto/hashing (`ooda-standard/sec/hash/...`, `capability/...`)—never re-implement
  duplicate local helpers!
- Build & Verify: `make build && make test` (or `ooda build && ooda test`), then
  `ooda check && ooda audit` and `ooda-verify cycle .` (`quorum_mask=255`).

## Agent Code Intelligence & Tooling (`ooda-language` + `ooda-bridge`)

Every agent (CLI, MCP, or LSP client) has direct access to `ooda-language` and `ooda-bridge` for
zero-grep structural navigation, `ooda-standard` discovery, Power-of-2 headroom inspection, and
full ecosystem tool execution:

| Action | CLI | MCP Tool (`ooda-bridge`) | LSP Command (`ooda-language`) |
| :--- | :--- | :--- | :--- |
| **Read this canonical `AGENTS.md` orientation** | `ooda card` / `cat ~/.openooda/AGENTS.md` | `get_orientation` | `ooda.about` |
| **Search `ooda-standard` for existing functions/types** | `ooda-language search-std <query>` | `ooda_language_search_std` | `ooda.search_std` |
| **Find symbol definition, import & signature** | `ooda-language def <sym> [dir]` | `ooda_language_def` | `ooda.def` |
| **List all call sites & references before editing** | `ooda-language refs <sym> [dir]` | `ooda_language_refs` | `ooda.refs` |
| **Check Power-of-2 shape headroom (`lines/256`, `fns/8`, `sloc/64`)** | `ooda-language shape <path>` | `ooda_language_shape` | `ooda.shape` |
| **Inspect structural skeleton (Loglines, imports, `pub fn`)** | `ooda-language outline <path>` | `ooda_language_outline` | `ooda.outline` |
| **Type-check `.oo` file with `ooda-compiler`** | `ooda-compiler check <file>` | `ooda_compiler_check` | `ooda.check` |
| **Run 8-Hat verification cycle (`quorum_mask=255`)** | `ooda-verify cycle <repo> --json` | `ooda_verify` | `ooda.verify` |
| **Run Zero-Trust binary & git falsification** | `ooda-verify falsify <repo>` | `ooda_falsify_audit` | `ooda.falsify` |
| **Run local/fleet GPU inference (`ooda-inference`)** | `ooda-inference run <prompt>` | `ooda_inference` / `ooda_inference_models` | — |
| **Apply deterministic source fixer** | `ooda fix <file> --yes` | `ooda_fix` | `ooda.fix` |

- **Native Inference (`ooda-inference`), Agent Tools & Dynamic Host Agent Drop-Ins (`ooda-bridge`)**:
  `ooda-bridge serve` exposes the built-in ecosystem tools (including `get_orientation`,
  `ooda_inference`, `ooda_inference_models`, `ooda_falsify_audit`, `ooda_code_inspect`,
  `ooda_memory_query`, and `ooda_govern_audit`) and dynamically loads any
  `~/.openooda/agents/*.oot` descriptors as `agent_list` and `agent_run` (`ooda-bridge agents`
  prints the live roster; `OODA_MCP_AGENT_DEPTH=1` prevents recursion). Register `ooda-bridge`
  in any JSON MCP client config via `ooda-bridge connect <config.json>`.
- **Full Ecosystem LSP Commands**: `ooda-language` also exposes the entire tool suite via
  `workspace/executeCommand` (`ooda.package`, `ooda.about`, `ooda.diff`, `ooda.grep`,
  `ooda.find`, `ooda.jq`, `ooda.ls`, `ooda.tree`, `ooda.cat`, `ooda.sed`, `ooda.fzf`,
  `ooda.archive`, `ooda.hw`, `ooda.proc`, `ooda.cron`, `ooda.theme`, `ooda.sh`, `ooda.falsify`,
  `ooda.code`, `ooda.memory`, `ooda.govern`) and seeds all openOODA tools into the canonical
  LSP symbol index (`workspace/symbol`, `textDocument/completion`, `textDocument/hover`).
- **Package, OS & Container Lifecycle (`ooda-package`)**: Always use `ooda-package` to install,
  update, or remove openOODA and its parts (never manual `cp`): `ooda-package install openOODA -y`,
  bare groups `ooda-package install @core` / `ooda-package install @system` / `ooda-package remove @apps`
  (`@core`/`@system`/`@apps`/`@games`/`@workstation`/`@all`), fast SHA-256-diff `ooda-package update`,
  `ooda-package install ooda-os -y` (`ooda-flasher` + `~/.openooda/images/ooda-os-x86_64.iso`), and
  `ooda-package install ooda-container -y` (`ooda-container` + `~/.openooda/containers/ooda-buildbox/`).
