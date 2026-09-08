"""Tests for H-B2-1v: independent cross-implementation check of H-B2-1u's small-eps Kreiss
constant growth via pseudopy.NonnormalAuto (a circle-based algorithm, not H-B2-1u's box grid or
H-B2-1s's NonnormalMeshgrid)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

_HERE = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260908-chernoff-neuralode-nd-kreiss-crossimpl-smalleps"
)
_SPEC = importlib.util.spec_from_file_location("chernoff_1v_run", _HERE / "run.py")
crossimpl = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(crossimpl)

_CACHED_RESULT = None


def _cached_run():
    """cmd_run() is expensive (~2min/matrix x 3 matrices via pseudopy.NonnormalAuto) -- cache
    across tests in this module, same fix as H-B2-1s/1u's _cached_run helper."""
    global _CACHED_RESULT
    if _CACHED_RESULT is None:
        _CACHED_RESULT = crossimpl.cmd_run()
    return _CACHED_RESULT


def test_reuses_build_matrix_with_seed_and_n_unchanged():
    import inspect

    _M_DIR = (
        Path(__file__).resolve().parent.parent
        / "experiments"
        / "20260907-chernoff-neuralode-nd-multiseed-multin"
    )
    _SPEC_M = importlib.util.spec_from_file_location("chernoff_1v_multin_direct", _M_DIR / "run.py")
    multin_direct = importlib.util.module_from_spec(_SPEC_M)
    _SPEC_M.loader.exec_module(multin_direct)
    assert inspect.getsource(crossimpl.multin.build_matrix_with_seed_and_n) == inspect.getsource(
        multin_direct.build_matrix_with_seed_and_n
    )


def test_plateau_check_detects_a_genuine_plateau():
    """Synthetic sanity check: a ratio sequence that STABILIZES (growth factor -> 1.0) must be
    flagged as a plateau, distinguishing it from H-B2-1u's real, still-growing sequence."""
    stable_ratios = {
        "0.02": 10.0,
        "0.01": 10.2,
        "0.005": 10.3,
        "0.002": 10.35,
        "0.001": 10.37,
    }
    check = crossimpl._plateau_check(stable_ratios)
    assert check["plateau_detected"] is True


def test_plateau_check_rejects_h_b2_1u_own_still_growing_sequence():
    """The ACTUAL grid-search sequence from H-B2-1u's worst-case matrix (seed=301,N=50) --
    growth factor ~1.6-2x per halving, no plateau -- must NOT be flagged as a plateau."""
    still_growing_ratios = {
        "0.02": 262.9,
        "0.01": 437.7,
        "0.005": 723.3,
        "0.002": 1377.8,
        "0.001": 2208.5,
    }
    check = crossimpl._plateau_check(still_growing_ratios)
    assert check["plateau_detected"] is False
    assert all(f > 1.3 for f in check["growth_factors"])


def test_pseudopy_auto_ratios_matches_exact_formula_for_symmetric_matrix():
    """Positive control: for a symmetric (normal) matrix, alpha_eps(A) = alpha(A) + eps
    EXACTLY, so ratio should be ~1.0 at every eps -- same positive control discipline as
    H-B2-1r/1u's own symmetric-matrix tests.

    This test is the one that CAUGHT the extraction bug documented at the top of run.py: a
    first-draft `points`/`vals` masking approach gave ratio~0.84 here (should be exactly 1.0),
    a systematic ~16% undershoot -- failed this exact assertion, at a much looser 0.15
    tolerance, before the fix. The fixed tricontour-based extraction gives ratio~0.9998-1.0000,
    so the tolerance here is tight (0.02, not the original 0.15) -- a loose tolerance would not
    have caught the original bug and must not be reintroduced."""
    rng = np.random.default_rng(0)
    m = rng.standard_normal((5, 5))
    a = (m + m.T) / 2 - 3 * np.eye(5)
    result = crossimpl.pseudopy_auto_ratios(a, eps_values=(0.02, 0.01, 0.005))
    for eps_key, ratio in result["ratios_by_eps"].items():
        assert ratio is not None
        assert abs(ratio - 1.0) < 0.02, f"eps={eps_key}: ratio={ratio}, expected ~1.0"


def test_cmd_run_produces_three_matrices_with_full_eps_comparison():
    result = _cached_run()
    assert len(result["per_matrix"]) == 3
    for m in result["per_matrix"].values():
        assert len(m["comparison"]) == len(crossimpl.EPS_VALUES)


def test_verdict_is_one_of_the_three_pre_registered_outcomes():
    result = _cached_run()
    assert result["verdict"] in (
        "CONFIRMED_GENUINE_MATRIX_PROPERTY",
        "GRID_SEARCH_ARTIFACT_SUSPECTED",
        "METHODS_DISAGREE",
    )


def test_worst_case_matrix_seed301_n50_is_included_and_matches_h_b2_1u_baseline():
    """The primary matrix must reuse H-B2-1u's own grid-search numbers unchanged, not
    recompute them -- Minimal Relaxation Rule."""
    result = _cached_run()
    m = result["per_matrix"]["n50_seed301"]
    grid_at_002 = m["comparison"]["0.02"]["grid"]
    assert abs(grid_at_002 - 261.74) < 0.01  # H-B2-1u's own reported k_estimate for this matrix
