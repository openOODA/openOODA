# openOODA sprint

## Pin
| Item | Value |
|------|--------|
| Release | `v0.184.0-alpha` |
| Product tip | `28d678b` — **full PM alpha pass** |
| Rails | `alpha_pm_floors_smoke` PASSED (floors + residual honesty packs) |
| Beta | **Not claimed** |

## Open (0)
*(none)*

## Closed
**M151 Full PM alpha pass**

What is production-ready (alpha):
- Every **product floor** leaf is **done (alpha)** with green smoke (caps, time/rand, memory, max-cycles, secret, fuzz, contracts, json-errors, ARC free, C/LLVM/WASM path A, outline/reflect/patch, diagnostics).
- Machine-readable check errors work under free (`--json-errors`); pass is `[]`; fails use stable codes + hints.
- Moonshots are **residual** with named packs + residual smokes — not fake done.

What is still not claimed (honest residual):
- AST auto-apply, biometric caps, CSPRNG, OS rlimits/cgroups, full IFC, JIT, GPU/NPU, bare-metal, hive-mind, native LSP, interactive HITL/playground, Cap vs C FFI seal, bit-identical hermetic dist, full pkg registry.

SWARM: solo Act (emit/diag modules overlap) — no multi-agent file collision.

## Residual named (honest)
- See PM.md **residual** rows + `bootstrap/*RESIDUAL*.md` packs (39 indexed)
- Beta not claimed

## S
`S: low — U=0 on product floors F=0 W=0 O=0 (diag_json ≤256)`
