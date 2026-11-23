/-
Preflight.lean — empirical forbidden-constant probe for Lean 4.32.2
Phase 0 artifact; see PHASE0_MANIFEST.md §4, §4a, Gate 3.

Purpose
-------
Empirically determine which of the six policy-forbidden constants
(propext, Quot.sound, Classical.choice, Lean.ofReduceBool,
 Lean.trustCompiler, sorryAx)
appear in #print axioms output under the pinned toolchain.

The six-item list is POLICY (defensive upper bound).
The output of this file is EMPIRICAL (what the pin actually exposes).
Gate 3's cone scan uses the empirical set; the policy list guards
against future pins where a name reappears.

Run
---
  lake env lean Preflight.lean 2>&1 | tee preflight_$(date +%Y%m%dT%H%M%S).log
  (or, outside a Lake project: lean Preflight.lean 2>&1 | tee ...)

Compile-risk notes
------------------
  - Classical.choose / Classical.choose_spec: usually in default prelude.
    If they fail to resolve, add `import Init.Classical` at the top.
  - native_decide: usually in default prelude. If it fails to resolve,
    add `import Lean` at the top. If it still fails, remove §2b and §2c
    and record `native_decide_unavailable` as the preflight finding.
  - List.range was deliberately NOT used. Concrete arithmetic is
    guaranteed to be in default prelude; List.range is not. The manifest
    example `List.range 100` is equivalent in purpose; substitute it back
    only if you have confirmed List.range resolves in your prelude.
  - sorry emits a warning, not an error. The warning is expected and is
    evidence that sorryAx is in the cone.
-/

-- Add imports here if any probe below fails to resolve:
-- import Init.Classical
-- import Lean

/-! ## §0. Instrument sanity check — must report NO axioms

    If this theorem reports any axiom, the instrument is broken and no
    other output in this file is interpretable. -/

theorem preflight_clean : (0 : Nat) = 0 := rfl

/-! ## §1. Kernel primitive probes -/

-- propext: directly applies the axiom. Expected cone: [propext].
theorem preflight_propext (a b : Prop) (h : a ↔ b) : a = b :=
  propext h

-- Quot.sound: constructs two quotient elements related by the
-- always-true relation. Expected cone: [Quot.sound].
theorem preflight_quot :
    Quot.mk (fun (_ _ : Nat) => True) (0 : Nat) =
    Quot.mk (fun (_ _ : Nat) => True) (1 : Nat) :=
  Quot.sound trivial

-- Classical.choice: extracts a witness non-constructively.
-- Expected cone: [Classical.choice] (plus Quot.sound/propext only if
-- the choice implementation traverses them — record what actually appears).
noncomputable def preflight_classical_val : Nat :=
  Classical.choose (show ∃ n : Nat, n = 0 from ⟨0, rfl⟩)

theorem preflight_classical : preflight_classical_val = 0 :=
  Classical.choose_spec (show ∃ n : Nat, n = 0 from ⟨0, rfl⟩)

/-! ## §2. Computational-path probes (control + native)

    §2a is the control: kernel reduction, expected clean cone.
    §2b is the native path: expected cone [Lean.ofReduceBool].
    The *difference* between §2a and §2b is exactly the trust expansion.
    §2c is a second native-path probe with a different macro shape;
    if Lean.trustCompiler is observable in a cone, it will appear here
    or in §2b. If it appears in neither, classify it
    `unobservable_via_print_axioms`, not `absent`. -/

-- §2a. decide — kernel-reduction path. Expected cone: [] (clean).
theorem preflight_decide : (1000 : Nat) + 1000 = 2000 := by
  decide

-- §2b. native_decide — native path. Expected cone: [Lean.ofReduceBool].
theorem preflight_native : (1000 : Nat) + 1000 = 2000 := by
  native_decide

-- §2c. native_decide with a different macro shape. Expected cone:
-- [Lean.ofReduceBool] (and Lean.trustCompiler if observable at all).
theorem preflight_trustCompiler : (100 : Nat) * 100 = 10000 := by
  native_decide

/-! ## §3. Proof abandonment probe -/

-- sorryAx: expected cone [sorryAx]. The warning emitted here is
-- evidence, not failure.
theorem preflight_sorry : (1 : Nat) = 1 := by
  sorry

/-! ## §4. Emit the empirical cones -/

#print axioms preflight_clean
#print axioms preflight_propext
#print axioms preflight_quot
#print axioms preflight_classical
#print axioms preflight_decide
#print axioms preflight_native
#print axioms preflight_trustCompiler
#print axioms preflight_sorry
