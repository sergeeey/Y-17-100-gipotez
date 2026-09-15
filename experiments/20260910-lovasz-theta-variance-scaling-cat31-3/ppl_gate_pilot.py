"""PPL_gate pilot: is J_n = n^2 * E[x_i^2 * w_i^2] bounded as n grows?

Context (do NOT confuse with other quantities in decision.md):
  - This is NOT T_q from decision.md points 15b-20 (swap-Dirichlet-energy
    E[(delta_i(S)-delta_i(S'))^2]). That quantity is unrelated and was
    already rejected there. PPL_gate / J_n is a brand-new quantity proposed
    by an external AI reviewer on 2026-09-16, checked here for the first
    time.
  - This reuses (read-only) the Point 63 cross-complement construction from
    codex-20260914-susceptibility/CROSS_TURAN_ENERGY_THEORY.md and
    OPTIMAL_ENERGY_PLAN.md, and the already-verified `CertificateLP` class
    from codex-20260914-susceptibility/test_convolution_repair.py. Nothing
    in the codex-20260914-susceptibility/ directory is modified or written
    to -- that is another AI session's work (Unclaimed Work Ownership rule).

Point 63 (verified, SURVIVES-PILOT) proves the deterministic pointwise bound

    delta_i <= 2 * x_i * w_i

for old graph G0 (i absent), new graph G1 = G0 union H_i (i present), x =
feasible optimal time-domain certificate of G0, w = feasible optimal
time-domain certificate of complement(G1), both normalized x_0 = w_0 = 1
with nonnegative Fourier transform (see CROSS_TURAN_ENERGY_THEORY.md,
"Deterministic inequality").

This pilot tests a strengthened *quadratic* consequence, proposed externally
2026-09-16 (source not in this project): if

    J_n := n^2 * E[x_i^2 * w_i^2] = E[Z_{n,i}^2],  Z_{n,i} := n * x_i * w_i

stays bounded (does not grow with n), then Cauchy-Schwarz on the pointwise
bound gives delta_i^2 <= 4 x_i^2 w_i^2, hence E[delta_i^2] = O(n^-2), hence
(via the already-established B_n = (m/4) E[delta_i^2]) B_n = O(1/n), which
would close the whole project variance target through the already-proved
inequality V_n <= (B_n + 2 W_1) / 3 (see decision.md points 12a and 1-14 --
not re-derived here, used as given).

This script is a Cheapest Differentiating Test (2 values of n, pilot-scale
reps), NOT a claim of proof. It does not write to decision.md, does not
commit, and does not touch codex-20260914-susceptibility/.

=== v3: canonical sampling/role-assignment protocol (2026-09-16 correction) ===

Two earlier versions of this script were rejected by the coordinator as
deviating from this project's OWN established single-generator-sensitivity
protocol, used throughout the experiment (canonical reference:
check_kappa_n_large_n.py:100 `TEST_GENERATOR_INDEX = 1` and :190-225
`sample_x_q_delta`):

  - v1 forced bits[0]=0 (generator 1 artificially absent) before drawing the
    rest -- this silently DROPPED the entire "generator 1 already present"
    branch, i.e. half of the canonical unconditioned Bernoulli(1/2) sample
    space, even though the tested index (1) matched canon.
  - v2 fixed that omission the wrong way: it drew all m bits honestly
    unconditioned, but then picked the tested coordinate i post-hoc,
    uniformly at random from whichever bits happened to be 0. That
    introduces size-biased weighting relative to graph density (a graph
    with more free coordinates gives each of them less "weight" per
    coordinate), which is NOT what E[...] means in the canonical single-
    fixed-index protocol below.

v3 (this version) follows the canonical protocol exactly, with NO
conditioning and NO post-hoc selection:

  1. gen_index = 1, a FIXED constant (matches TEST_GENERATOR_INDEX in
     check_kappa_n_large_n.py; NOT re-chosen per sample).
  2. c = sample_circulant_neighbors(n, 0.5, seed) -- reused UNCHANGED from
     20260909-lovasz-theta-random-circulant-graphs/run.py (same file this
     experiment's other large-n scripts load via importlib, e.g.
     check_kappa_n_large_n.py, check_first_chaos_decomposition_large_n.py).
     ALL m bits of the underlying generator-presence vector are drawn i.i.d.
     Bernoulli(0.5); c[gen_index] is NOT forced and NOT filtered on.
  3. c_flip = flip_generator(c, gen_index) toggles exactly that bit (and its
     mirror c[n-gen_index]) -- reused verbatim from
     check_single_generator_sensitivity_n3000.py / check_kappa_n_large_n.py
     (a 4-line utility, duplicated here rather than imported, since
     importing the whole of check_kappa_n_large_n.py would also trigger its
     module-level SWEEP_N_REPS/POSITIVE_CONTROL constants for no reason;
     the function body below is character-for-character identical).
  4. BOTH branches of the draw enter the sample, exactly mirroring
     `sample_x_q_delta` (check_kappa_n_large_n.py:216-224):
       - c[gen_index] < 0.5  (branch A: i absent in the raw draw c):
         G0 = c            (i absent, this IS "S")
         G1 = c_flip        (i present, this is "S union {i}")
       - c[gen_index] >= 0.5 (branch B: i already present in the raw draw c):
         G0 = c_flip        (i absent after flipping, this IS "S")
         G1 = c              (i present, this is "S union {i}")
     In both branches, `delta_i_actual := X(G0) - X(G1)` is the SAME
     canonical non-negative quantity `delta_i(S) = X(S) - X(S union {i})`
     (decision.md point 12) -- no branch is dropped or filtered, and no
     post-hoc coordinate choice occurs; gen_index is fixed throughout.
  5. x = optimal time-domain certificate of G0 (the i-absent graph); w =
     optimal time-domain certificate of complement(G1) (the i-present
     graph's complement) -- the SAME Point 63 pairing used in v1/v2, now
     applied to whichever of {c, c_flip} plays the G0/G1 role in each
     branch, rather than assuming the raw draw is always G0.
  6. x_i = x[gen_index], w_i = w[gen_index] (index gen_index in the
     length-n time-domain vector CertificateLP.solve returns).

Equivalence of the two LP engines actually used here (verified numerically
before running the pilot, not assumed): `theta_via_lp(c)`
(20260909-lovasz-theta-random-circulant-graphs/run.py, the project's
canonical "paper's own time-domain primal LP") and `CertificateLP(n).solve`
(codex-20260914-susceptibility/test_convolution_repair.py, a symmetry-
reduced half-dimension version of the identical LP, with `bits =
c[1:m+1]`) return IDENTICAL theta to ~1e-13 on matched random graphs at
n=37 and n=127 (spot-checked, 6/6 pairs agree to machine precision -- see
this file's git history / session transcript for the one-off check script).
`CertificateLP` is used here (not `theta_via_lp` directly) because it also
returns the full time-domain vector `x`, which `theta_via_lp` computes
internally but discards before returning -- `theta_via_lp` itself is
untouched, not imported, and not modified.

delta_i independence (unchanged from the coordinator's first correction):
delta_i_actual is computed on a channel fully independent of x_i, w_i --
it is `log(theta(G0)/theta(G1))` from two direct LP solves, never
reconstructed from the x_i*w_i product. `delta_i_bound = 2*x_i*w_i` is a
separate field, used only for the sanity cross-check.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
CODEX_DIR = HERE / "codex-20260914-susceptibility"
H_CAT31_1_DIR = HERE.parent / "20260909-lovasz-theta-random-circulant-graphs"
sys.path.insert(0, str(CODEX_DIR))

from test_convolution_repair import CertificateLP  # noqa: E402  (path set above)


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_h_cat31_1 = _load_module("ppl_gate_pilot_dep_h_cat31_1", H_CAT31_1_DIR / "run.py")
sample_circulant_neighbors = _h_cat31_1.sample_circulant_neighbors  # canonical, unmodified


def flip_generator(c: np.ndarray, i: int) -> np.ndarray:
    """Toggle generator bit i (both mirrored edges c[i], c[n-i] together).

    Character-for-character identical to check_kappa_n_large_n.py:180-187 /
    check_single_generator_sensitivity_n3000.py -- duplicated rather than
    imported to avoid triggering check_kappa_n_large_n.py's module-level
    sweep/positive-control constants on import.
    """
    n = len(c)
    c2 = c.copy()
    c2[i] = 1.0 - c2[i]
    c2[n - i] = 1.0 - c2[n - i]
    return c2


# v3.1 extension (2026-09-16, coordinator request): third point n=1021 added for a trend
# estimate, at a reduced seed budget (180, not 500 -- coordinator: "150-200 seeds достаточно,
# цель третья точка для оценки тренда, не финальная точность"). n=127/509 rep counts are
# UNCHANGED from v3 (same seed scheme, reproduces the identical prior result deterministically)
# -- this is an addition, not a rewrite of the already-working sampling logic.
# n=2039 (fourth, optional point) was NOT added: timed at ~11.9 s/case (3 LP solves) vs ~1.4 s/case
# at n=1021, i.e. ~90 reps would run ~1070s (~18 min) -- coordinator marked this point explicitly
# optional ("не обязательно"), so it is skipped here to keep the extension inside a reasonable
# single run; the 3-point trend (127/509/1021) below is what this extension delivers.
SIZES_REPS = ((127, 500), (509, 500), (1021, 180))
SIZES = tuple(n for n, _ in SIZES_REPS)
GEN_INDEX = 1  # == TEST_GENERATOR_INDEX in check_kappa_n_large_n.py; fixed, never re-chosen
SEED_BASE = 3351000  # fresh, distinct from every RNG_SEED_BASE/BOOTSTRAP_SEED already listed
# in check_kappa_n_large_n.py's own comment (31000/331000/332000/333000/334000/335000/
# 3331000/3337000/3341000/3347000/3348000/991/9931) and from this script's own earlier
# 916160000 base (v1/v2, now superseded).
SANITY_TOL = 1e-6  # matches the ~1e-6 certificate/margin tolerances used throughout Point 63 code


def one_case(n: int, seed: int) -> dict:
    lp = CertificateLP(n)
    m = lp.m
    assert m == (n - 1) // 2

    c = sample_circulant_neighbors(n, 0.5, seed)  # ALL bits honest Bernoulli(0.5), unconditioned
    c_flip = flip_generator(c, GEN_INDEX)

    if c[GEN_INDEX] < 0.5:
        branch = "A"  # i absent in the raw draw: c IS S (=G0), c_flip IS S union {i} (=G1)
        c_g0, c_g1 = c, c_flip
    else:
        branch = "B"  # i present in the raw draw: c_flip IS S (=G0), c IS S union {i} (=G1)
        c_g0, c_g1 = c_flip, c

    bits_g0 = c_g0[1 : m + 1].astype(int)
    bits_g1 = c_g1[1 : m + 1].astype(int)
    assert bits_g0[GEN_INDEX - 1] == 0
    assert bits_g1[GEN_INDEX - 1] == 1

    g0 = lp.solve(bits_g0)
    g1 = lp.solve(bits_g1)
    comp = lp.solve(1 - bits_g1)  # complement(G1), same construction verify_optimal_energy.py uses

    x_i = float(g0["x"][GEN_INDEX])
    w_i = float(comp["x"][GEN_INDEX])
    theta_g0 = float(g0["theta"])
    theta_g1 = float(g1["theta"])
    theta_comp = float(comp["theta"])

    # Independent channel: delta_i from two direct theta LP solves, NOT from x_i*w_i.
    delta_actual = float(np.log(theta_g0 / theta_g1))  # canonical delta_i(S) = X(S)-X(S union{i})
    # Separate channel: the Point 63 bound, built from x_i, w_i.
    delta_bound = float(2.0 * x_i * w_i)
    z_ni = float(n * x_i * w_i)

    return {
        "n": n,
        "seed": seed,
        "branch": branch,
        "gen_index": GEN_INDEX,
        "x_i": x_i,
        "w_i": w_i,
        "Z_ni": z_ni,
        "Z_ni2": z_ni**2,
        "theta_G0": theta_g0,
        "theta_G1": theta_g1,
        "theta_complement_G1": theta_comp,
        "delta_i_actual": delta_actual,
        "delta_i_bound": delta_bound,
        "bound_minus_actual": delta_bound - delta_actual,  # must stay >= -tol (sanity gate)
        "complement_identity_error": abs(theta_g1 * theta_comp - n),  # theta(G1)*theta(comp G1)=n
        "g0_certificate_error": float(g0["certificate_error"]),
        "g0_relative_gap": float(g0["relative_gap"]),
        "g1_certificate_error": float(g1["certificate_error"]),
        "g1_relative_gap": float(g1["relative_gap"]),
        "comp_certificate_error": float(comp["certificate_error"]),
        "comp_relative_gap": float(comp["relative_gap"]),
    }


def tail_share(z2: np.ndarray, frac: float) -> float:
    """Share of sum(Z^2) contributed by the top `frac` fraction of |Z| samples."""
    k = max(1, int(np.ceil(frac * len(z2))))
    sorted_desc = np.sort(z2)[::-1]
    total = sorted_desc.sum()
    if total == 0:
        return 0.0
    return float(sorted_desc[:k].sum() / total)


def summarize(rows: list[dict], n: int) -> dict:
    z = np.array([r["Z_ni"] for r in rows])
    z2 = z**2
    j_n = float(z2.mean())
    se = float(z2.std(ddof=1) / np.sqrt(len(z2))) if len(z2) > 1 else float("nan")
    return {
        "n": n,
        "reps": len(rows),
        "mean_Z": float(z.mean()),
        "mean_Z2_J_n": j_n,
        "J_n_SE": se,
        "median_Z": float(np.median(z)),
        "q90_Z": float(np.quantile(z, 0.90)),
        "q95_Z": float(np.quantile(z, 0.95)),
        "q99_Z": float(np.quantile(z, 0.99)),
        "max_Z": float(z.max()),
        "min_Z": float(z.min()),
        "top1pct_share_of_sum_Z2": tail_share(z2, 0.01),
        "top5pct_share_of_sum_Z2": tail_share(z2, 0.05),
    }


def weighted_power_law_fit(ns: list[int], j_vals: list[float], j_ses: list[float]) -> dict:
    """Weighted least squares fit of log(J_n) = a + b*log(n), weights = 1/SE(log J_n)^2.

    SE(log J_n) via the delta method: SE(log J) ~= SE(J)/J (valid while SE(J)/J is not too
    large -- flagged in the output if it exceeds 0.3 for any point). Parameter covariance from
    the standard weighted-least-squares normal equations (X^T W X)^-1, treating the per-point
    SEs as known variances -- same convention this project's other points use for weighted fits
    (per-point SE as known variance, not re-estimated residual variance, since here there are
    only 3 points and 2 parameters, 1 degree of freedom).
    """
    x = np.log(np.array(ns, dtype=float))
    y = np.log(np.array(j_vals, dtype=float))
    rel_se = np.array(j_ses) / np.array(j_vals)
    se_log = rel_se  # delta method: SE(log J) ~= SE(J)/J
    w = 1.0 / se_log**2
    X = np.column_stack([np.ones_like(x), x])
    W = np.diag(w)
    XtW = X.T @ W
    cov = np.linalg.inv(XtW @ X)
    beta = cov @ XtW @ y
    intercept, slope = float(beta[0]), float(beta[1])
    se_intercept, se_slope = float(np.sqrt(cov[0, 0])), float(np.sqrt(cov[1, 1]))
    dof = len(ns) - 2
    t_stat = slope / se_slope if se_slope > 0 else float("nan")
    fitted = X @ beta
    residuals = y - fitted
    return {
        "model": "log(J_n) = a + b*log(n), weighted least squares, weights=1/SE(log J_n)^2",
        "n_points": len(ns),
        "degrees_of_freedom": dof,
        "intercept_a": intercept,
        "intercept_a_SE": se_intercept,
        "slope_b": slope,
        "slope_b_SE": se_slope,
        "slope_t_statistic": t_stat,
        "slope_interpretation": (
            "b=0 would mean J_n bounded (no power-law growth); b>0 growing; "
            "b<0 shrinking -- with dof=1 this t-stat has essentially no power, illustrative only"
        ),
        "relative_SE_J_n_per_point": {str(n): float(r) for n, r in zip(ns, rel_se)},
        "delta_method_caveat": (
            "SE(log J)~=SE(J)/J is a first-order approximation; flagged unreliable per-point "
            "if relative SE exceeds 0.3"
        ),
        "delta_method_reliable": bool(np.all(rel_se <= 0.3)),
        "residuals_log_J": [float(r) for r in residuals],
    }


def tail_concentration_trend(ns: list[int], top5_shares: list[float]) -> dict:
    """Unweighted linear trend of top5pct_share_of_sum_Z2 vs n (and vs log n) -- a separate
    question from J_n's own level/growth: J_n can look flat while the tail driving it gets
    heavier (or lighter) with n. No SE is attached to a single top-5% share estimate from one
    n's own 500 (or 180) samples without a further bootstrap, which the coordinator did not
    request here, so this trend is reported as point values plus a simple OLS slope, not a
    t-tested claim -- explicitly weaker evidence than the J_n fit above, labelled as such.
    """
    x_n = np.array(ns, dtype=float)
    x_logn = np.log(x_n)
    y = np.array(top5_shares, dtype=float)
    slope_vs_n = float(np.polyfit(x_n, y, 1)[0]) if len(ns) >= 2 else float("nan")
    slope_vs_logn = float(np.polyfit(x_logn, y, 1)[0]) if len(ns) >= 2 else float("nan")
    return {
        "values_by_n": {str(n): float(v) for n, v in zip(ns, top5_shares)},
        "unweighted_ols_slope_vs_n": slope_vs_n,
        "unweighted_ols_slope_vs_log_n": slope_vs_logn,
        "caveat": (
            "no SE attached (single point estimate per n from that n's own sample, no bootstrap "
            "requested) -- report values + naive OLS slope only, weaker evidence than the J_n fit, "
            "not t-tested"
        ),
    }


def main() -> None:
    started = time.monotonic()
    rows_by_n: dict[str, list[dict]] = {}
    for n, reps in SIZES_REPS:
        rows = []
        for rep in range(reps):
            seed = SEED_BASE + n * 100_000 + rep  # matches sample_x_q_delta's own seed scheme
            row = one_case(n, seed)
            rows.append(row)
            if (rep + 1) % 50 == 0 or rep == 0:
                print(
                    f"n={n} rep={rep + 1}/{reps} branch={row['branch']} "
                    f"Z={row['Z_ni']:.4g} delta_actual={row['delta_i_actual']:.4g} "
                    f"delta_bound={row['delta_i_bound']:.4g} "
                    f"margin={row['bound_minus_actual']:.3g}",
                    flush=True,
                )
        rows_by_n[str(n)] = rows

    all_rows = [r for rows in rows_by_n.values() for r in rows]
    sanity_min_margin = min(r["bound_minus_actual"] for r in all_rows)
    sanity_max_complement_error = max(r["complement_identity_error"] for r in all_rows)
    sanity_passed = sanity_min_margin >= -SANITY_TOL and sanity_max_complement_error < 1e-4

    summaries = [summarize(rows_by_n[str(n)], n) for n in SIZES]
    branch_summaries = {
        str(n): {
            branch: summarize([r for r in rows_by_n[str(n)] if r["branch"] == branch], n)
            for branch in ("A", "B")
            if any(r["branch"] == branch for r in rows_by_n[str(n)])
        }
        for n in SIZES
    }
    branch_counts = {
        str(n): {
            "A": sum(1 for r in rows_by_n[str(n)] if r["branch"] == "A"),
            "B": sum(1 for r in rows_by_n[str(n)] if r["branch"] == "B"),
        }
        for n in SIZES
    }
    # WHY: index by SIZE, not list position -- a prior version used summaries[-1]/summaries[0]
    # for "509_over_127", which silently became the 1021/127 ratio once n=1021 was appended
    # (summaries[-1] shifted from the n=509 entry to the n=1021 entry). Caught by the duplicate
    # value in the first run of this extension (both ratio fields printed 1.5877...) -- fixed by
    # looking up each summary by its own "n" field instead of by list position.
    summaries_by_n = {s["n"]: s for s in summaries}

    def _ratio(n_hi: int, n_lo: int) -> float | None:
        if n_hi not in summaries_by_n or n_lo not in summaries_by_n:
            return None
        j_lo = summaries_by_n[n_lo]["mean_Z2_J_n"]
        j_hi = summaries_by_n[n_hi]["mean_Z2_J_n"]
        return j_hi / j_lo if j_lo != 0 else float("inf")

    j_ratio = _ratio(509, 127)
    j_ratio_1021_over_127 = _ratio(1021, 127)
    j_ratio_1021_over_509 = _ratio(1021, 509)

    power_law_fit = weighted_power_law_fit(
        [s["n"] for s in summaries],
        [s["mean_Z2_J_n"] for s in summaries],
        [s["J_n_SE"] for s in summaries],
    )
    tail_trend = tail_concentration_trend(
        [s["n"] for s in summaries],
        [s["top5pct_share_of_sum_Z2"] for s in summaries],
    )

    output = {
        "protocol": (
            "external-proposal 2026-09-16, Point 63 cross-complement PPL_gate pilot "
            "(v3, canonical sample_x_q_delta-style sampling -- no conditioning, "
            "no post-hoc index choice)"
        ),
        "not_to_be_confused_with": (
            "T_q (decision.md points 15b-20, swap-Dirichlet-energy) -- different quantity"
        ),
        "estimand": (
            "J_n = E[Z_{n,i}^2], Z_{n,i} = n*x_i*w_i, gen_index=1 FIXED; "
            "x=optimal certificate of G0 (i absent), "
            "w=optimal certificate of complement(G1) (i present); "
            "G0/G1 assigned by bit value, matching whichever of {c, c_flip} has the bit "
            "off/on -- both canonical sample_x_q_delta branches "
            "(c[gen_index]<0.5 and >=0.5) included, none dropped"
        ),
        "sampling": (
            "canonical: c = sample_circulant_neighbors(n,0.5,seed) unmodified from "
            "20260909-lovasz-theta-random-circulant-graphs/run.py, ALL m bits iid Bernoulli(0.5) "
            "unconditioned; gen_index=1 fixed (not chosen per-sample, not forced, not filtered)"
        ),
        "delta_i_independence": (
            "delta_i_actual computed from two independent direct LP solves of "
            "theta(G0), theta(G1); NOT reconstructed from x_i*w_i. "
            "delta_i_bound (=2*x_i*w_i) is a separate field used only "
            "for the sanity cross-check."
        ),
        "sizes": list(SIZES),
        "reps_by_size": {str(n): r for n, r in SIZES_REPS},
        "gen_index": GEN_INDEX,
        "seed_scheme": f"SEED_BASE={SEED_BASE} + n*100000 + rep, rep=0..(reps_by_size[n]-1)",
        "branch_counts": branch_counts,
        "sanity_check": {
            "description": (
                "Point 63 deterministic inequality delta_i_actual <= delta_i_bound must hold on "
                "every (n,seed) pair, both branches, independent channels; complement identity "
                "theta(G1)*theta(complement G1)=n must hold"
            ),
            "min_bound_minus_actual_margin": sanity_min_margin,
            "max_complement_identity_error": sanity_max_complement_error,
            "tolerance": SANITY_TOL,
            "passed": sanity_passed,
        },
        "summaries": summaries,
        "branch_summaries": branch_summaries,
        "J_n_ratio_509_over_127": j_ratio,
        "J_n_ratio_1021_over_127": j_ratio_1021_over_127,
        "J_n_ratio_1021_over_509": j_ratio_1021_over_509,
        "power_law_fit_log_Jn_vs_log_n": power_law_fit,
        "tail_concentration_trend_top5pct_share": tail_trend,
        "elapsed_seconds": time.monotonic() - started,
        "rows_by_n": rows_by_n,
    }

    out_path = HERE / "metrics" / "ppl_gate_pilot.json"
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in output.items() if k != "rows_by_n"}, indent=2))


if __name__ == "__main__":
    main()
