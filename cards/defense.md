# defense.md — Active Cyber Defense & Hardware Boundaries Card (`ooda defense`)

1. **Active Cyber Defense & Deception (`openOODA-tools/oodefense` & `oostd/sec/defense/*`)**:
   - **`oodefense ids` & `canary`**: Kernel eBPF syscall/network anomaly detector (`kernel_ebpf_monitor.oo`) and zero-false-positive canary tripwires (`network_canary_tripwire.oo`).
   - **`oodefense honeypot`**: Decoy service & credential deception mesh (`deception_mesh.oo`) that isolates and fingerprints probing processes.
   - **`oodefense mutate-verify`**: Self-healing AST/code engine (`self_healing_code_engine.oo`) with cryptographically signed, hash-chained mutation logs.
   - **`oodefense sidechannel` & `airgap`**: Constant-time jitter injection (`side_channel_jitter_injector.oo`), covert-channel detection, and instant `NetCap=0` airgap lockdown.

2. **Zero-Trust Network Boundary (`openOODA-tools/oofirewall` & `openOODA-OS/oonetd`)**:
   - Per-badge (`badge8`) socket egress filtering, declarative `nft` zones, and post-quantum WireGuard (`ML-KEM-768` + ChaCha20-Poly1305) mesh tunnels.

3. **Hardware & Memory Defense Boundaries (`openOODA-kernel` & `openOODA-OS`)**:
   - **IOMMU DMA Bounce Guard (`ookernel/mm/dram_mct_guard.oo` & `oomodemd`)**: Untrusted PCIe/Thunderbolt/WWAN baseband DMA is restricted to isolated 4 KiB bounce pages (`MmioCap` + `DmaCap`).
   - **DRAM MCT Zeroization**: Cryptographic memory scrub on arena reset and page free.
   - **Locked-Screen USB Firewall (`oodrv-io/usb/usb_class_firewall.oo`)**: Blocks new USB HID/Storage/Network device admission while the session seat is locked.
