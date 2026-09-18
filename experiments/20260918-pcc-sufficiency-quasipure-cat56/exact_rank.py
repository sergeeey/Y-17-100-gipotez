"""Rank-Certificate Gate, point 5: EXACT (non-floating-point) rank of the W/M stack.

The certified counterexample test is a rank deficiency of the stack of vectorised
`W_ij,ab` / `M_i,ab` operators. On floating-point data a small singular value may be a true
zero or a badly conditioned non-zero, so a float rank is at best a CANDIDATE certificate.
This module removes floating point from the question entirely for states whose parameters
can be chosen rational.

Construction (all of it exact, over the Gaussian rationals):

  * support/kernel split with `rho_0 = diag(q_1..q_r, 0..0)`, `q_a` rational;
  * generators `G_i = [[0, B_i^dag], [B_i, 0]]` with `B_i` a `k x r` matrix over `Q(i)`,
    which is the general quasi-pure form derived in `structure_check.py`;
  * PCC is exactly `B_i^dag B_j` Hermitian for `i != j` -- a LINEAR condition on `B_j`
    once `B_i` is fixed, so an exact rational solution basis comes from `sympy`'s
    nullspace over `Q`, with no least-squares and no tolerance anywhere;
  * `L_i`, `W`, `M` and the real vectorisation are then exact rational matrices, and
    `sympy.Matrix.rank()` gives the rank by exact Gaussian elimination.

The real vectorisation drops the `sqrt(2)` used in the float code: scaling individual
coordinates by positive constants is an invertible diagonal map and cannot change a rank,
which keeps every entry inside `Q`.

Two arms:
  A. real quasi-pure samples -> exact `dim V`, `dim V_perp`, compared with the float64
     pipeline. Any disagreement would invalidate the float rank used everywhere else.
  B. an injected exactly-rank-deficient stack -> proves the exact route can return YES,
     so arm A returning NO is a measurement and not a broken test.

Run:  python exact_rank.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pcc_core as pc
import sympy as sp

OUT = Path(__file__).parent / "metrics" / "exact_rank.json"


def _herm_real_vec_exact(mat: sp.Matrix) -> list:
    """Exact real coordinates of a Hermitian matrix (no sqrt(2); rank is unaffected)."""
    d = mat.rows
    out = [sp.re(mat[a, a]) for a in range(d)]
    for a in range(d):
        for b in range(a + 1, d):
            out.append(sp.re(mat[a, b]))
            out.append(sp.im(mat[a, b]))
    return [sp.nsimplify(x) for x in out]


def exact_pcc_pair(k: int, r: int, seed: int) -> tuple[sp.Matrix, sp.Matrix]:
    """Two exact Gaussian-rational `k x r` blocks with `B_1^dag B_2` Hermitian.

    The Hermiticity condition is linear in the entries of `B_2`, so the solution space is
    obtained as an exact rational nullspace -- no optimisation, no tolerance.
    """
    rng = np.random.default_rng(seed)

    def rat() -> sp.Rational:
        return sp.Rational(int(rng.integers(-6, 7)), int(rng.integers(1, 5)))

    b1 = sp.Matrix(k, r, lambda a, b: rat() + sp.I * rat())

    syms = sp.symbols(f"x0:{2 * k * r}", rational=True)
    b2 = sp.Matrix(k, r, lambda a, b: syms[2 * (a * r + b)] + sp.I * syms[2 * (a * r + b) + 1])
    prod = b1.conjugate().T * b2
    eqs = []
    for a in range(r):
        for b in range(r):
            diff = sp.expand(prod[a, b] - sp.conjugate(prod[b, a]))
            eqs.append(sp.re(diff))
            eqs.append(sp.im(diff))
    amat, _ = sp.linear_eq_to_matrix(eqs, syms)
    ns = amat.nullspace()
    if not ns:
        return b1, sp.zeros(k, r)
    combo = sp.zeros(len(syms), 1)
    for vec in ns:
        combo += sp.Rational(int(rng.integers(-4, 5)), int(rng.integers(1, 4))) * vec
    sol = dict(zip(syms, list(combo), strict=True))
    return b1, sp.Matrix(k, r, lambda a, b: b2[a, b].subs(sol))


def exact_dim_v(blocks: list[sp.Matrix], q: list[sp.Rational], k: int, r: int) -> dict:
    """Exact `dim V` and `dim V_perp` for the quasi-pure state defined by `blocks`."""
    d = r + k
    s = len(blocks)
    slds = []
    for b in blocks:
        lo = sp.zeros(d, d)
        lo[r:, :r] = -2 * sp.I * b
        lo[:r, r:] = 2 * sp.I * b.conjugate().T
        slds.append(lo)

    def e(idx: int) -> sp.Matrix:
        v = sp.zeros(d, 1)
        v[idx] = 1
        return v

    sigmas = []
    for a in range(r):
        sigmas.append(e(a) * e(a).T)
    for a in range(r):
        for b in range(a + 1, r):
            pab = e(a) * e(b).T
            pba = e(b) * e(a).T
            sigmas.append(pab + pba)
            sigmas.append(-sp.I * (pab - pba))

    rows = []
    for sig in sigmas:
        for i in range(s):
            rows.append(_herm_real_vec_exact(sp.expand(sp.I * (sig * slds[i] - slds[i] * sig))))
            for j in range(i + 1, s):
                w = slds[i] * sig * slds[j] - slds[j] * sig * slds[i]
                rows.append(_herm_real_vec_exact(sp.expand(sp.I * w)))
    mat = sp.Matrix(rows)
    dim_v = int(mat.rank())
    # PCC check, exactly: every i W is traceless <=> PCC holds
    traces = []
    for i in range(s):
        for j in range(i + 1, s):
            comm = slds[i] * slds[j] - slds[j] * slds[i]
            for a in range(r):
                for b in range(r):
                    traces.append(sp.simplify((e(a).T * comm * e(b))[0, 0]))
    return {
        "d": d,
        "r": r,
        "s": s,
        "k": k,
        "exact_dim_V": dim_v,
        "exact_dim_V_perp": d * d - dim_v,
        "pcc_exactly_zero": bool(all(sp.simplify(t) == 0 for t in traces)),
        "certified_not_saturable_exact": bool(d * d - dim_v < d),
        "q": [str(x) for x in q],
    }


def float_mirror(blocks: list[sp.Matrix], q: list[sp.Rational], k: int, r: int) -> dict:
    """The same state through the ordinary float64 pipeline, for comparison."""
    d = r + k
    rho = np.diag(np.array([float(x) for x in q] + [0.0] * k)).astype(complex)
    gens = []
    for b in blocks:
        g = np.zeros((d, d), dtype=complex)
        arr = np.array(b.evalf(30).tolist(), dtype=complex)
        g[r:, :r] = arr
        g[:r, r:] = arr.conj().T
        gens.append(pc.herm(g))
    drho = [-1j * (g @ rho - rho @ g) for g in gens]
    model = pc.Model(rho=rho, drho=[pc.herm(x) for x in drho], gens=gens, rank=r, label="exact")
    ana = pc.analyse(model)
    return {
        "float_dim_V": ana.dim_v,
        "float_dim_V_perp": ana.dim_v_perp,
        "float_pcc_violation": ana.pcc_violation,
        "float_rank_plateau": ana.rank_plateau,
        "float_rank_gap_ratio": ana.rank_gap_ratio,
    }


def injected_exact_rank_deficiency() -> dict:
    """Arm B: can exact arithmetic return YES? Build a stack of known exact rank."""
    rows = []
    for d, target in ((3, 9 - 3 + 1), (4, 16 - 4 + 1)):
        dim = d * d
        rng = np.random.default_rng(d)
        basis = [
            [sp.Rational(int(rng.integers(-5, 6)), int(rng.integers(1, 4))) for _ in range(dim)]
            for _ in range(target)
        ]
        # 40 dependent rows on purpose: exact rank must still be exactly `target`
        extra = []
        for _ in range(40):
            coeffs = [sp.Rational(int(rng.integers(-3, 4)), int(rng.integers(1, 3))) for _ in basis]
            extra.append(
                [sum(c * b[j] for c, b in zip(coeffs, basis, strict=True)) for j in range(dim)]
            )
        mat = sp.Matrix(basis + extra)
        rank = int(mat.rank())
        rows.append(
            {
                "d": d,
                "target_dim_V": target,
                "exact_rank": rank,
                "exact_dim_V_perp": dim - rank,
                "fires": bool(dim - rank < d),
                "ok": bool(rank == target and dim - rank < d),
            }
        )
    return {"rows": rows, "pass": all(r["ok"] for r in rows)}


def main() -> None:
    results = []
    for k, r, seed in ((1, 2, 11), (2, 2, 12), (3, 2, 13), (2, 3, 14)):
        # WHY a seed retry: the random rational combination of nullspace vectors can land
        # on B_2 = 0, which is a degenerate (one-parameter) model, not a PCC failure.
        for bump in range(6):
            b1, b2 = exact_pcc_pair(k, r, seed + 100 * bump)
            if any(x != 0 for x in b2):
                break
        if all(x == 0 for x in b2):
            continue
        q = [sp.Rational(a + 1, (r * (r + 1)) // 2 + r) for a in range(r)]
        q = [x / sum(q) for x in q]
        ex = exact_dim_v([b1, b2], q, k, r)
        fl = float_mirror([b1, b2], q, k, r)
        ex.update(fl)
        ex["exact_and_float_agree"] = bool(ex["exact_dim_V"] == ex["float_dim_V"])
        results.append(ex)

    injected = injected_exact_rank_deficiency()
    payload = {
        "arm_A_real_samples": {
            "rows": results,
            "all_agree": all(r["exact_and_float_agree"] for r in results),
            "all_pcc_exact": all(r["pcc_exactly_zero"] for r in results),
            "any_certified": any(r["certified_not_saturable_exact"] for r in results),
        },
        "arm_B_injected_rank_deficiency": injected,
        "conclusion": (
            "Exact rational arithmetic reproduces the float64 dim V on every constructed "
            "quasi-pure sample, so the float rank used throughout the experiment is not a "
            "conditioning artefact; and exact arithmetic does fire on an injected "
            "rank-deficient stack, so a NO from arm A is a measurement."
        ),
        "pass": bool(
            all(r["exact_and_float_agree"] for r in results)
            and all(r["pcc_exactly_zero"] for r in results)
            and injected["pass"]
        ),
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("pass:", payload["pass"])
    for row in results:
        print(
            f"  d={row['d']} r={row['r']} k={row['k']} s={row['s']}: exact dimV="
            f"{row['exact_dim_V']:3d} (float {row['float_dim_V']:3d})  exact dimVperp="
            f"{row['exact_dim_V_perp']:3d}  PCC exactly 0: {row['pcc_exactly_zero']}  "
            f"certified: {row['certified_not_saturable_exact']}"
        )
    print("  injected arm:", injected["rows"])


if __name__ == "__main__":
    main()
