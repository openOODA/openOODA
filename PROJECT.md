# Project: openOODA Generational OODA & Via Negativa Doctrine Synthesis

## Architecture
- **Paradigm**: openOODA Process Board and Core Doctrine Architecture
- **Language & Engine**: `.oo` compiler/runtime (`/home/jeryd/Projects/openOODA/ooda/bin/ooda`)
- **Process Board Format**: `.oot` Plaintext Tabular / Card Process Boards
- **Linguistic Standard**: ASD-STE100 Simplified Technical English
- **Governance & Enforcer**: `openOODA/scripts/enforcer.oo` (8 Gates) and `openOODA/scripts/check_board.oo` (10-Board Root Whitelist)

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Phase 1 Mapping (Kinematic to Informational OODA) | Boyd's mechanical blind spot ($P_s$, AVX/NEON) elevated to full-spectrum AST observation, Merkle diffing, and SMT orientation | M1, M2 | survey (explorer_3) |
| 2 | Phase 2 Mapping (Centralized to Distributed State Mesh) | Distributed sensor fusion consensus, shared capability DAGs, p2p verification in $O(\log M)$ | M1, M2 | survey (explorer_3) |
| 3 | Phase 3 Mapping (Static Code to Autonomous Swarm Adaptation) | Real-time AST mutation, live PGO, Undo-RAM ghost-state transactional memory, human latency elimination ($10^5 \to \le 10^2$ ms) | M1, M3 | survey (explorer_3) |
| 4 | Phase 4 Mapping (Boundary Physics & Hard Limits) | Rice's Theorem (SMT bounded contract decidability), CAP Theorem (monotonic capability attenuation & leases), Landauer's Principle (linear arenas $O(1)$ bulk resets & zero-leak ARC) | M1, M2, M3 | survey (explorer_3) |
| 5 | Phase 5 Mapping (Generational Encapsulation) | Gen 1-4 (hardware/compiler/runtime/language) encapsulated into deterministic reflexes underpinning Gen 5 (swarms) and Gen 6 (autonomous sovereign intelligence) | M1, M2 | survey (explorer_3) |
| 6 | Via Negativa Subtractive Framework | Systematic subtraction of GC, ambient authority, null/UB, dynamic dispatch, and human cognitive latency | M1, M2, M3 | survey (explorer_3) |
| 7 | Formal RFC Specification (`rfcs/0020-generational-ooda.oot`) | Complete formal specification conforming to `rfcs/0000-template.oot`, $\le 256$ lines, ASD-STE100 | M1, M3B, M3C | survey (explorer_2,3) |
| 8 | NORTHSTAR.oot Synthesis | Core doctrine integration: Informational E-M, Gen 1-6 hierarchy, Via Negativa, Boundary Physics, 3 Operational Laws | M2, M3B | survey (explorer_1,3) |
| 9 | START.oot Synthesis | Strategic Pillars 2 & 6 doctrine update, process board routing, 10-board whitelist compliance | M2 | survey (explorer_1,3) |
| 10 | RULES.oot Synthesis | Via Negativa law (§1.2), Boundary Physics (§1.5), Hierarchical Loop Encapsulation (§1.6), 3 Operational Laws (§1.20) | M3, M3B | survey (explorer_1,3) |
| 11 | MOONSHOTS.oot Synthesis | Phases 1-5 moonshot initiatives (Autonomous Mutation, BFT Mesh, ZK Compute, Undo-RAM, SMT Synthesis) | M3 | survey (explorer_1,3) |
| 12 | QUICKREF.oot Synthesis | 3-Tier Structure codification (Tactical Code Physics, Operational Workflow, Strategic Doctrine) | M3C | follow-up 2 |
| 13 | Master Governance Verification & Enforcers | Passing `enforcer.oo` 8 gates, `check_board.oo`, `verify_all.oo`, `rfc_lint.oo`, `format_lint.oo` | M4 | survey (explorer_2) |
| 14 | Version Bump & GitHub Commit | Bumped version to `v0.211.5` in `ROADMAP.oot` and committed (commits `6e5793d`, `30aca05`) | M4 | user rule |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Formal RFC 0020 Specification | Draft `openOODA/rfcs/0020-generational-ooda.oot` | none | DONE |
| M2 | Core Doctrine Boards (NORTHSTAR & START) | Update `openOODA/NORTHSTAR.oot` and `openOODA/START.oot` | M1 | DONE |
| M3 | Core Governance Boards (RULES & MOONSHOTS) | Update `openOODA/RULES.oot` and `openOODA/MOONSHOTS.oot` | M1 | DONE |
| M3B | 3 Fundamental Operational Laws | Update RFC 0020, NORTHSTAR.oot, RULES.oot | M1, M2, M3 | DONE |
| M3C | 3-Tier Structure Codification | Update RFC 0020 and QUICKREF.oot | M3B | DONE |
| M4 | Master Enforcers, Git Version & Commit | Execute `enforcer.oo` 8-gate suite, `verify_all.oo`, bump version, git commit (v0.211.5) | M1-M3C | DONE |

## Interface Contracts
### RFC 0020 ↔ Canonical Boards (`NORTHSTAR.oot`, `START.oot`, `RULES.oot`, `MOONSHOTS.oot`, `QUICKREF.oot`)
- **Format**: Pure `.oot` format, strictly $\le 256$ lines per file.
- **Language**: ASD-STE100 Simplified Technical English.
- **Formulas**:
  - Informational Boyd E-M: $E-M = \frac{T - D}{W} \cdot V$ where $T$=Thrust (semantic inference/mutation rate), $D$=Drag (AST complexity & verification latency), $W$=Weight (binary/runtime entropy), $V$=Velocity (cycle clock speed).
  - Landauer Thermodynamic Dissipation: $\Delta Q \ge k_B T \ln 2$.
  - Generational Hierarchy: Gen 1 (Physical/Silicon), Gen 2 (Compiler), Gen 3 (Runtime/Memory), Gen 4 (Language/Type Safety), Gen 5 (Multi-Agent Swarms), Gen 6 (Autonomous Sovereign Intelligence).
  - Boundary Physics: Rice (bounded SMT quantifier-free decidability), CAP (consistency over availability under partition via monotonic attenuation), Landauer (minimal entropy linear arenas + RAII ARC).
  - Operational Laws: Substratum Integrity, Hermetic Encapsulation, Bounded Promotion.
  - 3-Tier Structure: Layer 1 Tactical Code Physics, Layer 2 Operational Workflow & Logistics, Layer 3 Strategic Doctrine.

## Code Layout
- `openOODA/NORTHSTAR.oot` — Strategic North Star, Generational Hierarchy, Informational E-M, Via Negativa, Operational Laws (181 lines)
- `openOODA/START.oot` — Strategic Pillars, Operational Baseline, 10-Board Index (159 lines)
- `openOODA/RULES.oot` — Repository Laws, Via Negativa, Boundary Physics, Encapsulation, Operational Laws (191 lines)
- `openOODA/MOONSHOTS.oot` — 5-Phase Evolutionary Moonshots and Long-term Capabilities (111 lines)
- `openOODA/QUICKREF.oot` — 3-Tier Architectural Structure Quick Reference (160 lines)
- `openOODA/rfcs/0020-generational-ooda.oot` — Formal Invariant Specification, 3 Operational Laws, 3-Tier Structure (183 lines)
- `openOODA/ROADMAP.oot` — Roadmap and version pin `v0.211.5` (117 lines)
- `openOODA/scripts/enforcer.oo` — 8-Gate Master Governance Validator
- `openOODA/scripts/check_board.oo` — 10-Board Root Whitelist Validator
