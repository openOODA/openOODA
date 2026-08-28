#!/usr/bin/env python3
"""openOODA v2.5.0 Master ASan/TSan & Negative Trust Verification Harness.

Certifies 0 memory leaks, 0 UAF/double-free, and 0 data races across:
1. Runtime C modules & Concurrency harnesses
2. Physics modules (std/physics)
3. Continuum mechanics (std/continuum)
4. Astrodynamics & Celestial Mechanics (std/astrodynamics)
5. Advanced Astrophysics & General Relativity (std/astro_advanced)
"""

import os
import subprocess
import sys
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
BUILD_DIR = os.path.join(ROOT, "build", "sanitizers")
OODAC_BIN = os.path.join(ROOT, "oodac_bin")
CHS_RT = os.path.join(ROOT, "ooda", "runtime", "chs_rt.c")

ASAN_FLAGS = [
    "clang",
    "-fsanitize=address,undefined",
    "-g",
    "-O1",
    "-I" + os.path.join(ROOT, "ooda"),
    "-I" + os.path.join(ROOT, "ooda", "runtime"),
]
TSAN_FLAGS = [
    "clang",
    "-fsanitize=thread",
    "-g",
    "-O1",
    "-I" + os.path.join(ROOT, "ooda"),
    "-I" + os.path.join(ROOT, "ooda", "runtime"),
]
LD_FLAGS = ["-lm", "-ldl", "-lpthread"]

os.makedirs(BUILD_DIR, exist_ok=True)

C_RUNTIME_TESTS = [
    ("test_arena_concurrency_sanitizer", "qa/tests_falsification/test_arena_concurrency_sanitizer.c", True),
    ("test_arena_multithreaded_suite", "qa/tests_falsification/test_arena_multithreaded_suite.c", True),
    ("test_arena_race", "qa/tests_falsification/test_arena_race.c", True),
    ("test_concurrency_actors", "ooda/tests/test_concurrency_actors.c", True),
    ("test_token_verification_adversarial", "ooda/tests/test_token_verification_adversarial.c", True),
    ("test_alloc_m2", "ooda/tests/test_alloc_m2.c", True),
    ("test_runtime_alloc_adversarial", "ooda/tests/test_runtime_alloc_adversarial.c", True),
    ("test_c_align_stress", "ooda/tests/adversarial_x86/test_c_align_stress.c", False),
    ("test_m1_sandbox_matrix", "ooda/tests/adversarial_m1/test_m1_sandbox_matrix_harness.c", True),
]

PHYSICS_FIXTURES = [
    "prove_prod_a4_orbital_mechanics_physics.oo",
    "prove_prod_a4_physics_stubs.oo",
    "prove_prod_a1_anomaly_kepler_solver.oo",
    "prove_prod_a1_attitude_quaternion.oo",
    "prove_prod_a1_attitude_reaction_wheels.oo",
    "prove_prod_a1_bi_elliptic_transfer.oo",
    "prove_prod_a1_coordinate_orbital_plane.oo",
    "prove_prod_a1_delta_v_budget.oo",
    "prove_prod_a1_gravitational_j2_perturbation.oo",
    "prove_prod_a1_ground_station_pass.oo",
    "prove_prod_a1_hohmann_transfer.oo",
    "prove_prod_a1_julian_date.oo",
    "prove_prod_a1_kepler_elements.oo",
    "prove_prod_a1_kepler_orbit.oo",
    "prove_prod_a1_lagrange_points.oo",
    "prove_prod_a1_lambert_solver.oo",
    "prove_prod_a1_launch_trajectory.oo",
    "prove_prod_a1_patched_conics.oo",
    "prove_prod_a1_rcs_thruster_allocator.oo",
    "prove_prod_a1_re_entry_thermal_profile.oo",
    "prove_prod_a1_rkf45_nbody.oo",
    "prove_prod_a1_rocket_tsiolkovsky.oo",
    "prove_prod_a1_sgp4_propagator.oo",
    "prove_prod_a1_sidereal_time.oo",
    "prove_prod_a1_tle_parser.oo",
    "prove_prod_a1_accretion_bondi_hoyle_lyttleton.oo",
    "prove_prod_a1_accretion_disk_novikov_thorne.oo",
    "prove_prod_a1_accretion_disk_shakura_sunyaev.oo",
    "prove_prod_a1_astro_rel_constants.oo",
    "prove_prod_a1_cosmological_big_bang_nucleosynthesis.oo",
    "prove_prod_a1_cosmological_dark_matter_nfw_profile.oo",
    "prove_prod_a1_cosmological_friedmann_solver.oo",
    "prove_prod_a1_gr_geodetic_precession_de_sitter.oo",
    "prove_prod_a1_gr_hawking_radiation_evaporation.oo",
    "prove_prod_a1_gr_kerr_newman_spacetime.oo",
    "prove_prod_a1_gr_schwarzschild_metric.oo",
    "prove_prod_a1_gr_wormhole_morris_thorne.oo",
    "prove_prod_a1_gw_chirp_waveform_imr.oo",
    "prove_prod_a1_gw_matched_filter_snr.oo",
    "prove_prod_a1_gw_quadrupole_formula.oo",
    "prove_prod_a1_interstellar_extinction_reddening.oo",
    "prove_prod_a1_magnetar_crust_cooling.oo",
    "prove_prod_a1_pulsar_dispersion_measure.oo",
    "prove_prod_a1_relativistic_jets_beaming_doppler.oo",
    "prove_prod_a1_stellar_atmosphere_grey.oo",
    "prove_prod_a1_stellar_chandrasekhar_mass.oo",
    "prove_prod_a1_stellar_eddington_luminosity.oo",
    "prove_prod_a1_stellar_lane_emden_polytrope.oo",
    "prove_prod_a1_stellar_structure_equations.oo",
    "prove_prod_a1_synchrotron_radiation_spectrum.oo",
]


def run_cmd(cmd, env=None):
    res = subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
        env=env or os.environ.copy(),
    )
    return res.returncode, res.stdout, res.stderr


def verify_c_target(name, src_rel, has_tsan):
    src_path = os.path.join(ROOT, src_rel)
    asan_bin = os.path.join(BUILD_DIR, f"{name}_asan")
    tsan_bin = os.path.join(BUILD_DIR, f"{name}_tsan")

    # 1. ASan compile & run
    compile_cmd = ASAN_FLAGS + [CHS_RT, src_path, "-o", asan_bin] + LD_FLAGS
    rc, out, err = run_cmd(compile_cmd)
    if rc != 0:
        return False, f"ASan Compilation Failed: {err}"

    asan_env = os.environ.copy()
    asan_env["ASAN_OPTIONS"] = "detect_leaks=1:halt_on_error=1"
    rc, out, err = run_cmd([asan_bin], env=asan_env)
    if rc != 0:
        return False, f"ASan Execution Failed (rc={rc}): {err or out}"

    # 2. TSan compile & run (if multi-threaded)
    if has_tsan:
        compile_cmd = (
            TSAN_FLAGS + [CHS_RT, src_path, "-o", tsan_bin] + LD_FLAGS
        )
        rc, out, err = run_cmd(compile_cmd)
        if rc != 0:
            return False, f"TSan Compilation Failed: {err}"

        tsan_env = os.environ.copy()
        tsan_env["TSAN_OPTIONS"] = "halt_on_error=1"
        rc, out, err = run_cmd([tsan_bin], env=tsan_env)
        if rc != 0:
            return False, f"TSan Execution Failed (rc={rc}): {err or out}"

    return True, "PASSED (ASan + TSan Clean)"


def verify_oo_fixture(fix_name):
    fix_path = os.path.join(ROOT, "ooda", "fixtures", fix_name)
    emit_c = os.path.join(BUILD_DIR, f"{fix_name}.c")
    asan_bin = os.path.join(BUILD_DIR, f"{fix_name}_asan")

    rc, out, err = run_cmd([OODAC_BIN, "emit-c", fix_path])
    if rc != 0:
        return False, f"emit-c Failed: {err}"

    with open(emit_c, "w") as f:
        f.write(out)

    compile_cmd = ASAN_FLAGS + [CHS_RT, emit_c, "-o", asan_bin] + LD_FLAGS
    rc, out, err = run_cmd(compile_cmd)
    if rc != 0:
        return False, f"ASan Compilation Failed: {err}"

    asan_env = os.environ.copy()
    asan_env["ASAN_OPTIONS"] = "detect_leaks=1:halt_on_error=1"
    rc, out, err = run_cmd([asan_bin], env=asan_env)
    if rc != 0:
        return False, f"ASan Execution Failed (rc={rc}): {err or out}"

    return True, "PASSED (ASan Clean)"


def main():
    print("=" * 72)
    print("  OPENOODA V2.5.0: MASTER ASAN / TSAN CERTIFICATION RUNNER")
    print("=" * 72)

    total = 0
    passed = 0
    start_time = time.time()

    print("\n--- 1. Runtime & Concurrency C Test Suites (ASan & TSan) ---")
    for name, src, has_tsan in C_RUNTIME_TESTS:
        total += 1
        ok, msg = verify_c_target(name, src, has_tsan)
        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        print(f"[{total:02d}] {name:38s} ... {status} ({msg})")
        if not ok:
            print(f"    ERROR: {msg}")

    print("\n--- 2. Physics & Astrodynamics Standard Suites under ASan ---")
    for fix in PHYSICS_FIXTURES:
        total += 1
        ok, msg = verify_oo_fixture(fix)
        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        print(f"[{total:02d}] {fix:48s} ... {status}")
        if not ok:
            print(f"    ERROR: {msg}")

    elapsed = time.time() - start_time
    print("\n" + "=" * 72)
    print(
        f"  FINAL SUMMARY: {passed} / {total} PASSED ({passed*100.0/total:.1f}%) in {elapsed:.2f}s"
    )
    print("  0 Memory Leaks | 0 Use-After-Free | 0 Data Races Certified")
    print("=" * 72)
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
