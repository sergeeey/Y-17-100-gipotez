# ruff: noqa: E501
"""Regression tests for the H-CAT56-2 rank-family scripts (experiments/20260925-h-cat56-2-rank-family).

Pins the computed (not proven) statements used in note_draft.md section 6: the closed form
min_s LB(k,r,s) = r^2 + ceil(2kr/(r^2+1)) + 1 for k >= r, and the first size d*(r) where the dimension test can fire.
Also tests that check_predictions.py actually FAILS on a wrong or mislabelled result (it is the script that carries the
pre-registered comparison, so a checker that always says OK would be the worst outcome).
Numerical regression only, not a proof.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import math
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_DIR = _ROOT / "experiments" / "20260925-h-cat56-2-rank-family"
_METRICS = _ROOT / "experiments" / "20260919-pcc-generic-quasipure-cat56-2" / "metrics"


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, _DIR / filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cf = _load("h_cat56_2_closed_form_check", "closed_form_check.py")
cp = _load("h_cat56_2_check_predictions", "check_predictions.py")


def _first_firing_d(r: int, kmax: int = 80) -> int | None:
    for k in range(1, kmax + 1):
        if cf.exact_min(k, r)[0] < k + r:
            return k + r
    return None


def _saved(d: int, r: int, s: int) -> dict:
    return json.loads((_METRICS / f"fp_certify_d{d}_r{r}_s{s}.json").read_text(encoding="utf-8"))


def test_closed_form_min_lb_holds_for_k_at_least_r() -> None:
    for r in (2, 3, 4, 5, 6):
        for k in range(r, 41):
            s_star = math.ceil(2 * k * r / (r * r + 1))
            assert cf.exact_min(k, r)[0] == r * r + s_star + 1, (r, k)


def test_closed_form_is_known_to_fail_for_degenerate_small_k() -> None:
    """Negative control: k < r is outside the regime, and the closed form must NOT be assumed there."""
    r, k = 4, 2
    s_star = math.ceil(2 * k * r / (r * r + 1))
    assert cf.exact_min(k, r)[0] != r * r + s_star + 1


def test_first_firing_size_matches_registered_thresholds() -> None:
    assert {r: _first_firing_d(r) for r in (2, 3, 4, 5, 6)} == {2: 22, 3: 23, 4: 31, 5: 41, 6: 54}


def test_no_firing_below_threshold_for_r2() -> None:
    assert all(cf.exact_min(d - 2, 2)[0] >= d for d in range(4, 22))


def test_lower_bound_equals_saved_f_p_result_for_the_exact_instance_size() -> None:
    """d=22, r=2, s=16: LB = 21 and the SAVED F_p certificate reports dim V-perp = 21 on both primes."""
    assert cf.lb(20, 2, 16) == 21
    assert [x["dimVperp_mod_p"] for x in _saved(22, 2, 16)["runs"]] == [21, 21]


def test_check_predictions_accepts_every_saved_result() -> None:
    for d, r, s, kind in cp.CONFIGS:
        problems, _ = cp.evaluate(d, r, s, kind, _saved(d, r, s))
        assert problems == [], (d, r, s, kind, problems)


def test_check_predictions_fails_on_a_wrong_value() -> None:
    res = copy.deepcopy(_saved(31, 4, 13))
    res["runs"][0]["dimVperp_mod_p"] += 1
    problems, _ = cp.evaluate(31, 4, 13, "fire", res)
    assert "PRED_MISMATCH" in problems


def test_check_predictions_fails_on_a_mislabelled_file() -> None:
    problems, _ = cp.evaluate(41, 5, 14, "fire", _saved(31, 4, 13))
    assert "LABEL_MISMATCH" in problems


def test_check_predictions_fails_on_a_wrong_prime_and_a_false_flag() -> None:
    res = copy.deepcopy(_saved(23, 3, 12))
    res["runs"][1]["p"] = 7
    res["runs"][0]["pcc_zero"] = False
    problems, _ = cp.evaluate(23, 3, 12, "fire", res)
    assert "PRIME_MISMATCH" in problems
    assert "FLAG_FALSE" in problems


def test_check_predictions_flags_a_fire_claim_that_does_not_fire() -> None:
    """A below-crossing result labelled as a firing config must be rejected."""
    problems, _ = cp.evaluate(31, 4, 12, "fire", _saved(31, 4, 12))
    assert "FIRE_MISMATCH" in problems or "PRED_MISMATCH" in problems
