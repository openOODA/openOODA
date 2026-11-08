# security.md — Zero-Trust & 32 Capabilities Quick Card (`ooda security`)

1. **Zero Ambient Authority & `CapReg64` (`32 + 32 = 64` bits)**:
   - Lower 32 bits = Root Capability Mask (`0..31`, matching a 32-lane GPU warp):
     `0:NetCap` `1:FsReadCap` `2:FsWriteCap` `3:ProcessCap` `4:EnvCap` `5:TimeCap` `6:RandCap` `7:AllocCap`
     `8:ThreadCap` `9:GpuCap` `10:FfiCap` `11:MetricsCap` `12:SignCap` `13:BindCap` `14:CompilerReadCap`
     `15:ArenaCap` `16:FsCap` `17:TcpCap` `18:UdpCap` `19:SysCap` `20:AudioCap` `21:CameraCap` `22:UsbCap`
     `23:HidCap` `24:WindowCap` `25:FrameCap` `26:MmioCap` `27:DmaCap` `28:IrqCap` `29:PciCap` `30:BlockCap` `31:TpmCap`.
   - Upper 32 bits = `16-bit OODA Epoch` + `8-bit Rights Mask` + `8-bit Scope Badge`.
   - Functions receive borrowed capability tokens (`&FsReadCap`) from `main` and attenuate child masks before delegation.

2. **Canonical Security Hosts (`openOODA-tools`)**:
   - **`oosandbox`**: Capability + Landlock + seccomp-BPF + cgroupv2 containment (`run`, `landlock`, `seccomp`, `cgroup`, `limits`, `cap`, `policy`).
   - **`oosign`**: Post-quantum (`ML-KEM-768`, `ML-DSA-65`), Ed25519, X.509/mTLS, and ZK proof verification (`sign`, `verify`, `keygen`, `token`, `ssl`, `pqc`, `zk`).
   - **`ooprovenance`**: Hardware TPM2/SEV-SNP quotes, Stage0 256-byte `hex0` seed (`elf_init_array_cnt == 0`), Diverse Double-Compilation (`oo_ddc_seal_gated`), IMA, and Merkle audit logs.
   - **`oovault`**: Hardware-sealed secret store (`TpmCap`), FIDO2, Shamir secret sharing, and verified zeroization (`shred`).
