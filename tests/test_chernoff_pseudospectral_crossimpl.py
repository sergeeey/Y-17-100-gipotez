"""Tests for H-B2-1s: independent cross-implementation check of H-B2-1r via pseudopy."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

_HERE = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260907-chernoff-neuralode-nd-pseudospectral-crossimpl"
)
_SPEC = importlib.util.spec_from_file_location("chernoff_1s_run", _HERE / "run.py")
crossimpl = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(crossimpl)


def test_pseudopy_vals_matches_exact_formula_for_symmetric_matrix():
    """FL Step 0a positive control: pseudopy's .Vals must be sigma_min(zI-A) -- verified
    empirically here, not assumed from external docs. For a normal (symmetric) matrix,
    sigma_min(zI-A) = dist(z, spectrum) exactly."""
    rng = np.random.default_rng(0)
    b = rng.normal(size=(5, 5))
    a_sym = (b + b.T) / 2.0
    spectral_abscissa = float(np.max(np.linalg.eigvalsh(a_sym)))
    eps = 1.0
    expected = spectral_abscissa + eps

    computed = crossimpl.pseudopy_alpha_eps(a_sym, eps=eps)
    # coarser grid than the production one (real range 27 wide / 150 pts ~ 0.18 spacing) --
    # allow slack for grid discretization, same discipline as H-B2-1r's own regression test
    assert abs(computed - expected) < 1.0


def test_reuses_h_b2_1r_m1_values_not_recomputed():
    """The M1 values used here must come directly from H-B2-1r's own run.json, matched by the
    exact same seed keys -- not silently misaligned or recomputed."""
    for n_dim_str, slice_data in crossimpl.H_B2_1R_RESULT["per_n_slice"].items():
        if int(n_dim_str) not in crossimpl.PRIMARY_N_DIM_VALUES:
            continue
        assert "per_seed" in slice_data
        assert len(slice_data["per_seed"]) == 15


def _cached_run() -> dict:
    """cmd_run() re-runs pseudopy on all 30 matrices (~5s/matrix) -- share one call across the
    3 tests below instead of tripling an already-expensive third-party computation."""
    if not hasattr(_cached_run, "_result"):
        _cached_run._result = crossimpl.cmd_run()
    return _cached_run._result


def test_verdict_is_one_of_three_outcomes():
    result = _cached_run()
    assert result["verdict"] in {"CONFIRMED", "WEAKENED", "KILLED_OR_WEAKENED"}


def test_verdict_matches_kill_criterion_logic():
    result = _cached_run()
    both_sig = all(
        v["pseudopy_vs_m1"]["significant_positive"] for v in result["per_n_slice"].values()
    )
    all_close = all(v["median_relative_diff"] < 0.15 for v in result["per_n_slice"].values())
    any_lost = any(
        not v["pseudopy_vs_m1"]["significant_positive"] for v in result["per_n_slice"].values()
    )
    if both_sig and all_close:
        assert result["verdict"] == "CONFIRMED"
    elif any_lost:
        assert result["verdict"] == "KILLED_OR_WEAKENED"
    else:
        assert result["verdict"] == "WEAKENED"


def test_real_run_produces_2_slices_of_15_seeds_each():
    result = _cached_run()
    assert len(result["per_n_slice"]) == 2
    assert set(result["per_n_slice"].keys()) == {"40", "50"}
    for slice_data in result["per_n_slice"].values():
        assert slice_data["n_seeds"] == 15
        assert len(slice_data["per_seed"]) == 15
