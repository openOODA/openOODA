#!/bin/bash
# ISO milestone-2 gate: OVMF boots the ISO, serial markers assert the chain
# OVMF -> BOOTX64.EFI (OOEFI) -> ELF load (OOLOAD) -> _start (OOBM1)
# -> main -> OOMAIN-OK. Plus negative (corrupt ESP) and determinism checks.
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
BLD="$HERE/build"
OVMF="${OVMF_CODE:-/usr/share/edk2/ovmf/OVMF_CODE_4M.qcow2}"
ISO="${1:-$BLD/ooda.iso}"
TIMEOUT="${ISO_TIMEOUT:-25}"

boot_marker() {  # $1=iso-path $2=log-path
    rm -f "$2"
    timeout "$TIMEOUT" qemu-kvm \
        -drive if=pflash,format=qcow2,readonly=on,file="$OVMF" \
        -cdrom "$1" -m 256 -nographic -no-reboot \
        -device isa-debugcon,iobase=0x402,chardev=dbg \
        -chardev file,id=dbg,path="$2" >/dev/null 2>&1
    true
}

expect_marker() {  # $1=log $2=marker
    grep -q "$2" "$1" || { echo "FAIL: missing marker $2"; cat "$1"; exit 1; }
}

echo "=== ISO milestone-2 boot gate ==="
[ -f "$ISO" ] || { echo "FAIL: no ISO at $ISO (run build_iso.sh)"; exit 1; }
[ -f "$OVMF" ] || { echo "FAIL: no OVMF at $OVMF"; exit 1; }

boot_marker "$ISO" "$BLD/boot.log"
for m in OOEFI OOLOAD OOBM1 OOMAIN-OK; do expect_marker "$BLD/boot.log" "$m"; done
echo "PASS: markers $(grep -o 'OO[A-Z1-]*' "$BLD/boot.log" | tr '\n' ' ')"

echo "--- negative: corrupt BOOTX64.EFI never reaches the markers"
cp "$BLD/esp.img" "$BLD/esp_bad.img"
printf 'NOPE-NOT-AN-EFI-APP' > "$BLD/junk.efi"
mcopy -o -i "$BLD/esp_bad.img" "$BLD/junk.efi" ::/EFI/BOOT/BOOTX64.EFI
rm -rf "$BLD/badroot" && mkdir -p "$BLD/badroot" && cp "$BLD/esp_bad.img" "$BLD/badroot/esp.img"
xorriso -as mkisofs -o "$BLD/bad.iso" -R -J -V OODABAD \
    -eltorito-alt-boot -e /esp.img -no-emul-boot \
    "$BLD/badroot" 2>/dev/null
boot_marker "$BLD/bad.iso" "$BLD/bad.log"
grep -q "OOMAIN-OK" "$BLD/bad.log" && { echo "FAIL: corrupt image booted"; cat "$BLD/bad.log" | tail -5; exit 1; }
echo "PASS: negative case refused"

echo "--- determinism: rebuild and compare"
H1=$(sha256sum "$ISO" | cut -d' ' -f1)
"$HERE/build_iso.sh" >/dev/null
H2=$(sha256sum "$BLD/ooda.iso" | cut -d' ' -f1)
[ "$H1" = "$H2" ] || { echo "FAIL: iso not deterministic ($H1 != $H2)"; exit 1; }
echo "PASS: deterministic iso $H1"

echo "ALL ISO GATE CHECKS PASSED"
