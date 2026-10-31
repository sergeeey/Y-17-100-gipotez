"""Stage C: SOS dual certificate in (lam, xi) variables.

Reformulation: I_20 in cone{yy^dag : y in Y_S}  <=>  M_S = B^dag B in
cone{ lam lam^T (x) x x^dag : lam in R^|S|, x in C^2 }, where B = [A_i]_{i in S} (20 x 2|S|).
Dual certificate: Hermitian blocks W_ik (symmetric in i,k) with
    f_W(lam, x) = sum_{ik} lam_i lam_k x^dag W_ik x  >= 0 on V = { lam (x) x in Ran(B^dag) }   and   <W, M> = sum_ik tr(W_ik G_ik) < 0.
Positivity on V is certified by   |lam|^(2a) |xi|^(2b) f_W + sum_r l_r h_r = m^T G m,  G PSD,
with l_r the real bilinear equations of V and m the monomials lam^(1+a) xi^(1+b).
Usage: python -I c2_sos_dual.py <instance.jsonl> <S+|S-|csv> <a> <b> <out.json>
"""

import itertools
import json
import os
import sys
import time

import cvxpy as cp
import numpy as np
import scipy.sparse as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(
    0, os.path.normpath(os.path.join(HERE, "..", "..", "20261027-h-cat56-2-discovery", "code"))
)
import s8_admissible_span as sa  # noqa: E402

path, which, A_LEV, B_LEV, out = (
    sys.argv[1],
    sys.argv[2],
    int(sys.argv[3]),
    int(sys.argv[4]),
    sys.argv[5],
)
S = (
    list(range(12))
    if which == "S+"
    else list(range(4, 16))
    if which == "S-"
    else [int(t) for t in which.split(",")]
)
n = len(S)
As = sa.load_A(path)
B = np.hstack([As[i] for i in S])  # 20 x 2n
Mfull = B.conj().T @ B  # (2n x 2n), index (i,a)
LAM = list(range(n))
XI = list(range(n, n + 4))

Hs = [
    np.array([[1, 0], [0, 0]], complex),
    np.array([[0, 0], [0, 1]], complex),
    np.array([[0, 1], [1, 0]], complex),
    np.array([[0, -1j], [1j, 0]], complex),
]
T = np.array([[1, 1j, 0, 0], [0, 0, 1, 1j]], complex)  # x = T xi


def quad_xi(H):
    K = np.real(T.conj().T @ H @ T)
    c = {}
    for a in range(4):
        for b in range(a, 4):
            coef = K[a, b] * (1 if a == b else 2)
            if abs(coef) > 1e-15:
                c[(XI[a], XI[b])] = coef
    return c


QX = [quad_xi(H) for H in Hs]


def block(i, k):
    return Mfull[2 * i : 2 * i + 2, 2 * k : 2 * k + 2]


wkeys = [(i, k, p) for i in range(n) for k in range(i, n) for p in range(4)]
widx = {t: j for j, t in enumerate(wkeys)}
pair = np.zeros(len(wkeys))
for i, k, p in wkeys:
    pair[widx[(i, k, p)]] = np.real(np.trace(Hs[p] @ block(i, k)))

mono_id = {}


def mid(m):
    m = tuple(sorted(m))
    if m not in mono_id:
        mono_id[m] = len(mono_id)
    return mono_id[m]


def lam_monos(d):
    return list(itertools.combinations_with_replacement(LAM, d))


def xi_monos(d):
    return list(itertools.combinations_with_replacement(XI, d))


def power_sum_squares(vars_, e):
    res = {(): 1.0}
    for _ in range(e):
        new = {}
        for m, c in res.items():
            for v in vars_:
                key = tuple(sorted(m + (v, v)))
                new[key] = new.get(key, 0.0) + c
        res = new
    return res


MULT = {}
for m1, c1 in power_sum_squares(LAM, A_LEV).items():
    for m2, c2 in power_sum_squares(XI, B_LEV).items():
        key = tuple(sorted(m1 + m2))
        MULT[key] = MULT.get(key, 0.0) + c1 * c2

w_entries = {}
for i, k, p in wkeys:
    j = widx[(i, k, p)]
    for (xa, xb), cx in QX[p].items():
        base = (LAM[i], LAM[k], xa, xb)
        for mm, cm in MULT.items():
            r = mid(base + mm)
            w_entries[(r, j)] = w_entries.get((r, j), 0.0) + cx * cm

# ideal: q = lam (x) x must lie in Ran(B^dag) = (null B)^perp
U, sv, Vh = np.linalg.svd(B)
Nsp = Vh[20:].conj().T  # 2n x (2n-20), B @ Nsp = 0
ell = []
for r in range(Nsp.shape[1]):
    v = Nsp[:, r]
    coefs = np.zeros((n, 4), complex)
    for i in range(n):
        for a in range(2):
            coefs[i] += np.conj(v[2 * i + a]) * T[a]
    for part in (np.real, np.imag):
        d = {}
        for i in range(n):
            for a in range(4):
                c = part(coefs[i, a])
                if abs(c) > 1e-14:
                    d[(LAM[i], XI[a])] = c
        ell.append(d)
hbl, hbx = 1 + 2 * A_LEV, 1 + 2 * B_LEV
hmon = [lm + xm for lm in lam_monos(hbl) for xm in xi_monos(hbx)]
h_entries = {}
nh = len(ell) * len(hmon)
for ri, d in enumerate(ell):
    for hj, hm in enumerate(hmon):
        col = ri * len(hmon) + hj
        for (la_, xa_), c in d.items():
            r = mid((la_, xa_) + hm)
            h_entries[(r, col)] = h_entries.get((r, col), 0.0) + c

mvec = [lm + xm for lm in lam_monos(1 + A_LEV) for xm in xi_monos(1 + B_LEV)]
m_sz = len(mvec)
g_entries = {}
tri = [(a, b) for a in range(m_sz) for b in range(a, m_sz)]
for gj, (a, b) in enumerate(tri):
    r = mid(mvec[a] + mvec[b])
    g_entries[(r, gj)] = g_entries.get((r, gj), 0.0) + (1.0 if a == b else 2.0)

nr = len(mono_id)


def to_sp(ent, ncol):
    if not ent:
        return sp.csr_matrix((nr, ncol))
    rr, cc = zip(*ent.keys())
    return sp.csr_matrix((list(ent.values()), (rr, cc)), shape=(nr, ncol))


Aw, Ah, Ag = to_sp(w_entries, len(wkeys)), to_sp(h_entries, nh), to_sp(g_entries, len(tri))
print(
    f"{which} n={n} a={A_LEV} b={B_LEV}: monomials={nr}, W-params={len(wkeys)}, "
    f"h-params={nh}, Gram={m_sz} ({len(tri)} tri)",
    flush=True,
)

scale = float(np.real(np.trace(Mfull)))
w = cp.Variable(len(wkeys))
h = cp.Variable(nh)
G = cp.Variable((m_sz, m_sz), symmetric=True)
idx = np.array([a * m_sz + b for (a, b) in tri])
Sel = sp.csr_matrix((np.ones(len(idx)), (np.arange(len(idx)), idx)), shape=(len(idx), m_sz * m_sz))
gtri = Sel @ cp.vec(G, order="C")
tau = cp.Variable()
cons = [Aw @ w + Ah @ h - Ag @ gtri == 0, (pair / scale) @ w == -1.0, G - tau * np.eye(m_sz) >> 0, tau <= 1.0]
prob = cp.Problem(cp.Maximize(tau), cons)
t0 = time.time()
try:
    prob.solve(solver=cp.CLARABEL, verbose=False)
except Exception as e:  # noqa: BLE001
    print("clarabel failed:", e)
    prob.solve(solver=cp.SCS, eps=1e-8, max_iters=100000)
res = {
    "set": which,
    "n": n,
    "a": A_LEV,
    "b": B_LEV,
    "status": prob.status,
    "tau": None if tau.value is None else float(tau.value),
    "pair_scale": scale,
    "seconds": time.time() - t0,
    "gram": m_sz,
    "monomials": nr,
}
print(json.dumps(res, indent=1))
if tau.value is not None and tau.value > 0:
    np.savez_compressed(
        out.replace(".json", ".npz"), w=w.value, h=h.value, G=G.value, tau=tau.value
    )
json.dump(res, open(out, "w"), indent=1)
