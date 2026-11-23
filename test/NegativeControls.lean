/-
NegativeControls.lean — Gate 3 Negative Control Validation
Tests that the Gate 3 cone scanner actively detects and rejects:
1. Dynamic native_decide tactic axioms (*.native_decide.ax_*)
2. Proof abandonment axioms (sorryAx)
-/

-- Negative Control 1: native_decide under \noaxioms policy
theorem negative_control_native : (1000 : Nat) + 1000 = 2000 := by
  native_decide

#print axioms negative_control_native

-- Negative Control 2: sorry under \noaxioms policy
theorem negative_control_sorry : (0 : Nat) = 1 := by
  sorry

#print axioms negative_control_sorry
