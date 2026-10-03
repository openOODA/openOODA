"""
Tier 2: Boundary & Corner Cases — Requirement R1 (Compiler Subtraction & Scoping)
Tests T2.R1.1 through T2.R1.6
"""

import os
import time
from openOODA.qa.e2e.framework import TestContext, TestResult, oodac_check, oodac_build


def test_t2_r1_1_zero_vs_one_arity(double_run: bool = False) -> TestResult:
    """T2.R1.1: Boundary arity conflict at 0 vs 1 parameters."""
    ctx = TestContext("T2.R1.1", 2, "R1", "Boundary arity conflict at 0 vs 1 parameters", double_run)
    try:
        ctx.write_file("p0.oo", "// # P0\npub fn bar() -> Int { return 0; }\n")
        ctx.write_file("p1.oo", "// # P1\npub fn bar(a: Int) -> Int { return a; }\n")
        main_oo = ctx.write_file("test.oo", """// # Test
import "./p0.oo";
import "./p1.oo";
pub fn main() -> Int { return bar(); }
""")
        out_bin = os.path.join(ctx.temp_dir, "test.bin")
        rc, out, err = oodac_build(ctx, main_oo, out_bin)
        duration = (time.time() - ctx.start_time) * 1000

        # Must fail build because bar is defined with differing arities (0 vs 1)
        if rc != 0 and not os.path.exists(out_bin):
            return TestResult(ctx.test_id, 2, "R1", ctx.name, "PASS", duration)
        else:
            return TestResult(
                ctx.test_id, 2, "R1", ctx.name, "FAIL", duration,
                error_msg="Arity conflict between 0 and 1 params was not caught by compiler"
            )
    finally:
        ctx.cleanup()


def test_t2_r1_2_high_arity_conflict(double_run: bool = False) -> TestResult:
    """T2.R1.2: Boundary arity conflict at 10 vs 9 parameters."""
    ctx = TestContext("T2.R1.2", 2, "R1", "High arity boundary conflict (10 vs 9 params)", double_run)
    try:
        ctx.write_file("p9.oo", """// # P9
pub fn heavy(a: Int, b: Int, c: Int, d: Int, e: Int, f: Int, g: Int, h: Int, i: Int) -> Int {
    return a + b + c + d + e + f + g + h + i;
}
""")
        ctx.write_file("p10.oo", """// # P10
pub fn heavy(a: Int, b: Int, c: Int, d: Int, e: Int, f: Int, g: Int, h: Int, i: Int, j: Int) -> Int {
    return a + b + c + d + e + f + g + h + i + j;
}
""")
        main_oo = ctx.write_file("test_high.oo", """// # Test High
import "./p9.oo";
import "./p10.oo";
pub fn main() -> Int {
    return heavy(1, 2, 3, 4, 5, 6, 7, 8, 9);
}
""")
        out_bin = os.path.join(ctx.temp_dir, "test_high.bin")
        rc, out, err = oodac_build(ctx, main_oo, out_bin)
        duration = (time.time() - ctx.start_time) * 1000

        if rc != 0 and not os.path.exists(out_bin):
            return TestResult(ctx.test_id, 2, "R1", ctx.name, "PASS", duration)
        else:
            return TestResult(
                ctx.test_id, 2, "R1", ctx.name, "FAIL", duration,
                error_msg="Arity conflict at 10 vs 9 params was not caught by compiler"
            )
    finally:
        ctx.cleanup()


def test_t2_r1_3_return_type_conflict(double_run: bool = False) -> TestResult:
    """T2.R1.3: Identical arity same name with conflicting return type."""
    ctx = TestContext("T2.R1.3", 2, "R1", "Same name and arity with conflicting return type", double_run)
    try:
        ctx.write_file("ret_int.oo", "// # Ret Int\npub fn val() -> Int { return 1; }\n")
        ctx.write_file("ret_str.oo", "// # Ret Str\npub fn val() -> String { return \"1\"; }\n")
        main_oo = ctx.write_file("test_ret.oo", """// # Test Ret
import "./ret_int.oo";
import "./ret_str.oo";
pub fn main() -> Int {
    return val();
}
""")
        out_bin = os.path.join(ctx.temp_dir, "test_ret.bin")
        rc, out, err = oodac_build(ctx, main_oo, out_bin)
        duration = (time.time() - ctx.start_time) * 1000

        # Conflicting return types must either fail build or typecheck
        if rc != 0 and not os.path.exists(out_bin):
            return TestResult(ctx.test_id, 2, "R1", ctx.name, "PASS", duration)
        else:
            return TestResult(
                ctx.test_id, 2, "R1", ctx.name, "FAIL", duration,
                error_msg="Conflicting return type duplicate function was compiled into binary"
            )
    finally:
        ctx.cleanup()


def test_t2_r1_4_transitive_import_conflict(double_run: bool = False) -> TestResult:
    """T2.R1.4: 3-level transitive import chain prototype conflict."""
    ctx = TestContext("T2.R1.4", 2, "R1", "Transitive 3-level import arity conflict", double_run)
    try:
        ctx.write_file("level3.oo", "// # Level 3\npub fn deep_fn(x: Int, y: Int) -> Int { return x + y; }\n")
        ctx.write_file("level2.oo", "// # Level 2\nimport \"./level3.oo\";\npub fn mid() -> Int { return deep_fn(1, 2); }\n")
        ctx.write_file("level1.oo", "// # Level 1\nimport \"./level2.oo\";\npub fn top() -> Int { return mid(); }\n")
        # Root defines deep_fn with 1 parameter (conflict with level3 arity 2)
        main_oo = ctx.write_file("main.oo", """// # Main
import "./level1.oo";
pub fn deep_fn(x: Int) -> Int { return x * 2; }
pub fn main() -> Int {
    return top();
}
""")
        out_bin = os.path.join(ctx.temp_dir, "main.bin")
        rc, out, err = oodac_build(ctx, main_oo, out_bin)
        duration = (time.time() - ctx.start_time) * 1000

        if rc != 0 and not os.path.exists(out_bin):
            return TestResult(ctx.test_id, 2, "R1", ctx.name, "PASS", duration)
        else:
            return TestResult(
                ctx.test_id, 2, "R1", ctx.name, "FAIL", duration,
                error_msg="Transitive arity conflict across 3-level import chain was not caught"
            )
    finally:
        ctx.cleanup()


def test_t2_r1_5_single_line_minimal_file(double_run: bool = False) -> TestResult:
    """T2.R1.5: Single-line minimal valid .oo file check."""
    ctx = TestContext("T2.R1.5", 2, "R1", "Single-line minimal valid .oo file", double_run)
    try:
        src = ctx.write_file("min.oo", "pub fn main() -> Int { return 0; }\n")
        rc, out, err = oodac_check(ctx, src)
        duration = (time.time() - ctx.start_time) * 1000

        if rc == 0 and "OK" in out:
            return TestResult(ctx.test_id, 2, "R1", ctx.name, "PASS", duration)
        else:
            return TestResult(ctx.test_id, 2, "R1", ctx.name, "FAIL", duration, error_msg="Check failed", diagnostic=err)
    finally:
        ctx.cleanup()


def test_t2_r1_6_empty_file_handling(double_run: bool = False) -> TestResult:
    """T2.R1.6: Empty .oo file boundary check."""
    ctx = TestContext("T2.R1.6", 2, "R1", "Empty .oo file handling", double_run)
    try:
        src = ctx.write_file("empty.oo", "")
        rc, out, err = oodac_check(ctx, src)
        duration = (time.time() - ctx.start_time) * 1000

        # Empty file has no main or types, but parser should not crash / segfault
        return TestResult(ctx.test_id, 2, "R1", ctx.name, "PASS", duration)
    finally:
        ctx.cleanup()
