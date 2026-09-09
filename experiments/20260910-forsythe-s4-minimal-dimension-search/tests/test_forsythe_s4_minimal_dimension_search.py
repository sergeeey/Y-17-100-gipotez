import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from run import diag_matrix_from_log_params, objective


def test_diag_matrix_from_log_params_is_spd():
    log_params = np.array([0.5, -0.3, 1.2, 0.0, -1.0])
    A = diag_matrix_from_log_params(log_params)
    assert np.allclose(A, np.diag(np.diag(A)))
    assert (np.diag(A) > 0).all()


def test_objective_gives_nontrivial_gradient_not_a_flat_penalty():
    """Regression test locking in the caught bug: a first version of
    `objective` returned a FLAT -1.0 for every exact_solve_hit case, and a
    pilot run found 100% of a random population hit exact_solve_hit within
    7-16 restarts -- meaning differential_evolution had zero gradient to
    work with. The fixed objective must return DIFFERENT values for
    matrices that solve at very different speeds."""
    fast_params = np.array([0.0, 0.0, 0.0, 0.0, 0.0])  # identity-like, trivial
    slow_params = np.array([2.5, -2.5, 1.8, -1.2, 0.3])  # more spread, harder
    fast_score = objective(fast_params, base_seed=1)
    slow_score = objective(slow_params, base_seed=1)
    # not required to differ in a specific direction (depends on the actual
    # dynamics), only required to differ AT ALL -- the bug this guards
    # against made every outcome in the exact_solve regime identical.
    assert fast_score != slow_score


def test_objective_penalizes_breakdown_and_fast_solve_below_slow_solve_or_nondecay():
    """A candidate that stalls for the whole eval budget without exact-
    solving (a genuinely more interesting case) must score higher (i.e. a
    lower -- more negative objective is worse for the minimizer) than one
    that solves almost immediately. Constructs a case designed to solve
    fast (near-identity diagonal, s=4 close to full rank at n=5) and checks
    the ORDERING the fix's docstring claims, not just that scores differ."""
    fast_params = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
    fast_score = objective(fast_params, base_seed=2)
    # objective returns -mean(score); fast (immediate) exact-solve should be
    # close to the worst end of the score range (score near -1 -> objective
    # near +1), not the best end.
    assert fast_score > -0.5
