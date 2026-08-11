# openOODA sprint

## Pin
| Item | Value |
|------|--------|
| Release |  |
| Product tip |  — **PM 3.1 capability floor done (alpha)** |
| Rails |  |
| Beta | **Not claimed** |

## Open (0)
*(none)*

## Closed
**PM 3.1 Capability sandboxing → done (alpha)**

What is production-ready (alpha):
- Privileged actions need the right **capability token** (disk, network, process, env, time, random, alloc helpers).
- Missing token: refused at check time.
- Fake token: refused at run time.
- More “missing token” checks (write/path/size/sleep/seed).
- Full product-floor smoke is green.

What is still not claimed:
- FaceID / biometric tokens
- Unforgeable crypto capability objects
- OS-level isolation (cgroups / rlimits as the cap system)
- Caps that seal raw C foreign code

SWARM: 2 explore mappers → solo Act.

## Residual named (honest)
- Biometric/crypto object-caps residual
- Cap vs FFI residual
- Beta not claimed

## S

