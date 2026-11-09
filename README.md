# <img src="https://raw.githubusercontent.com/openOODA/.github/master/brand/option-b/openOODA.svg" width="36" align="top"> openOODA

Capability-secured computing stack (`L0`–`L7`) built 100% in native `.oo` with zero ambient authority and single-cycle 64-bit hardware/software capabilities (`CapReg64`).

- **Website**: [https://openOODA.org](https://openOODA.org)
- **Binary & ISO Release Hub**: [`openOODA/install@hub`](https://github.com/openOODA/install/releases/tag/hub)
- **Package Registry**: [`openOODA/catalog`](https://github.com/openOODA/catalog)
- **Brand & Icon Gallery**: [`openOODA/.github/brand`](https://github.com/openOODA/.github/tree/master/brand)

## Quick Install

```sh
curl -fsSL https://openOODA.org/install.sh | bash
```

Manage layers and packages with `oopm`:

```sh
oopm group list            # List @core, @kernel, @os, @tools, @de, @apps, @cloud, @agents, @workstation, @all
oopm install @core         # L0 toolchain: ooda, oodac, oodar, oostd, oopm, oolsp, oomcp
oopm install @tools        # 39 capability-sandboxed L3 utilities
oopm install @workstation  # Full workstation stack (@core + @tools + @de + @apps)
oopm install @all          # Complete L0–L7 stack
```

## L0–L7 Architecture

| Icon | Layer | Organization | Scope |
| :---: | :--- | :--- | :--- |
| <img src="https://raw.githubusercontent.com/openOODA/.github/master/brand/option-b/openOODA.svg" width="28"> | **Root** | [`@openOODA`](https://github.com/openOODA) | Governance & Quick Cards (`openOODA`), Binary & ISO Hub (`install`), Package Catalog (`catalog`), Website (`website`) |
| <img src="https://raw.githubusercontent.com/openOODA/.github/master/brand/option-b/openOODA-core.svg" width="28"> | **L0** | [`@openOODA-core`](https://github.com/openOODA-core) | Master CLI (`ooda`), Native Compiler (`oodac`), Runtime (`oodar`), Standard Library (`oostd`), Package Manager (`oopm`), `oolsp`, `oomcp` |
| <img src="https://raw.githubusercontent.com/openOODA/.github/master/brand/option-b/openOODA-kernel.svg" width="28"> | **L1** | [`@openOODA-kernel`](https://github.com/openOODA-kernel) | UEFI Bootloader (`ooboot`), HAL (`oohal`), Capability Microkernel (`ookernel`), Ring-3 Drivers (`oodrv-io`, `oodrv-storage`, `oodrv-virt`) |
| <img src="https://raw.githubusercontent.com/openOODA/.github/master/brand/option-b/openOODA-OS.svg" width="28"> | **L2** | [`@openOODA-OS`](https://github.com/openOODA-OS) | Zero-Root Daemons (`ooinit`, `oovfs`, `oonetd`, `oosysbus`, `ooauthd`, `oohealthd`, `oocontainer`, `oollama`, `oomodemd`) |
| <img src="https://raw.githubusercontent.com/openOODA/.github/master/brand/option-b/openOODA-tools.svg" width="28"> | **L3** | [`@openOODA-tools`](https://github.com/openOODA-tools) | 39 Capability-Sandboxed Unix, System, Security (`oodefense`, `oosandbox`), UI (`ootheme`, `ooui`), & Engine (`ooengine`) Utilities |
| <img src="https://raw.githubusercontent.com/openOODA/.github/master/brand/option-b/openOODA-DE.svg" width="28"> | **L4** | [`@openOODA-DE`](https://github.com/openOODA-DE) | Wayland Compositor (`oocomp`), Panel (`oopanel`), Privacy Portals (`ooportal`), Terminal (`ooterm`), Files, Settings, Bazaar, HUD |
| <img src="https://raw.githubusercontent.com/openOODA/.github/master/brand/option-b/openOODA-apps.svg" width="28"> | **L5** | [`@openOODA-apps`](https://github.com/openOODA-apps) | 16 Native Applications (`oobrowser`, `oostudio`, `oooffice`, `oocanvas`, `oomedia`, `ooflash`, `oodaw`, `ooarcade`, `oostrike`, `oovoxel`) |
| <img src="https://raw.githubusercontent.com/openOODA/.github/master/brand/option-b/openOODA-cloud.svg" width="28"> | **L6** | [`@openOODA-cloud`](https://github.com/openOODA-cloud) | Mesh (`oomesh`), Object Store (`oostore`), Bare-Metal Deploy (`oodeploy`), Gateway (`oogateway`), Identity, DB (`oodb`), Telemetry, Billing |
| <img src="https://raw.githubusercontent.com/openOODA/.github/master/brand/option-b/openOODA-agents.svg" width="28"> | **L7** | [`@openOODA-agents`](https://github.com/openOODA-agents) | Autonomous OODA Loops (`ooloop`, `ooswarm`), 8-Hat Verification (`oohat`), Falsification (`oofalsify`), Consensus, Code, Memory, Quota, Govern |

## The 8 Quick Cards (`cards/`)

| Card | CLI Command | Description |
| :--- | :--- | :--- |
| [`cards/ooda.md`](cards/ooda.md) | `ooda` | Ecosystem overview, install commands, and workflow reference |
| [`cards/layers.md`](cards/layers.md) | `ooda layers` | Complete `L0`–`L7` organization and repository map |
| [`cards/spec.md`](cards/spec.md) | `ooda spec` | `.oo` language grammar, `CapReg64` (`32 + 32 = 64`), and ABI specification |
| [`cards/rules.md`](cards/rules.md) | `ooda rules` | Power-of-2 shape ladder (`1 / 2 / 4 / 8 / 16 / 32 / 64 / 128 / 256`) and engineering rules |
| [`cards/ui.md`](cards/ui.md) | `ooda ui` | `ootheme` 25 presets, 34 semantic color tokens, TUI/Wayland layout laws |
| [`cards/security.md`](cards/security.md) | `ooda security` | Capability attenuation, CISA KEV defenses, and PQC (`ML-KEM-768` + `ML-DSA-65`) |
| [`cards/privacy.md`](cards/privacy.md) | `ooda privacy` | Zero telemetry, `ooportal` hardware lease gates, and `ooredact` PII scrubbing |
| [`cards/defense.md`](cards/defense.md) | `ooda defense` | Active defense (`oodefense`), `oosandbox` containment, and `oofirewall` rules |
