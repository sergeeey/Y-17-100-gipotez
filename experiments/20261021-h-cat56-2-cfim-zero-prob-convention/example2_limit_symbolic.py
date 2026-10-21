"""Symbolic (sympy) closed forms for the null outcome of Nurdin Example 2
(claims Z2, Z3 of claim.md).

Model: rho(theta) on C^3 with D = 1/2, s = 1 - theta_1, g^2 = D^2 (1 - D^2) = 3/16,
phi = c . theta with c = (1, 7/10), f = s g z, z = exp(i phi). The null outcome is
|y0><y0| with y0 = (-f0, 0, D^2 s0)/(D s0) at theta_0 = (3/10, 3/5).

Unit-circle bookkeeping: z and w = z(theta_0) are symbols; conj(z) = 1/z and conj(w) = 1/w.

Checked exactly:
  (i)  p_null(theta) = 2 (1 - theta_1) g^2 (1 - cos(phi(theta) - phi(theta_0))),
       written as a rational identity in z, w.
  (ii) For a direction h, the classical contribution (d_h p)^2 / p of the null outcome
       along theta_0 + t h tends to 4 s0 g^2 (c . h)^2 as t -> 0 (exact limit), and the
       matrix limit is N = 4 s0 g^2 c c^T (rank one).
  (iii) Hess p_null(theta_0) = 2 s0 g^2 c c^T = N / 2.
"""

import sympy as sp

z, w, t1, t2, tt = sp.symbols("z w t1 t2 tt")
D = sp.Rational(1, 2)
g2 = D**2 * (1 - D**2)  # = 3/16
c = sp.Matrix([1, sp.Rational(7, 10)])
th0 = sp.Matrix([sp.Rational(3, 10), sp.Rational(3, 5)])
s0 = 1 - th0[0]


def conj_expr(e):
    """Unit-circle conjugation: z <-> 1/z, w <-> 1/w, real symbols unchanged."""
    return e.subs({z: 1 / z, w: 1 / w}, simultaneous=True)


def rho_entries(s, zz):
    f = s * sp.sqrt(g2) * zz  # g = D sqrt(1-D^2) so g^2 = g2; use sqrt(g2) = sqrt(3)/4
    return f


def main():
    # (i) closed form of the null probability
    s = 1 - t1
    g = D * sp.sqrt(1 - D**2)
    f = s * g * z
    rho = sp.Matrix(
        [
            [D**2 * s, 0, f],
            [0, t1, 0],
            [conj_expr(f), 0, (1 - D**2) * s],
        ]
    )
    f0 = s0 * g * w
    y0 = sp.Matrix([-f0, 0, D**2 * s0]) / (D * s0)
    y0_conj = sp.Matrix(
        [conj_expr(sp.conjugate(y0[0])) if False else conj_expr(-f0), 0, D**2 * s0]
    ) / (D * s0)
    p_expr = (y0_conj.T * rho * y0)[0, 0]
    p_expr = sp.simplify(sp.expand(p_expr))
    closed = 2 * s * g**2 * (1 - (z / w + w / z) / 2)
    residual_i = sp.simplify(sp.expand(p_expr - closed))
    print("(i) p_null - closed form (should be 0):", residual_i)

    # (ii) and (iii): direction-wise limit of the null contribution and the Hessian at theta_0
    h = sp.Matrix([sp.Symbol("h1"), sp.Symbol("h2")])
    phi_theta = c.dot(sp.Matrix([t1, t2]))
    phi_0 = c.dot(th0)
    p_closed = 2 * (1 - t1) * g**2 * (1 - sp.cos(phi_theta - phi_0))
    grad = sp.Matrix([sp.diff(p_closed, t1), sp.diff(p_closed, t2)])
    theta_t = th0 + tt * h
    sub = {t1: theta_t[0], t2: theta_t[1]}
    sp.series(p_closed.subs(sub), tt, 0, 3).removeO()
    grad_t = grad.subs(sub)
    contrib = sp.Matrix(2, 2, lambda a, b: grad_t[a] * grad_t[b] / p_closed.subs(sub))
    limit_matrix = contrib.applyfunc(lambda e: sp.limit(sp.simplify(e), tt, 0))
    n_pred = 4 * s0 * g**2 * c * c.T
    print("(ii) limit of the null contribution along h (matrix):", sp.simplify(limit_matrix))
    print(
        "     equals 4 s0 g^2 (c.h)^2 as a quadratic form:",
        sp.simplify((h.T * limit_matrix * h)[0, 0] - 4 * s0 * g**2 * (c.T * h)[0, 0] ** 2) == 0,
    )
    print(
        "     matrix limit independent of h (rank-one N):",
        sp.simplify(limit_matrix - n_pred) == sp.zeros(2, 2),
    )

    hess = sp.Matrix(
        2,
        2,
        lambda a, b: sp.diff(p_closed, [t1, t2][a], [t1, t2][b]).subs({t1: th0[0], t2: th0[1]}),
    )
    print("(iii) Hess p_null(theta_0) =", sp.simplify(hess))
    print(
        "      equals N/2 with N = 4 s0 g^2 c c^T:",
        sp.simplify(hess - n_pred / 2) == sp.zeros(2, 2),
    )
    print("      s0 g^2 =", sp.simplify(s0 * g**2), "; N =", sp.simplify(n_pred))


if __name__ == "__main__":
    main()
