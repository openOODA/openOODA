# openOODA sprint

## Pin
| Item | Value |
|------|--------|
| Release | `v0.184.0-alpha` (stay alpha) |
| Focus | Pure multi self-host dual-green residual |
| Tip (product `ooda`) | `adeb3c9` (host binary still m174-class; source free-name ahead of host) |
| Tip (monorepo boards) | (this file) |
| Beta | **Not claimed** |

## Path A closed (do not re-open)
M158–M172 path A language floors · product residual smokes (m169, agy_lang_blockers, cap_forge, m167, bitwise, malloc) · M171 untyped-let SEGV · M172 token CLI.

**This rotation also closed path-A noise:** wrong `let mut e: Int = env` in emit (ident/block) → `String`; free-name String table expanded in sources for typecheck/env helpers.

## Open work (path A)

### 1. Pure multi self-host dual-green
**Status:** residual — not dual-green.

| Fact | Detail |
|------|--------|
| Product floors | Residual smokes exit 0 on tip host |
| Pure rebuild | `scripts/oodac_pure_build.sh oodac/main.oo` → gcc fails |
| Root class | Host tip emits cross-module String returns as `long long` (no cross-module `__fr__` map). Free-name table lives in **source** (`c_emit_let_ext.oo`); host binary must be rebuilt with that table before pure all.c types clean. |
| Progress | `long long e = env` eliminated (annotation fix). Source free-name table covers `resolve_type_alias`, `indent`, `build_*_table`, … Mechanical hostfix of pure all.c still ~200 gcc errs (ilist_get / concat residual). Bootstrap seed too old for current `main.oo`. |
| Done when | Pure rebuild produces executable that re-emits core modules without SEGV; product smokes still green |
| Out of scope | Bit-identical fixed-point forever; cold start from air |

**Evidence:** pure_rebuild.log / hostfix_gcc.err in agent SCRATCH. Prefer `ooda err-digest` — do not paste full `all.c`.

### 2. sec/net check residual (import-graph quota)
| Item | State |
|------|--------|
| `dnssec*` | Split ≤256 lines; **`DnssecRecord` type alias added**; evaluate uses `is_valid` field. **OK** under `OO_LIST_AMBIENT_QUOTA≥1GiB`. Default ambient may `ERRcap` on import-heavy check. |
| `ipsec*` | Split into types/selector/sa/ike/policy/… shims. **OK** under high ambient. |

**Done when:** `oodac check` green under product default ambient (or documented smoke-only quota without claiming lock compliance).

## Residual named (full DESIGN — not this path A)
Full SMT/quantifiers · free-form multi-code · full HITL · actor supervision · real GPU · unrestricted dlopen · native `&str` · nested `List[Struct]` · product `&mut T` · object-cap crypto / cast surface beyond path-A refuse · SOCK_RAW · full async epoll/inotify · OS rlimit heap · Tier C (temporal/hive/hot-reload/LSP/…)

**Cap forgery:** path A refuse green (`cap_forge_path_a`); object-caps DESIGN residual.

Beta not claimed.

## Library wave honesty
`std/` + `sec/*` path-A stub/check pattern stands. Do not re-list AGY “Currently missing” language floors (closed M166–M169).
