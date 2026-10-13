"""C2 check: do my transcribed m_i,n_i reproduce the paper's exact HY resultant R(Y1) = -C3 (200 Y1 - 117)(quintic) and k=1?
Also independently re-derive G~ from F and W_L (G_b = <grad F_b, X_L>) as a transcription-error check on n_i."""

import json

import numpy as np
import sympy as sp

from controls_def import FPTT_CANON, GRS_CANON, HY_CANON
from lc2_theory import FG_tilde, delta_b, exact_resultant, k_negative_roots, mn_coeffs

out = {}
Y0, Y1, y0, y1 = sp.symbols("Y0 Y1 y0 y1")
for name, d in [("HY", HY_CANON), ("FPTT21", FPTT_CANON), ("GRS", GRS_CANON)]:
    p = tuple(
        sp.Rational(d[k].numerator, d[k].denominator)
        for k in ("TL", "DL", "aL", "TR", "DR", "aR", "b")
    )
    TL, DL, aL, TR, DR, aR, b = p
    # --- independent derivation of G from F and the cubic vector field
    (m0, m1, m2, m3, m4, m5), _ = mn_coeffs(*p)
    Fb = (
        m0
        + m1 * (y0 + y1)
        + m2 * y0 * y1
        + m3 * (y0**2 + y1**2)
        + m4 * (y0 * y1**2 + y0**2 * y1)
        + m5 * y0**2 * y1**2
    )
    WL = lambda y: DL * y**2 - aL * TL * y + aL**2
    XL = (-y1 * WL(y0), -y0 * WL(y1))
    Gb = sp.expand(sp.diff(Fb, y0) * XL[0] + sp.diff(Fb, y1) * XL[1])
    # substitute symmetric reduction: express in (Y0,Y1)=(y0+y1,y0 y1) by comparing with the paper's G~ after phi
    Ft, Gt = FG_tilde(Y0, Y1, p)
    Gt_back = sp.expand(Gt.subs({Y0: y0 + y1, Y1: y0 * y1}))
    ratio_ok = sp.simplify(Gb - Gt_back) == 0
    # F~ vs F
    Ft_back = sp.expand(Ft.subs({Y0: y0 + y1, Y1: y0 * y1}))
    F_ok = sp.simplify(sp.expand(Fb) - Ft_back) == 0
    R, F, G = exact_resultant(p)
    rr = sp.Poly(R, Y1)
    roots = sp.Poly(rr, Y1).nroots(n=30, maxsteps=200)
    neg = [r for r in roots if abs(sp.im(r)) < 1e-20 and sp.re(r) <= 0]
    Dl = sp.nsimplify(delta_b(*p))
    ncoef, info = k_negative_roots(tuple(float(v) for v in p))
    out[name] = dict(
        G_matches_grad_F_dot_XL=bool(ratio_ok),
        F_matches=bool(F_ok),
        deg=rr.degree(),
        lead_nonzero=bool(rr.LC() != 0),
        n_nonpositive_real_roots_exact=len(neg),
        neg_roots=[str(sp.N(r, 12)) for r in neg],
        Delta_b=str(sp.N(Dl, 12)),
        k_numeric=ncoef,
        deg_numeric=info["deg"] if isinstance(info, dict) else None,
    )
    # factor check for HY: (200 Y1 - 117) divides R
    if name == "HY":
        out[name]["factor_200Y1_minus_117_divides_R"] = bool(
            sp.rem(rr, sp.Poly(200 * Y1 - 117, Y1)) == 0 or rr.eval(sp.Rational(117, 200)) == 0
        )
    print(name, out[name], flush=True)
json.dump(out, open("check_theory.json", "w"), indent=1, default=str)
