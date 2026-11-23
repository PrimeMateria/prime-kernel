# C1 Downstream Domain Fixtures Verification & SLA Benchmark Report

- **Execution Timestamp**: 2026-11-23T12:02:51Z
- **SLA Invariant**: `INV-023d-int` (Multi-Domain Integration Fixtures $\le 30.0\text{s}$)
- **Total Integration Duration**: `6.61s` (Utilization: 22.0%, Headroom: 78.0%)
- **SLA Status**: **PASS**
- **Fixtures Evaluated**: 5 distinct mathematical domains & literate packages

---

## 1. Executive Summary & Verification Matrix

This suite provides the empirical resolution of Ring Condition 1 (C1: additive inverse $\forall t, \exists u, t+u=0 \land u+t=0$) and its multiplicative group analogue across four mathematical domains, plus packaging verification for the literate dual-carrier rational fixture.

```markdown
| Fixture / Carrier | Target Theorem | Observed Axiom Cone | (a) PA | (b) Clean | TCB Tier | Gate 3 Global Audit | Duration |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- | :---: |
| **Finite Field ZMod 5 (Z/5Z)** | `C1ZMod5.c1_zmod5` | `[]` | **PASS** | **PASS** | Constructive Type Theory | **Gate 3 Certified** | `0.42s` |
| **Symmetric Group S3 (Order 6)** | `C1S3.c1_s3` | `[]` | **PASS** | **PASS** | Constructive Type Theory | **Gate 3 Certified** | `0.57s` |
| **Constructive Rational Prototype (Frac)** | `ConstructiveRat.c1_frac` | `[propext]` | **FAIL** | **PASS** | Constructive + Propext | **gate3_partial (Choice-Free Extension Section 4b)** | `0.52s` |
| **Standard Lean 4 Rat (Init.Data.Rat)** | `c1_elementary_rat` | `[propext, Classical.choice, Quot.sound]` | **FAIL** | **PASS** | Full Classical TCB | **gate3_partial (Declared Classical Extension Section 4b)** | `0.45s` |
| **Literate Dual-Carrier Rational Model (c1-std-rat)** | `C1StdRat.Main (rat_refl, frac_refl)` | `[]` | **PASS** | **PASS** | Dual-Carrier Packaging (Lean 4 + Frac) | **Gate 3 Certified** | `4.64s` |
```

---

## 2. In-Depth Domain Findings

### 1. Finite Field $\mathbb{Z}/5\mathbb{Z}$ (`c1-zmod5`)
- **Theorem**: `C1ZMod5.c1_zmod5 : ∀ t : ZMod5, ∃ u : ZMod5, add t u = zero ∧ add u t = zero`
- **Observed Axiom Cone**: **`[]`** (Zero axioms)
- **Mathematical Rationale**: In modular arithmetic over a finite field, additive inversion is computed by definitional case elimination (`rfl`). No extensionality or non-constructive choice principles are invoked.
- **TCB Status**: Fully PA-encodable and **Gate 3 Certified**.

### 2. Symmetric Group $S_3$ (`c1-s3`)
- **Theorem**: `C1S3.c1_s3 : ∀ g : S3, ∃ h : S3, mul g h = one ∧ mul h g = one`
- **Observed Axiom Cone**: **`[]`** (Zero axioms)
- **Mathematical Rationale**: In the non-abelian permutation group $S_3$ (order 6), each permutation's two-sided inverse is verified by definitional table lookup (`rfl`).
- **TCB Status**: Fully PA-encodable and **Gate 3 Certified**.

### 3. Constructive Rational Prototype (`c1-constructive-rat`)
- **Theorem**: `ConstructiveRat.c1_frac : ∀ t : Frac, ∃ u : Frac, (t + u) ~ zero ∧ (u + t) ~ zero`
- **Observed Axiom Cone**: **`[propext]`**
- **Breakthrough Finding**: **`Classical.choice` and `Quot.sound` are 100% eliminated!**
- **Mathematical Rationale**: By working over unreduced fraction pairs $(n, d)$ equipped with cross-multiplication equivalence, the non-constructive GCD normalization of Lean's standard library is bypassed. Only `propext` is required by the standard integer arithmetic lemmas (`Int.mul_one`, `Int.zero_mul`, `Int.add_mul`).
- **TCB Status**: Choice-free foundation, classified as **`gate3_partial (Choice-Free Extension Section 4b)`**.

### 4. Standard Lean 4 `Rat` (`c1-elementary-rat`)
- **Theorem**: `c1_elementary_rat : ∀ t : Rat, ∃ u : Rat, t + u = 0 ∧ u + t = 0`
- **Observed Axiom Cone**: **`[propext, Classical.choice, Quot.sound]`**
- **Mathematical Rationale**: Lean 4 core's `Init.Data.Rat` canonical normalization inherently relies on `Classical.choice` in `Rat.add_neg_cancel`.
- **TCB Status**: **`gate3_partial (Declared Classical Extension Section 4b)`**.

### 5. Literate Dual-Carrier Rational Fixture (`c1-std-rat`)
- **Theorems**: `rat_refl` (canonical Rat) and `frac_refl` (constructive Frac)
- **Observed Axiom Cone**: **`[]`** (Zero axioms for reflexive packaging validation)
- **Packaging vs. Full C1 Inversion**: Reflexive equality validates the entire literate compiler pipeline (`LexLean -> Lean -> leanchecker -> LexLeanAudit`) for both carriers. Full C1 additive inversion over canonical `Rat` inherits `{propext, Quot, Choice}`, whereas inversion over `Frac` requires only `[propext]`.
- **TCB Status**: **Gate 3 Certified** for packaging validation with declared Section 4b extensions.

---

## 3. SLA Budget Invariant Compliance (`INV-023d-int`)

- **Ceiling**: $\le 30.0\text{s}$
- **Measured Integration Duration**: `6.61s` across all 5 domain fixtures
- **Safety Margin**: `78.0%` headroom
- **Ledger Independence**: Executed strictly within downstream domain fixture boundaries without polluting the Phase 0 preflight guard ledger (`kernel/test` 9/9 pass).
