"""Attempts l=2 (pairwise) energy on the Johnson slice, per direct user request
("попробуй l=2 через парные эффекты") -- second-order ANOVA on the Hamming slice.

Method: the degree-<=2 polynomial space on the slice (span of {e_j} and {e_j*e_k, j<k}, e_j the
raw membership indicator) equals V_0+V_1+V_2 exactly (classical fact about the slice/Johnson
scheme, analogous to the Boolean cube's Fourier-Walsh degree filtration -- verified below against
this experiment's own exact diagonalization data before being trusted for new n, not just cited).
Fitting delta's best L2 projection onto this space gives E_{<=2} = E_1+E_2 directly.

The Gram matrix (covariance structure) of the raw features {e_j, e_j*e_k} depends ONLY on (N,q),
not on delta -- computed here from closed-form hypergeometric ("falling factorial") moment
formulas, each independently verified against DIRECT exhaustive enumeration at two different
(N,q) before use (not phantom formulas -- integrity.md). The data-dependent part (mu_j, mu_jk)
is computed via a single vectorized matrix multiply, not a python loop over pairs, to stay
tractable for the N~20 cases already reached in points 15b/16 (a naive per-pair python loop
would be O(v*N^2) in slow python; the matmul route is the same asymptotic cost but BLAS-fast).
"""

from __future__ import annotations

import importlib.util
import json
from itertools import combinations
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

necklace_mod = importlib.util.spec_from_file_location(
    "necklace_mod_l2", HERE / "check_necklace_orbit_reduction.py"
)
nm = importlib.util.module_from_spec(necklace_mod)
necklace_mod.loader.exec_module(nm)


def falling(a: float, k: int) -> float:
    r = 1.0
    for i in range(k):
        r *= a - i
    return r


def build_gram_matrix(big_n: int, q: int, pairs: list[tuple[int, int]]) -> np.ndarray:
    """Closed-form (N,q)-only Gram matrix for features [e_0..e_{N-1}, g_pair0, g_pair1, ...]."""
    p1 = q / big_n
    p2 = falling(q, 2) / falling(big_n, 2) if big_n >= 2 else 0.0
    p3 = falling(q, 3) / falling(big_n, 3) if big_n >= 3 else 0.0
    p4 = falling(q, 4) / falling(big_n, 4) if big_n >= 4 else 0.0

    n_pairs = len(pairs)
    dim = big_n + n_pairs
    gram = np.zeros((dim, dim))

    # e_j block
    for j in range(big_n):
        gram[j, j] = p1 * (1 - p1)
        for k in range(j + 1, big_n):
            cov = p2 - p1**2
            gram[j, k] = cov
            gram[k, j] = cov

    # e_j vs g_kl block
    for idx, (a, b) in enumerate(pairs):
        col = big_n + idx
        var_g = p2 - p2**2
        gram[col, col] = var_g
        for j in range(big_n):
            if j == a or j == b:
                cov = (1 - p1) * p2
            else:
                cov = p3 - p1 * p2
            gram[j, col] = cov
            gram[col, j] = cov

    # g vs g block
    for idx1, (a, b) in enumerate(pairs):
        for idx2 in range(idx1 + 1, n_pairs):
            c, d = pairs[idx2]
            shared = len({a, b} & {c, d})
            if shared == 1:
                cov = p3 - p2**2
            else:  # shared == 0 (shared==2 impossible for idx1!=idx2 since pairs distinct)
                cov = p4 - p2**2
            col1 = big_n + idx1
            col2 = big_n + idx2
            gram[col1, col2] = cov
            gram[col2, col1] = cov

    return gram


def l2_energy_per_layer(n: int, max_pairs_dim: int = 260) -> list[dict]:
    m = (n - 1) // 2
    ground = list(range(1, m))
    big_n = len(ground)

    res = nm.solve_orbit_reduced(n, verbose=False)
    theta_full = res["theta_full"]
    x_arr = np.log(theta_full / np.sqrt(n))
    n_subsets = 1 << m
    delta = np.empty(n_subsets)
    for mask in range(n_subsets):
        if mask & 1:
            continue
        delta[mask] = x_arr[mask] - x_arr[mask | 1]

    pairs = list(combinations(range(big_n), 2))
    dim = big_n + len(pairs)
    if dim > max_pairs_dim:
        print(f"  n={n}: dim={dim} > {max_pairs_dim}, skipping l=2 (Gram solve would be costly)")
        return []

    rows = []
    for q in range(1, big_n):
        subsets = list(combinations(ground, q))
        masks = np.array([sum(1 << b for b in s) for s in subsets])
        f = delta[masks]
        c_q = float(np.var(f))
        v = len(subsets)
        f_centered = f - f.mean()

        big_e = np.zeros((v, big_n))
        for row_idx, s in enumerate(subsets):
            big_e[row_idx, [ground.index(g) for g in s]] = 1.0

        mu_e = big_e.T @ f_centered / v  # Cov(f, e_j) for each j

        # vectorized pairwise mu_jk: M[j,k] = mean(f_centered * e_j * e_k)
        m_full = (big_e * f_centered[:, None]).T @ big_e / v
        mu_pairs = np.array([m_full[a, b] for a, b in pairs])

        mu_vec = np.concatenate([mu_e, mu_pairs])
        gram = build_gram_matrix(big_n, q, pairs)
        gram_pinv = np.linalg.pinv(gram)
        e_le2 = float(mu_vec @ gram_pinv @ mu_vec)  # E_{<=2} = E_1 + E_2

        e1 = (
            float(np.sum(mu_e**2) * big_n * (big_n - 1) / (q * (big_n - q)))
            if q * (big_n - q) > 0
            else 0.0
        )
        e2 = e_le2 - e1

        rows.append(
            {
                "q": q,
                "N": big_n,
                "C_q": c_q,
                "E1": e1,
                "E_le2": e_le2,
                "E2": e2,
                "E2_frac_of_Cq": e2 / c_q if c_q > 0 else float("nan"),
            }
        )
        print(
            f"  q={q:2d}/{big_n:2d}  C_q={c_q:.6f}  E1={e1:.6f}  E_le2={e_le2:.6f}  "
            f"E2={e2:.6f}  E2/Cq={e2 / c_q:.4f}"
            if c_q > 0
            else f"  q={q}: C_q=0",
            flush=True,
        )
    return rows


def cross_validate(n_values: list[str]) -> bool:
    """Mandatory positive control: verify E_le2 = E_1+E_2 recovers the exact E_1+E_2 computed
    from full diagonalization (sum of the two lowest-gap levels) at n=23,29,31."""
    with open(METRICS / "johnson_eigenspace_decomposition.json", encoding="utf-8") as f:
        exact = json.load(f)

    all_ok = True
    for n_str in n_values:
        rows = l2_energy_per_layer(int(n_str))
        exact_rows = {r["q"]: r for r in exact[n_str]}
        print(f"\n--- cross-validation n={n_str} ---")
        for r in rows:
            q = r["q"]
            levels_sorted = sorted(exact_rows[q]["levels"], key=lambda lv: lv["gap"])
            exact_e1 = levels_sorted[0]["energy"] if len(levels_sorted) > 0 else 0.0
            exact_e2 = levels_sorted[1]["energy"] if len(levels_sorted) > 1 else 0.0
            exact_le2 = exact_e1 + exact_e2
            err = abs(exact_le2 - r["E_le2"])
            rel_err = err / exact_le2 if exact_le2 > 1e-9 else err
            ok = rel_err < 0.02
            all_ok = all_ok and ok
            print(
                f"  q={q:2d}  exact_E1+E2={exact_le2:.6f}  computed_E_le2={r['E_le2']:.6f}  "
                f"rel_err={rel_err:.4f}  ok={ok}"
            )
    return all_ok


if __name__ == "__main__":
    print("=== Cross-validation: E_le2 vs exact diagonalization's E1+E2 (n=23,29,31) ===")
    validated = cross_validate(["23", "29", "31"])
    print(f"\nCross-validation passed: {validated}")
    if not validated:
        raise RuntimeError("l=2 energy computation does NOT match exact diagonalization.")

    print("\n=== Extending to n=37,41,43,47 ===")
    out = {}
    for n in [37, 41, 43, 47]:
        print(f"\n--- n={n} ---")
        out[n] = l2_energy_per_layer(n)

    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "l2_pairwise_energy.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
