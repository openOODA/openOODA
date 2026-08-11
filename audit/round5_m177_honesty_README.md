# M177 audit round 5 — process-hygiene README

**Round:** M177 (3 subagents in parallel)
**Date:** 2026-08-11
**Subagents spawned:** 3 (read-only)
**Scope:** Public-facing READMEs, test runners, Grok fix-commit cross-check

## Findings (Issues added to SPRINT.md)

- Issue #44 (CRITICAL): `.github/profile/README.md` still has 5 hard false claims — `cargo build/release`, JIT, LLVM release, 0ms GC, AI auto-fix. Public org face is misleading.
- Issue #45 (HIGH): `install.sh` and `install` are one release behind (`v0.183.0-alpha` vs actual `v0.184.0-alpha`).
- Issue #46 (MEDIUM): `ooda/README.md` is an honesty gap by omission (residual table expected but missing).
- Issue #47 (MEDIUM): `openOODA.github.io/research.html` has dead "Playground" link.
- Issue #48 (LOW): `docs/index.html` and `docs/docs/{getting-started,security,performance}.md` version drift.
- Issue #49 (MEDIUM): `qa/qa_module_check.py` referenced in docs but missing.
- Issue #50 (HIGH): 5 false-pass risks in test runners (RULES §1.6 violations).
- Issue #51 (MEDIUM): 6 weak/soft-pass assertions in test runners.
- Issue #52 (MEDIUM): Counters broken across master/e2e.
- Issue #53 (LOW): Coverage claim "100%" is false.
- Issue #54 (LOW): Grok's commit `88baccd` (Issue #13) is partial close.
- Issue #55 (LOW): Grok's `de59bc0` path drift.

## Provenance note (RULES §1.9)

Subagent reports in this session lived in `~/.grok/sessions/<session_id>/subagents/<id>/output.json` (session-coupled JSON, not durable). The orchestrator transcribed the findings inline into SPRINT.md:161-268. This README persists the round 5 audit output to disk for future recovery.

## Recommended follow-up (for round 6, if any)

The audit itself is healthy; the audit *process* is fragile. The single highest-value next action is to add a CI gate that requires this file to exist for every "Issue #NN" cited in SPRINT.md's audit sections. That's a one-line shell check.

## Files inspected (read-only)

- `/home/jeryd/Projects/openOODA/.github/profile/README.md`
- `/home/jeryd/Projects/openOODA/openOODA.github.io/install.sh`
- `/home/jeryd/Projects/openOODA/openOODA.github.io/install`
- `/home/jeryd/Projects/openOODA/openOODA.github.io/index.html`
- `/home/jeryd/Projects/openOODA/openOODA.github.io/research.html`
- `/home/jeryd/Projects/openOODA/openOODA/README.md`
- `/home/jeryd/Projects/openOODA/openOODA/SPEC.md`
- `/home/jeryd/Projects/openOODA/openOODA/DESIGN.md`
- `/home/jeryd/Projects/openOODA/openOODA/SPRINT.md`
- `/home/jeryd/Projects/openOODA/openOODA/PM.md`
- `/home/jeryd/Projects/openOODA/README.md`
- `/home/jeryd/Projects/openOODA/ooda/README.md`
- `/home/jeryd/Projects/openOODA/.github/README.md`
- `/home/jeryd/Projects/openOODA/docs/README.md`
- `/home/jeryd/Projects/openOODA/qa/README.md`
- `/home/jeryd/Projects/openOODA/helloworld/README.md`
- `/home/jeryd/Projects/openOODA/brand/README.md`
- `/home/jeryd/Projects/openOODA/odaa/README.md` (does not exist; `ooda/README.md` audited)
- `/home/jeryd/Projects/openOODA/qa/qa_runner.sh`
- `/home/jeryd/Projects/openOODA/qa/qa_harness_common.sh`
- `/home/jeryd/Projects/openOODA/qa/qa_phase{1_4,5a,5b,6_8}.sh`
- `/home/jeryd/Projects/openOODA/qa/e2e/e2e_harness_common.sh`
- `/home/jeryd/Projects/openOODA/qa/e2e/e2e_assertions.sh`
- `/home/jeryd/Projects/openOODA/qa/e2e/tier{1,2,3,4}/t{1,2,3,4}_*.sh`
- `.git/logs/HEAD` for the monorepo and the `qa/` and `ooda/` submodules

No files were modified by this audit.
