"""Example 2 (Nurdin arXiv:2405.01471 v1, p. 11): point CFIM versus limit CFIM,
Hellinger form and QFIM.

Claims checked (see claim.md): Z1 (point CFIM misses the null outcome), Z2 (closed form of
the null probability), Z3 (direction-wise limit of the CFIM equals the QFIM), Z4 (Hellinger
quadratic form equals QFIM / 4).

Model as in ../20261021-h-cat56-2-projective-criterion/example2_check.py:
rho_theta on C^3 with D = 1/2, phi = c1 theta_1 + c2 theta_2, c1 = 1, c2 = 7/10,
f = (1 - theta_1) D sqrt(1 - D^2) e^{i phi}. Specified POVM (regular projectors on the support
eigenbasis plus the null projector on the kernel), evaluated at theta_0 = (0.3, 0.6). All
arithmetic is mpmath with 50 digits; the derivatives are mpmath central differences at high
precision (no float64 in the verdicts).
"""

import json
from pathlib import Path

import mpmath as mp

mp.mp.dps = 50
D = mp.mpf(1) / 2
G = D * mp.sqrt(1 - D**2)
C1, C2 = mp.mpf(1), mp.mpf("0.7")
THETA0 = (mp.mpf("0.3"), mp.mpf("0.6"))
DIRECTIONS = [(1, 0), (0, 1), (1, 1), (1, -2)]
TS = [mp.mpf("1e-3"), mp.mpf("1e-5"), mp.mpf("1e-7")]
OUT = Path(__file__).resolve().parent / "metrics" / "example2_zero_prob_limits_2026-10-21.json"


def phi(th):
    return C1 * th[0] + C2 * th[1]


def rho(th):
    t1 = th[0]
    s = 1 - t1
    f = s * G * mp.exp(1j * phi(th))
    return [
        [D**2 * s, 0, f],
        [0, t1, 0],
        [mp.conj(f), 0, (1 - D**2) * s],
    ]


def quad(vec, mat, vec2=None):
    """<vec | mat | vec2> for lists of mpc."""
    vec2 = vec if vec2 is None else vec2
    return sum(mp.conj(vec[i]) * mat[i][j] * vec2[j] for i in range(3) for j in range(3))


def basis_at_theta0():
    t1, _t2 = THETA0
    s0 = 1 - t1
    f0 = s0 * G * mp.exp(1j * phi(THETA0))
    psi = [D**2 * s0 / (D * s0), 0, mp.conj(f0) / (D * s0)]
    e1 = [0, 1, 0]
    y = [-f0 / (D * s0), 0, D**2 * s0 / (D * s0)]
    return psi, e1, y


def outer(v):
    return [[v[i] * mp.conj(v[j]) for j in range(3)] for i in range(3)]


def prob(proj, th):
    """p = tr(proj rho(th)) = Re <v|rho|v> for a rank-one projector given as outer product of v."""
    r = rho(th)
    return mp.re(sum(proj[j][i] * r[i][j] for i in range(3) for j in range(3)))


def dprob(proj, th, a):
    return mp.diff(lambda x: prob(proj, tuple(x if k == a else th[k] for k in range(2))), th[a])


def cfim_at(povm, th):
    """Classical Fisher matrix at th, summing over outcomes with p > 0 (null outcomes
    contribute iff p > 0)."""
    m = [[mp.mpf(0)] * 2 for _ in range(2)]
    for proj in povm:
        p = prob(proj, th)
        if p > 0:
            d = [dprob(proj, th, a) for a in range(2)]
            for a in range(2):
                for b in range(2):
                    m[a][b] += d[a] * d[b] / p
    return m


def drho_entries(th):
    """d_a rho as 3x3 mpc matrices, via central differences of the entries."""
    out = []
    for a in range(2):
        mat = [[None] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                mat[i][j] = mp.diff(
                    lambda x, i=i, j=j: rho(tuple(x if k == a else th[k] for k in range(2)))[i][j],
                    th[a],
                )
        out.append(mat)
    return out


def qfim_at(th, eigvecs, eigvals):
    """F^Q_ab = sum_{i,j, w_i + w_j > 0} 2 Re( (d_a rho)_{ij} conj((d_b rho)_{ij}) ) / (w_i + w_j)
    in the eigenbasis."""
    da = drho_entries(th)
    m = [[mp.mpf(0)] * 2 for _ in range(2)]
    proj = [[[mp.mpc(0)] * 3 for _ in range(3)] for _ in range(2)]
    for a in range(2):
        for i in range(3):
            for j in range(3):
                proj[a][i][j] = quad(eigvecs[i], da[a], eigvecs[j])
    for i in range(3):
        for j in range(3):
            s = eigvals[i] + eigvals[j]
            if s > 0:
                for a in range(2):
                    for b in range(2):
                        m[a][b] += 2 * mp.re(proj[a][i][j] * mp.conj(proj[b][i][j])) / s
    return m


def hellinger_form(povm, th0, h):
    """lim_{t->0} t^{-2} sum_k (sqrt p_k(th0+th) - sqrt p_k(th0))^2,
    evaluated at small t (quadratic-form estimate)."""
    vals = []
    for t in TS:
        th = tuple(th0[k] + t * h[k] for k in range(2))
        s = mp.mpf(0)
        for proj in povm:
            p0 = prob(proj, th0)
            p1 = prob(proj, th)
            s += (mp.sqrt(max(p1, 0)) - mp.sqrt(max(p0, 0))) ** 2
        vals.append(s / t**2)
    return vals


def main():
    psi, e1, y = basis_at_theta0()
    povm = [outer(psi), outer(e1), outer(y)]
    # sanity: completeness and orthonormality of the eigenbasis at theta_0
    total = [[sum(povm[k][i][j] for k in range(3)) for j in range(3)] for i in range(3)]
    complete = max(abs(total[i][j] - (1 if i == j else 0)) for i in range(3) for j in range(3))
    eigvecs = [psi, e1, y]
    eigvals = [1 - THETA0[0], THETA0[0], mp.mpf(0)]

    fq = qfim_at(THETA0, eigvecs, eigvals)
    f_pos = cfim_at(povm[:2], THETA0)  # regular outcomes only: the point CFIM
    null_prob_at_theta0 = prob(povm[2], THETA0)

    result = {
        "completeness_residual": float(complete),
        "p_null_at_theta0": mp.nstr(null_prob_at_theta0, 12),
        "F_Q": [[mp.nstr(fq[a][b], 12) for b in range(2)] for a in range(2)],
        "F_pos_point_CFIM": [[mp.nstr(f_pos[a][b], 12) for b in range(2)] for a in range(2)],
        "F_Q_minus_F_pos": [
            [mp.nstr(fq[a][b] - f_pos[a][b], 12) for b in range(2)] for a in range(2)
        ],
        "limits": [],
    }

    # Z2: closed form of the null probability along theta
    closed_form_err = []
    for h in DIRECTIONS:
        for t in TS:
            th = tuple(THETA0[k] + t * h[k] for k in range(2))
            s_prime = 1 - th[0]
            closed = 2 * s_prime * G**2 * (1 - mp.cos(phi(th) - phi(THETA0)))
            closed_form_err.append(float(abs(prob(povm[2], th) - closed)))
    result["Z2_closed_form_max_abs_error"] = max(closed_form_err)

    # Z3: direction-wise limit of the full CFIM (regular + null outcomes) at theta_0 + t h
    for h in DIRECTIONS:
        rows = []
        for t in TS:
            th = tuple(THETA0[k] + t * h[k] for k in range(2))
            m = cfim_at(povm, th)
            rows.append(
                {
                    "t": mp.nstr(t, 3),
                    "CFIM": [[mp.nstr(m[a][b], 12) for b in range(2)] for a in range(2)],
                    "max_abs_minus_F_Q": mp.nstr(
                        max(abs(m[a][b] - fq[a][b]) for a in range(2) for b in range(2)), 6
                    ),
                }
            )
        result["limits"].append({"h": list(h), "rows": rows})

    # Z4: Hellinger quadratic form versus QFIM / 4
    hel = []
    for h in DIRECTIONS:
        vals = hellinger_form(povm, THETA0, h)
        quad_fq = sum(h[a] * h[b] * fq[a][b] for a in range(2) for b in range(2)) / 4
        hel.append(
            {
                "h": list(h),
                "H_over_t2": [mp.nstr(v, 12) for v in vals],
                "F_Q_over_4_quadratic": mp.nstr(quad_fq, 12),
            }
        )
    result["Z4_hellinger"] = hel

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"WROTE {OUT}")


if __name__ == "__main__":
    main()
