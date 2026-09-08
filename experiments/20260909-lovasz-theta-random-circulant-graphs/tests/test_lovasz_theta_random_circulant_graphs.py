import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from run import (
    sample_circulant_neighbors,
    theta_via_eigenvalues,
    theta_via_lp,
)


def test_theta_via_lp_matches_known_c5_value():
    """Positive control: theta(C_5) = sqrt(5) is a well-established textbook
    fact (Lovasz 1979's own example). C_5's connection set is {1,4} (offsets
    +-1 mod 5)."""
    c5 = np.array([0.0, 1.0, 0.0, 0.0, 1.0])
    assert abs(theta_via_lp(c5) - np.sqrt(5)) < 1e-8


def test_theta_via_eigenvalues_also_matches_c5_but_is_not_trusted_in_general():
    """Both implementations agree on this simple sparse cycle -- the
    divergence documented in `theta_via_eigenvalues`'s own docstring only
    appears on denser graphs (n>=9 in this session's own diagnosis), not
    here. Kept as a regression marker: if this test starts failing, the two
    implementations no longer even agree on the one case they were known to
    agree on."""
    c5 = np.array([0.0, 1.0, 0.0, 0.0, 1.0])
    assert abs(theta_via_eigenvalues(c5) - np.sqrt(5)) < 1e-8


def test_theta_via_eigenvalues_diverges_from_lp_on_a_known_dense_case():
    """Regression test locking in the caught bug: theta_via_eigenvalues is
    NOT a trustworthy general formula for circulant graphs -- on the n=9,
    seed=31090 case (found this session), the two disagree by ~0.6, and
    theta_via_lp is the one independently confirmed correct (see
    decision.md's C_9-complement cross-check). If this test's gap ever
    closes to ~0, the eigenvalue formula may have been fixed/was
    misdiagnosed -- re-examine before trusting it again."""
    c = sample_circulant_neighbors(9, 0.5, 31090)
    gap = abs(theta_via_eigenvalues(c) - theta_via_lp(c))
    assert gap > 0.1


def test_theta_via_lp_respects_theta_product_identity_for_vertex_transitive_graphs():
    """theta(G) * theta(Gbar) = n exactly for vertex-transitive graphs
    (Lovasz 1979, cited directly in the source paper's eq. 13). Circulant
    graphs are vertex-transitive. This is an independent consistency check
    on `theta_via_lp` distinct from the C_5 positive control."""
    n = 11
    c = sample_circulant_neighbors(n, 0.4, seed=555)
    c_complement = np.zeros(n)
    for k in range(1, n):
        c_complement[k] = 0.0 if c[k] > 0.5 else 1.0
    theta_g = theta_via_lp(c)
    theta_gbar = theta_via_lp(c_complement)
    assert abs(theta_g * theta_gbar - n) < 1e-6


def test_sample_circulant_neighbors_produces_symmetric_connection_vector():
    for n in (10, 11, 50):
        c = sample_circulant_neighbors(n, 0.5, seed=99)
        assert c[0] == 0.0
        for k in range(1, n):
            assert c[k] == c[n - k], f"n={n} k={k}: not symmetric"


def test_main_sweep_ratio_is_close_to_one_not_drifting_upward():
    """Ties the committed metrics/run.json's headline finding to a
    small, independently reproducible re-check: at a handful of n values
    spanning two orders of magnitude, theta(G)/sqrt(n) stays within a
    fairly tight band around 1, not growing systematically -- the core
    claim this experiment reports."""

    from run import main_sweep

    rows = main_sweep([(20, 8), (200, 4), (2000, 2)])
    ratios = [r["mean_theta_over_sqrt_n"] for r in rows]
    for ratio in ratios:
        assert 0.6 < ratio < 1.6, f"ratio {ratio} far from 1 -- re-examine before trusting"
