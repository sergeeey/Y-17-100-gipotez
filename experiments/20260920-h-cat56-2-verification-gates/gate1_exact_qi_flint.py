"""Gate 1: explicit Gaussian-rational (Q(i)) firing instance, using FLINT for the kernel + LLL.

exact_certify.py (H-CAT56-2) failed to finish at d=22 because sympy's kernel/LLL blew up (no-LLL
variant killed after ~30 min, sympy LLL asserted). Here the ONLY change is the kernel_basis routine:
python-flint's fmpz_mat.nullspace() (exact) + fmpz_mat.lll() (row-reduction). Everything downstream
(exact PCC, exact Lyapunov, exact QFIM determinant, rank mod p of the full d x d iW/iM stack) is the
unchanged, already-reviewed exact_certify.certify().

Logic of the certificate (what it does and does NOT need):
  * rank over F_p  <=  rank over Q(i)  (reduction Z[i] -> F_p is a ring homomorphism)
  * non-saturation needs only dim V >= d^2 - d + 1, i.e. a LOWER bound on rank. So rank_p = 463
    already gives dim V >= 463, dim V-perp <= 21 < 22 = d. No upper bound is needed for the
    theorem; an upper bound (dim V-perp >= 21 from the dimension bound) only pins the value.
"""

from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import flint

sys.set_int_max_str_digits(0)

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "20260919-pcc-generic-quasipure-cat56-2"))
import exact_certify as ec  # noqa: E402


def kernel_basis_flint(rows: list[list[int]], n: int, lll: bool) -> list[list[int]]:
    if not rows:
        return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    m = flint.fmpz_mat(rows)
    nul, nullity = m.nullspace()  # columns 0..nullity-1 span the integer kernel
    vecs = []
    for j in range(nullity):
        col = [int(nul[i, j]) for i in range(n)]
        g = math.gcd(*col)
        vecs.append([x // g for x in col] if g else col)
    if lll and len(vecs) > 1:
        red = flint.fmpz_mat(vecs).lll()
        vecs = [[int(red[i, j]) for j in range(n)] for i in range(red.nrows())]
        vecs = [v for v in vecs if any(v)]
    return vecs


def main() -> int:
    k, r, s, seed = (int(x) for x in sys.argv[1:5])
    ec.kernel_basis = kernel_basis_flint
    t0 = time.time()
    res = ec.certify(k, r, s, seed, True)
    res["total_seconds"] = time.time() - t0
    res["kernel_backend"] = f"python-flint {flint.__version__} nullspace+lll"
    path = HERE / "metrics" / f"gate1_exact_d{k + r}_r{r}_s{s}_seed{seed}.json"
    path.write_text(json.dumps(res, indent=2, default=str), encoding="utf-8")
    keep = {
        x: res[x]
        for x in res
        if x
        in (
            "d",
            "r",
            "s",
            "rank_mod_p",
            "dim_v_perp_lower_bound_ok",
            "total_seconds",
            "pcc_exact",
            "qfim_det_nonzero",
        )
    }
    print(json.dumps(keep, default=str), flush=True)
    print("keys:", sorted(res)[:40], flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
