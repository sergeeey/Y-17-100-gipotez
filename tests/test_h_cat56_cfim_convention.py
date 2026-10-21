"""Regression tests for the zero-probability / CFIM-convention analysis
(experiments/20261021-h-cat56-2-cfim-zero-prob-convention).

Each test loads a script of the folder by path (as in
test_h_cat56_projective_criterion.py) and checks an exact or high-precision identity from
claim.md. Heavy random sweeps are reduced to one seed per configuration. Each geometric check
counts every class separately and asserts that each class is non-empty and agrees with its
expected truth value, so agreement cannot be vacuous.
"""

import importlib.util
from pathlib import Path

import mpmath as mp
import sympy as sp

EXP = (
    Path(__file__).resolve().parents[1]
    / "experiments"
    / "20261021-h-cat56-2-cfim-zero-prob-convention"
)


def _load(name):
    spec = importlib.util.spec_from_file_location(name, EXP / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_example2_point_cfim_gap_is_null_term():
    """Z1 at Example 2 (50 digits): F^Q - F_pos = N = 4 s0 G^2 c c^T, the rank-one null term."""
    m = _load("example2_zero_probability_limits")
    psi, e1, y = m.basis_at_theta0()
    povm = [m.outer(psi), m.outer(e1), m.outer(y)]
    eigvals = [1 - m.THETA0[0], m.THETA0[0], mp.mpf(0)]
    fq = m.qfim_at(m.THETA0, [psi, e1, y], eigvals)
    f_pos = m.cfim_at(povm[:2], m.THETA0)
    s0 = 1 - m.THETA0[0]
    c = [m.C1, m.C2]
    for a in range(2):
        for b in range(2):
            n_pred = 4 * s0 * m.G**2 * c[a] * c[b]
            assert abs(fq[a][b] - f_pos[a][b] - n_pred) < mp.mpf("1e-25")


def test_example2_null_probability_closed_form_and_hessian():
    """Z2 and Z5 at Example 2: p_null(theta) = 2(1-theta_1) g^2 (1 - cos(c.(theta - theta0)))
    and Hess = N/2."""
    m = _load("example2_zero_probability_limits")
    _psi, _e1, y = m.basis_at_theta0()
    null_proj = m.outer(y)
    for th in [(mp.mpf("0.31"), mp.mpf("0.59")), (mp.mpf("0.27"), mp.mpf("0.66"))]:
        closed = 2 * (1 - th[0]) * m.G**2 * (1 - mp.cos(m.phi(th) - m.phi(m.THETA0)))
        assert abs(m.prob(null_proj, th) - closed) < mp.mpf("1e-40")
    s0 = 1 - m.THETA0[0]
    c = [m.C1, m.C2]
    n_pred = [[4 * s0 * m.G**2 * c[a] * c[b] for b in range(2)] for a in range(2)]
    for a in range(2):
        for b in range(2):
            order = [0, 0]
            order[a] += 1
            order[b] += 1
            hess = mp.diff(
                lambda x, yv: m.prob(null_proj, (x, yv)), (m.THETA0[0], m.THETA0[1]), tuple(order)
            )
            assert abs(hess - n_pred[a][b] / 2) < mp.mpf("1e-30")


def test_example2_symbolic_null_matrix_and_limit():
    """Z3 (exact, direction h = (1, -2) with c.h != 0): the matrix limit of the null contribution
    is N = 4 s0 g^2 c c^T. Directions with c.h = 0 are excluded: there p_null vanishes
    identically and the limit is F_pos (decision.md, A7)."""
    _z, _w, t1, t2, tt = sp.symbols("z w t1 t2 tt")
    dd = sp.Rational(1, 2)
    g2 = dd**2 * (1 - dd**2)
    c = sp.Matrix([1, sp.Rational(7, 10)])
    th0 = sp.Matrix([sp.Rational(3, 10), sp.Rational(3, 5)])
    s0 = 1 - th0[0]
    p_closed = 2 * (1 - t1) * g2 * (1 - sp.cos(c[0] * t1 + c[1] * t2 - c.dot(th0)))
    grad = sp.Matrix([sp.diff(p_closed, t1), sp.diff(p_closed, t2)])
    h = sp.Matrix([sp.Rational(1, 1), sp.Rational(-2, 1)])
    sub = {t1: th0[0] + tt * h[0], t2: th0[1] + tt * h[1]}
    p_t = p_closed.subs(sub)
    g_t = grad.subs(sub)
    limit = sp.Matrix(2, 2, lambda a, b: sp.limit(sp.simplify(g_t[a] * g_t[b] / p_t), tt, 0))
    n_pred = 4 * s0 * g2 * c * c.T
    assert sp.simplify(limit - n_pred) == sp.zeros(2, 2)


def test_random_identities_one_seed_each_mode():
    """Z5-Z8 on one random family per mode (rank-two and rank-one null parts)."""
    m = _load("zero_prob_identities_random")
    for mode in ["generic", "proportional"]:
        rep = m.run_seed(1, mode)
        assert all(float(x["rel_error"]) < 1e-25 for x in rep["Z5"])
        assert all(float(x["rel_error"]) < 1e-15 for x in rep["Z6"])
        assert all(float(x["rel_error"]) < 1e-15 for x in rep["Z7"])
        assert all(x["agree"] for x in rep["Z8"])


def test_geometric_criterion_element_and_union_characterization():
    """G1 (regular and null) and G2 (members, non-members, and the zero branch P_+ v = 0), and
    the N-level identity. Each class is non-empty and agrees with its expected truth value."""
    m = _load("geometric_criterion_check")
    for p_params in [2, 3]:
        rho, ls, drhos, p_plus, ls_coeff = m.setup(p_params)
        g1 = m.g1_check(rho, ls, drhos, p_plus, ls_coeff, trials=60)
        assert g1["skipped"] == 0
        assert g1["regular_pos_tested"] > 0 and g1["regular_neg_tested"] > 0
        assert g1["regular_pos_agree"] == g1["regular_pos_tested"]
        assert g1["regular_neg_agree"] == g1["regular_neg_tested"]
        assert g1["null_vectors_tested"] > 0
        assert g1["null_agree"] == g1["null_vectors_tested"]
        g1n = m.g1_null_check(p_params, trials=40)
        assert g1n["positive_tested"] > 0 and g1n["negative_tested"] > 0
        assert g1n["positive_agree"] == g1n["positive_tested"]
        assert g1n["negative_agree"] == g1n["negative_tested"]
        g2 = m.g2_check(ls, p_plus, ls_coeff, trials=80)
        assert g2["skipped"] == 0
        for name in m.G2_CLASSES:
            assert g2[f"{name}_tested"] > 0
            assert g2[f"{name}_agree"] == g2[f"{name}_tested"]
        w_random = m.identity_check(rho, ls, drhos, trials=5)
        w_block = m.identity_check(rho, ls, drhos, trials=5, block=True)
        assert w_random["worst_abs"] < 1e-10
        assert w_block["worst_abs"] < 1e-10 and w_block["null_outcomes"] > 0


def test_prop6_readings_at_control_point_D():
    """P1 (literal reading fails at D) and P2 (one-sided reading holds at D) for both POVMs,
    exact arithmetic."""
    m = _load("prop6_readings_check")
    rows = m.main()
    for row in rows:
        assert row["literal_failing_ordered_pairs"] > 0
        assert row["one_sided_failing_unordered_pairs"] == 0
