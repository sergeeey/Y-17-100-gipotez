"""Algebraic side of arXiv:2508.02321 (Carmona, Fernandez-Sanchez, Novaes): coefficients m_i,n_i (eq.9, Remark 4),
F~,G~ (eq.13), resultant R(Y1)=Res_{Y0}(F~,G~), discriminant Delta_b (Remark 6).
Everything is written for the Lienard canonical form (5)/(6); exact (sympy) and numeric (numpy) versions."""

from __future__ import annotations

import numpy as np
import sympy as sp


def mn_coeffs(TL, DL, aL, TR, DR, aR, b):
    m0 = aL**2 * (aR**2 * b + b**3 * DR + aR * b**2 * TR)
    m1 = -(aL**2) * b * (2 * b * DR + aR * TR)
    m2 = (
        -(aR**2) * (b * DL + aL * TL)
        + b * DR * (3 * aL**2 - b**2 * DL + aL * b * TL)
        + aR * (aL**2 - b**2 * DL) * TR
    )
    m3 = aL**2 * b * DR
    m4 = aR**2 * DL - DR * (aL**2 - b**2 * DL + aL * b * TL) + aR * b * DL * TR
    m5 = aL * DR * TL - aR * DL * TR - b * DL * DR
    n1 = aL**4 * b * (2 * b * DR + aR * TR)
    n2 = -2 * aL**3 * b * (2 * aL * DR + 2 * b * DR * TL + aR * TL * TR)
    n3 = aL**2 * (
        aR**2 * (b * DL + aL * TL)
        + b * DR * (-3 * aL**2 + b**2 * DL - aL * b * TL)
        + aR * (-(aL**2) * TR + b**2 * DL * TR)
    )
    n4 = aL * (
        2 * aL**3 * DR
        + aL**2 * TL * (7 * b * DR + aR * TR)
        - b * DL * TL * (aR**2 + b**2 * DR + aR * b * TR)
        - aL * (-(b**2) * DR * TL**2 + aR**2 * (2 * DL + TL**2) + aR * b * DL * TR)
    )
    n5 = aL**2 * (-(aR**2) * DL + DR * (aL**2 - b**2 * DL + aL * b * TL) - aR * b * DL * TR)
    n6 = 2 * (
        aR**2 * DL * (b * DL + 3 * aL * TL)
        + DR
        * (b**3 * DL**2 - 2 * aL**3 * TL + aL * b**2 * DL * TL - aL**2 * b * (3 * DL + 2 * TL**2))
        + aR * DL * (-(aL**2) + b**2 * DL + 2 * aL * b * TL) * TR
    )
    n7 = aL * (
        aR**2 * DL * TL
        + DR * TL * (-3 * aL**2 + b**2 * DL - aL * b * TL)
        + aR * DL * (2 * aL + b * TL) * TR
    )
    n8 = (
        -3 * aR**2 * DL**2
        + DR * (-3 * b**2 * DL**2 + aL * b * DL * TL + aL**2 * (3 * DL + 2 * TL**2))
        - aR * DL * (3 * b * DL + 2 * aL * TL) * TR
    )
    n9 = 4 * DL * (b * DL * DR - aL * DR * TL + aR * DL * TR)
    return (m0, m1, m2, m3, m4, m5), (n1, n2, n3, n4, n5, n6, n7, n8, n9)


def FG_tilde(Y0, Y1, p):
    (m0, m1, m2, m3, m4, m5), (n1, n2, n3, n4, n5, n6, n7, n8, n9) = mn_coeffs(*p)
    F = m0 + m1 * Y0 + (m2 - 2 * m3) * Y1 + m3 * Y0**2 + m4 * Y0 * Y1 + m5 * Y1**2
    G = (
        n1 * Y0
        + (n2 - 2 * n3) * Y1
        + n3 * Y0**2
        + (n4 - 3 * n5) * Y0 * Y1
        + (n6 - 2 * n7) * Y1**2
        + n5 * Y0**3
        + n7 * Y0**2 * Y1
        + n8 * Y0 * Y1**2
        + n9 * Y1**3
    )
    return F, G


def exact_resultant(p):
    """p = tuple of sympy Rationals (TL,DL,aL,TR,DR,aR,b).  Returns (R as sympy poly in Y1, F, G)."""
    Y0, Y1 = sp.symbols("Y0 Y1")
    F, G = FG_tilde(Y0, Y1, p)
    R = sp.Poly(sp.resultant(sp.expand(F), sp.expand(G), Y0), Y1)
    return R, sp.expand(F), sp.expand(G)


def delta_b(TL, DL, aL, TR, DR, aR, b):
    return (
        DR * (aL**2 - aL * b * TL + b**2 * DL) + aR**2 * DL + aR * b * DL * TR
    ) ** 2 - 4 * aL**2 * aR**2 * DL * DR


def resultant_numeric(p):
    """Numeric R(Y1) coefficients (highest degree first) via evaluation/interpolation of the 5x5 Sylvester determinant
    (F~ quadratic, G~ cubic in Y0).  Degree <= 6.  Returns np.array of 7 coefficients (may have tiny leading terms)."""
    (m0, m1, m2, m3, m4, m5), (n1, n2, n3, n4, n5, n6, n7, n8, n9) = mn_coeffs(*p)

    def sylv(y):
        f = [m3, m1 + m4 * y, m0 + (m2 - 2 * m3) * y + m5 * y * y]  # F~ in Y0: f0 Y0^2+f1 Y0+f2
        g = [
            n5,
            n3 + n7 * y,
            n1 + (n4 - 3 * n5) * y + n8 * y * y,
            (n2 - 2 * n3) * y + (n6 - 2 * n7) * y * y + n9 * y**3,
        ]  # G~ in Y0
        M = np.zeros((5, 5))
        for r in range(3):  # 3 rows of F (deg G =3)
            M[r, r : r + 3] = f
        for r in range(2):  # 2 rows of G (deg F =2)
            M[3 + r, r : r + 4] = g
        return np.linalg.det(M)

    # scale the variable to keep the Vandermonde well conditioned
    sc = max(1.0, abs(m5) ** 0 * 1.0)
    ys = np.cos(np.pi * (np.arange(13) + 0.5) / 13) * 3.0
    vals = np.array([sylv(y) for y in ys])
    coef = np.polyfit(ys, vals, 6)
    return coef


def k_negative_roots(p, tol=1e-9):
    """number of real roots of R(Y1) with Y1 <= 0 (the 'k' of Thm 6), plus leading coefficient info."""
    c = resultant_numeric(p)
    scale = np.max(np.abs(c))
    if scale == 0 or not np.isfinite(scale):
        return None, c
    cn = c / scale
    # drop numerically-zero leading terms
    nz = np.nonzero(np.abs(cn) > 1e-13)[0]
    if len(nz) == 0:
        return None, c
    cn = cn[nz[0] :]
    r = np.roots(cn)
    real = r[np.abs(r.imag) < tol * (1 + np.abs(r.real))].real
    return int(np.sum(real <= 0)), dict(deg=len(cn) - 1, lead=float(c[0] / scale), roots=r)
