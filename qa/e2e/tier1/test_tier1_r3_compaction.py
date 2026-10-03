"""
Tier 1: Feature Coverage — Requirement R3 (Source Outlier Algorithmic Compaction)
Tests T1.R3.1 through T1.R3.5
"""

import hashlib
import os
import re
import time
from openOODA.qa.e2e.framework import TestContext, TestResult, oodac_build, POLYROOT


def test_t1_r3_1_sha512_sliding_window(double_run: bool = False) -> TestResult:
    """T1.R3.1: Verify s5_compress uses 16-variable sliding window instead of unrolled 80 variables."""
    ctx = TestContext("T1.R3.1", 1, "R3", "SHA-512 16-variable sliding window compaction", double_run)
    target = os.path.join(POLYROOT, "std/sec/hash/sha512.oo")
    if not os.path.exists(target):
        return TestResult(ctx.test_id, 1, "R3", ctx.name, "FAIL", 0, error_msg=f"Missing {target}")

    with open(target, "r", encoding="utf-8") as f:
        content = f.read()

    # In the unrolled version, variables w16 through w79 existed.
    # In the compacted 16-variable sliding window, only w0 through w15 exist.
    has_unrolled_vars = any(f"w{i}:" in content or f"w{i} =" in content for i in range(16, 80))
    has_sliding_window = "w0 = w1;" in content and "w14 = w15;" in content

    duration = (time.time() - ctx.start_time) * 1000
    if not has_unrolled_vars and has_sliding_window:
        return TestResult(ctx.test_id, 1, "R3", ctx.name, "PASS", duration)
    else:
        return TestResult(
            ctx.test_id, 1, "R3", ctx.name, "FAIL", duration,
            error_msg="SHA-512 retains unrolled variables or lacks sliding window loop"
        )


def test_t1_r3_2_monolithic_fn_length(double_run: bool = False) -> TestResult:
    """T1.R3.2: Verify s5_compress and s_compress function lengths comply with <= 40 lines limit."""
    ctx = TestContext("T1.R3.2", 1, "R3", "Function length <= 40 lines for SHA-512 helpers", double_run)
    targets = [
        ("std/sec/hash/sha512.oo", "s5_compress"),
        ("std/sec/hash/sha512_compress.oo", "s_compress"),
    ]

    violations = []
    fn_re = re.compile(r"^[ \t]*(?:pub[ \t]+)?fn[ \t]+([A-Za-z0-9_]+)")

    for rel_path, target_fn in targets:
        p = os.path.join(POLYROOT, rel_path)
        if not os.path.exists(p):
            violations.append(f"{rel_path}: file missing")
            continue
        with open(p, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for idx, line in enumerate(lines):
            m = fn_re.match(line)
            if m and m.group(1) == target_fn:
                depth = 0
                begun = False
                end_idx = len(lines) - 1
                for j in range(idx, len(lines)):
                    for ch in lines[j]:
                        if ch == "{":
                            depth += 1
                            begun = True
                        elif ch == "}":
                            depth -= 1
                    if begun and depth <= 0:
                        end_idx = j
                        break
                fn_len = end_idx - idx + 1
                if fn_len > 40:
                    violations.append(f"{rel_path}:{target_fn} ({fn_len} lines > 40)")

    duration = (time.time() - ctx.start_time) * 1000
    if not violations:
        return TestResult(ctx.test_id, 1, "R3", ctx.name, "PASS", duration)
    else:
        return TestResult(
            ctx.test_id, 1, "R3", ctx.name, "FAIL", duration,
            error_msg=f"Functions exceed 40-line ceiling: {', '.join(violations)}"
        )


def test_t1_r3_3_sha512_nist_empty_string(double_run: bool = False) -> TestResult:
    """T1.R3.3: Verify SHA-512 NIST KAT vector for empty string ("")."""
    ctx = TestContext("T1.R3.3", 1, "R3", "SHA-512 NIST KAT vector: empty string", double_run)
    expected_digest = hashlib.sha512(b"").hexdigest()
    try:
        src = ctx.write_file("test_sha_empty.oo", """// # SHA-512 Empty String Test
// Logline: FIPS 180-4 empty string test vector.
// Setup: Import std/sec/hash/sha512.oo.
// Beats: Print digest.

import "std/sec/hash/sha512.oo";

pub fn main() -> Int {
    let d: String = sha512("");
    print(d);
    return 0;
}
""")
        out_bin = os.path.join(ctx.temp_dir, "sha_empty.bin")
        rc, out, err = oodac_build(ctx, src, out_bin)
        duration = (time.time() - ctx.start_time) * 1000

        if rc != 0:
            return TestResult(ctx.test_id, 1, "R3", ctx.name, "FAIL", duration, error_msg="Build failed", diagnostic=err)

        rc_run, out_run, _ = ctx.run_cmd([out_bin])
        if rc_run == 0 and out_run.strip() == expected_digest:
            return TestResult(ctx.test_id, 1, "R3", ctx.name, "PASS", duration)
        else:
            return TestResult(
                ctx.test_id, 1, "R3", ctx.name, "FAIL", duration,
                error_msg=f"Digest mismatch: got {out_run.strip()}, expected {expected_digest}"
            )
    finally:
        ctx.cleanup()


def test_t1_r3_4_sha512_nist_abc(double_run: bool = False) -> TestResult:
    """T1.R3.4: Verify SHA-512 NIST KAT vector for 'abc'."""
    ctx = TestContext("T1.R3.4", 1, "R3", "SHA-512 NIST KAT vector: 'abc'", double_run)
    expected_digest = hashlib.sha512(b"abc").hexdigest()
    try:
        src = ctx.write_file("test_sha_abc.oo", """// # SHA-512 'abc' Test
// Logline: FIPS 180-4 'abc' test vector.
// Setup: Import std/sec/hash/sha512.oo.
// Beats: Print digest.

import "std/sec/hash/sha512.oo";

pub fn main() -> Int {
    let d: String = sha512("abc");
    print(d);
    return 0;
}
""")
        out_bin = os.path.join(ctx.temp_dir, "sha_abc.bin")
        rc, out, err = oodac_build(ctx, src, out_bin)
        duration = (time.time() - ctx.start_time) * 1000

        if rc != 0:
            return TestResult(ctx.test_id, 1, "R3", ctx.name, "FAIL", duration, error_msg="Build failed", diagnostic=err)

        rc_run, out_run, _ = ctx.run_cmd([out_bin])
        if rc_run == 0 and out_run.strip() == expected_digest:
            return TestResult(ctx.test_id, 1, "R3", ctx.name, "PASS", duration)
        else:
            return TestResult(
                ctx.test_id, 1, "R3", ctx.name, "FAIL", duration,
                error_msg=f"Digest mismatch: got {out_run.strip()}, expected {expected_digest}"
            )
    finally:
        ctx.cleanup()


def test_t1_r3_5_sha512_nist_multiblock(double_run: bool = False) -> TestResult:
    """T1.R3.5: Verify SHA-512 NIST KAT vector for 112-byte multi-block message."""
    ctx = TestContext("T1.R3.5", 1, "R3", "SHA-512 NIST KAT vector: 112-byte multi-block", double_run)
    msg_bytes = b"abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu"
    expected_digest = hashlib.sha512(msg_bytes).hexdigest()
    msg_str = msg_bytes.decode("ascii")

    try:
        src = ctx.write_file("test_sha_multiblock.oo", f"""// # SHA-512 Multi-Block Test
// Logline: FIPS 180-4 112-byte vector.
// Setup: Import std/sec/hash/sha512.oo.
// Beats: Print digest.

import "std/sec/hash/sha512.oo";

pub fn main() -> Int {{
    let d: String = sha512("{msg_str}");
    print(d);
    return 0;
}}
""")
        out_bin = os.path.join(ctx.temp_dir, "sha_multiblock.bin")
        rc, out, err = oodac_build(ctx, src, out_bin)
        duration = (time.time() - ctx.start_time) * 1000

        if rc != 0:
            return TestResult(ctx.test_id, 1, "R3", ctx.name, "FAIL", duration, error_msg="Build failed", diagnostic=err)

        rc_run, out_run, _ = ctx.run_cmd([out_bin])
        if rc_run == 0 and out_run.strip() == expected_digest:
            return TestResult(ctx.test_id, 1, "R3", ctx.name, "PASS", duration)
        else:
            return TestResult(
                ctx.test_id, 1, "R3", ctx.name, "FAIL", duration,
                error_msg=f"Digest mismatch: got {out_run.strip()}, expected {expected_digest}"
            )
    finally:
        ctx.cleanup()
