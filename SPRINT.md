# openOODA sprint

## Pin
| Item | Value |
|------|--------|
| Release | `v0.184.0-alpha` (stay alpha) |
| Focus | Pure multi self-host dual-green residual + board hygiene |
| Tip (product `ooda`) | `c554319` (+ local host binary m174-class; pure rebuild not dual-green) |
| Tip (monorepo boards) | `3ebef74` |
| Beta | **Not claimed** |

## Path A closed (do not re-open)
M158–M169 path A · M166 AGY language floors · M167 residual deepen · M168 AGY blockers · M169 residual closeout · M171 untyped-let SEGV short-circuit · M172 token tooling + product CLI (`outline`/`reflect`/`digest`/`health`/`err-digest`/`pack`).

Product residual smokes green on tip host (2026-08-11): `m169_residual_closeout`, `agy_lang_blockers`, `cap_forge_path_a`, `m167_residual_deepen`, `bitwise_ops`, `malloc_path_a` — all exit 0.

## Open work (path A)

### 1. Pure multi self-host dual-green
**Status:** residual — not dual-green.

| Fact | Detail |
|------|--------|
| Product floors | Dual-green for language path-A smokes on tip host binary |
| Pure rebuild | `scripts/oodac_pure_build.sh oodac/main.oo` reaches gcc then **fails** |
| Root class | Emit quality: many untyped `let` bind as `long long` where `OoStr`/`OoSList` expected (`oo_str_eq`, `oo_str_concat`, env push/release) |
| Partial fix this rotation | `oodac/main.oo`: removed wrong `: Int` on `sys_exec`/`read_file` Result lets so free-name → `OoResS` (matches `cli_emit.oo`) |
| Done when | Pure rebuild produces executable that re-emits core modules without SEGV; product smokes still green |
| Out of scope | Bit-identical fixed-point forever; cold start from air |

**Evidence:** pure rebuild log + error kind digest (session SCRATCH / agent leave-off). Prefer `ooda health` / `scripts/ooda_err_digest.sh` — do not paste full `all.c`.

### 2. sec/net line-pressure residual
| File | State | Blocker |
|------|-------|---------|
| `sec/net/dnssec.oo` | ERR | Ambient List quota at ~882 lines; typechecker phantom + real bugs (`let mut valid` pattern; param shadows field `iterations`) |
| `sec/net/ipsec.oo` | ERR | Same class at ~840 lines |

**Done when:** both pass `oodac check` under product quota rules (split files ≤256 lines preferred, or documented quota for smoke only without lying about lock).

Other `sec/net/*` (spiffe, mtls, jwt, ids, waf) already OK this rotation.

## Residual named (full DESIGN — not this path A)
Full SMT/quantifiers · free-form multi-code auto-apply · full HITL record/replay · actor supervision trees · real GPU/NPU shaders · unrestricted any-path dlopen · native `&str` lifetimes · nested `List[Struct]` · product `&mut T` · object-cap crypto / cast-surface beyond path-A refuse · SOCK_RAW · full async epoll/inotify product · OS rlimit heap sandbox · Tier C (temporal/hive/hot-reload/LSP/…)

**Cap forgery:** path A refuse/smoke green (`cap_forge_path_a`); object-caps / remaining cast surface still DESIGN residual (`STATIC_CAPS.md`).

Beta not claimed.

## Library wave honesty
`std/` mass fleshing + `sec/*` wave (crypto/sys/net/cps/ai) path-A stub/check pattern stands. Do **not** re-list AGY “Currently missing” language floors — those path-A items closed under M166–M169 (malloc free names, bitops+caret product, float/trig, tensor helpers, tcp slot IO, sealed syscalls, `xs[i]`, `ord` via `byte_at`, `Int < 0`, param/field shadow, …). Only DESIGN-class limits remain (list above).
