# ISO-PLAN.md — Bootable ISO Workstream Recon & Plan

Scope: ooda-os bootable ISO per northstar.oot §1.1 (UEFI `ooboot`, `ookernel`
microkernel, ring-3 drivers). Recon only — no code shipped in this doc.
Sources surveyed: ookernel-boot, ookernel-sched, ooinit, oodrv-display-gop,
openOODA-core/oodac (emit targets + link recipe proven in-flight).

## 1. Inventory — real boot-chain pieces that exist today

### ookernel-boot/  (northstar: UEFI `ooboot`, 16 .oo pages)
| page | role | boot-relevant? |
|---|---|---|
| `core/uefi_boot.oo` | efi_main entry shapes, GopFramebuffer, EfiMemoryDescriptor, UefiArchBridge (x86_64/aarch64/riscv64), ExitBootServices handshake | YES — the handover contract |
| `core/elf_loader.oo` | ELF64 PT_LOAD parser + segment pinning under FrameCap/DmaCap/TpmCap | YES — kernel loader |
| `core/boot_proto.oo` | boot protocol descriptor structs | YES — ooboot→kernel ABI |
| `core/acpi_madt.oo` | ACPI MADT table walk | YES — CPU/APIC enumeration |
| `bootenv/boot_env.oo` | A/B slot environment + reg64 gate | later (OTA) |
| `relink/boot_relink.oo` | kernel KASLR relink model | later |
| `fs/fsprobe.oo`, `fs/manifest.oo` | ESP/manifest probing model | YES (media discovery) |
| `ota/slot_swap_revert.oo`, `theme/ootheme.oo` | OTA, theme | no |
| `main.oo`, `dispatch.oo`, `anchor.oo`, `tests/` | hosted CLI + 31-assert self-test | hosted shell only |

Honest status: these pages model the boot chain as pure functions verified
under the hosted test harness. Nothing yet emits as a real firmware entry —
`efi_main` shapes exist but no produced artifact ever runs at firmware.

### ookernel-sched/  (northstar: `ookernel`, 40+ .oo pages)
`main.oo` is "CLI & Self-Test Entrypoint" (ProcessCap/FsReadCap hosted model).
Machinery present: CSpace/CDT, badged IPC endpoints, W^X MMU/IOMMU pinning,
EEVDF sched, upcall queues, micro-VM trace probe. No bare-metal `kmain`,
no vector table / trap entry, no serial console bring-up.

### ooinit (openOODA-OS, 41 .oo pages)
Hosted multi-call daemon: init/service/probe personas on ProcessCap/FsReadCap.
It is a userspace root-process CANDIDATE for the image, but every capability
token is host-syscall-bound — it cannot execute on bare metal until a syscall
shim or nostd profile exists for it. Keep userspace out of milestone 1.

### oodrv-display-gop
GOP driver model pages (cap/parse/ring/table) — matches the framebuffer the
UEFI loader discovers. Model-level today.

### Proven substrate (this week, github master)
- `oodac`: `--target x86_64-none-elf|riscv64-none-elf|aarch64-none-elf` admit +
  map to `*-unknown-*` triples; `cli_target_freestanding` selects the profile.
- `cli_build.oo` bare recipe: `clang --target=<triple> -fuse-ld=lld -static
  -ffreestanding -nostdlib @rsp liboodar-nostd*.a` → static ET_EXEC.
- `oodar`: `liboodar-nostd{,-riscv64,-aarch64}.a` — weak `_start`→`main`→
  `oo_nostd_abort`, `oodar_cap_lock_prologue`, 16550 UART sink+source,
  bump arena, MMIO accessors. Pattern-rule matrix ready for more arches.
- `emit/pe/` backend exists in oodac (`--backend pe`, PE32+ emission) —
  currently subsystem=console for Windows, not EFI_APPLICATION.

### Host tooling present on this box
`qemu-kvm`, `qemu-system-x86_64`, `xorriso`, `mkisofs`,
`/usr/share/edk2/ovmf/OVMF_CODE*.fd` (OVMF UEFI firmware), `ld.lld`, `clang 23`.

## 2. Gap list — to a bootable ISO

1. **Kernel entry**: no `_start`-family kernel entry consuming the ooboot
   handover. Needed: `kmain(boot_proto)` convention — `_start` (or a PE entry)
   reads framebuffer+memmap+descriptor pointer instead of `main(0,NULL)`.
   Smallest honest slice: kernel binary that UARTs "ookernel alive" and halts.
2. **UEFI app emission**: two candidate paths —
   a. `--backend pe` variant with EFI subsystem (pe_hdr emits subsystem console
      today; EFI_APPLICATION=10 needed, plus efi_main entry name);
   b. freestanding ELF + `objcopy`→PE is uglier but zero new emit code.
   Recommend (a): one-subsystem switch in pe lane is smaller than a new format.
3. **ESP/rootfs packaging**: nothing builds the FAT ESP (`/EFI/BOOT/BOOTX64.EFI`)
   or assembles the ISO. xorriso is installed; mtools/mformat NOT confirmed —
   check for mkfs.fat/genimage, else xorriso can embed an ESP image directly.
4. **ooboot realness gap**: today ooboot binary is the hosted self-test
   multi-call persona. Milestone 1 ISO can boot the *proven* freestanding
   binary instead of waiting for a real efi_main — decision point (§3.2).
5. **Userspace**: ooinit + services are hosted-capability-bound. First ISO
   has NO ring-3 payload; adding one is a later milestone needing a syscall
   ABI or a nostd-lowered init.
6. **Determinism**: ISO image bytes vary (ISO9660 timestamps, GPT GUIDs) —
   recipe must pin SOURCE_DATE_EPOCH + fixed volume IDs to keep the
   double-run determinism law.

## 3. Sketched build recipe + test plan

### 3.1 Bootloader choice
Northstar §1.1 line 36 declares **UEFI `ooboot`** — OVMF is on the box, and
the PE backend is one subsystem field away from EFI. **Reject limine**:
it would add a foreign GPL loader + second protocol surface; the house path
is already the UEFI app route (pe backend + uefi_boot.oo structures).

### 3.2 Milestone 1 (minimal honest ISO)
```
oodac build --target x86_64-none-elf metal/kmain_min.oo -o BOOTX64_PAYLOAD.elf
# kernel payload: emits UART "ookernel alive" then halts (weak _start path)
oodac build --backend pe  uefi_stub.oo      -o BOOTX64.EFI   # gap 2: EFI subsystem
mformat -i esp.img -C -F ::  BOOTX64.EFI BOOTX64_PAYLOAD.elf # or xorriso ESP embed
xorrisofs -o ooda.iso -e esp.img -no-emul-boot \
          -V OODAISO -set_date 2000-01-01T00:00:00Z iso_root/
```
ISO layout: eltorito no-emulation boot with ESP image; kernel payload sits on
the ESP as a data file the stub loads, OR statically inside the UEFI app for
milestone 1 (loader is real in a later milestone).

### 3.3 qemu-kvm test plan
```
qemu-kvm -bios /usr/share/edk2/ovmf/OVMF_CODE.fd -cdrom ooda.iso \
         -nographic -serial file:serial.log -no-reboot
# assert: serial.log contains the UART boot marker; exit after marker or
# timeout=60s → FAIL. Negative: corrupt BOOTX64.EFI → OVMF shell, marker absent.
# Determinism: two iso builds → sha256 equal.
```

### 3.4 Ordered work items (proposed; owner pane = kernel-lane)
1. oodac pe backend: `subsystem` selectable console→efi-app (pe_hdr + cli flag).
2. `metal/` dir in ooboot: `kmain_min.oo` freestanding payload page (UART hello).
3. `iso/` script dir in ooda-os repo: esp.img + xorriso assembly recipe.
4. qemu-kvm OVMF test harness + negative case + determinism check.
5. (later) real efi_main ooboot replacing the stub; ELF loader path; userspace.

## 4. Risks
- pe backend is a spike lane (foreign commits in flight) — coordinate the EFI
  subsystem switch with that lane or keep milestone 1 on freestanding ELF.
- `efi_main` ABI (MS x64 calling convention on real firmware) ≠ SysV — the
  uefi_boot.oo bridge models this; a stub app dodges it for milestone 1.
- xen/kvm availability on this box is unverified beyond binary presence —
  first harness run should smoke `qemu-kvm -version` + OVMF path existence.

## 5. Rollback / honesty notes
- ISO-PLAN.md itself is the only artifact this workstream produced; the
  container dir /Projects/openOODA-kernel has no .git, so the canonical copy
  is committed to openOODA/openOODA (spec repo) and mirrored here.
- No kernel/loader code is claimed working on firmware — the plan's milestone
  1 keeps the proven freestanding link as its only execution dependency.
