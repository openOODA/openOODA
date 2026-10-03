"""
Tier 1: Feature Coverage — Requirement R4 (Standard Library Tree-Rot & WUI/MCP)
Tests T1.R4.1 through T1.R4.6
"""

import os
import re
import time
from openOODA.qa.e2e.framework import TestContext, TestResult, oodac_check, POLYROOT


def test_t1_r4_1_struct_mutability_rule(double_run: bool = False) -> TestResult:
    """T1.R4.1: Verify let vs let mut struct field mutation enforcement."""
    ctx = TestContext("T1.R4.1", 1, "R4", "Struct field mutation let vs let mut enforcement", double_run)
    try:
        # 1. Immutable binding assignment MUST fail
        immut_src = ctx.write_file("immut.oo", """// # Immut Test
type Data = struct { val: Int };
pub fn main() -> Int {
    let d: Data = Data { val: 1 };
    d.val = 2;
    return 0;
}
""")
        rc_immut, out_immut, err_immut = oodac_check(ctx, immut_src)
        combined_immut = out_immut + err_immut
        if rc_immut == 0 or "cannot assign to field of immutable binding" not in combined_immut:
            duration = (time.time() - ctx.start_time) * 1000
            return TestResult(
                ctx.test_id, 1, "R4", ctx.name, "FAIL", duration,
                error_msg="Immutable binding assignment did not fail with expected type error",
                diagnostic=f"rc={rc_immut}, out={combined_immut}"
            )

        # 2. Mutable binding assignment MUST pass
        mut_src = ctx.write_file("mut.oo", """// # Mut Test
type Data = struct { val: Int };
pub fn main() -> Int {
    let mut d: Data = Data { val: 1 };
    d.val = 2;
    return 0;
}
""")
        rc_mut, out_mut, err_mut = oodac_check(ctx, mut_src)
        duration = (time.time() - ctx.start_time) * 1000
        if rc_mut == 0 and "OK" in out_mut:
            return TestResult(ctx.test_id, 1, "R4", ctx.name, "PASS", duration)
        else:
            return TestResult(
                ctx.test_id, 1, "R4", ctx.name, "FAIL", duration,
                error_msg="Mutable binding assignment failed check unexpectedly",
                diagnostic=err_mut
            )
    finally:
        ctx.cleanup()


def test_t1_r4_2_redundant_builtin_imports(double_run: bool = False) -> TestResult:
    """T1.R4.2: Verify importing built-in primitives is rejected as unused import."""
    ctx = TestContext("T1.R4.2", 1, "R4", "Rejection of redundant built-in primitive imports", double_run)
    try:
        src = ctx.write_file("redundant.oo", """// # Redundant Import Test
import "std/core/primitives/result.oo";
pub fn main() -> Int {
    return 0;
}
""")
        rc, out, err = oodac_check(ctx, src)
        combined = out + err
        duration = (time.time() - ctx.start_time) * 1000

        if rc != 0 and "unused import 'std/core/primitives/result.oo'" in combined:
            return TestResult(ctx.test_id, 1, "R4", ctx.name, "PASS", duration)
        else:
            return TestResult(
                ctx.test_id, 1, "R4", ctx.name, "FAIL", duration,
                error_msg="Redundant primitive import was not rejected", diagnostic=combined
            )
    finally:
        ctx.cleanup()


def test_t1_r4_3_disambiguated_markers(double_run: bool = False) -> TestResult:
    """T1.R4.3: Verify zero duplicate shim_marker_engine_init functions in std."""
    ctx = TestContext("T1.R4.3", 1, "R4", "Disambiguation of global marker functions in std", double_run)
    std_dir = os.path.join(POLYROOT, "std")
    matches = []

    for root, _, files in os.walk(std_dir):
        for f in files:
            if f.endswith(".oo"):
                p = os.path.join(root, f)
                with open(p, "r", encoding="utf-8", errors="replace") as fh:
                    for idx, line in enumerate(fh, 1):
                        if "pub fn shim_marker_engine_init" in line:
                            matches.append(f"{os.path.relpath(p, POLYROOT)}:{idx}")

    duration = (time.time() - ctx.start_time) * 1000
    if not matches:
        return TestResult(ctx.test_id, 1, "R4", ctx.name, "PASS", duration)
    else:
        return TestResult(
            ctx.test_id, 1, "R4", ctx.name, "FAIL", duration,
            error_msg=f"Found duplicate shim_marker_engine_init in: {matches}"
        )


def test_t1_r4_4_wui_vnode_flat_arena(double_run: bool = False) -> TestResult:
    """T1.R4.4: Verify complete elimination of .children in favor of child_ids flat arena in WUI."""
    ctx = TestContext("T1.R4.4", 1, "R4", "WUI VNode flat arena refactoring across companion files", double_run)
    wui_dir = os.path.join(POLYROOT, "std/app/ui/wui")
    companion_files = [
        "wui_diff.oo",
        "wui_canvas_renderer.oo",
        "wui_vdom_builder.oo",
        "wui_components.oo",
        "wui_app.oo",
    ]

    children_references = []
    for rel in companion_files:
        p = os.path.join(wui_dir, rel)
        if not os.path.exists(p):
            continue
        with open(p, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f, 1):
                # Look for .children access on VNode or children: List[VNode] parameter declarations
                if ".children" in line or "children: List[VNode]" in line:
                    children_references.append(f"{rel}:{idx}: {line.strip()}")

    duration = (time.time() - ctx.start_time) * 1000
    if not children_references:
        return TestResult(ctx.test_id, 1, "R4", ctx.name, "PASS", duration)
    else:
        return TestResult(
            ctx.test_id, 1, "R4", ctx.name, "FAIL", duration,
            error_msg=f"Found {len(children_references)} legacy .children references in WUI companion files",
            diagnostic="\n".join(children_references[:5])
        )


def test_t1_r4_5_genomics_float_annotations(double_run: bool = False) -> TestResult:
    """T1.R4.5: Verify genomics files use Float for state.raw_metric."""
    ctx = TestContext("T1.R4.5", 1, "R4", "Genomics Float type annotations for raw_metric", double_run)
    genomics_dir = os.path.join(POLYROOT, "std/science/bio/genomics")
    int_metric_violations = []

    if os.path.exists(genomics_dir):
        for f in os.listdir(genomics_dir):
            if f.endswith(".oo"):
                p = os.path.join(genomics_dir, f)
                with open(p, "r", encoding="utf-8") as fh:
                    for idx, line in enumerate(fh, 1):
                        if "let raw: Int = state.raw_metric" in line:
                            int_metric_violations.append(f"{f}:{idx}")

    duration = (time.time() - ctx.start_time) * 1000
    if not int_metric_violations:
        return TestResult(ctx.test_id, 1, "R4", ctx.name, "PASS", duration)
    else:
        return TestResult(
            ctx.test_id, 1, "R4", ctx.name, "FAIL", duration,
            error_msg=f"Found {len(int_metric_violations)} genomics files with Int instead of Float for raw_metric",
            diagnostic=f"Violations: {int_metric_violations[:5]}"
        )


def test_t1_r4_6_mcp_fail_closed_negative_control(double_run: bool = False) -> TestResult:
    """T1.R4.6: Verify MCP probe_attenuation fails closed without secret and has no hardcoded fallback."""
    ctx = TestContext("T1.R4.6", 1, "R4", "MCP attenuation fail-closed negative control", double_run)
    probe_path = os.path.join(POLYROOT, "mcp/qa/sec/probe_attenuation.oo")
    if not os.path.exists(probe_path):
        return TestResult(ctx.test_id, 1, "R4", ctx.name, "FAIL", 0, error_msg=f"Missing {probe_path}")

    with open(probe_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for presence of fallback secret bypass added in commit e1e3073
    has_fallback = 's.attenuation_secret = "probe-attenuation-secret-32bytes!"' in content
    duration = (time.time() - ctx.start_time) * 1000

    if not has_fallback:
        return TestResult(ctx.test_id, 1, "R4", ctx.name, "PASS", duration)
    else:
        return TestResult(
            ctx.test_id, 1, "R4", ctx.name, "FAIL", duration,
            error_msg="MCP probe_attenuation.oo has hardcoded fallback secret neutralizing negative control in CI"
        )
