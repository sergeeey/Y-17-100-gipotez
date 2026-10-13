"""Fast closed-form half-return maps for planar 2-zone piecewise-linear (Filippov)
systems with straight switching line x=0.

    x>0 (zone R):  z' = A_R z + b_R
    x<0 (zone L):  z' = A_L z + b_L          z=(x,y)

Both zones must be linear FOCI (tr^2 < 4 det). In each zone
    z(t) = z_e + e^{tau t} [cos(w t) I + sin(w t)/w (A - tau I)] (z0 - z_e),
    tau=tr/2, w=sqrt(det - tau^2), z_e = -A^{-1} b.
First return time to x=0 = first zero of x(t) after the start; found by a sign scan on a
fixed grid in s=w t (log-spaced near 0, then uniform) followed by vectorised bisection.

Crossing cycle (2 crossings per period): (0,y0) --R arc--> (0,y1) --L arc--> (0,y2); cycle iff
y2=y0.  G(y0)=y2-y0.  Entry conditions (transversality) are enforced: the arc into zone s
must start with s*x'(0,y)>0.

Domain caveat: points where the arc would start tangentially or never return are NaN.
"""

from __future__ import annotations

import numpy as np

S_MAX = 4.0 * np.pi
NOISE_TOL = 1e-11  # |G| below this (relative to 1+|y|) at a sign change is flagged as suspect
_S = np.unique(np.concatenate([np.logspace(-7, -2, 30), np.arange(0.01, S_MAX + 0.004, 0.004)]))


class Zone:
    def __init__(self, A, b):
        A = np.asarray(A, float)
        b = np.asarray(b, float)
        self.A, self.b = A, b
        tr = A[0, 0] + A[1, 1]
        det = A[0, 0] * A[1, 1] - A[0, 1] * A[1, 0]
        self.tau = tr / 2.0
        w2 = det - self.tau**2
        if not (w2 > 0):
            raise ValueError("zone is not a focus")
        self.w = float(np.sqrt(w2))
        self.ze = -np.linalg.solve(A, b)
        self.a11, self.a12, self.a21, self.a22 = A[0, 0], A[0, 1], A[1, 0], A[1, 1]
        self.b1 = b[0]
        self.k = self.tau / self.w  # exponent per unit s

    def xdot0(self, y):
        """x-component of the field on the line x=0."""
        return self.a12 * y + self.b1

    def _coef(self, y0):
        u0x = -self.ze[0]
        u0y = np.asarray(y0, float) - self.ze[1]
        K1 = (self.a11 - self.tau) * u0x + self.a12 * u0y
        K2 = self.a21 * u0x + (self.a22 - self.tau) * u0y
        return u0x, u0y, K1, K2

    def _terms(self, s):
        """cancellation-free pieces of e^{At}-I as functions of s=w t."""
        ek = np.exp(self.k * s)
        em1 = np.expm1(self.k * s)
        c = np.cos(s)
        sn = np.sin(s)
        hs2 = np.sin(0.5 * s) ** 2
        esw = ek * sn / self.w
        E11m1 = em1 * c - 2.0 * hs2 + esw * (self.a11 - self.tau)
        E22m1 = em1 * c - 2.0 * hs2 + esw * (self.a22 - self.tau)
        return esw, E11m1, E22m1

    def x_of_s(self, s, u0y):
        """x(t) on the arc started at (0,y0) with u0y=y0-ze_y; x(0)=0 exactly."""
        esw, E11m1, _ = self._terms(s)
        return -self.ze[0] * E11m1 + self.a12 * esw * u0y

    def dy_of_s(self, s, u0y):
        esw, _, E22m1 = self._terms(s)
        return E22m1 * u0y - self.a21 * esw * self.ze[0]

    def half_return(self, side, y0, chunk=400, nbis=64):
        """side=+1: arc in x>0; side=-1: arc in x<0.  Returns (y1, t) with NaN where the
        start is not transversal-into-the-zone or no return within S_MAX/w time."""
        y0 = np.atleast_1d(np.asarray(y0, float))
        n = y0.size
        y1 = np.full(n, np.nan)
        tt = np.full(n, np.nan)
        valid = side * self.xdot0(y0) > 0
        idx = np.nonzero(valid & np.isfinite(y0))[0]
        esw_g, E11m1_g, _ = self._terms(_S)
        for a in range(0, idx.size, chunk):
            ii = idx[a : a + chunk]
            u0y = y0[ii] - self.ze[1]
            X = -self.ze[0] * E11m1_g[None, :] + self.a12 * u0y[:, None] * esw_g[None, :]
            neg = side * X <= 0
            has = neg.any(axis=1)
            j = np.argmax(neg, axis=1)
            if not has.any():
                continue
            r = np.nonzero(has)[0]
            jr = j[r]
            hi = _S[jr]
            lo = np.where(jr > 0, _S[np.maximum(jr - 1, 0)], 0.0)
            u0yr = u0y[r]
            for _ in range(nbis):
                mid = 0.5 * (lo + hi)
                xm = side * self.x_of_s(mid, u0yr)
                pos = xm > 0
                lo = np.where(pos, mid, lo)
                hi = np.where(pos, hi, mid)
            s = 0.5 * (lo + hi)
            y1[ii[r]] = y0[ii[r]] + self.dy_of_s(s, u0yr)
            tt[ii[r]] = s / self.w
        return y1, tt


def compose(zR: Zone, zL: Zone, y0):
    """y0 -> (y1, y2, tR, tL) for the cycle y0 --R--> y1 --L--> y2."""
    y1, tR = zR.half_return(+1, y0)
    y2 = np.full_like(y1, np.nan)
    tL = np.full_like(y1, np.nan)
    m = np.isfinite(y1)
    if m.any():
        y2m, tLm = zL.half_return(-1, y1[m])
        y2[m] = y2m
        tL[m] = tLm
    return y1, y2, tR, tL


def G(zR: Zone, zL: Zone, y0):
    y1, y2, _, _ = compose(zR, zL, y0)
    return y2 - np.asarray(y0, float)


def y_grid(zR: Zone, n=6000, dmin=1e-6, dmax=200.0):
    """Grid of y0 values with R-entry (x'_R(0,y0)>0), log-spaced in distance from the fold."""
    if zR.a12 == 0:
        raise ValueError("degenerate")
    yf = -zR.b1 / zR.a12
    d = np.logspace(np.log10(dmin), np.log10(dmax), n)
    # xdot0 = a12*(y - yf); >0 for y>yf if a12>0 else y<yf
    return yf + (d if zR.a12 > 0 else -d)


def count_cycles(zR: Zone, zL: Zone, n=6000, dmin=1e-6, dmax=200.0, refine=True):
    """Count simple sign changes of G on the grid.  Returns dict with roots (y0,y1,tR,tL),
    stability, and diagnostics (gap-ambiguities)."""
    yg = y_grid(zR, n, dmin, dmax)
    g = G(zR, zL, yg)
    fin = np.isfinite(g)
    br = []
    amb = 0
    suspect = 0
    last = None
    for i in range(n):
        if not fin[i]:
            continue
        if last is not None:
            if i == last + 1:
                if g[last] == 0.0:
                    br.append((yg[last], yg[last]))
                elif g[last] * g[i] < 0:
                    tol = NOISE_TOL * (1.0 + abs(yg[i]))
                    if min(abs(g[last]), abs(g[i])) < tol:
                        suspect += 1
                    else:
                        br.append((yg[last], yg[i]))
            else:
                if g[last] * g[i] < 0:
                    amb += 1
        last = i
    roots = []
    if refine and br:
        lo = np.array([b[0] for b in br])
        hi = np.array([b[1] for b in br])
        glo = G(zR, zL, lo)
        for _ in range(70):
            mid = 0.5 * (lo + hi)
            gm = G(zR, zL, mid)
            bad = ~np.isfinite(gm)
            same = gm * glo > 0
            lo = np.where(same & ~bad, mid, lo)
            glo = np.where(same & ~bad, gm, glo)
            hi = np.where(~same & ~bad, mid, hi)
        ym = 0.5 * (lo + hi)
        y1, y2, tR, tL = compose(zR, zL, ym)
        h = 1e-6 * np.maximum(1.0, np.abs(ym))
        dG = (G(zR, zL, ym + h) - G(zR, zL, ym - h)) / (2 * h)
        for k in range(len(ym)):
            roots.append(
                dict(
                    y0=float(ym[k]),
                    y1=float(y1[k]),
                    tR=float(tR[k]),
                    tL=float(tL[k]),
                    res=float(y2[k] - ym[k]),
                    dG=float(dG[k]),
                )
            )
    return dict(
        n_sign_changes=len(br),
        roots=roots,
        ambiguous_gaps=amb, noise_suspect=suspect,
        n_valid=int(fin.sum()),
        grid=(yg[0], yg[-1]),
    )


# ---------- constructors ----------
def lienard_zone(T, D, a):
    return Zone([[T, -1.0], [D, 0.0]], [0.0, -a])


def shifted_zone(A, b_orig, x_line):
    """Zone data for z' = A z + b_orig with switching line x = x_line, shifted so line is x=0."""
    A = np.asarray(A, float)
    b = np.asarray(b_orig, float) + A @ np.array([x_line, 0.0])
    return Zone(A, b)


def two_foci_common_eq(A_R, A_L, e_R, e_L):
    """Zones with equilibria e_R, e_L (in coordinates where the line is x=0)."""
    A_R = np.asarray(A_R, float)
    A_L = np.asarray(A_L, float)
    return Zone(A_R, -A_R @ np.asarray(e_R, float)), Zone(A_L, -A_L @ np.asarray(e_L, float))


# Huan-Yang / Llibre-Ponce system (line x=1, origin = common equilibrium)
HY_AP = np.array([[19 / 500, -1 / 10], [1 / 10, 19 / 500]])
HY_AM = np.array([[1.0, -5.0], [377 / 1000, -13 / 10]])
HY_Y = [
    1.68119451051893996990946394580,
    0.96579985584668225513544927484,
    0.61885416518252501376067323768,
]


def hy_zones():
    zR = shifted_zone(HY_AP, [0.0, 0.0], 1.0)
    zL = shifted_zone(HY_AM, [0.0, 0.0], 1.0)
    return zR, zL
