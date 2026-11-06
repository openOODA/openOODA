// # ISO milestone-2 payload embed
//
// Logline: Embed the built kernel ELF in .rdata for the ooboot loader.
// Setup: Assembled for x86_64-unknown-windows; path is relative to the
//        build working directory (build_iso.sh cds to iso/build/).
//        COFF x64 symbols carry no leading underscore.
// Beats:
//   1. kernel_start / kernel_end bracket the embedded image.

    .section .rdata
    .globl kernel_start
    .globl kernel_end
kernel_start:
    .incbin "payload.elf"
kernel_end:
