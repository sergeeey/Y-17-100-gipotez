import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from run import (
    _log_decay_slope,
    build_spd_matrix,
    krylov_orthonormal_basis,
    restart_step,
    run_restarted_iteration,
)


def test_build_spd_matrix_is_genuinely_spd_for_every_mode():
    for mode in ("random", "clustered", "geometric"):
        A = build_spd_matrix(10, seed=1, mode=mode)
        assert np.allclose(A, A.T)
        eigvals = np.linalg.eigvalsh(A)
        assert (eigvals > 0).all()


def test_krylov_basis_is_orthonormal_regardless_of_conditioning():
    """Regression test for the bug caught this session: the raw power basis
    [y, Ay, A^2 y, ...] loses independence exponentially fast for
    ill-conditioned A (cond(V) hit 1e19 at s=7 for cond(A)=1e6, verified via
    diag_krylov.py). The fix (Lanczos + full reorthogonalization) must keep
    cond(Q)=1 independent of cond(A)."""
    A = build_spd_matrix(10, seed=2, mode="geometric")  # cond(A) ~ 1e6
    assert np.linalg.cond(A) > 1e5
    rng = np.random.default_rng(3)
    y = rng.standard_normal(10)
    y = y / np.linalg.norm(y)
    Q, breakdown = krylov_orthonormal_basis(A, y, s=8)
    assert not breakdown
    gram = Q.T @ Q
    assert np.allclose(gram, np.eye(8), atol=1e-10)


def test_restart_step_with_full_dimension_solves_exactly():
    """With s = n, the Krylov subspace spans all of R^n, so one restart must
    reduce the residual to (numerically) zero -- the Galerkin condition
    becomes the exact linear solve."""
    A = build_spd_matrix(6, seed=4, mode="random")
    rng = np.random.default_rng(5)
    r0 = rng.standard_normal(6)
    y0 = r0 / np.linalg.norm(r0)
    r1, breakdown = restart_step(A, r0, y0, s=6)
    assert not breakdown
    assert np.linalg.norm(r1) < 1e-8


def test_breakdown_detected_when_residual_is_already_an_eigenvector():
    """If r_0 is an eigenvector of A, d(A, r_0) = 1: the Krylov subspace
    K_s(A, r_0) for any s >= 2 collapses to a 1-dimensional space (every
    power A^j y is parallel to y), so the construction must flag breakdown,
    not silently return a degenerate answer."""
    A = build_spd_matrix(6, seed=6, mode="random")
    _, eigvecs = np.linalg.eigh(A)
    y0 = eigvecs[:, 0]
    _, breakdown = restart_step(A, y0.copy(), y0, s=3)
    assert breakdown


def test_log_decay_slope_distinguishes_real_decay_from_plateau():
    k = np.arange(200)
    decaying = list(np.exp(-0.05 * k))
    plateaued = list(0.01 + 1e-6 * np.sin(k))
    growing = list(0.001 * np.exp(0.01 * k))
    assert _log_decay_slope(decaying) < -0.01
    assert _log_decay_slope(plateaued) > -1e-4
    assert _log_decay_slope(growing) > 0


def test_run_restarted_iteration_on_identity_reports_breakdown_not_false_convergence():
    """Edge-case positive control: A = I has d(A) = 1 distinct eigenvalue, so
    no s >= 2 satisfies the conjecture's own precondition 2 <= s < d(A) --
    K_s(I, y) collapses to span{y} for any s (A y = y, every power is a
    duplicate direction). The harness must report this as a breakdown
    (checked directly at the single-step level, matching what
    `restart_step` itself reports) rather than silently producing a
    spurious "converged" or "counterexample" verdict on a case the
    conjecture does not even apply to."""
    A = np.eye(5)
    y0 = np.array([1.0, 0.0, 0.0, 0.0, 0.0])
    _, step_breakdown = restart_step(A, y0.copy(), y0, s=2)
    assert step_breakdown

    res = run_restarted_iteration(A, s=2, seed=7, max_restarts=50)
    assert res["breakdown_hit"]


@pytest.mark.parametrize(
    "n,seed,s",
    [
        (8, 37800, 5),
        (8, 37801, 5),
        (12, 38200, 7),
        (12, 38201, 4),
        (12, 38201, 6),
        (12, 38202, 7),
    ],
)
def test_no_genuine_counterexample_survives_extended_restart_budget(n, seed, s):
    """Consistency check tying the committed metrics/run.json's honest
    'no_decay_detected' bucket (an artifact of the 1500-restart budget, not
    a real counterexample -- see decision.md) to a directly-reproducible,
    higher-budget re-run. Every (n, seed, s) that looked like a plateau at
    1500 restarts must resolve (exact solve or confirmed negative decay
    slope) well before 8000 restarts."""
    A = build_spd_matrix(n, seed, "geometric")
    res = run_restarted_iteration(A, s, seed, max_restarts=8000)
    resolved = res["exact_solve_hit"] or (
        res.get("decay_slope") is not None and res["decay_slope"] < -1e-4
    )
    assert resolved, f"n={n} seed={seed} s={s} still unresolved at 8000 restarts: {res}"
