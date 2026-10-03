"""
Tier 1: Feature Coverage — Requirement R5 (Check Cache Reactivation & Governance Hardening)
Tests T1.R5.1 through T1.R5.5
"""

import os
import time
from openOODA.qa.e2e.framework import TestContext, TestResult, oodac_check, OODAC_BIN, POLYROOT


def test_t1_r5_1_check_cache_subsecond_hit(double_run: bool = False) -> TestResult:
    """T1.R5.1: Verify check_cache_hit achieves sub-second warm re-checks."""
    ctx = TestContext("T1.R5.1", 1, "R5", "Sub-second warm check cache hit", double_run)
    target = os.path.join(POLYROOT, "oodac/check/check_cache.oo")
    if not os.path.exists(target):
        return TestResult(ctx.test_id, 1, "R5", ctx.name, "FAIL", 0, error_msg=f"Missing {target}")

    # First run (warmup / cache population)
    rc1, out1, err1 = oodac_check(ctx, target)
    if rc1 != 0:
        return TestResult(ctx.test_id, 1, "R5", ctx.name, "FAIL", 0, error_msg="Initial check failed", diagnostic=err1)

    # Second run (measured warm check)
    t0 = time.time()
    rc2, out2, err2 = oodac_check(ctx, target)
    duration_sec = time.time() - t0
    duration_ms = duration_sec * 1000

    if rc2 == 0 and "OK" in out2 and duration_sec < 1.0:
        return TestResult(ctx.test_id, 1, "R5", ctx.name, "PASS", duration_ms)
    else:
        return TestResult(
            ctx.test_id, 1, "R5", ctx.name, "FAIL", duration_ms,
            error_msg=f"Warm check exceeded 1.0s SLA or failed: duration={duration_sec:.4f}s, rc={rc2}",
            diagnostic=f"out={out2}, err={err2}"
        )


def test_t1_r5_2_polyrepo_qa_cli_integration(double_run: bool = False) -> TestResult:
    """T1.R5.2: Verify cli/qa/suite.oo is included in openOODA/qa/polyrepo_suite.oo dispatch list."""
    ctx = TestContext("T1.R5.2", 1, "R5", "Polyrepo QA suite includes cli/qa/suite.oo", double_run)
    suite_file = os.path.join(POLYROOT, "openOODA/qa/polyrepo_suite.oo")
    if not os.path.exists(suite_file):
        return TestResult(ctx.test_id, 1, "R5", ctx.name, "FAIL", 0, error_msg=f"Missing {suite_file}")

    with open(suite_file, "r", encoding="utf-8") as f:
        content = f.read()

    has_cli_suite = 'list_push(suites, "cli/qa/suite.oo")' in content or '"cli/qa/suite.oo"' in content
    duration = (time.time() - ctx.start_time) * 1000

    if has_cli_suite:
        return TestResult(ctx.test_id, 1, "R5", ctx.name, "PASS", duration)
    else:
        return TestResult(
            ctx.test_id, 1, "R5", ctx.name, "FAIL", duration,
            error_msg="openOODA/qa/polyrepo_suite.oo is missing cli/qa/suite.oo in its test suite list"
        )


def test_t1_r5_3_size_linter_execution(double_run: bool = False) -> TestResult:
    """T1.R5.3: Verify openOODA/qa/lint_oo_size.sh executes and produces lint inventory."""
    ctx = TestContext("T1.R5.3", 1, "R5", "Size linter execution and inventory generation", double_run)
    linter_sh = os.path.join(POLYROOT, "openOODA/qa/lint_oo_size.sh")
    if not os.path.exists(linter_sh):
        return TestResult(ctx.test_id, 1, "R5", ctx.name, "FAIL", 0, error_msg=f"Missing {linter_sh}")

    rc, out, err = ctx.run_cmd(["bash", linter_sh], cwd=POLYROOT)
    duration = (time.time() - ctx.start_time) * 1000

    has_header = "# .oo size lint inventory" in out
    has_violations_line = "violations: BIGFILE=" in out

    if has_header and has_violations_line:
        return TestResult(ctx.test_id, 1, "R5", ctx.name, "PASS", duration)
    else:
        return TestResult(
            ctx.test_id, 1, "R5", ctx.name, "FAIL", duration,
            error_msg="lint_oo_size.sh did not produce valid inventory output",
            diagnostic=f"rc={rc}\nout={out[:500]}\nerr={err[:500]}"
        )


def test_t1_r5_4_resource_scorecard_bounds(double_run: bool = False) -> TestResult:
    """T1.R5.4: Verify module check satisfies quantitative bounds (<= 64MB RSS, <= 3.0s CPU)."""
    ctx = TestContext("T1.R5.4", 1, "R5", "Quantitative resource bounds (<=64MB RSS, <=3.0s CPU)", double_run)
    target = os.path.join(POLYROOT, "std/sec/hash/sha512.oo")

    rc, out, err, cpu_sec, rss_kb = ctx.run_cmd_measured(
        [OODAC_BIN, "check", target],
        cwd=POLYROOT
    )
    duration = (time.time() - ctx.start_time) * 1000
    rss_mb = rss_kb / 1024.0

    if rc == 0 and rss_mb <= 64.0 and cpu_sec <= 3.0:
        return TestResult(ctx.test_id, 1, "R5", ctx.name, "PASS", duration)
    else:
        return TestResult(
            ctx.test_id, 1, "R5", ctx.name, "FAIL", duration,
            error_msg=f"Resource bounds exceeded: RSS={rss_mb:.1f}MB (limit 64MB), CPU={cpu_sec:.2f}s (limit 3.0s)",
            diagnostic=f"rc={rc}\nout={out}\nerr={err}"
        )


def test_t1_r5_5_root_std_anchor_check(double_run: bool = False) -> TestResult:
    """T1.R5.5: Verify root std/anchor.oo check passes clean with exit code 0."""
    ctx = TestContext("T1.R5.5", 1, "R5", "Root std/anchor.oo clean check", double_run)
    # Pre-stage 8 domain anchors to isolate memory and populate typed artifacts
    domains = ["core", "fs", "net", "sec", "science", "app", "hw", "meta"]
    for d in domains:
        rc_d, out_d, err_d = ctx.run_cmd([OODAC_BIN, "check", f"{d}/anchor.oo"], cwd=os.path.join(POLYROOT, "std"), timeout=300)
        if rc_d != 0:
            return TestResult(ctx.test_id, 1, "R5", ctx.name, "FAIL", 0, error_msg=f"Domain pre-check {d}/anchor.oo failed", diagnostic=err_d)

    rc, out, err = ctx.run_cmd(
        [OODAC_BIN, "check", "anchor.oo"],
        cwd=os.path.join(POLYROOT, "std"),
        timeout=600
    )
    duration = (time.time() - ctx.start_time) * 1000

    if rc == 0 and "OK" in out:
        return TestResult(ctx.test_id, 1, "R5", ctx.name, "PASS", duration)
    else:
        return TestResult(
            ctx.test_id, 1, "R5", ctx.name, "FAIL", duration,
            error_msg="Root std/anchor.oo check failed",
            diagnostic=f"rc={rc}\nout={out}\nerr={err}"
        )
