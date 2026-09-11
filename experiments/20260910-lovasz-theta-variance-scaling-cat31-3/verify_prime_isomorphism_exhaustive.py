"""Exhaustive (not sampled) verification of the deterministic isomorphism claim underlying
the prime-n generator-homogeneity theorem in decision.md's Addendum § 4:

    For n prime and a a unit mod n, theta(G_S) = theta(G_{a*S mod n}) EXACTLY, for every
    fixed generator set S subset {1,...,m}, m=(n-1)/2 -- because multiplication by a is a
    graph automorphism (vertex relabeling) of the circulant graph.

Checked here by brute force over ALL 2^m subsets at a small prime n (n=7, m=3, a=3), not by
sampling -- this is the load-bearing deterministic half of the theorem; the other half
(S -> a*S is a measure-preserving bijection under the product Bernoulli(1/2) measure) is
elementary once the isomorphism claim holds, and is not separately checked here.

Result: max|theta(G_S)-theta(G_aS)| over all 8 subsets = ~5e-15 (floating-point noise only).
"""

from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
H_CAT31_1_DIR = HERE.parent / "20260909-lovasz-theta-random-circulant-graphs"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h_cat31_1 = _load_module("verify_iso_dep_h_cat31_1", H_CAT31_1_DIR / "run.py")
theta_via_lp = h_cat31_1.theta_via_lp

N = 7  # prime
A = 3  # unit mod 7 (gcd(3,7)=1)


def build_c(generator_set: set[int], n: int) -> np.ndarray:
    c = np.zeros(n)
    for i in generator_set:
        c[i] = 1.0
        c[n - i] = 1.0
    return c


def fold(idx: int, n: int, m: int) -> int:
    idx = idx % n
    return idx if idx <= m else n - idx


def run() -> float:
    m = (N - 1) // 2
    max_diff = 0.0
    for r in range(m + 1):
        for combo in itertools.combinations(range(1, m + 1), r):
            s = set(combo)
            a_s = {fold(A * i, N, m) for i in s}
            theta_s = theta_via_lp(build_c(s, N))
            theta_as = theta_via_lp(build_c(a_s, N))
            diff = abs(theta_s - theta_as)
            max_diff = max(max_diff, diff)
            print(
                f"S={sorted(s)} aS={sorted(a_s)} theta(G_S)={theta_s:.6f} "
                f"theta(G_aS)={theta_as:.6f} diff={diff:.2e}"
            )
    print(f"\nmax |theta(G_S)-theta(G_aS)| over all {2**m} subsets: {max_diff:.2e}")
    return max_diff


if __name__ == "__main__":
    run()
