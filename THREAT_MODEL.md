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
| **Secret & Credential Exfiltration** | `Secret` taint tracking, `NO_SWAP \| NO_DUMP \| ZERO_ON_FREE` kernel pages, `@zeroize_frame` stack/register wipe, software-HSM `ooda-vault` (keys unmapped from apps), `Secret[ConfigKey]` (no ambient env dumps), and metadata-blind encrypted storage | Compile-time taint refusal tests, secret-pool/zeroize audits, `ooda-vault` HSM & storage tests |
| **Network & IPC Spoofing / Replay** | Universal `OodaTunnel` zero-negotiation fixed-width authenticated encrypted frames carrying `CapReg64` warrants and replay counters across IPC/storage/network boundaries | Crypto KATs (`X25519`, `ML-KEM-768`, `ML-DSA-65`, `SLH-DSA`, AEAD), tunnel replay refusal suites |
| **Crypto Misuse & Implementation Flaws** | Linear single-use `Nonce[Aead]`, purpose/algorithm-typed `Key[Purpose, Alg]`, AEAD-only decryption (no unauthenticated/ECB/CBC APIs), hedged deterministic+HW-RNG crypto, `QuorumWarrant` threshold signing, and crypto agility by subtraction (no weak primitives linked) | Nonce-reuse/key-confusion compile refusals, threshold-signing tests, binary symbol audit |
| **Confused-Deputy & Prompt / Command Injection** | Dual-polarity `Untrusted[T]` integrity taint + OODA phase separation forcing explicit validation/declassification or signed `Warrant` before reaching `act_*`/`ProcessCap`/`FsWriteCap` (Phase 2.4) | Compile-time IFC taint refusal tests & capability confinement suites |
| **Path Traversal, SSRF, Shell Injection & Writable Exec** | Directory-rooted `RelPath` (`FsCap`), peer/CIDR-scoped `NetCap`, no `fork()` or shell-string `exec()` (explicit `spawn(SignedExecCap, ...)` only), and kernel VFS Code/Data separation (`FsWriteCap` data never executable) | Refusal suites, Ring-3 VFS `SignedExecCap` & peer-allowlist confinement tests |
| **Cryptographic Timing, PMU Side Channels & PQ Breaks** | Compiler-enforced `@const_time` (no `Secret` branches, table lookups, var-time ALU, or unbucketed allocs), capability-gated high-res timers/PMUs (`PerfCap`/`RawTimerCap`), hybrid `X25519 + ML-KEM-768` + continuous `OodaTunnel` ratcheting, hash-based `SLH-DSA` root signatures, and `&NetCap`-only TLS/ASN.1 translators | Compiled-binary `ct_dudect` CI gate, hybrid/SLH-DSA KATs, perimeter confinement suites |
| **Long-Lived Credentials, Parser DoS, Clock Jumps & Backdoors** | Time-bounded epoch-revocable `CapReg64` leases, fuel-bounded `Untrusted[Bytes]` arenas, incompatible `MonotonicInstant` vs `WallUtc` types, deterministic capability replay + concurrency scheduler, and Diverse Double-Compiling (`DDC`) bootstrap proof | Lease/fuel/clock/replay suites, deterministic concurrency CI, DDC fixed-point build gate |
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
