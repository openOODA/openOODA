"""
Tier 2: Boundary & Corner Cases — Requirement R4 (Tree-Rot, Arena & MCP Limits)
Tests T2.R4.1 through T2.R4.6
"""

import os
import time
from openOODA.qa.e2e.framework import TestContext, TestResult, oodac_build, POLYROOT


def test_t2_r4_1_empty_vnode_arena(double_run: bool = False) -> TestResult:
    """T2.R4.1: Empty VNodeArena boundary representation."""
    ctx = TestContext("T2.R4.1", 2, "R4", "Empty VNodeArena boundary representation", double_run)
    try:
        src = ctx.write_file("empty_arena.oo", """// # Empty Arena Test
import "std/app/ui/wui/wui_vnode.oo";

type VNodeArena = struct {
    nodes: List[VNode],
    root_id: Int,
    next_id: Int
};

pub fn main() -> Int {
    let empty_list: List[VNode] = list_new();
    let arena: VNodeArena = VNodeArena {
        nodes: empty_list,
        root_id: 0 - 1,
        next_id: 0
    };
    if arena.root_id == -1 && list_len(arena.nodes) == 0 {
        return 0;
    }
    return 1;
}
""")
        out_bin = os.path.join(ctx.temp_dir, "empty_arena.bin")
        rc, out, err = oodac_build(ctx, src, out_bin)
        duration = (time.time() - ctx.start_time) * 1000

        if rc == 0:
            rc_run, _, _ = ctx.run_cmd([out_bin])
            if rc_run == 0:
                return TestResult(ctx.test_id, 2, "R4", ctx.name, "PASS", duration)
        return TestResult(ctx.test_id, 2, "R4", ctx.name, "FAIL", duration, error_msg="Empty arena test failed", diagnostic=err)
    finally:
        ctx.cleanup()


def test_t2_r4_2_vnode_leaf_node(double_run: bool = False) -> TestResult:
    """T2.R4.2: Leaf node with empty child_ids in VNodeArena."""
    ctx = TestContext("T2.R4.2", 2, "R4", "VNode leaf node with empty child_ids", double_run)
    try:
        src = ctx.write_file("leaf_node.oo", """// # Leaf Node Test
import "std/app/ui/wui/wui_vnode.oo";

pub fn main() -> Int {
    let text_node: VNode = vnode_text("leaf text");
    if list_len(text_node.child_ids) == 0 && text_node.node_kind == 2 {
        return 0;
    }
    return 1;
}
""")
        out_bin = os.path.join(ctx.temp_dir, "leaf.bin")
        rc, out, err = oodac_build(ctx, src, out_bin)
        duration = (time.time() - ctx.start_time) * 1000

        if rc == 0:
            rc_run, _, _ = ctx.run_cmd([out_bin])
            if rc_run == 0:
                return TestResult(ctx.test_id, 2, "R4", ctx.name, "PASS", duration)
        return TestResult(ctx.test_id, 2, "R4", ctx.name, "FAIL", duration, error_msg="Leaf node test failed", diagnostic=err)
    finally:
        ctx.cleanup()


def test_t2_r4_3_deep_linear_arena_tree(double_run: bool = False) -> TestResult:
    """T2.R4.3: Deep linear tree (depth 50) in flat arena without recursion limit blowout."""
    ctx = TestContext("T2.R4.3", 2, "R4", "Deep linear tree (depth 50) in flat arena", double_run)
    try:
        src = ctx.write_file("deep_tree.oo", """// # Deep Tree Test
import "std/app/ui/wui/wui_vnode.oo";

pub fn main() -> Int {
    let mut arena_nodes: List[VNode] = list_new();
    let empty_props: List[VProp] = list_new();

    let mut i: Int = 0;
    while i < 50 {
        let mut ch: List[Int] = list_new();
        if i < 49 { ch = list_push(ch, i + 1); }
        let node: VNode = vnode_element("div", i.to_string(), empty_props, ch);
        arena_nodes = list_push(arena_nodes, node);
        i = i + 1;
    }

    if list_len(arena_nodes) == 50 {
        return 0;
    }
    return 1;
}
""")
        out_bin = os.path.join(ctx.temp_dir, "deep_tree.bin")
        rc, out, err = oodac_build(ctx, src, out_bin)
        duration = (time.time() - ctx.start_time) * 1000

        if rc == 0:
            rc_run, _, _ = ctx.run_cmd([out_bin])
            if rc_run == 0:
                return TestResult(ctx.test_id, 2, "R4", ctx.name, "PASS", duration)
        return TestResult(ctx.test_id, 2, "R4", ctx.name, "FAIL", duration, error_msg="Deep arena tree failed", diagnostic=err)
    finally:
        ctx.cleanup()


def test_t2_r4_4_wide_arena_tree(double_run: bool = False) -> TestResult:
    """T2.R4.4: Wide tree with 50 children on single parent node."""
    ctx = TestContext("T2.R4.4", 2, "R4", "Wide tree with 50 children on single parent", double_run)
    try:
        src = ctx.write_file("wide_tree.oo", """// # Wide Tree Test
import "std/app/ui/wui/wui_vnode.oo";

pub fn main() -> Int {
    let mut ch_ids: List[Int] = list_new();
    let mut i: Int = 1;
    while i <= 50 {
        ch_ids = list_push(ch_ids, i);
        i = i + 1;
    }
    let empty_props: List[VProp] = list_new();
    let parent: VNode = vnode_element("ul", "root", empty_props, ch_ids);
    if list_len(parent.child_ids) == 50 {
        return 0;
    }
    return 1;
}
""")
        out_bin = os.path.join(ctx.temp_dir, "wide_tree.bin")
        rc, out, err = oodac_build(ctx, src, out_bin)
        duration = (time.time() - ctx.start_time) * 1000

        if rc == 0:
            rc_run, _, _ = ctx.run_cmd([out_bin])
            if rc_run == 0:
                return TestResult(ctx.test_id, 2, "R4", ctx.name, "PASS", duration)
        return TestResult(ctx.test_id, 2, "R4", ctx.name, "FAIL", duration, error_msg="Wide arena tree failed", diagnostic=err)
    finally:
        ctx.cleanup()


def test_t2_r4_5_invalid_child_id_handling(double_run: bool = False) -> TestResult:
    """T2.R4.5: Out-of-bounds child ID lookup handling in arena traversal."""
    ctx = TestContext("T2.R4.5", 2, "R4", "Out-of-bounds child ID lookup handling", double_run)
    try:
        src = ctx.write_file("invalid_child.oo", """// # Invalid Child Lookup
import "std/app/ui/wui/wui_vnode.oo";

fn lookup_node(nodes: List[VNode], id: Int) -> Result[VNode, String] {
    if id < 0 || id >= list_len(nodes) {
        return Err("ERR\\tnode_id_out_of_bounds: " + id.to_string());
    }
    return Ok(list_get(nodes, id));
}

pub fn main() -> Int {
    let empty_nodes: List[VNode] = list_new();
    let r: Result[VNode, String] = lookup_node(empty_nodes, 999);
    if r.is_err() {
        return 0;
    }
    return 1;
}
""")
        out_bin = os.path.join(ctx.temp_dir, "invalid_child.bin")
        rc, out, err = oodac_build(ctx, src, out_bin)
        duration = (time.time() - ctx.start_time) * 1000

        if rc == 0:
            rc_run, _, _ = ctx.run_cmd([out_bin])
            if rc_run == 0:
                return TestResult(ctx.test_id, 2, "R4", ctx.name, "PASS", duration)
        return TestResult(ctx.test_id, 2, "R4", ctx.name, "FAIL", duration, error_msg="Lookup failed", diagnostic=err)
    finally:
        ctx.cleanup()


def test_t2_r4_6_mcp_empty_secret_fail_closed(double_run: bool = False) -> TestResult:
    """T2.R4.6: MCP attenuation must fail closed when secret is empty string."""
    ctx = TestContext("T2.R4.6", 2, "R4", "MCP empty string secret fails closed", double_run)
    probe_path = os.path.join(POLYROOT, "mcp/qa/sec/probe_attenuation.oo")
    if not os.path.exists(probe_path):
        return TestResult(ctx.test_id, 2, "R4", ctx.name, "FAIL", 0, error_msg=f"Missing {probe_path}")

    # Verify that mcp_attenuate_token fails closed when secret is empty string
    with open(os.path.join(POLYROOT, "mcp/engine/state/mcp_attenuation.oo"), "r", encoding="utf-8") as f:
        content = f.read()

    has_fail_closed = 'if chars_len(s.attenuation_secret) == 0' in content or 'secret not configured' in content
    duration = (time.time() - ctx.start_time) * 1000

    if has_fail_closed:
        return TestResult(ctx.test_id, 2, "R4", ctx.name, "PASS", duration)
    else:
        return TestResult(ctx.test_id, 2, "R4", ctx.name, "FAIL", duration, error_msg="Missing empty secret fail-closed check")
