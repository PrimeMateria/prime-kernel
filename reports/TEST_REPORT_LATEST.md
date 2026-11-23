# PRIME Kernel Automated Test & Formal Verification Report

- **Execution Timestamp**: 2026-11-23T13:20:15.021351+00:00
- **Overall Verdict**: **ALL GATES PASSED**
- **Total Execution Duration**: `54.64s`
- **Governing Architecture**: ADR-0027 (PRIME Kernel Test Harness & Pre-Commit Gate)

---

## 1. Executive Summary & SLA Invariant Compliance

| Invariant / SLA Metric | Budget Ceiling | Measured Duration | Headroom | Status |
| :--- | :---: | :---: | :---: | :--- |
| **`INV-023-probe` (Axiom Guard & Negative Controls)** | `<= 3.00s` | `1.14s` | `62.1%` | **PASS** |
| **`INV-023d-unit` (Host Literate Foundation)** | `<= 35.00s` | `23.11s` | `34.0%` | **PASS** |
| **`INV-023d-int` (5-Domain Algebraic Ledger)** | `<= 30.00s` | `19.79s` | `34.0%` | **PASS** |
| **`INV-027e` (Pure ASCII Table Formatting)** | `0 non-ASCII` | `0 non-ASCII` | `100.0%` | **PASS** |

---

## 2. Two-Tier Verification Matrix (Pure ASCII)

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

---

## 3. Five-Domain Algebraic Fixtures Ledger

```markdown
| Fixture / Carrier | Target Theorem | Observed Axiom Cone | (a) PA | (b) Clean | TCB Tier | Gate 3 Global Audit | Duration |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- | :---: |
| **Finite Field ZMod 5 (Z/5Z)** | `C1ZMod5.c1_zmod5` | `[]` | **PASS** | **PASS** | Constructive Type Theory | **Gate 3 Certified** | `1.45s` |
| **Symmetric Group S3 (Order 6)** | `C1S3.c1_s3` | `[]` | **PASS** | **PASS** | Constructive Type Theory | **Gate 3 Certified** | `1.66s` |
| **Constructive Rational Prototype (Frac)** | `ConstructiveRat.c1_frac` | `[propext]` | **FAIL** | **PASS** | Constructive + Propext | **gate3_partial (Choice-Free Extension Section 4b)** | `1.60s` |
| **Standard Lean 4 Rat (Init.Data.Rat)** | `c1_elementary_rat` | `[propext, Classical.choice, Quot.sound]` | **FAIL** | **PASS** | Full Classical TCB | **gate3_partial (Declared Classical Extension Section 4b)** | `1.77s` |
| **Literate Dual-Carrier Rational Model (c1-std-rat)** | `C1StdRat.Main (rat_refl, frac_refl)` | `[]` | **PASS** | **PASS** | Dual-Carrier Packaging (Lean 4 + Frac) | **Gate 3 Certified** | `13.31s` |
```

- **Packaging Validation vs. Full Inversion**:
  `c1-std-rat` validates the dual-carrier literate compiler pipeline for both `rat_refl` and `frac_refl` with observed `[]` (Gate 3 Certified). Full additive inversion over canonical `Rat` inherently requires `[propext, Classical.choice, Quot.sound]`, while inversion over constructive `Frac` requires strictly `[propext]`.

---

## 4. Attestation Certificates & Cryptographic Hashes

- **Foundation Attestation ID**: `76d8d49f20155eef26c94b23fd78c8627dfac5f4a6ea11b23e8cc935f445c6c1`
- **Dual-Carrier Fixture Attestation**: `8caad4efa85cf5d6e77b2ef0c2e1b1189cc04e999195772b6bb880f80922bec3`
- **Application Binary (core-wasm@1)**: 1,923 Bytes (SHA-256 Verified)
- **Hologram Application Container**: 15,035 Bytes (6/6 Acceptance Vectors Sub-45us)
