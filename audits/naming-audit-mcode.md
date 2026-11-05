# Naming & Single-Responsibility Audit — Independent Pass (mcode / MiniMax M3.1-Flash)

**Auditor:** MiniMax Code (`mcode`, MiniMax-M3.1-Flash) — Stage 1 Code Reviewer, openOODA `spotlight` (`w3:p1`)
**Date:** 2026-11-05
**Scope:** all 9 openOODA organizations — `/Projects/openOODA`, `/Projects/openOODA-core`, `/Projects/openOODA-kernel`, `/Projects/openOODA-OS`, `/Projects/openOODA-tools`, `/Projects/openOODA-DE`, `/Projects/openOODA-apps`, `/Projects/openOODA-cloud`, `/Projects/openOODA-agents`
**Method:** read-only inspection. Directory names, `README.md`, `Makefile` `BIN`/`PERSONAS`/`SRC`/`VER`, `anchor.oo`, `ooda.pkg`, `VERSION`, persona dispatch tables, and `.oo` source headers were read directly.
**Build constraint honoured:** no compiler was invoked. No `make`, no `oodac`, no `cc`/`clang`/`gcc`/`rustc`, no build or test target, no binary executed, no git state mutated. Only file reads, path/name search, and read-only shell (`wc`, `diff`, `awk`, `sed`, `find -type l`, `stat`).

> **Snapshot caveat.** The `openOODA-apps` tree changed *during* this audit. `openOODA-apps/ooflash/` was created and populated between 03:55 and 03:58 HST on 2026-11-05, and the flasher half was deleted from `openOODA-apps/oomedia/` at ~03:59. Both the pre-split and post-split states were captured and are reported separately where they differ. All other claims describe the tree as found.

---

## 0. Executive summary

The project does **not** have a naming problem so much as a **name-ownership** problem. The vocabulary is mostly disciplined (`oo` prefix, one repo per binary, `PERSONAS` tables, RFC 0012 consolidation targets). What is broken is the **binding between a name and exactly one owner**.

| # | Finding | Severity |
|---|---|---|
| **F1** | **82 distinct name tokens are simultaneously a standalone repo/binary and a persona of another binary.** 57 are served by **two or more different hosts**; 49 are repo-vs-persona collisions inside one org; 5 cross an org boundary. | **Critical** |
| **F2** | **20 of those 82 are published in the signed public package catalog** (`catalog/index`), so the ambiguity is user-visible on the install surface, not just internal. | **Critical** |
| **F3** | **Two mutually-recursive persona claims exist**: `oohash` claims `oob3sum` and `oob3sum` claims `oohash` (`oohash/ipc/dispatch_persona.oo:33`, `oob3sum/ipc/persona_dispatch.oo:32`). Neither can be archived until the cycle is broken. | **Critical** |
| **F4** | **Two incompatible multi-call dispatch contracts are simultaneously in force.** RFC 0012 §2.2 mandates explicit-subcommand dispatch and Rule 1.25 bans symlinks, but `openOODA-OS/ooimage` selects personas from `sys_argv0` basename (`ooimage/main.oo:62`), and `website/llms.txt:35` still advertises "`sys_argv0` symlink dispatch". | **High** |
| **F5** | **`openOODA-core/std` carries 112 `.oo` files of Layer-1 kernel/driver code**, duplicating `openOODA-kernel` responsibilities including two verbatim-identical capability-space pages. A "standard library" repo is doing kernel work. | **High** |
| **F6** | **`openOODA-OS/ooimage` claims three responsibilities and implements one.** Its README promises Level-1 ISO and Level-2 UEFI/Firecracker image building; zero source implements either. The name `ooimage` is a pure overclaim. | **High** |
| **F7** | **All 17 `openOODA-kernel` repos are one template**, not 17 responsibilities: the same 15 cross-cutting pages in every repo, differing only by a repo-name token. | **High** |
| **F8** | **Absorption is declared but never enacted.** Across the fleet, absorbed repos still build and publish their own standalone binary, so the "one canonical binary per domain" rule is not enforced anywhere in the tree. | **High** |
| **F9** | **`openOODA-apps/oomedia` was the canonical scope-pollution example** (media player + USB flasher). It has since been split into `ooflash` — the split is *correct in direction* but `ooflash` introduces a C-binary fallback (`dd`, `truncate`, `sha256sum`, `sync`) that contradicts Rule 1.25 and `roadmap.oot:90`. | **High** |
| **F10** | **The consolidation spec itself has gaps.** RFC 0012 §2.3 names canonical targets that do not exist as repos, and leaves 30+ existing repos with no planned home. | **Medium** |
| **F11** | **Documentation drift is systemic**: stale page counts, assertion counts, versions, and — in 9 repos — README lines advertising `ooagent-*` symlink applets that were deliberately deleted. | **Medium** |
| **F12** | **Hardcoded hostnames/Tailscale IPs survive inside `.oo` sources** in `openOODA/openOODA/buildbox/` and as live function identifiers in `openOODA-OS/ooaid`. | **Medium** |

**Positive findings (also first-principles):** the **Zero Symlinks and Hardlinks Law is fully complied with** — 0 symlinks and 0 hardlinks across all 9 org trees. The **Page Rule is honoured** — exactly 1 `.oo` file exceeds 256 lines fleet-wide and it is a deliberate negative-test fixture (`openOODA-core/oodac/tests/fixtures/boundary_257_lines.oo`). The **catalog index has zero drift** against the 256 on-disk packages. The `oo` namespace prefix is applied consistently with a small, explicable exception set.

---

## 1. The governing contract (what the audit measures against)

The audit is scored against the project's own written standards, not an external opinion.

| Contract | Location | Substance |
|---|---|---|
| **Rule 1.25 — Zero Symlinks and Hardlinks Law** | `openOODA/openOODA/rules.oot:244-248` | Zero symlinks/hardlinks anywhere. Every `bin/`/`dist/` executable is a real standalone ELF (`! -L`, link count 1). Consolidated tools expose personas via **explicit CLI subcommands or flags**, never symlink aliases. Code sharing via `import "std/..."`, never filesystem links. |
| **Executive Zero-Symlinks Directive** | `openOODA/ZERO_SYMLINKS_DIRECTIVE.md:10-16` | Codifies Rule 1.25 and names the canonical consolidated tools: `oohash`, `oobase64`/`oocodec`, `ooarchive`, `oosort`/`ootext`, `ooherdr`, `oocoder`, `oocomp`, `oopanel`, `oostore`, `oooda-engine`, `ooconsensus`. |
| **RFC 0012 — Unix Less-Is-More Consolidation** | `openOODA/openOODA/rfcs/0012-unix-less-is-more-consolidation.oot` | §2.2 defines persona tables and the zero-link rule. §2.3 sets the consolidation target: **377 → 129 canonical repos**, with a per-org target list. |
| **Roadmap** | `openOODA/openOODA/roadmap.oot:81,90` | `ooflash` listed as a backlog item ("separated from `oomedia` media player"). `2026-11: Deprecate non-sandboxed subprocess execution shims across all tooling.` |

---

## 2. Defect class (a) — Naming mismatch / misleading names

### 2.1 `openOODA-core/std` — a "standard library" that carries the kernel (F5)

`openOODA-core/std/anchor.oo:19` declares the `hw/` domain to hold `bare_metal, drivers_hal, unikernel`. `openOODA-core/std/hw/anchor.oo:3` simultaneously declares the *same* directory to be "a theoretical-foundation library … No public API code -- the directory is documentation and verification rules." Both cannot hold: `std/hw/` contains **112 `.oo` files with real implementations** across 9 subdirectories.

Direct duplication of named sibling repos in `openOODA-kernel`:

| `std` file (Academy logline) | `openOODA-kernel` counterpart |
|---|---|
| `std/hw/unikernel/firecracker.oo:3` — "Manages Firecracker MicroVMs via REST API socket, vsock streams, and sub-millisecond snapshot restores." | `ookernel-unikernel/README.md:3` — "Single-address-space Firecracker and QEMU microVM target" |
| `std/hw/unikernel/virtio.oo:3` — "Implements VirtIO MMIO transport, Split Virtqueue descriptors, and VirtIO-Net / VirtIO-Blk / VirtIO-Console drivers." | `oodrv-virtio/README.md:3` — "Ring-3 VirtIO block, net, gpu, and input split/packed virtqueue driver suite" |
| `std/hw/drivers_hal/lapic_driver.oo:1` — "x86_64 Local APIC and IO-APIC Hardware Driver" | `ookernel-hal-x86/README.md:3` — "x86_64 GDT/IDT, SYSCALL/SYSRET, LAPIC/IOAPIC, and SMP startup HAL" |
| `std/hw/drivers_hal/gicv3_driver.oo:1` — "ARM GICv3 (Generic Interrupt Controller v3) Driver" | `ookernel-hal-arm64/README.md:3` — "ARM64 EL1 exception vectors, GICv3 interrupt controller, and PSCI SMP HAL" |
| `std/hw/drivers_hal/uefi_framebuffer.oo:1` — "UEFI 64-Bit Linear Framebuffer Graphics Driver" | `oodrv-display-gop/README.md:3` — "Ring-3 UEFI GOP, VirtIO-GPU, and DRM scanout driver" |
| `std/hw/bare_metal/cnode_tree.oo` — "Capability Derivation Tree (CDT) … cascading subtree revocation" | `ookernel-ob/ob/cnode_tree.oo` — **same logline verbatim** |
| `std/hw/bare_metal/cspace_table.oo` — "CSpace root table directory storing and retrieving full 256-bit capability descriptors" | `ookernel-ob/ob/cspace_table.oo` — **same logline verbatim** |

`std/ipc/wire.oo:3` implements an IPC wire codec — the same duty as `ookernel-ipc/README.md:3` — yet `std/ipc/` has **no `anchor.oo`** and is not in the declared 8-domain public surface (`std/anchor.oo:36-46`).

**This is the closest structural analogue to the `oomedia` defect class anywhere in the fleet**: a repo whose name states one domain, carrying a second, separately-named domain.

**Verdict: SPLIT** → `std` (the 8 declared domains) + `std-hw` (the 112 driver/unikernel files, Layer 1).

### 2.2 `openOODA-OS/ooimage` — claims three responsibilities, implements one (F6)

`openOODA-OS/ooimage/README.md:76` claims:

> "Deterministic OS & 3-tier OCI container image builder … + Level 1 Linux+OODA ISO and Level 2 `ookernel` UEFI/Firecracker images."

| # | Claimed responsibility | Declared at | Implemented? |
|---|---|---|---|
| 1 | 3-tier OCI container image builder | `README.md:14,76` | **Yes** — `ooimage/containers/ooda_core.oo:18-33` returns a Containerfile string; `ooimage/containers/ooda_inference.oo:34-42` returns a Quadlet unit string |
| 2 | Level 1 Linux+OODA ISO builder | `README.md:76` | **No** — 0 source hits for `iso|uefi|firecracker|\.img|squashfs|bootloader|grub` |
| 3 | Level 2 `ookernel` UEFI/Firecracker image builder | `README.md:76` | **No** — same 0 hits |

Two further overclaims in the same file:
- **"Quadlet *manager*"`** — there is no lifecycle management. The only Quadlet interaction is a string lookup (`ooimage/containers/anchor.oo:18`). No install/start/stop/enable path exists.
- **"Image layer table"** — the table is the generic `core/{types,store,machine}.oo` boilerplate shared with every OS repo, differentiated only by an IPC magic number.

**Bonus defect in the same repo (port mismatch):** `ooimage/containers/ooda_inference.oo:24` sets `ENV OODA_AID_PORT="11434"` and `:28` declares `EXPOSE 11434`, but `:39` emits `Environment=OODA_AID_PORT=11435` in the Quadlet. `ooaid/net/config.oo:54` uses `11434`. The Quadlet would start the container on the wrong port.

**Verdict: SPLIT + RENAME.** Ship `oocontainer` (the generator that actually exists) now; open `ooiso` and `ookernelimg` later to make the ISO/UEFI claims true. `ooflash` correctly sidesteps the name axis — it names the *action* (flash), not the *artifact* (image), so it does not collide with `ooimage` (image **builder**).

### 2.3 `openOODA-OS/oorealm` — "realm" spans three unrelated substrates

`openOODA-OS/oorealm/README.md:5` — "Flathub OSTree realms, the 3 canonical rootless OCI server containers (`ooda-core`, `ooda-buildbox`, `ooda-inference`), and Steam/Proton + WinRealm IOMMU gaming realms." `oorealm/core/engine.oo:8` — "validate tier-specific capability requirements (Tier 1 Flathub, Tier 2 OCI, Tier 3 Proton/WinRealm IOMMU)".

Three domains (desktop app distribution / server containers / gaming anti-cheat virtualization). `oorealm/cli.oo:66` additionally hardcodes `"containers":["ooda-core","ooda-buildbox","ooda-inference"]` — **the same canonical tier list `ooimage/containers/anchor.oo:15-17` owns**. Two repos independently assert the canonical container composition: a single-source-of-truth defect that will silently drift.

**Verdict: SPLIT** → `ooflathub`, `oocontainerrealm`, `oowinrealm`; shared realm engine becomes a library.

### 2.4 `openOODA-DE/oofiles` — named for a file manager, actually a 6-domain shell host

`openOODA-DE/oofiles/README.md:3` — "Dual-pane spatial and Miller-column file manager". But `oofiles/README.md:64-69` declares six absorbed domains:

```
| `oofiles`    | — (canonical)  | `list`  |
| `ooview`     | `ooview` repo  | `open`  |
| `ooedit`     | `ooedit` repo  | `open`  |
| `ooclip`     | `ooclip` repo  | `copy`  |
| `ooshot`     | `ooshot` repo  | `capture`|
| `ootaskmgr`  | `ootaskmgr` repo | `ps`  |
```

File manager + document viewer + code editor + clipboard broker + screenshot capture + process inspector. **Verdict: RENAME → `ooshell`** (see §2.5 — only one DE repo may claim `ooshell`).

### 2.5 `openOODA-DE/oopanel` — named for a panel, actually the DE shell host

`openOODA-DE/oopanel/README.md:3` — "Top status panel, workspace pill strip, system tray, clock, and active capability indicator bar". It additionally absorbs `ooshelf`, `ootoast`, `oocockpit` (an entire OODA command deck) and `oolaunch` (`oopanel/README.md:63-67`). A panel that dispatches to a command deck is a shell.

`openOODA-DE/ooportal` vs `oopanel` differ by two characters in the middle and are both DE shell-surface hosts — **high confusion risk**.

**Verdict:** rename one of `oofiles`/`oopanel` → **`ooshell`**; rename `ooportal` → **`oogrant`** (it is the capability-grant/privacy surface, per `ooportal/core/persona/dispatch.oo:17`).

### 2.6 `openOODA-DE/oobazaar` — a "bazaar" hosting four install backends

`openOODA-DE/oobazaar/README.md:5-9` browses/installs: native `opm` packages, Tier-1 Flathub/Bazaar Flatpaks, Tier-2 Podman-style rootless containers, Tier-3 Steam/Proton/WinRealm games. Four provisioning backends in one store binary. **Verdict: SPLIT** per backend, or keep one store with thin backend adapters.

### 2.7 `openOODA-apps/oovm-ui` — declares a KVM VM manager, implements a `/proc` monitor

`openOODA-apps/oovm-ui/README.md:3` — "**Virtual machine manager UI over KVM cells**". The only domain page in the repo is `oovm-ui/monitor.oo` (42 lines), which reads `/proc/meminfo` and `/proc/loadavg` and returns one string (`mem_total=… mem_avail=… cached=… load1=… load5=… load15=… tasks=…`). Negative evidence: no `qemu`, `kvm`, `libvirt`, `virt`, `cell`, `domain`, `vcpu`, or `snapshot` string anywhere in the repo.

"VM" is ambiguous *and* misleading — it is not "vector markup" nor "volume manager"; the name asserts a virtual-machine domain the code does not implement. The real behaviour is a host resource monitor.

**Verdict: RENAME → `oohostmon`.** (`oomonitor` is rejected — collides with `openOODA-tools/oomonitor`.)

### 2.8 `openOODA-core` — repo name ≠ shipped binary name

| repo | Makefile `BIN` | CI artifact | Disposition |
|---|---|---|---|
| `lsp` | — | `dist/ooda-lsp-linux-x86_64` (`lsp/.github/workflows/ci.yml:150`) | **RENAME → `ooda-lsp`** |
| `mcp` | `dist/mcp` (`mcp/Makefile:26`) | `dist/ooda-mcp-linux-x86_64` (`mcp/.github/workflows/ci.yml:141`) | **RENAME → `ooda-mcp`** (two names for one binary inside one repo) |

Consumers carry both names: `cli/README.md:28` says "ooda-mcp / ooda-lsp / opm" while `cli/persona/router_run.oo:21-22` spawns bare `"lsp"` and `"mcp"`; `cli/build/spawn.oo:35-36` papers over it with an explicit legacy-alias fallback commented "Old on-disk names only." `openOODA-core/tui/mcp_client.oo:79` carries a **five-step sequential legacy-name fallback** for one binary.

### 2.9 `openOODA-core/oodar` — three-way metadata contradiction

| Claim | Value | Source |
|---|---|---|
| Library name | `liboodar-core.a` | `oodar/README.md:21` |
| Library name | `liboodar.a` | `oodar/scripts/Makefile:3`, `oodar/anchor.oo:5`, CI `oodar/.github/workflows/ci.yml:55` |
| Layer | `Layer 0` | `oodar/README.md:21` |
| Layer | `Layer 1 Host Substrate` | `oodar/anchor.oo:1` |
| `.c` file count | `111 .c files` | `oodar/anchor.oo:3,5` — actual 130 non-`qa` files, 124 `#include`s in `oodar.c` |

### 2.10 `openOODA-kernel/oodrv-net` — name promises NICs, code delivers a generic ring

`oodrv-net/README.md:3` — "**Ring-3 e1000e, RTL8125, and VirtIO-net packet ring driver**". `e1000e`/`RTL8125` appear **only** in the persona description string (`persona/self_set.oo:60-62`) and in zero implementation files. The only domain artifact is `core/drv_net_parse.oo:3` — "7-word wire codec for the ethernet frame header". No descriptor ring, no MMIO, no PHY.

**Verdict: RENAME → `oodrv-io`** (its own union persona is already `oodrv-io`, `persona/self_set.oo:77`).

### 2.11 `openOODA-kernel/ookernel-hal-x86` — an x86-named host for three architectures

`ookernel-hal-x86/persona/anchor.oo:123` — "Canonical unified HAL surface for x86_64, ARM64, and RISC-V". The directory and binary say x86 only, while `ookernel-hal-arm64` and `ookernel-hal-riscv` are absorbed by it. **Verdict: RENAME → `oohal`.**

### 2.12 `openOODA-agents/oooda-engine` — a stutter, plus an alias stolen by another host

`oooda-engine` reads as `oo` + `ooda-engine`, i.e. a stutter against the project's own `oo` prefix convention. Worse, the alias `engine` is claimed by two hosts:

- `openOODA-agents/oooda-engine/persona/meta.oo:24` — `if id == "oooda-engine" { return "engine"; }`
- `openOODA-agents/ooherdr/persona/meta.oo:34` — `if name == "engine" { return "ooherdr"; }`

`--persona engine` resolves to a different binary depending on which host is invoked.

**Verdict: RENAME → `ooooda`** and drop the `engine` alias from one of the two hosts.

### 2.13 `openOODA-agents/oocoder` — a vendor name used as a top-level persona id

`openOODA-agents/oocoder/persona/meta.oo:19,36,55` registers persona id `oodeepseek`, alias `deepseek`, described as "DeepSeek model coding persona: prompts and review backed by deepseek-coder endpoint". A single vendor's model binding inside a generic code-analysis agent, with a hardcoded port `(:11435)` at `oocoder/ooda.pkg:8`. **Verdict: RENAME persona `oodeepseek` → `oocoder-deepseek`.**

### 2.14 Redundant org suffixes inside the cloud org

`oodns-cloud`, `oosched-cloud`, `ooregistry-cloud` all restate the org name that already appears in the repo path (`openOODA-cloud/…`). The majority style in the same org — `oocdn`, `oobilling`, `oogateway`, `oomesh`, `oorelay`, `oostore`, `ootelemetry` — carries no suffix. The suffix is also load-bearing: `openOODA-tools/oodns` already exists, so `oodns-cloud` is the only thing preventing a stem collision with L3 tooling.

**Verdict: RENAME** → `oodns`, `oosched`, `ooregistry`.

### 2.15 `openOODA-tools/oote` — collides with the reserved name `ootext`

`ZERO_SYMLINKS_DIRECTIVE.md:14` reserves `oosort`/`ootext` as the canonical text-processing host. `openOODA-tools/oote/README.md:1` is "**openOODA Theming Engine**" — a colour/theme engine, not text processing. The reserved name `ootext` therefore has no home, while the near-identical `oote` is occupied by an unrelated tool. **Verdict:** create the canonical `ootext` host, and rename the theme engine to `ootheme` (or `oopalette`) to free the axis.

### 2.16 `openOODA-tools/oomd5` — a repo whose own title says "LEGACY"

`openOODA-tools/oomd5/README.md:1` — "**oomd5: Native MD5 LEGACY**". It is simultaneously a standalone repo, a published catalog package, and a persona of *both* `oob3sum` and `oohash`. MD5 is a legacy digest with no correctness role. **Verdict: ARCHIVE** (absorbed into the digest host); the `md5sum`/`md5` **persona tokens** may remain for CLI compatibility per RFC 0012 §2.2.

### 2.17 `openOODA-OS/ooimage` vs `openOODA-apps/oomedia` vs `openOODA-apps/ooflash` — the "image" name axis

Three repos use image language for three different things: `ooimage` **builds** container/ISO images; `oomedia` **played** media and **wrote** images to devices; `ooflash` **writes** images to devices. A user typing `ooimage` to flash a USB stick would be wrong by two layers. `ooflash` is the correct verb-name and resolves this; `ooimage` should be narrowed to `oocontainer` (§2.2).

### 2.18 Names that are clean (explicitly checked, no finding)

- `openOODA-apps/oopass` (credential vault, `oopass/audit.oo:3`) vs `openOODA-DE/oodeck` (slide deck, `oodeck/slides.oo:3`) — different domains, no collision.
- `openOODA-apps/oodaw` (audio workstation, `oodaw/session.oo:3`) vs `openOODA-DE/ooedit` (code editor) — different domains, different orgs.
- `openOODA-cloud/oostore` (object/bucket storage, `oostore/core/bucket.oo:3`) vs `openOODA-cloud/oostore-cas` (content-addressed blob store + PQC provenance, `oostore-cas/core/cas.oo:3`) — genuinely distinct domains; the near-collision is resolved by archiving `oostore-cas` into `oostore` (§4).
- `openOODA-cloud/oobilling` (commercial metering, `oobilling/core/meter.oo:3`) vs `openOODA-agents/ooquota` (agent token burn-rate, `ooquota/core/pace.oo:3`) vs `openOODA-cloud/ootelemetry` (metrics) — three different currencies; no collision.
- `openOODA-cloud/ooconsent` and `openOODA-agents/ooconsensus` are **different names** — no cross-org collision (the hypothesis was tested and rejected).

---

## 3. Defect class (b) — Scope pollution / Unix single-responsibility

### 3.1 `openOODA-apps/oomedia` → `ooflash` — the reference case, now resolved (F9)

**Pre-split state (`oomedia/README.md:3`, captured 03:55 HST):**
> "**Media player with playlist ring + Fedora-style bootable image flasher**"

Measured dominance:

| Cluster | Pages | `.oo` lines | Functions |
|---|---|---|---|
| Flasher domain — `flash/{devlock,digest,catalog,imagew,restore,ui}.oo` | 6 | 332 | 24 |
| Flasher CLI — `personas/oomedia/{verbs,ops}.oo` | 2 | 141 | 11 |
| Flasher tests — `tests/flash/test_flash.oo` | 1 | 140 | 8 |
| **Flasher subtotal** | **9** | **613** | **43** |
| Media-player domain — `probe.oo` + `core/state.oo` + `ui/view.oo` | 3 | 142 | 2 |
| Generic harness (`core/*`, `ipc/*`, `sec/*`, `personas/{multicall,harness}`, `tests/test_*`) | 27 | 1 645 | — |

**The flasher dominated by 4.3:1 on domain lines and ≈21:1 on domain-specific functions.** The "media player" was 23 lines of extension-sniffing plus a generic ring shared structurally with every sibling repo.

Corroborating smell: `oomedia/ooda.pkg:9` declared `caps=FrameCap,FsReadCap,FsWriteCap,ProcessCap,TcpCap` — the `TcpCap` existed **only** for the flasher's catalog fetch (`oomedia/flash/catalog.oo:35`). A media player has no business holding a network capability.

**Post-split state (verified 04:0x HST):**
- `openOODA-apps/ooflash/` exists with `Makefile` (`BIN := bin/ooflash`, `PERSONAS := ooflash`, `VER := 0.1.0`), `README.md`, `VERSION`, `ooda.pkg`, `.github/workflows/ci.yml`.
- `oomedia/flash/`, `oomedia/personas/oomedia/{verbs,ops}.oo`, `oomedia/tests/flash/test_flash.oo` are deleted.
- `oomedia/Makefile` `SRC` no longer lists any flash page — the dangling `SRC` prerequisites and the dangling `import "tests/flash/test_flash.oo";` that existed transiently during the split have both been resolved.
- `ooflash` is a **strict superset** of the old flasher: it adds `flash/rawio.oo` (97 lines, new — bare-metal raw block I/O) and `tests/test_raw.oo` (78 lines, new).

**Verdict: SPLIT — correct, and the canonical name `ooflash` is right** (verb-named, not artifact-named; no collision with `ooimage`).

**But `ooflash` introduces a new standards defect.** `openOODA-apps/ooflash/flash/rawio.oo` shells out to **GNU coreutils binaries**:

| `ooflash/flash/rawio.oo` | Exec |
|---|---|
| `:21` | `sys_exec(sys, "sha256sum", path)` |
| `:35,37` | `sys_exec(sys, "dd", "if=" + img, "of=" + dpath, "bs=1M", "oflag=direct", "conv=fsync", "status=none")` |
| `:43` | `sys_exec(sys, "sync")` |
| `:50,52` | `sys_exec(sys, "dd", "if=/dev/zero", …)` |
| `:59,61` | `sys_exec(sys, "dd", "if=" + dpath, "of=" + tmp, …)` |
| `:73` | `sys_exec(sys, "truncate", "-s", …, tmp)` |

`ooflash/flash/rawio.oo:3` describes itself as a "**dd-delegated** raw device pipeline" — delegation to a C binary. `ooflash/flash/digest.oo:8,44-47` adds a size-based "digest road pick": in-process `crypto_sha256_internal` up to 512 MiB, `sha256sum` above.

This contradicts:
- **Rule 1.25 / the Zero-Legacy-Wrapper standard** — the project standard requires pure native `.oo` compiled via `oodac` to ELF64/wasm32, with zero C/Rust/Python fallbacks.
- **`roadmap.oot:90`** — "2026-11: Deprecate non-sandboxed subprocess execution shims across all tooling." New code introduced on 2026-11-05 adds exactly such a shim, in the same month the roadmap item is scheduled to land.
- **The `oohash`/`oob3sum` persona surface** — `sha256sum` is already a persona token of the digest host. `ooflash` therefore introduces a *third* owner of the `sha256sum` token (see §4.2).

`ooflash` also ships `ooflash/lint-oo-size`, a `/bin/sh` script, whereas the sibling repos implement the same Page-Rule linter inline in their Makefile and ban `.sh` outside `install.sh`/`uninstall.sh`.

**Verdict on `ooflash`: KEEP the repo and the name; REPLACE the `dd`/`truncate`/`sha256sum`/`sync` execs with native `.oo` implementations** (O_DIRECT + `fsync` are reachable through the existing `FsWriteCap`/`ProcessCap` surface; `sha256sum` is already implemented natively by `oohash`/`oob3sum` and by `openOODA-tools/oosha256`).

### 3.2 `openOODA-core/std` — stdlib carrying a kernel stack (F5)
See §2.1. 112 `.oo` files of driver code in a library repo, with two verbatim-identical capability-space pages against `openOODA-kernel`.

### 3.3 `openOODA-kernel` — 17 repos, one implementation (F7)

Every kernel repo carries the same 15 cross-cutting pages: `cap_reg64.oo`, `wire.oo`, `warrant.oo`, `attest.oo`, `chain.oo`, `quorum/*`, `speculate/*`, `delegate/*`, `revoke/*`, `proof/*`, `heal/*`, plus a `core/{engine,cap,ring,table}` quartet. Verified by diff: `oodrv-net/cap_reg64.oo` and `oodrv-pci/cap_reg64.oo` differ **only** in the repo-name token (lines 1 and 3).

The per-repo domain delta is 4 files — `core/{domain}_cap.oo`, `core/{domain}_ring.oo`, `core/{domain}_table.oo`, `core/{domain}_parse.oo` — and these are themselves name-substituted clones (`drv_net_ring.oo` vs `drv_nvme_ring.oo` differ only in type/function names and one logline word, "packets" vs "NVMe commands").

**This is Fowler "Duplicated Code" + "Shotgun Surgery" at fleet scale:** a fix to the capability register must be applied in 17 repos.

### 3.4 `openOODA-kernel/ookernel-mm` — a memory manager hosting a third-party anti-cheat gate

`ookernel-mm/iommu/bedaisy_gate.oo:1-3` — "ookernel-mm BEDaisy.sys & Tiger Engine DX11/DX12 IOMMU Compatibility Gate … proving the IOMMU exposes the DMA translation, interrupt-remapping, and shared-virtual-memory surface that **BattlEye's BEDaisy.sys and the Destiny 2 Tiger Engine require**." The same gate concept is duplicated at `ookernel-ob/nt/{reqs,gate,render}.oo`.

A memory-manager repo must not carry a BattlEye/anti-cheat compatibility gate, and the gate is duplicated across two repos. **Verdict: extract to `ookernel-ob/nt/` before archiving `ookernel-mm`.**

### 3.5 `openOODA-agents/oorouter` — an L7 agent router carrying L6 GPU infrastructure

`oorouter/core/gpu_schedule.oo:3` — "Selects healthy GPU nodes for capability-masked inference tasks with fail-closed drops." `oorouter/core/fleet.oo:3` — "Routes inference tasks across the local 4-GPU Ollama fleet using health-probe admission."

The L6 canonical owner is `openOODA-cloud/ooinfer-grid/core/fleet.oo:3` — "Declares the local 4-GPU inference fleet with per-node masks and load" — and `ooinfer-grid/core/route.oo:3` — "Routes inference tasks to the lowest-load policy-admitted healthy GPU with fail-closed drops."

Same 4-GPU fleet, same admission, same lowest-load routing, implemented twice across a layer boundary. **Verdict: delete `oorouter/core/fleet.oo` and `oorouter/core/gpu_schedule.oo`.**

### 3.6 `openOODA-agents/ooherdr` — four domains in one binary

`ooherdr/core/herd.oo:3` (roster dispatch) + `persona/cluster.oo:3` (3-node cluster failover) + `persona/driver.oo:3` ("external CLI drivers (devin, mcode, vibe, grok, agy, oopi)") + `persona/oomux.oo:3` ("Multi-pane terminal layout manager for 5-pane builder, 5-pane reviewer, and experiment nodes").

A terminal multiplexer UI and a hardcoded vendor-driver registry inside the Layer-7 autonomous-agent repo. **Verdict: SPLIT** — extract `oomux` (TUI) and the driver registry.

### 3.7 `openOODA-apps` — the shared app framework is copy-pasted into every repo

Each of the 16 apps repos carries its own private copy of the same framework pages: `core/engine.oo`, `core/state.oo`, `core/persist.oo`, `core/capreg.oo`, `core/quorum.oo`, `core/share.oo`, `core/blackbox.oo`, `core/speculate.oo`, `ui/view.oo`, `ipc/wayland_client.oo`, `ipc/payload.oo`, `ipc/framebuf.oo`, `sec/pqcseal.oo`, `sec/audit.oo`, `sec/delegate.oo`, `sec/revoke.oo`, plus `tests/test_{pqc,audit,quorum,blackbox,speculate,delegate,revoke}.oo`.

Measured: `core/capreg.oo` is 43 lines in every repo, `ipc/wayland_client.oo` 54 lines, `sec/pqcseal.oo` 95 lines, `tests/test_main.oo` 112–113 lines — with distinct hashes per repo (i.e. hand-renamed copies, not one shared library).

This is exactly the duplication RFC 0012 §1 identifies as its second structural cause ("1,079 tiny `.oo` wrapper pages … are copied across the fleet instead of being imported from `openOODA-core/std`"). **Verdict: extract to a shared `std/app/…` module and import it, per Rule 1.25 §3.**

### 3.8 `openOODA-OS/ooinit` — PID 1 + service manager + health watchdog

`ooinit/README.md:68-70` and `ooinit/Makefile:9` compile `svcmgr/*.oo` (8 pages) and `healthd/*.oo` (8 pages) into the PID-1 binary alongside its own core. Lower severity than `ooimage` because all three share the `ProcessCap` supervision domain, but `healthd/` is separable. **Verdict: SPLIT candidate** — keep `oosvc-mgr` inside `ooinit`, split `oohealthd` out.

### 3.9 `openOODA-core/cli` — language driver + package installer + self-updater

`cli/README.md:36-52` lists 17 verbs across four domains: language (`build`/`run`/`test`/`fmt`), packaging (`install`), self-update (`update`/`upgrade`/`update --bootstrap`), scaffolding (`init`), telemetry (`token`), meta (`qa`/`context`/`fix`/`spec`). `cli/fix/fix.oo:21` is a 170-line function. **Verdict: KEEP** — the breadth is the CLI's stated job — but the `fix` verb is a large, separable domain.

### 3.10 `openOODA-tools` — the tools layer is un-consolidated

`openOODA-tools` holds ~257 micro-repos, each with `BIN := dist/<repo-name>`. **No Makefile in the entire repo declares a `PERSONAS :=` variable.** The only persona tables live in `qa/parity/personas.oot`, and exactly **8** repos have one: `oogzip`, `oohash`, `oob3sum`, `oocert`, `oo7z`, `oovault`, `ooxxd`, `ootar`.

The tools layer therefore has 249 tools with no persona surface at all, while RFC 0012 §2.3 targets **257 → 64 canonical multi-call utilities**. The gap is 193 tools with no declared canonical host.

Furthermore, those 8 persona tables **relay to system C binaries**:

- `oohash/ipc/dispatch_persona.oo:17-25` maps `sha256sum`/`sha512sum`/`sha1sum`/`sha224sum`/`sha384sum`/`b2sum`/`md5sum`/`cksum`/`xxhsum` to upstream names; `:49-61` resolves them in `/usr/local/bin`, `/usr/bin`, `/bin`, `/usr/local/sbin`, `/usr/sbin`, `/sbin`; `:64-78` `exec`s them.
- `oohash/qa/parity/personas.oot` holds 24 parity cases against GNU coreutils.
- `oo7z/qa/parity/personas.oot` holds 16 cases against `zip`/`unzip`/`zipinfo`.
- `oogzip/qa/parity/personas.oot` holds 24 cases against `gzip`/`xz`/`zstd`.
- `ooxxd/qa/parity/personas.oot` holds 8 cases against `hexdump`/`od`.
- `ootar/qa/parity/personas.oot` holds 8 cases against `cpio`/`ar`.
- `oocert/qa/parity/personas.oot` holds 9 cases against `openssl`/`trust`.
- `oovault/qa/parity/personas.oot` holds 5 cases against `gpg`.

**This is the single largest Rule-1.25 exposure in the fleet**: the canonical consolidated tools of Layer 3 do not implement their own persona modes — they `exec` GNU coreutils, OpenSSL and GPG. `oohash` in particular advertises itself as a "Sovereign Multi-Algorithm Cryptographic Digest Engine" (`oohash/Makefile:2`) while its `sha256`/`sha512`/`md5`/`cksum` personas are `exec` calls into `/usr/bin`.

**Verdict: this is a native-implementation debt, not a naming defect** — but it directly determines the archive/keep map, because a tool cannot be declared "absorbed" until its persona is natively implemented and parity-tested without the upstream binary present.

### 3.11 `openOODA-cloud/oobuild-fleet` ↔ `oodeploy` — mutual absorption cycle

Both repos declare each other as a persona, and both physical subtrees exist:
- `openOODA-cloud/oobuild-fleet/Makefile:24` — `built $(BIN) (--persona personas: oodeploy)`
- `openOODA-cloud/oodeploy/Makefile:25` — `built $(BIN) (--persona personas: oobuild-fleet, ooinfer-grid, oosched-cloud)`
- `oobuild-fleet/ooda.pkg:8` — "absorbs oodeploy into one sys_argv0 multi-call binary"
- `oodeploy/ooda.pkg:8` — "absorbs oobuild-fleet, ooinfer-grid, and oosched-cloud into one sys_argv0 multi-call binary"

Two canonical binaries for one domain, and the two drag in *different* third-party subtrees. `oobuild-fleet` additionally carries a stale `oobuild-fleet/etc/oodeploy.conf` — the absorbed sibling's config, with no `oobuild-fleet.conf` of its own.

**Verdict: break the cycle.** One host owns build+deploy+infer+sched; the other is archived.

---

## 4. Defect class (c) — Ambiguous, redundant, and colliding names (F1, F2, F3)

### 4.1 The fleet-wide collision matrix (machine-computed)

Method: every persona token was extracted from every persona dispatch table across all 9 orgs (`persona/dispatch.oo`, `personas/dispatch.oo`, `ipc/dispatch_persona.oo`, `ipc/persona_dispatch.oo`, `persona/meta.oo`), and intersected with the set of repo directory names (= the shipped binary names).

| Class | Count | Meaning |
|---|---|---|
| Tokens served as a persona by **2 or more distinct hosts** | **57** | The same invocation token resolves to different binaries depending on which host is invoked. |
| Tokens that are **a repo/binary in one org AND a persona of a different repo** | **49** (same-org) + **5** (cross-org) = **54** | The same token names a standalone binary and a subcommand of another binary. |
| **Union of all ambiguous / double-shipped tokens** | **82** | |
| Of those, **published in the signed public catalog** | **20** | User-visible on the install surface. |

### 4.2 The 20 catalog-exposed collisions — the highest-severity set

Each of these is a **signed, publicly installable package** whose name is *also* a persona token of a different canonical binary. Verified present in `/Projects/openOODA/catalog/index` and evidenced in source:

| Token | Published package | Also a persona of | Evidence |
|---|---|---|---|
| `oob3sum` | `openOODA-tools/oob3sum` | `oohash` | `oohash/ipc/dispatch_persona.oo:33` |
| `oohash` | `openOODA-tools/oohash` | `oob3sum` | `oob3sum/ipc/persona_dispatch.oo:32` |
| `oosha256` | `openOODA-tools/oosha256` | `oob3sum` **and** `oohash` | `oob3sum/ipc/persona_dispatch.oo:17`; `oohash/ipc/dispatch_persona.oo:17` |
| `oosha512` | `openOODA-tools/oosha512` | `oob3sum` **and** `oohash` | `oob3sum/ipc/persona_dispatch.oo:18`; `oohash/ipc/dispatch_persona.oo:18` |
| `oomd5` | `openOODA-tools/oomd5` | `oob3sum` **and** `oohash` | `oob3sum/ipc/persona_dispatch.oo:23`; `oohash/ipc/dispatch_persona.oo:23` |
| `oobase32` | `openOODA-tools/oobase32` | `oobase64` | `oobase64/ipc/…` |
| `oobase58` | `openOODA-tools/oobase58` | `oobase64` | `oobase64/ipc/…` |
| `oohex` | `openOODA-tools/oohex` | `oobase64` | `oobase64/ipc/…` |
| `oowget` | `openOODA-tools/oowget` | `oocurl` | `oocurl/persona/…` |
| `oowget2` | `openOODA-tools/oowget2` | `oocurl` | `oocurl/persona/…` |
| `oofetch` | `openOODA-tools/oofetch` | `oocurl` | `oocurl/persona/…` |
| `oogzip` | `openOODA-tools/oogzip` | `ooarchive` | `ooarchive/ipc/…` |
| `ooxz` | `openOODA-tools/ooxz` | `ooarchive` **and** `oogzip` | `oogzip/ipc/…`; `ooarchive/ipc/…` |
| `oozstd` | `openOODA-tools/oozstd` | `ooarchive` **and** `oogzip` | `oogzip/ipc/…`; `ooarchive/ipc/…` |
| `oounzip` | `openOODA-tools/oounzip` | `oo7z` **and** `ooarchive` | `oo7z/ipc/…`; `ooarchive/ipc/…` |
| `oossl` | `openOODA-tools/oossl` | `oocert` | `oocert/…` |
| `oomcp` | `openOODA-tools/oomcp` | **`openOODA-core/mcp`** | `mcp/persona/resolve.oo:60,66` |
| `oomcprun` | `openOODA-tools/oomcprun` | **`openOODA-core/mcp`** | `mcp/persona/resolve.oo:61,66` |
| `ooripl` | `openOODA-tools/ooripl` | **`openOODA-core/tui`** | `tui/persona/resolve.oo:60,65` |
| `oonotify` | `openOODA-tools/oonotify` | **`openOODA-DE/oopanel`** | `oopanel/core/persona/dispatch.oo:18,32` |
| `oobar` | `openOODA-tools/oobar` | **`openOODA-DE/oopanel`** | `oopanel/core/persona/dispatch.oo:16,35` |

Five of these cross an **organizational** boundary: a Layer-3 tool package is served as a persona by a Layer-0, Layer-2, or Layer-4 binary. The install surface and the runtime surface disagree.

### 4.3 The mutual-claim cycle (F3) — `oohash` ↔ `oob3sum`

```
openOODA-tools/oohash/ipc/dispatch_persona.oo:33
  if prog == "oohash" || prog == "b3sum" || prog == "oob3sum" || prog == "blake3" || prog == "b3" { return true; }

openOODA-tools/oob3sum/ipc/persona_dispatch.oo:32
  if prog == "oob3sum" || prog == "b3sum" || prog == "oohash" { return true; }
```

Each host claims the other as its own persona. Their relay tables are also near-identical: `oohash/ipc/dispatch_persona.oo:17-25` and `oob3sum/ipc/persona_dispatch.oo:17-24` map the same eight upstream digests. Their native engines are likewise duplicated — `oob3sum/core/{b3_chunk,b3_compress,b3_hex,b3_io,b3_keys,b3_state,b3_tree}.oo` versus `oohash/core/b3_hex.oo` and friends.

Neither repo can be archived until the cycle is broken and one owner is designated. RFC 0012 §2.2 item 4 assigns the digest family to **`oob3sum`**, which suggests `oohash` is the one to archive into it — but the directive (`ZERO_SYMLINKS_DIRECTIVE.md:14`) lists `oohash` as a canonical tool and does not list `oob3sum`. **The spec is itself ambiguous here**, which is the root cause.

### 4.4 Same-org dual-host ambiguities (the complete list)

| Token | Claimed by | Note |
|---|---|---|
| `ooclip` | `oofiles`, `ooportal` | DE — two hosts, full source copies in both |
| `ooshot` | `oofiles`, `ooportal` | DE — two hosts |
| `ootaskmgr` | `oocockpit`, `oofiles` | DE — two hosts |
| `oodns-cloud` | `oodns-cloud`, `oogateway`, `oomesh` | **3 hosts** (cloud) |
| `ooqueue` / `queue` | `oodb-dist`, `ooqueue`, `oosched-cloud` | **3 hosts** (cloud) |
| `oobuild-fleet` / `oodeploy` | each other | **mutual cycle** (cloud) |
| `oob3sum` / `oohash` | each other | **mutual cycle** (tools) |
| `oocockpit` | `oocockpit`, `oopanel` | DE — host is also a persona |
| `oolock` | `oocomp`, `oolock` | DE — host is also a persona |
| `ooidle`, `ooscreensaver` | `oocomp`, `oolock` | DE — the same two hosts both claim them |
| `oopi` | `oocoder`, `ooherdr` | agents |
| `dns` | `oodns-cloud`, `oogateway`, `oomesh` | cloud |
| `cas`, `cdn`, `consent`, `infer`, `relay`, `registry`, `queue` | respective pairs | cloud |
| `sha1sum`, `sha224sum`, `sha256sum`, `sha384sum`, `sha512sum`, `md5sum`, `cksum`, `b2sum`, `sha1`, `sha224`, `sha256`, `sha384`, `sha512`, `md5` | `oob3sum`, `oohash` | tools |
| `b3sum`, `b2`, `b3` | `oob3sum`, `oohash` | tools |

### 4.5 The archive/keep decision is blocked by a missing ownership table

There is **no machine-readable persona registry** for most of the fleet. `personas=` exists in `ooda.pkg` for only 3 agents repos (`oooda-engine/ooda.pkg:14`, `oocoder/ooda.pkg:14`, `ooherdr/ooda.pkg:14`) and **zero** cloud repos, whose absorption is recorded only in prose `tags=`/`description=` (e.g. `oostore/ooda.pkg:5,8`).

Until an authoritative table exists — one row per token, one column per candidate host — no repo can be safely archived, because there is no way to prove a token has exactly one owner.

### 4.6 Hidden aliases: persona ids that appear in no README

| Alias | Resolves to | Evidence |
|---|---|---|
| `oocompctl` | `oocomp` | `oocomp/core/persona/dispatch.oo:16,33` |
| `oowallpaper` | `oowall` | `oocomp/core/persona/dispatch.oo:18,31` |
| `oobar` | `oopanel` | `oopanel/core/persona/dispatch.oo:16,35` |
| `oonotify` | `ootoast` | `oopanel/core/persona/dispatch.oo:18,32` |
| `engine` | `oooda-engine` **and** `ooherdr` | `oooda-engine/persona/meta.oo:24`; `ooherdr/persona/meta.oo:34` |
| `ooidle`, `ooscreensaver` | `oolock` (self-absorbed) | `oolock/README.md:62-63` |

These are invisible to the documented contract and collide silently.

### 4.7 `sys_argv0` vs explicit-subcommand: two incompatible contracts (F4)

**Contract A — explicit subcommand (RFC 0012 §2.2 + Rule 1.25, compliant):**
`oohash/ipc/dispatch_persona.oo:16-46`; `oohash/main.oo:50-53`; `oob3sum/ipc/persona_dispatch.oo`; `openOODA-apps/oodocs/personas/dispatch.oo:38-45`; `openOODA-DE/*/core/persona/dispatch.oo`; `openOODA-cloud/*/persona/dispatch.oo`; `openOODA-agents/*/persona/meta.oo`.

**Contract B — argv0 basename (the superseded, symlink-dependent mechanism):**
- `openOODA-OS/ooimage/README.md:8-10` — "The persona is selected from the invocation basename under `ProcessCap` with `sys_argv0`, so one verified binary answers to every name of the consolidated daemon."
- `openOODA-OS/ooimage/main.oo:62` — `let argv0: String = sys_argv0(proc_cap);`
- `openOODA-OS/ooimage/main.oo:8` — "Resolve the persona from argv[0], the dispatch controls, or a leading persona subcommand."

**Public documentation still advertises Contract B:**
- `openOODA/website/llms.txt:35` — "RFC 0012 Unix \"Less-Is-More\" multi-call **`sys_argv0` symlink dispatch**".
- `openOODA/openOODA/rfcs/0012-…:14-17` explicitly *supersedes* it — the RFC itself is correct; the website is not.

**Stale symlink-applet documentation (9 agents repos):** each advertises an `ooagent-*` argv0 symlink applet that was deliberately deleted (commit `e6e8b2c "fix(oocoder): drop argv0/symlink dispatch per Rule 1.25 — operand+--persona only"`):
`ooarchitect/README.md:33`, `ooeval/README.md:33`, `ooevolve/README.md:33`, `oomemory/README.md:33`, `ooplanner/README.md:33`, `ooquota/README.md:34`, `ooredteam/README.md:34`, `oorelease/README.md:33`, `oorouter/README.md:33`.
Also `openOODA-agents/oooda-engine/README.md:25,61` ("installs an applet symlink per absorbed persona under `bin/`") and `AGENTS.md:44,53` ("`make build` symlinks `bin/ooplanner` and `bin/ooarchitect` to the engine") — the Makefile contains no `ln`/`symlink` command at all.

**Verdict:** Contract A is correct and universally implemented except in `ooimage`; Contract B survives only in `ooimage`'s source and in stale documentation. **Fix `ooimage` to Contract A and scrub the documentation** — this is a zero-code-cost correctness fix for the public contract.

### 4.8 Redundant name forms

| Form | Instances | Assessment |
|---|---|---|
| `oo` prefix on a non-`oo` binary | `cli`, `tui`, `lsp`, `mcp`, `opm` in `openOODA-core` | The `oo` prefix is the project namespace convention; these five do not carry it. `~/.openooda/bin/mcp` and `~/.openooda/bin/lsp` are dangerously generic global names. **RENAME → `oocli`, `ootui`, `ooda-lsp`, `ooda-mcp`, `oopm`.** |
| `-cloud` suffix inside `openOODA-cloud` | `oodns-cloud`, `oosched-cloud`, `ooregistry-cloud` | Redundant (§2.14). |
| `ooagent-*` prefix | 9 stale README references; `oocoder/persona/meta.oo:20` still registers `ooagent-cli` as a live persona id | Conflicts conceptually with the live `openOODA-DE/ooagent-hud` family. |
| `v2` suffix | `oocgroup` vs `oocgroupv2` (tools) | `oocgroupv2` is a sibling repo, not a version of a persona. `oosdiff`/`oowdiff`/`oocmp`/`oodiff` are four repos for one diff domain. |
| `ookernel-mmu` vs `ookernel-mm` | kernel | One-token near-duplicate, both persona ids of `ookernel-mm`. |

---

## 5. Defect class (d) — Absorption status, and which repos are ready to archive

### 5.1 The structural rule that is not being enforced (F8)

RFC 0012 §2.2 item 5 requires: *"One consolidated binary is installed under its canonical name only. The persona names of section 2.2 item 4 are accepted as tokens by that binary and are not installed as files."*

Across the fleet, **every absorbed repo still declares `BIN := bin/<name>` and still ships a compiled binary of that name.** Examples with `bin/` evidence:

- `openOODA-apps/oopdf/bin/oopdf`, `oosheet/bin/oosheet`, `oodeck/bin/oodeck`, `oonotes/bin/oonotes`, `oopaint/bin/oopaint`, `oomail/bin/oomail`, `oogit-ui/bin/oogit-ui` — all absorbed personas of `oodocs`/`oocanvas`/`oochat`/`oostudio`, all still shipping.
- `openOODA-DE/ooshot/bin/ooshot` (80,944 B), `ooview/bin/ooview` (84,952 B) — absorbed, still shipping.
- `openOODA-kernel/ookernel-mm/bin/ookernel-mm`, `ookernel-iommu/bin/ookernel-iommu`, `ookernel-ipc/bin/ookernel-ipc`, `ookernel-ob/bin/ookernel-ob`, `ookernel-unikernel/bin/ookernel-unikernel`, `ookernel-hal-arm64/bin/…`, `ookernel-hal-riscv/bin/…`, `oodrv-pci/bin/…`, `oodrv-usb-hid/bin/…`, `oodrv-virtio/bin/…`, `oodrv-display-gop/bin/…` — 12 kernel repos absorbed, 12 binaries still shipping.
- `openOODA-cloud/oocdn/bin/oocdn`, `oodns-cloud/bin/…`, `oorelay/bin/…`, `ooconsent/bin/…`, `ooregistry-cloud/bin/…`, `oostore-cas/bin/…`, `ooqueue/bin/…`, `ooinfer-grid/bin/…`, `oosched-cloud/bin/…` — absorbed, still shipping.
- `openOODA-agents/ooplanner/bin/ooplanner`, `ooarchitect/bin/…`, `ooeval/bin/…`, `ooevolve/bin/…`, `ooredteam/bin/…`, `oorelease/bin/…` — absorbed, still shipping.

**Consequence:** the ambiguity in §4 is not a documentation defect — it is a live install-surface defect. The name `ooshot` denotes a real file and a real subcommand.

### 5.2 The 20 repos that are unambiguously ready to archive

These are absorbed by exactly one host, the host ships the full source copy, and the standalone binary is a duplicate. Archiving them removes a token from the ambiguity set.

| # | Repo | Canonical host | Host evidence | Also in signed catalog? |
|---|---|---|---|---|
| 1 | `openOODA-apps/oopdf` | `oodocs` | `oodocs/Makefile:10`; `oodocs/personas/oopdf/*` | no |
| 2 | `openOODA-apps/oosheet` | `oodocs` | `oodocs/Makefile:10`; `oodocs/personas/oosheet/*` | no |
| 3 | `openOODA-apps/oodeck` | `oodocs` | `oodocs/Makefile:10`; `oodocs/personas/oodeck/*` | no |
| 4 | `openOODA-apps/oonotes` | `oodocs` | `oodocs/Makefile:10`; `oodocs/personas/oonotes/*` | no |
| 5 | `openOODA-apps/oopaint` | `oocanvas` | `oocanvas/Makefile:10`; `oocanvas/personas/oopaint/info.oo` **byte-identical** | no |
| 6 | `openOODA-apps/oomail` | `oochat` | `oochat/Makefile:9`; `oochat/personas/oomail/*` | no |
| 7 | `openOODA-apps/oogit-ui` | `oostudio` | `oostudio/Makefile:9`; `oostudio/personas/oogit-ui/*` | no |
| 8 | `openOODA-DE/ooagent-hud` | `oocockpit` | `oocockpit/core/persona/dispatch.oo:17,29` | no |
| 9 | `openOODA-DE/ooedit` | `oofiles` | `oofiles/core/persona/dispatch.oo:18,33` | no |
| 10 | `openOODA-DE/oolaunch` | `oopanel` | `oopanel/core/persona/dispatch.oo:20,34` | no |
| 11 | `openOODA-DE/ooshelf` | `oopanel` | `oopanel/core/persona/dispatch.oo:17,31` | no |
| 12 | `openOODA-DE/ootoast` | `oopanel` | `oopanel/core/persona/dispatch.oo:18,32` | no |
| 13 | `openOODA-DE/ooview` | `oofiles` | `oofiles/core/persona/dispatch.oo:17,32` | no |
| 14 | `openOODA-DE/oowm` | `oocomp` | `oocomp/core/persona/dispatch.oo:17,30` | no |
| 15 | `openOODA-DE/oowall` | `oocomp` | `oocomp/core/persona/dispatch.oo:18,31` | no |
| 16 | `openOODA-agents/ooplanner` | `oooda-engine` | `oooda-engine/persona/meta.oo:18,25` | no |
| 17 | `openOODA-agents/ooeval` | `ooconsensus` | `ooconsensus/main.oo:34,38`; `ooconsensus/Makefile:9` | no |
| 18 | `openOODA-agents/ooevolve` | `ooconsensus` | `ooconsensus/main.oo:34,39` | no |
| 19 | `openOODA-agents/ooredteam` | `oofalsify` | `oofalsify/main.oo:19-23`; `oofalsify/Makefile:9` | no |
| 20 | `openOODA-agents/oorelease` | `oogovern` | `oogovern/main.oo:44,49`; `oogovern/Makefile:9` | no |

### 5.3 Repos ready to archive **after** an arbitration (2+ candidate hosts)

These cannot be archived until exactly one host is designated, because archiving them would break the other host's persona.

| Repo | Candidate hosts | Arbitration needed |
|---|---|---|
| `openOODA-DE/ooclip` | `oofiles`, `ooportal` | pick one (recommend `ooportal`) |
| `openOODA-DE/ooshot` | `oofiles`, `ooportal` | pick one (recommend `ooportal`) |
| `openOODA-DE/ootaskmgr` | `oocockpit`, `oofiles` | pick one (recommend `oocockpit`) |
| `openOODA-DE/oocockpit` | `oopanel` (it is also a host) | demote to persona-only |
| `openOODA-DE/oolock` | `oocomp` (it is also a host) | demote to persona-only |
| `openOODA-kernel/oodrv-usb-hid` | `oodrv-net`, `oodrv-display-gop` | pick one |
| `openOODA-kernel/ookernel-iommu` | `ookernel-mm`, `ookernel-sched` | pick one |
| `openOODA-kernel/ookernel-unikernel` | `ookernel-boot`, `ookernel-sched` | pick one |
| `openOODA-kernel/oodrv-pci` | `oodrv-net` (it is also a host) | demote |
| `openOODA-kernel/oodrv-virtio` | `oodrv-pci` (it is also a host) | demote |
| `openOODA-kernel/oodrv-display-gop` | `oodrv-net` (it is also a host) | demote |
| `openOODA-kernel/ookernel-mm` | `ookernel-sched` (it is also a host) | demote — **after** extracting `iommu/bedaisy_gate.oo` (§3.4) |
| `openOODA-kernel/ookernel-ipc` | `ookernel-sched` | archive |
| `openOODA-kernel/ookernel-ob` | `ookernel-sched` | archive |
| `openOODA-kernel/ookernel-hal-arm64` | `ookernel-hal-x86` | archive |
| `openOODA-kernel/ookernel-hal-riscv` | `ookernel-hal-x86` | archive |
| `openOODA-cloud/oodns-cloud` | `oogateway`, `oomesh` | pick one |
| `openOODA-cloud/ooqueue` | `oodb-dist`, `oosched-cloud` | pick one |
| `openOODA-cloud/oobuild-fleet` | `oodeploy` (and vice versa) | **break the cycle** |
| `openOODA-cloud/oodeploy` | `oobuild-fleet` (and vice versa) | **break the cycle** |
| `openOODA-cloud/oocdn` | `oogateway` | archive |
| `openOODA-cloud/ooconsent` | `ooidentity` | archive |
| `openOODA-cloud/oorelay` | `oomesh` | archive |
| `openOODA-cloud/ooregistry-cloud` | `oostore` | archive |
| `openOODA-cloud/oostore-cas` | `oostore` | archive |
| `openOODA-cloud/ooinfer-grid` | `oodeploy` | archive |
| `openOODA-cloud/oosched-cloud` | `oodeploy` | archive |
| `openOODA-agents/ooarchitect` | `oooda-engine`, `oogovern` (**divergent implementations**) | pick one; `oogovern/ooarchitect/core/layout.oo` is byte-identical to the standalone, `oooda-engine/persona/architect.oo` is a rewritten variant that **drops** `ooarch_basename` |
| `openOODA-agents/oocoder` | `ooreviewer` (it is also a host) | demote |
| `openOODA-core/ooda` | `cli` | archive — already a persona (`cli/persona/resolve.oo:59`) |

### 5.4 The catalog-exposed set that must be archived or withdrawn (highest user impact)

These 20 are signed public packages **and** personas of another binary. Each needs one of: (a) archive the standalone repo and withdraw the catalog entry, or (b) withdraw the persona from the host.

| Catalog package | Persona owner | Recommended action |
|---|---|---|
| `oob3sum`, `oohash` | each other | designate one owner (RFC 0012 says `oob3sum`), archive the other, remove the reciprocal persona entry |
| `oosha256`, `oosha512`, `oomd5` | `oob3sum` + `oohash` | archive all three repos; keep the persona tokens |
| `oobase32`, `oobase58`, `oohex` | `oobase64` | archive the three; keep the persona tokens |
| `oowget`, `oowget2`, `oofetch` | `oocurl` | archive the three; keep the persona tokens |
| `oogzip`, `ooxz`, `oozstd`, `oounzip` | `ooarchive` / `oogzip` / `oo7z` | designate `ooarchive` as the archive host (RFC 0012 §2.2 lists `ootar`, `oozstd`, `oogzip`, `ooxz`, `oozip` together); archive the four |
| `oossl` | `oocert` | archive; keep the persona token |
| `oomcp`, `oomcprun` | `openOODA-core/mcp` | **cross-org** — archive the tools repos, withdraw from `catalog/index` |
| `ooripl` | `openOODA-core/tui` | **cross-org** — archive, withdraw |
| `oonotify`, `oobar` | `openOODA-DE/oopanel` | **cross-org** — archive, withdraw, or rename the DE persona to `oopanel-notify` / `oopanel-bar` |

### 5.5 The `oollama` anomaly

`openOODA-tools/oollama` is the **only** tools repo with **no catalog entry** (all 256 other tool repos are registered). Meanwhile `openOODA-OS/ooaid/persona/anchor.oo:50-74` absorbs `oollama` as a persona ("Publish the canonical ooaid persona and the absorbed oollama persona").

The catalog omission and the cross-org absorption are the same fact: the tool was absorbed into `ooaid` but the standalone repo was never archived. `oollama` is therefore the one tools repo whose absence from the catalog is *correct* — every other tool's presence is the anomaly.

### 5.6 Canonical hosts to KEEP (do not archive)

| Org | Canonical hosts |
|---|---|
| core (L0) | `cli`, `oodac`, `oodar`, `opm`, `tui` (+ `std` after the §2.1 split) |
| kernel (L1) | `oodrv-net`→`oodrv-io`, `oodrv-nvme`→`oodrv-storage`, `oodrv-pci`, `oodrv-display-gop`→`oodrv-ui`, `ookernel-sched`→`ookernel`, `ookernel-boot`→`ooboot`, `ookernel-hal-x86`→`oohal` |
| OS (L2) | `ooinit`, `oovfs`, `oonetd`, `oosysbus`, `ooaid`, `oodevd`, `oosession`, `ooimage`→`oocontainer` |
| tools (L3) | `oohash`/`oob3sum` (one), `oobase64`→`oocodec`, `ooarchive`, `oocurl`, `oodiff`, `oosh`, `ootext` (to be created) |
| DE (L4) | `oocomp`, `oopanel`→`ooshell`, `ooportal`→`oogrant`, `oofiles`→`ooshell`/rename, `ooterm`, `oosettings`, `oobazaar`, `oolock` |
| apps (L5) | `oodocs`→`oooffice`, `oocanvas`, `oochat`, `oostudio`, `ooflash`, `oobrowser`, `oodaw`, `oopass`, `oovm-ui`→`oohostmon` |
| cloud (L6) | `oostore`, `oomesh`, `oogateway`, `ooidentity`, `oodb-dist`, `ootelemetry`, `oobilling` |
| agents (L7) | `oooda-engine`→`ooooda`, `ooherdr`, `ooconsensus`, `oofalsify`, `oogovern`, `ooreviewer`, `oocoder`, `oomemory`, `ooquota` |

---

## 6. Defect class (e) — Consolidation target vs reality (F10)

RFC 0012 §2.3 sets the target: **377 → 129 canonical repos**, with a per-org list. Cross-checked against the tree:

### 6.1 Canonical target names in RFC 0012 §2.3 that do not exist as repos

| Org | RFC target name | Status |
|---|---|---|
| kernel | `ooboot` | no repo — the boot repo is `ookernel-boot` (which carries `ooboot` as a persona) |
| kernel | `oohal` | no repo — the HAL repo is `ookernel-hal-x86` (carries `oohal` as a persona) |
| kernel | `ookernel` | no repo — `ookernel-sched` carries it as a persona |
| kernel | `oodrv-storage` | no repo — `oodrv-nvme` carries it as a persona |
| kernel | `oodrv-io` | no repo — `oodrv-net` carries it as a persona |
| kernel | `oodrv-virt` | no repo — `oodrv-virtio` carries it as a persona |
| OS | `ooauthd` | **no repo and no persona anywhere** — the real repos are `ooaid` and `oopolicyd` |
| DE | `ooshell` | no repo — the role is split between `oopanel` and `oofiles` (§2.4, §2.5) |
| apps | `oooffice` | **no repo** — the office host is named `oodocs`, though `oodocs/personas/multicall.oo:3` calls it "the canonical oooffice engine" and `oodocs/personas/dispatch.oo:20` serves the alias `oooffice` |
| tools | `oocodec` | no repo — the codec host is `oobase64`, which absorbs `oobase32`, `oobase58`, `oohex` |
| tools | `ootext` | no repo — `oote` is a **theme** engine (§2.15) |
| agents | `oofalse` | no agent repo — and **`openOODA-tools/oofalse` is the POSIX `false` utility**. The RFC's agents list names a token owned by a different org |

**Two of these are outright errors in the governing spec**: `ooauthd` (a repo that never existed) and `oofalse` in the agents list (a token owned by `openOODA-tools`).

### 6.2 Existing repos with no canonical target in RFC 0012 §2.3

| Org | RFC target count | Repos with no planned home |
|---|---|---|
| kernel (16→6) | 6 | `oodrv-net`, `oodrv-pci`, `oodrv-nvme`, `oodrv-usb-hid`, `oodrv-virtio`, `oodrv-display-gop`, `ookernel-boot`, `ookernel-hal-x86`, `ookernel-hal-arm64`, `ookernel-hal-riscv`, `ookernel-sched`, `ookernel-mm`, `ookernel-ipc`, `ookernel-iommu`, `ookernel-ob`, `ookernel-unikernel` — all 16 are named only via *persona* names, not repo names |
| OS (18→8) | 8 | `oorealm`, `oosvc-mgr`, `oopowerd`, `oodnsd`, `oosession`, `oofs-ext4`, `oodevd`, `oofs-tmp`, `ooaudiod`, `oologd`, `oopolicyd` — 11 repos unassigned |
| tools (257→64) | 64 | ~193 repos have no declared host; only 5 persona tables exist (RFC §2.2 item 4) |
| DE (20→9) | 9 | `oocockpit`, `ootoast`, `ootaskmgr`, `ooview`, `oowm`, `ooshelf`, `oowall`, `oolaunch`, `ooedit`, `ooshot`, `ooclip` — 11 repos unassigned |
| apps (17→11) | 11 | `oodocs` (the actual office host is not in the list; `oooffice` is), `oochat` (the actual comms host is not in the list) |
| cloud (18→8) | 8 | `ooconsent`, `ooqueue` — 2 repos unassigned |
| agents (16→8) | 8 | `oorouter`, `ooreviewer`, `ooevolve`, `ooplanner`, `oorelease`, `ooarchitect`, `ooeval`, `ooredteam` — 8 repos unassigned |

### 6.3 The spec's own persona table vs the tree

RFC 0012 §2.2 item 4 assigns:
- **HTTP/Transfer → `oocurl`**: `oocurl`, `curl`, `oowget`, `wget`, `oowget2`, `wget2`, `oofetch` — implemented as personas of `oocurl`, but `oowget`, `oowget2`, `oofetch` also ship as standalone catalog packages (§4.2).
- **Diff/Comparison → `oodiff`**: `oodiff`, `diff`, `oosdiff`, `sdiff`, `oowdiff`, `wdiff`, `oocmp`, `cmp`, `oocomm`, `comm` — the tree has **five separate diff repos** (`oodiff`, `oodiff3`, `oogitdiff`, `oowdiff`, `oosdiff`) plus `oocmp`, `oocomm`, `ooschemadiff`, `oosemantcdiff`, `oostructureddiff`, `oobindiff`.
- **Cryptographic Digests → `oob3sum`**: `oob3sum`, `b3sum`, `oosha256`, `sha256sum`, `oomd5`, `md5sum`, `oocksum`, `cksum`, `oohash` — the tree's owner is `oohash`, and both claim each other (§4.3). The spec names `oob3sum`; the directive names `oohash`. **The spec must pick one.**
- **Archive/Compression → `ootar`, `oozstd`, `oogzip`, `ooxz`, `oozip`**: the tree's de-facto owner is `ooarchive`, which absorbs `oogzip`, `ooxz`, `oozstd`, `oounzip`. **`oozip` and `ooarchive` are not in the RFC list.**
- **Shell Builtins → `oosh`**: `oosh`, `sh`, `oobash`, `bash`, `ootrue`, `true`, `oofalse`, `false`, `ooyes`, `yes`, `oowhich`, `which` — the tree has `oosh`, `oobash`, `ootrue`, `oofalse`, `ooyes` as separate repos. `oowhich` does not exist; `openOODA-tools/owhich`… does not exist (verified).
- **Cloud → 8 engines**: matches the tree's absorption graph, except `ooconsent` and `ooqueue` are unassigned (§6.2).

### 6.4 The `unix_consolidation_blueprint.md` referenced by the directive does not exist

`openOODA/ZERO_SYMLINKS_DIRECTIVE.md:19-20` states: *"`unix_consolidation_blueprint.md` has been updated to remove `oo_sys_argv0` symlink dispatch and codify the Zero Symlinks / Hardlinks Law."*

**No file named `unix_consolidation_blueprint.md` exists anywhere under `/Projects`** (searched recursively across all 9 orgs). The consolidation contract actually lives in `openOODA/openOODA/rfcs/0012-unix-less-is-more-consolidation.oot`. The directive points at a phantom document — the same class of defect as the `ooffice`/`oooffice` typo (§4.8, §7.2).

---

## 7. Additional defects found while verifying (not in the original hunt list)

### 7.1 `website/llms.txt` is factually wrong about the dispatch mechanism and the repo counts

`openOODA/website/llms.txt:35`:
> "…RFC 0012 Unix \"Less-Is-More\" multi-call **`sys_argv0` symlink dispatch**, `102/102` KVM microVM verification…"

- The "`sys_argv0` symlink dispatch" claim contradicts Rule 1.25 and the RFC's own "Supersedes" clause (`rfcs/0012-…:14-17`).
- The per-org repo counts are stale: `openOODA-apps 16/16` (there are now **17** apps repos, `ooflash` added), and the fleet total `385` / `377/377` no longer matches.

### 7.2 `oodocs/README.md:54` documents a persona alias that does not exist

> "…the office-suite personas: `oodocs`, `oosheet`, `oodeck`, `oonotes`, and `oopdf` (**umbrella alias `ooffice` maps to `oodocs`**)."

The code implements **`oooffice`** (two leading `o`s), not `ooffice`:
`oodocs/personas/dispatch.oo:20` — `if name == "oodocs" || name == "oooffice" { return oodocs_mc_persona_docs(); }`; `oodocs/Makefile:146` — `@./$(BIN) oooffice --version | grep -q …`; `oodocs/tests/multicall/test_multicall.oo:50,59` asserts `"oooffice"`.

A user following the README would run a subcommand the dispatcher rejects. The same phantom-documentation class as the missing `unix_consolidation_blueprint.md`.

### 7.3 README page-count and assertion-count drift is systemic

- **Page counts**: `openOODA-apps` READMEs use a boilerplate `## Architecture — 25 .oo pages` header and a 25-row table; the actual counts are 30 (`oopdf`, `oosheet`, `oodeck`, `oonotes`, `oopaint`, `oomail`, `oogit-ui`, `oobrowser`, `oodaw`, `oopass`, `oovm-ui`), 34 (`oocanvas`, `oochat`, `oostudio`), 47 (`oodocs`), 30 (`oomedia` post-split), 16 (`ooflash`).
- **Kernel** is worse: `oodrv-display-gop/README.md:5` claims 16 pages but has **36**; `oodrv-pci` claims 15, has 36; `ookernel-boot` claims 15, has 36; `ookernel-hal-x86` claims 14, has 37; `oodrv-usb-hid` claims 10, has 30. The undocumented files are the shared scaffolding.
- **Assertion counts**: 11 apps repos gate `95/95` in their Makefile but the README header *and* table say `80`.
- **Versions**: 11 agents repos have README versions one behind the Makefile `VER` (e.g. `ooarchitect` 0.3.9 vs 0.4.0; `oocoder` 0.3.9 vs 0.4.1; `ooherdr` 0.3.9 vs 0.4.1). `openOODA-core/oodac/ooda.pkg` says `0.2.3` while `oodac/VERSION` says `oodac=0.11.63`; `oodar/ooda.pkg` says `0.2.3` while `oodar/VERSION` says `oodar=4.2.0`.
- **Org profile tables**: `openOODA-DE/.github/README.md:19` says "The 20 Desktop Environment Repositories" but lists **18** (`oobazaar` and `oocockpit` are absent). `openOODA-OS/.github/README.md:17` says `v0.2.3` while `.github/profile/README.md:17` says `v0.3.3`.

### 7.4 The org profile tables advertise absorbed personas as independent products

`openOODA-DE/.github/profile/README.md:33-46` lists every absorbed persona (`oowm`, `ooshelf`, `ootoast`, `ooshot`, `ooview`, `ooclip`, `ootaskmgr`, `ooedit`, `oolaunch`) as if each were an independent repository. The same is true of `openOODA-OS/.github/profile/README.md:23-40`. This is how the §4 ambiguity survived: the public surface still advertises 18 DE repos as peers when 11 are already personas.

Separately, **every one of the 20 DE micro-repos carries a `.github/profile/README.md` whose body is byte-identical** across all 20 (sha256 prefix `b44b0837587a31fb`) — a generated template stub, not documentation.

### 7.5 `openOODA-core/oodac` ships four differently-named copies of the compiler

| path | md5 |
|---|---|
| `oodac/bin/oodac` | `45868c8b6f155286d613b9f5f00307bd` |
| `oodac/bin/oodac.real` | `45868c8b6f155286d613b9f5f00307bd` (identical) |
| `oodac/bin/oodac_bin.core` | `0927031ee9d0d9637425ad05d55814e6` (stale, Oct 25) |
| `oodac/oodac_bin` (repo **root**) | `65375110dc557371a7647fd25de33ce3` (stale, Nov 2) |

Plus `cli/dist/cli` and `cli/dist/cli-linux-x86_64` are byte-identical copies under two names in one `dist/`.

### 7.6 `openOODA-kernel` `SRC` lists omit `fs/fsprobe.oo`

`main.oo:11` (or `:12`) imports `"fs/fsprobe.oo"` in `oodrv-net`, `oodrv-pci`, `oodrv-nvme`, `ookernel-mm`, `ookernel-iommu`, `ookernel-ipc` — but the `SRC :=` variable in each Makefile never lists it. The build still succeeds because `SRC` is only a `$(BIN): $(SRC)` **prerequisite** while the actual compile follows imports — so `SRC` is an incomplete dependency list and incremental rebuilds will not re-trigger on a `fsprobe.oo` change.

### 7.7 The "ELF64 boot image" inspect claim is copy-pasted into unrelated kernel drivers

`README.md` lines for `oodrv-net:43`, `oodrv-nvme:41`, `ookernel-iommu:35`, `ookernel-ipc:36`, `ookernel-mm:53`, `ookernel-sched:43` all say `inspect # JSON status + decoded ELF64 boot image header record`. Their actual codecs decode unrelated records: `oodrv-net/core/drv_net_parse.oo:3` = "ethernet frame header"; `oodrv-nvme/core/drv_nvme_parse.oo:3` = "NVMe submission command"; `ookernel-ipc/core/ipc_parse.oo:3` = "IPC message frame"; `ookernel-iommu/core/iommu_parse.oo:3` = "IOMMU context entry". Only `ookernel-boot/README.md:17` legitimately decodes an ELF64 boot image.

### 7.8 Hardcoded hostnames and Tailscale IPs inside `.oo` sources (F12)

| file:line | content |
|---|---|
| `openOODA/openOODA/buildbox/eco/status.oo:176` | `status_node_telemetry(sys, fs_r, fs_w, "zebes", "100.102.186.93", "control/herdr")` |
| `openOODA/openOODA/buildbox/eco/status.oo:177` | `… "ringmaster", "100.88.249.93", "buildbox+gpu")` |
| `openOODA/openOODA/buildbox/eco/status.oo:178` | `… "spotlight", "100.66.54.24", "llm+replica")` |
| `openOODA/openOODA/buildbox/fanout.oo:91` | `env_or(env, "OODA_SPOTLIGHT", "http://100.66.54.24:11434")` — hardcoded Tailscale default |
| `openOODA/openOODA/buildbox/eco/ledger/quota_ledger.oo:76` | `ql_probe_host(sys, "100.88.249.93")` |
| `openOODA/openOODA/buildbox/eco/ledger/quota_ledger.oo:77` | `ql_probe_host(sys, "100.66.54.24")` |
| `openOODA/openOODA/buildbox/spotlight/reviewer.oo:3` | "…continuous review daemon for spotlight (100.66.54.24)…" |

**Fair qualification:** `fanout.oo:91` and `quota_ledger.oo:76-77` are env-overridable, so they are *defaults*, not hard bindings. `status.oo:176-178` are hard bindings.

**Hostnames inside live identifiers (values are env-driven, names are not):**
`openOODA-OS/ooaid/net/config.oo:50` `pub fn ooaid_node_spotlight(env: &EnvCap)`, `:61` `pub fn ooaid_node_ringmaster(env: &EnvCap)`, `:73-74` call sites; `openOODA-OS/ooaid/net/router.oo:47,76,77`. The *values* are correctly env-driven (`OODA_AID_NODE0_ADDR` default `"unbound"`), but the *identifiers* embed fleet hostnames into a repo that must run standalone.

**One legitimate exception:** `openOODA/openOODA/buildbox/eco/status_sync/sections_p2.oo:79-84` and `test_status_helpers.oo:87-97` deliberately contain those literals **in order to redact them** before publication. That is an acceptable, intentional use — a redaction table is not a host binding. It should be declared as a scoped exemption rather than left as an incidental violation.

**Note on `openOODA-core/oodac/qa/emit_gap_inline_repro.oo`** — the `spotlight` hits at `:9,20,121` and the `OODA_SPOTLIGHT` env reads at `:12,124` are in a QA fan-out script, not a library; and `openOODA-core/std/app/ui/pbr_raytracing/light_point_directional.oo:21` (`type SpotLight = struct`), `std/app/ui/3d/lights_spot.oo`, `lights_engine.oo` are a legitimate 3D lighting type, **not** the `spotlight` service — false positives.

### 7.9 `openOODA-core/oodac/scripts/oodac_cluster.sh` is a real legacy fallback path

`oodac/scripts/oodac_cluster.sh:24` — `REAL_BIN="${OODA_COMPILER:-$REPO_ROOT/bin/oodac}"` — a distributed build router that fans out to remote builders, an alternate implementation path around the real compiler.

`openOODA-core/tui/mcp_client.oo:79` — a shell one-liner probing `command -v ooda-mcp || command -v mcp`, then two `$codex/bin` paths, then two `$HOME/.openooda/bin` paths, then bare `"mcp"` — **five sequential legacy-name fallbacks** for one binary.

`openOODA-core/cli/build/spawn.oo:33-38` — `spawn_alias()` maps `"lsp"`→`"ooda-lsp"` and `"mcp"`→`"ooda-mcp"`, commented "Old on-disk names only."

### 7.10 The `install/` surface installs only 8 components, and 5 of them lack the `oo` prefix

`install/install.sh:105` — `declare -A BINARIES=([ooda]=ooda [oodac]=oodac [oodar]=liboodar.a [opm]=opm [lsp]=lsp [mcp]=mcp [cli]=cli [tui]=tui)`, mirrored by `install/docs/surface.oot:33` and gated by `install/qa/qa-02-bin_manifest.oo`.

Correct per Rule 1.25 (canonical binaries only, no persona aliases as files). But `~/.openooda/bin/mcp` and `~/.openooda/bin/lsp` are dangerously generic global binary names that will collide with unrelated tools, and they break the project's own `oo` namespace convention.

### 7.11 The catalog is clean on drift but is the only registry — L1/L2/L4/L5/L6/L7 have no registry at all

`catalog/index` holds 260 names; `catalog/` holds 256 package directories; the 4 extras (`caps`, `echo`, `hello`, `sqlite`) are example packages. **Zero drift** between the index and the on-disk set — this is the single best-maintained surface in the project.

But the catalog registers **only L3 tools**. `grep -cE "^(oomedia|oodocs|oopaint|oochat|oostudio|oobrowser|oonotes|oopdf|oopass|oosheet|oodeck|oodaw|oocanvas|oogit-ui|oovm-ui|oomail|ooflash)\|" catalog/index` → **0**. No apps binary is registry-checked, which is precisely why the §4.1 apps collisions survived.

---

## 8. Coding-standards conformance sweep (fleet-wide, read-only)

| Standard | Result |
|---|---|
| **`.oo` file ≤ 256 lines** | **1 finding fleet-wide**: `openOODA-core/oodac/tests/fixtures/boundary_257_lines.oo` (257 lines) — a deliberate negative-test fixture whose sibling `boundary_256_lines.oo` is exactly 256. **Needs a CI allowlist entry**, otherwise a naive `find`-based line gate flags it. |
| **≤ 8 functions per file** | **0 findings** in kernel, OS, DE, apps, cloud, agents, tools. **246 files exceed it in `openOODA-core`** (195 in `std`, 32 in `oodac`, 9 in `tui`, 4 in `opm`, 3 in `mcp`, 2 in `cli`, 1 in `lsp`). Worst: `std/app/ai/multimodal/ai_multimodal.oo` (87 fns), `std/meta/test/anchor.oo` (58), `oodac/ast/ast.oo` (57), `std/hw/runtime/rt_caps_check.oo` (55). The dominant class is machine-generated `anchor.oo` re-export shims — an exemption class that needs to be declared, not silently tolerated. |
| **≤ 40 lines per function** | **0 findings** in kernel, OS, DE, apps, cloud, agents, tools. **1,857 findings in `openOODA-core`** (1,517 in `std`, 194 in `oodac`, 58 in `tui`, 28 in `opm`, 28 in `mcp`, 17 in `cli`, 10 in `lsp`, 5 in `ooda`). Worst: `std/science/bio/smiles_parse.oo:14` (222), `std/sec/hash/sha256_engine.oo:15` (210), `oodac/lex/lex.oo:15` (209), `std/sec/symmetric/poly1305.oo:14` (206), `std/sec/symmetric/poly1305_core.oo:14` (204) — the last two are a **duplicated 200-line `poly1305_mac` in two files**. |
| **Directory density ≤ 8 entries** | 0 findings in apps (densest `ooflash/flash/` = 7). |
| **Academy 4-block header** | 0 findings in apps (371+ files), OS, DE, cloud, agents, tools. |
| **Zero symlinks** | **0 symlinks across all 9 org trees** (excluding `.git/`). ✅ Fully compliant with Rule 1.25. |
| **Zero hardlinks** | **0 files with link count > 1** across all 9 org trees. ✅ |
| **No `zebes`/`ringmaster`/`spotlight`/`100.x.y.z` in `.oo`** | **Violations**, all listed in §7.8 (buildbox hardcodes; `ooaid` identifiers). The `100.64.0.0/10` hits in `openOODA-core/std/net/egress.oo:13,31` and `std/qa/probe_net_egress.oo:9-22` are legitimate RFC 6598 CGNAT constants, not host bindings. |
| **Zero C/Rust/Python fallbacks** | `openOODA-core/oodar` holds 208 `.c`/`.h` files — **this is the repo's declared product** (the host runtime ABI), not a wrapper. The genuine wrappers are `oodac/scripts/oodac_cluster.sh` (§7.9), `tui/mcp_client.oo:79` (§7.9), and — newly — `openOODA-apps/ooflash/flash/rawio.oo` (§3.1). `ooflash/lint-oo-size` is a `/bin/sh` linter, a build tool rather than a runtime fallback, but it diverges from the sibling convention where the same linter is inline in the Makefile. |
| **`catalog/index` vs disk drift** | **0 drift.** ✅ |
| **Repo name == shipped binary name** | Holds for **all** kernel, OS, DE, apps, cloud, agents repos. **Fails in `openOODA-core`**: `lsp` ships as `ooda-lsp`, `mcp` ships as both `mcp` and `ooda-mcp`. |

---

## 9. Recommended sequencing (first principles: ownership before archival)

The evidence points to one conclusion: **the fleet's problem is not bad names — it is that names have no single owner.** Renaming before ownership is settled would multiply the ambiguity. The order that removes ambiguity fastest:

1. **Publish an authoritative persona-ownership table** — one row per token, one column per candidate host, with a required single winner. Today there is no machine-readable registry for 13 of the 17 absorbing binaries (§4.5), and no tool can detect the 57 dual-host tokens automatically.
2. **Break the two mutual-claim cycles** — `oohash`↔`oob3sum` (§4.3) and `oobuild-fleet`↔`oodeploy` (§3.11). Nothing in either domain can be archived until these are broken.
3. **Arbitrate the 3-host tokens** — `oodns-cloud`/`dns` (`oogateway` vs `oomesh`) and `ooqueue`/`queue` (`oodb-dist` vs `oosched-cloud`).
4. **Archive the 20 unambiguous absorbed repos** (§5.2) and withdraw their standalone binaries. This removes 20 tokens from the ambiguity set with zero design risk.
5. **Archive the 20 catalog-exposed double-shipped tools** (§5.4) and withdraw their `catalog/index` entries. This is the step that fixes the **public** surface.
6. **Rename only after ownership is settled**, in this order: `ooflash` (done), `oooffice` (`oodocs`→`oooffice`, per RFC), `oocontainer` (`ooimage`), `oohostmon` (`oovm-ui`), `ooshell`+`oogrant` (DE), `oohal`/`ookernel`/`ooboot`/`oodrv-io` (kernel), `ooooda` (agents), `ooda-lsp`/`ooda-mcp` (core).
7. **Fix the contract documentation** — `website/llms.txt:35` (symlink dispatch + repo counts), `oodocs/README.md:54` (`ooffice`→`oooffice`), the 9 stale `ooagent-*` README lines, `oooda-engine/README.md:25,61` + `AGENTS.md:44,53`, and the reference to the non-existent `unix_consolidation_blueprint.md`.
8. **Replace the new `ooflash` subprocess shims with native `.oo`** — this is a Rule-1.25 regression introduced on 2026-11-05 and it should not survive into a release.
9. **Split `std` → `std` + `std-hw`**, and extract the shared app framework out of the 16 apps repos into an imported module.

---

## 10. Unknowns and risks (explicit)

1. **The tree mutated during this audit.** `ooflash` was created and populated 03:55–03:58 and the `oomedia` flash half was deleted ~03:59. Both states are reported. Any finding about `oomedia`'s current content should be re-verified before action.
2. **No binary was executed and no build was run.** Every assertion-count and parity claim is a *string* comparison between README and Makefile, not an observed test result. "Ready to archive" is judged from source/Makefile/persona-registry evidence, not from a green suite.
3. **Persona-table extraction is pattern-based.** Tokens were extracted from `== "…"` comparisons in persona dispatch files. A persona implemented through a data table rather than an equality chain would be missed. `cloud`/`agents` use `persona/meta.oo` id tables, which were included; `tools` uses `ipc/dispatch_persona.oo`, which was included.
4. **The `openOODA-tools` per-repo inventory was not read page-by-page.** The 257-repo consolidation map (§3.10) is established from the 8 persona tables, the `BIN` declarations, and RFC 0012 §2.3 — not from a full read of 257 READMEs. A tool whose README overclaims in the way `ooimage` does would need a targeted read to detect.
5. **`std/anchor.oo` vs `std/hw/anchor.oo`** may reflect an intentional re-layering that only one document was updated for. I cannot determine which is authoritative from the tree alone.
6. **The `ooagent-*` README lines may have been kept deliberately** for an external install script not present in these trees. I could not verify such a script exists.
7. **`/Projects/idlescreen`** exists alongside the 9 orgs and contains `spotlight`/`spotlights` strings in its ASCII-effect scenes (`idlescreen/idlescreen/ascii/effects.oo:14,35`, `ascii/scenes/orbit/spotlights.oo:3`). It is **outside the requested scope** and was not audited, but it should be noted: the `spotlight` literal rule, if applied repo-wide, would hit it.
8. **The `catalog/index` signature files** (`index.sig`, `index.minisig`, `registry.pub`) were confirmed to exist; their cryptographic coverage was not independently verified.

---

## 11. Bottom line

The naming vocabulary is in better shape than the naming **ownership**. Twenty repos are genuinely ready to archive with zero design risk. Twenty more are ready once an ownership table exists. Five canonical hosts and the catalog itself are already correct and should not be touched.

The single most consequential finding is that **20 signed, publicly installable package names are simultaneously persona tokens of other binaries**, and that **two pairs of binaries claim each other**. Until every token has exactly one owner, "one canonical binary per domain" is a stated intention rather than an enforced property — and the install surface will keep advertising binaries that the runtime also answers to.

*End of independent pass.*
