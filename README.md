<div align="center">

<pre>
   ____  ____  ___  ____    ___   ___  ____    _
  / __ \/ __ \/ _ \/ __ \  / _ \ / _ \|  _ \  / \
 / /_/ / /_/ /  __/ / / / | | | | | | | | | |/ _ \
/_____/ .___/\___/_/ /_/  | |_| | |_| | |_| / ___ \
      /_/                   \___/ \___/|____/_/   \_\
</pre>

### openOODA — Capability-Secure Computing Stack (`L0`–`L7`)

[openooda.org](https://openooda.org) • [Overview (`llms.txt`)](https://openooda.org/llms.txt) • [Public Binary Hub (`install@hub`)](https://github.com/openOODA/install/releases/tag/hub) • [Package Catalog (`catalog`)](https://github.com/openOODA/catalog)

</div>

---

## Quick Install & Fedora-Style Group Bundles (`oopm`)

Install the core toolchain (`ooda`, `oodac`, `oopm`, `oolsp`, `oomcp`, `liboodar.a`, and `oostd`) from the cryptographically verified public binary hub (`openOODA/install@hub`):

```sh
curl -fsSL https://openooda.org/install.sh | bash
```

Once installed, `oopm` manages individual packages or Fedora-style `@group` bundles across all 8 layers (`93` canonical product packages + `oostd`, verified against signed `SHA256SUMS`):

```sh
oopm group list                  # List @core, @kernel, @os, @tools, @de, @apps, @cloud, @agents, @workstation, @all
oopm install @core               # L0 compiler (oodac), runtime (oodar), stdlib (oostd), CLI (ooda), oopm, oolsp, oomcp
oopm install @tools              # 39 capability-sandboxed L3 Unix, security, UI, and game-engine utilities
oopm install @workstation        # Full desktop stack (@core + @tools + @de + @apps)
oopm install @all                # All 93 canonical packages across L0–L7
```

---

## About openOODA

**openOODA** is an AI-native, capability-secured, fail-closed computing stack built from first principles across eight unified layers (`L0`–`L7`).

In conventional systems, imported libraries, scripts, and autonomous routines inherit the full ambient privileges of the user running the process. **openOODA** eliminates ambient authority across the entire stack: every external effect requires an explicit capability token verified at compile time by `oodac` and enforced at runtime by hardware and kernel isolation boundaries.

At its core, **openOODA** fuses four pillars into a single deterministic computing substrate:

1. **Zero Ambient Authority & Single-Cycle 64-Bit Capability Register (`CapReg64` = `32 + 32 = 64`)**:
   - **Lower 32 bits (`WHAT`)**: Encode all **32 Root Capabilities (`0..31`)** (`13` Hardware + `19` Software/OS, fitting natively into a 32-lane GPU warp mask and a 32-bit seccomp-BPF accumulator):
     `0:NetCap` `1:FsReadCap` `2:FsWriteCap` `3:ProcessCap` `4:EnvCap` `5:TimeCap` `6:RandCap` `7:AllocCap` `8:ThreadCap` `9:GpuCap` `10:FfiCap` `11:MetricsCap` `12:SignCap` `13:BindCap` `14:CompilerReadCap` `15:ArenaCap` `16:FsCap` `17:TcpCap` `18:UdpCap` `19:SysCap` `20:AudioCap` `21:CameraCap` `22:UsbCap` `23:HidCap` `24:WindowCap` `25:FrameCap` `26:MmioCap` `27:DmaCap` `28:IrqCap` `29:PciCap` `30:BlockCap` `31:TpmCap`.
   - **Upper 32 bits (`HOW & WHEN`)**: Pack a **16-bit OODA Epoch** (instant revocation) + **8-bit Rights Mask** (`R/W/X/Delegate/Revoke` + `Bit 64 RIGHT_PRIVACY_REDACT` + `Bit 128 RIGHT_ZERO_TELEMETRY`) + **8-bit Scope Badge** (`badge8`).
2. **CISA KEV Shield, Active Cyber Defense & Post-Quantum Provenance**:
   - **Zero-Trust CWE Elimination (`oostd/sec/kev_guard.oo` & `oodefense`)**: Built-in compile-time and runtime defenses against the **CISA Known Exploited Vulnerabilities (KEV)** catalog (`CWE-22` path traversal admission, `CWE-78` shell-free argv execution, `CWE-190`/`CWE-787` checked integer/slice arithmetic, and `CWE-502` depth-bounded `.oot` parsing).
   - **Active Defense & Containment (`oodefense` & `oosandbox`)**: Bijective key-seeded ELF binary polymorphism (`oodefense mutate`/`unmutate`), kernel eBPF syscall/network IDS (`oodefense ids`), canary tripwires, prompt-injection/LLM tarpits (`llm-tarpit`), and Landlock `O_NOFOLLOW` `link_count==1` + `W^X` + Seccomp-BPF sandboxes (`oosandbox kev-contain`).
   - **Post-Quantum & Hardware Provenance (`oosign` & `ooprovenance`)**: `ML-KEM-768`, `ML-DSA-65`, Ed25519, Stage0 256-byte `hex0` bootstrap seed, Diverse Double-Compilation (`make det`), and TPM2/SEV-SNP attestation.
3. **Full-Stack `L0`–`L7` Hardware + Software Media, Surround Audio & Document Architecture (Zero `ffmpeg`)**:
   - **Hardware Acceleration (`oodar`, `oostd/hw/media.oo`, `oohal`, `oodrv-io`, `oohw`)**: Direct GPU/driver probing for NVIDIA NVENC/NVDEC (`libnvidia-encode.so.1`, `libnvcuvid.so.1`), VAAPI (`libva-drm.so.2`), Vulkan Video, V4L2/MIPI-CSI, DRM/KMS/GOP scanout, DMA-BUF zero-copy rings, and ALSA/HDA multi-channel PCM under `GpuCap`, `FrameCap`, `DmaCap`, and `AudioCap`.
   - **Surround/Spatial Audio, Video, Images & Subtitles (`oomedia`, `oodaw`, `oocanvas`)**: Native zero-FFmpeg codecs and transcoding across **Surround/Spatial Audio** (`1.0`, `2.0`, `4.0`, `5.1`, `7.1`, `7.1.4` 12-channel Dolby Atmos bed, Ambisonics, WAV/RF64/`WAVE_FORMAT_EXTENSIBLE`, FLAC, QOA, DTS/DTS:X, AC-3/E-AC-3/TrueHD, IAMF, Opus, MP3, AAC + ITU-R BS.775 downmix/upmix & HRTF binaural), **Video & HDR** (MP4/MOV, MKV/WebM, MPEG-TS, AVI, Y4M, `.oov` with PQC frame seals, AV1 OBU, H.264/HEVC NAL, HDR10 `SMPTE ST 2086`, Dolby Vision), **Images** (`.qoi`, `.png` with `iCCP`/`eXIf`/`cICP` HDR chunks, `.ppm`, `.bmp`, `.svg`, `.tga`, `.ico`, `.webp`, `.jpeg`, `.tiff`/`.dng` RAW), **Subtitles** (`.srt`, `.vtt`, `.ass`), and **MIDI/DAW Synthesis** (`oodaw` `.mid` `MThd`/`MTrk`, `.sf2`/`.sfz`, MusicXML).
   - **Office & Document Suite (`oooffice`)**: Native ZIP/Deflate/XML engine across Word (`.docx`/`.odt`/`.rtf`/`.md`/`.html`), PowerPoint (`oodeck` `.pptx`/`.odp`/`.svg`), Excel (`oosheet` `.xlsx`/`.ods`/`.csv`/`.parquet` + formulas), and PDF/eBook (`oopdf`/`oonotes` `%PDF-1.7` + `.epub`).
4. **Power-of-2 Shape Ladder (`1/2/4/8/16/32/64/128/256`) & 8-Hat Adversarial Consensus (`oohat` + `oofalsify`)**:
   - Every `.oo` page across all 93 repositories obeys the strict Power-of-2 structural laws (`1` link count / `1` stmt per line, `2` test axes, `<= 4` nesting depth, `<= 8` files/dir & `<= 8` fns/file & `<= 8` params/fn, `>= 16` lines/file, `32` capabilities & `<= 32` chars/identifier, `<= 64` code lines/fn, `<= 128` chars/line, `<= 256` lines/file) and must pass deterministic double-compilation (`make det`) and the 8-Hat consensus gate (`oohat cycle` `quorum_mask=255`: White, Gray, Black, Red, Blue, Purple, Green, Yellow).

---

## The Unified 8-Layer Architecture (`L0`–`L7` — `93` Canonical Packages)

| Layer | Organization | Repos | Canonical Packages & Architectural Focus |
| :--- | :--- | :---: | :--- |
| **Root** | [`@openOODA`](https://github.com/openOODA) | `6` | Governance & Quick Cards (`openOODA`), Package Index (`catalog`), Public Binary Hub (`install`), Docs (`website`), Telemetry (`status`), Benchmarks (`bench`) |
| **`L0`** | [`@openOODA-core`](https://github.com/openOODA-core) | `7` | `ooda` (master CLI), `oodac` (`.oo` compiler), `oodar` (`liboodar.a` C/ASM/GPU/audio runtime), `oostd` (standard library + `sec/kev_guard.oo` + `hw/media.oo`), `oopm` (package manager), `oolsp` (LSP), `oomcp` (MCP broker) |
| **`L1`** | [`@openOODA-kernel`](https://github.com/openOODA-kernel) | `6` | `ooboot` (UEFI), `oohal` (x86_64/ARM64/RISC-V + `hal-media` DRM/KMS/HDR10), `ookernel` (sched/mm/ipc/IOMMU DMA guard), `oodrv-storage` (NVMe/VirtIO), `oodrv-io` (GOP/PCIe/USB/HID/MIPI-CSI/ALSA 8ch/DMA-BUF `media-io`), `oodrv-virt` |
| **`L2`** | [`@openOODA-OS`](https://github.com/openOODA-OS) | `9` | `ooinit` (PID 1), `oovfs` (CoW/LUKS), `oonetd` (WPA3/WireGuard/BGP), `oosysbus` (devd, sensors, IPP print, PipeWire-style `media-graph`), `ooauthd`, `oohealthd`, `oocontainer`, `oollama` (local LLM + `ingest-media`), `oomodemd` (5G/LTE/eSIM) |
| **`L3`** | [`@openOODA-tools`](https://github.com/openOODA-tools) | `39` | **Security (`7`)**: `oodefense` (`kev-sync`/`kev-audit`/`kev-shield`/`mutate`), `oosandbox` (`kev-contain`), `ooprovenance`, `ooredact`, `oosign`, `oofirewall`, `oovault`. **Core/UI/Engine (`32`)**: `oofs`, `ooperm`, `oopath`, `oomount`, `ools`, `oocat`, `oosort`, `ootext`, `oogrep`, `oodiff`, `oojq`, `oocodec`, `oosh`, `ooproc`, `oohw` (`media`/`audio`), `oopower`, `oocron`, `oonet`, `oocurl`, `oossh`, `ootty`, `ootheme` (25 themes / 34 tokens), `oorgb`, `ooarchive`, `ooawk`, `oofind`, `oofzf`, `oohash`, `ooless`, `oosed`, `ooui` (`export-frame`), `ooengine` (`asset-pack`) |
| **`L4`** | [`@openOODA-DE`](https://github.com/openOODA-DE) | `8` | `oocomp` (Wayland compositor + DMA-BUF scanout + `.oov` screen capture), `oopanel` (bar/launcher + `osk`), `ooportal` (clipboard TTL auto-burn, `screencast`/`audio-capture` leases, a11y, USB guard), `ooterm`, `oofiles`, `oosettings`, `oobazaar`, `ooagent-hud` |
| **`L5`** | [`@openOODA-apps`](https://github.com/openOODA-apps) | `16` | `oomedia` (`hw-probe`/`probe`/`transcode` surround audio, HDR video, images, subtitles), `oodaw` (MIDI/SF2/MusicXML/VBAP surround DAW), `oocanvas` (`export`/`probe` QOI/PNG/BMP/PPM/SVG/RAW), `oooffice` (`docs`/`sheet`/`deck`/`notes`/`pdf`), `oobrowser`, `oostudio`, `ooflash` (`+pack-iso`), `oochat`, `oopass`, `ookvm`, `oocamera`, `ooemu`, `ooarcade`, `oocommand`, `oostrike`, `oovoxel` |
| **`L6`** | [`@openOODA-cloud`](https://github.com/openOODA-cloud) | `8` | `oostore` (content-addressed store + `media-ingest`), `oomesh` (PQC mesh + `media-relay`), `oodb` (`sql`/`btree`/`wal`/`kv`), `oodeploy` (`pxe`/`bmc`/`vm-fleet`), `oogateway`, `ooidentity`, `ootelemetry`, `oobilling` |
| **`L7`** | [`@openOODA-agents`](https://github.com/openOODA-agents) | `10` | `oohat` (8-Hat consensus + CISA KEV scanner), `oofalsify` (`kev-battery` + `media-battery` fuzzing), `ooloop`, `ooswarm`, `oobench`, `ooquota`, `ooconsensus`, `oocode`, `oomemory`, `oogovern` |

---

## The 8 Built-In Quick Cards (`ooda <card>`)

Every developer and autonomous agent has instant offline access to the 8 canonical governance cards via the `ooda` CLI or directly in this repository:

| Command | Document | Summary |
| :--- | :--- | :--- |
| `ooda ooda` | [`ooda.md`](ooda.md) | How to rapidly build, test, and adapt openOODA software (`<= 32` pages, 3-command loop) |
| `ooda layers` | [`layers.md`](layers.md) | Complete 8-Layer Architecture Map (`L0`–`L7`) and 93-package census |
| `ooda spec` | [`spec.md`](spec.md) | `.oo` language syntax, algebraic data types, capability signatures, and `oostd` builtins |
| `ooda rules` | [`rules.md`](rules.md) | Canonical Power-of-2 Shape Ladder (`1/2/4/8/16/32/64/128/256`) and CLI/Subcommand laws |
| `ooda ui` | [`ui.md`](ui.md) | `ootheme` (25 presets, 34 semantic tokens), `ooui` (`tui`/`gui`/`wui`/`vui`), `ooengine`, and `oorgb` |
| `ooda security` | [`security.md`](security.md) | `CapReg64` (`0..31` capabilities), `oosandbox`, `oosign` (PQC/ZK), `ooprovenance`, and `oovault` |
| `ooda privacy` | [`privacy.md`](privacy.md) | Kernel privacy attenuation, `SECRET:` IFC taint, `ooredact`, camera/mic LED gates, clipboard TTL burn |
| `ooda defense` | [`defense.md`](defense.md) | CISA KEV Shield, `oodefense` (eBPF IDS, canary, honeypot, ELF `mutate`), `oofirewall`, IOMMU DMA guards |
