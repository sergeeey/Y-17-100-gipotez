"""exact3.py -- THIRD validator (round 2), written from scratch, independent of cox.py / cox2.py.

Exact arithmetic in K = Q(sqrt2, sqrt3) (elements a0 + a1*r2 + a2*r3 + a3*r6, Fractions).
Supports Coxeter labels 0 (none), 3, 4, 6, 99 (= infinity, Gram -1) and also 2*... only those.
(label 5 would need sqrt5 -> not supported here on purpose; raises.)

What it does for a Gram matrix G (n x n, real, diag 1):
  * exact rank (so exact nullity), signature via high-precision (mpmath) eigenvalues
  * exact enumeration of the extreme rays of the cone K = {x in R^{d,1} : <e_i,x> <= 0}
    WITHOUT ever realising the e_i: a ray is x = sum_j c_j e_j with (G c)_S = 0 for a d-subset S;
    two c give the same x iff they differ by ker G.  The ray is recorded by y = G c = (<e_i,x>)_i.
  * rays must be timelike or lightlike (c^T G c <= 0), all in ONE sheet (pairwise <x_a,x_b> <= 0)
  * each facet must contain a rank-d set of rays, ridge (rank d-1 common set) <=> G_ij > -1
  * full face lattice, f-vector, Euler sum, vertex degrees, list of facet pairs with NO common ray
Zero tests are exact; sign tests of nonzero field elements use mpmath at 60 digits.
"""

import itertools
from fractions import Fraction as Fr
import mpmath as mp

mp.mp.dps = 60
R2, R3, R6 = mp.sqrt(2), mp.sqrt(3), mp.sqrt(6)


class QF:
    __slots__ = ("a",)

    def __init__(self, a0=0, a1=0, a2=0, a3=0):
        self.a = (Fr(a0), Fr(a1), Fr(a2), Fr(a3))

    def __add__(s, o):
        o = _q(o)
        return QF(*(x + y for x, y in zip(s.a, o.a)))

    __radd__ = __add__

    def __neg__(s):
        return QF(*(-x for x in s.a))

    def __sub__(s, o):
        return s + (-_q(o))

    def __rsub__(s, o):
        return _q(o) - s

    def __mul__(s, o):
        o = _q(o)
        a0, a1, a2, a3 = s.a
        b0, b1, b2, b3 = o.a
        return QF(
            a0 * b0 + 2 * a1 * b1 + 3 * a2 * b2 + 6 * a3 * b3,
            a0 * b1 + a1 * b0 + 3 * (a2 * b3 + a3 * b2),
            a0 * b2 + a2 * b0 + 2 * (a1 * b3 + a3 * b1),
            a0 * b3 + a3 * b0 + a1 * b2 + a2 * b1,
        )

    __rmul__ = __mul__

    def iszero(s):
        return all(x == 0 for x in s.a)

    def conj1(s):  # sqrt2 -> -sqrt2
        a0, a1, a2, a3 = s.a
        return QF(a0, -a1, a2, -a3)

    def conj2(s):  # sqrt3 -> -sqrt3
        a0, a1, a2, a3 = s.a
        return QF(a0, a1, -a2, -a3)

    def conj12(s):
        a0, a1, a2, a3 = s.a
        return QF(a0, -a1, -a2, a3)

    def inv(s):
        if s.iszero():
            raise ZeroDivisionError
        t = s.conj1() * s.conj2() * s.conj12()
        n = s * t
        assert n.a[1] == n.a[2] == n.a[3] == 0
        return t * QF(1 / n.a[0])

    def __truediv__(s, o):
        return s * _q(o).inv()

    def mpf(s):
        a0, a1, a2, a3 = s.a
        return (
            mp.mpf(a0.numerator) / a0.denominator
            + mp.mpf(a1.numerator) / a1.denominator * R2
            + mp.mpf(a2.numerator) / a2.denominator * R3
            + mp.mpf(a3.numerator) / a3.denominator * R6
        )

    def sign(s):
        if s.iszero():
            return 0
        v = s.mpf()
        assert abs(v) > mp.mpf(10) ** (-40), "nonzero element evaluating ~0: precision problem"
        return 1 if v > 0 else -1

    def __repr__(s):
        return "QF%s" % (tuple(str(x) for x in s.a),)


def _q(o):
    return o if isinstance(o, QF) else QF(o)


ZERO, ONE = QF(0), QF(1)


def entry(code):
    """Gram entry -cos(pi/m) exactly."""
    if code == 0:
        return QF(0)
    if code == 99:
        return QF(-1)
    if code == 3:
        return QF(Fr(-1, 2))
    if code == 4:  # -sqrt2/2
        return QF(0, Fr(-1, 2))
    if code == 6:  # -sqrt3/2
        return QF(0, 0, Fr(-1, 2))
    raise ValueError("label %r not supported (needs another field)" % (code,))


def gram(n, edges):
    G = [[ZERO for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = ONE
    for (i, j), m in edges.items():
        G[i][j] = G[j][i] = entry(m)
    return G


def parse_edges(s):
    """'0-1:inf 0-6:4 ...' -> dict"""
    e = {}
    for tok in s.split():
        ij, lab = tok.split(":")
        i, j = map(int, ij.split("-"))
        e[(i, j)] = 99 if lab == "inf" else int(lab)
    return e


# ------------------------------------------------------------------ exact linear algebra over K
def rref(M, ncols=None):
    """Return (R, pivots) reduced row echelon form of list-of-lists M over K (copy)."""
    M = [row[:] for row in M]
    rows = len(M)
    cols = len(M[0]) if rows else (ncols or 0)
    piv = []
    r = 0
    for c in range(cols):
        p = None
        for i in range(r, rows):
            if not M[i][c].iszero():
                p = i
                break
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        iv = M[r][c].inv()
        M[r] = [x * iv for x in M[r]]
        for i in range(rows):
            if i != r and not M[i][c].iszero():
                f = M[i][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == rows:
            break
    return M, piv


def rank(M):
    return len(rref(M)[1]) if M and M[0] else 0


def nullspace(M, ncols):
    R, piv = rref(M, ncols)
    free = [c for c in range(ncols) if c not in piv]
    basis = []
    for f in free:
        v = [ZERO] * ncols
        v[f] = ONE
        for ri, pc in enumerate(piv):
            v[pc] = -R[ri][f]
        basis.append(v)
    return basis


def matvec(G, c):
    n = len(G)
    out = []
    for i in range(n):
        s = ZERO
        for j in range(n):
            if not G[i][j].iszero() and not c[j].iszero():
                s = s + G[i][j] * c[j]
        out.append(s)
    return out


def dot(a, b):
    s = ZERO
    for x, y in zip(a, b):
        if not x.iszero() and not y.iszero():
            s = s + x * y
    return s


def signature(G):
    n = len(G)
    A = mp.matrix(n, n)
    for i in range(n):
        for j in range(n):
            A[i, j] = G[i][j].mpf()
    E = mp.eigsy(A, eigvals_only=True)
    pos = sum(1 for x in E if x > mp.mpf(10) ** -30)
    neg = sum(1 for x in E if x < -(mp.mpf(10) ** -30))
    zer = n - pos - neg
    return pos, neg, zer


def normalize_y(y):
    """scale y by a positive element so first nonzero entry has |.| = 1 (as exact element)."""
    for v in y:
        if not v.iszero():
            s = v.sign()
            return [x * (v.inv() * QF(s)) for x in y]
    return y


def validate(n, edges, want_lattice=True, verbose=False):
    G = gram(n, edges)
    out = dict(n=n)
    rk = rank(G)
    pos, neg, zer = signature(G)
    out.update(rank=rk, nullity=n - rk, sig=(pos, neg, zer))
    d = pos
    out["d"] = d
    if neg != 1 or zer != n - rk or rk != d + 1:
        out.update(ok=False, reason="signature/rank (%d,%d,%d) rank %d" % (pos, neg, zer, rk))
        return out
    # connectivity of the diagram (indecomposable)
    seen = {0}
    st = [0]
    while st:
        u = st.pop()
        for v in range(n):
            if v not in seen and not G[u][v].iszero():
                seen.add(v)
                st.append(v)
    if len(seen) != n:
        out.update(ok=False, reason="decomposable")
        return out
    # --- rays
    rays = {}  # key: tuple of y entries repr -> (y, c, q)
    for S in itertools.combinations(range(n), d):
        rows = [G[i] for i in S]
        N = nullspace(rows, n)  # c with (G c)_S = 0, dimension n-rank(rows)
        # images y = G c
        Ys = [matvec(G, c) for c in N]
        # rank of image set = dim N - nullity(G) when ker G subset N (always true)
        rkY = rank(Ys) if Ys else 0
        if rkY != 1:
            continue
        # pick a c with nonzero image
        for c, y in zip(N, Ys):
            if any(not v.iszero() for v in y):
                break
        q = dot(c, y)  # <x,x>
        # sign orientation: want all y_i <= 0
        pos_i = any(v.sign() > 0 for v in y)
        neg_i = any(v.sign() < 0 for v in y)
        if pos_i and neg_i:
            continue  # not in the cone either way
        if pos_i:  # flip
            c = [-x for x in c]
            y = [-x for x in y]
        yn = normalize_y(y)
        # positive scalar used for y -> same factor for c (not needed besides q sign)
        key = tuple(tuple(v.a) for v in yn)
        if key not in rays:
            rays[key] = dict(y=yn, c=c, qsign=q.sign())
    R = list(rays.values())
    out["n_rays"] = len(R)
    if not R:
        out.update(ok=False, reason="empty cone")
        return out
    nspace = sum(1 for r in R if r["qsign"] > 0)
    if nspace:
        out.update(ok=False, reason="spacelike rays: %d of %d" % (nspace, len(R)))
        return out
    # one sheet: pairwise <x_a,x_b> = c_a^T G c_b <= 0
    for a, b in itertools.combinations(range(len(R)), 2):
        ip = dot(R[a]["c"], matvec(G, R[b]["c"]))  # y_b pairing
        if ip.sign() > 0:
            out.update(ok=False, reason="rays on different sheets")
            return out
    out["n_ideal"] = sum(1 for r in R if r["qsign"] == 0)
    out["compact"] = out["n_ideal"] == 0
    # tight sets
    tight = [frozenset(i for i in range(n) if r["y"][i].iszero()) for r in R]
    facet_rays = [frozenset(ri for ri in range(len(R)) if i in tight[ri]) for i in range(n)]
    for i in range(n):
        if len(facet_rays[i]) < d or rank([R[ri]["y"] for ri in facet_rays[i]]) != d:
            out.update(ok=False, reason="facet %d not (d-1)-dimensional" % i)
            return out
    # ridge <=> G_ij > -1 ; common rays
    disjoint = []
    for i in range(n):
        for j in range(i + 1, n):
            com = facet_rays[i] & facet_rays[j]
            rr = rank([R[ri]["y"] for ri in com]) if com else 0
            ridge = rr == d - 1
            adj = (G[i][j] + 1).sign() > 0  # G_ij > -1
            if ridge != adj:
                out.update(
                    ok=False, reason="ridge mismatch (%d,%d) rank %d Gij=%s" % (i, j, rr, G[i][j])
                )
                return out
            if not com:
                disjoint.append((i, j))
                if (G[i][j] + 1).sign() >= 0:
                    out.update(ok=False, reason="disjoint facets with |G|<=1")
                    return out
    out["disjoint_pairs"] = disjoint
    deg = [len(tight[ri]) for ri in range(len(R))]
    out["vertex_degrees"] = sorted(deg)
    out["nonsimple_vertices"] = sum(1 for x in deg if x > d)
    out["ok"] = True
    out["reason"] = "ok"
    if want_lattice:
        # faces = intersections of facets' ray-sets
        full = frozenset(range(len(R)))
        faces = {full}
        frontier = [full]
        while frontier:
            nxt = []
            for f in frontier:
                for fr in facet_rays:
                    g = f & fr
                    if g and g not in faces:
                        faces.add(g)
                        nxt.append(g)
            frontier = nxt
        fv = [0] * (d + 1)
        for f in faces:
            dim = rank([R[ri]["y"] for ri in f]) - 1
            fv[dim] += 1
        out["fvec"] = fv
        out["euler"] = sum((-1) ** i * fv[i] for i in range(d + 1))
        out["facets_ok"] = fv[d - 1] == n
        out["_faces"] = faces
        out["_rays"] = R
        out["_tight"] = tight
        out["_facet_rays"] = facet_rays
    return out


def vinberg_exact(n, edges):
    """Vinberg criterion with exact principal minors (Sylvester) -- code-independent of cox.py."""
    G = gram(n, edges)
    pos, neg, zer = signature(G)
    d = pos
    if neg != 1:
        return dict(finite=False, reason="signature")

    cache = {}

    def det(S):
        S = tuple(S)
        if S in cache:
            return cache[S]
        if not S:
            cache[S] = ONE
            return ONE
        M = [[G[i][j] for j in S] for i in S]
        # fraction-free-ish: use rref based determinant via elimination
        M = [r[:] for r in M]
        m = len(M)
        dt = ONE
        for c in range(m):
            p = None
            for r in range(c, m):
                if not M[r][c].iszero():
                    p = r
                    break
            if p is None:
                cache[S] = ZERO
                return ZERO
            if p != c:
                M[c], M[p] = M[p], M[c]
                dt = -dt
            dt = dt * M[c][c]
            iv = M[c][c].inv()
            for r in range(c + 1, m):
                if not M[r][c].iszero():
                    f = M[r][c] * iv
                    M[r] = [x - f * y for x, y in zip(M[r], M[c])]
        cache[S] = dt
        return dt

    ell_cache = {}

    def elliptic(S):
        S = tuple(sorted(S))
        if S in ell_cache:
            return ell_cache[S]
        # positive definite iff all leading principal minors (in this order) > 0
        ok = all(det(S[:k]).sign() > 0 for k in range(1, len(S) + 1))
        ell_cache[S] = ok
        return ok

    def comps(S):
        S = list(S)
        seen = set()
        cs = []
        for s in S:
            if s in seen:
                continue
            c = []
            st = [s]
            seen.add(s)
            while st:
                u = st.pop()
                c.append(u)
                for v in S:
                    if v not in seen and not G[u][v].iszero():
                        seen.add(v)
                        st.append(v)
            cs.append(sorted(c))
        return cs

    def parabolic_conn(c):
        # connected, >=2 nodes, det = 0 exactly, every proper subdiagram (drop one node) elliptic
        if len(c) < 2:
            return False
        if not det(c).iszero():
            return False
        return all(elliptic([x for x in c if x != v]) for v in c)

    def parabolic(S):
        cs = comps(S)
        return len(cs) if all(parabolic_conn(c) for c in cs) else 0

    anyparab = False
    k = d - 1
    for S in itertools.combinations(range(n), k):
        if not elliptic(S):
            continue
        rest = [v for v in range(n) if v not in S]
        cnt = sum(1 for v in rest if elliptic(S + (v,)))
        for r in range(1, len(rest) + 1):
            for T in itertools.combinations(rest, r):
                c = parabolic(list(S) + list(T))
                if c == r:
                    cnt += 1
                    anyparab = True
        if cnt != 2:
            return dict(finite=False, reason="edge %s has %d ext" % (S, cnt))
    return dict(finite=True, compact=not anyparab, d=d)


if __name__ == "__main__":
    import sys

    s = sys.argv[1]
    nn = int(sys.argv[2])
    e = parse_edges(s)
    v = validate(nn, e)
    print({k: v[k] for k in v if not k.startswith("_")})
    print("vinberg_exact:", vinberg_exact(nn, e))
