"""Tests for the H-B2-1 correction (theorem_3_1_check.py) -- written BEFORE trusting the
reversal, per this project's discipline.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

_HERE = (
    Path(__file__).resolve().parent.parent / "experiments" / "20260906-chernoff-neuralode-1d-decay"
)
_SPEC = importlib.util.spec_from_file_location("t31_check", _HERE / "theorem_3_1_check.py")
t31 = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(t31)


def test_bound_formula_matches_hand_derivation():
    # m=1: t^2/(2*n); m=2: t^3/(6*n)
    assert abs(t31.theorem_3_1_bound(1.0, 1, 1) - 0.5) < 1e-12
    assert abs(t31.theorem_3_1_bound(1.0, 1, 2) - (1.0 / 6.0)) < 1e-12
    assert abs(t31.theorem_3_1_bound(3.0, 6400, 1) - (9.0 / (2 * 6400))) < 1e-12


def test_bound_decreases_with_n_at_correct_order():
    b_50 = t31.theorem_3_1_bound(1.0, 50, 2)
    b_100 = t31.theorem_3_1_bound(1.0, 100, 2)
    # order 2: doubling n should quarter the bound
    assert abs(b_50 / b_100 - 4.0) < 1e-9


def test_m2_condition_holds_for_small_step_negative_control_for_large_step():
    assert t31.m2_condition_holds(t31.chernoff.block_order1, 1.0, 100)  # h=0.01, |1-h|<1
    assert not t31.m2_condition_holds(t31.chernoff.block_order1, 3.0, 1)  # h=3, |1-3|=2>1


def test_correction_bound_dominates_true_empirical_error_for_all_tested_cases():
    out = t31.cmd_run()
    assert out["theorem_3_1_bound_valid_and_tight_for_all_tested_cases"] is True
    for key, row in out["results"].items():
        for n, data in row["per_n"].items():
            assert data["bound_holds"], f"{key} n={n}: bound violated!"
            # "tight-ish": efficiency should not be absurdly small (bound not wildly loose)
            assert data["efficiency_true_over_bound"] > 0.01, (
                f"{key} n={n}: bound is {1 / data['efficiency_true_over_bound']:.0f}x looser "
                "than true error -- not actually tight"
            )
