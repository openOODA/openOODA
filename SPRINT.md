# openOODA sprint

## Pin
| Item | Value |
|------|--------|
| Release | `v0.184.0-alpha` |
| Product tip | `ad05f16` — **PM 3.6 fuzz path A done (alpha)** |
| Rails | `fuzz_product_floor_smoke: PASSED` |
| Beta | **Not claimed** |

## Open (0)
*(none)*

## Closed
**PM 3.6 Automated contract fuzzer → done (alpha)**

What is production-ready (alpha):
- `ooda test --fuzz` works without Python.
- Domains: int, bool, string, list (with markers).
- Pass and fail checks for those domains.
- Multi-argument functions of one type (homogeneous).
- Floor smoke is green.

What is still not claimed:
- Reading real `requires`/`ensures` from the AST (markers only).
- Mixed-type multi-arg fuzz.
- Hive-mind / network fuzz.
- Full formal proof of contracts.

SWARM: 2 explore mappers → solo Act.

## Residual named (honest)
- AST contracts / mixed multi / other domains residual
- Beta not claimed

## S
`S: low — U=0 on 3.6 path A F=0 W=0 O=0`
