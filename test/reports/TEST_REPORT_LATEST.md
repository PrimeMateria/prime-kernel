# PIRTM Kernel Test Execution & Verification Report

**Status**: ✅ PASSED  
**Execution Timestamp**: `2026-11-23T06:02:25.724621`  
**Target Directory**: [`/run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel/test`](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel/test)  
**Lean Toolchain**: `leanprover/lean4:v4.32.2`  
**LexLean Version**: `0.4.3` (Language: `1.2`)  

---

## 1. Executive Summary

| Metric | Value | Status |
| :--- | :--- | :--- |
| Total Test Suites | 9 | ✅ All Passed |
| Suites Passed | 9 / 9 | ✅ 100% |
| Instrument Sanity Check (`preflight_clean`) | Clean (`[]` axioms) | ✅ PASS |
| Gate 3 Empirical Status | `partially_confirmed (dynamic native_decide tactic axioms identified)` | ✅ Assessed |
| LexLean Modules Verified | 4 | ✅ Full Pipeline Verified |
| Cryptographic Attestation | `76d8d49f20155eef26c94b23fd78c8627dfac5f4a6ea11b23e8cc935f445c6c1` | ✅ Generated |

---

## 2. Test Suites Matrix

| Suite ID | Test Name | Target / Command | Result | Duration |
| :--- | :--- | :--- | :--- | :--- |
| TS-01 | Toolchain Pin & Conformance | `lean --version / lake --version` | ✅ PASS | 0.11s |
| TS-02 | Lake Host Build & Hygiene | `lake build` | ✅ PASS | 0.21s |
| TS-03 | Phase 0 Forbidden-Constant Preflight | `lake env lean Preflight.lean` | ✅ PASS | 2.15s |
| TS-04 | LexLean Lock Parity | `lexlean lock --check` | ✅ PASS | 1.11s |
| TS-05 | LexLean Static IR & Type Check | `lexlean check` | ✅ PASS | 1.17s |
| TS-06 | LexLean Kernel Formal Verification | `lexlean verify` | ✅ PASS | 20.39s |
| TS-07 | Attestation Certificate Audit | `.lexlean/verified inspection` | ✅ PASS | N/A |
| TS-08 | Gate 3 Negative Control (native_decide pattern rejection) | `NegativeControls.lean (matches *.native_decide.ax_*)` | ✅ PASS | 1.40s |
| TS-09 | Gate 3 Negative Control (sorryAx literal rejection) | `NegativeControls.lean (matches sorryAx)` | ✅ PASS | 1.40s |

---

## 3. Phase 0 Empirical Axiom Dependency Ledger

Ledger rows generated directly from empirical `#print axioms` output under Lean `leanprover/lean4:v4.32.2`:

| Probe ID | Theorem | Predicted | Actual Cone (Verbatim) | On Policy List | Unknown | Classification | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `preflight_clean` | `preflight_clean` | `[]` | `[]` | `[]` | `[]` | `present_as_expected` | Instrument sanity check passed (clean) |
| `preflight_propext` | `preflight_propext` | `propext` | `propext` | `propext` | `[]` | `present_as_expected` | Observed exact predicted cone ['propext'] |
| `preflight_quot` | `preflight_quot` | `Quot.sound` | `Quot.sound` | `Quot.sound` | `[]` | `present_as_expected` | Observed exact predicted cone ['Quot.sound'] |
| `preflight_classical` | `preflight_classical` | `Classical.choice` | `Classical.choice` | `Classical.choice` | `[]` | `present_as_expected` | Observed exact predicted cone ['Classical.choice'] |
| `preflight_decide` | `preflight_decide` | `[]` | `[]` | `[]` | `[]` | `absent_as_expected` | Kernel reduction path is completely clean |
| `preflight_native` | `preflight_native` | `Lean.ofReduceBool` | `preflight_native._native.native_decide.ax_1_1` | `[]` | `preflight_native._native.native_decide.ax_1_1` | `present_unexpected` | Refactored native evaluation: dynamic tactic axiom emitted: ['preflight_native._native.native_decide.ax_1_1'] |
| `preflight_trustCompiler` | `preflight_trustCompiler` | `Lean.ofReduceBool` | `preflight_trustCompiler._native.native_decide.ax_1_1` | `[]` | `preflight_trustCompiler._native.native_decide.ax_1_1` | `present_unexpected` | Refactored native evaluation: dynamic tactic axiom emitted: ['preflight_trustCompiler._native.native_decide.ax_1_1'] |
| `preflight_sorry` | `preflight_sorry` | `sorryAx` | `sorryAx` | `sorryAx` | `[]` | `present_as_expected` | Observed exact predicted cone ['sorryAx'] |

### Empirical Findings Summary
```lean
empirical_forbidden_set := ["Classical.choice", "Quot.sound", "propext", "sorryAx"]
unobservable_forbidden_set := ["Lean.ofReduceBool", "Lean.trustCompiler"]
unknown_constants_observed := ["preflight_native._native.native_decide.ax_1_1", "preflight_trustCompiler._native.native_decide.ax_1_1"]
gate3_empirical_list_status := partially_confirmed (dynamic native_decide tactic axioms identified)
```

**Key Architectural Finding**:
- Under Lean 4.32.2, native evaluation (`native_decide`) does not emit the legacy static constant `Lean.ofReduceBool`, but rather generates dynamic tactic axioms (e.g. `preflight_native._native.native_decide.ax_1_1`).
- `Lean.trustCompiler` remains unobservable via `#print axioms` as expected (compiler-trace marker rather than kernel axiom).
- Core mathematical axioms `propext`, `Quot.sound`, and non-constructive choice `Classical.choice` are faithfully captured.
- Proof abandonment `sorryAx` is correctly isolated.

---

## 4. LexLean Formal Verification Pipeline Details

- **Compiler Semantics ID**: `4bd46ef62ba56a77cb3c6453346671a809ccd665fc1f5334e4b1b9dce01f3245`
- **Language Spec**: `1.2`
- **Checked Modules Count**: `4`
- **Verified Modules Count**: `4`
- **Attestation Hash**: `76d8d49f20155eef26c94b23fd78c8627dfac5f4a6ea11b23e8cc935f445c6c1`
- **Verified Content Trees**: `5 cached targets`

---

## 5. Artifacts and Output Files

- **Markdown Report**: [`test_report_20261123T060225.md`](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel/test/reports/test_report_20261123T060225.md)
- **Latest Markdown**: [`test_report_latest.md`](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel/test/reports/test_report_latest.md)
- **JSON Data**: [`test_report_20261123T060225.json`](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel/test/reports/test_report_20261123T060225.json)
- **Latest JSON**: [`test_report_latest.json`](file:///run/media/multiplic/AGI/prismagi/mount/PRIME/prime-kernel/test/reports/test_report_latest.json)