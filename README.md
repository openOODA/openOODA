<div align="center">

<pre>
   ____  ____  ___  ____    ___   ___  ____    _
  / __ \/ __ \/ _ \/ __ \  / _ \ / _ \|  _ \  / \
 / /_/ / /_/ /  __/ / / / | | | | | | | | | |/ _ \
/_____/ .___/\___/_/ /_/  | |_| | |_| | |_| / ___ \
      /_/                   \___/ \___/|____/_/   \_\
</pre>

### openOODA — Capability-Secure Computing Stack (L0–L7)

[openooda.org](https://openooda.org) • [@openOODA](https://github.com/openOODA)

</div>

---

## About openOODA

**openOODA** is an AI-native, capability-secured, fail-closed computing stack built from first principles across eight unified layers (`L0`–`L7`).

In conventional systems, imported libraries and autonomous routines inherit the full ambient privileges of the user running the process. **openOODA** eliminates ambient authority across the entire stack: every external effect requires an explicit capability verified at compile time and enforced at runtime by hardware and kernel isolation boundaries.

At its core, **openOODA** fuses three paradigms into a single computing substrate:
- **Systems & OS Engineering (Linux/Unix Heritage)**: Bare-metal capability microkernel, Landlock and IOMMU hardware isolation, zero-root system services, deterministic linear-arena memory, and composable userland tools.
- **Single-Cycle 64-Bit Capability Architecture (`32 + 32 = 64`)**: Making full use of every 64-bit CPU clock cycle—the **lower 32 bits (`WHAT`)** encode all **32 Root Capabilities** (`13` Hardware + `19` Software/OS, fitting natively into a 32-lane GPU warp mask and a 32-bit seccomp-BPF accumulator), while the **upper 32 bits (`HOW & WHEN`)** pack a **16-bit OODA Epoch** (instant revocation) + **8-bit Rights Mask** (`R/W/X/Delegate/Revoke`) + **8-bit Scope Badge**.
- **Cryptographic Authority & Provenance (At Silicon Speed)**: Bearer capabilities governed by conservation of authority and monotonic attenuation, Merkle-DAG AST and build provenance, post-quantum warrants, and strict resource quotas—operating at compile-time and single-cycle CPU/GPU speed without blockchain consensus latency.
- **Autonomous AI (Closed-Loop OODA & Adversarial Falsification)**: Bounded Observe–Orient–Decide–Act engines and formal verification workflows where autonomous loops synthesize, audit, and falsify software inside provable capability budgets.

## The Unified 8-Layer Architecture (`L0`–`L7`)

| Layer | Domain | Architectural Focus |
| :--- | :--- | :--- |
| **Root (`@openOODA`)** | **Umbrella & Portal** | Architectural specifications, governance standards, installer, and package catalog ([openooda.org](https://openooda.org)) |
| **Layer 0 (`L0`)** | **Core Language & Toolchain** | Capability-secure systems language, self-hosting native compiler, deterministic standard library, and developer tooling |
| **Layer 1 (`L1`)** | **Microkernel & Drivers** | Capability microkernel, hardware abstraction layers, IOMMU DMA isolation, and user-space device drivers |
| **Layer 2 (`L2`)** | **Zero-Root Operating System** | Least-privilege system services, capability filesystems, networking stack, and isolated compatibility realms |
| **Layer 3 (`L3`)** | **Userland Toolchain** | Capability-scoped command-line utilities, structured data pipelines, and system inspection tools |
| **Layer 4 (`L4`)** | **Desktop Environment** | Capability compositor, spatial window management, interactive privacy portals, and visual authority indicators |
| **Layer 5 (`L5`)** | **Native Applications** | Productivity, creative, communication, and engineering applications with zero ambient tracking |
| **Layer 6 (`L6`)** | **Distributed Cloud Grid** | Content-addressed storage, encrypted mesh networking, cluster scheduling, and distributed compute |
| **Layer 7 (`L7`)** | **Autonomous OODA Loops** | Capability-bounded Observe–Orient–Decide–Act engines, formal verification workflows, and fleet governance |
