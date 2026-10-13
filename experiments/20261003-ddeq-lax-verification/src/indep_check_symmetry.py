"""Independent re-check (re-run round): does the printed 5-point flow G commute with F of eq (72), alpha=3/2?
Written without using symmetry.py; uses explicit shifts. Commutator condition: D_F(G) - D_G(F) = 0."""

import sympy as sp

N = range(-4, 5)
u1 = {i: sp.Symbol(f"a{i}") for i in N}
u2 = {i: sp.Symbol(f"b{i}") for i in N}
al = sp.Rational(3, 2)


def shift(e, k):
    return e.xreplace(
        {
            **{u1[i]: u1[i + k] for i in N if i + k in u1},
            **{u2[i]: u2[i + k] for i in N if i + k in u2},
        }
    )


F1 = 2 * (u2[0] * u1[0] ** 2 + al * u1[0] - u1[1])
F2 = 2 * (u2[-1] - u1[0] * u2[0] ** 2 - al * u2[0])
G1 = (
    u1[0] ** 3 * u2[0] ** 2
    - u1[0] ** 2 * u2[-1]
    - 2 * u1[0] * u1[1] * u2[0]
    - u1[1] ** 2 * u2[1]
    + u1[2]
)
G2 = (
    -(u1[0] ** 2) * u2[0] ** 3
    + 2 * u1[0] * u2[0] * u2[-1]
    + u1[1] * u2[0] ** 2
    + u1[-1] * u2[-1] ** 2
    - u2[-2]
)


def D(vec1, vec2, e):
    """derivation sum_i S^i(vec1) d/du1_i + S^i(vec2) d/du2_i"""
    tot = 0
    for i in N:
        for k, (sym, v) in enumerate([(u1[i], vec1), (u2[i], vec2)]):
            d = sp.diff(e, sym)
            if d != 0:
                tot += shift(v, i) * d
    return tot


c1 = sp.expand(D(F1, F2, G1) - D(G1, G2, F1))
c2 = sp.expand(D(F1, F2, G2) - D(G1, G2, F2))
print("commutator comp1 =", c1)
print("commutator comp2 =", c2)
# negative control: perturb G1
c1n = sp.expand(D(F1, F2, G1 + u1[0] ** 2 * u2[0]) - D(G1 + u1[0] ** 2 * u2[0], G2, F1))
print("NEG (G1 += u1_0^2 u2_0) comp1 nonzero:", c1n != 0)
# G is not a multiple of F
print("G1/F1 proportional? ", sp.simplify(G1 * F2 - G2 * F1) != 0)
