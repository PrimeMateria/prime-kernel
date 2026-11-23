# ADR-0023 PIRTM Kernel Verification Benchmark Report

**Status**: ✅ ALL SLA BUDGETS PASSED  
**Execution Timestamp**: `2026-11-22T18:16:48.895155`  
**Target Directory**: [`/run/media/multiplic/AGI/prismagi/mount/PRIME/kernel/test`](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/kernel/test)  
**Governing ADR**: [`ADR-0023`](file:///home/multiplic/adr/03_accepted/ADR-0023-pirtm-kernel-benchmarking-framework.md) | **Plan**: [`PLAN-ADR-0023`](file:///home/multiplic/adr/01_planning/PLAN-ADR-0023.md)  
**Iterations Sampled**: `3`  
**Attestation Digest**: `98e3d246b595fcbb98dceebce384283c3501173a6154a4966a9f55ee7d398190`  

---

## 1. Invariant Performance Budget Evaluation (SLAs)

| Invariant ID | Target Benchmark | Metric | Budget SLA | Measured (Mean/Val) | Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **INV-023a** | Lake Host Build (Clean) | Latency / Ratio | `<= 5.0s` | `0.361s` | ✅ PASS |
| **INV-023a** | Lake Host Build (Incremental) | Latency / Ratio | `<= 0.5s` | `0.160s` | ✅ PASS |
| **INV-023a** | Lake Incremental Speedup Factor | Latency / Ratio | `>= 1.5x` | `2.260x` | ✅ PASS |
| **INV-023b** | Phase 0 Axiom Cone Traversal (8 Probes) | Latency / Ratio | `<= 1.0s` | `0.321s` | ✅ PASS |
| **INV-023c** | LexLean Static IR & Type Check | Latency / Ratio | `<= 2.0s` | `0.721s` | ✅ PASS |
| **INV-023d** | LexLean Kernel Verification (Zero-Trust) | Latency / Ratio | `<= 15.0s` | `9.082s` | ✅ PASS |
| **INV-023e** | Attestation Hash Drift | Latency / Ratio | `<= 0drift` | `0 drift` | ✅ PASS |

---

## 2. Statistical Distribution Matrix

| Operation | Mean | Median | Min | Max | P95 | StdDev | Samples |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Lake Build (Cold Clean) | `0.361s` | `0.358s` | `0.356s` | `0.368s` | `0.368s` | `0.005s` | `[0.3561, 0.3584, 0.3676]` |
| Lake Build (Warm Incremental) | `0.160s` | `0.158s` | `0.156s` | `0.165s` | `0.165s` | `0.004s` | `[0.1558, 0.1579, 0.165]` |
| Phase 0 Axiom Cone Preflight | `0.321s` | `0.314s` | `0.310s` | `0.337s` | `0.337s` | `0.012s` | `[0.3105, 0.3136, 0.3372]` |
| LexLean Static Check (`check`) | `0.721s` | `0.725s` | `0.681s` | `0.757s` | `0.757s` | `0.031s` | `[0.6812, 0.7251, 0.7569]` |
| LexLean Kernel Verification (`verify`) | `9.082s` | `9.444s` | `8.184s` | `9.617s` | `9.617s` | `0.639s` | `[8.1842, 9.4441, 9.6172]` |

---

## 3. Acceleration & Determinism Analysis

- **Lake Incremental Elaboration Speedup**: `2.26x` (Clean: `0.361s` vs Incremental: `0.160s`).
- **LexLean Zero-Trust Proof Throughput**: `9.082s` across 4 formal models (`Foundation.Arch`, `Qual`, `Sec`, `Main`), running non-shortcutted Lean kernel type checking on every pass.
- **Attestation Hash Stability**: Zero drift observed across all runs (`98e3d246b595fcbb98dceebce384283c3501173a6154a4966a9f55ee7d398190`).
- **Compliance Controls Satisfied**: NIST SP 800-53 Rev. 5 `CA-2`, `CA-7`, `SA-11`, `SI-7`, `AU-10`.

---

## 4. Benchmark Artifacts

- **Markdown Report**: [`BENCHMARK_REPORT_20261122T181648.md`](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/kernel/test/reports/BENCHMARK_REPORT_20261122T181648.md)
- **Latest Markdown**: [`BENCHMARK_REPORT_LATEST.md`](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/kernel/test/reports/BENCHMARK_REPORT_LATEST.md)
- **JSON Metrics**: [`benchmark_report_20261122T181648.json`](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/kernel/test/reports/benchmark_report_20261122T181648.json)
- **Latest JSON**: [`benchmark_report_latest.json`](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/kernel/test/reports/benchmark_report_latest.json)