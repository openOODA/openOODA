# M176 audit round 4 — e2e / doc honesty / harness (recoverability)

**Round:** M176 (3 subagents in parallel)
**Date:** 2026-08-11
**Scope:** Weakest e2e tier scripts, top doc-vs-tree gaps, test-corpus quality. Findings were transcribed into `SPRINT.md` before the M178 closeout rewrite.

## Provenance note (RULES §1.9)

Subagent reports for this round lived in session-coupled storage, not durable disk, until this recoverability file. Primary dispositions remain in SPRINT closed tables. The detailed issue bodies below are recovered from the pre-closeout SPRINT board text (`d9a3ab5^`), not invented.

## Findings (Issues #40–#43) — summary

| Issue | Severity | Disposition (board) |
|-------|----------|---------------------|
| **#40** soft-pass e2e | HIGH | **FIXED** — pure soft-pass tier scripts deleted (`qa` `c97b281`) |
| **#41** loose e2e | MEDIUM | **FIXED** — fail-closed targets; empty/wrong output fails (`qa` `372c489`) |
| **#42** doc-vs-tree | HIGH | **FIXED** — 10 honesty `[STATUS:]` tags (`openOODA` `4c0c9d4`) |
| **#43** harness quality | MEDIUM | **FIXED** — phase5a jq, expect_fail signature, wasm no soft-pass (`qa` `52a016e`) |

Also closed in the same wave (not all from this audit): Issue #15 monofile shims, Issue #7 remainder shims, Issue #6 remainder paren batch (crypto/cps/fin/bio). Leftover #6 domains listed residual.

## Session findings

Session findings persisted for recoverability; see SPRINT closed tables for dispositions. Full per-file lists for #40–#43 lived in the board’s “M176 audit round 4” section prior to closeout compaction.

## Recommended follow-up

- Keep this round’s README required by CI alongside M177.
- Continue leftover Issue #6 domains separately (Issue #60).
