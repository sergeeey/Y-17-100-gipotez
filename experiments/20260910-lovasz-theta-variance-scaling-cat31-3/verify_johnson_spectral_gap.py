"""Verifies, by DIRECT diagonalization (not a recalled formula -- integrity.md: no phantom
formulas from memory), the spectral gap of the Johnson graph J(N,q)'s single-swap random walk,
and checks whether the resulting Poincare inequality

    Var_pi(f) <= [1 / (2*(1-lambda_2))] * E_edge[(f(S)-f(S'))^2]

is consistent with the observed (C_q, T_q) pairs from check_johnson_swap_energy.py's n=23 run
(N=10). J(N,q) is regular of degree d=q*(N-q) (q choices to remove times N-q choices to add),
so the transition matrix P = A/d is symmetric and its eigenvalues can be read directly off A/d.

Matrices are built explicitly and diagonalized with numpy.linalg.eigvalsh -- feasible here only
because N=10 keeps every layer's vertex count at C(10,q) <= 252.
"""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"


def johnson_transition_eigs(big_n: int, q: int) -> np.ndarray:
    subsets = list(combinations(range(big_n), q))
    idx = {s: i for i, s in enumerate(subsets)}
    v = len(subsets)
    a = np.zeros((v, v))
    for s in subsets:
        s_set = set(s)
        out = [x for x in range(big_n) if x not in s_set]
        for rem in s:
            base = s_set - {rem}
            for add in out:
                nb = tuple(sorted(base | {add}))
                a[idx[s], idx[nb]] = 1.0
    d = q * (big_n - q)
    if d == 0:
        return np.array([1.0])
    p = a / d
    eigs = np.linalg.eigvalsh(p)
    return np.sort(eigs)[::-1]  # descending: eigs[0]=1 (trivial), eigs[1]=lambda_2, ...


def run() -> dict:
    with open(METRICS / "johnson_swap_energy.json", encoding="utf-8") as f:
        swap_data = json.load(f)
    rows_n23 = swap_data["23"]

    big_n = 10  # N=m-1 for n=23 (m=11)
    results = []
    for row in rows_n23:
        q = row["q"]
        if q == 0 or q == big_n:
            continue
        eigs = johnson_transition_eigs(big_n, q)
        lambda2 = float(eigs[1])
        gap = 1.0 - lambda2
        poincare_bound = row["T_q"] / (2 * gap) if gap > 0 else float("inf")
        results.append(
            {
                "q": q,
                "lambda2": lambda2,
                "gap": gap,
                "T_q": row["T_q"],
                "C_q": row["C_q"],
                "poincare_bound_on_Var": poincare_bound,
                "bound_holds": row["C_q"] <= poincare_bound + 1e-9,
                "tightness_ratio_C_over_bound": row["C_q"] / poincare_bound
                if poincare_bound > 0
                else float("nan"),
            }
        )
        print(
            f"q={q:2d}  lambda2={lambda2:.6f}  gap={gap:.6f}  "
            f"Poincare_bound={poincare_bound:.6f}  observed_C_q={row['C_q']:.6f}  "
            f"holds={row['C_q'] <= poincare_bound + 1e-9}  "
            f"tightness={row['C_q'] / poincare_bound:.4f}",
            flush=True,
        )
    return {"N": big_n, "rows": results}


def verify_gap_formula_generalizes(n_values: list[int]) -> dict:
    """Second, independent check (integrity.md spot-check rule): does gap(N,q)=N/(q*(N-q))
    hold at N values OTHER than the N=10 used in run() above, or was that a coincidence of one
    specific N? Diagonalizes fresh for each N, does not reuse the N=10 result."""
    all_ok = True
    rows = []
    for big_n in n_values:
        for q in range(1, big_n):
            eigs = johnson_transition_eigs(big_n, q)
            lambda2 = float(eigs[1])
            gap_diag = 1.0 - lambda2
            gap_formula = big_n / (q * (big_n - q))
            err = abs(gap_diag - gap_formula)
            ok = err < 1e-9
            all_ok = all_ok and ok
            rows.append(
                {
                    "N": big_n,
                    "q": q,
                    "gap_diagonalized": gap_diag,
                    "gap_formula": gap_formula,
                    "err": err,
                    "ok": ok,
                }
            )
            print(
                f"N={big_n:2d} q={q:2d}  diag={gap_diag:.8f}  formula={gap_formula:.8f}  "
                f"err={err:.2e}  ok={ok}"
            )
    return {"all_ok": all_ok, "rows": rows}


if __name__ == "__main__":
    out = run()
    with open(METRICS / "johnson_spectral_gap_verification.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    print("\n--- independent generalization check: does gap=N/(q(N-q)) hold at OTHER N? ---")
    gen_check = verify_gap_formula_generalizes([6, 8, 13])
    print(f"\nALL formula matches across N in [6,8,13]: {gen_check['all_ok']}")
    with open(
        METRICS / "johnson_gap_formula_generalization_check.json", "w", encoding="utf-8"
    ) as f:
        json.dump(gen_check, f, indent=2)
