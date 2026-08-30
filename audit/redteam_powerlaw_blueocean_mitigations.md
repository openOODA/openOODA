# Power Law & Blue Ocean Mitigations: openOODA

## 1. Executive Summary

This document specifies the Power Law (80/20) architectural leverage points for openOODA.
Four core hubs dictate 80% of system stability, build velocity, and security.
The architecture introduces Blue Ocean innovations that eliminate operational friction.
It formalizes capability contracts, fail-closed state machines, and a phased migration plan.

---

## 2. The Four 20% Systems Leverage Hubs

| Hub | Exact File Path | Structural Impact |
| :--- | :--- | :--- |
| **1. Canonical Grammar** | `ooda/ooda.ebnf` | Governs 100% of parser lowering, AST construction, and LSP semantic tokens. |
| **2. Capability Checker** | `ooda/oodac/check_caps.oo` | Enforces zero ambient authority and Landlock sandbox boundaries at compile time. |
| **3. Pure ISA Emitter** | `ooda/oodac/x86_ssa_compile.oo` | Synthesizes native ELF machine code directly in sub-second build loops (<1s). |
| **4. Master Rule Enforcer** | `openOODA/scripts/enforcer.oo` | Enforces the 256-line limit, header compliance, and zero-cheat invariants. |

---

## 3. Blue Ocean Architectural Innovations

### 3.1 Zero Ambient Authority as a Language Primitive
Traditional systems rely on heavyweight container virtualization (Docker or Firejail).
These containers add multi-second startup latency.
The openOODA ecosystem enforces capability security directly in the type system.
Functions declare unforgeable capability tokens (`&FsReadCap`, `&NetCap`, `&AllocCap`).
Unprivileged code cannot access operating system resources without explicit tokens.

### 3.2 Deterministic Dual-Run Replay Verification
Every verification harness executes twice in fresh processes.
The framework compares output digests between runs.
If $\Delta H \ne 0$, the build system rejects the artifact.
This invariant guarantees that state drift remains mathematically impossible.

### 3.3 Autonomic Self-Healing Memory (RASP)
Runtime Application Self-Protection monitors active memory segments.
A background watchdog compares process memory against sealed Gold Master digests.
If tampering occurs, the runtime executes autonomic in-memory rollback.

---

## 4. Formal Capability Lattice Contracts

The security architecture structures capabilities as a bounded lattice:
$$\bot < \text{AllocCap} < \text{FsReadCap} < \text{FsWriteCap} < \text{NetCap} < \text{SysCap} = \top$$

```
                   [SysCap] (Bitmask 32)
                      ▲
                      │
                   [NetCap] (Bitmask 16)
                      ▲
                      │
                [FsWriteCap] (Bitmask 8)
                      ▲
                      │
                [FsReadCap] (Bitmask 4)
                      ▲
                      │
                [AllocCap] (Bitmask 2)
                      ▲
                      │
                    [⊥ / 0] (Pure Math)
```

### 4.1 Monotonic Capability Invariant
A child package cannot request capabilities that the parent package lacks.
The package manager validates this constraint using bitwise conjunction:
$$(\text{mask}_{\text{child}} \ \& \ \text{mask}_{\text{parent}}) == \text{mask}_{\text{child}}$$

If the equation evaluates to false, the package manager aborts with `ERR_CAP_ESCALATION`.

---

## 5. Fail-Closed Security State Machines

### 5.1 Bootstrap Package Retrieval State Machine

```
[INIT: Start Download]
         │
         ▼
[FETCH: curl asset + sha256 + minisig]
         │
         ├───► [ERROR: Network Timeout / 404] ──────► [FAIL_CLOSED: Exit Code 1]
         │
         ▼
[VERIFY_DIGEST: Compare SHA-256]
         │
         ├───► [ERROR: Digest Mismatch] ─────────────► [FAIL_CLOSED: Exit Code 1]
         │
         ▼
[VERIFY_SIGNATURE: Validate Ed25519]
         │
         ├───► [ERROR: Bad Signature] ──────────────► [FAIL_CLOSED: Exit Code 1]
         │
         ▼
[INSTALL: Extract to ~/.local/bin]
         │
         ▼
[SUCCESS: Write INSTALL_RECEIPT.txt]
```

### 5.2 Capability Grant State Machine

```
[PARSE: Read package manifest `caps`]
         │
         ▼
[CHECK: Subtype test against parent mask]
         │
         ├───► [ESCALATION: child & parent != child] ─► [DENY: Exit Code 1]
         │
         ▼
[APPLY: Restrict Landlock sandbox paths]
         │
         ▼
[EXECUTE: Compile package with granted tokens]
```

---

## 6. Phased Migration & Rollback Runbook

The restructuring executes across four non-destructive phases:

### 6.1 Phase 0: Baseline & Supply Chain Hardening
1. Create git tag `v2.9.0-baseline` across all repositories.
2. Enforce mandatory SHA-256 and Minisign Ed25519 verification in `install.sh`.
3. Rollback command: `git reset --hard v2.9.0-baseline`.

### 6.2 Phase 1: Decoupling (CUT-01..14)
1. Delete workspace root symlinks (`bin`, `runtime`, `fixtures`, `std`).
2. Remove relative directory hops (`../..`) in editor tooling scripts.
3. Switch editor communication to stdio JSON-RPC.
4. Rollback command: `git reset --hard pre-migration-phase-1`.

### 6.3 Phase 2: Consolidation into 3 Tiers
1. Pre-purge stale `ooda/qa/` stub directory.
2. Merge `qa`, `tree-sitter`, `vscode`, and `helloworld` into `ooda`.
3. Merge `research` into `openOODA`.
4. Merge `install` and `brand` into `openOODA.github.io`.
5. Rollback command: `git reset --hard pre-migration-phase-2`.

### 6.4 Phase 3: Version Locking & CI/CD Deployment
1. Deploy centralized workflows under `.github/workflows/ci.yml`.
2. Generate lockfile `ooda.lock` with toolchain binary hashes.
3. Rollback command: `git reset --hard pre-migration-phase-3`.

---

## 7. Governance Verification & Invariant Proofs

Verify ecosystem conformance with master governance commands:

```bash
# Execute master enforcer
./ooda/bin/ooda run openOODA/scripts/enforcer.oo

# Verify process board integrity
./ooda/bin/ooda run openOODA/scripts/check_board.oo

# Run master ecosystem verification
./ooda/bin/ooda run openOODA/scripts/verify_all.oo
```

All three commands must exit with return code 0 to certify release readiness.
