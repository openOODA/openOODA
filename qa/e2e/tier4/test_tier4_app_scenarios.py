"""
Tier 4: Real-World Application Scenarios
Tests T4.APP1 through T4.APP5
"""

import hashlib
import os
import time
from openOODA.qa.e2e.framework import (
    TestContext, TestResult, cli_run, cli_build, oodac_build, oodac_check, sha256_file, POLYROOT
)


def test_t4_app1_cli_application_lifecycle(double_run: bool = False) -> TestResult:
    """T4.APP1: Scenario 1 — Full CLI Application Lifecycle (author -> build -> run)."""
    ctx = TestContext("T4.APP1", 4, "APP", "Full CLI Application Lifecycle (author -> build -> run)", double_run)
    try:
        app_src = ctx.write_file("service.oo", """// # Sovereign Telemetry Service
// Logline: Autonomous service logging node events.
// Setup: Sovereign CLI driver execution.
// Beats: Format and emit telemetry record.

pub fn main() -> Int {
    println("SERVICE_STATUS: OK");
    println("TELEMETRY_EMIT: 100_EVENTS_PROCESSED");
    return 0;
}
""")
        # Run using CLI driver
        rc, out, err = cli_run(ctx, app_src)
        duration = (time.time() - ctx.start_time) * 1000

        expected_tokens = ["SERVICE_STATUS: OK", "TELEMETRY_EMIT: 100_EVENTS_PROCESSED"]
        if rc == 0 and all(t in out for t in expected_tokens):
            return TestResult(ctx.test_id, 4, "APP", ctx.name, "PASS", duration)
        else:
            return TestResult(
                ctx.test_id, 4, "APP", ctx.name, "FAIL", duration,
                error_msg=f"CLI run failed: rc={rc}", diagnostic=f"out={out}\nerr={err}"
            )
    finally:
        ctx.cleanup()


def test_t4_app2_deterministic_release_pipeline(double_run: bool = False) -> TestResult:
    """T4.APP2: Scenario 2 — Bit-Identical Sovereign CI Release Pipeline."""
    ctx = TestContext("T4.APP2", 4, "APP", "Bit-Identical CI Release Pipeline (double compilation)", double_run)
    try:
        release_src = ctx.write_file("release_app.oo", """// # Release Target
pub fn compute_checksum(val: Int) -> Int {
    return val * 31 + 17;
}

pub fn main() -> Int {
    let res: Int = compute_checksum(42);
    println("RELEASE_DIGEST: " + res.to_string());
    return 0;
}
""")
        bin1 = os.path.join(ctx.temp_dir, "release_v1.bin")
        bin2 = os.path.join(ctx.temp_dir, "release_v2.bin")

        rc1, _, err1 = oodac_build(ctx, release_src, bin1)
        rc2, _, err2 = oodac_build(ctx, release_src, bin2)
        duration = (time.time() - ctx.start_time) * 1000

        if rc1 != 0 or rc2 != 0:
            return TestResult(
                ctx.test_id, 4, "APP", ctx.name, "FAIL", duration,
                error_msg="Release compilation failed", diagnostic=f"err1={err1}, err2={err2}"
            )

        h1 = sha256_file(bin1)
        h2 = sha256_file(bin2)

        if h1 == h2:
            return TestResult(ctx.test_id, 4, "APP", ctx.name, "PASS", duration)
        else:
            return TestResult(
                ctx.test_id, 4, "APP", ctx.name, "FAIL", duration,
                error_msg=f"Deterministic release failed: binary hash mismatch ({h1} != {h2})"
            )
    finally:
        ctx.cleanup()


def test_t4_app3_wui_dom_hierarchy_rendering(double_run: bool = False) -> TestResult:
    """T4.APP3: Scenario 3 — WUI Component Hierarchy Rendering & Arena Traversal."""
    ctx = TestContext("T4.APP3", 4, "APP", "WUI Component Hierarchy Rendering & Arena Traversal", double_run)
    try:
        src = ctx.write_file("wui_cockpit.oo", """// # WUI Cockpit Tree
import "std/app/ui/wui/wui_vnode.oo";

type VNodeArena = struct {
    nodes: List[VNode],
    root_id: Int,
    next_id: Int
};

fn add_node(arena: &mut VNodeArena, node: VNode) -> Int {
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

    // 1. Text badge: 'CYBERPUNK COCKPIT'
    let title_id: Int = add_node(&mut arena, vnode_text("CYBERPUNK COCKPIT"));

    // 2. Status badge: 'STATUS: ACTIVE'
    let badge_id: Int = add_node(&mut arena, vnode_text("STATUS: ACTIVE"));

    // 3. Card container holding badge and title
    let mut card_children: List[Int] = list_new();
    card_children = list_push(card_children, title_id);
    card_children = list_push(card_children, badge_id);

    let card_id: Int = add_node(&mut arena, vnode_element("div", "card", list_new(), card_children));
    arena.root_id = card_id;

    // Verify traversal
    let root: VNode = list_get(arena.nodes, arena.root_id);
    let ch_count: Int = list_len(root.child_ids);

    if ch_count == 2 && list_len(arena.nodes) == 3 {
        println("COCKPIT_TREE_RENDERED: SUCCESS");
        return 0;
    }
    return 1;
}
""")
        out_bin = os.path.join(ctx.temp_dir, "cockpit.bin")
        rc, out, err = oodac_build(ctx, src, out_bin)
        duration = (time.time() - ctx.start_time) * 1000

        if rc != 0:
            return TestResult(ctx.test_id, 4, "APP", ctx.name, "FAIL", duration, error_msg="Build failed", diagnostic=err)

        rc_run, out_run, _ = ctx.run_cmd([out_bin])
        if rc_run == 0 and "COCKPIT_TREE_RENDERED: SUCCESS" in out_run:
            return TestResult(ctx.test_id, 4, "APP", ctx.name, "PASS", duration)
        else:
            return TestResult(
                ctx.test_id, 4, "APP", ctx.name, "FAIL", duration,
                error_msg=f"Runtime failure: {out_run}"
            )
    finally:
        ctx.cleanup()


def test_t4_app4_crypto_package_manifest_verification(double_run: bool = False) -> TestResult:
    """T4.APP4: Scenario 4 — Cryptographic Package Manifest Verification with SHA-512."""
    ctx = TestContext("T4.APP4", 4, "APP", "Cryptographic Package Manifest Verification with SHA-512", double_run)
    manifest_payload = "pkg_name=sovereign_core\nversion=1.0.0\nauthor=openOODA\nlicense=MIT\n"
    expected_digest = hashlib.sha512(manifest_payload.encode("ascii")).hexdigest()

    try:
        src = ctx.write_file("pkg_verify.oo", f"""// # Package Manifest Verifier
import "std/sec/hash/sha512.oo";

pub fn main() -> Int {{
    let payload: String = "pkg_name=sovereign_core\\nversion=1.0.0\\nauthor=openOODA\\nlicense=MIT\\n";
    let computed_digest: String = sha512(payload);
    let expected: String = "{expected_digest}";

    if computed_digest == expected {{
        println("MANIFEST_INTEGRITY_VERIFIED: PASS");
        return 0;
    }} else {{
        println("MANIFEST_INTEGRITY_VERIFIED: FAIL");
        return 1;
    }}
}}
""")
        out_bin = os.path.join(ctx.temp_dir, "pkg_verify.bin")
        rc, out, err = oodac_build(ctx, src, out_bin)
        duration = (time.time() - ctx.start_time) * 1000

        if rc != 0:
            return TestResult(ctx.test_id, 4, "APP", ctx.name, "FAIL", duration, error_msg="Build failed", diagnostic=err)

        rc_run, out_run, _ = ctx.run_cmd([out_bin])
        if rc_run == 0 and "MANIFEST_INTEGRITY_VERIFIED: PASS" in out_run:
            return TestResult(ctx.test_id, 4, "APP", ctx.name, "PASS", duration)
        else:
            return TestResult(
                ctx.test_id, 4, "APP", ctx.name, "FAIL", duration,
                error_msg=f"Manifest verification failed: {out_run}"
            )
    finally:
        ctx.cleanup()


def test_t4_app5_multimodule_package_verification(double_run: bool = False) -> TestResult:
    """T4.APP5: Scenario 5 — Multi-Module Sovereign Package Verification with Sub-Second Cache Re-check."""
    ctx = TestContext("T4.APP5", 4, "APP", "Multi-Module Sovereign Package Verification with Cache Re-check", double_run)
    try:
        # Structure a sovereign package with core, net, and root anchor
        ctx.write_file("sovereign_pkg/core/types.oo", """// # Core Types
pub type Config = struct { timeout_ms: Int, retries: Int };
pub fn default_config() -> Config { return Config { timeout_ms: 5000, retries: 3 }; }
""")
        ctx.write_file("sovereign_pkg/core/anchor.oo", """// # Core Anchor
import "./types.oo";
pub fn core_init() -> Config { return default_config(); }
""")
        ctx.write_file("sovereign_pkg/net/client.oo", """// # Net Client
pub fn connect(retries: Int) -> Int { return retries; }
""")
        ctx.write_file("sovereign_pkg/net/anchor.oo", """// # Net Anchor
import "./client.oo";
pub fn net_init(retries: Int) -> Int { return connect(retries); }
""")
        root_anchor = ctx.write_file("sovereign_pkg/anchor.oo", """// # Sovereign Pkg Root Anchor
import "./core/anchor.oo";
import "./net/anchor.oo";

pub fn run_package() -> Int {
    let cfg: Config = core_init();
    return net_init(cfg.retries);
}

pub fn main() -> Int {
    let r: Int = run_package();
    println("PACKAGE_RUN: " + r.to_string());
    return 0;
}
""")
        # First check (compiles and seeds cache)
        rc1, out1, _ = oodac_check(ctx, root_anchor)
        if rc1 != 0:
            return TestResult(ctx.test_id, 4, "APP", ctx.name, "FAIL", 0, error_msg="Initial check failed")

        # Second check (warm cache SLA < 0.5s)
        t0 = time.time()
        rc2, out2, _ = oodac_check(ctx, root_anchor)
        dur = (time.time() - t0) * 1000

        if rc2 == 0 and "OK" in out2 and dur < 500.0:
            return TestResult(ctx.test_id, 4, "APP", ctx.name, "PASS", dur)
        else:
            return TestResult(
                ctx.test_id, 4, "APP", ctx.name, "FAIL", dur,
                error_msg=f"Multi-module warm check exceeded 500ms SLA or failed: dur={dur:.1f}ms, rc={rc2}"
            )
    finally:
        ctx.cleanup()
