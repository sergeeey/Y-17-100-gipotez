# ruff: noqa
"""Independent exact verification of a saved tuple: dim_R V over Q computed EXACTLY as the rank of the integer matrix
of real vectorisations [Re, Im] of the 544 generators i W, i M (definition of V as a REAL span), with FLINT.

Shares no construction code with exact_certify.py (own Gaussian-integer arithmetic on pairs of Python-int arrays) and uses
a different rank method (integer rank over Q, both bounds at once) than the F_p check. Also re-checks PCC on the full
22 x 22 commutators and det QFIM exactly (the SLD identity holds by construction of L = [[0, A^dag],[A, 0]], and is checked in verify_instance.py).

Usage: python verify_exact_Q.py <jsonl> <seed>   (row must carry 'blocks')
"""

import json
import sys
from pathlib import Path

import flint
import numpy as np

sys.set_int_max_str_digits(0)
K, R, S = 20, 2, 16
D = K + R


def zeros(shape):
    return np.zeros(shape, dtype=object), np.zeros(shape, dtype=object)


def mul(a, b):
    return a[0].dot(b[0]) - a[1].dot(b[1]), a[0].dot(b[1]) + a[1].dot(b[0])


def sub(a, b):
    return a[0] - b[0], a[1] - b[1]


def dag(a):
    return a[0].T.copy(), (-a[1]).T.copy()


def times_i(a):
    return -a[1], a[0]


def zero(a):
    return not (a[0].any() or a[1].any())


def load(path, seed):
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row["seed"] == seed and row.get("blocks"):
            return [[int(v) for v in x] for x in row["blocks"]]
    raise SystemExit("no tuple")


def main():
    blocks = load(sys.argv[1], int(sys.argv[2]))
    kr = K * R
    B = []
    for x in blocks:
        re = np.array([[x[c * R + a] for a in range(R)] for c in range(K)], dtype=object)
        im = np.array([[x[kr + c * R + a] for a in range(R)] for c in range(K)], dtype=object)
        B.append((re, im))
    Ls = []
    for re, im in B:
        A = (2 * im, -2 * re)  # -2i * (re + i im) = 2 im - 2 i re
        L = zeros((D, D))
        L[0][R:, :R], L[1][R:, :R] = A
        Ad = dag(A)
        L[0][:R, R:], L[1][:R, R:] = Ad
        Ls.append(L)
    # PCC on the full commutators, support block only
    pcc = all(
        zero((c[0][:R, :R], c[1][:R, :R]))
        for i in range(S)
        for j in range(i + 1, S)
        for c in [sub(mul(Ls[i], Ls[j]), mul(Ls[j], Ls[i]))]
    )
    # QFIM F_ij = Re sum_a q_a (A_i^dag A_j)_aa with q = (1, 2)
    q = [1, 2]
    F = [[0] * S for _ in range(S)]
    for i in range(S):
        for j in range(S):
            Ai = (Ls[i][0][R:, :R], Ls[i][1][R:, :R])
            Aj = (Ls[j][0][R:, :R], Ls[j][1][R:, :R])
            m = mul(dag(Ai), Aj)
            F[i][j] = int(sum(q[a] * m[0][a, a] for a in range(R)))
    det = flint.fmpz_mat(F).det()
    # sigma operators (support projectors are the first R standard basis vectors)
    sig = []
    for a in range(R):
        m = zeros((D, D))
        m[0][a, a] = 1
        sig.append(m)
    for a in range(R):
        for b in range(a + 1, R):
            m = zeros((D, D))
            m[0][a, b] = m[0][b, a] = 1
            sig.append(m)
            m = zeros((D, D))
            m[1][a, b] = -1
            m[1][b, a] = 1
            sig.append(m)  # -i(P_ab - P_ba)
    rows = []
    for sg in sig:
        for i in range(S):
            mm = times_i(sub(mul(sg, Ls[i]), mul(Ls[i], sg)))
            rows.append([int(v) for v in mm[0].ravel()] + [int(v) for v in mm[1].ravel()])
        for i in range(S):
            for j in range(i + 1, S):
                w = sub(mul(mul(Ls[i], sg), Ls[j]), mul(mul(Ls[j], sg), Ls[i]))
                ww = times_i(w)
                rows.append([int(v) for v in ww[0].ravel()] + [int(v) for v in ww[1].ravel()])
    M = flint.fmpz_mat(rows)
    rank = M.rank()
    out = {
        "n_rows": len(rows),
        "n_cols": len(rows[0]),
        "max_abs_entry_B": max(abs(v) for x in blocks for v in x),
        "pcc_exact_full_commutators": bool(pcc),
        "qfim_det_nonzero_exact": bool(det != 0),
        "dimV_over_Q_exact": int(rank),
        "dimVperp_exact": D * D - int(rank),
        "fires_dimVperp_lt_d": bool(D * D - int(rank) < D),
    }
    print(out)
    Path(__file__).parent.joinpath("metrics", f"verify_exactQ_seed{sys.argv[2]}.json").write_text(
        json.dumps(out, indent=1), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
