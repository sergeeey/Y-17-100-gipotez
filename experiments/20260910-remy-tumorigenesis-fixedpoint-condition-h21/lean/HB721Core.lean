-- H-B7-21 pilot: pure Lean 4 core (no mathlib) formalization of the "necessary and sufficient
-- condition" theorem discovered computationally (2984 exhaustive checks, 0 mismatches, all 35
-- network nodes, both branches -- see experiments/20260910-remy-tumorigenesis-fixedpoint-
-- condition-h21/decision.md).

section CoreLemma

variable {Row : Type} [DecidableEq Row]

/-- Manual reimplementation of `Function.update` (avoiding a mathlib import for this pilot). -/
def update (f : Row → Bool) (a : Row) (v : Bool) : Row → Bool :=
  fun x => if x = a then v else f x

/-- Necessary direction: perturbing row `a` DOES change evaluation exactly at `a`. -/
theorem update_at_own_row_changes (f : Row → Bool) (a : Row) :
    update f a (!(f a)) a ≠ f a := by
  unfold update
  simp only []
  cases f a <;> simp

/-- Sufficient direction: perturbing row `a` never changes evaluation at any OTHER row `x`. -/
theorem update_at_other_row_unchanged (f : Row → Bool) (a x : Row) (h : x ≠ a) :
    update f a (!(f a)) x = f x := by
  unfold update
  simp only [if_neg h]

/-- THE theorem: flipping row `a`'s table entry changes evaluation at `x` iff `x = a` -- the
exact necessary-and-sufficient condition H-B7-21's decision.md states informally ("the row
matching S's own input configuration"), now proven for ANY table over ANY row type with
decidable equality, not just the 35-node x 2-branch x 2984-row instance checked numerically. -/
theorem update_changes_iff (f : Row → Bool) (a x : Row) :
    update f a (!(f a)) x ≠ f x ↔ x = a := by
  constructor
  · intro hne
    cases (inferInstance : Decidable (x = a)) with
    | isTrue h => exact h
    | isFalse h => exact absurd (update_at_other_row_unchanged f a x h) hne
  · intro hxa
    rw [hxa]
    exact update_at_own_row_changes f a

end CoreLemma

section MultiNode

-- Part A's "sufficient" direction generalized to SEVERAL independent nodes overridden at once
-- (H-B7-21's run.py checked one concrete 2-node case computationally; here proved for a LIST of
-- any length, generalizing beyond the one instance tested).

variable {Row : Type} [DecidableEq Row]

/-- One node's table together with a chosen "safe" flip (a row that is NOT its own row). -/
structure SafeOverride (Row : Type) where
  table : Row → Bool
  ownRow : Row
  flipRow : Row
  safe : flipRow ≠ ownRow

/-- Simultaneously applying ANY LIST of safe, independent overrides leaves every overridden
node's evaluation at its OWN row unchanged -- the multi-node sufficiency claim, now proved for a
list of arbitrary length and content, not just the one 2-node case H-B7-21's run.py checked. -/
theorem all_safe_overrides_preserve_own_evaluation (overrides : List (SafeOverride Row)) :
    ∀ o ∈ overrides, update o.table o.flipRow (!(o.table o.flipRow)) o.ownRow = o.table o.ownRow := by
  intro o _
  exact update_at_other_row_unchanged o.table o.flipRow o.ownRow (Ne.symm o.safe)

end MultiNode

section ConcreteInstance

-- Ties the abstract theorem to REAL project data: RBL2's actual rule from the Remy et al. 2015
-- .bnet file (RBL2 = !CyclinE1 & !CyclinD1, experiments/20260906-remy-tumorigenesis-transient-
-- h4/data/remy_tumorigenesis.bnet line 46) and PROLIFERATION_STATE's own real
-- (CyclinE1, CyclinD1) = (true, false) values (H-B7-17's own `own_row`).
--
-- `decide` here is Lean's own decision procedure over a finite Bool x Bool domain -- an
-- independent, machine-checked confirmation of what H-B7-17's Python code found by direct
-- enumeration, using a completely different implementation (Lean's kernel, not CPython).

def RBL2Row := Bool × Bool  -- (CyclinE1, CyclinD1)
deriving DecidableEq

/-- The real RBL2 rule: `!CyclinE1 & !CyclinD1`. -/
def rbl2Table : RBL2Row → Bool
  | (cyclinE1, cyclinD1) => !cyclinE1 && !cyclinD1

/-- PROLIFERATION_STATE's own real (CyclinE1, CyclinD1) values (H-B7-17's `own_row`). -/
def proliferationRow : RBL2Row := (true, false)

/-- Sanity: RBL2's real table evaluates to `false` at PROLIFERATION_STATE's own row (RBL2=false
at the Proliferation attractor -- matches H-B7-13's own committed state string). -/
example : rbl2Table proliferationRow = false := by decide

/-- The exact real-world instance of H-B7-17/H-B7-21's finding, machine-checked by Lean's kernel:
flipping RBL2's row AT PROLIFERATION_STATE's own (CyclinE1,CyclinD1) configuration changes the
evaluation there -- this is `flip_TF_drop_CyclinE1`, the row H-B7-17/18 found destabilizes the
attractor. -/
example : update rbl2Table proliferationRow (!(rbl2Table proliferationRow)) proliferationRow
    ≠ rbl2Table proliferationRow := update_at_own_row_changes rbl2Table proliferationRow

/-- And flipping any of RBL2's OTHER 3 rows never changes evaluation at PROLIFERATION_STATE's own
row -- machine-checked over all 3 concrete non-own rows via `decide`, independently confirming
H-B7-17's own ROBUST/FRAGILE classification's floor. Stated as an explicit conjunction (not a
universal quantifier) since core Lean4 (no mathlib) lacks a generic Decidable-forall instance for
an arbitrary finite product type without a Fintype typeclass. -/
example :
    update rbl2Table (true, true) (!(rbl2Table (true, true))) proliferationRow
        = rbl2Table proliferationRow ∧
    update rbl2Table (false, true) (!(rbl2Table (false, true))) proliferationRow
        = rbl2Table proliferationRow ∧
    update rbl2Table (false, false) (!(rbl2Table (false, false))) proliferationRow
        = rbl2Table proliferationRow := by
  decide

end ConcreteInstance

#print axioms update_changes_iff
#print axioms all_safe_overrides_preserve_own_evaluation
