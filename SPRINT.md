# openOODA sprint

## Pin
| Item | Value |
|------|--------|
| Release | `v0.184.0-alpha` |
| Product tip | `7a46f6a` — **PM 3.2 + 3.3 done (alpha)** |
| Rails | `time_entropy_product_floor_smoke` + `memory_quota_product_floor_smoke` PASSED |
| Beta | **Not claimed** |

## Open (0)
*(none)*

## Closed
**PM 3.2 Time & entropy → done (alpha)**  
**PM 3.3 Memory quotas → done (alpha)**

What is production-ready (alpha):
- Clock and sleep need a **time token**.
- Random and seed need a **random token**.
- Fake tokens are refused at run time.
- List growth can hit a **quota** and fail closed; alloc helpers need an **alloc token**.

What is still not claimed:
- Crypto-grade random (CSPRNG).
- OS memory limits / typed alloc caps.
- FaceID / biometric tokens (already residual under 3.1).

SWARM: 2 explore mappers → solo Act.

## Residual named (honest)
- CSPRNG / OS rlimit residual
- Beta not claimed

## S
`S: low — U=0 on 3.2/3.3 floors F=0 W=0 O=0`
