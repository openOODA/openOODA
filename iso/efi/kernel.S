// # ISO milestone-1 payload embed
//
// Logline: Embed the built kernel ELF in .rdata for efi_stub's loader.
// Setup: Assembled for x86_64-unknown-windows; path is relative to the
//        build working directory (build_iso.sh cds to iso/build/).
// Beats:
//   1. _kernel_start / _kernel_end bracket the embedded image.

    .section .rdata
    .globl _kernel_start
    .globl _kernel_end
_kernel_start:
    .incbin "payload.elf"
_kernel_end:
