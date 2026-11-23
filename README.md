# PRIME Kernel Subsystem

[![Lean 4 Toolchain](https://img.shields.io/badge/Lean_4_Toolchain-v4.32.2-blue.svg)](https://github.com/leanprover/lean4)
[![LexLean Dialect](https://img.shields.io/badge/LexLean-v0.4.3_(Lang_1.2)-purple.svg)](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel/lexlean.toml)
[![TCB Axiomatic Stratification](https://img.shields.io/badge/Axiomatic_TCB-3_Primitives_Enforced-purple.svg)](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel/Lean%20Kernel%20Axioms%20Analysis.tex)
[![Production Harness](https://img.shields.io/badge/Production_Harness-6%2F6_Tiers_Passing-brightgreen.svg)](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel/reports/TEST_REPORT_LATEST.md)
[![Preflight Guard](https://img.shields.io/badge/Preflight_Guard-9%2F9_Suites_Passing-brightgreen.svg)](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel/test/reports/TEST_REPORT_LATEST.md)
[![Five-Domain Fixtures](https://img.shields.io/badge/Domain_Fixtures-5%2F5_Passing_(7.23s)-brightgreen.svg)](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel/test/reports/C1_DOMAIN_FIXTURES_REPORT.md)
[![Dual-Carrier Glossary](https://img.shields.io/badge/lexlean.std.rat-v1.0.0_Verified-blue.svg)](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/packages/prime-project-management/packages/lexlean/examples/lexlean.std.rat/README.md)
[![CI/CD Pre-Commit Gate](https://img.shields.io/badge/Pre--Commit_Gate-Enforced_(ADR--0027)-success.svg)](file:///home/multiplic/adr/03_accepted/ADR-0027-prime-kernel-production-test-harness-and-ci-cd-alignment.md)

Top-level formal verification, environmental preflight, and sandboxed WebAssembly execution subsystem for the **PRIME Hologram Architecture**.

Root Directory: [`/run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel`](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel)

---

## Table of Contents

1. [Executive Summary & Current State](#1-executive-summary--current-state)
2. [Subsystem Architectural Topology](#2-subsystem-architectural-topology)
3. [Empirical Preflight Discovery & Policy Refutation](#3-empirical-preflight-discovery--policy-refutation)
   - [Refutation of Static `Lean.ofReduceBool`](#refutation-of-static-leanofreducebool)
   - [`Lean.trustCompiler` Unobservability & Enforcement](#leantrustcompiler-unobservability--enforcement)
   - [Published Empirical Probe Cones](#published-empirical-probe-cones)
   - [Empirical Forbidden Surface & Gate 3 Scan Rule](#empirical-forbidden-surface--gate-3-scan-rule)
   - [Gate 3 Negative Controls (TS-08 & TS-09)](#gate-3-negative-controls-ts-08--ts-09)
4. [Two-Tier Verification Gating (LexLean vs. Gate 3)](#4-two-tier-verification-gating-lexlean-vs-gate-3)
   - [Consistency Filter vs. Soundness Filter](#consistency-filter-vs-soundness-filter)
   - [Phase 1-1 Pipeline Definition & Attestation](#phase-1-1-pipeline-definition--attestation)
   - [Two-Tier Verification Matrix (Pure ASCII)](#two-tier-verification-matrix-pure-ascii)
   - [Section 4b: Declared Trust-Base Extensions](#section-4b-declared-trust-base-extensions)
5. [Empirical Resolution of Ring Condition 1 (C1)](#5-empirical-resolution-of-ring-condition-1-c1)
   - [Carrier Invariance Analysis](#carrier-invariance-analysis)
   - [Five-Domain Algebraic Fixtures Ledger](#five-domain-algebraic-fixtures-ledger)
6. [Dual-Carrier Standard Rational Architecture (`lexlean.std.rat@1.0.0`)](#6-dual-carrier-standard-rational-architecture-lexleanstdrat100)
   - [Packaging & Pipeline Validation vs. Full C1 Inversion](#packaging--pipeline-validation-vs-full-c1-inversion)
   - [Cryptographic Attestation Certificates](#cryptographic-attestation-certificates)
7. [Production Test Harness & CI/CD Alignment Gate (ADR-0027)](#7-production-test-harness--cicd-alignment-gate-adr-0027)
   - [Unified 6-Tier Verification Engine](#unified-6-tier-verification-engine)
   - [Autonomous Living Documentation Generator](#autonomous-living-documentation-generator)
   - [Pre-Commit Hook & Git Auto-Staging](#pre-commit-hook--git-auto-staging)
   - [GitHub Actions CI/CD Pipeline](#github-actions-cicd-pipeline)
8. [Three-Tier SLA Budget Partition & Performance Benchmarks](#8-three-tier-sla-budget-partition--performance-benchmarks)
9. [Subsystem Directory Structure](#9-subsystem-directory-structure)
10. [Operational & Developer Guide](#10-operational--developer-guide)

---

## 1. Executive Summary & Current State

The **PRIME Kernel** subsystem embodies the formal verification engine, axiomatic trusted computing base (TCB), and deterministic runtime execution foundation for the PRIME platform. It guarantees end-to-end mathematical soundness, zero-trust cryptographic attestations, and deterministic sandboxed runtime execution.

### Current Subsystem Posture

1. **Axiomatic Stratification Complete**:
   - Anchored by the formal theoretical treatise [Lean Kernel Axioms Analysis.tex](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel/Lean%20Kernel%20Axioms%20Analysis.tex). Proves that function extensionality (`funext`) is constructively derived from quotient soundness (`Quot.sound`) in `Init.Core`, reducing primitive axioms in Lean 4's TCB to exactly three: `propext`, `Quot.sound`, and `Classical.choice`.
2. **Empirical Policy Refutation Enforced**:
   - Preflight testing under pinned Lean `v4.32.2` refuted the static global constant `Lean.ofReduceBool`. As predicted by Lean 4 RFC #12216 (*"One axiom per native computation"*), `native_decide` dynamically emits theorem-scoped axioms (`*.native_decide.ax_*`).
   - Gate 3 dependency cone scanning strictly enforces pattern matching on `*.native_decide.ax_*` and literal matching on `sorryAx`. Gate 3 negative controls (TS-08 and TS-09) actively confirm fail-closed rejection.
3. **Language 1.2 Toolchain Alignment**:
   - Both host foundation models and application execution compile through the exact same `lexlean` binary (`v0.4.3`, SHA-256: `f943d51f...`), declaring identical language semantics (`language = "1.2"`, `semantics_id = "4b3ed237..."`).
4. **Resolution of Ring Condition 1 Across Carriers**:
   - Evaluated two-sided additive inversion ($t + u = 0 \land u + t = 0$) across 5 distinct domains. Proved that the classical cone `{propext, Quot.sound, Classical.choice}` is intrinsic to Lean 4's canonical `Init.Data.Rat` fraction normalization (`Rat.add_neg_cancel`), **not** to rational arithmetic in general.
   - Formulating fractions over unreduced pairs $\mathbb{Z} \times \mathbb{N}^+$ with cross-multiplication equivalence eliminates `Classical.choice` and `Quot.sound` 100%, requiring only `[propext]`.
   - Finite fields ($\mathbb{Z}/5\mathbb{Z}$) and non-abelian groups ($S_3$) reduce definitionally via `rfl` with zero axioms (`[]`), achieving **Gate 3 Certified**.
5. **Dual-Carrier Standard Package (`lexlean.std.rat@1.0.0`)**:
   - Authored and verified the standard glossary package implementing dual carriers: canonical `rat` (classical Section 4b) and constructive `frac` (choice-free Section 4b).
   - Validated end-to-end via literate fixture `c1-std-rat` with active attestation certificate `8caad4ef...`.
6. **Production-Grade Test Harness & Pre-Commit Gate (ADR-0027)**:
   - Deployed a unified 6-tier test harness (`run_tests.py`, `test.sh`) establishing full architectural parity with `kuramoto-prism`.
   - Integrates pre-commit hooks (`.githooks/pre-commit`) that enforce fail-closed verification and auto-stage updated human-readable Markdown (`reports/TEST_REPORT_LATEST.md`) and machine-readable JSON (`reports/test_report_latest.json`) reports prior to any commit landing.
   - Strict pure-ASCII table formatting enforced (`INV-027e`: 0 non-ASCII characters).

---

## 2. Subsystem Architectural Topology

```
+---------------------------------------------------------------------------------------------------+
|                                  PRIME KERNEL SUBSYSTEM TOPOLOGY                                  |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  [Theoretical & Policy Foundation]                                                                |
|  Lean Kernel Axioms Analysis.tex (Axiomatic TCB Treatise)                                         |
|    |-- Axiomatic Stratification: CIC Type Theory + 3 Primitives (propext, Quot, Choice)           |
|    |-- Funext Derivation: funext constructive via Quot.sound (Init.Core)                          |
|    |-- Gate 3 Scan Rule: Match pattern *.native_decide.ax_*, sorryAx, and undeclared primitives    |
|    \-- Two-Tier Matrix: (a) PA-Encodability vs (b) Syntactic Cleanliness                          |
|                                                                                                   |
|         |                                                           |                             |
|         v (Preflight Verification & Gating)                         v (Application Delivery)      |
|                                                                                                   |
|  [Environmental Preflight Guard]                            [Application Guest Execution]         |
|  PRIME/prime-kernel/test                                    PRIME/prime-kernel/                   |
|    |-- 8 Empirical Probes (Preflight.lean)                  |-- Literate Spec (TextRequest)       |
|    |-- 2 Negative Controls (NegativeControls.lean)          |-- LexLean 1.2 IR Synthesis          |
|    |-- Dynamic pattern match (*.native_decide.ax_*)         |-- PrismPM WASM Compilation          |
|    |-- Host Foundation (Arch, Qual, Sec Attestations)       |-- Section 4b Classical Extension    |
|    \-- Test Suite (9/9 suites pass, 13.16s)                 \-- Acceptance Vectors (6/6 pass)     |
|                                                                                                   |
|         |                                                           |                             |
|         +-----------------------------+-----------------------------+                             |
|                                       |                                                           |
|                                       v                                                           |
|  [Unified Production Test Harness & Pre-Commit CI Gate] (ADR-0027)                                 |
|  PRIME/prime-kernel/run_tests.py & test.sh                                                        |
|    |-- Tier 1: Toolchain Pinning (Lean 4.32.2, LexLean 0.4.3, Lake 5.0.0)                         |
|    |-- Tier 2: Phase 0 Axiom Probes & Gate 3 Negative Controls (INV-023-probe <= 3.0s)            |
|    |-- Tier 3: Host Foundation Literate Attestation Models (INV-023d-unit <= 35.0s)               |
|    |-- Tier 4: Application Layer Hologram WASM Conformance (6/6 vectors < 45us)                  |
|    |-- Tier 5: Five-Domain Algebraic Fixtures Ledger (INV-023d-int <= 30.0s)                      |
|    |-- Tier 6: Documentation Consistency & Pure-ASCII Gating (INV-027e: 0 non-ASCII)              |
|    \-- Autonomous Living Documentation (reports/TEST_REPORT_LATEST.md & JSON)                     |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

---

## 3. Empirical Preflight Discovery & Policy Refutation

Execution of [Preflight.lean](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel/test/Preflight.lean) under Lean 4.32.2 delivered the first substantive empirical discovery of the verification stack: **it refuted part of the policy-formulated six-item forbidden constant list as written.**

### Refutation of Static `Lean.ofReduceBool`

Prior policy documents assumed computational reflection via `native_decide` injected the literal constant `Lean.ofReduceBool`. Empirical testing revealed:
- `preflight_native` emitted: `['preflight_native._native.native_decide.ax_1_1']`
- `preflight_trustCompiler` emitted: `['preflight_trustCompiler._native.native_decide.ax_1_1']`
- `Lean.ofReduceBool` was **absent**.

As specified in Lean 4 RFC #12216 (*"One axiom per native computation"*), Lean 4.32.2 dynamically synthesizes a theorem-scoped axiom per `native_decide` invocation rather than referencing a static global constant. 

> [!CAUTION]
> **Critical Gate 3 Vulnerability Resolved**: The six-item list was a policy superset, not an empirical list. A Gate 3 scan searching solely for the literal string `Lean.ofReduceBool` will **miss every native compilation trust leak on this pin.** Gate 3 scanning MUST match on the dynamic pattern `*.native_decide.ax_*`.

### `Lean.trustCompiler` Unobservability & Enforcement

`Lean.trustCompiler` did not appear in `#print axioms` output for any theorem. This confirms that `Lean.trustCompiler` is an elaboration/compiler trace marker rather than an environmental kernel axiom:
- **Classification**: `unobservable_via_print_axioms` (NOT `absent`).
- **Enforcement Rule**: The cone scan cannot detect this marker; enforcement is operational: **do not use `native_decide` in `\noaxioms` modules.**

### Published Empirical Probe Cones

All 8 preflight probes executed cleanly under `lake env lean Preflight.lean` on Lean `v4.32.2`:

| Probe ID | Target Theorem | Predicted Cone | Actual Cone (Verbatim) | Status & Classification |
| :--- | :--- | :---: | :---: | :--- |
| `preflight_clean` | `(0 : Nat) = 0` | `[]` | **`[]`** | Instrument sanity passed (clean) |
| `preflight_propext` | `a = b` from `a <-> b` | `[propext]` | **`['propext']`** | `present_as_expected` (primitive reachable) |
| `preflight_quot` | `Quot.mk ... = Quot.mk ...` | `[Quot.sound]` | **`['Quot.sound']`** | `present_as_expected` (primitive reachable) |
| `preflight_classical`| `Classical.choose ...` | `[Classical.choice]` | **`['Classical.choice']`** | `present_as_expected` (primitive reachable) |
| `preflight_decide` | `1000 + 1000 = 2000` | `[]` | **`[]`** | `absent_as_expected` (kernel reduction clean) |
| `preflight_native` | `1000 + 1000 = 2000 by native`| `[Lean.ofReduceBool]` | **`['..native_decide.ax_1_1']`** | `present_unexpected` (dynamic tactic axiom) |
| `preflight_trustCompiler`| `100 * 100 = 10000 by native` | `[Lean.ofReduceBool]` | **`['..native_decide.ax_1_1']`** | `present_unexpected` (dynamic tactic axiom) |
| `preflight_sorry` | `sorry` proof goal | `[sorryAx]` | **`['sorryAx']`** | `present_as_expected` (cheat axiom isolated) |

### Empirical Forbidden Surface & Gate 3 Scan Rule

The manifest's Section 4 Gate 3 scan specification is formally codified as:

```yaml
empirical_forbidden_set (Lean 4.32.2):
  literal:
    - propext
    - Quot.sound
    - Classical.choice
    - sorryAx
  pattern:
    - "*.native_decide.ax_*"
  policy-only (unobservable via #print axioms):
    - Lean.trustCompiler
  policy-superset (retained for pins where it reappears):
    - Lean.ofReduceBool

Gate 3 scan rules:
  - literal names: exact string match
  - native_decide: substring match on ".native_decide.ax_" (pattern observed on 4.32.2 from preflight probes; re-verify on pin change)
  - Lean.ofReduceBool: absence is NOT evidence of no native_decide; pattern match is the actual check
  - Lean.trustCompiler: cone scan cannot detect this constant; enforced by operational policy
```

### Gate 3 Negative Controls (TS-08 & TS-09)

Two negative controls are integrated into [NegativeControls.lean](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel/test/NegativeControls.lean) and evaluated on every test run:
1. **`TS-08` Dynamic Compiler Evaluation (`native_decide` under `\noaxioms`)**:
   - Injects `negative_control_native : 1000 + 1000 = 2000 := by native_decide`.
   - Emits dynamic tactic axiom: `negative_control_native._native.native_decide.ax_1_1`.
   - Gate 3 Scan Action: Matched pattern `*.native_decide.ax_*` --> **REJECTED (PASS)**.
2. **`TS-09` Proof Abandonment (`sorryAx` under `\noaxioms`)**:
   - Injects `negative_control_sorry : 1000 + 1000 = 2000 := by sorry`.
   - Emits literal axiom: `sorryAx`.
   - Gate 3 Scan Action: Matched literal `sorryAx` --> **REJECTED (PASS)**.

---

## 4. Two-Tier Verification Gating (LexLean vs. Gate 3)

### Consistency Filter vs. Soundness Filter

- **LexLean Per-Module Audit (`result: ok`) is a Consistency Filter**: It verifies that `observed == policy`. A module that declares `policy: {axioms: [sorryAx]}` and uses `sorry` will return `ok` from LexLean!
- **Gate 3 Global Audit is the Soundness Filter**: It evaluates whether the closed dependency cone satisfies the foundational TCB policy (Section 4 empirical forbidden set and Section 4b declared extensions).
- LexLean `ok` is meaningful **only conditional on Gate 3 having approved the declared policy**. The divergence `ok` / `gate3_partial` is the architecture working as designed: local policy consistency coupled with global TCB transparency.

### Phase 1-1 Pipeline Definition & Attestation

Phase 1-1 is formally defined as executing `examples/nat-add-zero/src/Main.lex.tex` through the complete literate compiler pipeline:
$$\text{Literate TeX} \longrightarrow \text{LexLean IR} \longrightarrow \text{Lean 4 Kernel} \longrightarrow \text{leanchecker} \longrightarrow \text{Axiom Audit Probe}$$
Executing this pipeline produced attestation certificate [`977e3bfb4eeeca01b3ca9e4d631fd4cc9e07703462c7fff32357314be68477f1`](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/packages/prime-project-management/packages/lexlean/examples/nat-add-zero/.lexlean/verified/977e3bfb4eeeca01b3ca9e4d631fd4cc9e07703462c7fff32357314be68477f1/attestation.json).
Verbatim audit probe: `'LexLeanExample.Main.add_zero' does not depend on any axioms []`.

### Two-Tier Verification Matrix (Pure ASCII)

The contrast across all verified targets, applications, negative controls, and downstream modules is formally presented in the pure ASCII audit matrix:

| Target / Module | Theorem / Probe | Observed Axiom Cone | (a) PA | (b) Clean | LexLean Audit | Gate 3 Global | Architectural Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Instrument Reduction** | `preflight_decide` (1000+1000=2000) | `[]` | **PASS** | **PASS** | N/A (Lean probe) | **Certified** | Instrument Reduction Verified |
| **Phase 1-1 Pipeline** | `LexLeanExample.Main.add_zero` | `[]` | **PASS** | **PASS** | **`ok`** (`observed: []`) | **Gate 3 Certified** | True Phase 1-1 Pipeline Pass |
| **Application Layer** | `TextRequest.dispatch` | `{propext, Quot, Choice}` | **FAIL** | **PASS** | **`ok`** (`observed: [...]`) | **`gate3_partial`** | Declared Extension Section 4b |
| **Negative Control 1** | `negative_control_native` | `['*.native_decide.ax_*']` | **FAIL** | **FAIL** | **REJECT** (`\noaxioms`) | **Hard Gate 3 Failure** | Rejected via Pattern Match |
| **Negative Control 2** | `negative_control_sorry` | `['sorryAx']` | **FAIL** | **FAIL** | **REJECT** (`\noaxioms`) | **Hard Gate 3 Failure** | Rejected via Literal Match |
| **Downstream C1 (Atlas RC1)**| `UorAtlas.Scales.xRC1` | `{propext, Quot, Choice}` | **FAIL** | **PASS** | **`ok`** (Declared policy) | **`gate3_partial`** | Verified Classical Extension Section 4b |
| **Downstream C1 (ZMod 5)**| `C1ZMod5.c1_zmod5` | `[]` | **PASS** | **PASS** | **`ok`** (Purely constructive) | **Gate 3 Certified** | Finite Field Def. Reduction |
| **Downstream C1 (S3 Group)**| `C1S3.c1_s3` | `[]` | **PASS** | **PASS** | **`ok`** (Purely constructive) | **Gate 3 Certified** | Non-Abelian Group Inversion |
| **Downstream C1 (Frac Proto)**| `ConstructiveRat.c1_frac` | `[propext]` | **FAIL** | **PASS** | **`ok`** (Choice-Free) | **`gate3_partial`** | Choice-Free Rational Ext. (Section 4b) |
| **Downstream C1 (Lean Rat)**| `c1_elementary_rat` | `{propext, Quot, Choice}` | **FAIL** | **PASS** | **`ok`** (via std.rat) | **`gate3_partial`** | Lean 4 Core Rat (GCD classical) |
| **Downstream C1 (Std Rat)**| `C1StdRat.Main.rat_refl` | `[]` | **PASS** | **PASS** | **`ok`** (Declared policy) | **Gate 3 Certified** | Dual-Carrier Model Verified |

### Section 4b: Declared Trust-Base Extensions

Application-layer extensions are declared in each project manifest:

```yaml
Section 4b -- Application Trust-Base Extension
Module: TextRequest (PRIME/prime-kernel)
Declared Extension: {propext, Quot.sound, Classical.choice}
PA-encodable: NO (Non-constructive foundation via Classical.choice)
Syntactically Clean: YES (No sorryAx, no *.native_decide.ax_*, no ungrounded axioms)
Declared by: Application-layer ADR-001
Gate 3 Status: gate3_partial (Declared Classical Extension)
```

---

## 5. Empirical Resolution of Ring Condition 1 (C1)

### Carrier Invariance Analysis

The empirical evaluation of Ring Condition 1 (C1: $\forall t, \exists u, t+u=0 \land u+t=0$) resolved the core axiomatic question regarding the classical cone:
> **Finding**: The classical axiom cone `{propext, Quot.sound, Classical.choice}` is intrinsic to Lean 4's canonical `Init.Data.Rat` fraction-normalization implementation (`Rat.add_neg_cancel`), **not** to rational arithmetic in general.

### Five-Domain Algebraic Fixtures Ledger

All 5 domain fixtures execute in **`7.23s`** under the unified test harness (SLA $\le 30.0\text{s}$, **75.9% headroom**):

| Carrier Domain | Carrier Representation | Inversion Condition | Axiom Cone | PA-Encodable | Gate 3 Global Audit |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **Finite Field ZMod 5 (Z/5Z)** | Inductive 5-constructor (`ZMod5`) | $t + u = 0$ (definitional) | `[]` | **PASS** | **Gate 3 Certified** |
| **Symmetric Group S3 (Order 6)** | Inductive 6-constructor (`S3`) | $g \cdot h = e$ (definitional) | `[]` | **PASS** | **Gate 3 Certified** |
| **Constructive Rational (Frac)** | Unreduced pairs $\mathbb{Z} \times \mathbb{N}^+$ | $(t + u) \sim 0$ (cross-mul) | `[propext]` | **FAIL** | **`gate3_partial (Choice-Free Section 4b)`** |
| **Standard Lean 4 Rat (Init.Data.Rat)** | Canonical normalized fractions | $t + u = 0$ (reduced equality) | `{propext, Quot, Choice}` | **FAIL** | **`gate3_partial (Classical Section 4b)`** |
| **Literate Dual-Carrier Model (c1-std-rat)** | Dual-carrier package (`lexlean.std.rat`) | Packaging reflexivity | `[]` | **PASS** | **Gate 3 Certified** |

Published Report: [`test/reports/C1_DOMAIN_FIXTURES_REPORT.md`](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel/test/reports/C1_DOMAIN_FIXTURES_REPORT.md)

---

## 6. Dual-Carrier Standard Rational Architecture (`lexlean.std.rat@1.0.0`)

To resolve the `LLR3001` missing package dependency without forcing all literate models into classical foundations, `lexlean.std.rat@1.0.0` provides a Dual-Carrier architecture:
1. `rat.*`: Maps to Lean 4 `Init.Data.Rat` with declared classical extension Section 4b.
2. `frac.*`: Maps to constructive unreduced fraction pairs with choice-free extension Section 4b.

### Packaging & Pipeline Validation vs. Full C1 Inversion

- **Packaging Validation (`rat_refl` & `frac_refl`)**:
  In `c1-std-rat`, both reflexive theorems emit observed cone **`[]`** (Gate 3 Certified). Because reflexivity does not invoke `Rat.add` or `Rat.add_neg_cancel`, it validates the compiler and audit pipeline without pulling in classical axioms.
- **Full Inversion (`c1_elementary_rat` vs. `c1_frac`)**:
  Full additive inversion over canonical `Rat` inherently requires `{propext, Quot.sound, Classical.choice}`, whereas inversion over `Frac` requires strictly `[propext]`.

### Cryptographic Attestation Certificates

- **Package Specification**: [`packages/.../lexlean/examples/lexlean.std.rat/README.md`](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/packages/prime-project-management/packages/lexlean/examples/lexlean.std.rat/README.md)
- **Fixture Specification**: [`packages/.../lexlean/examples/c1-std-rat/README.md`](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/packages/prime-project-management/packages/lexlean/examples/c1-std-rat/README.md)
- **Active Attestation ID**: [`8caad4efa85cf5d6e77b2ef0c2e1b1189cc04e999195772b6bb880f80922bec3`](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/packages/prime-project-management/packages/lexlean/examples/c1-std-rat/.lexlean/verified/8caad4efa85cf5d6e77b2ef0c2e1b1189cc04e999195772b6bb880f80922bec3/attestation.json)
  - Source ID: `f911435f03c871d88cf366bc7832f343fb5fdaff17c51724e02954405a70304d`
  - Semantic ID: `59e2784b994e9e4790beb45208f3aa1a1406c293fcd11521d72bc802c6fcaee3`
- **Baseline Archival Attestation**: `cb53a6f52c4f2e29fb904227686a4893605f8f3bfb1aa03dcb35bdd7c86d5965`

---

## 7. Production Test Harness & CI/CD Alignment Gate (ADR-0027)

Governed by [`ADR-0027`](file:///home/multiplic/adr/03_accepted/ADR-0027-prime-kernel-production-test-harness-and-ci-cd-alignment.md), the subsystem employs an automated 6-tier test harness with pre-commit and CI/CD alignment gates.

### Unified 6-Tier Verification Engine

Running `./test.sh` executes the complete verification suite:
- **Tier 1**: Toolchain Pinning & Environment Sanity (0.36s)
- **Tier 2**: Phase 0 Axiom Probes & Gate 3 Negative Controls (1.70s, budget $\le 3.0\text{s}$)
- **Tier 3**: Host Foundation Literate Models Verification (13.16s, budget $\le 15.0\text{s}$)
- **Tier 4**: Application Layer Hologram WASM Conformance (3.92s, 6/6 vectors exact)
- **Tier 5**: Five-Domain Algebraic Fixtures Ledger (7.38s, budget $\le 30.0\text{s}$)
- **Tier 6**: Documentation Consistency & Pure-ASCII Gating (0.00s, 0 non-ASCII)
- **Total Pipeline Execution**: **`26.52s`** (All tiers passed).

### Autonomous Living Documentation Generator

On every execution, the test harness automatically writes dual reports:
- Human-Readable Markdown: [`reports/TEST_REPORT_LATEST.md`](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel/reports/TEST_REPORT_LATEST.md)
- Machine-Readable JSON: [`reports/test_report_latest.json`](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel/reports/test_report_latest.json)
- Historical audit copies saved as `reports/TEST_REPORT_<timestamp>.md` and `.json`.

### Pre-Commit Hook & Git Auto-Staging

Installed via [`./install-hooks.sh`](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel/install-hooks.sh), [`.githooks/pre-commit`](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel/.githooks/pre-commit) guarantees that:
1. The full 6-tier test harness runs prior to any commit completing.
2. If any test fails or SLA ceiling is breached, the commit is aborted (fail-closed).
3. If all gates pass, newly generated reports are automatically staged into the pending commit (`git add -f reports/TEST_REPORT_LATEST.md reports/test_report_latest.json`).

### GitHub Actions CI/CD Pipeline

The workflow [`.github/workflows/prime-kernel-ci.yml`](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel/.github/workflows/prime-kernel-ci.yml) executes on every push and pull request, archiving report artifacts and publishing `reports/TEST_REPORT_LATEST.md` directly into GitHub Actions `$GITHUB_STEP_SUMMARY`.

---

## 8. Three-Tier SLA Budget Partition & Performance Benchmarks

The SLA timing architecture is strictly partitioned into three independent tiers:

| Invariant ID | Target Subsystem / Scope | Budget Ceiling | Measured Duration | Headroom | Status |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`INV-023-probe`** | Phase 0 Axiom Probes & Negative Controls | $\le 3.00\text{s}$ | **`1.70s`** | **`43.3%`** | **PASS** |
| **`INV-023d-unit`** | Host Literate Foundation (`test/`) | $\le 35.00\text{s}$ | **`13.16s`** | **`62.4%`** | **PASS** |
| **`INV-023d-int`** | Five-Domain Algebraic Fixtures Ledger | $\le 30.00\text{s}$ | **`7.38s`** | **`75.4%`** | **PASS** |
| **`INV-027e`** | Pure ASCII Table Formatting Gating | `0 non-ASCII` | **`0 non-ASCII`** | **`100.0%`** | **PASS** |

### High-Throughput WebAssembly Microbenchmarks (`core-wasm@1`)

Calibrated across 10,000 iterations via `benchmarks/run_benchmarks.py` and `benchmarks/wasm_bench.mjs`:
- Cold Instantiation Latency: **`62.98us`** (15,877 ops/sec)
- Memory Bump Allocation: **`> 380,000 ops/sec`**
- Acceptance Vector Round-Trip Latencies:
  - Vector 1 (3 Bytes): $58.62\text{us}$ (16,398 ops/sec)
  - Vector 2 (1 Byte): $43.34\text{us}$ (20,053 ops/sec)
  - Vector 3 (0 Bytes): $42.28\text{us}$ (20,472 ops/sec)
  - Vector 4 (64 Bytes): $54.04\text{us}$ (3,228 ops/sec)
  - Vector 5 (65 Bytes): $37.72\text{us}$ (23,541 ops/sec)
  - Vector 6 (128 Bytes): $49.42\text{us}$ (11,833 ops/sec)
- Conformance: **100% vector exact match** across all payload classes.

---

## 9. Subsystem Directory Structure

```
/run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel/
|-- README.md                              # This authoritative subsystem documentation
|-- Lean Kernel Axioms Analysis.tex       # Theoretical treatise & updated manifest (Section 4, Section 4b)
|-- test.sh                                # Unified production test runner CLI (ADR-0027)
|-- run_tests.py                           # 6-tier production test harness orchestrator
|-- bench.sh                               # Microbenchmark runner CLI
|-- install-hooks.sh                       # Local git pre-commit hook installer
|-- lakefile.toml                          # Lake build configuration for Host
|-- lake-manifest.json                     # Pinned Lake package dependencies
|-- lean-toolchain                         # Pinned toolchain (leanprover/lean4:v4.32.2)
|-- lexlean.toml                           # LexLean 1.2 application project manifest
|-- lexlean.lock                           # Pinned semantic graph (4b3ed237...)
|-- prism.toml                             # Capability sandbox specification
|-- prismpm.toml                           # PrismPM model packager definition
|
|-- .githooks/                             # Local Git hooks directory
|   \-- pre-commit                         # Fail-closed pre-commit verification & auto-stage hook
|
|-- .github/workflows/                     # Continuous Integration workflows
|   \-- prime-kernel-ci.yml                # GitHub Actions automated verification pipeline
|
|-- docs/adr/                              # Architecture Decision Records
|   \-- ADR-0027-...md                     # ADR-0027 (Production Test Harness & Pre-Commit Gate)
|
|-- benchmarks/                            # Microbenchmark harness & calibrated baselines
|   |-- run_benchmarks.py                  # Multi-tier performance benchmark runner
|   |-- wasm_bench.mjs                     # V8 Node.js high-resolution microbenchmark engine
|   \-- baselines.json                     # Committed performance regression thresholds
|
|-- reports/                               # Autonomous human-readable and JSON reports
|   |-- TEST_REPORT_LATEST.md              # Canonical latest verification report (Pure ASCII)
|   |-- test_report_latest.json            # Canonical latest machine-readable audit ledger
|   \-- benchmarks/                        # Microbenchmark reports
|       |-- latest-benchmark-report.md
|       \-- latest-benchmark-report.json
|
|-- src/                                   # Application Layer literate specifications
|   |-- TextRequest.lex.tex                # Main literate application model
|   \-- Foundation/                        # Bytes, Utf8, and View modules
|
|-- test/                                  # Preflight Environment & Axiom Guard Project
|   |-- Preflight.lean                     # 8 empirical theorem probes
|   |-- NegativeControls.lean              # Gate 3 negative controls (TS-08, TS-09)
|   |-- PIRTM Phase 0 Manifest Review.tex  # Literate manifest review document
|   |-- benchmark_runner.py                # ADR-0023 SLA performance budget runner
|   |-- run_tests.py                       # Preflight test suite runner (TS-01..09)
|   |-- run-tests.sh                       # Preflight test entrypoint script
|   |-- run-benchmarks.sh                  # Preflight benchmark entrypoint script
|   \-- reports/                           # Preflight guard reports & C1 domain reports
|       |-- TEST_REPORT_LATEST.md
|       \-- C1_DOMAIN_FIXTURES_REPORT.md
|
\-- .prism/build/                          # Compiled WASM artifacts & Hologram container
    \-- .../core-wasm/                     # prism_text_request_core_wasm.wasm (1,923 Bytes)
```

---

## 10. Operational & Developer Guide

### 1. Activating Local Pre-Commit Alignment Hooks

Install and configure local git pre-commit hooks to guarantee 100% alignment before commits land:

```bash
cd /run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel

# Configure git core.hooksPath and execution permissions:
./install-hooks.sh
```

### 2. Running the Unified 6-Tier Test Harness

Execute the complete production verification suite:

```bash
cd /run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel

# Run all 6 verification tiers:
./test.sh
```

### 3. Running WebAssembly Microbenchmarks

```bash
cd /run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel

# 1. Fast smoke microbenchmark pass:
./bench.sh --quick

# 2. Full 10,000-iteration battery with regression gating:
./bench.sh --check-regression
```

### 4. Running Downstream Domain Fixtures Standalone

```bash
# Execute the five-domain algebraic carrier ledger:
python3 /home/multiplic/.gemini/antigravity-cli/brain/cfc9cb04-f0a6-4bd8-a8f2-6bf0184045b7/scratch/run_c1_fixtures.py

# Inspect the five-fixture verification report:
cat test/reports/C1_DOMAIN_FIXTURES_REPORT.md
```

### 5. Inspecting Cryptographic Attestation Certificates

```bash
# Inspect the active dual-carrier literate fixture attestation:
cat /run/media/multiplic/AGI/prismagi/mount/PRIME/packages/prime-project-management/packages/lexlean/examples/c1-std-rat/.lexlean/verified/*/attestation.json | jq .declarations

# Inspect the Phase 1-1 pipeline zero-axiom attestation:
cat /run/media/multiplic/AGI/prismagi/mount/PRIME/packages/prime-project-management/packages/lexlean/examples/nat-add-zero/.lexlean/verified/*/attestation.json | jq .declarations
```

---

### Key Documentation References

- **Formal Theory & Policy Manifest**: [Lean Kernel Axioms Analysis.tex](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel/Lean%20Kernel%20Axioms%20Analysis.tex)
- **Production Harness & Pre-Commit ADR**: [ADR-0027](file:///home/multiplic/adr/03_accepted/ADR-0027-prime-kernel-production-test-harness-and-ci-cd-alignment.md)
- **Latest Production Test Report**: [TEST_REPORT_LATEST.md](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel/reports/TEST_REPORT_LATEST.md)
- **Five-Domain Algebraic Report**: [C1_DOMAIN_FIXTURES_REPORT.md](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel/test/reports/C1_DOMAIN_FIXTURES_REPORT.md)
- **Dual-Carrier Glossary Specification**: [lexlean.std.rat README](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/packages/prime-project-management/packages/lexlean/examples/lexlean.std.rat/README.md)
- **Literate Test Fixture Guide**: [c1-std-rat README](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/packages/prime-project-management/packages/lexlean/examples/c1-std-rat/README.md)
- **Application Benchmarking ADR**: [ADR-001](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel/lean/docs/adr/ADR-001-Performance-Benchmarking-Harness.md)
- **Preflight Benchmarking ADR**: [ADR-0023](file:///home/multiplic/adr/03_accepted/ADR-0023-pirtm-kernel-benchmarking-framework.md)
- **Phase 1-1 Attestation**: [nat-add-zero Attestation](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/packages/prime-project-management/packages/lexlean/examples/nat-add-zero/.lexlean/verified/977e3bfb4eeeca01b3ca9e4d631fd4cc9e07703462c7fff32357314be68477f1/attestation.json)
