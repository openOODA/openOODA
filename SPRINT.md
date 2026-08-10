# openOODA sprint
Team: planner · coder · devil · reviewer · through 2026-08-11 17:00

## Pin
| Item | Value |
|------|--------|
| Release | `v0.184.0-alpha` |
| Product tip (`ooda` `main`) | `ed5e4ea` — M130–M134 ship |
| Rails | `secret_sink_enforce_smoke` + residual PASS · line lock `O=0` |
| CLI | `ooda 0.184.0-alpha (pure .oo CLI)` |
| Beta | **Not claimed** |

## Open (0)
*(none — pick next ≤5 from PM.md by first principles)*

## Closed (this rotation)
**M130** Pin honesty — tip `ed5e4ea`; PM pin matches product HEAD.  
**M131** Secret `fetch` URL sink refuse (3.5) — bare SECRET IDENT as URL fails emit+check; pass/fail fixtures.  
**M132** Secret enforce smoke structure — valid bash; fetch fixtures wired.  
**M133** SECRET_TAINT residual honesty — fetch In; other OS/NetCap friends residual; marker kept.  
**M134** Prove rails — smokes green; line lock O=0 on `c_emit_secret` / `c_emit_lower` (≤256).  

## Residual named (honest)
- Secret ≠ full IFC / `#[Secret]` attr / all OS sinks  
- Ambient quota ≠ OS rlimit  
- MaxCycles ≠ OS cgroup / attr grammar  
- LLVM ≠ self-host floor  

## S report (optional)
`S: low (Δ down) — U=0 on M131 claim F=0 W=0 O=0` (touched files ≤256)
