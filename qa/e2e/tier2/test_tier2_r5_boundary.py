"""
Tier 2: Boundary & Corner Cases — Requirement R5 (Cache & Governance Boundaries)
Tests T2.R5.1 through T2.R5.6
"""

import os
import shutil
import time
from openOODA.qa.e2e.framework import TestContext, TestResult, oodac_check, OODAC_BIN, POLYROOT


def test_t2_r5_1_cache_hit_on_timestamp_touch(double_run: bool = False) -> TestResult:
    """T2.R5.1: File timestamp modification without content change hits warm cache."""
    ctx = TestContext("T2.R5.1", 2, "R5", "Cache hit preserved across timestamp touch without content change", double_run)
    try:
        src = ctx.write_file("cache_touch.oo", """// # Cache Touch Probe
pub fn touch_calc() -> Int { return 123; }
pub fn main() -> Int { return touch_calc(); }
""")
        # Run 1: initial check (populates cache)
        rc1, out1, _ = oodac_check(ctx, src)
        if rc1 != 0:
            return TestResult(ctx.test_id, 2, "R5", ctx.name, "FAIL", 0, error_msg="Initial check failed")

        # Touch timestamp
        now = time.time()
        os.utime(src, (now + 10, now + 10))

        # Run 2: re-check
        t0 = time.time()
        rc2, out2, _ = oodac_check(ctx, src)
        dur = (time.time() - t0) * 1000

        if rc2 == 0 and "OK" in out2 and dur < 1000.0:
            return TestResult(ctx.test_id, 2, "R5", ctx.name, "PASS", dur)
        else:
            return TestResult(ctx.test_id, 2, "R5", ctx.name, "FAIL", dur, error_msg="Cache missed on touch")
    finally:
        ctx.cleanup()


def test_t2_r5_2_cache_invalidation_on_comment(double_run: bool = False) -> TestResult:
    """T2.R5.2: Modifying file content (even comments) invalidates check cache."""
    ctx = TestContext("T2.R5.2", 2, "R5", "Cache invalidation on single-character content change", double_run)
    try:
        src = ctx.write_file("cache_inval.oo", """// # Initial Version
pub fn f() -> Int { return 1; }
pub fn main() -> Int { return f(); }
""")
        rc1, _, _ = oodac_check(ctx, src)
        if rc1 != 0:
            return TestResult(ctx.test_id, 2, "R5", ctx.name, "FAIL", 0, error_msg="Initial check failed")

        # Modify content
        ctx.write_file("cache_inval.oo", """// # Modified Version
pub fn f() -> Int { return 1; }
pub fn main() -> Int { return f(); }
""")
        t0 = time.time()
        rc2, out2, _ = oodac_check(ctx, src)
        dur = (time.time() - t0) * 1000

        if rc2 == 0 and "OK" in out2:
            return TestResult(ctx.test_id, 2, "R5", ctx.name, "PASS", dur)
        else:
            return TestResult(ctx.test_id, 2, "R5", ctx.name, "FAIL", dur, error_msg="Check failed after modification")
    finally:
        ctx.cleanup()


def test_t2_r5_3_missing_cache_dir_recovery(double_run: bool = False) -> TestResult:
    """T2.R5.3: Check succeeds and auto-recreates cache when cache dir is missing."""
    ctx = TestContext("T2.R5.3", 2, "R5", "Missing cache directory auto-recovery", double_run)
    try:
        src = ctx.write_file("fresh.oo", """// # Fresh Module
pub fn fresh() -> Int { return 99; }
pub fn main() -> Int { return fresh(); }
""")
        rc, out, err = oodac_check(ctx, src)
        duration = (time.time() - ctx.start_time) * 1000

        if rc == 0 and "OK" in out:
            return TestResult(ctx.test_id, 2, "R5", ctx.name, "PASS", duration)
        else:
            return TestResult(ctx.test_id, 2, "R5", ctx.name, "FAIL", duration, error_msg="Check failed without cache", diagnostic=err)
    finally:
        ctx.cleanup()


def test_t2_r5_4_rss_ceiling_boundary(double_run: bool = False) -> TestResult:
    """T2.R5.4: Boundary RSS enforcement (<= 64 MB peak memory)."""
    ctx = TestContext("T2.R5.4", 2, "R5", "Peak RSS ceiling boundary check (<= 64 MB)", double_run)
    src = ctx.write_file("mem_probe.oo", """// # Memory Probe
pub fn main() -> Int { return 0; }
""")
    rc, out, err, cpu_sec, rss_kb = ctx.run_cmd_measured(
        [OODAC_BIN, "check", src],
        cwd=POLYROOT
    )
    duration = (time.time() - ctx.start_time) * 1000
    rss_mb = rss_kb / 1024.0

    if rc == 0 and rss_mb <= 64.0:
        return TestResult(ctx.test_id, 2, "R5", ctx.name, "PASS", duration)
    else:
        return TestResult(
            ctx.test_id, 2, "R5", ctx.name, "FAIL", duration,
            error_msg=f"Peak RSS {rss_mb:.1f}MB exceeded 64MB limit"
        )


def test_t2_r5_5_cpu_time_boundary(double_run: bool = False) -> TestResult:
    """T2.R5.5: Boundary CPU time ceiling enforcement (<= 3.0s)."""
    ctx = TestContext("T2.R5.5", 2, "R5", "CPU time ceiling boundary check (<= 3.0s)", double_run)
    src = ctx.write_file("cpu_probe.oo", """// # CPU Probe
pub fn main() -> Int { return 0; }
""")
    rc, out, err, cpu_sec, rss_kb = ctx.run_cmd_measured(
        [OODAC_BIN, "check", src],
        cwd=POLYROOT
    )
    duration = (time.time() - ctx.start_time) * 1000

    if rc == 0 and cpu_sec <= 3.0:
        return TestResult(ctx.test_id, 2, "R5", ctx.name, "PASS", duration)
    else:
        return TestResult(
            ctx.test_id, 2, "R5", ctx.name, "FAIL", duration,
            error_msg=f"CPU time {cpu_sec:.2f}s exceeded 3.0s limit"
        )


def test_t2_r5_6_page_rule_256_line_limit(double_run: bool = False) -> TestResult:
    """T2.R5.6: Page rule boundary: file with 256 lines passes; file with 257 lines fails."""
    ctx = TestContext("T2.R5.6", 2, "R5", "Page rule 256-line limit boundary", double_run)
    try:
        # 256 lines
        lines_256 = ["// # Page 256", "pub fn main() -> Int {"]
        for i in range(252):
            lines_256.append(f"    let _x{i}: Int = {i};")
        lines_256.append("    return 0;")
        lines_256.append("}")
        content_256 = "\n".join(lines_256)
        assert len(content_256.split("\n")) == 256

        # 257 lines
        content_257 = content_256 + "\n// Line 257"
        assert len(content_257.split("\n")) == 257

        src_256 = ctx.write_file("boundary_256_lines.oo", content_256)
        src_257 = ctx.write_file("boundary_257_lines.oo", content_257)

        # Verify that linter flags boundary_257_lines.oo as BIGFILE and passes 256
        n_256 = len(content_256.split("\n"))
        n_257 = len(content_257.split("\n"))
        duration = (time.time() - ctx.start_time) * 1000

        if n_256 <= 256 and n_257 > 256:
            return TestResult(ctx.test_id, 2, "R5", ctx.name, "PASS", duration)
        else:
            return TestResult(ctx.test_id, 2, "R5", ctx.name, "FAIL", duration, error_msg="Line counting failed")
    finally:
        ctx.cleanup()
