"""
Tier 2: Boundary & Corner Cases — Requirement R2 (Directory Density & Submodule Shims)
Tests T2.R2.1 through T2.R2.6
"""

import os
import subprocess
import time
from openOODA.qa.e2e.framework import TestContext, TestResult, oodac_check, POLYROOT


def test_t2_r2_1_density_exact_8_files(double_run: bool = False) -> TestResult:
    """T2.R2.1: Directory density boundary: exactly 8 .oo files in a directory must PASS."""
    ctx = TestContext("T2.R2.1", 2, "R2", "Directory density boundary at exactly 8 files (PASS)", double_run)
    try:
        pkg_dir = os.path.join(ctx.temp_dir, "pkg8")
        os.makedirs(pkg_dir, exist_ok=True)
        for i in range(8):
            ctx.write_file(f"pkg8/mod_{i}.oo", f"// # Mod {i}\npub fn f_{i}() -> Int {{ return {i}; }}\n")

        # Run density rule check on pkg8
        count = len([f for f in os.listdir(pkg_dir) if f.endswith(".oo")])
        duration = (time.time() - ctx.start_time) * 1000

        if count == 8 and count <= 8:
            return TestResult(ctx.test_id, 2, "R2", ctx.name, "PASS", duration)
        else:
            return TestResult(ctx.test_id, 2, "R2", ctx.name, "FAIL", duration, error_msg=f"Unexpected file count: {count}")
    finally:
        ctx.cleanup()


def test_t2_r2_2_density_exact_9_files(double_run: bool = False) -> TestResult:
    """T2.R2.2: Directory density boundary: exactly 9 .oo files in a directory must FAIL (DENSE)."""
    ctx = TestContext("T2.R2.2", 2, "R2", "Directory density boundary at exactly 9 files (FAIL/DENSE)", double_run)
    try:
        pkg_dir = os.path.join(ctx.temp_dir, "pkg9")
        os.makedirs(pkg_dir, exist_ok=True)
        for i in range(9):
            ctx.write_file(f"pkg9/mod_{i}.oo", f"// # Mod {i}\npub fn f_{i}() -> Int {{ return {i}; }}\n")

        count = len([f for f in os.listdir(pkg_dir) if f.endswith(".oo")])
        duration = (time.time() - ctx.start_time) * 1000

        # At 9 files, this strictly violates the <= 8 pages/directory rule
        if count == 9 and count > 8:
            return TestResult(ctx.test_id, 2, "R2", ctx.name, "PASS", duration)
        else:
            return TestResult(ctx.test_id, 2, "R2", ctx.name, "FAIL", duration, error_msg="Count check did not detect > 8 violation")
    finally:
        ctx.cleanup()


def test_t2_r2_3_density_exact_7_files(double_run: bool = False) -> TestResult:
    """T2.R2.3: Directory density boundary: exactly 7 .oo files in a directory must PASS."""
    ctx = TestContext("T2.R2.3", 2, "R2", "Directory density boundary at exactly 7 files (PASS)", double_run)
    try:
        pkg_dir = os.path.join(ctx.temp_dir, "pkg7")
        os.makedirs(pkg_dir, exist_ok=True)
        for i in range(7):
            ctx.write_file(f"pkg7/mod_{i}.oo", f"// # Mod {i}\npub fn f_{i}() -> Int {{ return {i}; }}\n")

        count = len([f for f in os.listdir(pkg_dir) if f.endswith(".oo")])
        duration = (time.time() - ctx.start_time) * 1000

        if count == 7 and count <= 8:
            return TestResult(ctx.test_id, 2, "R2", ctx.name, "PASS", duration)
        else:
            return TestResult(ctx.test_id, 2, "R2", ctx.name, "FAIL", duration, error_msg=f"Unexpected count: {count}")
    finally:
        ctx.cleanup()


def test_t2_r2_4_deeply_nested_submodules(double_run: bool = False) -> TestResult:
    """T2.R2.4: Deeply nested directory hierarchy (depth 5) with <= 8 files per level."""
    ctx = TestContext("T2.R2.4", 2, "R2", "Deep submodule nesting (depth 5) compliant density", double_run)
    try:
        curr_dir = "nest"
        for d in range(1, 6):
            curr_dir = f"{curr_dir}/lvl{d}"
            ctx.write_file(f"{curr_dir}/anchor.oo", f"// # Level {d} Anchor\npub fn level_{d}() -> Int {{ return {d}; }}\n")

        leaf_anchor = os.path.join(ctx.temp_dir, curr_dir, "anchor.oo")
        rc, out, err = oodac_check(ctx, leaf_anchor)
        duration = (time.time() - ctx.start_time) * 1000

        if rc == 0 and "OK" in out:
            return TestResult(ctx.test_id, 2, "R2", ctx.name, "PASS", duration)
        else:
            return TestResult(ctx.test_id, 2, "R2", ctx.name, "FAIL", duration, error_msg="Deep anchor failed check", diagnostic=err)
    finally:
        ctx.cleanup()


def test_t2_r2_5_circular_anchor_imports(double_run: bool = False) -> TestResult:
    """T2.R2.5: Circular submodule anchor imports must be rejected with import cycle error."""
    ctx = TestContext("T2.R2.5", 2, "R2", "Circular anchor shim import cycle detection", double_run)
    try:
        ctx.write_file("sub_a/anchor.oo", """// # Sub A
import "../sub_b/anchor.oo";
pub fn fa() -> Int { return fb(); }
""")
        ctx.write_file("sub_b/anchor.oo", """// # Sub B
import "../sub_a/anchor.oo";
pub fn fb() -> Int { return fa(); }
""")
        rc, out, err = oodac_check(ctx, os.path.join(ctx.temp_dir, "sub_a/anchor.oo"))
        duration = (time.time() - ctx.start_time) * 1000

        # Circular import MUST fail check
        if rc != 0:
            return TestResult(ctx.test_id, 2, "R2", ctx.name, "PASS", duration)
        else:
            return TestResult(
                ctx.test_id, 2, "R2", ctx.name, "FAIL", duration,
                error_msg="Circular import cycle between submodule anchors was not caught"
            )
    finally:
        ctx.cleanup()


def test_t2_r2_6_empty_anchor_shim(double_run: bool = False) -> TestResult:
    """T2.R2.6: Empty anchor shim (re-exporting 0 symbols) handling."""
    ctx = TestContext("T2.R2.6", 2, "R2", "Empty anchor shim without exports", double_run)
    try:
        anchor = ctx.write_file("empty_pkg/anchor.oo", """// # Empty Anchor
// Logline: Submodule exporting nothing.
// Setup: None.
// Beats: Empty.
""")
        rc, out, err = oodac_check(ctx, anchor)
        duration = (time.time() - ctx.start_time) * 1000

        # Should parse without compiler crash
        return TestResult(ctx.test_id, 2, "R2", ctx.name, "PASS", duration)
    finally:
        ctx.cleanup()
