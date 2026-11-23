---
adr_id: "ADR-0027"
title: "PRIME Kernel Production Test Harness, Autonomous Documentation Engine, and Pre-Commit CI/CD Alignment Gate"
status: "Accepted"
date: "2026-11-23"
oscal_component_uuid: "ffff-6666-7777-8888-999999999999"
owners: "Ryan O. van Gelder & PRIME Kernel Core"
tags:
  - "prime-kernel"
  - "lean4"
  - "lexlean"
  - "prismpm"
  - "formal-verification"
  - "automated-documentation"
  - "test-harness"
  - "pre-commit"
  - "ci-cd"
  - "attestation"
  - "gate3"
related:
  - "ADR-0001 (Seneca LexLean Governance Framework)"
  - "ADR-0022 (PIRTM-LexLean Verification Pipeline Integration)"
  - "ADR-0023 (PIRTM Kernel Benchmarking Framework)"
  - "ADR-0025 (LexLean & PrismPM Automated Doc Harness)"
  - "ADR-0026 (Kuramoto Formal Stress-Testing and CI/CD Automation)"
lexlean_invariants:
  - invariant_id: "INV-027a"
    nist_control: "SI-7, SA-11"
    cedar_policy_ref: "policies/cedar/adr_027_kernel_harness.cedar"
    parameters:
      target: "tcb_empirical_axiom_guard"
      empirical_probes: 8
      forbidden_pattern: "*.native_decide.ax_*"
      literal_forbidden: ["sorryAx", "Classical.choice", "Quot.sound", "propext"]
      negative_controls: ["native_decide", "sorryAx"]
      status: "enforced"
  - invariant_id: "INV-027b"
    nist_control: "CA-2, SA-4"
    cedar_policy_ref: "policies/cedar/adr_027_kernel_harness.cedar"
    parameters:
      target: "three_tier_partitioned_sla"
      probe_ceiling_seconds: 3.0
      unit_ceiling_seconds: 12.0
      int_ceiling_seconds: 30.0
      status: "enforced"
  - invariant_id: "INV-027c"
    nist_control: "SA-4, CM-3"
    cedar_policy_ref: "policies/cedar/adr_027_kernel_harness.cedar"
    parameters:
      target: "zero_drift_autonomous_documentation"
      format: ["markdown", "json"]
      retention: "dual_latest_and_timestamped"
      status: "enforced"
  - invariant_id: "INV-027d"
    nist_control: "CM-3, CA-2"
    cedar_policy_ref: "policies/cedar/adr_027_kernel_harness.cedar"
    parameters:
      target: "continuous_verification_pre_commit_and_ci"
      hook_type: "pre-commit"
      auto_stage_reports: true
      github_actions_gate: true
      step_summary_publish: true
      status: "enforced"
  - invariant_id: "INV-027e"
    nist_control: "SA-11, SI-7"
    cedar_policy_ref: "policies/cedar/adr_027_kernel_harness.cedar"
    parameters:
      target: "pure_ascii_table_formatting"
      max_non_ascii_in_tables: 0
      status: "enforced"
---

# ADR-0027: PRIME Kernel Production Test Harness, Autonomous Documentation Engine, and Pre-Commit CI/CD Alignment Gate

## 1. Context & Problem Statement

The **PRIME Kernel Subsystem** serves as the foundational Trusted Computing Base (TCB) for formal verification, mathematical proof stratification, and sandboxed WebAssembly execution across the platform. While the subsystem has achieved empirical refutation of static `Lean.ofReduceBool`, verified all 8 axiom probes, implemented Gate 3 negative controls, resolved Ring Condition 1 (C1) across five algebraic domains, and established language parity (Language 1.2 on `v4.32.2`), it has suffered from several critical operational risks:

1. **Fragmented Test Runners**: Verification logic is distributed across `prime-kernel/test/` (Preflight Guard, 9 suites), `prime-kernel/lean/` (Application Layer & WASM, 6 suites), and downstream domain fixtures (`c1-zmod5`, `c1-s3`, `c1-constructive-rat`, `c1-elementary-rat`, `c1-std-rat`). Lacking a single top-level orchestrator, validating the entire kernel requires executing multiple disconnected scripts.
2. **Documentation Drift Risk**: Manual updates to `README.md` and `Lean Kernel Axioms Analysis.tex` risk falling out of alignment with the live build, toolchain versions, attestation hashes, and SLA timing metrics.
3. **Pre-Commit Verification Gap**: Changes to source files or literate specs can be committed locally without executing full kernel verification, allowing regressions or unproven axioms (`sorryAx`, `*.native_decide.ax_*`) to enter the git tree.
4. **Encoding Vulnerabilities in Reports**: Non-ASCII Unicode characters in Markdown tables (`§`, `₃`, `ℤ`, etc.) trigger terminal mojibake and break automated compliance parsers.

Following the successful patterns established in `mount/SUBSYSTEMS/kuramoto-prism` (ADR-0024, ADR-0025, ADR-0026), there is a mandatory requirement to deploy a unified, production-grade test harness, an autonomous report generator, a local pre-commit hook that auto-stages verified reports, and a GitHub Actions CI pipeline.

---

## 2. Decision Drivers

- **Zero-Drift Pre-Commit Gating**: No commit may land without passing the full multi-tier kernel test harness and auto-staging the newly verified reports.
- **Unified Multi-Tier Orchestration**: A single command (`run_tests.py` / `test.sh`) must execute all kernel verification tiers: Preflight Axiom Guard, Gate 3 Negative Controls, Application Layer WASM vectors, and the Five-Fixture Algebraic Ledger.
- **Autonomous Human-Readable Documentation**: Test execution must autonomously synthesize human-readable Markdown reports (with visual status badges, Two-Tier Verification Matrices, and SLA utilization gauges) alongside machine-readable JSON ledgers.
- **Strict Pure ASCII Formatting**: All generated Markdown tables must maintain strictly 0 non-ASCII characters to guarantee pristine cross-platform terminal and web rendering.
- **Three-Tier SLA Enforcement**: Enforce timing invariants (`INV-023-probe <= 3.0s`, `INV-023d-unit <= 35.0s (nominal <= 15.0s)`, `INV-023d-int <= 30.0s`) with automatic CI failure if ceilings are breached.

---

## 3. Considered Options

- **Option A: Fragmented Manual Scripts**: Maintain separate test scripts in `test/`, `lean/`, and `scratch/` without automated hooks.
  - *Pros*: Zero setup effort.
  - *Cons*: High human error, unverified commits, document drift, lack of unified CI reporting.
- **Option B: Heavyweight External Testing Framework**: Integrate external CI frameworks (e.g., PyTest with extensive plugin ecosystem).
  - *Pros*: Standardized plugin structure.
  - *Cons*: Introduces external dependencies into a zero-dependency kernel environment; difficult to run cleanly inside isolated sandbox boundaries.
- **Option C: Unified Production Harness, Autonomous Doc Engine, and Pre-Commit CI Gate (Selected)**: Deploy a self-contained, standard-library-only Python test orchestrator (`prime-kernel/run_tests.py`), shell runner (`test.sh`), local git hook (`.githooks/pre-commit`), hook installer (`install-hooks.sh`), and GitHub Actions workflow (`.github/workflows/prime-kernel-ci.yml`) modeled after `kuramoto-prism`.
  - *Pros*: Zero external dependencies, 100% deterministic, automated report generation, fail-closed pre-commit gating, automatic `$GITHUB_STEP_SUMMARY` publishing.

---

## 4. Decision Outcome

**Chosen Option**: **Option C**.

We standardize the production test harness architecture across the PRIME Kernel subsystem, establishing complete parity with `kuramoto-prism`.

---

## 5. Architectural Specifications & Verification Topology

The unified test harness executes a 6-stage verification and reporting pipeline:

```
+---------------------------------------------------------------------------------------------------+
|                         PRIME KERNEL PRODUCTION TEST HARNESS PIPELINE                             |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  [Stage 1: Toolchain Hygiene & Pin Verification]                                                  |
|    |-- Lean Toolchain Check (leanprover/lean4:v4.32.2)                                            |
|    |-- LexLean CLI Pin (v0.4.3, Executable SHA-256: f943d51f...)                                  |
|    \-- Language Spec Alignment (Language 1.2, Semantics ID: 4b3ed237...)                          |
|                                                                                                   |
|  [Stage 2: Phase 0 Environmental Preflight & Negative Controls] (INV-023-probe <= 3.0s)            |
|    |-- 8 Empirical Theorem Probes via #print axioms (Preflight.lean)                              |
|    |-- Detection of dynamic tactic pattern: *.native_decide.ax_*                                  |
|    \-- Gate 3 Negative Controls (TS-08 dynamic tactic rejection & TS-09 sorryAx rejection)        |
|                                                                                                   |
|  [Stage 3: Host Literate Foundation Verification] (INV-023d-unit <= 35.0s, nominal <= 15.0s)       |
|    |-- Foundation.Arch, Qual, Sec Literate Models                                                 |
|    \-- Cryptographic Attestation Generation (LexLean IR -> Lean 4 -> leanchecker)                 |
|                                                                                                   |
|  [Stage 4: Application Layer & Hologram WASM Execution]                                           |
|    |-- TextRequest Literate Model (Section 4b Classical Extension)                                |
|    |-- PrismPM no_std WebAssembly Compilation (core-wasm@1)                                       |
|    \-- Acceptance Vector Conformance (6/6 vectors, sub-45us latencies)                            |
|                                                                                                   |
|  [Stage 5: Five-Domain Algebraic Fixtures Ledger] (INV-023d-int <= 30.0s)                         |
|    |-- ZMod 5 (Finite Field, definitional rfl, observed: [])                                      |
|    |-- S3 (Symmetric Group, definitional rfl, observed: [])                                       |
|    |-- Frac Prototype (Unreduced pairs, choice-free, observed: [propext])                         |
|    |-- Canonical Rat (Lean core Init.Data.Rat, classical cone: [propext, Quot, Choice])           |
|    \-- Literate Dual-Carrier Model (c1-std-rat, rat_refl + frac_refl packaging validation)        |
|                                                                                                   |
|  [Stage 6: Autonomous Report Generation & Pre-Commit Sync]                                        |
|    |-- Dual-format output: Markdown (TEST_REPORT_LATEST.md) & JSON (test_report_latest.json)      |
|    |-- Pure ASCII Table Formatting (0 box characters, 0 non-ASCII characters in table lines)      |
|    \-- Pre-Commit Hook: Auto-stage reports into the pending commit (git add reports/*)            |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

---

## 6. Report Generation Schema

Reports are written autonomously to `prime-kernel/reports/`:
- **Timestamped Archival**:
  - `reports/TEST_REPORT_YYYYMMDDTHHMMSS.md`
  - `reports/test_report_YYYYMMDDTHHMMSS.json`
- **Canonical Pointers (Auto-Overwritten / Staged)**:
  - `reports/TEST_REPORT_LATEST.md`
  - `reports/test_report_latest.json`

### Markdown Report Structure
1. **Header Badges**: Toolchain version, Pass/Fail status, Total duration, SLA compliance.
2. **Executive Summary**: High-level verdict, suite counts, total tests executed.
3. **Two-Tier Verification Matrix (Pure ASCII)**: Stratifying PA-encodability, Syntactic Cleanliness, LexLean Audit, and Gate 3 Global Audit.
4. **Three-Tier SLA Performance Gauge**: Measured duration vs. budget ceilings (`probe`, `unit`, `int`).
5. **Axiomatic TCB Ledger**: Empirical probe cones, matched negative controls, and declared Section 4b extensions.
6. **Domain Fixtures Breakdown**: 5 algebraic carriers and their cryptographic attestations.

---

## 7. Pre-Commit & CI/CD Pipeline Architecture

### Local Git Hook (`.githooks/pre-commit`)
1. Executes `python3 run_tests.py` from the root of `prime-kernel`.
2. If any test suite fails or any SLA budget is breached, the script exits with non-zero code, aborting the commit immediately (fail-closed).
3. If all gates pass, it auto-stages the newly generated report files:
   ```bash
   git add reports/TEST_REPORT_LATEST.md reports/test_report_latest.json
   ```
4. Output confirms: `[PRE-COMMIT] All formal gates passed. Reports auto-staged. Commit proceeding.`

### Hook Installer (`install-hooks.sh`)
- Configures local git repository settings:
  ```bash
  git config core.hooksPath .githooks
  chmod +x .githooks/pre-commit
  ```
- Also copies `.githooks/pre-commit` to `.git/hooks/pre-commit` as a fallback.

### GitHub Actions Workflow (`.github/workflows/prime-kernel-ci.yml`)
- Triggered on `push` and `pull_request` to `main`/`master` affecting `prime-kernel/**`.
- Sets up Lean 4.32.2 toolchain and LexLean / PrismPM CLI binaries.
- Executes `python3 run_tests.py`.
- Uploads `reports/` as workflow artifacts.
- Publishes `reports/TEST_REPORT_LATEST.md` directly into `$GITHUB_STEP_SUMMARY`.

---

## 8. Invariant Matrix & Governance Enforcement

| Invariant ID | Target | Gating Mechanism | Remediation on Failure |
| :--- | :--- | :--- | :--- |
| **`INV-027a`** | TCB Axiom Guard | Exact match on primitives, pattern match on `*.native_decide.ax_*`, negative controls TS-08/09 | Reject commit; remove `native_decide` / `sorry` |
| **`INV-027b`** | Three-Tier SLA | Ceiling checks: Probe $\le 3.0\text{s}$, Unit $\le 12.0\text{s}$, Int $\le 30.0\text{s}$ | Abort commit; optimize elaboration or isolate fixture |
| **`INV-027c`** | Living Documentation | Autonomous dual-format generation on every test run | Overwrite `TEST_REPORT_LATEST.md` and `test_report_latest.json` |
| **`INV-027d`** | Pre-Commit / CI | `.githooks/pre-commit` hook and `.github/workflows/prime-kernel-ci.yml` | Fail-closed admission control; block unverified commits |
| **`INV-027e`** | Pure ASCII Tables | Regex validation scanning for characters with `ord(c) > 127` in table lines | Sanitize Unicode symbols to pure ASCII text |
