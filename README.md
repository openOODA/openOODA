<div align="center">

# openOODA Governance & Meta-SSoT
### Tier 1 Sovereign Process Architecture, Formal RFCs & Rule Enforcement

[![Version](https://img.shields.io/badge/version-v2.9.4-00f2fe.svg?style=flat-square)](https://github.com/openOODA/openOODA)
[![10-Pillar Enforcer](https://img.shields.io/badge/10--Pillar%20Enforcer-PASS%20(__FAILS__%3D0)-00e676.svg?style=flat-square)](scripts/enforcer.oo)
[![13 Process Boards](https://img.shields.io/badge/13%20Process%20Boards-13%2F13%20VERIFIED-7928ca.svg?style=flat-square)](scripts/verify_all.oo)
[![8D Red Team](https://img.shields.io/badge/8D%20Red%20Team-PASS%20(9%20Gates)-brightgreen.svg?style=flat-square)](scripts/redteam_hook.oo)
[![Zero Ambient Authority](https://img.shields.io/badge/Zero%20Ambient%20Authority-14%20OCap%20Tokens-ff0055.svg?style=flat-square)](SECURITY.oot)
[![Topology](https://img.shields.io/badge/Topology-Tier%201%20Governance%20SSoT-blue.svg?style=flat-square)](https://openooda.org)
[![License](https://img.shields.io/badge/license-MIT%20OR%20Apache--2.0-ffd700.svg?style=flat-square)](LICENSE)

```text
   ____  ____  ___  ____    ___   ___  ____    _   
  / __ \/ __ \/ _ \/ __ \  / _ \ / _ \|  _ \  / \  
 / /_/ / /_/ /  __/ / / / | | | | | | | | | |/ _ \ 
 \____/ .___/\___/_/ /_/  | |_| | |_| | |_| / ___ \
     /_/                   \___/ \___/|____/_/   \_\
   Tier 1: Single Source of Truth (SSoT) — Governance & Meta-Specification
```

**13 Canonical Process Boards · 10 Strategic Governance Pillars · Energy-Maneuverability ($P_{s,\text{info}}$)**

[Organization Hub](https://github.com/openOODA) • [Compiler & Runtime (Tier 2)](https://github.com/openOODA/ooda) • [Portal & Distribution (Tier 3)](https://github.com/openOODA/openOODA.github.io)

---

</div>

## Overview

The `openOODA` repository serves as the **Tier 1 Sovereign Single Source of Truth (SSoT)** and architectural governance anchor for the entire openOODA ecosystem.

Tier 1 governs Tier 2 (Compiler & Engine) and Tier 3 (Distribution Portal) through formal specifications, machine-executable process boards, formal RFC standards, academic research papers, and deterministic governance linters. All policies are immutable laws verified fail-closed on every commit.

---

## The 13 Canonical Process Boards

All organizational state, operational doctrine, architectural constraints, and roadmap milestones are maintained in 13 machine-parseable OpenOODA Text (`.oot`) boards. Every board is constrained to **strictly $\le 256$ lines**:

| # | Board File | Title & Strategic Domain | Invariant Limit | Verification Linter |
|---|---|---|---|---|
| 1 | [`START.oot`](START.oot) | Orientation, Mission, Topology DAG, and 3-Tier Architecture | $\le 256$ lines | `scripts/check_board.oo` |
| 2 | [`RULES.oot`](RULES.oot) | Repository Law, Core Principles, and Invariant Directives | $\le 256$ lines | `scripts/check_board.oo` |
| 3 | [`NORTHSTAR.oot`](NORTHSTAR.oot) | 100-Year Architectural Vision & Autonomic AI Substrate | $\le 256$ lines | `scripts/check_board.oo` |
| 4 | [`MOONSHOTS.oot`](MOONSHOTS.oot) | High-Risk High-Reward Breakthrough Projects | $\le 256$ lines | `scripts/check_board.oo` |
| 5 | [`ROADMAP.oot`](ROADMAP.oot) | Phase & Milestone Timeline (Current: v2.9.4) | $\le 256$ lines | `scripts/check_board.oo` |
| 6 | [`SHIPPED.oot`](SHIPPED.oot) | Chronological Shipped Artifacts & Releases (Generated) | $\le 256$ lines | `scripts/verify_all.oo` |
| 7 | [`FORMAT.oot`](FORMAT.oot) | ASD-STE100 Academy Header Standards & Grammar Rules | $\le 256$ lines | `scripts/enforcer.oo` |
| 8 | [`SECURITY.oot`](SECURITY.oot) | 14 OCap Capability Tokens & Zero Ambient Authority | $\le 256$ lines | `scripts/check_board.oo` |
| 9 | [`WORKFLOW.oot`](WORKFLOW.oot) | Autonomous Agent Swarm Protocols & Dispatch Loops | $\le 256$ lines | `scripts/check_board.oo` |
| 10 | [`QUICKREF.oot`](QUICKREF.oot) | Developer Syntax, Capability Tokens, and CLI Handbook | $\le 256$ lines | `scripts/check_board.oo` |
| 11 | [`CONSTRAINTS.oot`](CONSTRAINTS.oot) | Structural Limits, Prohibited Patterns, and Invariants | $\le 256$ lines | `scripts/check_board.oo` |
| 12 | [`STRUCTURE_EM.oot`](STRUCTURE_EM.oot) | Energy-Maneuverability Formulations & Drag Proofs | $\le 256$ lines | `scripts/check_board.oo` |
| 13 | [`REDTEAM.oot`](REDTEAM.oot) | 8-Dimensional Adversarial Falsification & Attack Vectors | $\le 256$ lines | `scripts/redteam_hook.oo` |

---

## The 10 Strategic Governance Pillars

Enforced programmatically by `openOODA/scripts/enforcer.oo` with zero error tolerance (`__FAILS__=0`):

### 1. First Principles & Pure File Extension Laws
Product source trees admit **only `.oo` and `.oot` files**. Foreign scripting files (`.py`, `.sh`, `.js`, `.md`) are strictly quarantined or forbidden in core product scope to prevent ambient execution vectors.

### 2. Boyd Energy-Maneuverability Invariant ($\le 256$ Lines)
Every `.oo` and `.oot` file must strictly satisfy $\text{lines} \le 256$. Files exceeding this bound induce cognitive drag on human and LLM context windows and are automatically rejected. Zero residual intermediate artifacts (`*.tmp.c`, `*.protos.c`, `*.tu.c`, `*.bin`, `*.txt`) are permitted in product trees.

### 3. Adversarial Validation & Double-Run Invariant
No milestone is marked complete without negative-trust tests, mutant injection, and double-run verification:

$$\text{Double-Run: } \text{Run}_1(\text{Test}) \equiv \text{Run}_2(\text{Test}) \implies \text{Deterministic State}$$

### 4. Academy 4-Element Headers
Every `.oo` file must begin with an ASD-STE100 controlled English header:
```rust
// # <Module Name> — <Summary Title>
//
// Logline: <One-line functional synopsis of purpose and invariants>
//
// Setup: <Capability tokens required and preconditions>
//
// Beats:
//   1. <Execution beat 1>
//   2. <Execution beat 2>
//   3. <Execution beat 3>
```

### 5. Capability Security & Zero Ambient Authority
Code has zero implicit I/O capability. Functions receive explicit capability references (`&FsReadCap`, `&FsWriteCap`, `&ProcessCap`, `&NetCap`, `&SysCap`, etc.). Helper routines cannot synthesize ambient access.

### 6. Multi-Agent Swarm Safety & Topology Invariance
Autonomous agent swarms operate on stationary workspace topologies ($\Delta_{\text{path}} = 0$). Agent self-replication and identity mutation are strictly blocked fail-closed.

### 7. Formal RFC Template Compliance
All RFC proposals in `openOODA/rfcs/` must follow `0000-template.oot` with valid `RFC ID`, `Author`, `Status`, `Security`, and `Testing` sections. Implemented RFCs must contain concrete adversarial test suites.

### 8. Two-Binary Architecture
The compiler (`oodac`) is decoupled from the workflow driver (`ooda`). `oodac` is dedicated to pure SSA lowering, typechecking, and machine code generation; `ooda` coordinates commands, tests, LSP, and MCP discovery.

### 9. Gen 1 C/H Substrate Isolation
All low-level C runtime shims (`chs_rt_*.c`, `chs_rt.h`) are strictly confined to `ooda/runtime/`. No C header or source leakage into standard library modules is tolerated.

### 10. Zero Loose Unheaded Files & Clean Workspaces
The root directory of all product trees must contain zero unmanaged or unheaded `.oo` files. All source files must be indexed and traceable to a canonical process board.

---

## Energy-Maneuverability ($P_{s,\text{info}}$) Formulation

openOODA models software development and execution through John Boyd's Energy-Maneuverability framework:

$$P_{s,\text{info}} = \left(\frac{T_{\text{semantic}} - D_{\text{systemic}}}{W_{\text{entropy}}}\right) \cdot V_{\text{ooda}}$$

```text
                      THRUST (T_semantic)
  High-rate SSA Lowering + 256-bit SIMD (f32x8) + Direct ELF64/WASM
────────────────────────────────────────────────────────────────────────
                      DRAG (D_systemic -> 0)
  0ms GC Pauses + Merkle AST (<100μs) + 95.5% Coordination Reduction
────────────────────────────────────────────────────────────────────────
                     WEIGHT (W_entropy -> min)
  28 KB Standalone Binary + Linear Bump Arenas + <= 256 Line Files
────────────────────────────────────────────────────────────────────────
                    VELOCITY (V_ooda = 2,500 Hz)
  0.4 ms Autonomic Agent Loop Turnover (125,000x over legacy VM stacks)
```

### Systemic Drag Elimination
$$D_{\text{systemic}} = D_{\text{rebuild}} + D_{\text{token\_burn}} + D_{\text{alloc}} + D_{\text{search}} + D_{\text{verify}} \longrightarrow 0$$

- $D_{\text{rebuild}} < 100\,\mu\text{s}$ via content-addressed Merkle AST hashes.
- $D_{\text{token\_burn}} \le 1.3\%$ via high-density sparing ingress compression ($\rho \ge 98.7\%$).
- $D_{\text{alloc}} = 0\,\text{ms}$ via linear bump arenas with $O(1)$ bulk resets.
- $D_{\text{search}} = 0$ via 13 canonical process boards and 18-tool MCP auto-discovery.
- $D_{\text{verify}} < 500\,\text{ms}$ via deterministic master enforcers.

---

## Governance Verification Suite

Run the full governance verification suite from repository root:

```bash
# 1. Verify 10-Pillar Master Governance & Invariants
./ooda/bin/ooda run openOODA/scripts/enforcer.oo

# 2. Verify 13 Process Boards & RFC Freshness
./ooda/bin/ooda run openOODA/scripts/verify_all.oo

# 3. Verify Board Line Limits & Academy Headers
./ooda/bin/ooda run openOODA/scripts/check_board.oo

# 4. Verify 8-Dimensional Adversarial Red Team Gates
./ooda/bin/ooda run openOODA/scripts/redteam_hook.oo
```

All governance checks must exit with `__FAILS__=0` before any release artifact is staged.

---

## License

Dual-licensed under either of:
- **MIT License** ([LICENSE-MIT](LICENSE-MIT) or https://opensource.org/licenses/MIT)
- **Apache License, Version 2.0** ([LICENSE-APACHE](LICENSE-APACHE) or https://www.apache.org/licenses/LICENSE-2.0)

at your option.
