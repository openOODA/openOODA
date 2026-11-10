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
oopm group list            # List @core, @kernel, @os, @tools, @de, @apps, @games, @cloud, @agents, @workstation, @all
oopm install @core         # L0 toolchain: ooda, oodac, oodar, oostd, oopm, oolsp, oomcp, oohat
oopm install @tools        # 39 capability-sandboxed L3 utilities
oopm install @workstation  # Full workstation stack (@core + @tools + @de + @apps)
oopm install @all          # Complete L0–L7 stack
```

## L0–L7 Architecture

| Icon | Layer | Organization | Scope |
| :---: | :--- | :--- | :--- |
| <img src="https://raw.githubusercontent.com/openOODA/.github/master/brand/option-b/openOODA.svg" width="28"> | **Root** | [`@openOODA`](https://github.com/openOODA) | Governance & Quick Cards (`openOODA`), Binary & ISO Hub (`install`), Package Catalog (`catalog`), Website (`website`), Org Profile & Brand (`.github`) |
| <img src="https://raw.githubusercontent.com/openOODA/.github/master/brand/option-b/openOODA-core.svg" width="28"> | **L0** | [`@openOODA-core`](https://github.com/openOODA-core) | Master CLI (`ooda`), Native Compiler (`oodac`), Runtime (`oodar`), Standard Library (`oostd`), Package Manager (`oopm`), `oolsp`, `oomcp`, 8-Hat Verifier & Debugger (`oohat`) |
| <img src="https://raw.githubusercontent.com/openOODA/.github/master/brand/option-b/openOODA-kernel.svg" width="28"> | **L1** | [`@openOODA-kernel`](https://github.com/openOODA-kernel) | UEFI Bootloader (`ooboot`), HAL (`oohal`), Capability Microkernel (`ookernel`), 5 Ring-3 Driver Suites (`oodrv-storage`, `oodrv-net`, `oodrv-io`, `oodrv-virt`, `oodrv-accel`) |
| <img src="https://raw.githubusercontent.com/openOODA/.github/master/brand/option-b/openOODA-OS.svg" width="28"> | **L2** | [`@openOODA-OS`](https://github.com/openOODA-OS) | Zero-Root Daemons (`ooinit`, `oovfs`, `oonetd`, `oosysbus`, `ooauthd`, `oohealthd`, `oocontainer`, `oollama`, `oomodemd`) |
| <img src="https://raw.githubusercontent.com/openOODA/.github/master/brand/option-b/openOODA-tools.svg" width="28"> | **L3** | [`@openOODA-tools`](https://github.com/openOODA-tools) | 39 Capability-Sandboxed Unix, System, Security (`oodefense`, `oosandbox`), UI (`ootheme`, `ooui`), & Engine (`ooengine`) Utilities |
| <img src="https://raw.githubusercontent.com/openOODA/.github/master/brand/option-b/openOODA-DE.svg" width="28"> | **L4** | [`@openOODA-DE`](https://github.com/openOODA-DE) | Wayland Compositor (`oocomp`), Panel & Agent HUD (`oopanel` `+ooagent-hud`), Privacy Portals (`ooportal`), Terminal (`ooterm`), Files, Settings, Bazaar, Screensaver (`oosaver`) |
| <img src="https://raw.githubusercontent.com/openOODA/.github/master/brand/option-b/openOODA-apps.svg" width="28"> | **L5** | [`@openOODA-apps`](https://github.com/openOODA-apps) | 16 Native Applications (`oobrowser`, `oostudio`, `oooffice`, `oocanvas`, `oomedia`, `ooflash`, `oodaw`, `ooarcade`, `oostrike`, `oovoxel`) |
| <img src="https://raw.githubusercontent.com/openOODA/.github/master/brand/option-b/openOODA-cloud.svg" width="28"> | **L6** | [`@openOODA-cloud`](https://github.com/openOODA-cloud) | Mesh (`oomesh`), Object Store (`oostore`), Bare-Metal Deploy (`oodeploy`), Gateway (`oogateway`), Identity, DB (`oodb`), Telemetry, Billing |
| <img src="https://raw.githubusercontent.com/openOODA/.github/master/brand/option-b/openOODA-agents.svg" width="28"> | **L7** | [`@openOODA-agents`](https://github.com/openOODA-agents) | Autonomous OODA Loops (`ooloop`, `ooswarm`), Bench (`oobench`), Dream (`oodream`), Falsification (`oofalsify`), Consensus (`ooconsensus`), Code (`oocode`), Memory (`oomemory`), Govern (`oogovern` `+ooquota`) |

`oostd` (L0) ships the expanded scientific & mathematical discovery library: `oostd/core/math/{exact,geometry,blas,fft,algebra,graph_topology}/...`, `oostd/core/proofs/...`, `oostd/core/science/{phys,chem,bio,comm,econ}/...`, frontier AI-for-science `oostd/core/app/ai/...`, 2D/3D engine physics `oostd/core/app/ui/game_engine/...` (`collision_{aabb,circle,gjk,sat}` + `ecs_*`), `oostd/core/collection/...`, and `oostd/sec/{hash,capability,pqc,symmetric}/...`.

## The 8 Quick Cards (`cards/`)

| Card | CLI Command | Description |
| :--- | :--- | :--- |
| [`cards/ooda.md`](cards/ooda.md) | `ooda` | Ecosystem overview, install commands, and workflow reference |
| [`cards/layers.md`](cards/layers.md) | `ooda layers` | Complete `L0`–`L7` organization and repository map |
| [`cards/spec.md`](cards/spec.md) | `ooda spec` | `.oo` language grammar, `CapReg64` (`32 + 32 = 64`), and ABI specification |
| [`cards/rules.md`](cards/rules.md) | `ooda rules` | Power-of-2 shape ladder (`1 / 2 / 4 / 8 / 16 / 32 / 64 / 128 / 256`) and engineering rules |
| [`cards/ui.md`](cards/ui.md) | `ooda ui` | `ootheme` 26 presets, 48 semantic color tokens, TUI/Wayland layout laws |
| [`cards/security.md`](cards/security.md) | `ooda security` | Capability attenuation, CISA KEV defenses, and PQC (`ML-KEM-768` + `ML-DSA-65`) |
| [`cards/privacy.md`](cards/privacy.md) | `ooda privacy` | Zero telemetry, `ooportal` hardware lease gates, and `ooredact` PII scrubbing |
| [`cards/defense.md`](cards/defense.md) | `ooda defense` | Active defense (`oodefense`), `oosandbox` containment, and `oofirewall` rules |

## System Requirements

| Tier | Target Workload | CPU & Vector / TEE Extensions | Memory (RAM & CXL) | Storage & Bus | Host OS / Firmware / Interconnect |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Tier 1: CLI / TUI & Tools** | Pre-built `L2`–`L5` tools, `oosaver` (`idlescreen`), `ooflash` | `x86_64` (AVX2/AVX-512), `ARM64` (`SVE2`), or `RISC-V` (`RVV 1.0`) (1+ core) | **64 – 256 MiB** (`2–24 MiB` RSS per tool) | **10 – 250 MiB** (`~0.3–3 MiB` per static binary) | Linux `4.19+` (`5.15+` for `io_uring`/Landlock), openOODA OS, Windows 10/11 (`PE32+`), macOS, WASM32 |
| **Tier 2: Bare-Metal OS & Desktop** | `ooboot` + `ookernel` + `oode` (`oocomp`, `ooterm`, `oobrowser`, 128 Hz engines) | 2+ cores (`4+` rec; Intel RDT / ARM MPAM L3 QoS) | **512 MiB** min (TUI) / **2 – 4 GiB** rec (Wayland desktop & 3D apps) | **1 – 4 GiB** NVMe (ZNS), SATA/AHCI, VirtIO-Blk, SDHCI/eMMC/UFS, or USB4 | UEFI (`x86_64`/`AA64`) + TPM 2.0 / DICE / Caliptra Root-of-Trust, GOP/DRM-KMS/VirtIO-GPU 3D |
| **Tier 3: Developer Workstation** | Building from source with `oodac`, SMT/Z3 proofs & 8-hat `oohat` verification | 4+ cores / 8+ threads (`16+` threads; AMD SEV-SNP / Intel TDX / ARM CCA TEE) | **8 – 16 GiB** min (`3` compiler slots) / **32 – 64 GiB+** rec (`8` slots) | **20 – 50 GiB** NVMe SSD (110 repos + `.ooda-cache`) | Linux `x86_64` / `ARM64` or openOODA Buildbox container (SR-IOV VF / VirtIO-FS DAX) |
| **Tier 4: AI & Frontier Science** | Local `L7` agent swarm (`ooswarm`, `oocode`, `oodream`) & `oostd` GPU/NPU compute kernels | Multi-core CPU (Intel AMX / ARM SME) + NVIDIA (`CUDA` SM 7.5+) or AMD (`ROCm`) | **16 GiB+** system RAM / **CXL 3.0** pool + **8 – 24 GiB+ VRAM** per GPU | **50 GiB+** NVMe / Peer-to-Peer DMA (`peer_dma`) | Zero-Copy **RDMA / RoCEv2 / InfiniBand** fabric + CUDA, ROCm, or Vulkan (automatic CPU fallback) |
