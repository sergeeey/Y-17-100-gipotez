"""Exact (rational) certificate for a firing configuration (Rank-Certificate Gate point 5).

Construction over Z[i] (no floating point anywhere):
  * blocks B_1..B_s (k x r Gaussian integers) built sequentially: PCC is LINEAR in B_j once
    B_1..B_{j-1} are fixed, so B_j is a small random integer combination of an LLL-reduced
    integer basis of the exact kernel (sympy DomainMatrix over QQ/ZZ);
  * state: rho = diag(q_1,..,q_r,0..0) with INTEGER weights (rho is only defined up to scale for
    the SLD), generators G_i = [[0,B_i^dag],[B_i,0]], d_i rho = -i [G_i, rho];
  * SLD L_i = [[0, A_i^dag],[A_i, 0]], A_i = -2i B_i, verified EXACTLY against the defining
    Lyapunov equation  L rho + rho L = 2 d rho;
  * PCC verified EXACTLY: A_i^dag A_j Hermitian, and <a|[L_i,L_j]|b> = 0 from the full matrices;
  * QFIM F_ij = Re sum_a q_a (A_i^dag A_j)_aa exact integer matrix, determinant != 0 exactly;
  * iM, iW built from the FULL d x d definitions (independent of the reduced formulas), rank of
    the complex d^2-vectors over F_p (p prime, p = 1 mod 4, I^2 = -1). Reduction Z[i] -> F_p is a
    ring homomorphism, so rank_{F_p} <= rank_{Q(i)} = dim_R V (real-independent Hermitian
    matrices are complex-independent): the F_p rank is a rigorous LOWER bound on dim V, which is
    exactly the direction the certificate needs (dim V >= d^2 - d + 1).
"""

from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import caps
import numpy as np
import sympy as sp
from sympy import ZZ
from sympy.polys.matrices import DomainMatrix

HERE = Path(__file__).parent
OUT = HERE / "metrics"
CANDS = HERE / "candidates"


def constraint_rows(prev: list[tuple], k: int, r: int) -> list[list[int]]:
    """Integer rows of the map x -> (Re N - Re N^T)_{a<b}, (Im N + Im N^T)_{a<=b} for every
    previous block, N = B_i^dag X, X = X_re + i X_im (x = [X_re, X_im] flattened row-major)."""
    kr = k * r
    n = 2 * kr
    rows: list[list[int]] = []
    for br, bi in prev:
        # coefficient tables: N_re[a,b'] = sum_c (br[c,a] Xr[c,b'] + bi[c,a] Xi[c,b'])
        #                     N_im[a,b'] = sum_c (br[c,a] Xi[c,b'] - bi[c,a] Xr[c,b'])
        def coef(a: int, bp: int, part: str) -> list[int]:
            v = [0] * n
            for c in range(k):
                if part == "re":
                    v[c * r + bp] += br[c][a]
                    v[kr + c * r + bp] += bi[c][a]
                else:
                    v[kr + c * r + bp] += br[c][a]
                    v[c * r + bp] -= bi[c][a]
            return v

        for a in range(r):
            for b in range(a + 1, r):
                u, w = coef(a, b, "re"), coef(b, a, "re")
                rows.append([x - y for x, y in zip(u, w, strict=True)])
        for a in range(r):
            for b in range(a, r):
                u, w = coef(a, b, "im"), coef(b, a, "im")
                rows.append([x + y for x, y in zip(u, w, strict=True)])
    return rows


def kernel_basis(rows: list[list[int]], n: int, lll: bool) -> list[list[int]]:
    if not rows:
        return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    dm = DomainMatrix([[sp.Rational(x) for x in row] for row in rows], (len(rows), n), sp.QQ)
    ns = dm.nullspace().to_Matrix()
    vecs = []
    for i in range(ns.rows):
        row = [sp.Rational(ns[i, j]) for j in range(n)]
        den = math.lcm(*[int(x.q) for x in row])
        ints = [int(x * den) for x in row]
        g = math.gcd(*ints)
        vecs.append([x // g for x in ints])
    if lll and len(vecs) > 1:
        red = DomainMatrix([[ZZ(x) for x in v] for v in vecs], (len(vecs), n), ZZ).lll()
        vecs = [[int(x) for x in row] for row in red.to_Matrix().tolist()]
        vecs = [v for v in vecs if any(v)]
    return vecs


def build_blocks(k: int, r: int, s: int, seed: int, lll: bool = True) -> tuple[list, list[int]]:
    rng = np.random.default_rng(seed)
    kr = k * r
    n = 2 * kr
    first = [int(x) for x in rng.integers(-3, 4, size=n)]
    blocks = [first]
    nulls = [n]
    for _ in range(1, s):
        prev = []
        for x in blocks:
            br = [[x[c * r + a] for a in range(r)] for c in range(k)]
            bi = [[x[kr + c * r + a] for a in range(r)] for c in range(k)]
            prev.append((br, bi))
        basis = kernel_basis(constraint_rows(prev, k, r), n, lll)
        nulls.append(len(basis))
        coefs = rng.integers(-1, 2, size=len(basis))
        if not coefs.any():
            coefs[0] = 1
        vec = [sum(int(c) * v[t] for c, v in zip(coefs, basis, strict=True)) for t in range(n)]
        g = math.gcd(*vec)
        blocks.append([x // g for x in vec])
    return blocks, nulls


# ---------------- Gaussian-integer matrix helpers (object arrays of Python ints) -------------
def gz(shape) -> tuple[np.ndarray, np.ndarray]:
    return np.zeros(shape, dtype=object), np.zeros(shape, dtype=object)


def gmul(a, b):
    return a[0].dot(b[0]) - a[1].dot(b[1]), a[0].dot(b[1]) + a[1].dot(b[0])


def gadd(a, b):
    return a[0] + b[0], a[1] + b[1]


def gsub(a, b):
    return a[0] - b[0], a[1] - b[1]


def gdag(a):
    return a[0].T.copy(), (-a[1]).T.copy()


def gscal_i(a, c: int = 1):
    """c * i * a."""
    return -c * a[1], c * a[0]


def is_zero(a) -> bool:
    return not (a[0].any() or a[1].any())


def prime_1mod4(start: int) -> int:
    p = start
    while True:
        p = sp.prevprime(p)
        if p % 4 == 1:
            return int(p)


def sqrt_minus_one(p: int) -> int:
    for g in range(2, 100):
        t = pow(g, (p - 1) // 4, p)
        if (t * t) % p == p - 1:
            return t
    raise RuntimeError("no sqrt(-1)")


def rank_mod_p(rows_re: list, rows_im: list, p: int) -> int:
    ip = sqrt_minus_one(p)
    m = np.array(
        [
            [(int(a) + int(b) * ip) % p for a, b in zip(rr, ri, strict=True)]
            for rr, ri in zip(rows_re, rows_im, strict=True)
        ],
        dtype=np.int64,
    )
    rank = 0
    nrows, ncols = m.shape
    for c in range(ncols):
        if rank == nrows:
            break
        piv = np.nonzero(m[rank:, c])[0]
        if piv.size == 0:
            continue
        pr = rank + int(piv[0])
        if pr != rank:
            m[[rank, pr]] = m[[pr, rank]]
        inv = pow(int(m[rank, c]), p - 2, p)
        m[rank] = (m[rank] * inv) % p
        below = m[rank + 1 :, c].copy()
        nz = np.nonzero(below)[0]
        if nz.size:
            idx = rank + 1 + nz
            m[idx] = (m[idx] - np.outer(below[nz], m[rank]) % p) % p
        rank += 1
    return rank


def certify(k: int, r: int, s: int, seed: int, lll: bool = True) -> dict:
    d = k + r
    t0 = time.time()
    blocks, nulls = build_blocks(k, r, s, seed, lll)
    t_build = time.time() - t0
    kr = k * r
    bmats = []
    for x in blocks:
        br = np.array([[x[c * r + a] for a in range(r)] for c in range(k)], dtype=object)
        bi = np.array([[x[kr + c * r + a] for a in range(r)] for c in range(k)], dtype=object)
        bmats.append((br, bi))
    q = [a + 1 for a in range(r)]  # integer weights, rho = diag(q, 0)
    rho = gz((d, d))
    for a in range(r):
        rho[0][a, a] = q[a]
    gens, slds = [], []
    for br, bi in bmats:
        g = gz((d, d))
        g[0][r:, :r], g[1][r:, :r] = br, bi
        bd = gdag((br, bi))
        g[0][:r, r:], g[1][:r, r:] = bd
        gens.append(g)
        a_blk = gscal_i((br, bi), -2)  # A = -2i B
        lm = gz((d, d))
        lm[0][r:, :r], lm[1][r:, :r] = a_blk
        ad = gdag(a_blk)
        lm[0][:r, r:], lm[1][:r, r:] = ad
        slds.append(lm)
    # exact Lyapunov check: L rho + rho L - 2 d rho = 0, d rho = -i [G, rho]
    lyap_ok = True
    for g, lm in zip(gens, slds, strict=True):
        lhs = gadd(gmul(lm, rho), gmul(rho, lm))
        comm = gsub(gmul(g, rho), gmul(rho, g))
        rhs = gscal_i(comm, -2)  # 2 * (-i) [G, rho]
        lyap_ok &= is_zero(gsub(lhs, rhs))
    # exact PCC on the full matrices: <a|[L_i, L_j]|b> = 0 for a,b in the support
    pcc_ok = True
    for i in range(s):
        for j in range(i + 1, s):
            comm = gsub(gmul(slds[i], slds[j]), gmul(slds[j], slds[i]))
            pcc_ok &= is_zero((comm[0][:r, :r], comm[1][:r, :r]))
    # exact QFIM
    f = sp.zeros(s, s)
    for i in range(s):
        for j in range(s):
            m = gmul(
                gdag((slds[i][0][r:, :r], slds[i][1][r:, :r])),
                (slds[j][0][r:, :r], slds[j][1][r:, :r]),
            )
            f[i, j] = sum(q[a] * m[0][a, a] for a in range(r))
    fdet = sp.Matrix(f).det(method="bareiss")
    # F is a Gram matrix (PSD); nonzero determinant <=> positive definite <=> real-independent
    # sigma operators (exactly the paper's definition)
    sig = []
    for a in range(r):
        m = gz((d, d))
        m[0][a, a] = 1
        sig.append(m)
    for a in range(r):
        for b in range(a + 1, r):
            m = gz((d, d))
            m[0][a, b] = m[0][b, a] = 1
            sig.append(m)
            m = gz((d, d))
            m[1][a, b] = -1  # -i at (a,b)
            m[1][b, a] = 1
            sig.append(m)
    rows_re, rows_im = [], []
    for sg in sig:
        for i in range(s):
            mm = gscal_i(gsub(gmul(sg, slds[i]), gmul(slds[i], sg)))
            rows_re.append(mm[0].ravel().tolist())
            rows_im.append(mm[1].ravel().tolist())
            for j in range(i + 1, s):
                w = gsub(gmul(gmul(slds[i], sg), slds[j]), gmul(gmul(slds[j], sg), slds[i]))
                ww = gscal_i(w)
                rows_re.append(ww[0].ravel().tolist())
                rows_im.append(ww[1].ravel().tolist())
    bits = max(int(abs(v)).bit_length() for row in rows_re + rows_im for v in row)
    primes = [prime_1mod4(2**31 - 1), prime_1mod4(2**31 - 100000)]
    ranks = [rank_mod_p(rows_re, rows_im, p) for p in primes]
    need = d * d - d + 1
    cert = bool(lyap_ok and pcc_ok and fdet != 0 and all(rk >= need for rk in ranks))
    res = {
        "d": d,
        "r": r,
        "k": k,
        "s": s,
        "seed": seed,
        "lll": lll,
        "kernel_dims": nulls,
        "max_bits_of_entries_in_stack": bits,
        "max_bits_of_B_entries": max(int(abs(v)).bit_length() for x in blocks for v in x),
        "lyapunov_exact_zero": bool(lyap_ok),
        "pcc_exact_zero": bool(pcc_ok),
        "qfim_det_nonzero": bool(fdet != 0),
        "qfim_det_bits": int(abs(int(fdet)).bit_length()),
        "primes": primes,
        "rank_mod_p": ranks,
        "need_dimV_ge": need,
        "dimV_lower_bound_exact": int(min(ranks)),
        "dimVperp_upper_bound_exact": int(d * d - min(ranks)),
        "exact_certified_dimVperp_lt_d": cert,
        "seconds_build": t_build,
        "seconds_total": time.time() - t0,
        "resources": caps.state(),
    }
    CANDS.mkdir(exist_ok=True)
    (CANDS / f"exact_blocks_d{d}_r{r}_s{s}_seed{seed}.json").write_text(
        json.dumps(
            {
                "k": k,
                "r": r,
                "s": s,
                "B_flat_re_then_im_rowmajor": [[str(v) for v in x] for x in blocks],
                "q_weights": q,
            }
        ),
        encoding="utf-8",
    )
    return res


def main() -> None:
    args = sys.argv[1:]
    d, r, s, seed = (int(a) for a in args[:4])
    use_lll = not (len(args) > 4 and args[4] == "nolll")
    res = certify(d - r, r, s, seed, use_lll)
    OUT.mkdir(exist_ok=True)
    tmp = OUT / f"exact_certify_d{d}_r{r}_s{s}.json.tmp"
    tmp.write_text(json.dumps(res, indent=1), encoding="utf-8")
    tmp.replace(OUT / f"exact_certify_d{d}_r{r}_s{s}.json")
    print({k: v for k, v in res.items() if k not in ("resources",)})


if __name__ == "__main__":
    main()
