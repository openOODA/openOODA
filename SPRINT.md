# openOODA sprint

## Pin
| Item | Value |
|------|--------|
| Release | `v0.184.0-alpha` |
| Product tip | `88084ae` — **PM 6.3 Cap vs FFI path A** |
| Rails | `cap_ffi_product_floor_smoke` PASSED |
| Beta | **Not claimed** |

## Open (0)
*(none)*

## Closed
**M152 Cap vs FFI path A → done (alpha)**

What is production-ready (alpha):
- Calling raw **dlopen** / host-FFI names without an **unsafe FFI token** is refused at check.
- With `&UnsafeFFICap` and the token as the first argument, check allows the name form.
- The C backend still **does not** lower real `dlopen` (fail-closed residual) — no silent fake lower.

What is still not claimed:
- Runtime process-local FFI token / forge deny for OS `dlopen`.
- Full C TCB seal, raw pointers, compile-time FFI generation.

SWARM: solo Act (check_cap_util / lower / fixtures / docs overlap).

## Residual named (honest)
- Runtime UnsafeFFICap, OS dlopen, raw-pointer, FFI_GEN
- Beta not claimed

## S
`S: low — U=0 on 6.3 path A F=0 W=0 O=0`
