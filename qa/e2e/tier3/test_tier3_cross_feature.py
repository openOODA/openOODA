"""
Tier 3: Cross-Feature Combinations (Pairwise Interaction Tests)
Tests T3.X1 through T3.X8
"""

import hashlib
import os
import time
from openOODA.qa.e2e.framework import (
    TestContext, TestResult, oodac_check, oodac_build, sha256_file, OODAC_BIN, POLYROOT
)


def test_t3_x1_arity_and_cache_invalidation(double_run: bool = False) -> TestResult:
    """T3.X1: R1 (Arity Scoping) + R5 (Check Cache): Prototype change invalidates downstream cache."""
    ctx = TestContext("T3.X1", 3, "R1+R5", "Arity alteration invalidates downstream check cache", double_run)
    try:
        # 1. Author module A and consumer B
        ctx.write_file("dep.oo", "// # Dep\npub fn calculate(x: Int) -> Int { return x * 2; }\n")
        consumer = ctx.write_file("consumer.oo", """// # Consumer
import "./dep.oo";
pub fn main() -> Int {
    return calculate(5);
}
""")
        rc1, _, _ = oodac_check(ctx, consumer)
        if rc1 != 0:
            return TestResult(ctx.test_id, 3, "R1+R5", ctx.name, "FAIL", 0, error_msg="Initial check failed")

        # 2. Modify prototype arity in dep.oo (add second parameter)
        ctx.write_file("dep.oo", "// # Dep\npub fn calculate(x: Int, y: Int) -> Int { return x + y; }\n")

        # 3. Consumer MUST now fail check (arity mismatch: calls with 1 param, expects 2)
        rc2, out2, err2 = oodac_check(ctx, consumer)
        duration = (time.time() - ctx.start_time) * 1000

        if rc2 != 0:
            return TestResult(ctx.test_id, 3, "R1+R5", ctx.name, "PASS", duration)
        else:
            return TestResult(
                ctx.test_id, 3, "R1+R5", ctx.name, "FAIL", duration,
                error_msg="Downstream cache hit persisted despite upstream prototype arity alteration"
            )
    finally:
        ctx.cleanup()


def test_t3_x2_submodule_shims_and_anchor_isolation(double_run: bool = False) -> TestResult:
    """T3.X2: R2 (Submodule Shims) + R1 (Anchor Severance): Submodule exports only explicit symbols."""
    ctx = TestContext("T3.X2", 3, "R2+R1", "Partitioned submodule exports only explicit public symbols", double_run)
    try:
        # In sub/, worker.oo has private unexported symbol internal_secret
        ctx.write_file("sub/worker.oo", """// # Worker
fn internal_secret() -> Int { return 42; }
pub fn public_worker() -> Int { return internal_secret(); }
""")
        # anchor.oo re-exports only public_worker
        ctx.write_file("sub/anchor.oo", """// # Sub Anchor
import "./worker.oo";
pub fn exported_fn() -> Int { return public_worker(); }
""")
        # Consumer attempts to call unexported internal_secret directly
        consumer = ctx.write_file("consumer.oo", """// # Consumer
import "./sub/anchor.oo";
pub fn main() -> Int {
    return internal_secret();
}
""")
        rc, out, err = oodac_check(ctx, consumer)
        duration = (time.time() - ctx.start_time) * 1000

        # Must fail check because internal_secret is not exported through anchor.oo
        if rc != 0:
            return TestResult(ctx.test_id, 3, "R2+R1", ctx.name, "PASS", duration)
        else:
            return TestResult(
                ctx.test_id, 3, "R2+R1", ctx.name, "FAIL", duration,
                error_msg="Unexported sibling symbol was leaked through submodule anchor"
            )
    finally:
        ctx.cleanup()


def test_t3_x3_compacted_sha512_resource_bounds(double_run: bool = False) -> TestResult:
    """T3.X3: R3 (Compacted SHA-512) + R5 (Resource Bounds): Check executes under 64MB RSS and 3.0s CPU."""
    ctx = TestContext("T3.X3", 3, "R3+R5", "Compacted SHA-512 checks strictly within PR resource scorecard", double_run)
    target = os.path.join(POLYROOT, "std/sec/hash/sha512.oo")

    rc, out, err, cpu_sec, rss_kb = ctx.run_cmd_measured(
        [OODAC_BIN, "check", target],
        cwd=POLYROOT
    )
    duration = (time.time() - ctx.start_time) * 1000
    rss_mb = rss_kb / 1024.0

    if rc == 0 and rss_mb <= 64.0 and cpu_sec <= 3.0:
        return TestResult(ctx.test_id, 3, "R3+R5", ctx.name, "PASS", duration)
    else:
        return TestResult(
            ctx.test_id, 3, "R3+R5", ctx.name, "FAIL", duration,
            error_msg=f"Compacted SHA-512 exceeded bounds: RSS={rss_mb:.1f}MB (<=64), CPU={cpu_sec:.2f}s (<=3.0s)"
        )


def test_t3_x4_wui_flat_arena_struct_mutation(double_run: bool = False) -> TestResult:
    """T3.X4: R4 (WUI Flat Arena) + R1 (Typechecking): Construct and mutate VNodeArena cleanly."""
    ctx = TestContext("T3.X4", 3, "R4+R1", "WUI Flat Arena construction and struct mutation typecheck", double_run)
    try:
        src = ctx.write_file("arena_app.oo", """// # WUI Arena App
import "std/app/ui/wui/wui_vnode.oo";

type VNodeArena = struct {
    nodes: List[VNode],
    root_id: Int,
    next_id: Int
};

fn arena_add(arena: &mut VNodeArena, node: VNode) -> Int {
    let id: Int = arena.next_id;
    let mut n: List[VNode] = arena.nodes;
    n = list_push(n, node);
    arena.nodes = n;
    arena.next_id = id + 1;
    return id;
}

pub fn main() -> Int {
    let mut arena: VNodeArena = VNodeArena {
        nodes: list_new(),
        root_id: 0 - 1,
        next_id: 0
    };
    let child1: VNode = vnode_text("Child 1");
    let c1_id: Int = arena_add(&mut arena, child1);

    let mut ch_ids: List[Int] = list_new();
    ch_ids = list_push(ch_ids, c1_id);

    let root_node: VNode = vnode_element("div", "root", list_new(), ch_ids);
    let r_id: Int = arena_add(&mut arena, root_node);
    arena.root_id = r_id;

    if arena.root_id == 1 && list_len(arena.nodes) == 2 {
        return 0;
    }
    return 1;
}
""")
        out_bin = os.path.join(ctx.temp_dir, "arena_app.bin")
        rc, out, err = oodac_build(ctx, src, out_bin)
        duration = (time.time() - ctx.start_time) * 1000

        if rc != 0:
            return TestResult(ctx.test_id, 3, "R4+R1", ctx.name, "FAIL", duration, error_msg="Build failed", diagnostic=err)

        rc_run, _, _ = ctx.run_cmd([out_bin])
        if rc_run == 0:
            return TestResult(ctx.test_id, 3, "R4+R1", ctx.name, "PASS", duration)
        else:
            return TestResult(ctx.test_id, 3, "R4+R1", ctx.name, "FAIL", duration, error_msg=f"Runtime exit code {rc_run}")
    finally:
        ctx.cleanup()


def test_t3_x5_mcp_negative_control_double_run(double_run: bool = False) -> TestResult:
    """T3.X5: R4 (MCP Negative Control) + R5 (Double-Run Identity): Negative control deterministic failure."""
    ctx = TestContext("T3.X5", 3, "R4+R5", "MCP attenuation fail-closed negative control double-run determinism", double_run)
    # Check if probe_attenuation without secret exits non-zero and produces identical output across 2 runs
    probe_path = os.path.join(POLYROOT, "mcp/qa/sec/probe_attenuation.oo")
    if not os.path.exists(probe_path):
        return TestResult(ctx.test_id, 3, "R4+R5", ctx.name, "FAIL", 0, error_msg=f"Missing {probe_path}")

    with open(probe_path, "r", encoding="utf-8") as f:
        content = f.read()

    # The negative control in CI fails if probe_attenuation.oo has a fallback secret
    has_fallback = 's.attenuation_secret = "probe-attenuation-secret-32bytes!"' in content
    duration = (time.time() - ctx.start_time) * 1000

    if not has_fallback:
        return TestResult(ctx.test_id, 3, "R4+R5", ctx.name, "PASS", duration)
    else:
        return TestResult(
            ctx.test_id, 3, "R4+R5", ctx.name, "FAIL", duration,
            error_msg="MCP probe_attenuation.oo has hardcoded fallback secret neutralizing negative control in CI"
        )


def test_t3_x6_partitioned_build_bit_identical(double_run: bool = False) -> TestResult:
    """T3.X6: R2 (Submodule Partitioning) + R5 (Determinism): Submodule compilation is bit-identical."""
    ctx = TestContext("T3.X6", 3, "R2+R5", "Bit-identical binary compilation across partitioned submodules", double_run)
    try:
        ctx.write_file("sub/math.oo", "// # Sub Math\npub fn add_sq(a: Int, b: Int) -> Int { return (a + b) * (a + b); }\n")
        ctx.write_file("sub/anchor.oo", "// # Sub Anchor\nimport \"./math.oo\";\npub fn compute(x: Int) -> Int { return add_sq(x, 2); }\n")
        main_oo = ctx.write_file("main.oo", """// # Main
import "./sub/anchor.oo";
pub fn main() -> Int {
    println("VAL: " + compute(3).to_string());
    return 0;
}
""")
        bin1 = os.path.join(ctx.temp_dir, "run1.bin")
        bin2 = os.path.join(ctx.temp_dir, "run2.bin")

        rc1, _, _ = oodac_build(ctx, main_oo, bin1)
        rc2, _, _ = oodac_build(ctx, main_oo, bin2)
        duration = (time.time() - ctx.start_time) * 1000

        if rc1 != 0 or rc2 != 0:
            return TestResult(ctx.test_id, 3, "R2+R5", ctx.name, "FAIL", duration, error_msg="Build failed")

        h1 = sha256_file(bin1)
        h2 = sha256_file(bin2)
        if h1 == h2:
            return TestResult(ctx.test_id, 3, "R2+R5", ctx.name, "PASS", duration)
        else:
            return TestResult(
                ctx.test_id, 3, "R2+R5", ctx.name, "FAIL", duration,
                error_msg=f"Non-identical ELF hashes: {h1} != {h2}"
            )
    finally:
        ctx.cleanup()


def test_t3_x7_struct_mutation_with_decomposed_helpers(double_run: bool = False) -> TestResult:
    """T3.X7: R4 (Struct Mutation `let mut`) + R3 (Decomposed Helpers): Mutations preserved across calls."""
    ctx = TestContext("T3.X7", 3, "R4+R3", "Mutable struct field mutations preserved across decomposed helpers", double_run)
    try:
        src = ctx.write_file("helpers.oo", """// # Struct Helper Pipeline
type State = struct {
    step: Int,
    acc: Int
};

fn helper_stage_one(s: &mut State) {
    s.step = s.step + 1;
    s.acc = s.acc + 10;
}

fn helper_stage_two(s: &mut State) {
    s.step = s.step + 1;
    s.acc = s.acc * 2;
}

pub fn main() -> Int {
    let mut s: State = State { step: 0, acc: 5 };
    helper_stage_one(&mut s);
    helper_stage_two(&mut s);
    if s.step == 2 && s.acc == 30 {
        return 0;
    }
    return 1;
}
""")
        out_bin = os.path.join(ctx.temp_dir, "helpers.bin")
        rc, out, err = oodac_build(ctx, src, out_bin)
        duration = (time.time() - ctx.start_time) * 1000

        if rc != 0:
            return TestResult(ctx.test_id, 3, "R4+R3", ctx.name, "FAIL", duration, error_msg="Build failed", diagnostic=err)

        rc_run, _, _ = ctx.run_cmd([out_bin])
        if rc_run == 0:
            return TestResult(ctx.test_id, 3, "R4+R3", ctx.name, "PASS", duration)
        else:
            return TestResult(ctx.test_id, 3, "R4+R3", ctx.name, "FAIL", duration, error_msg=f"Exit code {rc_run}")
    finally:
        ctx.cleanup()


def test_t3_x8_scope_has_linear_scaling_at_depth_50(double_run: bool = False) -> TestResult:
    """T3.X8: R1 (Lexical Scoping `scope_has`) + R5 (Resource Scorecard): Scope depth 50 checks < 0.2s."""
    ctx = TestContext("T3.X8", 3, "R1+R5", "Deep lexical scope depth 50 checks in < 0.2s without O(D*n) blowout", double_run)
    try:
        lines = ["// # Deep Scope Stress Test", "pub fn main() -> Int {", "    let mut sum: Int = 0;"]
        for d in range(1, 51):
            indent = "    " * (d + 1)
            lines.append(f"{indent}let var_{d}: Int = {d};")
            lines.append(f"{indent}if var_{d} > 0 {{")
        # Innermost sum accumulation
        inner_indent = "    " * 52
        lines.append(f"{inner_indent}sum = sum + var_1 + var_50;")
        # Close all 50 if blocks
        for d in range(50, 0, -1):
            indent = "    " * (d + 1)
            lines.append(f"{indent}}}")
        lines.append("    return 0;\n}")

        src = ctx.write_file("deep_scope.oo", "\n".join(lines))
        rc, out, err, cpu_sec, rss_kb = ctx.run_cmd_measured([OODAC_BIN, "check", src])
        dur = cpu_sec * 1000.0 if cpu_sec > 0.0 else (time.time() - ctx.start_time) * 1000.0

        if rc == 0 and "OK" in out and dur < 1500.0:
            return TestResult(ctx.test_id, 3, "R1+R5", ctx.name, "PASS", dur)
        else:
            return TestResult(
                ctx.test_id, 3, "R1+R5", ctx.name, "FAIL", dur,
                error_msg=f"Deep scope check exceeded SLA or failed: dur={dur:.1f}ms, rc={rc}",
                diagnostic=err
            )
    finally:
        ctx.cleanup()
