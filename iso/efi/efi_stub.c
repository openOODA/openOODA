// # ISO milestone-1 UEFI stub + ELF64 loader
//
// Logline: efi_main emits the OOEFI debugcon marker, copies embedded PT_LOAD
//          segments of the milestone-1 kernel payload to their physical
//          addresses, and jumps to its entry point.
// Setup: Built for x86_64-unknown-windows (UEFI/PE MS ABI) with lld
//        -entry:efi_main -subsystem:efi_application. The kernel ELF is
//        embedded in .rdata by kernel.S via .incbin.
// Beats:
//   1. Marker OOEFI on firmware entry (proves OVMF loaded BOOTX64.EFI).
//   2. Validate ELF64 class/LE/machine and copy PT_LOAD segments identity.
//   3. Marker OOLOAD, jump to payload _start (no ExitBootServices in m1 —
//      the payload only touches I/O ports and its own image pages).
//
// Honest gap for milestone 2: ExitBootServices handshake + real memory-map
// ownership transfer before the jump (uefi_boot.oo models it).

typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef unsigned long long u64;

extern u8 _kernel_start;
extern u8 _kernel_end;

static void outb(u16 port, u8 val) {
    __asm__ volatile("outb %0, %1" :: "a"(val), "Nd"(port));
}

static void dbg(const char *s) {
    while (*s) {
        outb(0x402, (u8)*s);
        s++;
    }
}

// Returns the payload entry address, 0 on rejection.
static u64 elf_load(void) {
    u8 *img = &_kernel_start;
    if (img[0] != 0x7f || img[1] != 'E' || img[2] != 'L' || img[3] != 'F') return 0;
    if (img[4] != 2 || img[5] != 1) return 0;          // ELF64, little-endian
    if (*(u16 *)(img + 18) != 62) return 0;            // EM_X86_64
    u64 entry = *(u64 *)(img + 24);
    u64 phoff = *(u64 *)(img + 32);
    u16 phsz = *(u16 *)(img + 54);
    u16 phnum = *(u16 *)(img + 56);
    u16 i = 0;
    while (i < phnum) {
        u8 *ph = img + phoff + (u64)i * phsz;
        if (*(u32 *)ph == 1) {                          // PT_LOAD
            u64 off = *(u64 *)(ph + 8);
            u64 va = *(u64 *)(ph + 16);
            u64 fs = *(u64 *)(ph + 32);
            u64 ms = *(u64 *)(ph + 40);
            u8 *dst = (u8 *)va;
            u8 *src = img + off;
            u64 j = 0;
            while (j < fs) { dst[j] = src[j]; j++; }
            while (j < ms) { dst[j] = 0; j++; }
        }
        i++;
    }
    return entry;
}

int efi_main(void *image, void *systab) {
    (void)image; (void)systab;
    dbg("OOEFI\n");
    u64 entry = elf_load();
    if (entry == 0) {
        dbg("OOELF-FAIL\n");
        for (;;) { __asm__ volatile("hlt"); }
    }
    dbg("OOLOAD\n");
    ((void (*)(void))entry)();
    dbg("OOBACK\n");
    for (;;) { __asm__ volatile("hlt"); }
}
