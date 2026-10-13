"""Symmetry-approach necessary condition: look for a higher symmetry G of u_t=F by linear algebra
over a polynomial ansatz.  Condition (evolutionary flows commute):
    [F,G]^xi = D_F(G^xi) - sum_{zeta,l} S^l(G^zeta) dF^xi/du^zeta_l = 0 ,
D_F(f) = sum_{l,zeta} S^l(F^zeta) df/du^zeta_l.
Linear in the unknown coefficients of G.  Rank decided by SVD (floats); every reported symmetry is
then re-verified EXACTLY (rational reconstruction + sympy expand)."""

import itertools, json, sys, time
import numpy as np
import sympy as sp
from fractions import Fraction

sys.path.insert(0, __file__.rsplit("src", 1)[0] + "src")
from ddlax import mk, parse, S


def run(
    name, F, fams, lo, hi, weights, target_w, maxdeg, mindeg=1, extra_filter=None, seed_syms=None
):
    """F: dict fam->expr. fams: ordered list. window [lo,hi]. weights: fam->int weight per variable.
    target_w: fam -> required weight of G^fam (None = any; uses weights as charge)."""
    t0 = time.time()
    vars_ = [(f, i) for f in fams for i in range(lo, hi + 1)]
    syms = {fv: mk(*fv) for fv in vars_}
    # all generators needed: window enlarged by F stencil
    flat = [mk(f, i) for f in fams for i in range(lo - 3, hi + 4)]
    gens = flat
    basis = []  # (comp, monomial-expr)
    for comp in fams:
        for d in range(mindeg, maxdeg + 1):
            for combo in itertools.combinations_with_replacement(vars_, d):
                w = sum(weights[f] for f, _ in combo)
                if w != target_w[comp]:
                    continue
                if extra_filter and not extra_filter(comp, combo):
                    continue
                m = sp.Integer(1)
                for fv in combo:
                    m *= syms[fv]
                basis.append((comp, m))
    print(
        f"[{name}] ansatz size = {len(basis)} unknown coefficients; vars={len(vars_)}", flush=True
    )

    # F-derivative data
    SF = {}  # (fam,l) -> Poly(S^l F^fam)

    def SFp(fam, l):
        if (fam, l) not in SF:
            SF[(fam, l)] = sp.Poly(S(F[fam], l), *gens, domain="QQ")
        return SF[(fam, l)]

    dF = {}  # (xi, zeta, l) -> expr dF^xi/du^zeta_l
    for xi in fams:
        for s in F[xi].free_symbols:
            p = parse(s)
            if p and p[0] in fams:
                dF[(xi, p[0], p[1])] = sp.diff(F[xi], s)

    rows = {}
    for col, (comp, m) in enumerate(basis):
        # D_F(m) in component comp
        tot = sp.Poly(0, *gens, domain="QQ")
        for s in m.free_symbols:
            p = parse(s)
            dm = sp.Poly(sp.diff(m, s), *gens, domain="QQ")
            tot = tot + SFp(p[0], p[1]) * dm
        for mon, cf in tot.terms():
            rows.setdefault((comp, mon), {})
            rows[(comp, mon)][col] = rows[(comp, mon)].get(col, 0) + cf
        # - sum_l S^l(m) dF^xi/du^comp_l
        for (xi, zeta, l), dexpr in dF.items():
            if zeta != comp:
                continue
            pr = sp.Poly(S(m, l) * dexpr, *gens, domain="QQ")
            for mon, cf in pr.terms():
                rows.setdefault((xi, mon), {})
                rows[(xi, mon)][col] = rows[(xi, mon)].get(col, 0) - cf
    keys = list(rows.keys())
    A = np.zeros((len(keys), len(basis)))
    for r, k in enumerate(keys):
        for col, cf in rows[k].items():
            A[r, col] = float(cf)
    print(f"[{name}] matrix {A.shape}, built in {time.time() - t0:.1f}s", flush=True)
    # reduce: SVD on A^T A (cols x cols) for speed
    sv = np.linalg.svd(A, compute_uv=False)
    smax = sv[0]
    tol = 1e-8 * smax
    nullity = int(len(basis) - np.sum(sv > tol))
    print(
        f"[{name}] nullity = {nullity}; smallest singular values near gap: "
        f"{[f'{x:.2e}' for x in sorted(sv)[: max(0, 0)]]} | sv just above tol: "
        f"{[f'{x:.2e}' for x in sv[sv > tol][-3:]]} | sv below tol (max 5): {[f'{x:.1e}' for x in sv[sv <= tol][:5]]}",
        flush=True,
    )
    U_, s_, Vt = np.linalg.svd(A, full_matrices=True)
    N = Vt[np.sum(s_ > tol) :].T  # cols = nullspace basis (basis-size x nullity)
    # rational reconstruction via RREF of N^T
    Mx = N.T.copy()
    piv = []
    r = 0
    for cc in range(Mx.shape[1]):
        if r >= Mx.shape[0]:
            break
        pr_ = np.argmax(np.abs(Mx[r:, cc])) + r
        if abs(Mx[pr_, cc]) < 1e-7:
            continue
        Mx[[r, pr_]] = Mx[[pr_, r]]
        Mx[r] /= Mx[r, cc]
        for r2 in range(Mx.shape[0]):
            if r2 != r:
                Mx[r2] -= Mx[r2, cc] * Mx[r]
        piv.append(cc)
        r += 1
    syms_by_comp = {f: sp.Integer(0) for f in fams}
    sols = []
    for rr in range(Mx.shape[0]):
        G = {f: sp.Integer(0) for f in fams}
        for cc in range(Mx.shape[1]):
            if abs(Mx[rr, cc]) > 1e-7:
                fr = Fraction(Mx[rr, cc]).limit_denominator(2000)
                comp, m = basis[cc]
                G[comp] += sp.Rational(fr.numerator, fr.denominator) * m
        sols.append(G)
    # exact verification
    verified = []
    for G in sols:
        ok = True
        for xi in fams:
            DF = 0
            for s in G[xi].free_symbols:
                p = parse(s)
                DF += S(F[p[0]], p[1]) * sp.diff(G[xi], s)
            DG = 0
            for (xi2, zeta, l), dexpr in dF.items():
                if xi2 == xi:
                    DG += S(G[zeta], l) * dexpr
            if sp.expand(DF - DG) != 0:
                ok = False
        verified.append(ok)
    res = dict(
        name=name,
        ansatz=len(basis),
        matrix=list(A.shape),
        nullity=nullity,
        exact_verified=verified,
        solutions=[{f: str(G[f]) for f in fams} for G in sols],
    )
    # span of stencil per solution
    for k, G in enumerate(sols):
        idxs = [parse(s)[1] for f in fams for s in G[f].free_symbols]
        print(
            f"[{name}] sol#{k}: exact_verified={verified[k]}, stencil span = [{min(idxs)},{max(idxs)}], "
            f"#terms = {[len(sp.Add.make_args(G[f])) for f in fams]}",
            flush=True,
        )
    return res, sols, basis


if __name__ == "__main__":
    pass
