"""F_p-lifting certificate (Rank-Certificate Gate point 5, second exact route).

WHY this exists: `exact_certify.py` builds Gaussian-integer blocks over Q(i), but the sequential
kernel construction has entry growth that is exponential in the number of stages (measured: the
no-LLL run at d = 22, s = 16 did not finish; sympy's LLL asserted). An explicit Q(i) point is
therefore not produced for the firing configurations. Instead this script works EXACTLY over
F_p[i] = F_p[x]/(x^2+1) (p = 1 mod 4) with every step, including PCC, the SLD Lyapunov equation,
the QFIM determinant and the rank of the stacked iW / iM built from the FULL d x d definitions,
done in exact modular arithmetic.

Lifting argument (a derivation, not machine-checked):
  the sequential construction is an iterated linear tower over Z: at stage j the unknown block
  lies in the kernel of a linear map whose matrix entries are polynomial in earlier blocks. On
  the Zariski-open set where a chosen maximal minor of each constraint matrix is non-zero, the
  kernel is a free module of constant rank (graph over free coordinates), so that open set U is
  an open subscheme of an affine space over Z[minors^-1]. The QFIM determinant and a chosen
  (d^2-d+1)-minor of the iW/iM stack are polynomials on U. A point of U(F_p) where all of them
  are non-zero shows each is a NON-ZERO element of the coordinate ring of U over Z_(p), hence of
  U over Q, hence there are Q(i)-points of the same tower (Q(i)-points are dense in an affine
  space) with QFIM non-singular and dim V >= d^2 - d + 1, i.e. an exact rational
  counterexample exists. Necessary computational check made here: the F_p kernel dimension at
  every stage EQUALS the generic char-0 kernel dimension measured in floating point.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import caps
import exact_certify as ec
import numpy as np
import sympy as sp

HERE = Path(__file__).parent
OUT = HERE / "metrics"


def rref_kernel(m: np.ndarray, p: int) -> np.ndarray:
    """Kernel basis (rows) of an integer matrix mod p via reduced row echelon form."""
    a = m.copy() % p
    rows, cols = a.shape
    piv_cols = []
    r = 0
    for c in range(cols):
        if r == rows:
            break
        nz = np.nonzero(a[r:, c])[0]
        if nz.size == 0:
            continue
        pr = r + int(nz[0])
        if pr != r:
            a[[r, pr]] = a[[pr, r]]
        a[r] = (a[r] * pow(int(a[r, c]), p - 2, p)) % p
        others = np.nonzero(a[:, c])[0]
        for o in others:
            if o != r:
                a[o] = (a[o] - int(a[o, c]) * a[r]) % p
        piv_cols.append(c)
        r += 1
    free = [c for c in range(cols) if c not in set(piv_cols)]
    basis = np.zeros((len(free), cols), dtype=np.int64)
    for t, f in enumerate(free):
        basis[t, f] = 1
        for i, pc in enumerate(piv_cols):
            basis[t, pc] = (-a[i, f]) % p
    return basis


def build_blocks_fp(k: int, r: int, s: int, p: int, seed: int) -> tuple[list[list[int]], list[int]]:
    rng = np.random.default_rng(seed)
    kr = k * r
    n = 2 * kr
    blocks = [[int(v) for v in rng.integers(0, p, size=n)]]
    nulls = [n]
    for _ in range(1, s):
        prev = []
        for x in blocks:
            br = [[x[c * r + a] for a in range(r)] for c in range(k)]
            bi = [[x[kr + c * r + a] for a in range(r)] for c in range(k)]
            prev.append((br, bi))
        rows = np.array(ec.constraint_rows(prev, k, r), dtype=object)
        mat = np.array([[int(v) % p for v in row] for row in rows], dtype=np.int64)
        basis = rref_kernel(mat, p)
        nulls.append(int(basis.shape[0]))
        co = rng.integers(0, p, size=basis.shape[0])
        vec = (co.astype(object) @ basis.astype(object)) % p
        blocks.append([int(v) for v in vec])
    return blocks, nulls


def det_mod_p(mat: list[list[int]], p: int) -> int:
    a = np.array(mat, dtype=np.int64) % p
    n = a.shape[0]
    det = 1
    for c in range(n):
        nz = np.nonzero(a[c:, c])[0]
        if nz.size == 0:
            return 0
        pr = c + int(nz[0])
        if pr != c:
            a[[c, pr]] = a[[pr, c]]
            det = (-det) % p
        det = (det * int(a[c, c])) % p
        inv = pow(int(a[c, c]), p - 2, p)
        for o in range(c + 1, n):
            f = (int(a[o, c]) * inv) % p
            if f:
                a[o] = (a[o] - f * a[c]) % p
    return det


def certify_fp(k: int, r: int, s: int, p: int, seed: int) -> dict:
    d = k + r
    t0 = time.time()
    blocks, nulls = build_blocks_fp(k, r, s, p, seed)
    kr = k * r

    def z():
        return np.zeros((d, d), dtype=np.int64), np.zeros((d, d), dtype=np.int64)

    def mul(a, b):
        return (a[0] @ b[0] - a[1] @ b[1]) % p, (a[0] @ b[1] + a[1] @ b[0]) % p

    def sub(a, b):
        return (a[0] - b[0]) % p, (a[1] - b[1]) % p

    def add(a, b):
        return (a[0] + b[0]) % p, (a[1] + b[1]) % p

    def dag(a):
        return a[0].T.copy(), (-a[1].T) % p

    def times_i(a, c=1):
        return (-c * a[1]) % p, (c * a[0]) % p

    q = [a + 1 for a in range(r)]
    rho = z()
    for a in range(r):
        rho[0][a, a] = q[a]
    gens, slds = [], []
    for x in blocks:
        br = np.array([[x[c * r + a] for a in range(r)] for c in range(k)], dtype=np.int64)
        bi = np.array([[x[kr + c * r + a] for a in range(r)] for c in range(k)], dtype=np.int64)
        g = z()
        g[0][r:, :r], g[1][r:, :r] = br, bi
        g[0][:r, r:], g[1][:r, r:] = dag((br, bi))
        gens.append(g)
        ab = times_i((br, bi), -2)
        lm = z()
        lm[0][r:, :r], lm[1][r:, :r] = ab
        lm[0][:r, r:], lm[1][:r, r:] = dag(ab)
        slds.append(lm)
    lyap = True
    for g, lm in zip(gens, slds, strict=True):
        lhs = add(mul(lm, rho), mul(rho, lm))
        rhs = times_i(sub(mul(g, rho), mul(rho, g)), -2)
        d0 = sub(lhs, rhs)
        lyap &= not (d0[0].any() or d0[1].any())
    pcc = True
    for i in range(s):
        for j in range(i + 1, s):
            cm = sub(mul(slds[i], slds[j]), mul(slds[j], slds[i]))
            pcc &= not (cm[0][:r, :r].any() or cm[1][:r, :r].any())
    f = [[0] * s for _ in range(s)]
    for i in range(s):
        for j in range(s):
            mm = mul(
                dag((slds[i][0][r:, :r], slds[i][1][r:, :r])),
                (slds[j][0][r:, :r], slds[j][1][r:, :r]),
            )
            f[i][j] = int(sum(q[a] * int(mm[0][a, a]) for a in range(r)) % p)
    fdet = det_mod_p(f, p)
    sig = []
    for a in range(r):
        m = z()
        m[0][a, a] = 1
        sig.append(m)
    for a in range(r):
        for b in range(a + 1, r):
            m = z()
            m[0][a, b] = m[0][b, a] = 1
            sig.append(m)
            m = z()
            m[1][a, b] = p - 1
            m[1][b, a] = 1
            sig.append(m)
    rows_re, rows_im = [], []
    for sg in sig:
        for i in range(s):
            mm = times_i(sub(mul(sg, slds[i]), mul(slds[i], sg)))
            rows_re.append(mm[0].ravel().tolist())
            rows_im.append(mm[1].ravel().tolist())
            for j in range(i + 1, s):
                w = sub(mul(mul(slds[i], sg), slds[j]), mul(mul(slds[j], sg), slds[i]))
                ww = times_i(w)
                rows_re.append(ww[0].ravel().tolist())
                rows_im.append(ww[1].ravel().tolist())
    rank = ec.rank_mod_p(rows_re, rows_im, p)
    need = d * d - d + 1
    return {
        "p": p,
        "seed": seed,
        "kernel_dims_mod_p": nulls,
        "lyapunov_zero": bool(lyap),
        "pcc_zero": bool(pcc),
        "qfim_det_nonzero_mod_p": bool(fdet != 0),
        "rank_mod_p": int(rank),
        "need": need,
        "dimVperp_mod_p": int(d * d - rank),
        "fires_mod_p": bool(rank >= need),
        "seconds": time.time() - t0,
    }


def main() -> None:
    d, r, s = (int(a) for a in sys.argv[1:4])
    seeds = [20260919, 20260920]
    k = d - r
    # generic char-0 kernel dims from the float sampler (same tower, must match mod p)
    import h2_core as h

    fl = h.sample_sequential(k, r, s, np.random.default_rng(20260919))
    float_nulls = fl[1] if fl else None
    primes = []
    p = 2**26
    while len(primes) < 2:
        p = int(sp.prevprime(p))
        if p % 4 == 1:
            primes.append(p)
    runs = [certify_fp(k, r, s, pp, sd) for pp, sd in zip(primes, seeds, strict=True)]
    for rr in runs:
        rr["kernel_dims_equal_float_generic"] = bool(rr["kernel_dims_mod_p"] == float_nulls)
    res = {
        "d": d,
        "r": r,
        "k": k,
        "s": s,
        "float_generic_kernel_dims": float_nulls,
        "runs": runs,
        "all_ok": bool(
            all(
                x["lyapunov_zero"]
                and x["pcc_zero"]
                and x["qfim_det_nonzero_mod_p"]
                and x["fires_mod_p"]
                and x["kernel_dims_equal_float_generic"]
                for x in runs
            )
        ),
        "resources": caps.state(),
    }
    OUT.mkdir(exist_ok=True)
    tmp = OUT / f"fp_certify_d{d}_r{r}_s{s}.json.tmp"
    tmp.write_text(json.dumps(res, indent=1), encoding="utf-8")
    tmp.replace(OUT / f"fp_certify_d{d}_r{r}_s{s}.json")
    print(json.dumps({k2: v for k2, v in res.items() if k2 != "resources"})[:1500])


if __name__ == "__main__":
    main()
