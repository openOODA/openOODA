# layers.md — The 8-Layer Architecture Map (`L0`–`L7`, `ooda layers`)

1. **Root Umbrella (`@openOODA`)**: Governance Cards (`ooda.md`, `layers.md`, `spec.md`, `rules.md`, `ui.md`, `security.md`, `privacy.md`, `defense.md`), `catalog`, `install`, `website`, `status`, `bench`.
2. **`L0` `@openOODA-core` (Compiler, Runtime & Stdlib)**:
   - `ooda` (flagship master CLI), `oodac` (`.oo` compiler), `oodar` (native runtime `liboodar.a`), `oostd` (standard library + `oostd/hw/*`), `oopm` (package solver), `oolsp` (LSP), `oomcp` (MCP broker).
3. **`L1` `@openOODA-kernel` (Bare-Metal Microkernel, HAL & Ring-3 Drivers — `6` Repos)**:
   - `ooboot` (UEFI), `oohal` (x86_64/ARM64/RISC-V), `ookernel` (sched/mm/ipc/iommu), `oodrv-storage` (NVMe/VirtIO-Blk), `oodrv-io` (GOP/PCIe/USB/HID/MIPI-CSI/IIO-IMU/WWAN/Wi-Fi/BT), `oodrv-virt`.
4. **`L2` `@openOODA-OS` (Zero-Root System Daemons across Desktop, Server & Mobile — `9` Repos)**:
   - `ooinit` (PID 1 & services), `oovfs` (CoW pools, LUKS, mounts), `oonetd` (Wi-Fi WPA3, BT, WireGuard, BGP/OSPF/VLAN), `oosysbus` (devd, wakelocks, sensors, IPP print, A/V graph), `ooauthd`, `oohealthd`, `oocontainer`, `oollama`, `oomodemd` (Mobile 5G/LTE/eSIM).
5. **`L3` `@openOODA-tools` (Capability-Sandboxed Unix, System & Security Multi-Call Utilities — `39` Repos)**:
   - Security/Defense (`7`): `oodefense`, `oosandbox`, `ooprovenance`, `ooredact`, `oosign`, `oofirewall`, `oovault`.
   - Core/System (`32`): `oofs`, `ooperm` (`+elevate`), `oopath`, `oomount` (`+crypt`), `ools`, `oocat`, `oosort`, `ootext`, `oogrep`, `oodiff`, `oojq`, `oocodec`, `oosh`, `ooproc`, `oohw` (`+bt|audio`), `oopower`, `oocron`, `oonet` (`+vpn`), `oocurl`, `oossh`, `ootty`, `ootheme`, `oorgb` (RGB controller), `ooarchive`, `ooawk`, `oofind`, `oofzf`, `oohash`, `ooless`, `oosed`, `ooui`, `ooengine`.
6. **`L4` `@openOODA-DE` (Wayland Desktop & Mobile Touch Environment — `8` Repos)**:
   - `oocomp` (compositor + touch gestures/autorotate), `oopanel` (bar/launcher + `osk` virtual keyboard), `ooportal` (clipboard TTL burn, cast, a11y, USB guard), `ooterm`, `oofiles`, `oosettings`, `oobazaar`, `ooagent-hud`.
7. **`L5` `@openOODA-apps` (Flagship Desktop & Mobile Applications — `16` Repos)**:
   - `oobrowser`, `oostudio`, `oooffice` (`docs|sheet|deck|notes|pdf`), `oocanvas` (`draw|paint|cad`), `oomedia`, `ooflash` (`+pack-iso`), `oodaw`, `oochat`, `oopass`, `ookvm`, `oocamera` (`photo|video|qr|isp`), `ooemu` (multi-core emulator), `ooarcade` (arcade suite), `oocommand` (strategy suite), `oostrike` (6-DoF space combat sim), `oovoxel` (voxel sandbox).
8. **`L6` `@openOODA-cloud` (`8` Repos) & `L7` `@openOODA-agents` (`10` Repos)**:
   - `L6`: `oomesh`, `oostore`, `oodeploy` (`pxe|bmc|vm-fleet`), `oogateway`, `ooidentity`, `oodb` (`sql|local|btree|wal|kv|dump`), `ootelemetry`, `oobilling`.
   - `L7`: `ooloop`, `ooswarm`, `oobench`, `ooquota`, `oofalsify`, `ooconsensus`, `oocode`, `oohat`, `oomemory`, `oogovern`.
9. **Fleet Census**: `92` total product binaries across `L1`–`L7` + `6` `@openOODA` governance repos (`openOODA`, `catalog`, `install`, `status`, `website`, `bench`) = `98` total repos.
