# openOODA sprint

## Pin
| Item | Value |
|------|--------|
| Release | `v0.184.0-alpha` (stay alpha) |
| Focus | Pure multi dual-green residual; finish Issue #7 remaining over-600 files |
| Tip (product `ooda`) | `4317efb` source + **host binary m174** (product residual smokes green) |
| Boards monorepo | `88baccd`+ (SPEC/DESIGN honesty) |
| Beta | **Not claimed** |

## Path A closed this swarm (do not re-open)
| Issue | Disposition |
|-------|-------------|
| **#14** migrate sed rewrite | **FIXED** — `ooda_product_migrate.sh` fail-closed exit 1; no file rewrite |
| **#13** critical doc honesty (5 claims) | **FIXED** — SPEC.md + DESIGN.md `[STATUS: residual]` tags |
| **#11** `if field.chain == false` | **FIXED** — `tc_control_cond.oo` EQEQ/NEQ scan; commit `ff0187d` |
| **#12** zero coverage of typechecker bugs | **FIXED** path A — pass/fail/xfail fixtures + `typecheck_bug_rails_smoke` (`de59bc0`) |
| **#6** `&Struct` field access (batch) | **FIXED** path A batch — 41 files, ~372 sites, `std@899815b` (perf + priority sec/sys) |
| **#9** line numbers (single-file) | **FIXED** path A — `tc_diag.oo` + high-traffic printers + `typecheck_line_smoke` |
| **#7** over-600 splits (partial) | **FIXED** batch: mtls, waf, wireguard, jwt, ztidentity, spiffe, ids, physics/collision, robot/kinematics — shims ≤256, modules check green |
| Free-name Int mistypes | **FIXED** — `lhs`/`name`/`fty`/`cty` were wrongly `: Int` (commit `4317efb`) |

Prior closed: M158–M172, dnssec/ipsec/perf, Issues #1/#2/#4.

## Open work (path A)

### 1. Pure multi self-host dual-green
**Status:** residual — not dual-green.

Source free-name + Int-annotation fixes should drop the ~16 pure gcc cascade; **re-prove** pure rebuild on free-name host before tip flip. Product tip stays **m174** (caret green). Pure-linked hosts still need caret/`^` lex proof.

### 2. Issue #7 remaining over-600 files
Still need split (not done this swarm):
- `crypto/fhe.oo` (~768)
- `quantum/anneal.oo` (~702)
- `aero/aerodynamics.oo` (~643)
- `auto/behavior.oo` (~624)

### 3. Issue #15 files 300–600 lines
watermark, redteam, aml, rsa_pss, cell, battery, attestation, dispatch, inference, audit, prompt_filter — pending shim split.

### 4. Issue #6 remainder
~1,150 sites tree-wide; this swarm closed **perf + priority sec/sys** only. Remaining domains: bio, fin, sec/crypto, sec/cps, quantum, robot (partial), etc.

### 5. Issue #9/#10 multi-module residual
- Multi-import absolute line numbers still residual (need load_import offsets).
- lit_env / struct_table global contamination (Issue #10) residual; same-param-name xfail documents poison.

### 6. Issue #13 remaining doc gaps
5 critical claims fixed; ~57 other DESIGN/SPEC honesty gaps residual.

## Residual named (full DESIGN)
Full SMT · free-form multi-code · full HITL · actor supervision · real GPU · unrestricted dlopen · native `&str` · nested `List[Struct]` · product `&mut T` · object-cap crypto · SOCK_RAW · full async I/O · OS rlimit heap · Tier C · **object-caps** · beta not claimed.

## Smokes (tip m174)
- product residual: m169, cap_forge, … green  
- `typecheck_bug_rails_smoke`: ALL OK  
- `typecheck_line_smoke`: ALL OK (single-file; multi-import residual)

## M173 audit disposition

| # | Item | Status |
|---|------|--------|
| 6 | `&Struct` parens | **partial** — 41 files; remainder open |
| 7 | >600 line split | **partial** — 9/13+ of listed files split |
| 8/15 | 300–600 | open |
| 9 | line numbers | **path A single-file**; multi residual |
| 10 | lit_env pollution | residual (+ xfail) |
| 11 | control cond binop | **done** |
| 12 | fixtures | **done** |
| 13 | doc honesty | **5 critical done**; rest residual |
| 14 | migrate | **done** (disabled) |
