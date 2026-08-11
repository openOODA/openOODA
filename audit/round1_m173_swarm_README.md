# M173 audit — swarm disposition (recoverability stub)

**Round:** M173
**Date:** 2026-08-11 (approx.; board commit `bc11776`)
**Scope:** Swarm disposition of Issues #11–#14 and partial #6/#7 (typecheck control-cond, typecheck rails, migrate disable, SPEC honesty, monofile splits, first paren batch).

## Provenance note (RULES §1.9)

Full subagent session JSON for this round is not recoverable from disk. Board dispositions were transcribed into `SPRINT.md` (see closed tables and the M173 disposition commit message). This file exists so the audit pipeline has a durable round marker.

## Session findings

Session findings persisted for recoverability; see SPRINT closed tables for dispositions. Do not treat this stub as a substitute for the original subagent report bodies.

## Known closed dispositions (from SPRINT / board history — not re-audited here)

| # | Item | Status (as closed on board) |
|---|------|------------------------------|
| 11 | `if field.chain == false` control cond | FIXED (`ooda` `ff0187d`) |
| 12 | typecheck bug rails | FIXED path A (`ooda` `de59bc0`) |
| 13 | critical doc honesty (5 claims) | FIXED (SPEC/DESIGN STATUS tags) |
| 14 | migrate sed rewrite | FIXED (fail-closed disabled) |
| 6 | `&Struct` paren field access | partial this round — perf + priority sec/sys (`std` `899815b`) |
| 7 | over-600 splits | partial — mtls/waf/wireguard/jwt/… + collision/kinematics |

No new findings invented for this stub. Residual long-tail work continued in later rounds.
