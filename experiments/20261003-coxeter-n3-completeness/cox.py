"""Small Coxeter-polytope toolkit (no CoxIter available locally).

Label codes: 0 = no edge (angle pi/2), m>=3 = angle pi/m, 99 = infinity (parallel, Gram -1).
Dotted (ultraparallel) edges are supported in the Gram-matrix API only (entries < -1).

Two independent implementations of the finite-volume decision:
  vinberg_check(G)  -- Vinberg criterion on elliptic/parabolic subdiagrams
  geo_check(G)      -- extreme rays of the cone {x: <e_i,x> <= 0} in R^{d,1}
"""

import itertools, math
import numpy as np
import networkx as nx

TOL = 1e-9
INF = 99


def entry(code):
    if code == 0:
        return 0.0
    if code == INF:
        return -1.0
    return -math.cos(math.pi / code)


def gram_from_L(L):
    n = len(L)
    G = np.eye(n)
    for i in range(n):
        for j in range(i + 1, n):
            c = L[i][j]
            if c:
                G[i, j] = G[j, i] = entry(c)
    return G


def L_from_edges(n, edges):
    L = np.zeros((n, n), dtype=int)
    for (i, j), m in edges.items():
        L[i, j] = L[j, i] = m
    return L


def chain(labels):
    n = len(labels) + 1
    return L_from_edges(n, {(i, i + 1): m for i, m in enumerate(labels)})


def signature(G, tol=TOL):
    w = np.linalg.eigvalsh(G)
    return int((w > tol).sum()), int((w < -tol).sum()), int((np.abs(w) <= tol).sum())


def components(G, S, tol=1e-12):
    S = list(S)
    seen = set()
    comps = []
    for s in S:
        if s in seen:
            continue
        stack = [s]
        comp = []
        seen.add(s)
        while stack:
            u = stack.pop()
            comp.append(u)
            for v in S:
                if v not in seen and abs(G[u, v]) > tol:
                    seen.add(v)
                    stack.append(v)
        comps.append(comp)
    return comps


def is_elliptic(G, S, tol=TOL):
    S = list(S)
    if not S:
        return True
    return np.linalg.eigvalsh(G[np.ix_(S, S)])[0] > tol


def parabolic_comps(G, S, tol=TOL):
    """Return number of components if S is a parabolic subdiagram (all comps affine), else 0."""
    comps = components(G, S)
    for c in comps:
        if len(c) < 2:
            return 0
        w = np.linalg.eigvalsh(G[np.ix_(c, c)])
        if w[0] < -tol or int((np.abs(w) <= tol).sum()) != 1:
            return 0
    return len(comps)


# ---------------------------------------------------------------- Vinberg criterion
def vinberg_check(G, tol=TOL, priority=None, count_only_fail_fast=True):
    """Return dict(finite=bool, compact=bool, d=int, reason=str).

    Criterion (Vinberg 1985, as implemented in CoxIter): G Gram matrix of signature (d,1),
    indecomposable; polytope has finite volume iff every elliptic subdiagram S of rank d-1
    (|S| = d-1) has exactly two extensions, an extension being either S+{v} elliptic of rank d
    or S+T parabolic of rank d-1 with |T| = number of components. Compact iff no parabolic ones.
    """
    n = G.shape[0]
    npos, nneg, nz = signature(G, tol)
    if nneg != 1:
        return dict(
            finite=False, compact=False, d=npos, reason="signature (%d,%d,%d)" % (npos, nneg, nz)
        )
    d = npos
    if d < 2:
        return dict(finite=False, compact=False, d=d, reason="d<2")
    if len(components(G, range(n))) != 1:
        return dict(finite=False, compact=False, d=d, reason="decomposable")
    k = d - 1
    anyparab = False
    seq = []
    if priority:
        seq.extend(priority)
    seen = set(tuple(sorted(s)) for s in seq)
    rest_iter = (s for s in itertools.combinations(range(n), k) if s not in seen)
    for S in itertools.chain((tuple(sorted(s)) for s in seq), rest_iter):
        if len(S) != k or not is_elliptic(G, S, tol):
            continue
        Sset = set(S)
        rest = [v for v in range(n) if v not in Sset]
        cnt = 0
        for v in rest:
            if is_elliptic(G, S + (v,), tol):
                cnt += 1
        for r in range(1, len(rest) + 1):
            for T in itertools.combinations(rest, r):
                c = parabolic_comps(G, list(S) + list(T), tol)
                if c == r:
                    cnt += 1
                    anyparab = True
        if cnt != 2:
            return dict(
                finite=False, compact=False, d=d, reason="edge %s has %d extensions" % (S, cnt)
            )
    return dict(finite=True, compact=not anyparab, d=d, reason="ok")


def vinberg_fvector(G, tol=TOL):
    """f-vector via elliptic subdiagrams (finite faces) + ideal vertices (parabolic rank d-1).
    Returns (f list indexed by dimension 0..d, n_ideal, ideal_types) and the Euler sum."""
    n = G.shape[0]
    npos, nneg, _ = signature(G, tol)
    d = npos
    cnt_ell = [0] * (d + 1)  # by size
    for k in range(0, d + 1):
        for S in itertools.combinations(range(n), k):
            if is_elliptic(G, S, tol):
                cnt_ell[k] += 1
    ideal = []
    for k in range(d, n + 1):
        for S in itertools.combinations(range(n), k):
            c = parabolic_comps(G, S, tol)
            if c and len(S) - c == d - 1:
                ideal.append((S, c))
    f = [0] * (d + 1)
    for k in range(0, d + 1):
        f[d - k] = cnt_ell[k]
    f[0] += len(ideal)
    euler = sum((-1) ** i * f[i] for i in range(d + 1))
    return f, len(ideal), [c for _, c in ideal], euler


# ---------------------------------------------------------------- geometric criterion
def geo_check(G, tol=1e-7):
    """Independent decision of finite volume via extreme rays of the cone in R^{d,1}."""
    n = G.shape[0]
    w, Q = np.linalg.eigh(G)
    pos = [i for i in range(n) if w[i] > 1e-9]
    neg = [i for i in range(n) if w[i] < -1e-9]
    if len(neg) != 1:
        return dict(finite=False, compact=False, d=len(pos), reason="signature")
    d = len(pos)
    idx = pos + neg
    V = Q[:, idx] * np.sqrt(np.abs(w[idx]))
    J = np.diag([1.0] * d + [-1.0])
    A = V @ J
    rays = {}
    for S in itertools.combinations(range(n), d):
        M = A[list(S)]
        u, s, vt = np.linalg.svd(M)
        if s[-1] < 1e-9:
            continue
        x = vt[-1]
        v = A @ x
        if np.all(v <= tol):
            y = x
        elif np.all(v >= -tol):
            y = -x
        else:
            continue
        y = y / np.linalg.norm(y)
        key = tuple((np.round(y, 6) + 0.0).tolist())
        rays[key] = y
    if not rays:
        return dict(finite=False, compact=False, d=d, reason="empty cone")
    n_time = n_null = n_space = 0
    q_time_min = 9.0
    q_null_max = 0.0
    orient = set()
    tight_counts = []
    for y in rays.values():
        q = float(y @ J @ y)
        if q > tol:
            n_space += 1
        elif q < -tol:
            n_time += 1
            q_time_min = min(q_time_min, abs(q))
            orient.add(y[-1] > 0)
            tight_counts.append(int((np.abs(A @ y) < 1e-6).sum()))
        else:
            n_null += 1
            q_null_max = max(q_null_max, abs(q))
            orient.add(y[-1] > 0)
            tight_counts.append(int((np.abs(A @ y) < 1e-6).sum()))
    finite = (n_space == 0) and len(orient) == 1
    return dict(
        finite=finite,
        compact=finite and n_null == 0,
        d=d,
        reason="ok" if finite else "spacelike/mixed ray",
        n_vertices=len(rays),
        n_time=n_time,
        n_null=n_null,
        n_space=n_space,
        q_time_min=q_time_min,
        q_null_max=q_null_max,
        nonsimple_vertices=sum(1 for t in tight_counts if t > d),
    )


# ---------------------------------------------------------------- diagram libraries
def spherical_connected(maxn, maxlab=6):
    out = []
    for n in range(1, maxn + 1):
        out.append(("A%d" % n, chain([3] * (n - 1)) if n > 1 else np.zeros((1, 1), dtype=int)))
    for n in range(2, maxn + 1):
        out.append(("B%d" % n, chain([3] * (n - 2) + [4])))
    for n in range(4, maxn + 1):  # D_n
        e = {(i, i + 1): 3 for i in range(n - 2)}
        e[(n - 3, n - 1)] = 3
        out.append(("D%d" % n, L_from_edges(n, e)))
    for n, arms in ((6, (1, 2, 2)), (7, (1, 2, 3)), (8, (1, 2, 4))):
        if n <= maxn:
            out.append(("E%d" % n, star(arms)))
    if maxn >= 4:
        out.append(("F4", chain([3, 4, 3])))
    if maxn >= 3:
        out.append(("H3", chain([5, 3])))
    if maxn >= 4:
        out.append(("H4", chain([5, 3, 3])))
    for m in (5, 6):
        if maxn >= 2 and m <= maxlab:
            out.append(("I2(%d)" % m, chain([m])))
    return out


def star(arms):
    """Star-shaped tree: center + arms of given lengths, all labels 3."""
    n = 1 + sum(arms)
    e = {}
    idx = 1
    for a in arms:
        prev = 0
        for _ in range(a):
            e[(prev, idx)] = 3
            prev = idx
            idx += 1
    return L_from_edges(n, e)


def affine_connected(maxn):
    """Connected affine diagrams with <= maxn nodes. Returns (name, L)."""
    out = []
    if maxn >= 2:
        out.append(("A1~", chain([INF])))
    for n in range(2, maxn):  # A_n~ has n+1 nodes
        if n + 1 <= maxn:
            e = {(i, i + 1): 3 for i in range(n)}
            e[(0, n)] = 3
            out.append(("A%d~" % n, L_from_edges(n + 1, e)))
    for n in range(3, maxn):  # B_n~: n+1 nodes
        if n + 1 <= maxn:
            e = {(0, 2): 3, (1, 2): 3}
            for i in range(2, n - 1):
                e[(i, i + 1)] = 3
            e[(n - 1, n)] = 4
            out.append(("B%d~" % n, L_from_edges(n + 1, e)))
    for n in range(2, maxn):  # C_n~
        if n + 1 <= maxn:
            labs = [4] + [3] * (n - 2) + [4]
            out.append(("C%d~" % n, chain(labs)))
    for n in range(4, maxn):  # D_n~
        if n + 1 <= maxn:
            e = {(0, 2): 3, (1, 2): 3}
            for i in range(2, n - 2):
                e[(i, i + 1)] = 3
            e[(n - 2, n - 1)] = 3
            e[(n - 2, n)] = 3
            out.append(("D%d~" % n, L_from_edges(n + 1, e)))
    for name, arms in (("E6~", (2, 2, 2)), ("E7~", (1, 3, 3)), ("E8~", (1, 2, 5))):
        if 1 + sum(arms) <= maxn:
            out.append((name, star(arms)))
    if maxn >= 5:
        out.append(("F4~", chain([3, 3, 4, 3])))
    if maxn >= 3:
        out.append(("G2~", chain([3, 6])))
    return out


# ---------------------------------------------------------------- isomorphism
def to_nx(L):
    g = nx.Graph()
    n = len(L)
    g.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i + 1, n):
            if L[i][j]:
                g.add_edge(i, j, lab=int(L[i][j]))
    return g


class IsoSet:
    def __init__(self):
        self.buckets = {}
        self.items = []

    def add(self, L, payload=None):
        g = to_nx(L)
        h = nx.weisfeiler_lehman_graph_hash(g, edge_attr="lab", iterations=3)
        key = (len(L), h)
        for g2, _ in self.buckets.get(key, []):
            if nx.is_isomorphic(g, g2, edge_match=lambda a, b: a["lab"] == b["lab"]):
                return False
        self.buckets.setdefault(key, []).append((g, len(self.items)))
        self.items.append((np.array(L), payload))
        return True


def describe(L):
    n = len(L)
    es = []
    for i in range(n):
        for j in range(i + 1, n):
            if L[i][j]:
                es.append("%d-%d:%s" % (i, j, "inf" if L[i][j] == INF else L[i][j]))
    return "n=%d [%s]" % (n, " ".join(es))
