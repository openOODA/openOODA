# openOODA sprint

## Pin
| Item | Value |
|------|--------|
| Release | `v0.184.0-alpha` (stay alpha) |
| Focus | M161 library residuals path A (not Tier C / not beta) |
| Rails | assert_eq_result, crypto_md5_sha1, libfloor_*, std_semver/markup/archive, byte_str residual, etc_autofix, contracts_and, std_smoke, secret_eprintln |
| Beta | **Not claimed** |

## Closed
**M158** E_TC undefined-var `ooda fix`  
**M159** simple `&&` contracts product rails + std `res_map_ok_prefix` / `res_ok_eq`  
**M160** Secret `eprintln` sink depth  
**M161** Library residuals path A (25-agent backlog) — see below

## M161 Library Residuals — path A closed

| Swarm | Item | Path A | Residual honesty |
|-------|------|--------|------------------|
| s1 | Result `assert_eq!` / `OoResS` structural eq | C `oo_res_eq` + LLVM extractvalue; `assert_eq_result_smoke` | generic `Result[T,E]` not lowered |
| s2 | Byte / `&str` | residual pack + `std/byte.oo` Int convention; `byte_str_residual_smoke` | no native borrow / Byte arrays |
| s3–s6 | ThreadCap / GpuCap / mutex / thread_spawn / gpu_launch | grant+seal+runtime Err residual; dual forge deny | no OS pthreads / GPU shaders |
| s4 | MD5 / SHA-1 / AES | real MD5+SHA1 hex; AES `STUB_FAIL_CLOSED` | no AES product crypto |
| s5 | TCP / UDP / TLS | NetCap seal + residual Err | no real sockets/TLS |
| s7 | sys_spawn / wait / kill | SysCap seal + residual Err; real work via `sys_exec` | no fork/wait/kill product on residual names |
| s8 | `std/semver` | pure major.minor.patch | prerelease/build residual |
| s9 | markup TOML/YAML/XML/JSON Schema | tiny subsets + residual | full parsers residual |
| s10 | archive tar/zip/gzip | magic-detect only | full decompress residual |

## Residual named (still open)
SMT contracts · multi-code autofix · interactive HITL · OS dlopen · full TLS/AES/threads/GPU · native `&str`/Byte arrays · Tier C moonshots  
Beta not claimed

## S
`S: low — U=0 on M161 F=0 W=0 O=0`
