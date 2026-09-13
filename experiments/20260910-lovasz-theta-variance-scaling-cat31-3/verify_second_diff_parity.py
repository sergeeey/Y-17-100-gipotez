"""Verify analytically (via direct Walsh-Hadamard transform, same method as
check_delta_i_even_parity.py) that Delta_i Delta_j X -- viewed as a function of the remaining
m-2 coordinates -- has its Fourier spectrum confined to ODD degree levels, for PRIME n (the
only n this experiment's circulant-graph construction is actually used with -- n=23,29,31,37,
41,43,47 throughout).

Chain of standard shift-identity applications (each already established/cited in this
experiment, points 11 and 32): X has spectrum on ODD |T| (point 11, pre-existing). D_i X (=
delta_i, single difference) has spectrum on EVEN |T| (point 32, via the shift identity
(D_i f)^(T) = f_hat(T union {i})). Applying the SAME shift identity a second time to D_j(D_i X)
predicts spectrum on ODD |T| again. Confirmed exactly at n=17,19 (even_fraction ~1e-29..1e-31,
pure floating noise). This analytically explains (not just empirically observes) the exact
frac(Delta<=0)=0.5, mean=0 pattern found in check_submodularity_second_differences.py: a
function with purely-odd-degree Fourier spectrum satisfies g(S) = -g(complement of S) exactly
(standard fact: chi_T(-x)=(-1)^|T| chi_T(x)), so as S ranges uniformly over all subsets, {g(S)}
is symmetric around 0 by construction -- a naive sign/mean test of submodularity is therefore
STRUCTURALLY uninformative for this X, independent of any interesting or uninteresting content.

Side-finding, OUT OF SCOPE for this experiment (recorded here, not chased further): the SAME
check at COMPOSITE n (15, 21) gives a clean 50/50 split too, but for an entirely different and
mundane reason -- `theta_full` contains exact zeros for some generator-subsets at composite n,
making `log(theta_full/sqrt(n))` produce -inf/NaN (confirmed directly: X's own base odd-parity
check, run at n=13,15,17,19,21,23, gives NaN precisely at n=15,21 and clean 1.0 odd-fraction at
every prime n tested). This experiment's whole construction (`theta_via_lp`,
`solve_orbit_reduced`) has evidently only ever been exercised at prime n -- composite n breaks
the pipeline outright (degenerate/disconnected circulant graphs for certain generator subsets),
not the parity property specifically. Not investigated further since it is outside this
experiment's actual n-range; flagged as a Pearl in decision.md for anyone extending this
pipeline to composite n later.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

HERE = Path(
    r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez"
    r"\experiments\20260910-lovasz-theta-variance-scaling-cat31-3"
)

necklace_spec = importlib.util.spec_from_file_location(
    "necklace_mod_parity2", HERE / "check_necklace_orbit_reduction.py"
)
nm = importlib.util.module_from_spec(necklace_spec)
necklace_spec.loader.exec_module(nm)


def fwht(a: np.ndarray) -> np.ndarray:
    a = a.astype(np.float64).copy()
    n = len(a)
    h = 1
    while h < n:
        for i in range(0, n, h * 2):
            for j in range(i, i + h):
                x, y = a[j], a[j + h]
                a[j] = x + y
                a[j + h] = x - y
        h *= 2
    return a


def popcount(x: int) -> int:
    return bin(x).count("1")


def verify(n: int, i: int, j: int):
    m = (n - 1) // 2
    res = nm.solve_orbit_reduced(n, verbose=False)
    theta_full = res["theta_full"]
    x = np.log(theta_full / np.sqrt(n))

    rest_bits = [b for b in range(m) if b not in (i, j)]
    n_rest = len(rest_bits)
    g = np.empty(1 << n_rest)
    for idx in range(1 << n_rest):
        base = 0
        for k, b in enumerate(rest_bits):
            if idx & (1 << k):
                base |= 1 << b
        S, Si, Sj, Sij = base, base | (1 << i), base | (1 << j), base | (1 << i) | (1 << j)
        g[idx] = x[S] - x[Si] - x[Sj] + x[Sij]

    ghat = fwht(g) / len(g)
    even_energy = sum(ghat[t] ** 2 for t in range(len(ghat)) if popcount(t) % 2 == 0)
    odd_energy = sum(ghat[t] ** 2 for t in range(len(ghat)) if popcount(t) % 2 == 1)
    total = even_energy + odd_energy
    print(
        f"n={n} i={i} j={j}: even_fraction={even_energy / total:.2e}  "
        f"odd_fraction={odd_energy / total:.6f}  (expect: odd~1.0, even~0)"
    )


if __name__ == "__main__":
    print("--- primary check: prime n (this experiment's actual domain) ---")
    for n in (17, 19):
        verify(n, i=0, j=1)

    print("\n--- side-probe only, OUT OF SCOPE: composite n, multiple (i,j) pairs ---")
    print("(expect NaN or a degenerate 50/50 split from theta_full's exact zeros, not a")
    print(" genuine parity violation -- see module docstring)")
    for i, j in [(0, 1), (1, 2)]:
        verify(21, i=i, j=j)
