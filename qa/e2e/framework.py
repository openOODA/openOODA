"""
openOODA E2E Test Suite Framework
Provides test primitives, execution harnesses, metrics collectors, and reporters.
"""

import dataclasses
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

POLYROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
OODAC_BIN = os.environ.get("OODA_COMPILER") or shutil.which("oodac") or os.path.join(POLYROOT, "oodac/bin/oodac")
if not os.path.exists(OODAC_BIN):
    user_oodac = os.path.expanduser("~/.openooda/bin/oodac")
    if os.path.exists(user_oodac):
        OODAC_BIN = user_oodac

CLI_BIN = shutil.which("cli") or os.path.join(POLYROOT, "cli/dist/cli")
if not os.path.exists(CLI_BIN):
    user_cli = os.path.expanduser("~/.openooda/bin/cli")
    if os.path.exists(user_cli):
        CLI_BIN = user_cli


@dataclasses.dataclass
class TestResult:
    test_id: str
    tier: int
    domain: str
    name: str
    status: str  # "PASS", "FAIL", "SKIP"
    duration_ms: float
    error_msg: str = ""
    diagnostic: str = ""
    run1_output: str = ""
    run2_output: str = ""
    is_deterministic: bool = True


class TestContext:
    def __init__(self, test_id: str, tier: int, domain: str, name: str, double_run: bool = False):
        self.test_id = test_id
        self.tier = tier
        self.domain = domain
        self.name = name
        self.double_run = double_run
        self.temp_dir = tempfile.mkdtemp(prefix=f"e2e_{test_id}_")
        self.start_time = time.time()

    def cleanup(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def write_file(self, rel_path: str, content: str) -> str:
        abs_path = os.path.join(self.temp_dir, rel_path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(content)
        return abs_path

    def read_file(self, rel_path: str) -> str:
        abs_path = os.path.join(self.temp_dir, rel_path)
        with open(abs_path, "r", encoding="utf-8") as f:
            return f.read()

    def run_cmd(
        self,
        cmd: List[str],
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: int = 60,
    ) -> Tuple[int, str, str]:
        run_env = os.environ.copy()
        run_env["OODA_POLYROOT"] = POLYROOT
        run_env["OODA_COMPILER"] = OODAC_BIN
        if env:
            run_env.update(env)

        try:
            proc = subprocess.run(
                cmd,
                cwd=cwd or self.temp_dir,
                env=run_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout,
            )
            return proc.returncode, proc.stdout, proc.stderr
        except subprocess.TimeoutExpired as te:
            out = te.stdout or ""
            err = te.stderr or ""
            if isinstance(out, bytes):
                out = out.decode("utf-8", "replace")
            if isinstance(err, bytes):
                err = err.decode("utf-8", "replace")
            return 124, out, f"Command timed out after {timeout} seconds: {err}"

    def run_cmd_measured(
        self,
        cmd: List[str],
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: int = 60,
    ) -> Tuple[int, str, str, float, int]:
        """Runs command measuring returncode, stdout, stderr, cpu_sec, peak_rss_kb."""
        time_bin = shutil.which("time") or "/usr/bin/time"
        run_env = os.environ.copy()
        run_env["OODA_POLYROOT"] = POLYROOT
        run_env["OODA_COMPILER"] = OODAC_BIN
        if env:
            run_env.update(env)

        full_cmd = [time_bin, "-v"] + cmd
        try:
            proc = subprocess.run(
                full_cmd,
                cwd=cwd or self.temp_dir,
                env=run_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            return 124, "", f"Command timed out after {timeout} seconds", 0.0, 0

        cpu_sec = 0.0
        peak_rss_kb = 0
        stderr_clean = []
        for line in proc.stderr.splitlines():
            if "User time (seconds):" in line:
                try:
                    cpu_sec += float(line.split(":")[1].strip())
                except ValueError:
                    pass
            elif "System time (seconds):" in line:
                try:
                    cpu_sec += float(line.split(":")[1].strip())
                except ValueError:
                    pass
            elif "Maximum resident set size (kbytes):" in line:
                try:
                    peak_rss_kb = int(line.split(":")[1].strip())
                except ValueError:
                    pass
            else:
                stderr_clean.append(line)

        return proc.returncode, proc.stdout, "\n".join(stderr_clean), cpu_sec, peak_rss_kb


def oodac_check(ctx: TestContext, file_path: str, cwd: Optional[str] = None) -> Tuple[int, str, str]:
    return ctx.run_cmd([OODAC_BIN, "check", file_path], cwd=cwd or POLYROOT)


def oodac_build(ctx: TestContext, file_path: str, out_bin: str, cwd: Optional[str] = None) -> Tuple[int, str, str]:
    return ctx.run_cmd([OODAC_BIN, "build", file_path, "-o", out_bin], cwd=cwd or POLYROOT)


def cli_run(ctx: TestContext, file_path: str, cwd: Optional[str] = None) -> Tuple[int, str, str]:
    return ctx.run_cmd([CLI_BIN, "run", file_path], cwd=cwd or POLYROOT)


def cli_build(ctx: TestContext, file_path: str, cwd: Optional[str] = None) -> Tuple[int, str, str]:
    return ctx.run_cmd([CLI_BIN, "build", file_path], cwd=cwd or POLYROOT)


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()
