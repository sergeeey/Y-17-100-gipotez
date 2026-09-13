"""Route C, stage C2: cheap empirical falsification -- compute M_r(q) = <f, L^r f> for
r=1,2,3 DIRECTLY via the swap operator L=I-P (no per-level E_l truncation, which would risk
undercounting since points 22-24 already showed spectral mass migrating to high l).

Setup (matches point 15's own, reusing its exact delta data unchanged): within Hamming layer q
(S a q-subset of the N=m-1 remaining generators, i=bit0 excluded), f(S):=delta_i(S). The layer's
swap graph J(N,q) is d-regular (d=q(N-q)), vertex-transitive, uniform-stationary. Its simple
random walk operator P: (Pf)(S) = (1/d) * sum over single-swap-neighbors S' of f(S'). L:=I-P.

Standard Dirichlet-form identity for a reversible walk (verified against this project's own T_q,
not just cited): T_q = E[(f(S)-f(S'))^2] = 2*<f,Lf> = 2*M_1. This IS already-established math
(points 15-18), used here only as a self-consistency check before trusting M_2, M_3 (genuinely
NOT computed anywhere else in this experiment).

M_2 = <f,L^2 f> = ||Lf||^2 and M_3 = <f,L^3 f> = <Lf, L^2 f> are computed by literally applying
the swap-averaging operator P (hence L) 1, 2, 3 times to the exact f vector and taking inner
products -- no spectral decomposition, no E_l data, no truncation. gamma_l = l(N+1-l)/(q(N-q))
(already established, point 15/17) is itself N-dependent, so raw M2/M1 growing or shrinking with
n does NOT by itself say whether the effective level l_eff is growing or shrinking -- this script
also inverts gamma_l=M2/M1 (and =M3/M2) for l, giving an l_eff directly comparable to point 24's
own notation, and reports l_eff/N to separate "l_eff grows but sub-linearly" from "l_eff grows
linearly with N" (the latter would keep gamma, hence M2/M1, roughly CONSTANT as n grows).
"""

from __future__ import annotations

import importlib.util
import json
import math
from itertools import combinations
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

necklace_spec = importlib.util.spec_from_file_location(
    "necklace_mod_moments", HERE / "check_necklace_orbit_reduction.py"
)
nm = importlib.util.module_from_spec(necklace_spec)
necklace_spec.loader.exec_module(nm)


def build_layer_arrays(n: int, q: int):
    """Returns (masks, mask_to_idx, f) for the q-layer of the (m-1)-element ground set
    (bits 1..m-1, bit0=i excluded), f=delta_i restricted to that layer."""
    m = (n - 1) // 2
    ground = list(range(1, m))  # bits 1..m-1
    N = len(ground)

    res = nm.solve_orbit_reduced(n, verbose=False)
    theta_full = res["theta_full"]
    x = np.log(theta_full / np.sqrt(n))

    n_subsets = 1 << m
    delta = np.empty(n_subsets)
    for mask in range(n_subsets):
        if mask & 1:
            continue
        delta[mask] = x[mask] - x[mask | 1]

    combos = list(combinations(ground, q))
    masks = np.array([sum(1 << b for b in combo) for combo in combos], dtype=np.int64)
    mask_to_idx = {int(mk): i for i, mk in enumerate(masks)}
    f = np.array([delta[mk] for mk in masks], dtype=np.float64)
    return combos, masks, mask_to_idx, f, N


def apply_P(f: np.ndarray, combos, masks, mask_to_idx, ground: list[int]) -> np.ndarray:
    """(Pf)(S) = average of f(S') over all single-swap-neighbors S' of S."""
    out = np.zeros_like(f)
    ground_set_cache = set(ground)
    for idx, (combo, mask) in enumerate(zip(combos, masks)):
        in_set = combo
        out_set = [b for b in ground_set_cache if b not in in_set]
        acc = 0.0
        cnt = 0
        for a in in_set:
            base = int(mask) & ~(1 << a)
            for b in out_set:
                neighbor_mask = base | (1 << b)
                acc += f[mask_to_idx[neighbor_mask]]
                cnt += 1
        out[idx] = acc / cnt if cnt else 0.0
    return out


def l_eff_from_gamma(gamma: float, N: int, q: int) -> float:
    """Invert gamma_l = l(N+1-l)/(q(N-q)) for l (smaller root), giving an effective level
    directly comparable to point 24's own l_eff notation."""
    d = q * (N - q)
    a, b, c = 1.0, -(N + 1), gamma * d
    disc = b * b - 4 * a * c
    if disc < 0:
        return float("nan")
    return (-b - math.sqrt(disc)) / (2 * a)


def run_one(n: int) -> dict:
    m = (n - 1) // 2
    ground = list(range(1, m))
    N = len(ground)
    q = N // 2  # central layer, matching the convention used throughout points 15-31

    combos, masks, mask_to_idx, f, _ = build_layer_arrays(n, q)
    f_centered = f - f.mean()

    Lf = f_centered - apply_P(f_centered, combos, masks, mask_to_idx, ground)
    L2f = Lf - apply_P(Lf, combos, masks, mask_to_idx, ground)
    L3f = L2f - apply_P(L2f, combos, masks, mask_to_idx, ground)

    v = len(f_centered)
    C_q = float(np.var(f_centered))
    M1 = float(np.dot(f_centered, Lf) / v)
    M2 = float(np.dot(f_centered, L2f) / v)
    M3 = float(np.dot(f_centered, L3f) / v)

    # cross-check against already-established T_q = 2*M1 (point 15's own definition)
    d = q * (N - q)
    sq_diffs = []
    for combo, mask in zip(combos, masks):
        in_set = combo
        out_set = [b for b in ground if b not in in_set]
        fs = f_centered[mask_to_idx[int(mask)]]
        for a in in_set:
            base = int(mask) & ~(1 << a)
            for b in out_set:
                neighbor_mask = base | (1 << b)
                sq_diffs.append((fs - f_centered[mask_to_idx[neighbor_mask]]) ** 2)
    T_q_direct = float(np.mean(sq_diffs))

    gamma_21 = M2 / M1 if M1 else float("nan")
    gamma_32 = M3 / M2 if M2 else float("nan")
    l_eff_21 = l_eff_from_gamma(gamma_21, N, q)
    l_eff_32 = l_eff_from_gamma(gamma_32, N, q)

    result = {
        "n": n,
        "N": N,
        "q": q,
        "d": d,
        "C_q": C_q,
        "M1": M1,
        "M2": M2,
        "M3": M3,
        "M2_over_M1": gamma_21,
        "M3_over_M2": gamma_32,
        "M2_over_Cq": M2 / C_q if C_q else float("nan"),
        "l_eff_from_M2_M1": l_eff_21,
        "l_eff_from_M2_M1_over_N": l_eff_21 / N,
        "l_eff_from_M3_M2": l_eff_32,
        "l_eff_from_M3_M2_over_N": l_eff_32 / N,
        "T_q_direct": T_q_direct,
        "2_times_M1": 2 * M1,
        "consistency_check_T_q_vs_2M1": abs(T_q_direct - 2 * M1) / T_q_direct
        if T_q_direct
        else None,
    }
    print(
        f"n={n:3d} N={N:2d} q={q:2d}  C_q={C_q:.6f}  M1={M1:.6f}  M2={M2:.6f}  M3={M3:.6f}  "
        f"M2/M1={gamma_21:.4f}  M3/M2={gamma_32:.4f}  M2/Cq={result['M2_over_Cq']:.4f}  "
        f"l_eff(M2/M1)={l_eff_21:.4f} (l_eff/N={l_eff_21 / N:.4f})  "
        f"[consistency T_q vs 2M1: {result['consistency_check_T_q_vs_2M1']:.2e}]",
        flush=True,
    )
    return result


def run(n_values):
    return [run_one(n) for n in n_values]


if __name__ == "__main__":
    rows = run([23, 29, 31, 37])
    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "higher_moments_M_r.json", "w", encoding="utf-8") as f:
        json.dump({"rows": rows}, f, indent=2)
