# openOODA sprint

## Pin
| Item | Value |
|------|--------|
| Release | `v0.184.0-alpha` |
| Product tip | `bbae8ba` — **PM 3.4 MaxCycles done (alpha)** |
| Rails | `max_cycles_product_floor_smoke: PASSED` |
| Beta | **Not claimed** |

## Open (0)
*(none)*

## Closed (this work)
**PM 3.4 MaxCycles → done (alpha)**

What is production-ready (alpha product floor):
- You can set a cycle budget with `// MAX_CYCLES: N` (large numbers work).
- Loops and recursive calls spend that budget.
- Going over the budget fails clearly (error + non-zero exit).
- Zero/invalid budgets fail closed (not silent).

What is still not claimed (residual):
- Not an OS-level CPU jail.
- Not the fancy attribute form from the vision doc.
- Not a compile-time proof that every infinite loop is impossible.

Also shipped:
- Recursion check now runs from the product folder so it works reliably.
- One umbrella check runs all MaxCycles product rails.

## Residual named (honest)
- OS cgroup / attribute grammar / static WCET — residual only
- Beta not claimed
- Other PM items unchanged

## SWARM
solo Act

## S
`S: low — U=0 on 3.4 floor F=0 W=0 O=0`
