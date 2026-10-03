#!/usr/bin/env python3
# openOODA E2E Master Test Runner
# This file is an executable Python script when invoked with python3 or directly.
import argparse
import json
import os
import sys
import time
from typing import List

# Ensure parent directory is in sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
POLYROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../.."))
if POLYROOT not in sys.path:
    sys.path.insert(0, POLYROOT)

from openOODA.qa.e2e.framework import TestResult

# Tier 1
from openOODA.qa.e2e.tier1.test_tier1_r1_compiler import (
    test_t1_r1_1_sever_anchor_extra_names,
    test_t1_r1_2_scope_prototype_arity,
    test_t1_r1_3_lexical_scope_scanning,
    test_t1_r1_4_decomposed_matchers,
    test_t1_r1_5_compiler_happy_path,
)
from openOODA.qa.e2e.tier1.test_tier1_r2_density import (
    test_t1_r2_1_mesh_anchor_purged,
    test_t1_r2_2_mega_directory_fixture_separation,
    test_t1_r2_3_directory_density_rule,
    test_t1_r2_4_submodule_anchor_reexport,
    test_t1_r2_5_academy_headers,
)
from openOODA.qa.e2e.tier1.test_tier1_r3_compaction import (
    test_t1_r3_1_sha512_sliding_window,
    test_t1_r3_2_monolithic_fn_length,
    test_t1_r3_3_sha512_nist_empty_string,
    test_t1_r3_4_sha512_nist_abc,
    test_t1_r3_5_sha512_nist_multiblock,
)
from openOODA.qa.e2e.tier1.test_tier1_r4_treerot import (
    test_t1_r4_1_struct_mutability_rule,
    test_t1_r4_2_redundant_builtin_imports,
    test_t1_r4_3_disambiguated_markers,
    test_t1_r4_4_wui_vnode_flat_arena,
    test_t1_r4_5_genomics_float_annotations,
    test_t1_r4_6_mcp_fail_closed_negative_control,
)
from openOODA.qa.e2e.tier1.test_tier1_r5_governance import (
    test_t1_r5_1_check_cache_subsecond_hit,
    test_t1_r5_2_polyrepo_qa_cli_integration,
    test_t1_r5_3_size_linter_execution,
    test_t1_r5_4_resource_scorecard_bounds,
    test_t1_r5_5_root_std_anchor_check,
)

# Tier 2
from openOODA.qa.e2e.tier2.test_tier2_r1_boundary import (
    test_t2_r1_1_zero_vs_one_arity,
    test_t2_r1_2_high_arity_conflict,
    test_t2_r1_3_return_type_conflict,
    test_t2_r1_4_transitive_import_conflict,
    test_t2_r1_5_single_line_minimal_file,
    test_t2_r1_6_empty_file_handling,
)
from openOODA.qa.e2e.tier2.test_tier2_r2_boundary import (
    test_t2_r2_1_density_exact_8_files,
    test_t2_r2_2_density_exact_9_files,
    test_t2_r2_3_density_exact_7_files,
    test_t2_r2_4_deeply_nested_submodules,
    test_t2_r2_5_circular_anchor_imports,
    test_t2_r2_6_empty_anchor_shim,
)
from openOODA.qa.e2e.tier2.test_tier2_r3_boundary import (
    test_t2_r3_1_sha512_1_byte,
    test_t2_r3_2_sha512_55_bytes,
    test_t2_r3_3_sha512_111_bytes,
    test_t2_r3_4_sha512_112_bytes,
    test_t2_r3_5_function_length_boundary,
    test_t2_r3_6_sliding_window_16_vars,
)
from openOODA.qa.e2e.tier2.test_tier2_r4_boundary import (
    test_t2_r4_1_empty_vnode_arena,
    test_t2_r4_2_vnode_leaf_node,
    test_t2_r4_3_deep_linear_arena_tree,
    test_t2_r4_4_wide_arena_tree,
    test_t2_r4_5_invalid_child_id_handling,
    test_t2_r4_6_mcp_empty_secret_fail_closed,
)
from openOODA.qa.e2e.tier2.test_tier2_r5_boundary import (
    test_t2_r5_1_cache_hit_on_timestamp_touch,
    test_t2_r5_2_cache_invalidation_on_comment,
    test_t2_r5_3_missing_cache_dir_recovery,
    test_t2_r5_4_rss_ceiling_boundary,
    test_t2_r5_5_cpu_time_boundary,
    test_t2_r5_6_page_rule_256_line_limit,
)

# Tier 3
from openOODA.qa.e2e.tier3.test_tier3_cross_feature import (
    test_t3_x1_arity_and_cache_invalidation,
    test_t3_x2_submodule_shims_and_anchor_isolation,
    test_t3_x3_compacted_sha512_resource_bounds,
    test_t3_x4_wui_flat_arena_struct_mutation,
    test_t3_x5_mcp_negative_control_double_run,
    test_t3_x6_partitioned_build_bit_identical,
    test_t3_x7_struct_mutation_with_decomposed_helpers,
    test_t3_x8_scope_has_linear_scaling_at_depth_50,
)

# Tier 4
from openOODA.qa.e2e.tier4.test_tier4_app_scenarios import (
    test_t4_app1_cli_application_lifecycle,
    test_t4_app2_deterministic_release_pipeline,
    test_t4_app3_wui_dom_hierarchy_rendering,
    test_t4_app4_crypto_package_manifest_verification,
    test_t4_app5_multimodule_package_verification,
)

ALL_TEST_DISPATCH = [
    # Tier 1
    (1, "R1", "T1.R1.1", test_t1_r1_1_sever_anchor_extra_names),
    (1, "R1", "T1.R1.2", test_t1_r1_2_scope_prototype_arity),
    (1, "R1", "T1.R1.3", test_t1_r1_3_lexical_scope_scanning),
    (1, "R1", "T1.R1.4", test_t1_r1_4_decomposed_matchers),
    (1, "R1", "T1.R1.5", test_t1_r1_5_compiler_happy_path),
    (1, "R2", "T1.R2.1", test_t1_r2_1_mesh_anchor_purged),
    (1, "R2", "T1.R2.2", test_t1_r2_2_mega_directory_fixture_separation),
    (1, "R2", "T1.R2.3", test_t1_r2_3_directory_density_rule),
    (1, "R2", "T1.R2.4", test_t1_r2_4_submodule_anchor_reexport),
    (1, "R2", "T1.R2.5", test_t1_r2_5_academy_headers),
    (1, "R3", "T1.R3.1", test_t1_r3_1_sha512_sliding_window),
    (1, "R3", "T1.R3.2", test_t1_r3_2_monolithic_fn_length),
    (1, "R3", "T1.R3.3", test_t1_r3_3_sha512_nist_empty_string),
    (1, "R3", "T1.R3.4", test_t1_r3_4_sha512_nist_abc),
    (1, "R3", "T1.R3.5", test_t1_r3_5_sha512_nist_multiblock),
    (1, "R4", "T1.R4.1", test_t1_r4_1_struct_mutability_rule),
    (1, "R4", "T1.R4.2", test_t1_r4_2_redundant_builtin_imports),
    (1, "R4", "T1.R4.3", test_t1_r4_3_disambiguated_markers),
    (1, "R4", "T1.R4.4", test_t1_r4_4_wui_vnode_flat_arena),
    (1, "R4", "T1.R4.5", test_t1_r4_5_genomics_float_annotations),
    (1, "R4", "T1.R4.6", test_t1_r4_6_mcp_fail_closed_negative_control),
    (1, "R5", "T1.R5.1", test_t1_r5_1_check_cache_subsecond_hit),
    (1, "R5", "T1.R5.2", test_t1_r5_2_polyrepo_qa_cli_integration),
    (1, "R5", "T1.R5.3", test_t1_r5_3_size_linter_execution),
    (1, "R5", "T1.R5.4", test_t1_r5_4_resource_scorecard_bounds),
    (1, "R5", "T1.R5.5", test_t1_r5_5_root_std_anchor_check),
    # Tier 2
    (2, "R1", "T2.R1.1", test_t2_r1_1_zero_vs_one_arity),
    (2, "R1", "T2.R1.2", test_t2_r1_2_high_arity_conflict),
    (2, "R1", "T2.R1.3", test_t2_r1_3_return_type_conflict),
    (2, "R1", "T2.R1.4", test_t2_r1_4_transitive_import_conflict),
    (2, "R1", "T2.R1.5", test_t2_r1_5_single_line_minimal_file),
    (2, "R1", "T2.R1.6", test_t2_r1_6_empty_file_handling),
    (2, "R2", "T2.R2.1", test_t2_r2_1_density_exact_8_files),
    (2, "R2", "T2.R2.2", test_t2_r2_2_density_exact_9_files),
    (2, "R2", "T2.R2.3", test_t2_r2_3_density_exact_7_files),
    (2, "R2", "T2.R2.4", test_t2_r2_4_deeply_nested_submodules),
    (2, "R2", "T2.R2.5", test_t2_r2_5_circular_anchor_imports),
    (2, "R2", "T2.R2.6", test_t2_r2_6_empty_anchor_shim),
    (2, "R3", "T2.R3.1", test_t2_r3_1_sha512_1_byte),
    (2, "R3", "T2.R3.2", test_t2_r3_2_sha512_55_bytes),
    (2, "R3", "T2.R3.3", test_t2_r3_3_sha512_111_bytes),
    (2, "R3", "T2.R3.4", test_t2_r3_4_sha512_112_bytes),
    (2, "R3", "T2.R3.5", test_t2_r3_5_function_length_boundary),
    (2, "R3", "T2.R3.6", test_t2_r3_6_sliding_window_16_vars),
    (2, "R4", "T2.R4.1", test_t2_r4_1_empty_vnode_arena),
    (2, "R4", "T2.R4.2", test_t2_r4_2_vnode_leaf_node),
    (2, "R4", "T2.R4.3", test_t2_r4_3_deep_linear_arena_tree),
    (2, "R4", "T2.R4.4", test_t2_r4_4_wide_arena_tree),
    (2, "R4", "T2.R4.5", test_t2_r4_5_invalid_child_id_handling),
    (2, "R4", "T2.R4.6", test_t2_r4_6_mcp_empty_secret_fail_closed),
    (2, "R5", "T2.R5.1", test_t2_r5_1_cache_hit_on_timestamp_touch),
    (2, "R5", "T2.R5.2", test_t2_r5_2_cache_invalidation_on_comment),
    (2, "R5", "T2.R5.3", test_t2_r5_3_missing_cache_dir_recovery),
    (2, "R5", "T2.R5.4", test_t2_r5_4_rss_ceiling_boundary),
    (2, "R5", "T2.R5.5", test_t2_r5_5_cpu_time_boundary),
    (2, "R5", "T2.R5.6", test_t2_r5_6_page_rule_256_line_limit),
    # Tier 3
    (3, "R1+R5", "T3.X1", test_t3_x1_arity_and_cache_invalidation),
    (3, "R2+R1", "T3.X2", test_t3_x2_submodule_shims_and_anchor_isolation),
    (3, "R3+R5", "T3.X3", test_t3_x3_compacted_sha512_resource_bounds),
    (3, "R4+R1", "T3.X4", test_t3_x4_wui_flat_arena_struct_mutation),
    (3, "R4+R5", "T3.X5", test_t3_x5_mcp_negative_control_double_run),
    (3, "R2+R5", "T3.X6", test_t3_x6_partitioned_build_bit_identical),
    (3, "R4+R3", "T3.X7", test_t3_x7_struct_mutation_with_decomposed_helpers),
    (3, "R1+R5", "T3.X8", test_t3_x8_scope_has_linear_scaling_at_depth_50),
    # Tier 4
    (4, "APP", "T4.APP1", test_t4_app1_cli_application_lifecycle),
    (4, "APP", "T4.APP2", test_t4_app2_deterministic_release_pipeline),
    (4, "APP", "T4.APP3", test_t4_app3_wui_dom_hierarchy_rendering),
    (4, "APP", "T4.APP4", test_t4_app4_crypto_package_manifest_verification),
    (4, "APP", "T4.APP5", test_t4_app5_multimodule_package_verification),
]


def print_tap(results: List[TestResult]):
    print(f"1..{len(results)}")
    for idx, r in enumerate(results, 1):
        if r.status == "PASS":
            print(f"ok {idx} - {r.test_id} {r.name} ({r.duration_ms:.1f}ms)")
        else:
            print(f"not ok {idx} - {r.test_id} {r.name}: {r.error_msg}")
            if r.diagnostic:
                for line in r.diagnostic.splitlines():
                    print(f"  # {line}")


def print_json(results: List[TestResult], total_time_ms: float):
    payload = {
        "summary": {
            "total": len(results),
            "passed": sum(1 for r in results if r.status == "PASS"),
            "failed": sum(1 for r in results if r.status == "FAIL"),
            "duration_ms": total_time_ms,
        },
        "results": [
            {
                "id": r.test_id,
                "tier": r.tier,
                "domain": r.domain,
                "name": r.name,
                "status": r.status,
                "duration_ms": r.duration_ms,
                "error": r.error_msg,
                "diagnostic": r.diagnostic,
            }
            for r in results
        ],
    }
    print(json.dumps(payload, indent=2))


def print_text(results: List[TestResult], total_time_ms: float, verbose: bool):
    print("================================================================================")
    print("===            openOODA E2E OPAQUE-BOX VERIFICATION SUITE                    ===")
    print("================================================================================")

    current_tier = None
    for r in results:
        if r.tier != current_tier:
            current_tier = r.tier
            tier_names = {
                1: "Tier 1: Feature Coverage (Primary Happy Paths)",
                2: "Tier 2: Boundary & Corner Cases",
                3: "Tier 3: Cross-Feature Combinations (Pairwise)",
                4: "Tier 4: Real-World Application Scenarios",
            }
            print(f"\n--- {tier_names.get(current_tier, f'Tier {current_tier}')} ---")

        status_badge = "\033[92m[PASS]\033[0m" if r.status == "PASS" else "\033[91m[FAIL]\033[0m"
        # Plain fallback if terminal doesn't support ANSI
        if not sys.stdout.isatty():
            status_badge = f"[{r.status}]"

        print(f"  {status_badge} {r.test_id:<10} {r.name:<60} {r.duration_ms:>8.1f}ms")
        if r.status == "FAIL" and (verbose or True):
            print(f"         \033[33mError:\033[0m {r.error_msg}")
            if r.diagnostic and verbose:
                for line in r.diagnostic.splitlines()[:5]:
                    print(f"           \033[90m> {line}\033[0m")

    passed_count = sum(1 for r in results if r.status == "PASS")
    failed_count = sum(1 for r in results if r.status == "FAIL")

    print("\n================================================================================")
    print(f"=== TEST SUITE EXECUTION SUMMARY: {passed_count}/{len(results)} PASSED ({failed_count} FAILED) ===")
    print(f"=== Total Execution Time: {total_time_ms / 1000.0:.2f} seconds ===")
    print("================================================================================")


def main():
    parser = argparse.ArgumentParser(description="openOODA E2E Master Test Runner")
    parser.add_argument("--all", action="store_true", help="Run all 4 tiers")
    parser.add_argument("--tier", type=int, choices=[1, 2, 3, 4], help="Run specific tier")
    parser.add_argument("--domain", type=str, help="Filter by requirement domain (R1, R2, R3, R4, R5, APP)")
    parser.add_argument("--test", type=str, help="Run specific test ID (e.g. T1.R1.1)")
    parser.add_argument("--double-run", action="store_true", help="Enforce double-run determinism law")
    parser.add_argument("--format", choices=["text", "tap", "json"], default="text", help="Output format")
    parser.add_argument("--verbose", action="store_true", help="Verbose failure output")

    args = parser.parse_args()

    # Filter tests
    selected = ALL_TEST_DISPATCH
    if args.tier:
        selected = [t for t in selected if t[0] == args.tier]
    if args.domain:
        selected = [t for t in selected if args.domain.upper() in t[1].upper()]
    if args.test:
        selected = [t for t in selected if t[2] == args.test]

    if not selected:
        print("No tests matched the specified criteria.", file=sys.stderr)
        sys.exit(2)

    results: List[TestResult] = []
    t0 = time.time()

    for tier, domain, test_id, test_fn in selected:
        try:
            res = test_fn(double_run=args.double_run)
        except Exception as exc:
            res = TestResult(
                test_id=test_id,
                tier=tier,
                domain=domain,
                name=f"Exception in {test_id}",
                status="FAIL",
                duration_ms=0.0,
                error_msg=f"Unhandled exception: {exc}",
            )
        results.append(res)

    total_time_ms = (time.time() - t0) * 1000

    if args.format == "tap":
        print_tap(results)
    elif args.format == "json":
        print_json(results, total_time_ms)
    else:
        print_text(results, total_time_ms, args.verbose)

    failed = any(r.status == "FAIL" for r in results)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
