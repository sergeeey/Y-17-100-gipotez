"""Point 38: extend point 33's M_1,M_2,M_3 to M_1..M_6 across ALL n already used in this
experiment (23,29,31,37,41,43,47), per the external re-plan's item 3 -- cheap since it reuses
the already-verified L=I-P construction, just applied 6 times instead of 3. No new theta-solve
machinery -- same solve_orbit_reduced call as every other script in this experiment.

Adds one new diagnostic not computed anywhere else in this experiment: rho_gamma := M1*M3/M2^2.
By Cauchy-Schwarz applied to the spectral moments (M_r = sum_l gamma_l^r E_l is an inner product
of the sequence (gamma_l^{r/2} sqrt(E_l))_l with itself under different weightings), rho_gamma>=1
always; rho_gamma close to 1 indicates the spectral mass is concentrated near a single "typical"
gamma_l (a slowly-moving bump); rho_gamma growing indicates a heavier/wider spectral tail.
"""

from __future__ import annotations

import importlib.util
import json
import time
from itertools import combinations
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

necklace_spec = importlib.util.spec_from_file_location(
    "necklace_mod_m6", HERE / "check_necklace_orbit_reduction.py"
)
nm = importlib.util.module_from_spec(necklace_spec)
necklace_spec.loader.exec_module(nm)

hm_spec = importlib.util.spec_from_file_location(
    "higher_moments_mod_m6", HERE / "check_higher_moments_M_r.py"
)
hm = importlib.util.module_from_spec(hm_spec)
hm_spec.loader.exec_module(hm)


def apply_L_to_layer(values, combos, masks, mask_to_idx, ground_set):
    out = np.empty_like(values)
    for idx, (combo, mask) in enumerate(zip(combos, masks)):
        out_set = [b for b in ground_set if b not in combo]
        acc = 0.0
        cnt = 0
        for a in combo:
            base = int(mask) & ~(1 << a)
            for b in out_set:
                neighbor = base | (1 << b)
                acc += values[mask_to_idx[neighbor]]
                cnt += 1
        out[idx] = values[idx] - (acc / cnt if cnt else 0.0)
    return out


def run_one(n: int, r_max: int = 6) -> dict:
    print(f"=== n={n} ===", flush=True)
    t0 = time.time()
    m = (n - 1) // 2
    res = nm.solve_orbit_reduced(n, verbose=False)
    theta_full = res["theta_full"]
    x = np.log(theta_full / np.sqrt(n))
    theta_time = time.time() - t0
    print(f"  [theta computed in {theta_time:.1f}s]", flush=True)

    ground = list(range(1, m))
    N = len(ground)
    ground_set = set(ground)
    q = N // 2
    d = q * (N - q)

    t1 = time.time()
    combos_q = list(combinations(ground, q))
    masks_q = [sum(1 << b for b in c) for c in combos_q]
    mask_to_idx_q = {mk: i for i, mk in enumerate(masks_q)}
    v_q = len(masks_q)

    delta_q = np.array([x[mk] - x[mk | 1] for mk in masks_q])
    f_centered = delta_q - delta_q.mean()
    C_q = float(np.var(delta_q))

    Lf_list = []
    Lf = f_centered
    for _ in range(r_max):
        Lf = apply_L_to_layer(Lf, combos_q, masks_q, mask_to_idx_q, ground_set)
        Lf_list.append(Lf)

    M = {r: float(np.dot(f_centered, Lf_list[r - 1])) / v_q for r in range(1, r_max + 1)}
    ratios = {
        f"M{r + 1}_over_M{r}": (M[r + 1] / M[r] if M[r] else float("nan")) for r in range(1, r_max)
    }
    l_eff = {
        f"l_eff_from_M{r + 1}_M{r}": hm.l_eff_from_gamma(M[r + 1] / M[r], N, q)
        if M[r]
        else float("nan")
        for r in range(1, r_max)
    }
    rho_gamma = M[1] * M[3] / (M[2] ** 2) if M[2] else float("nan")

    elapsed = time.time() - t1
    result = {
        "n": n,
        "N": N,
        "q": q,
        "d": d,
        "v_q": v_q,
        "theta_time_s": theta_time,
        "moments_time_s": elapsed,
        "C_q": C_q,
        **{f"M{r}": M[r] for r in range(1, r_max + 1)},
        **ratios,
        **l_eff,
        "rho_gamma_M1M3_over_M2sq": rho_gamma,
    }
    print(
        f"  M1..M{r_max}=" + ", ".join(f"{M[r]:.6f}" for r in range(1, r_max + 1)),
        flush=True,
    )
    print(
        f"  rho_gamma(M1*M3/M2^2)={rho_gamma:.6f}  "
        f"l_eff(M2/M1)={l_eff['l_eff_from_M2_M1']:.4f}  "
        f"[theta {theta_time:.1f}s + moments {elapsed:.1f}s]",
        flush=True,
    )
    return result


def run(n_values: list[int], r_max: int = 6) -> list[dict]:
    METRICS.mkdir(exist_ok=True)
    out_path = METRICS / "higher_moments_M1_M6.json"
    all_results: list[dict] = []
    if out_path.exists():
        with open(out_path, encoding="utf-8") as f:
            all_results = json.load(f).get("rows", [])
    done_ns = {r["n"] for r in all_results}
    for n in n_values:
        if n in done_ns:
            print(f"=== n={n} already done, skipping ===", flush=True)
            continue
        all_results.append(run_one(n, r_max=r_max))
        all_results.sort(key=lambda r: r["n"])
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({"rows": all_results}, f, indent=2)
    return all_results


if __name__ == "__main__":
    run([23, 29, 31, 37, 41, 43, 47])
    print("\nDone.", flush=True)
