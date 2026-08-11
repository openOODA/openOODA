# openOODA sprint

## Pin
| Item | Value |
|------|--------|
| Release | `v0.184.0-alpha` (stay alpha) |
| Focus | M163 next residual deepen — TLS / join / bytes (not beta) |
| Rails | thread_join, byte_str_path_a, tls_path_a, libfloor_*, m162, hitl, contracts_and |
| Beta | **Not claimed** |

## Closed
**M158–M162** as prior  
**M163** TLS + joinable threads + byte slice path A — see below  

## M163 next residual deepen (path A) — 3 swarms

| Swarm | Item | What we did | Still not done (plain English) |
|-------|------|-------------|-------------------------------|
| **T** | TLS | TCP first, then residual `OpenSSL not linked`; opt-in insecure TCP; OpenSSL client when headers present | Full TLS product on this host (no OpenSSL installed) |
| **J** | Joinable threads | `thread_spawn` → `tid:N`, `thread_join(slot)` waits on pthread | Channels, thread pools, fearless concurrency DESIGN |
| **B** | Byte / string bytes | `bytes_len`, `byte_slice` (owned byte copy), `bytes_eq` + `byte_at` | True borrowed `&str` / lifetimes / `List[Byte]` ABI |

## Residual named (still open for full product)
SMT quantifiers · multi-code beyond E_CAP/E_TC · full HITL harness · unrestricted OS dlopen · **OpenSSL-linked TLS** · full AES modes · channels/GPU · native `&str` lifetimes · Tier C moonshots  
Beta not claimed

## S
`S: low — U=0 on M163 F=0 W=0 O=0`
