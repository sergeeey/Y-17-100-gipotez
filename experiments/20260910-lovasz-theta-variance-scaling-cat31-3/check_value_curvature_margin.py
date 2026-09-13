"""Priority B ("value-curvature" route), per frontier_after_point50.md Block 4: does the
discrete mixed second difference of the LOG-VALUE, Delta_i Delta_j X(S), get controlled by
LOCAL structure of the active LP constraints near a tie (dual slack / margin / a near-
degeneracy indicator), WITHOUT ever needing the norm of the difference between two optimal
dual vectors (the exact quantity that killed the closed-route in points 6, 8, 9a, 31)?

Two candidate structural forms are tested, pre-registered before any computation (Falsification
Ladder discipline):

  H1 (margin-domination form). Define, for a single LP solve, margin_min = the smallest
  |slack| among the INACTIVE (Fx>=0) inequality constraints at that optimum -- i.e. how close
  the "next" constraint is to becoming tight (a standard LP near-degeneracy indicator, no norm
  of a dual-vector DIFFERENCE required -- this is a property of ONE vertex, not a distance
  between two). For a quadruple (S, S+i, S+j, S+i+j), define M(S,i,j) = min over the 4 corners'
  margin_min (the single most fragile corner of the square). H1 predicts a real, detectable
  NEGATIVE monotonic relationship between M and |Delta_i Delta_j X(S)|: small margin (near a
  tie somewhere in the square) co-occurs with large curvature, large margin with small
  curvature. Falsified if the Spearman correlation is weak (|rho|<0.3 or p>=0.05, thresholds
  fixed before running) OR if clean counterexamples exist (large M together with large
  |Delta_i Delta_j X|).

  H2 (restructure-gating form). Reusing point 31's OWN verified "genuine restructure" criterion
  (active_full NOT a subset of active_rest, where "full"=corner with the flipped generator ON,
  "rest"=corner with it OFF -- exactly point 31's direction, applied here to all 4 edges of the
  (i,j)-square: S<->S+i, S+j<->S+i+j, S<->S+j, S+i<->S+i+j), define R(S,i,j)=1 if ANY of the 4
  edges is a genuine restructure, else 0. H2 predicts |Delta_i Delta_j X(S)| is small whenever
  R=0 (no active-set change anywhere on the square) and can be large only when R=1. Falsified
  if the R=0 group's |Delta_i Delta_j X| distribution is NOT substantially smaller than the R=1
  group's (no separation).

Reuses point 31's own verified `solve_lp` mechanics (time-domain primal LP, Table 1,
arXiv:2603.29571) rather than re-deriving them -- extended only to also return the raw slack
vector (point 31's version already returns theta + active_set; margin_min needs the slacks
themselves, not just which are active). Positive control: spot-checks this file's own
`solve_lp_with_slacks` against H-CAT31-1's independently-verified `theta_via_lp` before trusting
any new number.

Restricted to PRIME n only, matching every other point in this experiment past point 36 (point
37's own side-finding: `theta_via_lp`/orbit reduction produces degenerate/zero theta for some
generator-subsets at composite n).
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
from scipy import stats
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
H_CAT31_1_DIR = HERE.parent / "20260909-lovasz-theta-random-circulant-graphs"
METRICS = HERE / "metrics"

ACTIVE_TOL = 1e-7  # same tolerance as point 31's check_vertex_stability_probability.py


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h_cat31_1 = _load_module("curvature_margin_dep_h_cat31_1", H_CAT31_1_DIR / "run.py")
theta_via_lp = h_cat31_1.theta_via_lp


def solve_lp_with_slacks(n: int, edges_on: set[int]):
    """Point 31's own `solve_lp`, extended to also return the raw slack vector (needed for
    margin_min; point 31 itself only needed the active SET, not the slack magnitudes)."""
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
        if kk in edges_on:
            row = np.zeros(n)
            row[kk] = 1.0
            a_eq_rows.append(row)
            b_eq.append(0.0)
    a_eq = np.array(a_eq_rows)

    a_ub = -re_f
    b_ub = np.zeros(n)

    res = linprog(
        c=-np.ones(n),
        A_ub=a_ub,
        b_ub=b_ub,
        A_eq=a_eq,
        b_eq=b_eq,
        bounds=(None, None),
        method="highs",
    )
    if not res.success:
        return None, None, None
    x_star = res.x
    slacks = a_ub @ x_star - b_ub  # <=0 by feasibility; ~0 means constraint tight
    active_set = frozenset(int(kk) for kk in range(n) if abs(slacks[kk]) < ACTIVE_TOL)
    return -res.fun, active_set, slacks


def margin_min(active_set: frozenset, slacks: np.ndarray, n: int) -> float:
    inactive_abs = [abs(slacks[kk]) for kk in range(n) if kk not in active_set]
    return float(min(inactive_abs)) if inactive_abs else float("nan")


def genuine_restructure(active_full: frozenset, active_rest: frozenset) -> bool:
    """Point 31's exact criterion: 'full' = corner with the generator ON, 'rest' = corner with
    it dropped/OFF. Trivial DOF growth iff active_full subset of active_rest; genuine
    restructure otherwise (some previously-active constraint becomes inactive)."""
    return not active_full.issubset(active_rest)


def mask_to_edges(mask: int, m: int, n: int) -> set[int]:
    edges: set[int] = set()
    for b in range(m):
        if mask & (1 << b):
            k = b + 1
            edges.add(k)
            edges.add(n - k)
    return edges


def positive_control(n_values=(23, 29, 37), n_checks=5, seed=42) -> dict:
    """Spot-check solve_lp_with_slacks's theta against the independently-verified
    theta_via_lp, before trusting any new number from this file."""
    rng = np.random.default_rng(seed)
    rows = []
    max_abs_diff = 0.0
    for n in n_values:
        m = (n - 1) // 2
        for _ in range(n_checks):
            mask = int(rng.integers(0, 1 << m))
            edges = mask_to_edges(mask, m, n)
            c = np.zeros(n)
            for k in edges:
                c[k] = 1.0
            theta_ref = theta_via_lp(c)
            theta_new, _, _ = solve_lp_with_slacks(n, edges)
            diff = abs(theta_ref - theta_new)
            max_abs_diff = max(max_abs_diff, diff)
            rows.append(
                {"n": n, "mask": mask, "theta_ref": theta_ref, "theta_new": theta_new, "diff": diff}
            )
    return {"rows": rows, "max_abs_diff": max_abs_diff, "passed": bool(max_abs_diff < 1e-8)}


def run_one_n(n: int, n_samples: int, seed_base: int) -> dict:
    m = (n - 1) // 2
    rng = np.random.default_rng(seed_base + n)

    M_vals = []
    delta_vals = []  # signed, not just |Delta| -- needed for a model-free std(Delta)
    abs_delta_vals = []
    R_vals = []
    density_vals = []  # popcount(base_mask)/m -- for the F7 density-confound check
    ij_dist_vals = []  # |i-j| -- same purpose
    n_solved = 0
    n_failed = 0

    for _ in range(n_samples):
        i, j = rng.choice(m, size=2, replace=False)
        i, j = int(i), int(j)
        rest_bits = [b for b in range(m) if b not in (i, j)]
        base_mask = 0
        for b in rest_bits:
            if rng.random() < 0.5:
                base_mask |= 1 << b

        mask_S = base_mask
        mask_Si = base_mask | (1 << i)
        mask_Sj = base_mask | (1 << j)
        mask_Sij = base_mask | (1 << i) | (1 << j)

        corners = {}
        ok = True
        for label, mask in (("S", mask_S), ("Si", mask_Si), ("Sj", mask_Sj), ("Sij", mask_Sij)):
            edges = mask_to_edges(mask, m, n)
            theta, active_set, slacks = solve_lp_with_slacks(n, edges)
            if theta is None:
                ok = False
                break
            corners[label] = {
                "theta": theta,
                "active_set": active_set,
                "margin": margin_min(active_set, slacks, n),
            }
        if not ok:
            n_failed += 1
            continue
        n_solved += 1

        X = {lbl: float(np.log(c["theta"] / np.sqrt(n))) for lbl, c in corners.items()}
        delta = X["S"] - X["Si"] - X["Sj"] + X["Sij"]
        abs_delta = abs(delta)

        # defensive: min() over an iterable containing NaN is order-dependent in Python: row 0
        # of ReF is all-ones, so slack_0=-theta<=-1 always, making index 0 always inactive and
        # inactive_abs always nonempty -- NaN cannot occur here (confirmed empirically: every
        # row below has n_pairs_used_for_correlation==n_solved), but guard explicitly rather
        # than rely on that invariant silently (skeptic-fallback finding, point 51).
        corner_margins = [corners[lbl]["margin"] for lbl in corners]
        M_quad = float("nan") if any(np.isnan(v) for v in corner_margins) else min(corner_margins)

        density_vals.append(bin(base_mask).count("1") / m)
        ij_dist_vals.append(abs(i - j))
        delta_vals.append(delta)

        # 4 edges of the square, each per point 31's exact "full"=ON,"rest"=OFF convention.
        r1 = genuine_restructure(
            corners["Si"]["active_set"], corners["S"]["active_set"]
        )  # i: S<->Si
        r2 = genuine_restructure(
            corners["Sj"]["active_set"], corners["S"]["active_set"]
        )  # j: S<->Sj
        r3 = genuine_restructure(
            corners["Sij"]["active_set"], corners["Sj"]["active_set"]
        )  # i on top of j
        r4 = genuine_restructure(
            corners["Sij"]["active_set"], corners["Si"]["active_set"]
        )  # j on top of i
        R = int(r1 or r2 or r3 or r4)

        M_vals.append(M_quad)
        abs_delta_vals.append(abs_delta)
        R_vals.append(R)

    M_arr = np.array(M_vals)
    D_arr = np.array(abs_delta_vals)
    signed_D_arr = np.array(delta_vals)
    R_arr = np.array(R_vals)
    density_arr = np.array(density_vals)
    ij_dist_arr = np.array(ij_dist_vals)

    finite_mask = np.isfinite(M_arr) & np.isfinite(D_arr)
    M_arr_f = M_arr[finite_mask]
    D_arr_f = D_arr[finite_mask]

    if len(M_arr_f) >= 10:
        rho, pval = stats.spearmanr(M_arr_f, D_arr_f)
    else:
        rho, pval = float("nan"), float("nan")

    d0 = D_arr[R_arr == 0]
    d1 = D_arr[R_arr == 1]
    if len(d0) >= 5 and len(d1) >= 5:
        mw_stat, mw_p = stats.mannwhitneyu(d0, d1, alternative="less")
    else:
        mw_stat, mw_p = float("nan"), float("nan")

    # skeptic-fallback additions (point 51 review): (a) MW on M itself between R-groups --
    # does the margin quantity even predict restructuring; (b) Spearman restricted to the R=1
    # subset alone -- does margin add anything once restructuring has already occurred;
    # (c) exact, model-free std(Delta) (not the folded-normal-approximated |Delta| mean) for a
    # cleaner cross-check against point 37's own std(Delta); (d) density/|i-j| means per
    # R-group, to check the F7 confound (does R=0 skew toward denser base sets, which would
    # make part of the R0-vs-R1 separation an artifact of density rather than of churn alone).
    m0 = M_arr[R_arr == 0]
    m1 = M_arr[R_arr == 1]
    m0_f, m1_f = m0[np.isfinite(m0)], m1[np.isfinite(m1)]
    if len(m0_f) >= 5 and len(m1_f) >= 5:
        mw_M_stat, mw_M_p = stats.mannwhitneyu(m0_f, m1_f)
    else:
        mw_M_stat, mw_M_p = float("nan"), float("nan")

    mask_r1 = (R_arr == 1) & finite_mask
    if mask_r1.sum() >= 10:
        rho_r1, pval_r1 = stats.spearmanr(M_arr[mask_r1], D_arr[mask_r1])
    else:
        rho_r1, pval_r1 = float("nan"), float("nan")

    std_delta_exact = float(np.std(signed_D_arr, ddof=0))

    return {
        "n": n,
        "m": m,
        "n_samples_requested": n_samples,
        "n_solved": n_solved,
        "n_failed": n_failed,
        "spearman_rho_M_vs_absDelta": float(rho),
        "spearman_pvalue": float(pval),
        "n_pairs_used_for_correlation": len(M_arr_f),
        "restructure_fraction": float(R_arr.mean()) if len(R_arr) else float("nan"),
        "group_R0": {
            "n": len(d0),
            "mean_absDelta": float(d0.mean()) if len(d0) else None,
            "median_absDelta": float(np.median(d0)) if len(d0) else None,
            "max_absDelta": float(d0.max()) if len(d0) else None,
            "mean_density": float(density_arr[R_arr == 0].mean()) if len(d0) else None,
            "mean_ij_dist": float(ij_dist_arr[R_arr == 0].mean()) if len(d0) else None,
        },
        "group_R1": {
            "n": len(d1),
            "mean_absDelta": float(d1.mean()) if len(d1) else None,
            "median_absDelta": float(np.median(d1)) if len(d1) else None,
            "max_absDelta": float(d1.max()) if len(d1) else None,
            "mean_density": float(density_arr[R_arr == 1].mean()) if len(d1) else None,
            "mean_ij_dist": float(ij_dist_arr[R_arr == 1].mean()) if len(d1) else None,
        },
        "mannwhitney_R0_less_than_R1": {"stat": float(mw_stat), "pvalue": float(mw_p)},
        "mannwhitney_M_R0_vs_R1": {"stat": float(mw_M_stat), "pvalue": float(mw_M_p)},
        "spearman_within_R1": {
            "rho": float(rho_r1),
            "pvalue": float(pval_r1),
            "n": int(mask_r1.sum()),
        },
        "std_delta_exact": std_delta_exact,
        "M_summary": {
            "min": float(M_arr_f.min()) if len(M_arr_f) else None,
            "median": float(np.median(M_arr_f)) if len(M_arr_f) else None,
            "max": float(M_arr_f.max()) if len(M_arr_f) else None,
        },
        "absDelta_summary": {
            "min": float(D_arr.min()) if len(D_arr) else None,
            "median": float(np.median(D_arr)) if len(D_arr) else None,
            "max": float(D_arr.max()) if len(D_arr) else None,
        },
    }


def run(n_values=(23, 29, 37), n_samples=3000, seed_base=339000) -> dict:
    control = positive_control()
    if not control["passed"]:
        out = {"status": "BLOCKED-INFRASTRUCTURE", "positive_control": control}
        METRICS.mkdir(exist_ok=True)
        with open(METRICS / "value_curvature_margin_check.json", "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2)
        print(json.dumps(out, indent=2))
        return out

    rows = [run_one_n(n, n_samples, seed_base) for n in n_values]
    out = {"status": "OK", "positive_control": control, "rows": rows}
    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "value_curvature_margin_check.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    for row in rows:
        print(
            f"n={row['n']:3d} solved={row['n_solved']:5d} "
            f"rho(M,|D|)={row['spearman_rho_M_vs_absDelta']:.4f} p={row['spearman_pvalue']:.4g} "
            f"restructure_frac={row['restructure_fraction']:.3f} "
            f"E[|D||R=0]={row['group_R0']['mean_absDelta']} (n={row['group_R0']['n']}) "
            f"E[|D||R=1]={row['group_R1']['mean_absDelta']} (n={row['group_R1']['n']}) "
            f"MW_p(R0<R1)={row['mannwhitney_R0_less_than_R1']['pvalue']:.4g}",
            flush=True,
        )
    return out


if __name__ == "__main__":
    run()
