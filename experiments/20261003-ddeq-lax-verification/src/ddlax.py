"""Differential-difference zero-curvature checker (sympy).
Dynamical variables are Symbols named '<fam>_<idx>' (idx may be negative: 'u1_m1').
Families in F are dynamical (d/dt u^fam_l = S^l F^fam); other families (e.g. 'al' for alpha(n+k))
are n-dependent but time-constant; plain symbols (lam, c, q) are constants.
S shifts every idx by +1 (and n -> n+1, which is encoded by the al_k family)."""

import re, random
import sympy as sp
import mpmath as mp

SYM = re.compile(r"^([A-Za-z]\w*?)_(m?\d+)$")


def mk(fam, idx):
    return sp.Symbol(f"{fam}_{'m' + str(-idx) if idx < 0 else idx}")


def parse(s):
    m = SYM.match(s.name)
    if not m:
        return None
    return m.group(1), int(m.group(2).replace("m", "-"))


def S(e, k=1):
    if isinstance(e, sp.MatrixBase):
        return e.applyfunc(lambda x: S(x, k))
    e = sp.sympify(e)
    rep = {}
    for s in e.free_symbols:
        p = parse(s)
        if p:
            rep[s] = mk(p[0], p[1] + k)
    return e.xreplace(rep)


class System:
    def __init__(self, F):
        self.F = dict(F)  # fam -> expr at position n

    def Dt(self, e):
        if isinstance(e, sp.MatrixBase):
            return e.applyfunc(self.Dt)
        e = sp.sympify(e)
        tot = 0
        for s in e.free_symbols:
            p = parse(s)
            if p and p[0] in self.F:
                d = sp.diff(e, s)
                if d != 0:
                    tot += S(self.F[p[0]], p[1]) * d
        return tot

    def mlr_residual(self, M, U):
        return self.Dt(M) - S(U) * M + M * U


def sym_simplify(e):
    return sp.cancel(sp.together(e))


def rand_vals(syms, rng):
    return {
        s: sp.Rational(
            rng.choice([-7, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7]), rng.choice([1, 2, 3, 5, 7])
        )
        for s in syms
    }


def num_resid(e, trials=4, seed=1, prec=60):
    """max |e| over random rational points (mpmath dps=prec); complex ok (sqrt)."""
    mp.mp.dps = prec
    e = sp.sympify(e)
    rng = random.Random(seed)
    syms = sorted(e.free_symbols, key=lambda s: s.name)
    if not syms:
        return abs(mp.mpmathify(sp.N(e, prec)))
    f = sp.lambdify(syms, e, "mpmath")
    worst = mp.mpf(0)
    got = 0
    tries = 0
    while got < trials and tries < 300:
        tries += 1
        vals = [mp.mpf(v.p) / mp.mpf(v.q) for v in rand_vals(syms, rng).values()]
        try:
            r = abs(f(*vals))
        except (ZeroDivisionError, ValueError):
            continue
        if mp.isnan(r) or mp.isinf(r):
            continue
        worst = max(worst, r)
        got += 1
    return worst


def mat_num_resid(Mx, trials=4, seed=1):
    return max(num_resid(x, trials, seed) for x in Mx)


def mat_sym_zero(Mx):
    return all(sym_simplify(x) == 0 for x in Mx)


def miura_residual(tilde_sys, Phi, target_sys):
    """Def.5 eq (20): Dtilde_t(Phi^i) = F^i(n, S^a Phi, ...) with u^j_l -> S^l(Phi^j)."""
    out = {}
    for fam, Fi in target_sys.F.items():
        rep = {}
        for s in Fi.free_symbols:
            p = parse(s)
            if p and p[0] in Phi:
                rep[s] = S(Phi[p[0]], p[1])
        rhs = Fi.xreplace(rep)
        out[fam] = tilde_sys.Dt(Phi[fam]) - rhs
    return out


def gauge(M, U, G, sys_):
    Gi = G.inv()
    return S(G) * M * Gi, sys_.Dt(G) * Gi + G * U * Gi


def nabla(M, Q, k):
    """nabla_M^k(Q) for integer k (k<0 uses the inverse (14))."""
    Mi = M.inv()
    for _ in range(abs(k)):
        if k > 0:
            Q = S(Mi * Q * M)
        else:
            Q = M * S(Q, -1) * Mi
    return Q


def Delta(M, fam):
    """Delta^{u^fam}(M) = sum_l nabla_M^{-l}( dM/du^fam_l * M^-1 )  (eq (15))."""
    Mi = M.inv()
    tot = sp.zeros(*M.shape)
    for s in M.free_symbols:
        p = parse(s)
        if p and p[0] == fam:
            tot += nabla(M, M.diff(s) * Mi, -p[1])
    return tot
