"""Necklace/orbit-reduced exact enumeration for PRIME n, per direct user request and design:
Z_n^x/{+-1} is cyclic of order m=(n-1)/2 (multiplicative group of a finite field is cyclic;
quotient of a cyclic group is cyclic) and acts TRANSITIVELY on the m generator coordinates
(already proved, decision.md point 4) -- transitivity of an order-m group on m points forces
a REGULAR (free) action (orbit-stabilizer: |orbit|=|G|/|stab|=m=|G| means |stab|=1
everywhere), so after labeling coordinates via a primitive root the action is literally cyclic
rotation. Since theta(G_S)=theta(G_{aS}) exactly for units a (same point-4 theorem), X is
CONSTANT on each cyclic-rotation orbit of subsets S subset {1,...,m} -- i.e. on each binary
necklace of length m. Only one LP solve per necklace-orbit is needed, not one per subset.

For ODD m, complementation (S -> {1,...,m}\\S) maps every necklace-orbit to a DIFFERENT orbit
(never itself: |S|=|S^c| would need m=2|S|, impossible for odd m), and X(S^c)=-X(S) exactly
(already-proven antisymmetry). So orbits pair up completely for odd m; only one LP solve per
PAIR is needed (theta for the complement orbit obtained via theta(Gbar)=n/theta(G), no LP).

CRITICAL: this script does NOT trust the above reasoning on faith. It first re-derives the
necklace-orbit structure for n=23 (m=11, ALREADY fully solved exhaustively in
check_exact_walsh_decomposition.py / check_hamming_layer_decomposition.py) and checks the
orbit-reduced computation reproduces the EXACT SAME full 2^m theta array, element-by-element,
before trusting the method for new, larger n where no independent cross-check exists.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
H_CAT31_1_DIR = HERE.parent / "20260909-lovasz-theta-random-circulant-graphs"
METRICS = HERE / "metrics"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h_cat31_1 = _load_module("necklace_dep_h_cat31_1", H_CAT31_1_DIR / "run.py")
theta_via_lp = h_cat31_1.theta_via_lp


def theta_via_lp_robust(c: np.ndarray) -> float:
    val = theta_via_lp(c)
    if not np.isnan(val):
        return val
    n = len(c)
    j = np.arange(n).reshape(-1, 1)
    k = np.arange(n).reshape(1, -1)
    re_f = np.cos(-2 * np.pi * j * k / n)
    a_eq_rows = []
    b_eq = []
    e0 = np.zeros(n)
    e0[0] = 1.0
    a_eq_rows.append(e0)
    b_eq.append(1.0)
    for kk in range(1, (n - 1) // 2 + 1):
        row = np.zeros(n)
        row[kk] = 1.0
        row[n - kk] = -1.0
        a_eq_rows.append(row)
        b_eq.append(0.0)
    for kk in range(1, n):
        if c[kk] > 0.5:
            row = np.zeros(n)
            row[kk] = 1.0
            a_eq_rows.append(row)
            b_eq.append(0.0)
    res = linprog(
        c=-np.ones(n),
        A_ub=-re_f,
        b_ub=np.zeros(n),
        A_eq=np.array(a_eq_rows),
        b_eq=np.array(b_eq),
        bounds=(None, None),
        method="highs-ipm",
    )
    return -res.fun if res.success else float("nan")


def build_c(n: int, mask: int, m: int, relabel: list[int] | None = None) -> np.ndarray:
    """mask's bit `bit` (0-indexed) controls generator index `relabel[bit]` if given,
    else the natural index `bit+1`."""
    c = np.zeros(n)
    for bit in range(m):
        if mask & (1 << bit):
            k = relabel[bit] if relabel is not None else bit + 1
            c[k] = 1.0
            c[n - k] = 1.0
    return c


def find_primitive_root(n: int) -> int:
    """Smallest primitive root mod prime n (order n-1)."""
    phi = n - 1
    # factorize phi
    factors = set()
    d = 2
    x = phi
    while d * d <= x:
        if x % d == 0:
            factors.add(d)
            while x % d == 0:
                x //= d
        d += 1
    if x > 1:
        factors.add(x)
    for g in range(2, n):
        if all(pow(g, phi // p, n) != 1 for p in factors):
            return g
    raise RuntimeError(f"no primitive root found for n={n}")


def build_relabel(n: int, m: int) -> list[int]:
    """relabel[t] = the NATURAL generator index (1..m) corresponding to position t in the
    primitive-root power ordering, folded via +-k identification (since generator k and n-k
    are the same coordinate). Under THIS relabeling, multiplication by the primitive root g
    acts as a simple cyclic shift t -> t+1 (mod m) on positions -- verified, not assumed, by
    cross_validate_n23() below before being trusted for new n."""
    g = find_primitive_root(n)
    relabel = []
    val = 1
    for _ in range(m):
        k = min(val, n - val)  # fold via +-
        relabel.append(k)
        val = (val * g) % n
    return relabel


def rotate(mask: int, m: int, shift: int) -> int:
    """Cyclically rotate an m-bit mask by `shift` positions."""
    shift %= m
    return ((mask << shift) | (mask >> (m - shift))) & ((1 << m) - 1)


def necklace_representative(mask: int, m: int) -> int:
    return min(rotate(mask, m, s) for s in range(m))


def enumerate_necklace_orbits(m: int) -> dict[int, list[int]]:
    """Returns {representative: [all members]} for all binary necklaces of length m."""
    n_subsets = 1 << m
    seen = np.zeros(n_subsets, dtype=bool)
    orbits: dict[int, list[int]] = {}
    for mask in range(n_subsets):
        if seen[mask]:
            continue
        members = sorted({rotate(mask, m, s) for s in range(m)})
        rep = members[0]
        orbits[rep] = members
        for mem in members:
            seen[mem] = True
    return orbits


def solve_orbit_reduced(n: int, verbose: bool = True) -> dict:
    m = (n - 1) // 2
    relabel = build_relabel(n, m)
    orbits = enumerate_necklace_orbits(m)
    reps = sorted(orbits.keys())

    theta_by_rep: dict[int, float] = {}
    solved_via_lp = 0
    solved_via_complement = 0
    for rep in reps:
        comp_rep = necklace_representative(((1 << m) - 1) ^ rep, m)
        if m % 2 == 1 and comp_rep in theta_by_rep:
            # complement orbit already solved -- use theta(Gbar)=n/theta(G)
            theta_by_rep[rep] = n / theta_by_rep[comp_rep]
            solved_via_complement += 1
        else:
            theta_by_rep[rep] = theta_via_lp_robust(build_c(n, rep, m, relabel))
            solved_via_lp += 1

    # Reconstruct full 2^m array, converting relabeled-position masks back to
    # NATURAL-generator-index masks (bit i (0-indexed) <-> natural index i+1), since
    # theta_full must be indexed the same way as the exhaustive computation to compare.
    def relabeled_to_natural(mask: int) -> int:
        nat = 0
        for pos in range(m):
            if mask & (1 << pos):
                nat |= 1 << (relabel[pos] - 1)
        return nat

    theta_full = np.empty(1 << m)
    for rep, members in orbits.items():
        for mem in members:
            theta_full[relabeled_to_natural(mem)] = theta_by_rep[rep]

    if verbose:
        print(
            f"n={n:3d} m={m:2d} orbits={len(orbits):6d} lp_solves={solved_via_lp:6d} "
            f"complement_reused={solved_via_complement:6d} "
            f"(vs {1 << m} full subsets, {(1 << m) / max(solved_via_lp, 1):.1f}x reduction)",
            flush=True,
        )
    return {
        "n": n,
        "m": m,
        "n_orbits": len(orbits),
        "n_lp_solves": solved_via_lp,
        "n_complement_reused": solved_via_complement,
        "theta_full": theta_full,
    }


def cross_validate_n23() -> bool:
    """Positive control: n=23 already has a known-good exhaustive theta array from earlier
    scripts. Recompute it here both ways and compare element-by-element."""
    n = 23
    m = (n - 1) // 2
    print(f"--- Cross-validation on n={n} (m={m}), known result from prior exhaustive runs ---")

    theta_exhaustive = np.empty(1 << m)
    for mask in range(1 << m):
        theta_exhaustive[mask] = theta_via_lp_robust(build_c(n, mask, m))

    result = solve_orbit_reduced(n, verbose=True)
    theta_orbit = result["theta_full"]

    max_diff = float(np.max(np.abs(theta_exhaustive - theta_orbit)))
    matches = bool(max_diff < 1e-8)
    print(f"max |exhaustive - orbit_reduced| = {max_diff:.2e}  MATCH={matches}")
    return matches


def fwht(a: np.ndarray) -> np.ndarray:
    a = a.astype(np.float64).copy()
    h = 1
    n = len(a)
    while h < n:
        for i in range(0, n, h * 2):
            x = a[i : i + h].copy()
            y = a[i + h : i + 2 * h].copy()
            a[i : i + h] = x + y
            a[i + h : i + 2 * h] = x - y
        h *= 2
    return a


def popcount(x: int) -> int:
    return bin(x).count("1")


def summarize(n: int, theta_full: np.ndarray) -> dict:
    m = (n - 1) // 2
    n_subsets = 1 << m
    x = np.log(theta_full / np.sqrt(n))
    transform = fwht(x) / n_subsets
    level_weight = np.zeros(m + 1)
    level_b = np.zeros(m + 1)
    for mask in range(n_subsets):
        k = popcount(mask)
        level_weight[k] += transform[mask] ** 2
        level_b[k] += k * transform[mask] ** 2
    var_x = float(np.sum(level_weight[1:]))
    b_n = float(np.sum(level_b[1:]))
    w1 = float(level_weight[1])
    w3 = float(level_weight[3]) if m >= 3 else 0.0
    w5 = float(level_weight[5]) if m >= 5 else 0.0
    kappa = b_n / w1 if w1 > 0 else float("nan")
    return {
        "n": n,
        "m": m,
        "exact_Var_X": var_x,
        "exact_W1": w1,
        "exact_W3": w3,
        "exact_W5": w5,
        "exact_B_n": b_n,
        "kappa_n": kappa,
        "n_times_Var_X": n * var_x,
        "n_times_W1": n * w1,
        "n_times_W3": n * w3,
        "residual_over_ES_residual": (var_x - w1) / (b_n - w1) if b_n > w1 else float("nan"),
    }


if __name__ == "__main__":
    ok = cross_validate_n23()
    if not ok:
        raise RuntimeError(
            "Cross-validation FAILED -- orbit-reduced method does not match "
            "exhaustive enumeration. Do NOT trust results for larger n."
        )
    print("\nCross-validation PASSED. Proceeding to new prime n via orbit reduction only.\n")

    rows = []
    for n in [29, 31, 37]:
        res = solve_orbit_reduced(n, verbose=True)
        summary = summarize(n, res["theta_full"])
        summary["n_orbits"] = res["n_orbits"]
        summary["n_lp_solves"] = res["n_lp_solves"]
        rows.append(summary)
        print(
            f"    Var_X={summary['exact_Var_X']:.6f} n*Var_X={summary['n_times_Var_X']:.4f} "
            f"n*W1={summary['n_times_W1']:.4f} n*W3={summary['n_times_W3']:.4f} "
            f"kappa_n={summary['kappa_n']:.4f} "
            f"resid_ratio={summary['residual_over_ES_residual']:.4f}"
        )

    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "necklace_orbit_reduction.json", "w", encoding="utf-8") as f:
        json.dump({"cross_validation_passed": ok, "rows": rows}, f, indent=2)
