"""Quasi-pure models: the block POVM carries the whole QFI as null-outcome (rare-event)
information (float64 check).

Model: rho = diag(P, 0), P > 0 on R (dim 2), L_a = [[0, B_a^dagger], [B_a, L00_a]] with
L^{++}_a = 0 (quasi-pure), kernel dimension K = d - 2. Block POVM: the two support projectors
|e_0><e_0|, |e_1><e_1| plus an orthonormal basis of the kernel. Claims checked:
  (i)  the point CFIM of the block POVM is zero (F_pos = 0), because L^{++} = 0 gives
       d_a p = 0 on the support;
  (ii) the sum over kernel basis vectors of the null terms N_k equals the QFI F^Q exactly;
  (iii) hence H_quad = F^Q / 4 for the block POVM (Hellinger saturation without any
       condition), while the direction-wise limit (L) needs rank-one N_k for every kernel
       vector, which is not automatic.
"""

import json
from pathlib import Path

import numpy as np

RNG = np.random.default_rng(7)
OUT = Path(__file__).resolve().parent / "metrics" / "hellinger_block_triviality_2026-10-21.json"


def random_quasi_pure(d, p):
    b = [RNG.normal(size=(d - 2, 2)) + 1j * RNG.normal(size=(d - 2, 2)) for _ in range(p)]
    ls = []
    for bl in b:
        lmat = np.zeros((d, d), dtype=complex)
        lmat[:2, 2:] = bl.conj().T
        lmat[2:, :2] = bl
        ls.append(lmat)
    rho = np.zeros((d, d), dtype=complex)
    rho[:2, :2] = np.diag([0.6, 0.4])
    return rho, ls


def qfim(rho, ls):
    return np.array([[np.real(np.trace(rho @ La @ Lb)) for Lb in ls] for La in ls])


def block_pov_quantities(rho, ls, d):
    p = len(ls)
    f_pos = np.zeros((p, p))
    n_null = np.zeros((p, p))
    kernel_basis = np.eye(d, dtype=complex)[:, 2:]  # standard kernel basis (already orthonormal)
    for e in [np.eye(d, dtype=complex)[:, 0], np.eye(d, dtype=complex)[:, 1]]:
        pe = float(np.real(e.conj() @ rho @ e))
        dp = np.array([float(np.real(e.conj() @ (rho @ L + L @ rho) @ e)) / 2 for L in ls])
        if pe > 1e-14:
            f_pos += np.outer(dp, dp) / pe
    for j in range(kernel_basis.shape[1]):
        k = kernel_basis[:, j]
        n_null += np.array([[np.real(k.conj() @ (La @ rho @ Lb) @ k) for Lb in ls] for La in ls])
    return f_pos, n_null


def main():
    results = []
    for trial in range(5):
        d, p = 5 + trial % 2, 2 + trial % 3
        rho, ls = random_quasi_pure(d, p)
        fq = qfim(rho, ls)
        f_pos, n_null = block_pov_quantities(rho, ls, d)
        results.append(
            {
                "trial": trial,
                "d": d,
                "p": p,
                "max_abs_F_pos": float(np.max(np.abs(f_pos))),
                "max_abs_sum_null_minus_F_Q": float(np.max(np.abs(n_null - fq))),
                "max_abs_hellinger_minus_FQ_over_4": float(
                    np.max(np.abs((f_pos + n_null) / 4 - fq / 4))
                ),
            }
        )
        print(results[-1])
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"WROTE {OUT}")


if __name__ == "__main__":
    main()
