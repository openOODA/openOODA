# openOODA sprint
Team: planner · coder · devil · reviewer · through 2026-08-12 17:00

## Pin
| Item | Value |
|------|--------|
| Release | `v0.184.0-alpha` |
| Product tip (`ooda` `main`) | `ed5e4ea` — start of this rotation |
| Rails | prove each M done-bar; line lock `O=0` on touched files |
| CLI | `ooda 0.184.0-alpha (pure .oo CLI)` |
| Beta | **Not claimed** |

## Open (≤5) — power law + first principles

**Rank:** security fail-open → self-test depth → CPU quota honesty → diag honesty → lock.

**Note:** Closing an M# means the **slice** met its done-bar. PM leaf stays **partial** until the whole DESIGN claim is honest.

| # | Slice | PM leaf | Done-bar (this M only) | PM after ship |
|---|--------|---------|------------------------|---------------|
| **M135** | Secret `sys_exec` sink refuse | **3.5** | Bare SECRET IDENT in `sys_exec` argv (program or later args) fails **emit + check**; pass + fail fixtures; enforce smoke wired | 3.5 stays **partial** (other sinks / attr / IFC residual) |
| **M136** | Secret residual doc + smoke match M135 | **3.5** | `SECRET_TAINT.md` names sys_exec In; residual list honest; residual smoke still PASS | same |
| **M137** | Pure List multi-arg fuzz arity-2 | **3.6** | `ooda test --fuzz` pure path covers List arity-2 multi (or named fail-closed residual if blocked); immune smoke; no fake full fuzz claim | 3.6 stays **partial** (arity≥4 residual) |
| **M138** | MaxCycles multi-digit N prove | **3.4** | `// MAX_CYCLES: N` with **N≥10** (multi-digit) works on while or recursion path; pass + fail fixtures; residual still ≠ OS cgroup / `#[MaxCycles]` | 3.4 stays **partial** |
| **M139** | Lock + pin honesty | meta | Touched files line lock O=0; secret/fuzz/max_cycles smokes green as claimed; SPRINT/PM tip = real `ooda` HEAD | — |

## Closed (prior rotation)
**M130–M134** pin honesty · Secret fetch URL · enforce smoke fix · SECRET_TAINT · prove rails (`ed5e4ea`).

## Residual named (honest) — still true
- Secret ≠ full IFC / `#[Secret]` attr / all OS sinks  
- Fuzz ≠ full DESIGN contract fuzzer / arity≥4  
- MaxCycles ≠ OS cgroup / attr grammar / static WCET  
- LLVM ≠ self-host floor  
- Beta not claimed  

## Decide rationale (short)
1. **3.5** — keep closing fail-open Secret sinks (next: `sys_exec` after fetch/write_file/println).  
2. **3.6** — self-testing depth; List multi-arg is named residual with clear bar.  
3. **3.4** — prior residual said multi-digit weak; prove or keep honest.  
4. **M139** — RULES Lock; pin matches tree.  
5. Long tail (GPU, hive-mind, macros) ignored this turn.
