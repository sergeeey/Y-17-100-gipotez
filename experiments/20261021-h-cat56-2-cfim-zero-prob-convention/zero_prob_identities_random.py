"""General identities for null outcomes (claims Z5-Z8 in claim.md), checked on random
rank-constant families.

Family: rho(theta) = V(theta) P V(theta)^dagger / tr(P V^dagger V),
V(theta) = [I_2; A(theta)], A(theta) = sum_a theta_a A_a, so rho(0) = diag(P, 0)
(quasi-pure at theta_0 = 0). Regular outcomes: |e_0><e_0|, |e_1><e_1|. Null outcomes:
|k_j><k_j| with k_j the kernel basis vectors at theta_0. The POVM sums to the identity.

Checks at theta_0 = 0 (two parameters):
  Z5: Hessian of p_E equals N_E / 2 for every null outcome E, where
      N_E,ab = Re tr(E L_a rho L_b), L_a the SLD.
  Z6: CFIM of a null outcome along theta_0 + t h tends to (N_E h)(N_E h)^T / (h^T N_E h).
  Z7: Hellinger quadratic form tends to (F_pos + sum_E N_E)[h,h] / 4.
  Z8: for a null outcome, N_E has rank one iff the kernel-support rows
      r_a = (L_a)_{k, 0:2} are real-proportional.

All arithmetic in mpmath at 40 digits; derivatives by mpmath numerical differentiation.
"""

import json
import random
from pathlib import Path

import mpmath as mp

mp.mp.dps = 40
OUT = Path(__file__).resolve().parent / "metrics" / "zero_prob_identities_2026-10-21.json"
KDIM = 3
D_TOT = 2 + KDIM
PVEC = [mp.mpf("0.6"), mp.mpf("0.4")]
TOL = mp.mpf("1e-25")


def rand_complex(rng):
    return mp.mpc(rng.gauss(0, 1), rng.gauss(0, 1))


def make_As(rng, mode):
    """Two KDIM x 2 coefficient matrices. 'generic': independent;
    'proportional': A_2 = 0.7 A_1 (rank-one N)."""
    a1 = mp.matrix(KDIM, 2)
    for r in range(KDIM):
        for c in range(2):
            a1[r, c] = rand_complex(rng)
    if mode == "proportional":
        a2 = a1 * mp.mpf("0.7")
    else:
        a2 = mp.matrix(KDIM, 2)
        for r in range(KDIM):
            for c in range(2):
                a2[r, c] = rand_complex(rng)
    return [a1, a2]


def rho_of(theta, As):
    A = mp.matrix(KDIM, 2)
    for a in range(2):
        A += theta[a] * As[a]
    V = mp.matrix(D_TOT, 2)
    V[0, 0] = 1
    V[1, 1] = 1
    for r in range(KDIM):
        for c in range(2):
            V[2 + r, c] = A[r, c]
    M = V.H * V
    denom = sum(PVEC[i] * M[i, i] for i in range(2))
    return (V * mp.diag(PVEC) * V.H) / denom


def unit(i):
    v = mp.matrix(D_TOT, 1)
    v[i] = 1
    return v


def p_of(theta, As, v):
    return mp.re((v.H * rho_of(theta, As) * v)[0, 0])


def hess_entry(As, v, a, b):
    order = [0, 0]
    order[a] += 1
    order[b] += 1
    return mp.diff(lambda x, y: p_of((x, y), As, v), (mp.mpf(0), mp.mpf(0)), tuple(order))


def grad_at(As, v, theta):
    out = []
    for a in range(2):
        out.append(
            mp.diff(
                lambda x, a=a: p_of(tuple(x if k == a else theta[k] for k in range(2)), As, v),
                theta[a],
            )
        )
    return out


def sld_and_N(As):
    """Return rho0 and the SLD matrices L_a at theta_0 = 0 (standard eigenbasis)."""
    rho0 = rho_of((0, 0), As)
    w = [PVEC[0], PVEC[1]] + [mp.mpf(0)] * KDIM
    drho = []
    for a in range(2):
        mat = mp.matrix(D_TOT, D_TOT)
        for i in range(D_TOT):
            for j in range(D_TOT):
                mat[i, j] = mp.diff(
                    lambda x, i=i, j=j, a=a: rho_of(
                        tuple(x if k == a else 0 for k in range(2)), As
                    )[i, j],
                    mp.mpf(0),
                )
        drho.append(mat)
    L = []
    for a in range(2):
        la = mp.matrix(D_TOT, D_TOT)
        for i in range(D_TOT):
            for j in range(D_TOT):
                s = w[i] + w[j]
                if s > 0:
                    la[i, j] = 2 * drho[a][i, j] / s
        L.append(la)
    return rho0, L


def run_seed(seed, mode):
    rng = random.Random(seed)
    As = make_As(rng, mode)
    rho0, L = sld_and_N(As)
    regular = [unit(0), unit(1)]
    null = [unit(2 + j) for j in range(KDIM)]

    # F_pos from regular outcomes at theta_0
    f_pos = mp.matrix(2, 2)
    for v in regular:
        p = p_of((0, 0), As, v)
        g = grad_at(As, v, (mp.mpf(0), mp.mpf(0)))
        for a in range(2):
            for b in range(2):
                f_pos[a, b] += g[a] * g[b] / p

    # N_E,ab = Re <v| L_a rho0 L_b |v>
    nulls = []
    for j, v in enumerate(null):
        N = mp.matrix(2, 2)
        for a in range(2):
            for b in range(2):
                N[a, b] = mp.re((v.H * (L[a] * rho0 * L[b]) * v)[0, 0])
        H = mp.matrix(2, 2)
        for a in range(2):
            for b in range(2):
                H[a, b] = hess_entry(As, v, a, b)
        # kernel-support rows r_a = (L_a)[k, 0:2] for k = 2+j
        rows = [[L[a][2 + j, 0], L[a][2 + j, 1]] for a in range(2)]
        nulls.append({"j": j, "v": v, "N": N, "H": H, "rows": rows})

    rep = {"seed": seed, "mode": mode, "Z5": [], "Z6": [], "Z7": [], "Z8": []}

    # Z5
    for nl in nulls:
        scale = max(abs(nl["N"][a, b]) for a in range(2) for b in range(2)) + TOL
        err = max(abs(nl["H"][a, b] - nl["N"][a, b] / 2) for a in range(2) for b in range(2))
        det = nl["N"][0, 0] * nl["N"][1, 1] - nl["N"][0, 1] * nl["N"][1, 0]
        rep["Z5"].append(
            {
                "null_index": nl["j"],
                "rel_error": mp.nstr(err / scale, 6),
                "N_rank": 1 if abs(det) / (scale**2) < mp.mpf("1e-20") else 2,
            }
        )

    # Z6 for each null outcome (both ranks, when h^T N h > 0)
    t = mp.mpf("1e-12")
    for nl in nulls:
        N = nl["N"]
        for h in [(1, 0), (0, 1), (1, 1), (1, -2)]:
            hv = mp.matrix([h[0], h[1]])
            hNh = (hv.T * N * hv)[0, 0]
            if hNh <= TOL:
                continue
            Nh = N * hv
            pred = Nh * Nh.T / hNh
            theta = (t * h[0], t * h[1])
            g = grad_at(As, nl["v"], theta)
            p = p_of(theta, As, nl["v"])
            cf = mp.matrix(2, 2)
            for a in range(2):
                for b in range(2):
                    cf[a, b] = g[a] * g[b] / p
            scale = max(abs(pred[a, b]) for a in range(2) for b in range(2))
            err = max(abs(cf[a, b] - pred[a, b]) for a in range(2) for b in range(2))
            rep["Z6"].append(
                {"null_index": nl["j"], "h": list(h), "rel_error": mp.nstr(err / scale, 6)}
            )

    # Z7
    f_tot = f_pos + sum((nl["N"] for nl in nulls), mp.matrix(2, 2))
    for h in [(1, 0), (0, 1), (1, 1), (1, -2)]:
        hv = mp.matrix([h[0], h[1]])
        pred = (hv.T * f_tot * hv)[0, 0] / 4
        theta = (t * h[0], t * h[1])
        hel = mp.mpf(0)
        for v in regular + [nl["v"] for nl in nulls]:
            p0 = p_of((0, 0), As, v)
            p1 = p_of(theta, As, v)
            hel += (mp.sqrt(max(p1, 0)) - mp.sqrt(max(p0, 0))) ** 2
        val = hel / t**2
        rep["Z7"].append({"h": list(h), "rel_error": mp.nstr(abs(val - pred) / abs(pred), 6)})

    # Z8: rank-one N_E versus real-proportional kernel-support rows
    for nl in nulls:
        r0, r1 = nl["rows"][0], nl["rows"][1]
        m = 0 if abs(r1[0]) > abs(r1[1]) else 1
        c = r0[m] / r1[m]
        prop_real = abs(mp.im(c)) < mp.mpf("1e-20") and max(
            abs(r0[k] - c * r1[k]) for k in range(2)
        ) < mp.mpf("1e-20")
        rank1 = next(x for x in rep["Z5"] if x["null_index"] == nl["j"])["N_rank"] == 1
        rep["Z8"].append(
            {
                "null_index": nl["j"],
                "rank_one_N": rank1,
                "real_proportional_rows": bool(prop_real),
                "agree": rank1 == bool(prop_real),
            }
        )
    return rep


def main():
    out = []
    for mode in ["generic", "proportional"]:
        for seed in [1, 2, 3]:
            rep = run_seed(seed, mode)
            out.append(rep)
            worst5 = max(float(x["rel_error"]) for x in rep["Z5"])
            worst6 = max(float(x["rel_error"]) for x in rep["Z6"]) if rep["Z6"] else None
            worst7 = max(float(x["rel_error"]) for x in rep["Z7"])
            print(
                f"mode={mode} seed={seed}: Z5 max rel {worst5:.2e}; "
                f"Z6 max rel {worst6}; Z7 max rel {worst7:.2e}"
            )
            print(
                "  N ranks:",
                [x["N_rank"] for x in rep["Z5"]],
                " Z8 agree:",
                [x["agree"] for x in rep["Z8"]],
            )
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, default=str, ensure_ascii=False), encoding="utf-8")
    print(f"WROTE {OUT}")


if __name__ == "__main__":
    main()
