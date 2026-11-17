# layers.md — The 4-Organization Architecture Map (`ooda layers`)

1. **Umbrella (`@openOODA` — `4` Repos + `.github` Org Profile)**: Constitutional governance & Quick Cards (`cards/`), `openOODA`, `catalog`, `install`, `website`.
2. **`@openOODA-core` (Toolchain, Runtime, Engine & Provenance — `15` Packages)**:
   - Toolchain (`8`): `ooda` (flagship master CLI), `ooda-compiler` (`.oo` compiler), `ooda-runtime` (native runtime `liboodar-core.a`), `ooda-standard` (standard library), `ooda-package` (package solver), `ooda-language` (LSP), `ooda-bridge` (MCP broker), `ooda-verify` (8-hat verifier & debugger).
   - Foundations (`7`): `ooda-binary` (ELF/PE/Mach-O tools), `ooda-build` (deterministic build driver), `ooda-engine` (game & sim runtime), `ooda-format` (wire/codec formats), `ooda-interface` (multi-surface scenes), `ooda-provenance` (TPM2/SEV-SNP/DDC/Merkle provenance), `ooda-sign` (PQC/Ed25519/mTLS signing).
3. **`@openOODA-system` (Kernel, Boot, Daemons, Shell & Utilities — `37` Packages)**:
   - Kernel & Drivers (`10`): `ooda-archive`, `ooda-boot` (UEFI + TPM2/DICE/Caliptra), `ooda-container`, `ooda-data`, `ooda-drivers` (storage/net/io/virt/accel suites), `ooda-files`, `ooda-hardware`, `ooda-health`, `ooda-kernel` (capability microkernel + CXL 3.0), `ooda-machine`.
   - Daemons & Security (`11`): `ooda-authority`, `ooda-bus`, `ooda-connect`, `ooda-database`, `ooda-firewall`, `ooda-inference`, `ooda-modem`, `ooda-network`, `ooda-sandbox`, `ooda-shell`, `ooda-vault`.
   - Shell & Utilities (`16`): `ooda-compositor`, `ooda-disk`, `ooda-edit`, `ooda-filesystem`, `ooda-list`, `ooda-panel`, `ooda-portal`, `ooda-read`, `ooda-screensaver`, `ooda-settings`, `ooda-start`, `ooda-terminal`, `ooda-text`, `ooda-theme`, `ooda-version`, `ooda-web`.
4. **`@openOODA-apps` (Flagship Applications & Games — `18` Packages)**:
   - `ooda-arcade`, `ooda-audio`, `ooda-browser`, `ooda-calculator`, `ooda-camera`, `ooda-canvas`, `ooda-chat`, `ooda-commander`, `ooda-emulator`, `ooda-flasher`, `ooda-office`, `ooda-passwords`, `ooda-player`, `ooda-remote`, `ooda-store`, `ooda-strike`, `ooda-studio`, `ooda-voxel`.
5. **Fleet Census**: `70` product packages (`15` core + `37` system + `18` apps) + `4` `@openOODA` umbrella repos = `74` product+platform repos; plus `4` `.github` org-profile repos = `78` total repos across the 4 canonical organizations.
