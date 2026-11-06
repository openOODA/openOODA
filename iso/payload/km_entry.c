// # ISO milestone-1 kernel entry glue (freestanding, x86_64)
//
// Logline: Strong _start for the bare-metal kernel payload — emits the
//          OOBOOT/OOMAIN-OK markers over the isa-debugcon port, runs the
//          emitted main, halts.
// Setup: Linked before liboodar-nostd.a so this strong _start overrides the
//        weak archive entry. 0x402 is the qemu isa-debugcon iobase.
// Beats:
//   1. Marker OOBM1 on entry (proves firmware->kernel handover landed).
//   2. Call emitted main(0,NULL), then marker OOMAIN-OK on return.
//   3. hlt loop — no return path exists on bare metal.

#include "oodar_nostd.h"

extern int main(int argc, char **argv);

static void dbg(const char *s) {
    while (*s) {
        oo_nostd_outb8(0x402, (uint8_t)*s);
        s++;
    }
}

#if defined(__GNUC__) || defined(__clang__)
__attribute__((noreturn))
#endif
void _start(void) {
    dbg("OOBM1\n");
    (void)main(0, (char **)0);
    dbg("OOMAIN-OK\n");
    for (;;) {
#if defined(__x86_64__) || defined(__i386__)
        __asm__ volatile("hlt");
#endif
    }
}
