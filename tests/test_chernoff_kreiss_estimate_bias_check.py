"""Tests for H-B2-1y: does the shallow K(A) estimate's underestimation bias grow with the
matrix's own apparent K(A), and does a deeper measurement pull the M1~K(A) exponent back toward
linear?"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

_HERE = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260908-chernoff-neuralode-nd-kreiss-estimate-bias-check"
)
_SPEC = importlib.util.spec_from_file_location("chernoff_1y_run", _HERE / "run.py")
biascheck = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(biascheck)

_CACHED_RESULT = None


def _cached_run():
    """cmd_run() computes a DEEP K(A) estimate for 16 matrices (~100-150s each via
    pseudopy.NonnormalAuto) -- cache across tests, same fix as prior pseudopy-based experiments."""
    global _CACHED_RESULT
    if _CACHED_RESULT is None:
        _CACHED_RESULT = biascheck.cmd_run()
    return _CACHED_RESULT


def test_sample_matrices_are_all_drawn_from_h_b2_1x_train_data():
    train_rows = biascheck.H_B2_1X_RESULT["train_data"]
    train_pairs = {(r["n_dim"], r["seed"]) for r in train_rows}
    # No duplicate (n_dim, seed) rows -- otherwise cmd_run()'s `next(...)` lookup could
    # silently pick the wrong row (reviewer-caught gap, H-B2-1y).
    assert len(train_pairs) == len(train_rows)
    for pair in biascheck.SAMPLE_MATRICES:
        assert pair in train_pairs


def test_sample_spans_a_wide_k_range():
    ks = [
        next(
            r["k_estimate"]
            for r in biascheck.H_B2_1X_RESULT["train_data"]
            if r["n_dim"] == n and r["seed"] == s
        )
        for n, s in biascheck.SAMPLE_MATRICES
    ]
    assert min(ks) < 35
    assert max(ks) > 200


def test_alpha_eps_via_tricontour_matches_exact_formula_for_symmetric_matrix():
    """Positive control, same discipline as H-B2-1v's own -- ratio must be ~1.0 for a symmetric
    (normal) matrix, using this experiment's own deeper eps range."""
    rng = np.random.default_rng(0)
    m = rng.standard_normal((5, 5))
    a = (m + m.T) / 2 - 3 * np.eye(5)
    import pseudopy

    pspec = pseudopy.NonnormalAuto(a, **biascheck.DEEP_AUTO_KWARGS)
    spectral_abscissa = float(np.max(np.linalg.eigvalsh(a)))
    for eps in (0.02, 0.01, 0.005):
        alpha_eps = biascheck._alpha_eps_via_tricontour(pspec, eps)
        assert alpha_eps is not None
        ratio = (alpha_eps - spectral_abscissa) / eps
        assert abs(ratio - 1.0) < 0.05, f"eps={eps}: ratio={ratio}"


def test_deep_k_is_at_least_as_large_as_shallow_k_for_every_matrix():
    """Deep K(A) samples smaller eps than the shallow production estimate -- by the arc's own
    established understanding (grid/circle-based K estimates only ever UNDERSHOOT as eps grows
    coarser), deep_k must be >= shallow_k for every matrix, never smaller.

    Reviewer-caught gap (H-B2-1y): the original loop only asserted inside `if deep_k is not
    None`, so it would pass vacuously if EVERY deep_k came back None. Assert non-None coverage
    explicitly first, then require it for ALL 16 matrices (not just "any"), since a matrix
    silently missing its deep estimate would otherwise corrupt the bias-factor regression
    without failing this test."""
    result = _cached_run()
    rows = list(result["per_matrix"].values())
    assert all(row["deep_k"] is not None for row in rows), (
        "every one of the 16 sampled matrices must have a deep_k -- a None here would silently "
        "drop that matrix from the bias-factor regression"
    )
    for row in rows:
        assert row["deep_k"] >= row["shallow_k"] - 1e-6


def test_cmd_run_produces_expected_shape_and_verdict():
    result = _cached_run()
    assert result["config"]["n_matrices"] == 16
    assert result["verdict"] in (
        "ARTIFACT_HYPOTHESIS_SUPPORTED",
        "GENUINE_SUPERLINEAR_PATTERN_SURVIVES",
        "MIXED_INCONCLUSIVE",
    )


def test_verdict_matches_the_bias_and_exponent_flags():
    result = _cached_run()
    bias_grows = result["bias_grows_with_k"]
    moved = result["exponent_moved_toward_linear"]
    if bias_grows and moved:
        assert result["verdict"] == "ARTIFACT_HYPOTHESIS_SUPPORTED"
    elif not bias_grows and not moved:
        assert result["verdict"] == "GENUINE_SUPERLINEAR_PATTERN_SURVIVES"
    else:
        assert result["verdict"] == "MIXED_INCONCLUSIVE"
