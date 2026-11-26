# Security Policy

## Central Public Reporting & Scope

All `openOODA-*` component repositories (`@openOODA-core`, `@openOODA-system`, `@openOODA-apps`, `@openOODA-games`) are currently **private**. **This repository (`openOODA/openOODA`) is the sole public entry point for the entire openOODA ecosystem.**

Please report vulnerabilities affecting any component — `ooda-compiler`, `ooda-runtime`, `ooda-standard`, `ooda-kernel`, `ooda-boot`, `ooda-drivers`, `ooda-sign`, `ooda-package`, `catalog`, `install`, applications, or specifications — directly through `openOODA/openOODA`.

## Reporting a Vulnerability (Private Disclosure)

**Do NOT open a public GitHub Issue or Discussion for an unpatched security vulnerability.**

Submit confidential vulnerability reports using **GitHub Private Security Advisories**:

- **Private Security Advisory:** https://github.com/openOODA/openOODA/security/advisories/new

Please include:
1. Affected component(s), version/tag, and target triple (`x86_64-linux`, `x86_64-openooda`, `uefi`, `wasm32`, etc.).
2. Minimal reproducible `.oo` source, binary flag combination, or kernel/IPC input.
3. Security impact (e.g., capability bypass, ambient authority leak, `Secret` taint sink bypass, memory corruption, privilege escalation, cryptographic flaw, or build/catalog signature bypass).
4. Optional suggested fix or mitigation.

## Public Issues & Security Design Discussions

- **Non-sensitive bugs & feature requests:** https://github.com/openOODA/openOODA/issues
- **Architecture & security model questions:** https://github.com/openOODA/openOODA/discussions

## Coordinated Disclosure & Safe Harbor

- **Response Target:** Acknowledgment within **72 hours**, triage and severity assessment within **7 days**.
- **Coordinated Disclosure:** We ask for up to **90 days** to release a verified fix across affected packages and signed `SHA256SUMS` / `catalog` entries before public disclosure (shorter timelines coordinated when active exploitation exists).
- **Safe Harbor:** Good-faith security research, fuzzing, reverse-engineering, and vulnerability reporting conducted against your own builds/instances and disclosed privately via this policy are welcomed and encouraged.

See [`THREAT_MODEL.md`](THREAT_MODEL.md) for explicit security guarantees, assumptions, and out-of-scope boundaries.
