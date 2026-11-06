/* ooboot efi_bridge.c — hardware primitives for the .oo UEFI loader.
 *
 * The loader logic (markers, ELF validation, phdr walk, entry) lives in
 * ooboot_main.oo; this file only supplies the raw operations .oo cannot
 * express: port I/O, raw memory loads/stores, blob bounds, and the final
 * jump. Signatures match the .oo ABI: i64 scalars in, results via out ptr. */

#include <stdint.h>

static void outb(uint16_t port, uint8_t v) {
    __asm__ volatile("outb %0, %1" :: "a"(v), "Nd"(port));
}
static uint8_t inb(uint16_t port) {
    uint8_t v;
    __asm__ volatile("inb %1, %0" : "=a"(v) : "Nd"(port));
    return v;
}

/* isa-debugcon (0x402) is what the OVMF/qemu harness taps; it is
 * write-through with no line-status register, so no THR-empty spin. */
#define DBGPORT 0x402

void oo_efi_putb(int64_t c) {
    outb(DBGPORT, (uint8_t)c);
}

void oo_efi_ld16(int64_t a, int64_t *out) {
    *out = *(volatile uint16_t *)(uintptr_t)a;
}
void oo_efi_ld32(int64_t a, int64_t *out) {
    *out = *(volatile uint32_t *)(uintptr_t)a;
}
void oo_efi_ld64(int64_t a, int64_t *out) {
    *out = *(volatile uint64_t *)(uintptr_t)a;
}

void oo_efi_memcpy(int64_t d, int64_t s, int64_t n) {
    uint8_t *dp = (uint8_t *)(uintptr_t)d;
    const uint8_t *sp = (const uint8_t *)(uintptr_t)s;
    for (int64_t i = 0; i < n; i++) dp[i] = sp[i];
}

void oo_efi_memset(int64_t d, int64_t v, int64_t n) {
    uint8_t *dp = (uint8_t *)(uintptr_t)d;
    for (int64_t i = 0; i < n; i++) dp[i] = (uint8_t)v;
}

extern const uint8_t kernel_start[];

void oo_efi_kernel_start(int64_t *out) {
    *out = (int64_t)(uintptr_t)kernel_start;
}

void oo_efi_jump(int64_t e) {
    ((void (*)(void))(uintptr_t)e)();
}

/* oodac emits this declare for every module; the freestanding profile has
 * no capability runtime, so the prologue is a no-op here. */
void oodar_cap_lock_prologue(int mask) { (void)mask; }
