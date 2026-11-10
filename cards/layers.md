# layers.md — The 8-Layer Architecture Map (`L0`–`L7`, `ooda layers`)

1. **Root Umbrella (`@openOODA`)**: Governance Cards (`cards/ooda.md`, `cards/layers.md`, `cards/spec.md`, `cards/rules.md`, `cards/ui.md`, `cards/security.md`, `cards/privacy.md`, `cards/defense.md`), `openOODA`, `catalog`, `install`, `website`, `.github`.
2. **`L0` `@openOODA-core` (Compiler, Runtime & Stdlib — `8` Repos)**:
   - `ooda` (flagship master CLI), `oodac` (`.oo` compiler), `oodar` (native runtime `liboodar.a`), `oostd` (standard library + `oostd/hw/*`), `oopm` (package solver), `oolsp` (LSP), `oomcp` (MCP broker), `oohat` (8-hat verifier & debugger).
3. **`L1` `@openOODA-kernel` (Bare-Metal Microkernel, HAL & Ring-3 Drivers — `8` Repos)**:
   - `ooboot` (UEFI + TPM2/DICE/Caliptra), `oohal` (x86_64/ARM64/RISC-V + SEV-SNP/TDX/CCA + AMX/SVE2/RVV), `ookernel` (sched/mm/ipc/iommu + RDT/MPAM QoS + CXL 3.0), `oodrv-storage` (NVMe/ZNS/AHCI/SDHCI-eMMC/NOR), `oodrv-net` (NIC DMA/RDMA-RoCEv2-IB/Wi-Fi 802.11/BT/5G-WWAN/TSN-CAN-FD), `oodrv-io` (GOP/DRM/PCIe/USB4/HID/MIPI-CSI/V4L2/PCM/IIO-IMU), `oodrv-virt` (VirtIO/SR-IOV VF/VirtIO-GPU 3D/VirtIO-FS DAX), `oodrv-accel` (GPU compute queues, NPU/TPU matrix engines, CXL Type-2/3, PQC/QAT offload).
4. **`L2` `@openOODA-OS` (Zero-Root System Daemons across Desktop, Server & Mobile — `9` Repos)**:
   - `ooinit` (PID 1 & services), `oovfs` (CoW pools, LUKS, mounts), `oonetd` (Wi-Fi WPA3, BT, WireGuard, BGP/OSPF/VLAN), `oosysbus` (devd, wakelocks, sensors, IPP print, A/V graph), `ooauthd`, `oohealthd`, `oocontainer`, `oollama`, `oomodemd` (Mobile 5G/LTE/eSIM).
5. **`L3` `@openOODA-tools` (Capability-Sandboxed Unix, System & Security Multi-Call Utilities — `39` Repos)**:
   - Security/Defense (`7`): `oodefense`, `oosandbox`, `ooprovenance`, `ooredact`, `oosign`, `oofirewall`, `oovault`.
   - Core/System (`32`): `oofs`, `ooperm` (`+elevate`), `oopath`, `oomount` (`+crypt`), `ools`, `oocat`, `oosort`, `ootext`, `oogrep`, `oodiff`, `oojq`, `oocodec`, `oosh`, `ooproc`, `oohw` (`+bt|audio`), `oopower`, `oocron`, `oonet` (`+vpn`), `oocurl`, `ooh`, `ootty`, `ootheme`, `oorgb` (RGB controller), `ooarchive`, `ooawk`, `oofind`, `oofzf`, `oohash`, `ooless`, `oosed`, `ooui`, `ooengine`.
6. **`L4` `@openOODA-DE` (Wayland Desktop & Mobile Touch Environment — `8` Repos)**:
   - `oocomp` (compositor + touch gestures/autorotate), `oopanel` (bar/launcher + `osk` virtual keyboard + `ooagent-hud`), `ooportal` (clipboard TTL burn, cast, a11y, USB guard), `ooterm`, `oofiles`, `oosettings`, `oobazaar`, `oosaver` (51-scene Omarchy screensaver & locker).
7. **`L5` `@openOODA-apps` (Flagship Desktop & Mobile Applications — `16` Repos)**:
   - `oobrowser`, `oostudio`, `oooffice` (`docs|sheet|deck|notes|pdf`), `oocanvas` (`draw|paint|cad`), `oomedia`, `ooflash` (`+pack-iso`), `oodaw`, `oochat`, `oopass`, `ookvm`, `oocamera` (`photo|video|qr|isp`), `ooemu` (multi-core emulator), `ooarcade` (arcade suite), `oocommand` (strategy suite), `oostrike` (6-DoF space combat sim), `oovoxel` (voxel sandbox).
8. **`L6` `@openOODA-cloud` (`8` Repos) & `L7` `@openOODA-agents` (`8` Repos)**:
   - `L6`: `oomesh`, `oostore`, `oodeploy` (`pxe|bmc|vm-fleet`), `oogateway`, `ooidentity`, `oodb` (`sql|local|btree|wal|kv|dump`), `ootelemetry`, `oobilling`.
   - `L7`: `ooloop`, `ooswarm`, `oobench`, `oodream`, `oofalsify`, `ooconsensus`, `oocode`, `oomemory`, `oogovern` (`+ooquota`).
9. **Fleet Census**: `92` total product binaries across `L1`–`L7` (`100` across `L0`–`L7`) + `5` `@openOODA` governance repos (`openOODA`, `catalog`, `install`, `website`, `.github`) = `98` total repos.
