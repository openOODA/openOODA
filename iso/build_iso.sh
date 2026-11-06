#!/bin/bash
# ISO milestone-1 assembly: payload ELF + UEFI stub + ESP + ISO9660.
# Deterministic: SOURCE_DATE_EPOCH pinned, sorted copy order, fixed volume id.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
BLD="$HERE/build"
OODAC="${OODAC_BIN:-/Projects/openOODA-core/oodac/bin/oodac.real}"
NOSTD_A="${OODA_NOSTD_A:-/Projects/openOODA-core/oodar/scripts/lib/liboodar-nostd.a}"
OODAR_ROOT="${OODA_OODAR_ROOT:-/Projects/openOODA-core/oodar}"
export SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-946684800}"
export OODA_NO_JAIL=1
export OODA_FS_WRITEDIR="$BLD:$HERE"

mkdir -p "$BLD/efiroot/EFI/BOOT"
cd "$BLD"

echo "[1/4] payload: emit + freestanding link"
"$OODAC" check "$HERE/payload/app.oo" >/dev/null
OODA_LLVM_TRIPLE=x86_64-unknown-none "$OODAC" emit-llvm "$HERE/payload/app.oo" > "$BLD/app.ll"
clang --no-default-config --target=x86_64-unknown-none -fuse-ld=lld -static \
    -ffreestanding -nostdlib -fno-builtin -fno-stack-protector -Os -g0 \
    -fno-ident -ffunction-sections -fdata-sections \
    -fno-asynchronous-unwind-tables -fno-unwind-tables -Wno-override-module \
    -I"$OODAR_ROOT" "$HERE/payload/km_entry.c" "$BLD/app.ll" "$NOSTD_A" \
    -Wl,--build-id=none -Wl,--gc-sections -Wl,-z,noseparate-code \
    -Wl,-Ttext=0x1000000 -Wl,--strip-all -o "$BLD/payload.elf"

echo "[2/4] UEFI stub: pe32+ efi_application"
clang --no-default-config --target=x86_64-unknown-windows -ffreestanding \
    -fno-stack-protector -fno-builtin -Os -g0 -fno-ident -nostdlib \
    -fuse-ld=lld -Wl,-entry:efi_main -Wl,-subsystem:efi_application \
    -Wl,/debug:none -Wl,/timestamp:0 \
    "$HERE/efi/efi_stub.c" "$HERE/efi/kernel.S" -o "$BLD/BOOTX64.EFI"

echo "[3/4] ESP image + ISO9660 (eltorito, no-emulation)"
rm -f "$BLD/esp.img" "$BLD/ooda.iso"
# Determinism: --invariant pins FAT serial + dir timestamps to constants;
# -m preserves the source-file mtime (pinned to SOURCE_DATE_EPOCH) for files.
touch -d "@$SOURCE_DATE_EPOCH" "$BLD/BOOTX64.EFI" "$BLD/payload.elf"
mkfs.fat -C -F 12 --invariant -n OODAESP "$BLD/esp.img" 1440 >/dev/null
mmd -i "$BLD/esp.img" ::/EFI ::/EFI/BOOT
mcopy -m -i "$BLD/esp.img" "$BLD/BOOTX64.EFI" ::/EFI/BOOT/BOOTX64.EFI
mcopy -m -i "$BLD/esp.img" "$BLD/payload.elf" ::/KERNEL.ELF
rm -f "$BLD/efiroot/esp.img"
cp "$BLD/esp.img" "$BLD/efiroot/esp.img"
find "$BLD/efiroot" -exec touch -d "@$SOURCE_DATE_EPOCH" {} +
xorriso -as mkisofs -o "$BLD/ooda.iso" -R -J -V OODAISO \
    -A "openOODA milestone-1" \
    -eltorito-alt-boot -e /esp.img -no-emul-boot \
    "$BLD/efiroot" 2>/dev/null

echo "[4/4] artifacts"
ls -la "$BLD/ooda.iso" "$BLD/BOOTX64.EFI" "$BLD/payload.elf" "$BLD/esp.img"
sha256sum "$BLD/ooda.iso"
echo "BUILD-ISO OK"
