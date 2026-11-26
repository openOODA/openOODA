# openOODA Threat Model

This document defines what openOODA is engineered to defeat, what it explicitly assumes, and where security boundaries lie. Detailed architecture and active hardening milestones live in [`ROADMAP.md`](ROADMAP.md) and [`cards/security.md`](cards/security.md).

## Public Feedback Routing

All `openOODA-*` component repositories remain **private**. Send all public feedback strictly to `openOODA/openOODA`:
- **Vulnerability reports (private):** https://github.com/openOODA/openOODA/security/advisories/new (see [`SECURITY.md`](SECURITY.md))
- **Threat-model feedback & design questions:** https://github.com/openOODA/openOODA/discussions
- **Non-sensitive defects:** https://github.com/openOODA/openOODA/issues

---

## Security Guarantees & Mitigations (In-Scope)

| Threat Class | Mechanism in openOODA | Verification / Gate |
| :--- | :--- | :--- |
| **Ambient Authority & Privilege Escalation** | Explicit `&*Cap` / `&mut *Cap` borrow-checked capability tokens (`CapReg64`), `with_cap` attenuation, zero ambient globals, fail-closed `ooda-container` / Landlock confinement | Compile-time capability checker (`ooda-compiler`), Ring-3 syscall capability trap (`ooda-kernel`), refusal test suites |
| **Memory Corruption & Bounds Violations** | Linear ownership, deterministic ARC with 0-leak verification (`OODA_LEAK_CHECK=1`), Safe-Linking guarded slabs, QF_LIA SMT bounds checks, `W^X` page tables + unmapped stack guard pages (Phase 6.4) | Negative compiler tests, `OODA_LEAK_CHECK=1`, ASan/valgrind/runtime trap suites |
| **Secret & Credential Exfiltration** | `Secret` taint type tracking across borrows and sinks, refusing accidental printing/logging/network emission, explicit zeroization (`SECRET:` zeroization) | Compile-time taint refusal tests + `ooda-vault` PII scrubbing |
| **Network & IPC Spoofing / Replay** | Universal `OodaTunnel` zero-negotiation fixed-width authenticated encrypted frames carrying `CapReg64` warrants and replay counters across IPC/storage/network boundaries | Crypto KATs (`X25519`, `ML-KEM-768`, `ML-DSA-65`, `SLH-DSA`, AEAD), tunnel replay refusal suites |
| **Confused-Deputy & Prompt / Command Injection** | Dual-polarity `Untrusted[T]` integrity taint + OODA phase separation forcing explicit validation/declassification or signed `Warrant` before reaching `act_*`/`ProcessCap`/`FsWriteCap` (Phase 2.4) | Compile-time IFC taint refusal tests & capability confinement suites |
| **Cryptographic Timing Side Channels & Single-Assumption PQ Breaks** | Compiler-enforced `@const_time` (`Secret` branch & secret-indexed load ban), hybrid `X25519 + ML-KEM-768` + continuous `OodaTunnel` ratcheting, hash-based `SLH-DSA` (FIPS 205) root signatures, and zero-privilege `&NetCap`-only TLS/ASN.1 perimeter translators | Compiled-binary `ct_dudect` CI gate, hybrid/SLH-DSA KATs, perimeter confinement suites |
| **Long-Lived Credential Abuse & Compiler Backdoors** | Time-bounded epoch-revocable `CapReg64` leases (Phase 6.5), deterministic capability-input flight recording for offline replay (Phase 3.9), and Diverse Double-Compiling (`DDC`) bootstrap proof (Phase 4.7) | Lease expiry/revocation tests, deterministic replay suites, DDC fixed-point build gate |
| **Malicious DMA & Physical DRAM Snooping** | IOMMU DMA bounce-page lockdown (`ooda-drivers`/`ooda-hardware`), hardware DRAM encryption enablement (AMD SME/SEV, Intel TME/MKTME) | Kernel boot checks & device isolation suites |
| **Cross-Domain Speculative Side Channels** | `IBPB` / predictor barriers on Ring-3 context switches across untrusted domains (Phase 6.5) | Kernel domain-switch verification |
| **Supply-Chain Tampering & Non-Reproducible Builds** | Zero third-party dependencies, `S1 == S2` byte-identical fixed-point compiler self-hosting, signed `ooda-catalog` / `SHA256SUMS` / `ooda-sign`, measured & verified boot (`UEFI -> ooda-boot -> ooda-kernel -> Merkle rootfs` via `TpmCap` + `ooda-sign`) | Fixed-point determinism (`make det`), `catalog verify`, signed SPDX SBOM (Phase 6.3) |

---

## Trust Assumptions & Out-of-Scope Boundaries

Security depends on clear boundaries. openOODA **assumes** and treats the following as outside software-only defense unless paired with hardware/operational controls:

1. **Silicon & Firmware Root of Trust:** Correct hardware behavior of the CPU, MMU, IOMMU, hardware RNG, TPM 2.0 / DICE / Caliptra root-of-trust, and immutable UEFI firmware prior to `ooda-boot`.
2. **Hosted OS Kernel Integrity (Non-Native Builds):** When running openOODA tools hosted on Linux, Windows, or macOS instead of native `ooda-kernel`, host kernel compromises sit below the openOODA userspace/Landlock boundary.
3. **Physical Possession & Invasive Hardware Attacks:** Decapping chips, laser fault injection, or unencrypted bus probing on systems without SME/SEV/TME/MKTME or physical tamper controls.
4. **Authorized Operator Intent / Misconfiguration:** An operator intentionally granting an overly broad capability bundle (`FsWriteCap`, `NetCap`, `RawPtrCap`) or running an `unsafe` / `extern "C"` boundary without sandboxing.
5. **Pre-1.0 Clean-Break Evolution:** While openOODA is in `0.x` active hardening (`ROADMAP.md`), language/syscall ABIs evolve with clean breaks prior to `1.0` freeze.
