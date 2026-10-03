"""
Tier 1: Feature Coverage — Requirement R2 (Directory Density & Anchor Sanitization)
Tests T1.R2.1 through T1.R2.5
"""

import os
import re
import time
from openOODA.qa.e2e.framework import TestContext, TestResult, oodac_check, POLYROOT


def test_t1_r2_1_mesh_anchor_purged(double_run: bool = False) -> TestResult:
    """T1.R2.1: Verify std/net/mesh/anchor.oo does not import purged open_* test fixtures."""
    ctx = TestContext("T1.R2.1", 1, "R2", "Sanitize std/net/mesh/anchor.oo test fixtures", double_run)
    target = os.path.join(POLYROOT, "std/net/mesh/anchor.oo")
    if not os.path.exists(target):
        return TestResult(ctx.test_id, 1, "R2", ctx.name, "FAIL", 0, error_msg=f"Missing {target}")

    with open(target, "r", encoding="utf-8") as f:
        content = f.read()

    # Search for active import statements targeting open_* fixtures
    imports = re.findall(r'^[ \t]*import[ \t]+"open_[^"]+\.oo"', content, re.MULTILINE)
    duration = (time.time() - ctx.start_time) * 1000

    if not imports:
        return TestResult(ctx.test_id, 1, "R2", ctx.name, "PASS", duration)
    else:
        return TestResult(
            ctx.test_id, 1, "R2", ctx.name, "FAIL", duration,
            error_msg=f"Found {len(imports)} unpurged open_* imports in std/net/mesh/anchor.oo: {imports[:3]}"
        )


def test_t1_r2_2_mega_directory_fixture_separation(double_run: bool = False) -> TestResult:
    """T1.R2.2: Verify test fixtures are separated from production packages (e.g., enclave and silicon)."""
    ctx = TestContext("T1.R2.2", 1, "R2", "Mega-directory test fixture isolation", double_run)
    enclave_dir = os.path.join(POLYROOT, "std/sec/enclave")
    silicon_dir = os.path.join(POLYROOT, "std/hw/silicon")

    enclave_fixtures = [
        f for f in (os.listdir(enclave_dir) if os.path.exists(enclave_dir) else [])
        if f.startswith("secret_") and f.endswith("_fail.oo")
    ]
    silicon_fixtures = [
        f for f in (os.listdir(silicon_dir) if os.path.exists(silicon_dir) else [])
        if (f.startswith("x86_") or f.startswith("aarch64_")) and f.endswith(".oo") and not f.endswith("_asm.oo")
    ]

    duration = (time.time() - ctx.start_time) * 1000
    total_unrelocated = len(enclave_fixtures) + len(silicon_fixtures)
    if total_unrelocated == 0:
        return TestResult(ctx.test_id, 1, "R2", ctx.name, "PASS", duration)
    else:
        return TestResult(
            ctx.test_id, 1, "R2", ctx.name, "FAIL", duration,
            error_msg=f"Found {len(enclave_fixtures)} enclave fixtures and {len(silicon_fixtures)} silicon fixtures in production dirs",
            diagnostic=f"Enclave sample: {enclave_fixtures[:3]}, Silicon sample: {silicon_fixtures[:3]}"
        )


def test_t1_r2_3_directory_density_rule(double_run: bool = False) -> TestResult:
    """T1.R2.3: Verify <= 8 pages/directory density across named mega-directories in std."""
    ctx = TestContext("T1.R2.3", 1, "R2", "Directory density <= 8 pages in std mega-dirs", double_run)
    named_dirs = [
        os.path.join(POLYROOT, "std/science/phys/quantum"),
        os.path.join(POLYROOT, "std/hw/silicon"),
        os.path.join(POLYROOT, "std/science/phys/classical"),
        os.path.join(POLYROOT, "std/sec/asymmetric"),
        os.path.join(POLYROOT, "std/sec/enclave"),
        os.path.join(POLYROOT, "std/net/mesh"),
    ]

    dense_violations = {}
    for d in named_dirs:
        if os.path.exists(d):
            oo_files = [f for f in os.listdir(d) if f.endswith(".oo")]
            if len(oo_files) > 8:
                dense_violations[os.path.relpath(d, POLYROOT)] = len(oo_files)

    duration = (time.time() - ctx.start_time) * 1000
    if not dense_violations:
        return TestResult(ctx.test_id, 1, "R2", ctx.name, "PASS", duration)
    else:
        return TestResult(
            ctx.test_id, 1, "R2", ctx.name, "FAIL", duration,
            error_msg=f"{len(dense_violations)} directories violate <= 8 pages rule",
            diagnostic=f"Violations: {dense_violations}"
        )


def test_t1_r2_4_submodule_anchor_reexport(double_run: bool = False) -> TestResult:
    """T1.R2.4: Verify submodule anchor re-export pattern satisfies typechecking."""
    ctx = TestContext("T1.R2.4", 1, "R2", "Submodule anchor re-export pattern", double_run)
    try:
        # Create submodule sub1 (<= 8 files)
        ctx.write_file("pkg/sub1/worker1.oo", """// # Sub Worker
// Logline: Worker function.
// Setup: None.
// Beats: Return 100.
pub fn sub_calc() -> Int { return 100; }
""")
        ctx.write_file("pkg/sub1/anchor.oo", """// # Sub Anchor
// Logline: Submodule re-export.
// Setup: None.
// Beats: Re-export sub_calc.
import "./worker1.oo";
pub fn sub_calc_shim() -> Int { return sub_calc(); }
""")
        # Create root anchor.oo
        root_anchor = ctx.write_file("pkg/anchor.oo", """// # Root Anchor
// Logline: Main package entrypoint.
// Setup: None.
// Beats: Re-export sub1.
import "./sub1/anchor.oo";
pub fn pkg_main() -> Int { return sub_calc_shim(); }
""")
        rc, out, err = oodac_check(ctx, root_anchor)
        duration = (time.time() - ctx.start_time) * 1000

        if rc == 0 and "OK" in out:
            return TestResult(ctx.test_id, 1, "R2", ctx.name, "PASS", duration)
        else:
            return TestResult(
                ctx.test_id, 1, "R2", ctx.name, "FAIL", duration,
                error_msg="Submodule anchor re-export failed check", diagnostic=err
            )
    finally:
        ctx.cleanup()


def test_t1_r2_5_academy_headers(double_run: bool = False) -> TestResult:
    """T1.R2.5: Verify Academy 4-element docstrings exist in standard library anchors."""
    ctx = TestContext("T1.R2.5", 1, "R2", "Academy 4-element headers in std anchors", double_run)
    anchors = [
        "std/anchor.oo",
        "std/core/anchor.oo",
        "std/fs/anchor.oo",
        "std/net/anchor.oo",
        "std/sec/anchor.oo",
    ]

    missing = []
    required_tags = ["// #", "// Logline:", "// Setup:", "// Beats:"]
    for rel in anchors:
        p = os.path.join(POLYROOT, rel)
        if not os.path.exists(p):
            missing.append(f"{rel} (missing file)")
            continue
        with open(p, "r", encoding="utf-8") as f:
            header = "".join(f.readlines()[:20])
        for tag in required_tags:
            if tag not in header:
                missing.append(f"{rel} (missing '{tag}')")

    duration = (time.time() - ctx.start_time) * 1000
    if not missing:
        return TestResult(ctx.test_id, 1, "R2", ctx.name, "PASS", duration)
    else:
        return TestResult(
            ctx.test_id, 1, "R2", ctx.name, "FAIL", duration,
            error_msg=f"Academy docstring violations in std anchors: {missing}"
        )
