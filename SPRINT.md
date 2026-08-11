# openOODA sprint

## Pin
| Item | Value |
|------|--------|
| Release | `v0.184.0-alpha` |
| Focus | Deepen #2 agent fix, #3 Cap/FFI runtime + HITL moonshot, #4 hygiene |
| Rails | `ecap_autofix_smoke`, `cap_ffi_runtime_smoke`, `hitl_product_floor_smoke` dual-green |
| Beta | **Not claimed** |

## Closed
**M155 E_CAP structural auto-fix** — `ooda fix` adds `&Cap` + first-arg; re-check no E_CAP.  
**M156 UnsafeFFICap runtime** — process-local grant/require + `oo_dlopen` stub; forge deny.  
**M157 HITL deny-mode** — `// HITL: pause` fail-closed at check (E_HITL).

## Residual named (honest)
- Multi-code AST auto-apply; OS dlopen / full C TCB; interactive HITL harness
- Beta/production not claimed

## S
`S: low — U=0 on M155–157 floors F=0 W=0 O=0`
