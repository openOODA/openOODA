# openOODA sprint

## Pin
| Item | Value |
|------|--------|
| Release | `v0.184.0-alpha` (stay alpha) |
| Focus | M162 residual-named deepen (not beta) |
| Rails | m162_residual_deepen, libfloor_*, crypto_md5_sha1, hitl_product, etc_autofix, contracts_and |
| Beta | **Not claimed** |

## Closed
**M158** E_TC undefined-var `ooda fix`  
**M159** simple `&&` contracts  
**M160** Secret `eprintln` sink  
**M161** Library residuals path A  
**M162** Residual-named open items path A deepen — see below  

## M162 Residual-named deepen (path A)

| Item | What we did | Still not done (plain English) |
|------|-------------|-------------------------------|
| Multi-code autofix | `ooda fix` multi-pass E_CAP + E_TC | Other error codes; free-form rewrite |
| SMT / contracts | Simple `\|\|` runtime requires/ensures | Full SMT / quantifiers / old-state |
| Interactive HITL | Allow env + auto-approve without TTY; line-scan fix | Full human harness / record-replay |
| OS dlopen | Real `dlopen` only with allowlist env + dir | Free OS load of any path / full FFI |
| TLS | Still residual seal | Real TLS handshake |
| AES | AES-128-ECB for 16-byte blocks | Full AES modes / padding / product API |
| Threads | Real pthread mutex + spawn (noop) | Join / channels / fearless concurrency |
| GPU | Still residual seal | Real shaders |
| Byte / `&str` | `byte_at` raw 0..255 | Borrowed `&str`, true Byte arrays |
| Tier C moonshots | Still default-deny free names | Full moonshot products |

## Residual named (still open for full product)
SMT quantifiers · multi-code beyond E_CAP/E_TC · full HITL harness · unrestricted OS dlopen · full TLS · full AES · full threads/GPU · native `&str`/Byte arrays · Tier C moonshots  
Beta not claimed

## S
`S: low — U=0 on M162 F=0 W=0 O=0`
