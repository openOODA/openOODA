/* ooboot efi_bridge.c — hardware + firmware primitives for the .oo loader.
 *
 * The loader logic (markers, ELF validation, phdr walk, entry) lives in
 * ooboot_main.oo; this file only supplies what .oo cannot express: the
 * debugcon sink, volatile loads, memcpy/memset, and the UEFI protocol
 * walk that reads KERNEL.ELF off the ESP. Signatures match the .oo ABI:
 * i64 scalars in, results via out ptr. No EFI headers — flat offsets. */

#include <stdint.h>

static void outb(uint16_t port, uint8_t v) {
    __asm__ volatile("outb %0, %1" :: "a"(v), "Nd"(port));
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

void oo_efi_jump(int64_t e) {
    ((void (*)(void))(uintptr_t)e)();
}

/* --- KERNEL.ELF read off the ESP via UEFI ----------------------------- */

typedef uint64_t efi_status_t;
typedef void *efi_handle_t;
typedef efi_status_t (*efi_handle_proto_t)(efi_handle_t, const uint8_t *,
                                         void **);
typedef efi_status_t (*efi_open_vol_t)(void *, void **);
typedef efi_status_t (*efi_file_open_t)(void *, void **, const uint16_t *,
                                        uint64_t, uint64_t);
typedef efi_status_t (*efi_file_read_t)(void *, uint64_t *, void *);
typedef efi_status_t (*efi_file_close_t)(void *);

/* x64 layout offsets (UEFI 2.x):
 *   EFI_SYSTEM_TABLE.BootServices            96
 *   EFI_BOOT_SERVICES.HandleProtocol        152
 *   EFI_LOADED_IMAGE.DeviceHandle            24
 *   EFI_SIMPLE_FILE_SYSTEM.OpenVolume         8
 *   EFI_FILE_PROTOCOL: Close 16, Read 32, Open 8 */
#define ST_BOOT_SERVICES 96
#define BS_HANDLE_PROTO 152
#define LI_DEVICE_HANDLE 24
#define SFS_OPEN_VOLUME 8
#define FP_OPEN 8
#define FP_CLOSE 16
#define FP_READ 32

static const uint8_t GUID_LOADED_IMAGE[16] = {
    0xa1, 0x31, 0x1b, 0x5b, 0x62, 0x95, 0xd2, 0x11,
    0x8e, 0x3f, 0x00, 0xa0, 0xc9, 0x69, 0x72, 0x3b
};
static const uint8_t GUID_SIMPLE_FS[16] = {
    0x22, 0x5b, 0x4e, 0x96, 0x59, 0x64, 0xd2, 0x11,
    0x8e, 0x39, 0x00, 0xa0, 0xc9, 0x69, 0x72, 0x3b
};

static uint8_t kbuf[2 * 1024 * 1024];
static int64_t ksrc_addr;

void oo_efi_init(int64_t img, int64_t st) {
    ksrc_addr = 0;
    uint8_t *bs = *(uint8_t **)(uintptr_t)(st + ST_BOOT_SERVICES);
    efi_handle_proto_t handle_proto =
        *(efi_handle_proto_t *)(uintptr_t)(bs + BS_HANDLE_PROTO);
    void *li = 0, *sfs = 0, *root = 0, *f = 0;
    if (handle_proto((efi_handle_t)(uintptr_t)img, GUID_LOADED_IMAGE, &li))
        return;
    uint8_t *dev = *(uint8_t **)(uintptr_t)(li + LI_DEVICE_HANDLE);
    if (handle_proto((efi_handle_t)(uintptr_t)dev, GUID_SIMPLE_FS, &sfs))
        return;
    efi_open_vol_t open_vol = *(efi_open_vol_t *)(uintptr_t)(sfs + SFS_OPEN_VOLUME);
    if (open_vol(sfs, &root)) return;
    static const uint16_t name[] = { 'K','E','R','N','E','L','.','E','L','F',0 };
    efi_file_open_t fopen = *(efi_file_open_t *)(uintptr_t)(root + FP_OPEN);
    if (fopen(root, &f, name, 1, 0)) return; /* EFI_FILE_MODE_READ */
    uint64_t size = sizeof(kbuf);
    efi_file_read_t fread = *(efi_file_read_t *)(uintptr_t)(f + FP_READ);
    if (!fread(f, &size, kbuf) && size > 0) ksrc_addr = (int64_t)(uintptr_t)kbuf;
    efi_file_close_t fclose = *(efi_file_close_t *)(uintptr_t)(f + FP_CLOSE);
    fclose(f);
}

void oo_efi_kernel_start(int64_t *out) {
    *out = ksrc_addr;
}

/* oodac emits this declare for every module; the freestanding profile has
 * no capability runtime, so the prologue is a no-op here. */
void oodar_cap_lock_prologue(int mask) { (void)mask; }
