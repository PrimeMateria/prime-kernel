#!/usr/bin/env python3
"""
PRIME Kernel Lean - Multi-Tier Performance Benchmark Suite & Regression Gate
Orchestrates compiler pipeline measurements, WebAssembly microbenchmarks,
Lean 4 kernel elaboration timing, and automated regression tracking.
"""

import sys
import os
import json
import time
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BENCHMARKS_DIR = PROJECT_ROOT / "benchmarks"
REPORTS_DIR = PROJECT_ROOT / "reports" / "benchmarks"
BASELINE_FILE = BENCHMARKS_DIR / "baselines.json"


def get_process_env():
    env = os.environ.copy()
    local_bin = str(Path.home() / ".local" / "bin")
    cargo_bin = str(Path.home() / ".cargo" / "bin")
    elan_bin = str(Path.home() / ".elan" / "bin")
    current_path = env.get("PATH", "")
    env["PATH"] = f"{local_bin}:{cargo_bin}:{elan_bin}:{current_path}"
    env["RUSTUP_TOOLCHAIN"] = "1.97.1-x86_64-unknown-linux-gnu"
    return env


def compute_sample_stats(samples):
    if not samples:
        return {}
    s = sorted(samples)
    n = len(s)
    total = sum(s)
    mean = total / n
    variance = sum((x - mean) ** 2 for x in s) / n if n > 1 else 0.0
    stddev = variance ** 0.5

    p50 = s[int(n * 0.50)]
    p90 = s[int(n * 0.90)]
    p99 = s[min(int(n * 0.99), n - 1)]

    return {
        "samples": n,
        "min_ms": round(s[0], 2),
        "max_ms": round(s[-1], 2),
        "mean_ms": round(mean, 2),
        "stddev_ms": round(stddev, 2),
        "p50_ms": round(p50, 2),
        "p90_ms": round(p90, 2),
        "p99_ms": round(p99, 2),
    }


def run_benchmark_command(cmd, cwd=PROJECT_ROOT, runs=5, warmup=1):
    env = get_process_env()

    # Warmup
    for _ in range(warmup):
        subprocess.run(
            cmd,
            cwd=str(cwd),
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    samples_ms = []
    for _ in range(runs):
        t0 = time.perf_counter()
        res = subprocess.run(
            cmd,
            cwd=str(cwd),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        t1 = time.perf_counter()
        if res.returncode == 0:
            samples_ms.append((t1 - t0) * 1000.0)

    return compute_sample_stats(samples_ms)


def benchmark_pipelines(quick=False):
    print("-> Benchmarking Pipeline Stages (Tier 1 & Tier 4)...")
    check_runs = 5 if quick else 10
    verify_runs = 2 if quick else 3

    t0_check = time.perf_counter()
    lexlean_check_stats = run_benchmark_command(
        ["lexlean", "check", "--all", "--diagnostic-format", "json"],
        runs=check_runs,
        warmup=1,
    )
    print(f"   [Tier 1] lexlean check: mean = {lexlean_check_stats.get('mean_ms', 0):.1f}ms (p50: {lexlean_check_stats.get('p50_ms', 0):.1f}ms)")

    lexlean_verify_stats = run_benchmark_command(
        ["lexlean", "verify", "--all", "--diagnostic-format", "json"],
        runs=verify_runs,
        warmup=0,
    )
    print(f"   [Tier 1] lexlean verify: mean = {lexlean_verify_stats.get('mean_ms', 0):.1f}ms (p50: {lexlean_verify_stats.get('p50_ms', 0):.1f}ms)")

    prismpm_check_stats = run_benchmark_command(
        ["prismpm", "check", "--json"],
        runs=check_runs,
        warmup=1,
    )
    print(f"   [Tier 1] prismpm check: mean = {prismpm_check_stats.get('mean_ms', 0):.1f}ms (p50: {prismpm_check_stats.get('p50_ms', 0):.1f}ms)")

    lean_kernel_stats = run_benchmark_command(
        ["lake", "env", "lean", "LeanKernelAxiomsHost.lean"],
        runs=check_runs,
        warmup=1,
    )
    print(f"   [Tier 4] Lean Kernel Elaboration: mean = {lean_kernel_stats.get('mean_ms', 0):.1f}ms (p50: {lean_kernel_stats.get('p50_ms', 0):.1f}ms)")

    return {
        "lexlean_check": lexlean_check_stats,
        "lexlean_verify": lexlean_verify_stats,
        "prismpm_check": prismpm_check_stats,
        "lean_kernel_elaboration": lean_kernel_stats,
    }


def benchmark_wasm(iterations=10000, warmup=1000):
    print(f"-> Benchmarking Core Hologram WASM Microbenchmarks (Tier 2: {iterations:,} iterations)...")
    wasm_files = list((PROJECT_ROOT / ".prism" / "build").glob("*/core-wasm/prism_text_request_core_wasm.wasm"))
    if not wasm_files:
        raise FileNotFoundError("prism_text_request_core_wasm.wasm not found under .prism/build/")
    wasm_path = wasm_files[0]
    model_path = wasm_path.parent.parent / "model.prism.json"

    bench_script = BENCHMARKS_DIR / "wasm_bench.mjs"
    res = subprocess.run(
        ["node", str(bench_script), str(wasm_path), str(model_path), str(iterations), str(warmup)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if res.returncode != 0:
        raise RuntimeError(f"WASM benchmark failed: {res.stderr}")

    data = json.loads(res.stdout)
    cold = data.get("cold_instantiation", {})
    print(f"   [Tier 2] Cold Instantiation: mean = {cold.get('mean_us', 0):.1f}us ({cold.get('ops_per_sec', 0):,} ops/sec)")

    for v in data.get("vectors", []):
        st = v["stats"]
        print(f"   [Tier 2] {v['name']}: p50 = {st.get('p50_us', 0):.2f}us, p99 = {st.get('p99_us', 0):.2f}us ({st.get('ops_per_sec', 0):,} ops/sec)")

    return data


def evaluate_regressions(current, baseline, warn_threshold=0.10, fail_threshold=0.25):
    regressions = []
    comparisons = []

    # 1. Compare Pipelines
    curr_pipe = current.get("pipelines", {})
    base_pipe = baseline.get("pipelines", {})
    for key in ["lexlean_check", "lexlean_verify", "prismpm_check", "lean_kernel_elaboration"]:
        if key in curr_pipe and key in base_pipe:
            curr_val = curr_pipe[key].get("p50_ms", 0)
            base_val = base_pipe[key].get("p50_ms", 0)
            if base_val > 0:
                delta_pct = (curr_val - base_val) / base_val
                status = "OK"
                if delta_pct >= fail_threshold:
                    status = "FAIL"
                    regressions.append(f"CRITICAL: {key} p50 regressed by {delta_pct * 100:.1f}% ({base_val}ms -> {curr_val}ms)")
                elif delta_pct >= warn_threshold:
                    status = "WARN"
                    regressions.append(f"WARNING: {key} p50 regressed by {delta_pct * 100:.1f}% ({base_val}ms -> {curr_val}ms)")
                comparisons.append({
                    "metric": f"pipeline.{key}.p50_ms",
                    "baseline": base_val,
                    "current": curr_val,
                    "delta_pct": round(delta_pct * 100, 2),
                    "status": status,
                })

    # 2. Compare WASM Vectors
    curr_vecs = {v["name"]: v["stats"] for v in current.get("wasm", {}).get("vectors", [])}
    base_vecs = {v["name"]: v["stats"] for v in baseline.get("wasm", {}).get("vectors", [])}
    for name, curr_st in curr_vecs.items():
        if name in base_vecs:
            base_st = base_vecs[name]
            curr_p90 = curr_st.get("p90_us", 0)
            base_p90 = base_st.get("p90_us", 0)
            if base_p90 > 0:
                delta_pct = (curr_p90 - base_p90) / base_p90
                status = "OK"
                if delta_pct >= fail_threshold:
                    status = "FAIL"
                    regressions.append(f"CRITICAL: {name} p90 regressed by {delta_pct * 100:.1f}% ({base_p90}us -> {curr_p90}us)")
                elif delta_pct >= warn_threshold:
                    status = "WARN"
                    regressions.append(f"WARNING: {name} p90 regressed by {delta_pct * 100:.1f}% ({base_p90}us -> {curr_p90}us)")
                comparisons.append({
                    "metric": f"wasm.{name}.p90_us",
                    "baseline": base_p90,
                    "current": curr_p90,
                    "delta_pct": round(delta_pct * 100, 2),
                    "status": status,
                })

    return regressions, comparisons


def generate_benchmark_reports(report_data, comparisons=None, regressions=None, is_baseline_update=False):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    ts_slug = report_data["timestamp_utc"].replace(":", "-").replace("T", "_").replace("Z", "")

    # 1. JSON Report
    json_path = REPORTS_DIR / f"benchmark-{ts_slug}.json"
    latest_json_path = REPORTS_DIR / "latest-benchmark-report.json"
    content = json.dumps(report_data, indent=2)
    with open(json_path, "w", encoding="utf-8") as f:
        f.write(content)
    with open(latest_json_path, "w", encoding="utf-8") as f:
        f.write(content)

    # 2. Markdown Report
    md_path = REPORTS_DIR / f"benchmark-{ts_slug}.md"
    latest_md_path = REPORTS_DIR / "latest-benchmark-report.md"

    gate_status = "PASSED"
    if is_baseline_update:
        gate_status = "BASELINE RECORDED / CALIBRATED"
    elif any("CRITICAL" in r for r in (regressions or [])):
        gate_status = "FAILED (CRITICAL REGRESSIONS)"
    elif regressions:
        gate_status = "PASSED (WITH WARNINGS)"

    md = [
        "# PRIME Kernel Lean Benchmark & Performance Report",
        "",
        f"- **Timestamp (UTC)**: `{report_data['timestamp_utc']}`",
        f"- **Target Root**: `{report_data['project_root']}`",
        f"- **Total Benchmark Duration**: `{report_data['total_duration_seconds']:.2f}s`",
        f"- **Regression Gate Status**: **{gate_status}**",
        "",
        "---",
        "",
        "## 1. Toolchain & Compiler Pipeline Benchmarks (Tier 1 & Tier 4)",
        "",
        "| Pipeline Stage | Runs | Mean Latency | Median (p50) | p90 | Min / Max |",
        "| :--- | :---: | :---: | :---: | :---: | :---: |",
    ]

    for k, v in report_data["pipelines"].items():
        md.append(
            f"| `{k}` | {v.get('samples', 0)} | {v.get('mean_ms', 0):.1f}ms | **{v.get('p50_ms', 0):.1f}ms** | {v.get('p90_ms', 0):.1f}ms | {v.get('min_ms', 0):.1f}ms / {v.get('max_ms', 0):.1f}ms |"
        )

    wasm = report_data["wasm"]
    cold = wasm.get("cold_instantiation", {})
    md.extend([
        "",
        "---",
        "",
        "## 2. Core Hologram WebAssembly Runtime Microbenchmarks (Tier 2)",
        "",
        f"- **Iterations Per Vector**: `{wasm.get('iterations', 0):,}`",
        f"- **Warmup Cycles**: `{wasm.get('warmup', 0):,}`",
        f"- **Cold Instantiation**: **{cold.get('p50_us', 0):.2f}µs** median ({cold.get('ops_per_sec', 0):,} instantiations/sec)",
        "",
        "### Request Acceptance Vector Latency & Throughput",
        "",
        "| Vector Name | Req / Res Size | Median (p50) | p90 Latency | p99 Latency | Throughput (ops/s) | Conformance |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |",
    ])

    for v in wasm.get("vectors", []):
        st = v["stats"]
        status = "EXACT" if v.get("verified_exact") else "MISMATCH"
        md.append(
            f"| `{v['name']}` | {v['request_len']}B / {v['response_len']}B | **{st.get('p50_us', 0):.2f}µs** | {st.get('p90_us', 0):.2f}µs | {st.get('p99_us', 0):.2f}µs | {st.get('ops_per_sec', 0):,} req/s | **{status}** |"
        )

    md.extend([
        "",
        "### Memory Allocation Rates (`holo_alloc`)",
        "",
        "| Buffer Size | Median (p50) | Throughput (allocs/sec) |",
        "| :--- | :---: | :---: |",
    ])
    for sz, st in wasm.get("allocation", {}).items():
        md.append(f"| `{sz}` | **{st.get('p50_us', 0):.2f}µs** | {st.get('ops_per_sec', 0):,} ops/s |")

    if comparisons:
        md.extend([
            "",
            "---",
            "",
            "## 3. Regression Analysis vs Baseline",
            "",
            "| Metric | Baseline | Current | Delta (%) | Status |",
            "| :--- | :---: | :---: | :---: | :---: |",
        ])
        for c in comparisons:
            sign = "+" if c["delta_pct"] > 0 else ""
            md.append(
                f"| `{c['metric']}` | {c['baseline']} | {c['current']} | {sign}{c['delta_pct']}% | **{c['status']}** |"
            )

    md_content = "\n".join(md)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    with open(latest_md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    return str(latest_json_path), str(latest_md_path)


def main():
    parser = argparse.ArgumentParser(description="PRIME Kernel Lean Benchmark Runner")
    parser.add_argument("--quick", action="store_true", help="Run fast benchmark smoke pass")
    parser.add_argument("--iterations", type=int, default=10000, help="Iterations for WASM microbenchmarks")
    parser.add_argument("--update-baseline", action="store_true", help="Promote current results to baselines.json")
    parser.add_argument("--check-regression", action="store_true", help="Enforce regression checks against baseline")
    args = parser.parse_args()

    if args.quick:
        args.iterations = 1000

    print("=================================================================")
    print("  PRIME Kernel Lean Performance Benchmark & Regression Harness  ")
    print(f"  Target: {PROJECT_ROOT}")
    print("=================================================================\n")

    t_start = time.perf_counter()
    pipeline_results = benchmark_pipelines(quick=args.quick)
    wasm_results = benchmark_wasm(iterations=args.iterations)
    t_end = time.perf_counter()

    report_data = {
        "project_root": str(PROJECT_ROOT),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "total_duration_seconds": round(t_end - t_start, 2),
        "pipelines": pipeline_results,
        "wasm": wasm_results,
    }

    regressions = []
    comparisons = []
    is_baseline_update = args.update_baseline or not BASELINE_FILE.is_file()

    if BASELINE_FILE.is_file() and not args.update_baseline:
        try:
            with open(BASELINE_FILE, "r", encoding="utf-8") as f:
                baseline = json.load(f)
            regressions, comparisons = evaluate_regressions(report_data, baseline)
        except Exception as e:
            print(f"Warning: Failed to load baseline file {BASELINE_FILE}: {e}")

    if is_baseline_update:
        BENCHMARKS_DIR.mkdir(parents=True, exist_ok=True)
        with open(BASELINE_FILE, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)
        print(f"\n[+] Performance baseline saved to {BASELINE_FILE}")

    json_path, md_path = generate_benchmark_reports(
        report_data,
        comparisons=comparisons,
        regressions=regressions,
        is_baseline_update=is_baseline_update,
    )

    print("\nBenchmark Execution Complete:")
    print(f"  Total Duration: {t_end - t_start:.2f}s")
    print(f"  JSON Report:     {json_path}")
    print(f"  Markdown Report: {md_path}")

    if regressions:
        print("\n[!] Regression Warnings / Failures:")
        for r in regressions:
            print(f"  - {r}")
        if args.check_regression and any("CRITICAL" in r for r in regressions):
            print("\n[-] Gating failure: Performance regressed beyond failure threshold.")
            return 1

    print("\n[✓] All benchmarks passed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
