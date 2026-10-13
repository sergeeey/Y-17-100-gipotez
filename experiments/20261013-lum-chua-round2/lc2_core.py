"""Round-2 reliable crossing-cycle counter for planar 2-zone focus-focus Filippov PWL systems (line x=0).

Reuses the round-1 closed-form Zone/half_return (pwl_r1.py, copied unchanged) and replaces the blind
counter.  Differences from round-1 count_cycles:
  * no blanket relative noise filter: the float64 noise floor of G is MEASURED against mpmath (calibrate()),
    every float sign change whose |G| is below the trust threshold, and every near-tangency, is re-checked
    in mpmath (default 40 digits) before it is accepted or rejected;
  * wide amplitude range (d up to 1e6) + analytic large-amplitude multiplier kappa;
  * transversality of each root checked against BOTH vector fields (crossing, not sliding);
  * exact-degeneracy (G == 0 on an interval, e.g. a center) is flagged and not counted as isolated cycles.
Cycle convention (as round 1): (0,y0) --R arc--> (0,y1) --L arc--> (0,y2); cycle iff y2 == y0; G = y2 - y0.
"""

from __future__ import annotations

import numpy as np
import mpmath as mp

from pwl_r1 import Zone, G as G_float, compose, y_grid  # noqa: F401

mp.mp.dps = 40


# ---------------------------------------------------------------- canonical form
def canon_zones(TL, DL, aL, TR, DR, aR, b):
    """Lienard canonical form (arXiv:2508.02321 eq.(5)):  x<0: x'=TL x-y, y'=DL x-aL ;  x>0: x'=TR x-y+b, y'=DR x-aR."""
    zL = Zone([[TL, -1.0], [DL, 0.0]], [0.0, -aL])
    zR = Zone([[TR, -1.0], [DR, 0.0]], [b, -aR])
    return zR, zL


def kappa(zR: Zone, zL: Zone) -> float:
    """large-amplitude multiplier of the composed half-return map: exp(pi (tauR/wR + tauL/wL))."""
    return float(np.exp(np.pi * (zR.tau / zR.w + zL.tau / zL.w)))


# ---------------------------------------------------------------- mpmath mirror of the half-return
class MPZone:
    def __init__(self, A, b):
        A = mp.matrix(A)
        b = mp.matrix(b)
        self.A, self.b = A, b
        tr = A[0, 0] + A[1, 1]
        det = A[0, 0] * A[1, 1] - A[0, 1] * A[1, 0]
        self.tau = tr / 2
        self.w = mp.sqrt(det - self.tau**2)
        ze = -(mp.lu_solve(A, b))
        self.ze = ze
        self.k = self.tau / self.w

    def _E(self, s):
        A = self.A
        ek = mp.exp(self.k * s)
        c, sn = mp.cos(s), mp.sin(s)
        tau, w = self.tau, self.w
        E11 = ek * (c + sn * (A[0, 0] - tau) / w)
        E12 = ek * sn * A[0, 1] / w
        E21 = ek * sn * A[1, 0] / w
        E22 = ek * (c + sn * (A[1, 1] - tau) / w)
        return E11, E12, E21, E22

    def x_of_s(self, s, y0):
        E11, E12, _, _ = self._E(s)
        return self.ze[0] * (1 - E11) + E12 * (y0 - self.ze[1])

    def y_of_s(self, s, y0):
        _, _, E21, E22 = self._E(s)
        return self.ze[1] + E21 * (-self.ze[0]) + E22 * (y0 - self.ze[1])

    def half(self, y0, s_guess):
        """polish the first-return parameter s=w t starting from a float guess; return y1 in mp."""
        y0 = mp.mpf(y0)
        s = mp.findroot(lambda ss: self.x_of_s(ss, y0), mp.mpf(s_guess), tol=1e-35, maxsteps=60)
        return self.y_of_s(s, y0), s


def to_mpzone(z: Zone) -> MPZone:
    return MPZone([[mp.mpf(float(v)) for v in row] for row in z.A], [mp.mpf(float(v)) for v in z.b])


def mp_G(mzR: MPZone, mzL: MPZone, zR: Zone, zL: Zone, y0f: float):
    """G in 40-digit arithmetic at the float start y0f (exactly the binary double y0f); the float
    return times provide only the initial guess of the mp root finder."""
    y1f, tR = zR.half_return(+1, np.array([y0f]))
    if not np.isfinite(y1f[0]):
        return None
    y2f, tL = zL.half_return(-1, y1f)
    if not np.isfinite(y2f[0]):
        return None
    y0 = mp.mpf(y0f)
    y1, sR = mzR.half(y0, tR[0] * zR.w)
    y2, sL = mzL.half(y1, tL[0] * zL.w)
    # consistency guard: mp root must be the same branch as the float one
    if abs(float(y1) - float(y1f[0])) > 1e-6 * (1 + abs(float(y1f[0]))):
        return None
    return y2 - y0


# ---------------------------------------------------------------- noise calibration
def calibrate(zR, zL, ys):
    """max |G_float - G_mp| / (1+|y|) over the given starts (those with a valid return)."""
    mzR, mzL = to_mpzone(zR), to_mpzone(zL)
    g = G_float(zR, zL, np.asarray(ys, float))
    errs = []
    for y, gf in zip(ys, g):
        if not np.isfinite(gf):
            continue
        gm = mp_G(mzR, mzL, zR, zL, float(y))
        if gm is None:
            continue
        errs.append(abs(float(gm) - gf) / (1 + abs(y)))
    return (max(errs) if errs else float("nan")), len(errs)


# ---------------------------------------------------------------- the counter
def _xd(z: Zone, y):
    return z.a12 * y + z.b1


def classify_root(zR, zL, y0):
    y1, y2, tR, tL = compose(zR, zL, np.array([y0]))
    y1 = float(y1[0])
    s = dict(
        xdR_y0=float(_xd(zR, y0)),
        xdL_y0=float(_xd(zL, y0)),
        xdR_y1=float(_xd(zR, y1)),
        xdL_y1=float(_xd(zL, y1)),
    )
    s["crossing"] = bool(
        s["xdR_y0"] > 0 and s["xdL_y0"] > 0 and s["xdR_y1"] < 0 and s["xdL_y1"] < 0
    )
    h = 1e-6 * max(1.0, abs(y0))
    gp = G_float(zR, zL, np.array([y0 + h, y0 - h]))
    s["dG"] = float((gp[0] - gp[1]) / (2 * h)) if np.all(np.isfinite(gp)) else float("nan")
    s["multiplier"] = 1.0 + s["dG"]
    s["y1"] = y1
    s["tR"] = float(tR[0])
    s["tL"] = float(tL[0])
    return s


def count_cycles2(
    zR,
    zL,
    n=8000,
    dmin=1e-8,
    dmax=1e6,
    noise_rel=None,
    use_mp=True,
    tan_ratio=0.35,
    mp_floor_rel=1e-25,
    verbose=False,
):
    """Count isolated crossing cycles.  Returns dict(count, roots, ...).
    noise_rel: trusted relative float noise of G (|dG|/(1+|y|)); default 4e-13 pending calibrate()."""
    if noise_rel is None:
        noise_rel = 4e-13
    yg = y_grid(zR, n, dmin, dmax)
    g = G_float(zR, zL, yg)
    fin = np.isfinite(g)
    # early exit: G ~ 0 on a large share of the valid grid -> non-isolated (e.g. a center), do not enumerate noise roots
    _tolv = noise_rel * (1.0 + np.abs(yg))
    _flat = float(np.mean(np.abs(g[fin]) < _tolv[fin])) if fin.any() else 0.0
    if _flat > 0.2:
        return dict(count=None, n_roots_total=0, roots=[], non_crossing_roots=0, rejected_float_sign_changes=0,
                    flat_zone_events=0, flat_share=_flat, degenerate=True, flat_abort=True, hidden_pairs=[],
                    near_tangent=[], n_near_tangent=0, ambiguous_gaps=0, n_valid=int(fin.sum()),
                    grid=(float(yg[0]), float(yg[-1])), kappa=kappa(zR, zL), g_far_sign=0.0, g_near_sign=0.0)
    mzR = mzL = None
    if use_mp:
        mzR, mzL = to_mpzone(zR), to_mpzone(zL)

    brackets = []  # (ya, yb, tag)
    rejected = []  # float sign changes refuted by mp
    amb = 0
    n_flat = 0
    mp_checks = 0
    flat_abort = False
    near_tangent = []
    pairs = []

    def mp_sign(y):
        gm = mp_G(mzR, mzL, zR, zL, float(y))
        return gm

    last = None
    for i in range(n):
        if not fin[i]:
            continue
        if last is not None:
            if i == last + 1:
                if g[last] == 0.0:
                    brackets.append((yg[last], yg[last], "exact0"))
                elif g[last] * g[i] < 0:
                    tol = noise_rel * (1.0 + abs(yg[i]))
                    if min(abs(g[last]), abs(g[i])) < tol:
                        # below trust threshold -> must be confirmed in mp
                        if flat_abort:
                            n_flat += 1
                        elif use_mp:
                            mp_checks += 1
                            if mp_checks >= 40 and n_flat >= 0.9 * mp_checks:
                                flat_abort = True
                            ga, gb = mp_sign(yg[last]), mp_sign(yg[i])
                            if ga is not None and gb is not None:
                                fl = mp_floor_rel * (1 + abs(yg[i]))
                                if abs(ga) > fl and abs(gb) > fl and ga * gb < 0:
                                    brackets.append((yg[last], yg[i], "mp_confirmed"))
                                else:
                                    rejected.append(
                                        (float(yg[last]), float(yg[i]), float(ga), float(gb))
                                    )
                                    n_flat += 1
                            else:
                                rejected.append((float(yg[last]), float(yg[i]), None, None))
                        else:
                            rejected.append((float(yg[last]), float(yg[i]), None, None))
                    else:
                        brackets.append((yg[last], yg[i], "float"))
            else:
                if g[last] * g[i] < 0:
                    amb += 1
        last = i

    # ---- tangency / hidden-pair detector (local minima of |g| without a sign change)
    idx = np.nonzero(fin)[0]
    for j in range(1, len(idx) - 1):
        i0, i1, i2 = idx[j - 1], idx[j], idx[j + 1]
        if i1 != i0 + 1 or i2 != i1 + 1:
            continue
        a, b_, c = g[i0], g[i1], g[i2]
        if a * b_ > 0 and b_ * c > 0 and abs(b_) < abs(a) and abs(b_) < abs(c):
            # candidate local extremum of G: is it much closer to zero than its neighbours?
            if abs(b_) < tan_ratio * min(abs(a), abs(c)) or abs(b_) < 50 * noise_rel * (
                1 + abs(yg[i1])
            ):
                lo, hi = yg[i0], yg[i2]
                sgn = np.sign(b_)
                ys = np.linspace(lo, hi, 801)
                gs = G_float(zR, zL, ys)
                ok = np.isfinite(gs)
                if not ok.any():
                    continue
                k = np.nanargmin(np.where(ok, sgn * gs, np.inf))
                ymin = ys[k]
                gm_f = gs[k]
                found = False
                if sgn * gm_f <= 0:
                    found = True
                elif use_mp and abs(gm_f) < 1e3 * noise_rel * (1 + abs(ymin)):
                    gm = mp_sign(ymin)
                    if (
                        gm is not None
                        and float(sgn) * float(gm) < 0
                        and abs(gm) > mp_floor_rel * (1 + abs(ymin))
                    ):
                        found = True
                if found:
                    pairs.append(
                        dict(window=(float(lo), float(hi)), ymin=float(ymin), gmin=float(gm_f))
                    )
                    # add as two brackets (sign flips inside window): locate by dense sign change
                    sg = np.sign(gs)
                    for q in range(len(ys) - 1):
                        if ok[q] and ok[q + 1] and sg[q] * sg[q + 1] < 0:
                            brackets.append((ys[q], ys[q + 1], "dense_pair"))
                else:
                    near_tangent.append(
                        dict(y=float(ymin), g=float(gm_f), rel=float(abs(gm_f) / (1 + abs(ymin))))
                    )

    # ---- refine all brackets (float bisection) and classify
    roots = []
    seen = []
    for ya, yb, tag in brackets:
        lo, hi = float(ya), float(yb)
        if lo == hi:
            ym = lo
        else:
            glo = float(G_float(zR, zL, np.array([lo]))[0])
            for _ in range(80):
                mid = 0.5 * (lo + hi)
                gm = float(G_float(zR, zL, np.array([mid]))[0])
                if not np.isfinite(gm):
                    break
                if gm * glo > 0:
                    lo, glo = mid, gm
                else:
                    hi = mid
            ym = 0.5 * (lo + hi)
        if any(abs(ym - s0) <= 1e-9 * (1 + abs(ym)) for s0 in seen):
            continue
        seen.append(ym)
        c = classify_root(zR, zL, ym)
        c.update(y0=ym, tag=tag)
        roots.append(c)
    roots.sort(key=lambda r: r["y0"])

    # ---- degeneracy: G ~ 0 on a large share of the valid grid
    tolv = noise_rel * (1.0 + np.abs(yg))
    flat_share = float(np.mean(np.abs(g[fin]) < tolv[fin])) if fin.any() else 0.0
    out = dict(
        count=sum(1 for r in roots if r["crossing"]),
        n_roots_total=len(roots),
        roots=roots,
        non_crossing_roots=sum(1 for r in roots if not r["crossing"]),
        rejected_float_sign_changes=len(rejected),
        flat_zone_events=n_flat,
        flat_share=flat_share,
        degenerate=bool(flat_share > 0.2 or flat_abort),
        flat_abort=flat_abort,
        hidden_pairs=pairs,
        near_tangent=near_tangent[:10],
        n_near_tangent=len(near_tangent),
        ambiguous_gaps=amb,
        n_valid=int(fin.sum()),
        grid=(float(yg[0]), float(yg[-1])),
        kappa=kappa(zR, zL),
        g_far_sign=float(np.sign(g[fin][-1])) if fin.any() else 0.0,
        g_near_sign=float(np.sign(g[fin][0])) if fin.any() else 0.0,
    )
    return out
