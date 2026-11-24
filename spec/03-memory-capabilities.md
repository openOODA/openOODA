# 03 — Ownership, Memory Hardening & Capability Security

> **Status:** Clean-break specification (`openOODA v3.2.0`).

## 1. Zero Ambient Authority (`CapReg64`)
Every privileged operation requires an explicit borrowed capability token (`&CapKind`) threaded from `main` — functions cannot forge ambient authority.

- **32 Root Capability Bits (`0..31`):**
  `0:NetCap` `1:FsReadCap` `2:FsWriteCap` `3:ProcessCap` `4:EnvCap` `5:TimeCap` `6:RandCap` `7:AllocCap`
  `8:ThreadCap` `9:GpuCap` `10:FfiCap` `11:MetricsCap` `12:SignCap` `13:BindCap` `14:CompilerReadCap`
  `15:ArenaCap` `16:FsCap` `17:TcpCap` `18:UdpCap` `19:SysCap` `20:AudioCap` `21:CameraCap` `22:UsbCap`
  `23:HidCap` `24:WindowCap` `25:FrameCap` `26:MmioCap` `27:DmaCap` `28:IrqCap` `29:PciCap` `30:BlockCap` `31:TpmCap`.
- **Upper 32 bits:** `16-bit OODA Epoch` + `8-bit Rights Mask` + `8-bit Scope Badge`.
- **Lexical Effect Handlers & OODA Phases:** `with_cap v: &Cap = eff_*(...) { ... }` attenuates scoped capabilities; Observe is read-only, Orient/Decide admit `ArenaCap`/`SignCap`, Act is unrestricted.
- **Information Flow:** Variables marked `// SECRET:` cannot flow into print, file, network, or process sinks.

## 2. Ownership, Borrowing & ARC Runtime Model
- Bindings are immutable (`let`) unless declared `let mut`; borrowed references (`&T`, `&mut T`, `@&T`) are checked for move-before-use and exclusive mutability via CFG/MIR dataflow `[Target: Phase 2]`.
- Owned heap values (`String`, `List[T]`, `Box[T]`) use deterministic ARC with split-counter biased refcounting (`rc_biased.oo`).
- **Hardened Allocator & ARC Fast Path `[Target: Phase 3]`:**
  - Static/immortal string literals carry a 1-bit tag skipping heap/span validation on retain/release.
  - Compact 16-byte slab headers, 16B/32B/64B slab classes, per-thread slab caches, XOR Safe-Linking free lists, `PROT_NONE` guard pages, zero-on-free, and generational thread-local `Arena` handles.
  - Violation traps invoke Bellare-Yee `AuditRing` and exit `126` (`[CAPABILITY TRAP]`).

## 3. Capability-Gated Bare-Metal Primitives `[Target: Phase 1]`
- Typed `static` / `static mut` globals replace untyped BSS slot indexing.
- `MmioPtr[T]` / `RawPtr[T]` require `&MmioCap` or `&DmaCap` and emit direct volatile loads/stores.
- Inline `asm!(...)` is strictly gated by `&SysCap` / `&DmaCap` / `--rt-substrate`.
