# openOODA sprint
Team: planner · coder · devil · reviewer · through 2026-08-11 17:00

## Pin
| Item | Value |
|------|--------|
| Release | `v0.184.0-alpha` |
| Product tip (`ooda` `main`) | `e1f6e44` — M125–M129 ship |
| Rails | `ci_product: PASSED` · line lock `O=0` |
| CLI | `ooda 0.184.0-alpha (pure .oo CLI)` |
| Beta | **Not claimed** |

## Open (0)
*(none — pick next ≤5 from PM.md by first principles)*

## Closed (this rotation)
**M125** Ambient List quota fail-closed (3.3) — `OO_LIST_AMBIENT_QUOTA` + `alloc_bytes` raise; bounded `list_quota_smoke` in `ci_product`.  
**M126** MaxCycles recursion fuel (3.4) — file-static `__oo_mc` + call-entry debit; `OO_MC_LIMIT` macro (env 1-char marker; multi-digit budget not in ARC env).  
**M127** Secret residual honesty re-sync (3.5) — `SECRET_TAINT.md` / PM match product (interproc/concat/write_file In).  
**M128** Secret write_file sink (3.5) — content IDENT refuse emit+check.  
**M129** LLVM Secret dual-path (4.1.2) — `emit-llvm` runs Secret check; fail-closed smoke.  
**M123** TOOLS scrub · **M124** pin honesty + hygiene · **M119** LLVM proven surface · M122…M46 · residual packs  

## Residual named (honest)
- Ambient quota ≠ OS rlimit / typed `&AllocCap<N>`  
- MaxCycles ≠ OS cgroup / `#[MaxCycles]` / static WCET  
- Secret ≠ NetCap/fetch / `#[Secret]` attr / full IFC  
- LLVM ≠ self-host floor  
