# <img src="https://raw.githubusercontent.com/openOODA/.github/master/brand/option-b/openOODA.svg" width="36" align="top"> openOODA

Capability-secured computing stack built 100% in native `.oo` with zero ambient authority and single-cycle 64-bit hardware/software capabilities (`CapReg64`) — `66` product packages across `5` canonical organizations (`75` repos total).

- **Website**: [https://openOODA.org](https://openOODA.org)
- **Binary & ISO Release Hub**: [`openOODA/install@hub`](https://github.com/openOODA/install/releases/tag/hub)
- **Package Registry**: [`openOODA/catalog`](https://github.com/openOODA/catalog)
- **Brand & Icon Gallery**: [`openOODA/.github/brand`](https://github.com/openOODA/.github/tree/master/brand)

## Quick Install

```sh
curl -fsSL https://openOODA.org/install.sh | bash
```

Manage organizations and packages with `ooda-package`:

```sh
ooda-package group list            # List @core, @system, @apps, @games, @workstation, @all
ooda-package install @core         # 11 @openOODA-core toolchain, interface, signing & version packages
ooda-package install @system       # 27 capability-sandboxed @openOODA-system kernel, daemons & shell
ooda-package install @apps         # 19 flagship @openOODA-apps applications
ooda-package install @games        # 9 @openOODA-games engine & native games titles
ooda-package install @workstation  # Full workstation stack (@core + @system + @apps + @games)
ooda-package install @all          # Complete 5-organization stack (66 packages)
```

## 5-Organization Architecture

| Icon | Organization | Repos | Scope |
| :---: | :--- | :---: | :--- |
| <img src="https://raw.githubusercontent.com/openOODA/.github/master/brand/option-b/openOODA.svg" width="28"> | [`@openOODA`](https://github.com/openOODA) | `4` + `.github` | Governance & Quick Cards (`openOODA`), Binary & ISO Hub (`install`), Package Catalog (`catalog`), Website (`website`) |
| <img src="https://raw.githubusercontent.com/openOODA/.github/master/brand/option-b/openOODA-core.svg" width="28"> | [`@openOODA-core`](https://github.com/openOODA-core) | `11` + `.github` | Master CLI (`ooda` incl. build/format/binary), Compiler (`ooda-compiler` incl. `--target x86_64-openooda`), Runtime (`ooda-runtime` / `libooda-runtime*.a` via `OODA_RUNTIME_ROOT`), Standard Library (`ooda-standard`), `ooda-package`, `ooda-language`, `ooda-bridge`, `ooda-verify`, `ooda-interface`, Signing & Provenance (`ooda-sign`), `ooda-version` |
| <img src="https://raw.githubusercontent.com/openOODA/.github/master/brand/option-b/openOODA-system.svg" width="28"> | [`@openOODA-system`](https://github.com/openOODA-system) | `27` + `.github` | Kernel & Boot (`ooda-kernel`, `ooda-boot`, `ooda-drivers`), Zero-Root Daemons (`ooda-start`, `ooda-bus`, `ooda-authority`, `ooda-container`, `ooda-filesystem`, `ooda-health`, `ooda-inference`), Security (`ooda-firewall`, `ooda-vault`, `ooda-connect`), Hardware/Data/Shell/Desktop (`ooda-hardware`, `ooda-data`, `ooda-shell`, `ooda-theme`, `ooda-compositor`, `ooda-dashboard`, `ooda-panel`, `ooda-portal`, `ooda-screensaver`, `ooda-settings`, `ooda-web`) |
| <img src="https://raw.githubusercontent.com/openOODA/.github/master/brand/option-b/openOODA-apps.svg" width="28"> | [`@openOODA-apps`](https://github.com/openOODA-apps) | `19` + `.github` | Flagship Native Applications (`ooda-browser`, `ooda-calculator`, `ooda-calendar`, `ooda-camera`, `ooda-chat`, `ooda-clock`, `ooda-code`, `ooda-files`, `ooda-flasher`, `ooda-media`, `ooda-notepad`, `ooda-office`, `ooda-passwords`, `ooda-photos`, `ooda-remote`, `ooda-screenshot`, `ooda-software`, `ooda-studio`, `ooda-terminal`) |
| <img src="https://raw.githubusercontent.com/openOODA/.github/master/brand/option-b/openOODA-games.svg" width="28"> | [`@openOODA-games`](https://github.com/openOODA-games) | `9` + `.github` | Deterministic Game Engine & Native Games (`ooda-engine`, `ooda-arcade`, `ooda-capella`, `ooda-commander`, `ooda-island`, `ooda-retro`, `ooda-ski`, `ooda-strike`, `ooda-voxel`) |

`ooda-standard` organizes math, proofs, science, collections, and cryptography modules under [`ooda-standard`](https://github.com/openOODA-core/ooda-standard). See [`ROADMAP.md`](ROADMAP.md) and [`spec/01-lexical.md`](spec/01-lexical.md) for the active clean-break engineering specification and validation status.

## Implementation Status & Active Roadmap

| Capability Area | Live Today | Active Target ([`ROADMAP.md`](ROADMAP.md)) |
| :--- | :--- | :--- |
| **Compiler (`ooda-compiler`)** | Self-hosted `S1 == S2` fixed-point via LLVM/Clang (`ELF64`, `PE32+`, `nostd`, `openooda`, `uefi`, `wasm32`); `&*Cap` + `with_cap` + OODA phases + QF_LIA SMT bounds | Phase 1–2 & 4: Hex/bin literals, `[T; N]`, full ADTs, `@repr(C)`, `MmioPtr[T]`, `asm!`, generics/traits/closures, Typed AST → MIR, pure-`.oo` native x86_64/AArch64/RISC-V/WASM/GPU backends + linkers (`PATH=""` zero-Clang build) |
| **Runtime (`ooda-runtime`)** | Pure-`.oo` zero-C static runtime (`15` archives), guarded Safe-Linking slabs, generational arenas, `AuditRing` traps, Landlock | Phase 3: 1-bit literal ARC fast path, 16B slab headers + TLS caches, real OS threads (`clone3`/`futex`), `Mutex`/`Atomic*`/`Channel`, 0 stub exports (`234` → `0`) |
| **Stdlib (`ooda-standard`)** | Strings, paths, fs, hashes/AEAD/PQC (`SHA-2/3`, `ML-KEM-768`, `ML-DSA-65`), TUI/themes, foundational math/collection modules | Phase 5: Deduplicated generic collections (`Vec`, `HashMap`, O(log N) `BTreeMap`), multi-limb `U256`/`U384` ZK, full KAT + analytical/numerical validation of all science/AI modules |
| **OS & System (`@openOODA-system`)** | Bare-metal `ooda-boot` + `ooda-kernel` (paging/SMEP/SMAP/KASLR) + VirtIO drivers + hosted Linux tools | Phase 6: `@repr(C)`/`MmioPtr[T]` kernel/drivers (no `oo_hw_op`), complete Ring-3 syscall ABI + SMP, Linux-decoupled daemons, `make qemu-smoke` native OS boot |

## The 8 Quick Cards (`cards/`) & Spec (`spec/`)

| Card | CLI Command | Description |
| :--- | :--- | :--- |
| [`cards/ooda.md`](cards/ooda.md) | `ooda` | Ecosystem overview, install commands, and workflow reference |
| [`cards/layers.md`](cards/layers.md) | `ooda layers` | Complete 5-organization and 75-repository map |
| [`cards/spec.md`](cards/spec.md) | `ooda spec` | `.oo` syntax, types, structs, `match`, and `ooda-standard` builtins |
| [`cards/rules.md`](cards/rules.md) | `ooda rules` | Power-of-2 shape ladder (`1 / 2 / 4 / 8 / 16 / 32 / 64 / 128 / 256`) and engineering rules |
| [`cards/ui.md`](cards/ui.md) | `ooda ui` | `ooda-theme` 26 presets, 43 semantic color tokens, TUI/Wayland layout laws |
| [`cards/security.md`](cards/security.md) | `ooda security` | `CapReg64` (`32 + 32 = 64`), `ooda-container` containment, and PQC/provenance (`ooda-sign`) |
| [`cards/privacy.md`](cards/privacy.md) | `ooda privacy` | Zero telemetry, `ooda-portal` hardware lease gates, and `ooda-vault` PII scrubbing |
| [`cards/defense.md`](cards/defense.md) | `ooda defense` | Active defense (`ooda-firewall`), IOMMU DMA guards, and DRAM zeroization |

## System Requirements

| Tier | Target Workload | CPU & Vector / TEE Extensions | Memory (RAM & CXL) | Storage & Bus | Host OS / Firmware / Interconnect |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Tier 1: CLI / TUI & Tools** | Pre-built `@openOODA-system`/`@openOODA-apps` tools, `ooda-screensaver`, `ooda-flasher` | `x86_64` (AVX2/AVX-512), `ARM64` (`SVE2`), or `RISC-V` (`RVV 1.0`) (1+ core) | **64 – 256 MiB** (`2–24 MiB` RSS per tool) | **10 – 250 MiB** (`~0.3–3 MiB` per static binary) | Linux `4.19+` (`5.15+` for `io_uring`/Landlock), openOODA OS, Windows 10/11 (`PE32+`), macOS, WASM32 |
| **Tier 2: Bare-Metal OS & Desktop** | `ooda-boot` + `ooda-kernel` + desktop shell (`ooda-compositor`, `ooda-terminal`, `ooda-browser`, 128 Hz engines) | 2+ cores (`4+` rec; Intel RDT / ARM MPAM L3 QoS) | **512 MiB** min (TUI) / **2 – 4 GiB** rec (Wayland desktop & 3D apps) | **1 – 4 GiB** NVMe (ZNS), SATA/AHCI, VirtIO-Blk, SDHCI/eMMC/UFS, or USB4 | UEFI (`x86_64`/`AA64`) + TPM 2.0 / DICE / Caliptra Root-of-Trust, GOP/DRM-KMS/VirtIO-GPU 3D |
| **Tier 3: Developer Workstation** | Building from source with `ooda-compiler`, SMT/Z3 proofs & 8-hat `ooda-verify` verification | 4+ cores / 8+ threads (`16+` threads; AMD SEV-SNP / Intel TDX / ARM CCA TEE) | **8 – 16 GiB** min (`3` compiler slots) / **32 – 64 GiB+** rec (`8` slots) | **20 – 50 GiB** NVMe SSD (75 repos + `.ooda-cache`) | Linux `x86_64` / `ARM64` or openOODA Buildbox container (SR-IOV VF / VirtIO-FS DAX) |
| **Tier 4: AI & Frontier Science** | Local agent swarms (`ooda`, `ooda-inference`) & `ooda-standard` GPU/NPU compute kernels | Multi-core CPU (Intel AMX / ARM SME) + NVIDIA (`CUDA` SM 7.5+) or AMD (`ROCm`) | **16 GiB+** system RAM / **CXL 3.0** pool + **8 – 24 GiB+ VRAM** per GPU | **50 GiB+** NVMe / Peer-to-Peer DMA (`peer_dma`) | Zero-Copy **RDMA / RoCEv2 / InfiniBand** fabric + CUDA, ROCm, or Vulkan (automatic CPU fallback) |

## License, Security & Public Hub

- **License:** [`Apache-2.0 WITH LLVM-exception`](LICENSE) — permissive commercial & open-source adoption with patent grant and zero runtime attribution friction on compiled binaries. See [`TRADEMARKS.md`](TRADEMARKS.md) for brand guidelines.
- **Security & Threat Model:** [`SECURITY.md`](SECURITY.md) & [`THREAT_MODEL.md`](THREAT_MODEL.md).
- **Public Issues, Discussions & Advisories:** All `openOODA-*` component repositories remain **private**. Direct all public comments, bug reports, design discussions, and private vulnerability reports exclusively to [`openOODA/openOODA`](https://github.com/openOODA/openOODA):
  - **Issues:** [github.com/openOODA/openOODA/issues](https://github.com/openOODA/openOODA/issues)
  - **Discussions:** [github.com/openOODA/openOODA/discussions](https://github.com/openOODA/openOODA/discussions)
  - **Private Security Advisories:** [github.com/openOODA/openOODA/security/advisories/new](https://github.com/openOODA/openOODA/security/advisories/new)
