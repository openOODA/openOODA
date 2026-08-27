# E2E Test Infra: openOODA Generational OODA & Via Negativa Synthesis

## Test Philosophy
- Opaque-box, requirement-driven, and formal governance enforcement.
- Verification methodology: 8-Gate Master Governance Lint, 10-Board Hygiene Check, RFC Template Validator, AST Format Validator, Anti-Cheat Integrity Linter, and Line Count Boundary Check.

## Feature Inventory
| # | Feature | Source (requirement) | Tier 1 | Tier 2 | Tier 3 |
|---|---------|---------------------|:------:|:------:|:------:|
| 1 | Phase 1 (Kinematic to Informational OODA) | ORIGINAL_REQUEST §R1.1 | ✓ | ✓ | ✓ |
| 2 | Phase 2 (Centralized to Distributed State Mesh) | ORIGINAL_REQUEST §R1.2 | ✓ | ✓ | ✓ |
| 3 | Phase 3 (Autonomous Swarm Adaptation) | ORIGINAL_REQUEST §R1.3 | ✓ | ✓ | ✓ |
| 4 | Phase 4 (Rice/CAP/Landauer Boundary Physics) | ORIGINAL_REQUEST §R1.4 | ✓ | ✓ | ✓ |
| 5 | Phase 5 (Generational Encapsulation Gen 1-6) | ORIGINAL_REQUEST §R1.5 | ✓ | ✓ | ✓ |
| 6 | Core Doctrine Process Boards (NORTHSTAR, START, RULES, MOONSHOTS) | ORIGINAL_REQUEST §R2 | ✓ | ✓ | ✓ |
| 7 | Pure .oot Format & $\le 256$ Lines / File | RULES.oot §1.8, §1.13 | ✓ | ✓ | ✓ |
| 8 | ASD-STE100 Simplified Technical English | RULES.oot §1.11 | ✓ | ✓ | ✓ |
| 9 | 8-Gate Master Enforcer Suite | scripts/enforcer.oo | ✓ | ✓ | ✓ |

## Test Architecture
- **Runner**: `/home/jeryd/Projects/openOODA/ooda/bin/ooda run <script>`
- **Suite Command**:
  1. `/home/jeryd/Projects/openOODA/ooda/bin/ooda run openOODA/scripts/enforcer.oo`
  2. `/home/jeryd/Projects/openOODA/ooda/bin/ooda run openOODA/scripts/check_board.oo`
  3. `/home/jeryd/Projects/openOODA/ooda/bin/ooda run openOODA/scripts/verify_all.oo`
  4. `/home/jeryd/Projects/openOODA/ooda/bin/ooda run openOODA/scripts/rfc_lint.oo`
  5. `/home/jeryd/Projects/openOODA/ooda/bin/ooda run openOODA/scripts/anti_cheat_linter.oo`
  6. `wc -l openOODA/*.oot openOODA/rfcs/*.oot`
- **Pass/Fail Semantics**: Exit code 0 required for all validators. Zero line counts > 256. Zero forbidden file extensions. Zero unheaded files.

## Real-World Application Scenarios (Tier 4)
| # | Scenario | Features Exercised | Complexity |
|---|----------|--------------------|------------|
| 1 | Full Repository Governance & Board Hygiene Pass | F6, F7, F8, F9 | High |
| 2 | RFC 0020 Generational OODA Template & Formal Contract Pass | F1-F5, F7, F8, F9 | High |
| 3 | Core Doctrine Process Boards Line Limit & Format Verification | F1-F8 | High |
| 4 | Boyd E-M & Invariant Cross-Board Mathematical Consistency | F1-F6 | High |
| 5 | Version Bumping and Clean Git Tree Verification | F9 | Medium |

## Coverage Thresholds
- Tier 1: Feature coverage for all 5 evolution phases and 6 generational tiers across all target boards.
- Tier 2: Boundary & Corner verification ($\le 256$ lines ceiling, exact headers, exact whitelist names).
- Tier 3: Cross-board reference consistency (`NORTHSTAR.oot` ↔ `START.oot` ↔ `RULES.oot` ↔ `MOONSHOTS.oot` ↔ `rfcs/0020-generational-ooda.oot`).
- Tier 4: Master enforcer 8-gate pass + clean git commit.
