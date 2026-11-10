# openOODA (openOODA) — Constitutional Specification, Quick Cards & Ecosystem Root

Canonical governance root of the openOODA capability-secured computing stack (`L0`–`L7`,
zero ambient authority, single-cycle 64-bit `CapReg64` hardware/software capabilities).
This repository is the constitution: it holds the 8 canonical Quick Cards (`cards/`), the
docs semver (`VERSION`), the consolidated `L0`–`L7` ecosystem census, and a native `.oo`
self-verification surface (`bin/openooda`) that proves every card and invariant without stubs.

## Constitutional Root (10 Entries)

`AGENTS.md` `README.md` `VERSION` `Makefile` `ooda.pkg` `anchor.oo` `cards/` `cli/` `core/` `tests/`
= the canonical 8-entry product blueprint (`AGENTS.md`, `README.md`, `Makefile`, `ooda.pkg`,
`anchor.oo`, `cli/`, `core/`, `tests/`) **plus** `VERSION` + `cards/` (governance-only).

## The 8 Canonical Quick Cards (`cards/`)

Zero-bloat (~24-line) cards served live by the `ooda` master CLI (`ooda <verb>`):

| Card | Verb | Scope |
| :--- | :--- | :--- |
| `cards/ooda.md` | `ooda ooda` | How to rapidly build, test, and adapt openOODA software |
| `cards/layers.md` | `ooda layers` | The 8-Layer Architecture Map `L0`–`L7` across Desktop, Server & Mobile |
| `cards/spec.md` | `ooda spec` | `.oo` syntax, types, structs, `match`, and `oostd` builtins |
| `cards/rules.md` | `ooda rules` | Power-of-2 Shape Ladder `1/2/4/8/16/32/64/128/256` & CLI laws |
| `cards/ui.md` | `ooda ui` | CLI, TUI, Desktop & Mobile UI + `ootheme` 26 presets & 48 tokens |
| `cards/security.md` | `ooda security` | Zero-Trust `CapReg64` `0..31` caps, `oosandbox`, `oosign`, `ooprovenance`, `oovault` |
| `cards/privacy.md` | `ooda privacy` | Zero-telemetry, PII/EXIF/SECRET scrubbing `ooredact`, LED & clipboard TTL gates |
| `cards/defense.md` | `ooda defense` | Active defense `oodefense` IDS/canary/honeypot, `oofirewall`, DMA/DRAM/USB guards |

## The Exact Consolidated L0–L7 Ecosystem (110 Repos)

| Layer | Organization | Repos | Members |
| :--- | :--- | :---: | :--- |
| **Root** | `@openOODA` | `5` | `openOODA`, `catalog`, `install`, `website`, `.github` |
| **L0** | `@openOODA-core` | `8` | `ooda`, `oodac`, `oodar`, `oostd`, `oopm`, `oolsp`, `oomcp`, `oohat` |
| **L1** | `@openOODA-kernel` | `8` | `ooboot`, `oohal`, `ookernel`, `oodrv-storage`, `oodrv-net`, `oodrv-io`, `oodrv-virt`, `oodrv-accel` |
| **L2** | `@openOODA-OS` | `9` | `ooinit`, `oovfs`, `oonetd`, `oosysbus`, `ooauthd`, `oohealthd`, `oocontainer`, `oollama`, `oomodemd` |
| **L3** | `@openOODA-tools` | `39` | Security/Defense (`7`): `oodefense`, `oosandbox`, `ooprovenance`, `ooredact`, `oosign`, `oofirewall`, `oovault`; Core/System (`32`): `oofs`, `ooperm`, `oopath`, `oomount`, `ools`, `oocat`, `oosort`, `ootext`, `oogrep`, `oodiff`, `oojq`, `oocodec`, `oosh`, `ooproc`, `oohw`, `oopower`, `oocron`, `oonet`, `oocurl`, `ooh`, `ootty`, `ootheme`, `oorgb`, `ooarchive`, `ooawk`, `oofind`, `oofzf`, `oohash`, `ooless`, `oosed`, `ooui`, `ooengine` |
| **L4** | `@openOODA-DE` | `8` | `oocomp`, `oopanel` (`+ooagent-hud`), `ooportal`, `ooterm`, `oofiles`, `oosettings`, `oobazaar`, `oosaver` |
| **L5** | `@openOODA-apps` | `16` | `oobrowser`, `oostudio`, `oooffice`, `oocanvas`, `oomedia`, `ooflash`, `oodaw`, `oochat`, `oopass`, `ookvm`, `oocamera`, `ooemu`, `ooarcade`, `oocommand`, `oostrike`, `oovoxel` |
| **L6** | `@openOODA-cloud` | `8` | `oomesh`, `oostore`, `oodeploy`, `oogateway`, `ooidentity`, `oodb`, `ootelemetry`, `oobilling` |
| **L7** | `@openOODA-agents` | `9` | `ooloop`, `ooswarm`, `oobench`, `oodream`, `oofalsify`, `ooconsensus`, `oocode`, `oomemory`, `oogovern` (`+ooquota`) |

**Fleet Census**: `97` product binaries across `L1`–`L7` (`105` across `L0`–`L7`) +
`5` `@openOODA` governance repos = `110` total repos. Folded repos (`ooagent-hud` → `oopanel`,
`ooquota` → `oogovern`) count inside their host, never as separate rows.

## Power-of-2 Shape Ladder (`1/2/4/8/16/32/64/128/256`)

- `1`: Link count == 1 (0 symlinks/hardlinks) & max 1 statement/line.
- `2`: Lean 2-file `tests/` suite (`test_functional.oo` + `test_refusal.oo`, 0 source-grepping).
- `4`: Max 4 nesting depth & 4-Axis Code Review (`oohat Gate` + `Semantic & Spec` + `Native Binary & Systems` + `Ecosystem & Registry`).
- `8`: Max 8 entries/dir, 8 fns/file, 8 params/fn, 8-entry product repo root.
- `16`: Min 16 lines/file. `32`: 32 explicit capabilities (`0..31`), max 32 chars/name, <=32 `.oo` pages/repo.
- `64`: Max 64 code lines/fn. `128`: Max 128 chars/line. `256`: Max 256 lines/file.

## CLI Laws & Self-Verification Surface

- `bin/openooda` verbs: `check`/`audit`/`status`/`verify` (card + ladder + census + law verdicts),
  `cards`, `about`, `theme <name>`, `--self-test`, `--help`, `--version`, additive `--json`.
- Subcommand dispatch only (`<binary> <subcommand>`); `--persona`, `--mode`, `--personas` flags are
  forbidden and every unknown argument or `..` traversal operand refuses with exit `2`.
- Every canonical binary implements `<binary> about`, connects output to `ootheme`, supports
  `NO_COLOR` + `--json`, and refuses unknown flags (`--unknown-flag-zzz`) with exit `2`.
- `core/card_check.oo` proves: all 8 cards exist with markdown titles and real content, `rules.md`
  documents all nine ladder rungs, `VERSION` parses as semver digits, and `layers.md` carries the
  exact census (`97`/`105`/`110`, `L7` = `9` repos, `ooagent-hud`/`ooquota` folds, `ootheme` in `L3`).
- `core/card_law.oo` proves: the constitutional 10-entry root exists, `AGENTS.md` opens with the
  canonical constitutional title, and `README.md` links all eight cards.

## Syntax, Mandatory `oostd` Reuse & Workflow

- Relative string imports only (`import "core/engine.oo";` or `import "oostd/fs/os/fs.oo";`, never `::`).
  No parens on `if cond { }` / `while cond { }`. No struct trailing commas. Academy headers on every page.
- **Always import `oostd` (`L0`)** for math (`oostd/core/math/exact/...`, `geometry/...`), 2D/3D physics &
  collision (`oostd/core/science/phys/classical/...`, `gnc/...`, `relativistic/...`,
  `oostd/core/app/ui/game_engine/...`), frontier AI-for-science & graphs (`oostd/core/app/ai/...`),
  collections (`oostd/core/collection/...`), and crypto/hashing (`oostd/sec/hash/...`,
  `capability/...`)—never re-implement duplicate local helpers!
- Build & Verify: `make build && make test` (or `ooda build && ooda test`), then
  `ooda check && ooda audit` and `oohat cycle` (`quorum_mask=255`).

## Agent Code Intelligence & Tooling (`oolsp` + `oomcp`)

Every agent (CLI, MCP, or LSP client) has direct access to `oolsp` and `oomcp` for zero-grep structural navigation, `oostd` discovery, Power-of-2 headroom inspection, and full ecosystem tool execution:

| Action | CLI (`oolsp` / `oohat`) | MCP Tool (`oomcp`) | LSP Command (`oolsp`) |
| :--- | :--- | :--- | :--- |
| **Read this canonical `AGENTS.md` orientation** | `ooda card` / `cat ~/.openooda/AGENTS.md` | `get_orientation` | `ooda.about` |
| **Search `oostd` for existing functions/types** | `oolsp search-std <query>` | `oolsp_search_std` | `ooda.search_std` |
| **Find symbol definition, import & signature** | `oolsp def <sym> [dir]` | `oolsp_def` | `ooda.def` |
| **List all call sites & references before editing** | `oolsp refs <sym> [dir]` | `oolsp_refs` | `ooda.refs` |
| **Check Power-of-2 shape headroom (`lines/256`, `fns/8`, `sloc/64`)** | `oolsp shape <path>` | `oolsp_shape` | `ooda.shape` |
| **Inspect structural skeleton (Loglines, imports, `pub fn`)** | `oolsp outline <path>` | `oolsp_outline` | `ooda.outline` |
| **Type-check `.oo` file with `oodac`** | `oodac check <file>` | `oodac_check` | `ooda.check` |
| **Run 8-Hat verification cycle (`quorum_mask=255`)** | `oohat cycle <repo> --json` | `oohat_verify` | `ooda.oohat` |
| **Run Zero-Trust binary & git falsification (`L7`)** | `oofalsify audit <repo>` | `oofalsify_audit` | `ooda.falsify` |
| **Apply deterministic source fixer** | `ooda fix <file> --yes` | `ooda_fix` | `ooda.fix` |

- **Native `L7` Agent Tools & Dynamic Host Agent Drop-Ins (`oomcp`)**: `oomcp serve` exposes 34 built-in ecosystem tools (including `get_orientation`, `oofalsify_audit`, `oocode_inspect`, `oomemory_query`, and `oogovern_audit`) and dynamically loads any `~/.openooda/agents/*.oot` descriptors as `agent_list` and `agent_run` (`OODA_MCP_AGENT_DEPTH=1` prevents recursion; stock `oomcp` hardcodes zero external agents). Register `oomcp` in any JSON MCP client config via `oomcp connect <config.json>`.
- **Full Ecosystem LSP Commands**: `oolsp` also exposes the entire `L0`–`L7` tool suite via `workspace/executeCommand` (`ooda.oopm`, `ooda.about`, `ooda.diff`, `ooda.grep`, `ooda.find`, `ooda.jq`, `ooda.ls`, `ooda.tree`, `ooda.cat`, `ooda.sed`, `ooda.fzf`, `ooda.archive`, `ooda.hw`, `ooda.proc`, `ooda.cron`, `ooda.theme`, `ooda.sh`, `ooda.falsify`, `ooda.code`, `ooda.memory`, `ooda.govern`) and seeds all openOODA tools into the canonical LSP symbol index (`workspace/symbol`, `textDocument/completion`, `textDocument/hover`).
- **Package, OS & Container Lifecycle (`oopm`)**: Always use `oopm` to install, update, or remove openOODA and its parts (never manual `cp`): `oopm install openOODA -y` (9-part base platform: `core` + `openooda` + codex), bare groups `oopm install core` / `oopm install tools` / `oopm remove apps` (`core`/`kernel`/`os`/`tools`/`de`/`apps`/`games`/`cloud`/`agents`/`workstation`/`all`, or `@group` aliases), fast SHA-256-diff `oopm update` (`oopm update` or `oopm update tools`), `oopm install ooda-os -y` (`ooflash` + `~/.openooda/images/ooda-os-x86_64.iso`), and `oopm install ooda-container -y` (`oocontainer` + `~/.openooda/containers/ooda-buildbox/`).
