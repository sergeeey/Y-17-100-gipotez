"""Test T (Schur-complement closure), walk/spectral dimension estimates. Gasket control through the same code."""

import json
import os

import numpy as np

from lib import *

OUT = {}


def schur_closure(A_f, D_f_deg, coarse_idx, A_c, nu, extra=None):
    """Schur complement of (L1 - nu*D) of the fine graph onto the coarse vertex set, then least-squares fit
    in span{A_c, D_c, I (+extra)} with D_c the coarse-graph degrees. Returns (relative residual, coeffs)."""
    N = A_f.shape[0]
    Lf = (sp.diags(D_f_deg) - A_f).toarray() - nu * np.diag(D_f_deg)
    c = np.asarray(coarse_idx)
    mask = np.zeros(N, bool)
    mask[c] = True
    I_idx = np.nonzero(~mask)[0]
    Lcc = Lf[np.ix_(c, c)]
    Lci = Lf[np.ix_(c, I_idx)]
    Lii = Lf[np.ix_(I_idx, I_idx)]
    S = Lcc - Lci @ np.linalg.solve(Lii, Lci.T)
    S = (S + S.T) / 2
    Ac = A_c.toarray()
    Dc = np.diag(Ac.sum(axis=1))
    basis = [Ac, Dc, np.eye(len(c))] + ([e for e in extra] if extra else [])
    M = np.stack([b.ravel() for b in basis], axis=1)
    coef, *_ = np.linalg.lstsq(M, S.ravel(), rcond=None)
    res = np.linalg.norm(M @ coef - S.ravel()) / np.linalg.norm(S.ravel())
    return float(res), [float(x) for x in coef], S


def gasket_pair(n):
    Af, vf = gasket_graph(n + 1)
    Ac, vc = gasket_graph(n)
    key = {tuple(v): i for i, v in enumerate(vf)}
    cidx = [key[(2 * a, 2 * b)] for (a, b) in vc]
    return Af, cidx, Ac


def carpet_pair(n):
    Af, xyf = carpet_graph(n + 1)
    Ac, xyc = carpet_graph(n)
    key = {(int(x), int(y)): i for i, (x, y) in enumerate(xyf)}
    cidx = [key[(3 * int(x), 3 * int(y))] for x, y in xyc]
    # in-cell diagonal adjacency of the coarse graph: (x,y)~(x+1,y+1) and (x,y)~(x+1,y-1) when the cell is retained
    kc = {(int(x), int(y)): i for i, (x, y) in enumerate(xyc)}
    cells = carpet_cells(n)
    r, cc, v = [], [], []
    for yy in range(cells.shape[0]):
        for xx in range(cells.shape[1]):
            if cells[yy, xx]:
                for p, q in (((xx, yy), (xx + 1, yy + 1)), ((xx + 1, yy), (xx, yy + 1))):
                    i, j = kc[p], kc[q]
                    r += [i, j]
                    cc += [j, i]
                    v += [1.0, 1.0]
    Adiag = sp.csr_matrix((v, (r, cc)), shape=(len(kc), len(kc))).toarray()
    return Af, cidx, Ac, Adiag


def run_T():
    for n in (2, 3):
        Af, cidx, Ac = gasket_pair(n)
        deg = np.asarray(Af.sum(axis=1)).ravel()
        for nu in (0.0, 0.05, 0.15):
            res, coef, _ = schur_closure(Af, deg, cidx, Ac, nu)
            OUT[f"T_gasket_{n}to{n + 1}_nu{nu}"] = {"F3_resid": res, "coef(A,D,I)": coef}
            print(
                f"[T gasket {n}->{n + 1}] nu={nu}: span{{A,D,I}} residual {res:.2e} coef {np.round(coef, 5)}",
                flush=True,
            )
    for n in (2, 3):
        Af, cidx, Ac, Adiag = carpet_pair(n)
        deg = np.asarray(Af.sum(axis=1)).ravel()
        for nu in (0.0, 0.05, 0.15):
            res3, coef3, _ = schur_closure(Af, deg, cidx, Ac, nu)
            res4, coef4, _ = schur_closure(Af, deg, cidx, Ac, nu, extra=[Adiag])
            OUT[f"T_carpet_{n}to{n + 1}_nu{nu}"] = {
                "F3_resid": res3,
                "F4_resid": res4,
                "coef3": coef3,
                "coef4": coef4,
            }
            print(
                f"[T carpet {n}->{n + 1}] nu={nu}: F3 span{{A,D,I}} residual {res3:.3e}; F4 (+in-cell diagonals) residual {res4:.3e} coef4 {np.round(coef4, 5)}",
                flush=True,
            )


def kth_nonzero(ev, k):
    e = np.sort(ev)
    e = e[e > 1e-9]
    return e[k - 1]


def weyl_slope(ev, Nlo=30, frac_hi=0.15):
    e = np.sort(ev)
    e = e[e > 1e-9]
    Nhi = int(frac_hi * len(e))
    k = np.arange(1, len(e) + 1)
    sel = slice(Nlo - 1, Nhi)
    p = np.polyfit(np.log(e[sel]), np.log(k[sel]), 1)
    return float(2 * p[0])  # d_s = 2 * slope


def run_dims():
    G = np.load("gasket_4L2_spectra.npz")
    for n in range(3, 7):
        ratios = [kth_nonzero(G[f"L{n}"], k) / kth_nonzero(G[f"L{n + 1}"], k) for k in range(1, 7)]
        print(
            f"[dim gasket 4L2] level {n}->{n + 1}: lambda_k ratios k=1..6 {np.round(ratios, 4)}",
            flush=True,
        )
    for n in (5, 6, 7):
        print(
            f"[dim gasket 4L2] level {n}: Weyl d_s (window N in [30,0.15V]) = {weyl_slope(G[f'L{n}']):.3f}  (2 ln3/ln5 = {2 * np.log(3) / np.log(5):.3f})",
            flush=True,
        )
    for kind in ("L1", "L2"):
        S = dict(np.load(f"carpet_spectra_{kind}.npz"))
        if os.path.exists(f"carpet_spectra_{kind}_n5.npz"):
            S.update(dict(np.load(f"carpet_spectra_{kind}_n5.npz")))
        lv = sorted(int(k[1:]) for k in S)
        for n in lv:
            if f"n{n + 1}" in S:
                ratios = [
                    kth_nonzero(S[f"n{n}"], k) / kth_nonzero(S[f"n{n + 1}"], k) for k in range(1, 7)
                ]
                r1 = ratios[0]
                dw = [np.log(r) / np.log(3) for r in ratios]
                ds = [2 * np.log(8) / np.log(r) for r in ratios]
                print(
                    f"[dim carpet {kind}] level {n}->{n + 1}: ratios(k=1..6) {np.round(ratios, 4)}  d_w=ln(r)/ln3 {np.round(dw, 4)}  d_s=2ln8/ln r {np.round(ds, 4)}",
                    flush=True,
                )
                OUT[f"dim_{kind}_{n}to{n + 1}"] = {"ratios": [float(x) for x in ratios]}
        for n in lv:
            if n >= 3:
                print(
                    f"[dim carpet {kind}] level {n}: Weyl d_s (N in [30,0.15V]) = {weyl_slope(S[f'n{n}']):.3f}",
                    flush=True,
                )
                OUT[f"weyl_{kind}_{n}"] = weyl_slope(S[f"n{n}"])


if __name__ == "__main__":
    run_dims()
    run_T()
    json.dump(OUT, open("analysis_more.json", "w"), indent=1, default=float)
