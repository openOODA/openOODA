# openOODA sprint

## Pin
| Item | Value |
|------|--------|
| Release | `v0.184.0-alpha` (stay alpha) |
| Focus | M164 finish residual trio — TLS / channels / byte buffer |
| Rails | tls_path_a, channel_path_a, bytes_buffer, thread_join, byte_str_path_a |
| Beta | **Not claimed** |

## Closed
**M158–M163** as prior  
**M164** Finish residual trio path A — see below  

## M164 finish residual items (path A) — 3 workstreams

| Item | Finished as | Residual honesty |
|------|-------------|------------------|
| **TLS** | Real client handshake via system `libssl.so.3` (local decls, no headers needed); NetCap sealed | Full cert policy / mTLS / session reuse still residual |
| **Channels** | `channel_new` / `send` / `recv` under ThreadCap (process-local queue) | `actor_spawn` residual; multi-process channels residual |
| **Byte buffer** | `List[Int]` 0..255 buffer + `bytes_to_str` / concat / from_str | True `&str` borrow / `List[Byte]` ABI residual |

## Residual named (still open for full DESIGN)
SMT quantifiers · multi-code beyond E_CAP/E_TC · full HITL harness · unrestricted OS dlopen · actors · GPU shaders · native `&str` lifetimes · Tier C moonshots  
Beta not claimed

## S
`S: low — U=0 on M164 F=0 W=0 O=0`
