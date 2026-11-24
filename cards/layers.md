# layers.md — The 5-Organization Architecture Map (`ooda layers`)

1. **Umbrella (`@openOODA` — `4` Repos + `.github` Org Profile)**: Constitutional governance & Quick Cards (`cards/`), `openOODA`, `catalog`, `install`, `website`.
2. **`@openOODA-core` (Toolchain, Runtime, Interface & Signing — `11` Packages)**:
   - Toolchain (`8`): `ooda` (master CLI + build/format/binary), `ooda-compiler` (`.oo` compiler incl. `--target x86_64-openooda`), `ooda-runtime` (`libooda-runtime*.a` via `OODA_RUNTIME_ROOT`), `ooda-standard` (standard library), `ooda-package` (package solver), `ooda-language` (LSP), `ooda-bridge` (MCP broker), `ooda-verify` (8-hat verifier & debugger).
   - Foundations (`3`): `ooda-interface` (multi-surface scenes), `ooda-sign` (PQC/Ed25519/mTLS/ZK + TPM2/SEV-SNP/DDC/Merkle provenance), `ooda-version` (workspace & release versions).
3. **`@openOODA-system` (Kernel, Boot, Drivers, Daemons, Shell & Desktop — `27` Packages)**:
   - Kernel & Hardware (`6`): `ooda-archive`, `ooda-boot` (UEFI + TPM2/DICE/Caliptra), `ooda-container` (realms + sandbox/caps), `ooda-drivers` (storage/net/io/modem/virt/accel), `ooda-hardware` (hw/audio/bt/sensors/rgb), `ooda-kernel` (capability microkernel + CXL 3.0).
   - Daemons & Security (`9`): `ooda-authority`, `ooda-bus`, `ooda-connect`, `ooda-data` (data/text/read), `ooda-database`, `ooda-filesystem` (OOVFS + disk/list), `ooda-firewall`, `ooda-health` (ps/top/proc/units), `ooda-inference`.
   - Network, Shell & Desktop (`12`): `ooda-compositor`, `ooda-dashboard`, `ooda-network`, `ooda-panel`, `ooda-portal`, `ooda-screensaver`, `ooda-settings`, `ooda-shell` (shell/date/tty/mux), `ooda-start` (init/logs/cron/power), `ooda-theme`, `ooda-vault`, `ooda-web`.
4. **`@openOODA-apps` (Flagship Native Applications — `19` Packages)**:
   - `ooda-browser`, `ooda-calculator`, `ooda-calendar`, `ooda-camera`, `ooda-chat`, `ooda-clock`, `ooda-code`, `ooda-files`, `ooda-flasher`, `ooda-media`, `ooda-notepad`, `ooda-office`, `ooda-passwords`, `ooda-photos`, `ooda-remote`, `ooda-screenshot`, `ooda-software`, `ooda-studio`, `ooda-terminal`.
5. **`@openOODA-games` (Deterministic Game Engine & Native Games — `9` Packages)**:
   - `ooda-engine`, `ooda-arcade`, `ooda-capella`, `ooda-commander`, `ooda-island`, `ooda-retro`, `ooda-ski`, `ooda-strike`, `ooda-voxel`.
6. **Fleet Census**: `66` product packages (`11` core + `27` system + `19` apps + `9` games) + `4` `@openOODA` umbrella repos = `70` product+platform repos; plus `5` `.github` org-profile repos = `75` total repos across the 5 canonical organizations.
