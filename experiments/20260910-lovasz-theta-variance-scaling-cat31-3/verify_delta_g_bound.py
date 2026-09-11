"""Verifies an exact, deterministic structural fact used in the third (and, per decision.md's
honest conclusion, also unsuccessful) attempt at the Efron-Stein O(1/n) upper bound: flipping
ONE generator bit i perturbs the LP objective vector g=Fb by exactly

    Delta_g_k = +/- 4*cos(2*pi*k*i/n)   for all k

i.e. |Delta_g_k| <= 4 EXACTLY, for every n and every k -- a bound that does NOT grow with n,
unlike g itself (whose entries are ~sqrt(n log n) typically, per arXiv:2502.16227 Lemma
lem:nlogn_ub). This is checked directly (not assumed) by comparing two directly-computed g
vectors that differ in exactly one generator, at n=3000.
"""

from __future__ import annotations

import numpy as np


def compute_g(n: int, generator_set: set[int]) -> np.ndarray:
    f = np.array([[np.exp(-2j * np.pi * j * k / n) for k in range(n)] for j in range(n)])
    b = np.ones(n)
    half = (n - 1) // 2
    for k in range(1, half + 1):
        if k in generator_set:
            b[k] = -1.0
            b[n - k] = -1.0
    return f @ b


def run() -> dict:
    n = 3000
    i_flip = 777
    s_with = {5, 100, 500, 777, 1200}
    s_without = s_with - {i_flip}

    g_with = compute_g(n, s_with)
    g_without = compute_g(n, s_without)
    delta_g = g_without - g_with

    predicted = np.array([4 * np.cos(2 * np.pi * k * i_flip / n) for k in range(n)])
    max_err = float(np.max(np.abs(delta_g.real - predicted)))
    max_imag = float(np.max(np.abs(delta_g.imag)))
    max_abs = float(np.max(np.abs(delta_g)))

    result = {
        "n": n,
        "i_flip": i_flip,
        "max_abs_error_vs_predicted_4cos": max_err,
        "max_imag_part": max_imag,
        "max_abs_delta_g": max_abs,
        "predicted_bound": 4.0,
        "confirms_exact_bound": max_err < 1e-8 and max_abs <= 4.0 + 1e-8,
    }
    for key, value in result.items():
        print(f"{key}: {value}")
    return result


if __name__ == "__main__":
    run()
