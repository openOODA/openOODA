# defense.md — Active Cyber Defense & Hardware Boundaries Card (`ooda defense`)

1. **Active Cyber Defense & Deception (`@openOODA-system/ooda-firewall` & `ooda-standard/sec/defense/*`)**:
   - **`ooda-firewall ids` & `canary`**: Kernel eBPF syscall/network anomaly detector (`kernel_ebpf_monitor.oo`) and zero-false-positive canary tripwires (`network_canary_tripwire.oo`).
   - **`ooda-firewall honeypot`**: Decoy service & credential deception mesh (`deception_mesh.oo`) that isolates and fingerprints probing processes.
   - **`ooda-firewall mutate-verify`**: Self-healing AST/code engine (`self_healing_code_engine.oo`) with cryptographically signed, hash-chained mutation logs.
   - **`ooda-firewall sidechannel` & `airgap`**: Constant-time jitter injection (`side_channel_jitter_injector.oo`), covert-channel detection, and instant `NetCap=0` airgap lockdown.

2. **Zero-Trust Network Boundary (`@openOODA-system/ooda-firewall` & `ooda-network`)**:
   - Per-badge (`badge8`) socket egress filtering, declarative `nft` zones, and post-quantum WireGuard (`ML-KEM-768` + ChaCha20-Poly1305) mesh tunnels.

3. **Hardware & Memory Defense Boundaries (`@openOODA-system`)**:
   - **IOMMU DMA Bounce Guard (`ooda-kernel/mm/dram_mct_guard.oo` & `ooda-modem`)**: Untrusted PCIe/Thunderbolt/WWAN baseband DMA is restricted to isolated 4 KiB bounce pages (`MmioCap` + `DmaCap`).
   - **DRAM MCT Zeroization**: Cryptographic memory scrub on arena reset and page free.
   - **Locked-Screen USB Firewall (`ooda-drivers/io/usb_class_firewall.oo`)**: Blocks new USB HID/Storage/Network device admission while the session seat is locked.
