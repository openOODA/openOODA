# openOODA sprint

## Pin
| Item | Value |
|------|--------|
| Release | `v0.184.0-alpha` |
| Product tip | `43b3714` — **PM 3.5 secret path A done (alpha)** |
| Rails | `secret_product_floor_smoke: PASSED` |
| Beta | **Not claimed** |

## Open (0)
*(none)*

## Closed
**PM 3.5 Static secret / taint → done (alpha)**

What is production-ready (alpha):
- Tag secret data with `// SECRET: name`.
- Secret bare names cannot go to major sinks (print, files, network, process, env, time/random/alloc helpers, exit).
- Same refuse on LLVM emit path for representative cases.
- Floor smoke is green.

What is still not claimed:
- Special `#[Secret]` language attribute
- Perfect whole-program secrecy for every sink
- Crypto scrubbing of secrets

SWARM: 2 explore mappers → solo Act.

## Residual named (honest)
- Attribute grammar / full IFC residual
- Beta not claimed

## S
`S: low — U=0 on 3.5 path A F=0 W=0 O=0`
