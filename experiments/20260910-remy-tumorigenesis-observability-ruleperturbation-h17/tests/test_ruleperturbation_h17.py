import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from run import RBL2_PERTURBATIONS, h1


def _eval(expr, ce1: bool, cd1: bool) -> bool:
    return h1.evaluate_expression(expr, {"CyclinE1": ce1, "CyclinD1": cd1})


def _original_rbl2(ce1: bool, cd1: bool) -> bool:
    return (not ce1) and (not cd1)


def test_original_rbl2_truth_table_hand_verified():
    """Ground truth: RBL2 = !CyclinE1 & !CyclinD1 is True ONLY at (False, False)."""
    assert _original_rbl2(False, False) is True
    assert _original_rbl2(False, True) is False
    assert _original_rbl2(True, False) is False
    assert _original_rbl2(True, True) is False


def test_perturbation_flip_FF_is_constant_false_everywhere():
    """Flipping the (F,F) row True->False, with all other rows already False, makes the WHOLE
    function constant False -- computationally verified against all 4 rows, not just asserted."""
    expr = RBL2_PERTURBATIONS["flip_FF_constant_false"]
    for ce1 in (False, True):
        for cd1 in (False, True):
            assert _eval(expr, ce1, cd1) is False


def test_perturbation_flip_FT_drops_CyclinD1_dependency():
    """Flipping (F,T) False->True: new table is True at (F,F) and (F,T), False at (T,F),(T,T) --
    i.e. True whenever CyclinE1=False, regardless of CyclinD1. Computationally verified."""
    expr = RBL2_PERTURBATIONS["flip_FT_drop_CyclinD1"]
    original = {
        (ce1, cd1): _original_rbl2(ce1, cd1) for ce1 in (False, True) for cd1 in (False, True)
    }
    expected = dict(original)
    expected[(False, True)] = True  # the flipped row
    for (ce1, cd1), exp in expected.items():
        assert _eval(expr, ce1, cd1) == exp, f"mismatch at ({ce1},{cd1})"


def test_perturbation_flip_TF_drops_CyclinE1_dependency():
    """Flipping (T,F) False->True: new table True at (F,F) and (T,F), False at (F,T),(T,T) --
    i.e. True whenever CyclinD1=False, regardless of CyclinE1. Computationally verified."""
    expr = RBL2_PERTURBATIONS["flip_TF_drop_CyclinE1"]
    expected = {
        (ce1, cd1): _original_rbl2(ce1, cd1) for ce1 in (False, True) for cd1 in (False, True)
    }
    expected[(True, False)] = True  # the flipped row
    for (ce1, cd1), exp in expected.items():
        assert _eval(expr, ce1, cd1) == exp, f"mismatch at ({ce1},{cd1})"


def test_perturbation_flip_TT_is_xnor():
    """Flipping (T,T) False->True: new table True at (F,F) and (T,T), False at (F,T),(T,F) --
    exactly XNOR(CyclinE1, CyclinD1). Computationally verified."""
    expr = RBL2_PERTURBATIONS["flip_TT_xnor"]
    expected = {
        (ce1, cd1): _original_rbl2(ce1, cd1) for ce1 in (False, True) for cd1 in (False, True)
    }
    expected[(True, True)] = True  # the flipped row
    for (ce1, cd1), exp in expected.items():
        assert _eval(expr, ce1, cd1) == exp, f"mismatch at ({ce1},{cd1})"


def test_each_perturbation_differs_from_original_at_exactly_one_row():
    """Structural sanity check: each of the 4 perturbations must differ from the original truth
    table at EXACTLY one of the 4 rows -- confirms these are genuine single-bit flips, not
    accidentally multi-bit changes or no-ops."""
    for name, expr in RBL2_PERTURBATIONS.items():
        if name == "baseline_unperturbed":
            continue
        diffs = 0
        for ce1 in (False, True):
            for cd1 in (False, True):
                if _eval(expr, ce1, cd1) != _original_rbl2(ce1, cd1):
                    diffs += 1
        assert diffs == 1, f"{name} differs from original at {diffs} rows, expected exactly 1"


def test_full_run_classifies_flip_TF_as_criterion_invalid_not_robust():
    """Regression test for a real finding caught during review (FL Step 4a Floor-Ceiling
    discipline): flip_TF_drop_CyclinE1 (RBL2 := !CyclinD1) does not merely make the escape
    UNOBSERVABLE-vs-observable -- it ABOLISHES the escape mechanism entirely (every k=1..6 on
    both branches relapses to GROWTH_ARREST, confirmed by a direct fate-distribution check,
    scratchpad diag_h17_flip_tf_investigate.py). A perturbation with no underlying transition is
    NOT evidence that M1 is 'robust' -- there is nothing for M1 to succeed at distinguishing.
    cmd_run() must classify this as CRITERION_INVALID_no_transition, not ROBUST, using the floor
    marker's own collision count as the transition-exists signal."""
    from run import cmd_run

    result = cmd_run()
    assert (
        result["per_perturbation_classification"]["flip_TF_drop_CyclinE1"]
        == "CRITERION_INVALID_no_transition"
    )
    assert "flip_TF_drop_CyclinE1" not in result["genuinely_robust_perturbations"]
    assert "flip_TF_drop_CyclinE1" in result["criterion_invalid_perturbations"]
    # the two perturbations that DO preserve a real transition AND resolve it at j=1
    assert set(result["genuinely_robust_perturbations"]) == {
        "flip_FT_drop_CyclinD1",
        "flip_TT_xnor",
    }
    assert result["genuinely_fragile_perturbations"] == ["flip_FF_constant_false"]
    assert result["verdict"] == "PARTIALLY-ROBUST"
