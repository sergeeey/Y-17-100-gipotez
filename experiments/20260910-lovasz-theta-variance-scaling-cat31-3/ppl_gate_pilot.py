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
    rest. CORRECTED (2026-09-16, Point 67 forensic follow-up): this does NOT
    drop half the sample space as originally claimed here -- forcing the bit
    to 0 post-hoc is algebraically identical to v3's own branch-conditional
    flip_generator (proven via a per-seed forensic chain diff, 25/25 seeds,
    zero divergence at any field; also reproduced in aggregate over 500
    seeds, matching v3's own J_n(127) to 16 significant figures). The real
    ~11x numerical gap between v1's reported 5.9 and v3's J_n=64.66 remains
    UNEXPLAINED by any graph-construction mechanism tested so far -- the
    leading candidate (not confirmed) is an aggregator mismatch, since
    v1's target (5.9) sits within 1.7 SE of THIS SAME construction's own
    mean_Z=5.44 (E[Z], not E[Z^2]=J_n), and J_n/mean_Z=11.9 numerically
    matches the observed "~11x" almost exactly. See decision.md Point 67.
  - v2 fixed that omission the wrong way: it drew all m bits honestly
    unconditioned, but then picked the tested coordinate i post-hoc,
    uniformly at random from whichever bits happened to be 0. That
    introduces size-biased weighting relative to graph density (a graph
    with more free coordinates gives each of them less "weight" per
    coordinate), which is NOT what E[...] means in the canonical single-
    fixed-index protocol below.

=== v3.2 extension (2026-09-16, user-directed, final not pilot) ===

Extends n=1021 from 180 to 500 reps (matching n=127,509), REUSING the
already-computed 180 rows from the previous run (loaded from
metrics/ppl_gate_pilot.json if present, validated row-by-row against this
script's own canonical seed scheme before reuse -- a mismatch at any index
stops reuse at that point rather than silently trusting stale/foreign data)
and computing only the missing rep=180..499 (320 new LP-solve triples).
n=127,509 are always fully reused (0 new LP solves) when a matching prior
run exists.

Adds three further quantities, computed from data already collected (no
extra LP solves beyond the n=1021 extension above):
  - K_n := n^2 * E[delta_i_actual^2] -- the DIRECT target quantity (Point 66
    called this "n^2*E[delta^2]"; renamed K_n here per the user's own
    request, paired with J_n).
  - eta_n := K_n / (4*J_n) -- diagnostic ratio, already computed once
    informally in decision.md Point 69 from this same saved data
    (0.279/0.253/0.262); recomputed here with an SE via the delta method
    for a ratio of two (correlated, same-row) sample means -- NOT assumed
    independent, since both K_n and J_n are computed from the same rows.
  - ratio_J_over_K := J_n / K_n (the un-normalized proxy/target ratio,
    plain reciprocal-scaled version of eta_n, offered separately since it
    is the more natural axis for its own power-law fit).

Also corrects the significance-test framing that decision.md Point 66
identified as WRONG on skeptic review: under this script's own known-
variance convention (per-point SE treated as a KNOWN quantity, not a
re-estimated residual variance), testing slope=0 against a flat/constant
model is a nested-model comparison with a 1-degree-of-freedom DIFFERENCE
in free parameters -- the correct reference distribution is chi-square
with 1 dof (a Delta-chi-squared test), not a t-distribution at
dof=n_points-2. The former "dof=1, essentially no power, illustrative
only" framing is retired from this file's own output (it was accepted as
a corrected finding, not merely a stylistic change, in decision.md Point
66's skeptic-fallback review).

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
from scipy.stats import chi2 as chi2_dist  # for the Delta-chi-squared significance test only

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
# v3.2 (2026-09-16): n=1021 raised from 180 to 500 reps (matching 127/509), per explicit user
# instruction -- this is now a FINAL closure test at 3 points, not a trend-estimate pilot. n=2039
# remains skipped here (optional, user said "не обязательно ... явно скажи если пропускаешь" --
# skipped explicitly for this run's time budget; see this run's own report for the explicit note).
SIZES_REPS = ((127, 500), (509, 500), (1021, 500))
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
    """J_n (proxy, from x_i*w_i) AND K_n (the direct target, from delta_i_actual), computed
    jointly on the SAME rows -- both quantities and their covariance, since they are NOT
    independent (same underlying LP solves feed both channels via the same graph draw).

    K_n := n^2 * E[delta_i_actual^2] -- the direct target quantity B_n=(m/4)E[delta_i^2] is
    proportional to (K_n/n^2)*n = K_n/n up to the m/4 factor; K_n itself is the n^2-normalized
    second moment, matching J_n's own normalization so the two are directly comparable.

    eta_n := K_n/(4*J_n) is a diagnostic ratio (should lie in [0,1] by the Point 63 pointwise
    bound delta_i<=2*x_i*w_i, in an average-of-ratio sense only -- E[delta^2]/(4*E[(xw)^2]) is
    NOT the same object as E[delta^2/(4*(xw)^2)], stated explicitly to avoid an unearned
    Jensen-style claim). Its SE uses the delta method for a ratio of two CORRELATED sample
    means (same known-variance convention as J_n_SE elsewhere in this file: per-point SE is
    itself treated as a known quantity, not re-estimated residual variance):
      Var(K/(4J)) ~= (K/(4J))^2 * [Var(K)/K^2 + Var(J)/J^2 - 2*Cov(K,J)/(K*J)]
    Cov(K,J) is estimated directly from the paired per-row values (K_row=n^2*delta^2,
    J_row=Z^2), not assumed zero.
    """
    z = np.array([r["Z_ni"] for r in rows])
    delta = np.array([r["delta_i_actual"] for r in rows])
    reps = len(rows)
    z2 = z**2
    d2_scaled = (n**2) * delta**2  # per-row contribution to K_n

    j_n = float(z2.mean())
    j_se = float(z2.std(ddof=1) / np.sqrt(reps)) if reps > 1 else float("nan")
    k_n = float(d2_scaled.mean())
    k_se = float(d2_scaled.std(ddof=1) / np.sqrt(reps)) if reps > 1 else float("nan")
    cov_jk = float(np.cov(z2, d2_scaled, ddof=1)[0, 1] / reps) if reps > 1 else float("nan")

    if j_n != 0 and reps > 1 and not np.isnan(cov_jk):
        eta_n = k_n / (4.0 * j_n)
        eta_se = float(
            abs(eta_n) * np.sqrt((k_se / k_n) ** 2 + (j_se / j_n) ** 2 - 2.0 * cov_jk / (k_n * j_n))
        )
    else:
        eta_n = float("nan")
        eta_se = float("nan")

    if k_n != 0 and reps > 1 and not np.isnan(cov_jk):
        ratio_j_over_k = j_n / k_n
        ratio_se = float(
            abs(ratio_j_over_k)
            * np.sqrt((j_se / j_n) ** 2 + (k_se / k_n) ** 2 - 2.0 * cov_jk / (j_n * k_n))
        )
    else:
        ratio_j_over_k = float("nan")
        ratio_se = float("nan")

    return {
        "n": n,
        "reps": reps,
        "mean_Z": float(z.mean()),
        "mean_Z2_J_n": j_n,
        "J_n_SE": j_se,
        "mean_delta": float(delta.mean()),
        "n2E_delta2_K_n": k_n,
        "K_n_SE": k_se,
        "cov_Jrow_Krow_over_reps": cov_jk,
        "eta_n_K_over_4J": eta_n,
        "eta_n_SE_delta_method": eta_se,
        "ratio_J_over_K": ratio_j_over_k,
        "ratio_J_over_K_SE_delta_method": ratio_se,
        "median_Z": float(np.median(z)),
        "median_delta": float(np.median(delta)),
        "q90_Z": float(np.quantile(z, 0.90)),
        "q95_Z": float(np.quantile(z, 0.95)),
        "q99_Z": float(np.quantile(z, 0.99)),
        "max_Z": float(z.max()),
        "min_Z": float(z.min()),
        "top1pct_share_of_sum_Z2": tail_share(z2, 0.01),
        "top5pct_share_of_sum_Z2": tail_share(z2, 0.05),
        "top1pct_share_of_sum_delta2": tail_share(delta**2, 0.01),
        "top5pct_share_of_sum_delta2": tail_share(delta**2, 0.05),
    }


def weighted_power_law_fit(
    ns: list[int], y_vals: list[float], y_ses: list[float], label: str
) -> dict:
    """Weighted least squares fit of log(Y) = a + b*log(n), weights = 1/SE(log Y)^2, PLUS the
    correct significance test for b=0.

    SE(log Y) via the delta method: SE(log Y) ~= SE(Y)/Y (valid while SE(Y)/Y is not too
    large -- flagged in the output if it exceeds 0.3 for any point). Parameter covariance from
    the standard weighted-least-squares normal equations (X^T W X)^-1, treating the per-point
    SEs as known variances -- same convention this project's other points use for weighted fits
    (per-point SE as known variance, not re-estimated residual variance).

    WHY chi-square, not a t-test (corrected 2026-09-16, per decision.md Point 66's own skeptic
    correction -- the earlier "dof=1, essentially no power" framing in this file was FALSIFIED
    on review and must not be reused): under the known-variance convention above, the flat
    model (Y constant, 1 free parameter: the weighted mean) and the power-law model (2 free
    parameters: intercept + slope) are NESTED, and testing slope=0 is a comparison of their
    weighted chi-square goodness-of-fit statistics. The DIFFERENCE in free-parameter count
    between the two models is exactly 1, regardless of how many data points there are -- so
    Delta-chi2 := chi2_flat - chi2_power is chi-square distributed with 1 degree of freedom
    under the null (slope=0), by Wilks' theorem for nested weighted-least-squares models. This
    is well-defined and has real power even with only 3 points (2 residual dof for the flat
    model, 1 for the power-law model) -- unlike a small-sample t-test at dof=1, which is what
    the retired framing conflated it with.
    """
    x = np.log(np.array(ns, dtype=float))
    y = np.log(np.array(y_vals, dtype=float))
    rel_se = np.array(y_ses) / np.array(y_vals)
    se_log = rel_se  # delta method: SE(log Y) ~= SE(Y)/Y
    w = 1.0 / se_log**2

    X = np.column_stack([np.ones_like(x), x])
    W = np.diag(w)
    XtW = X.T @ W
    cov = np.linalg.inv(XtW @ X)
    beta = cov @ XtW @ y
    intercept, slope = float(beta[0]), float(beta[1])
    se_intercept, se_slope = float(np.sqrt(cov[0, 0])), float(np.sqrt(cov[1, 1]))
    fitted = X @ beta
    residuals = y - fitted
    chi2_power = float(np.sum(w * residuals**2))

    y_bar_w = float(np.sum(w * y) / np.sum(w))  # flat model = weighted mean, slope forced to 0
    chi2_flat = float(np.sum(w * (y - y_bar_w) ** 2))

    delta_chi2 = chi2_flat - chi2_power
    delta_chi2_clamped = max(delta_chi2, 0.0)  # numerical guard; nested models => delta_chi2>=0
    p_value = float(chi2_dist.sf(delta_chi2_clamped, 1))

    z95 = 1.959963984540054  # standard-normal 97.5th percentile
    label_safe = label.replace("/", "_over_")  # keep JSON keys free of "/" for downstream ease
    return {
        "label": label,
        "model": (
            f"log({label}) = a + b*log(n), weighted least squares, weights=1/SE(log {label})^2"
        ),
        "n_points": len(ns),
        "intercept_a": intercept,
        "intercept_a_SE": se_intercept,
        "slope_b": slope,
        "slope_b_SE": se_slope,
        "slope_b_95CI": [slope - z95 * se_slope, slope + z95 * se_slope],
        "slope_interpretation": (
            f"b=0 would mean {label} bounded (no power-law growth); b>0 growing; b<0 shrinking"
        ),
        f"relative_SE_{label_safe}_per_point": {str(n): float(r) for n, r in zip(ns, rel_se)},
        "delta_method_caveat": (
            "SE(log Y)~=SE(Y)/Y is a first-order approximation; flagged unreliable per-point "
            "if relative SE exceeds 0.3"
        ),
        "delta_method_reliable": bool(np.all(rel_se <= 0.3)),
        "residuals_log_Y": [float(r) for r in residuals],
        "chi2_flat_model": chi2_flat,
        "chi2_flat_model_dof": len(ns) - 1,
        "chi2_power_law_model": chi2_power,
        "chi2_power_law_model_dof": len(ns) - 2,
        "delta_chi2_dof1": delta_chi2,
        "delta_chi2_p_value": p_value,
        "significance_test_note": (
            "Delta-chi-squared test for slope=0 (nested flat-vs-power-law models under this "
            "script's known-variance convention), chi2 with 1 dof -- NOT a t-test; corrected "
            "framing per decision.md Point 66 skeptic-fallback review"
        ),
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


def _load_prior_run(out_path: Path) -> dict:
    """Best-effort load of a previous run's JSON, for row-reuse and for the n=1021
    180-vs-500-rep comparison. Returns {} if absent/unreadable -- absence must never be an
    error, just "compute everything from scratch"."""
    if not out_path.exists():
        return {}
    try:
        return json.loads(out_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def main() -> None:
    started = time.monotonic()
    out_path = HERE / "metrics" / "ppl_gate_pilot.json"
    prior = _load_prior_run(out_path)
    prior_rows_by_n: dict[str, list[dict]] = prior.get("rows_by_n", {})
    prior_summaries_by_n = {s["n"]: s for s in prior.get("summaries", [])}

    rows_by_n: dict[str, list[dict]] = {}
    for n, reps in SIZES_REPS:
        key = str(n)
        candidate_prior_rows = prior_rows_by_n.get(key, [])
        # WHY: validate each prior row against THIS run's own canonical seed scheme (seed must
        # equal SEED_BASE + n*100000 + its own rep-index position, and n must match) before
        # reusing it -- stops reuse at the first mismatch rather than silently trusting rows
        # from a differently-configured earlier run. Never reuse more than the new target reps.
        reusable: list[dict] = []
        for idx, row in enumerate(candidate_prior_rows):
            if idx >= reps:
                break
            expected_seed = SEED_BASE + n * 100_000 + idx
            if row.get("n") == n and row.get("seed") == expected_seed:
                reusable.append(row)
            else:
                break
        rows = list(reusable)
        start_rep = len(rows)
        if start_rep > 0:
            print(
                f"n={n}: reusing {start_rep} already-computed reps from {out_path.name}", flush=True
            )
        if start_rep < reps:
            print(
                f"n={n}: computing {reps - start_rep} new reps (rep={start_rep}..{reps - 1})",
                flush=True,
            )
        for rep in range(start_rep, reps):
            seed = SEED_BASE + n * 100_000 + rep  # matches sample_x_q_delta's own seed scheme
            row = one_case(n, seed)
            rows.append(row)
            if (rep + 1) % 50 == 0 or rep == start_rep:
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

    ns_sorted = [s["n"] for s in summaries]
    power_law_fit_Jn = weighted_power_law_fit(
        ns_sorted,
        [s["mean_Z2_J_n"] for s in summaries],
        [s["J_n_SE"] for s in summaries],
        "J_n",
    )
    power_law_fit_Kn = weighted_power_law_fit(
        ns_sorted,
        [s["n2E_delta2_K_n"] for s in summaries],
        [s["K_n_SE"] for s in summaries],
        "K_n",
    )
    # Ratio fit is illustrative/optional (user: "если интересно") -- J_n and K_n are computed
    # from the SAME rows, so this axis is correlated with both fits above, not independent
    # evidence; included because it is cheap (no new LP solves) and directly answers "does the
    # proxy/target relationship itself drift with n."
    ratio_ses_valid = all(not np.isnan(s["ratio_J_over_K_SE_delta_method"]) for s in summaries)
    power_law_fit_ratio = (
        weighted_power_law_fit(
            ns_sorted,
            [s["ratio_J_over_K"] for s in summaries],
            [s["ratio_J_over_K_SE_delta_method"] for s in summaries],
            "J_n/K_n",
        )
        if ratio_ses_valid
        else None
    )
    tail_trend = tail_concentration_trend(
        ns_sorted,
        [s["top5pct_share_of_sum_Z2"] for s in summaries],
    )

    # n=1021 180-rep (prior run) vs 500-rep (this run) tail-statistics comparison, per user
    # request -- only meaningful if the prior run actually had 180 (or fewer) reps at n=1021.
    prior_1021 = prior_summaries_by_n.get(1021)
    n1021_180_vs_500_comparison = (
        {
            "prior_reps": prior_1021["reps"],
            "current_reps": summaries_by_n[1021]["reps"],
            "prior_top1pct_share_of_sum_Z2": prior_1021["top1pct_share_of_sum_Z2"],
            "current_top1pct_share_of_sum_Z2": summaries_by_n[1021]["top1pct_share_of_sum_Z2"],
            "prior_top5pct_share_of_sum_Z2": prior_1021["top5pct_share_of_sum_Z2"],
            "current_top5pct_share_of_sum_Z2": summaries_by_n[1021]["top5pct_share_of_sum_Z2"],
            "prior_median_Z": prior_1021["median_Z"],
            "current_median_Z": summaries_by_n[1021]["median_Z"],
            "prior_mean_Z2_J_n": prior_1021["mean_Z2_J_n"],
            "current_mean_Z2_J_n": summaries_by_n[1021]["mean_Z2_J_n"],
        }
        if prior_1021 is not None and prior_1021["reps"] < summaries_by_n[1021]["reps"]
        else None
    )

    n2039_note = (
        "n=2039 SKIPPED this run -- optional per the task brief; not attempted (no rows, no "
        "fit contribution). Explicitly noted rather than silently omitted."
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
        "power_law_fit_log_Jn_vs_log_n": power_law_fit_Jn,
        "power_law_fit_Kn": power_law_fit_Kn,
        "power_law_fit_ratio_J_over_K": power_law_fit_ratio,
        "n1021_180_vs_500_rep_comparison": n1021_180_vs_500_comparison,
        "n2039_note": n2039_note,
        "_provenance_note": (
            "v3.2 (2026-09-16): full regeneration from this script's own main() -- ratios "
            "computed by n-lookup (summaries_by_n), not list position, per the indexing-bug fix "
            "documented in decision.md Point 66 (a prior '_reprocessed_note' field from an "
            "unnamed post-processing step is superseded by this run, which is produced entirely "
            "by ppl_gate_pilot.py itself, closing that point's own open provenance-chain gap)."
        ),
        "tail_concentration_trend_top5pct_share": tail_trend,
        "elapsed_seconds": time.monotonic() - started,
        "rows_by_n": rows_by_n,
    }

    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in output.items() if k != "rows_by_n"}, indent=2))


if __name__ == "__main__":
    main()
