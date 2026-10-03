"""
Tier 1: Feature Coverage — Requirement R1 (Compiler Subtraction & Scoping)
Tests T1.R1.1 through T1.R1.5
"""

import os
import re
import time
from openOODA.qa.e2e.framework import TestContext, TestResult, oodac_check, oodac_build, POLYROOT


def test_t1_r1_1_sever_anchor_extra_names(double_run: bool = False) -> TestResult:
    """T1.R1.1: Verify single-file check does not crawl sibling anchor.oo."""
    ctx = TestContext("T1.R1.1", 1, "R1", "Sever anchor_extra_names crawling", double_run)
    try:
        # Create an anchor.oo with a deliberate syntax error
        ctx.write_file("sub/anchor.oo", "INVALID SYNTAX THAT CANNOT PARSE {};;;")
        # Create an isolated module that does NOT import anchor.oo
        sibling = ctx.write_file("sub/worker.oo", """// # Worker Module
// Logline: Independent module in directory.
// Setup: None.
// Beats: Return 42.

pub fn calc() -> Int {
    return 42;
}

pub fn main() -> Int {
    return calc();
}
""")
        rc, out, err = oodac_check(ctx, sibling)
        duration = (time.time() - ctx.start_time) * 1000

        if rc == 0 and "OK" in out:
            return TestResult(ctx.test_id, 1, "R1", ctx.name, "PASS", duration)
        else:
            return TestResult(
                ctx.test_id, 1, "R1", ctx.name, "FAIL", duration,
                error_msg="Single file check crawled sibling anchor.oo",
                diagnostic=f"rc={rc}\nout={out}\nerr={err}"
            )
    finally:
        ctx.cleanup()


def test_t1_r1_2_scope_prototype_arity(double_run: bool = False) -> TestResult:
    """T1.R1.2: Verify duplicate prototype with conflicting arities is rejected."""
    ctx = TestContext("T1.R1.2", 1, "R1", "Scope prototype arity checks", double_run)
    try:
        ctx.write_file("mod_a.oo", """// # Mod A
// Logline: Exports foo with 0 params.
// Setup: None.
// Beats: Return 10.
pub fn foo() -> Int { return 10; }
""")
        ctx.write_file("mod_b.oo", """// # Mod B
// Logline: Exports foo with 1 param.
// Setup: None.
// Beats: Return x.
pub fn foo(x: Int) -> Int { return x; }
""")
        main_oo = ctx.write_file("main.oo", """// # Main
// Logline: Imports both mod_a and mod_b.
// Setup: Conflicting arities.
// Beats: Fail closed.
import "./mod_a.oo";
import "./mod_b.oo";

pub fn main() -> Int {
    return foo();
}
""")
        out_bin = os.path.join(ctx.temp_dir, "main.bin")
        rc, out, err = oodac_build(ctx, main_oo, out_bin)
        duration = (time.time() - ctx.start_time) * 1000

        # Expected behavior: build MUST fail (rc != 0) due to conflicting arity prototypes
        if rc != 0 and not os.path.exists(out_bin):
            return TestResult(ctx.test_id, 1, "R1", ctx.name, "PASS", duration)
        else:
            return TestResult(
                ctx.test_id, 1, "R1", ctx.name, "FAIL", duration,
                error_msg="Duplicate prototype with conflicting arity was permitted (regression in check_dup_proto)",
                diagnostic=f"rc={rc}, out_bin exists={os.path.exists(out_bin)}\nout={out}\nerr={err}"
            )
    finally:
        ctx.cleanup()


def test_t1_r1_3_lexical_scope_scanning(double_run: bool = False) -> TestResult:
    """T1.R1.3: Verify lexical scope resolution and nested shadowing."""
    ctx = TestContext("T1.R1.3", 1, "R1", "Lexical scope scanning and shadowing", double_run)
    try:
        main_oo = ctx.write_file("scope_test.oo", """// # Scope Shadowing Test
// Logline: Multi-level block shadowing.
// Setup: None.
// Beats: Verify innermost binding resolution.

pub fn main() -> Int {
    let mut x: Int = 10;
    if x > 5 {
        let x: Int = 20;
        if x > 15 {
            let x: Int = 30;
            println("DEEP: " + x.to_string());
        }
        println("MID: " + x.to_string());
    }
    println("OUTER: " + x.to_string());
    return 0;
}
""")
        out_bin = os.path.join(ctx.temp_dir, "scope_test.bin")
        rc, out, err = oodac_build(ctx, main_oo, out_bin)
        duration = (time.time() - ctx.start_time) * 1000

        if rc != 0:
            return TestResult(
                ctx.test_id, 1, "R1", ctx.name, "FAIL", duration,
                error_msg="Failed to compile scoped program", diagnostic=err
            )

        rc_run, out_run, _ = ctx.run_cmd([out_bin])
        expected = "DEEP: 30\nMID: 20\nOUTER: 10\n"
        if rc_run == 0 and out_run == expected:
            return TestResult(ctx.test_id, 1, "R1", ctx.name, "PASS", duration)
        else:
            return TestResult(
                ctx.test_id, 1, "R1", ctx.name, "FAIL", duration,
                error_msg=f"Unexpected runtime output: {out_run!r} != {expected!r}"
            )
    finally:
        ctx.cleanup()


def test_t1_r1_4_decomposed_matchers(double_run: bool = False) -> TestResult:
    """T1.R1.4: Verify decomposed matcher functions in tc_names_known.oo satisfy <= 40 lines."""
    ctx = TestContext("T1.R1.4", 1, "R1", "Decomposed matchers in tc_names_known.oo", double_run)
    target = os.path.join(POLYROOT, "oodac/check/tc_names_known.oo")
    if not os.path.exists(target):
        return TestResult(ctx.test_id, 1, "R1", ctx.name, "FAIL", 0, error_msg=f"Missing {target}")

    with open(target, "r", encoding="utf-8") as f:
        lines = f.readlines()

    fn_re = re.compile(r"^[ \t]*(?:pub[ \t]+)?fn[ \t]+([A-Za-z0-9_]+)")
    fn_starts = [(i, m.group(1)) for i, l in enumerate(lines) if (m := fn_re.match(l))]

    violations = []
    for s_idx, name in fn_starts:
        depth = 0
        begun = False
        e_idx = len(lines) - 1
        for i in range(s_idx, len(lines)):
            for ch in lines[i]:
                if ch == "{":
                    depth += 1
                    begun = True
                elif ch == "}":
                    depth -= 1
            if begun and depth <= 0:
                e_idx = i
                break
        fn_len = e_idx - s_idx + 1
        if fn_len > 40:
            violations.append(f"{name} ({fn_len} lines)")

    duration = (time.time() - ctx.start_time) * 1000
    if not violations:
        return TestResult(ctx.test_id, 1, "R1", ctx.name, "PASS", duration)
    else:
        return TestResult(
            ctx.test_id, 1, "R1", ctx.name, "FAIL", duration,
            error_msg=f"Functions exceeding 40 lines in tc_names_known.oo: {', '.join(violations)}"
        )


def test_t1_r1_5_compiler_happy_path(double_run: bool = False) -> TestResult:
    """T1.R1.5: Verify multi-function program with structs and methods builds and runs."""
    ctx = TestContext("T1.R1.5", 1, "R1", "Compiler multi-function happy path build", double_run)
    try:
        src = ctx.write_file("calc.oo", """// # Calculator Program
// Logline: Evaluates structured arithmetic operations.
// Setup: Custom Point struct and helper functions.
// Beats: Compute manhattan distance and print OK.

type Point = struct {
    x: Int,
    y: Int
};

fn manhattan(p1: Point, p2: Point) -> Int {
    let mut dx: Int = p2.x - p1.x;
    if dx < 0 { dx = 0 - dx; }
    let mut dy: Int = p2.y - p1.y;
    if dy < 0 { dy = 0 - dy; }
    return dx + dy;
}

pub fn main() -> Int {
    let p1: Point = Point { x: 3, y: 7 };
    let p2: Point = Point { x: 9, y: 15 };
    let d: Int = manhattan(p1, p2);
    println("DIST: " + d.to_string());
    return 0;
}
""")
        out_bin = os.path.join(ctx.temp_dir, "calc.bin")
        rc, out, err = oodac_build(ctx, src, out_bin)
        duration = (time.time() - ctx.start_time) * 1000

        if rc != 0:
            return TestResult(ctx.test_id, 1, "R1", ctx.name, "FAIL", duration, error_msg="Build failed", diagnostic=err)

        rc_run, out_run, _ = ctx.run_cmd([out_bin])
        if rc_run == 0 and out_run == "DIST: 14\n":
            return TestResult(ctx.test_id, 1, "R1", ctx.name, "PASS", duration)
        else:
            return TestResult(
                ctx.test_id, 1, "R1", ctx.name, "FAIL", duration,
                error_msg=f"Unexpected output: rc={rc_run}, out={out_run!r}"
            )
    finally:
        ctx.cleanup()
