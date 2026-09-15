"""Aggregate the RBA decomposition parent-level records into the summary report.

Reads every rba_parent_level*.csv produced by rba_decomposition_test.py,
aggregates BY PARENT (children of one parent are dependent -- the bootstrap
resamples parents, never individual children), and writes:

  rba_decomposition_results.csv    one row per (dataset, n) summary
  rba_decomposition_bootstrap.csv  bootstrap percentiles per (dataset, n)
  rba_decomposition_summary.md     the report
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
NBOOT = 20000
RNG = np.random.default_rng(20260915)


def load(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            d = {}
            for k, v in r.items():
                if v == "" or v is None:
                    d[k] = None
                elif v in ("True", "False"):
                    d[k] = v == "True"
                else:
                    try:
                        d[k] = float(v)
                    except ValueError:
                        d[k] = v
            rows.append(d)
    return rows


def boot_ci(vals, stat=np.mean, nboot=NBOOT, alpha=0.05):
    vals = np.asarray(vals, dtype=float)
    k = len(vals)
    if k < 2:
        return float(stat(vals)), float("nan"), float("nan")
    idx = RNG.integers(0, k, size=(nboot, k))
    draws = stat(vals[idx], axis=1)
    lo, hi = np.percentile(draws, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return float(stat(vals)), float(lo), float(hi)


def summarize(rows, label):
    """rows: parent records for ONE n, main sample only (no full-j audit rows)."""
    n = int(rows[0]["n"])
    q = int(rows[0]["q"])
    F = int(rows[0]["F"])
    def get(k):
        return np.array([r[k] for r in rows], dtype=float)

    out = {"dataset": label, "n": n, "q": q, "F": F, "parents": len(rows),
           "transitions": int(get("num_children").sum())}

    for name, key in (("R1", "mean_R1"), ("R2", "mean_R2"),
                      ("R1_plus_R2", "R1_plus_R2"), ("R_total", "R_total"),
                      ("R1_bulk", "mean_R1_bulk"),
                      ("R1_plus_R2_bulk", "R1_plus_R2_bulk"),
                      ("R_total_bulk", "R_total_bulk"),
                      ("R0", "R0")):
        v = get(key)
        mean, lo, hi = boot_ci(v)
        out[f"q_{name}"] = q * mean
        out[f"q_{name}_lo"] = q * lo
        out[f"q_{name}_hi"] = q * hi
        out[f"q_{name}_se"] = q * float(v.std(ddof=1) / math.sqrt(len(v)))

    i_vals = get("I")
    d_vals = get("D")
    out["E_I"] = float(i_vals.mean())
    out["E_I_se"] = float(i_vals.std(ddof=1) / math.sqrt(len(i_vals)))
    out["E_D"] = float(d_vals.mean())
    out["E_D_se"] = float(d_vals.std(ddof=1) / math.sqrt(len(d_vals)))
    out["K_ADC"] = float(d_vals.mean() / (i_vals.mean() - 1.0))

    r1 = get("mean_R1").mean()
    r2 = get("mean_R2").mean()
    out["cancel_ratio"] = float(abs(r1 + r2) / (abs(r1) + abs(r2)))
    out["cancel_fraction"] = 1.0 - out["cancel_ratio"]
    r1b = get("mean_R1_bulk").mean()
    out["cancel_ratio_bulk"] = float(abs(r1b + r2) / (abs(r1b) + abs(r2)))

    out["max_fourier_resid"] = float(max(get("fourier_resid_parent").max(),
                                         get("fourier_resid_child_max").max()))
    out["max_bulk_identity_error"] = float(get("bulk_identity_error").max())
    out["max_delta_I_identity_error"] = float(get("delta_I_identity_error").max())
    out["max_check4_error"] = float(get("check4_error").max())
    out["max_abs_g_on_S"] = float(get("max_abs_g_on_S").max())
    out["max_sum_w_err"] = float(get("sum_w_err_parent").max())
    out["ambiguous_parents"] = int(sum(1 for r in rows if r["ambiguous_support"]))
    out["ambiguous_children"] = int(get("child_ambiguous").sum())
    out["solver_failures"] = int(sum(1 for r in rows if r["solver_status"] != 0)
                                 + get("child_failures").sum())
    out["mean_solve_time_parent"] = float(get("solve_time_parent").mean())
    out["mean_solve_time_child"] = float(get("mean_solve_time_child").mean())
    out["mean_subset_vs_bulk_gap"] = float(get("subset_vs_bulk_gap").mean())
    return out


# ---------------------------------------------------------------------------
# model comparison
# ---------------------------------------------------------------------------
def _design(name, q):
    q = np.asarray(q, dtype=float)
    one = np.ones(len(q))
    if name == "constant":
        return one.reshape(-1, 1)
    if name == "a+b/q":
        return np.column_stack([one, 1.0 / q])
    if name == "a+b/sqrt(q)":
        return np.column_stack([one, 1.0 / np.sqrt(q)])
    if name == "a+b*log(q)":
        return np.column_stack([one, np.log(q)])
    raise ValueError(name)


MODELS = ("constant", "a+b/q", "a+b/sqrt(q)", "a+b*log(q)")


def _wls(X, y, se):
    w = 1.0 / np.asarray(se, dtype=float)
    Xw = X * w[:, None]
    yw = np.asarray(y, dtype=float) * w
    beta, *_ = np.linalg.lstsq(Xw, yw, rcond=None)
    return beta


def compare_models(qs, ys, ses):
    """Weighted fits with KNOWN per-point variances (bootstrap SEs), so the noise
    scale is not itself estimated from 4 residuals.  k counts only the regression
    coefficients; AICc = chi2 + 2k + 2k(k+1)/(N-k-1)."""
    qs = np.asarray(qs, float)
    ys = np.asarray(ys, float)
    ses = np.asarray(ses, float)
    N = len(qs)
    res = []
    for name in MODELS:
        X = _design(name, qs)
        k = X.shape[1]
        beta = _wls(X, ys, ses)
        pred = X @ beta
        chi2 = float((((ys - pred) / ses) ** 2).sum())
        aic = chi2 + 2 * k
        denom = N - k - 1
        aicc = aic + (2 * k * (k + 1) / denom if denom > 0 else float("inf"))
        # LOOCV
        errs = []
        for i in range(N):
            keep = np.arange(N) != i
            if keep.sum() <= k:
                errs.append(float("nan"))
                continue
            b = _wls(X[keep], ys[keep], ses[keep])
            errs.append(float(ys[i] - X[i] @ b))
        errs = np.asarray(errs, float)
        loocv = float(np.sqrt(np.nanmean(errs ** 2)))
        res.append({"model": name, "k": k, "beta": [float(b) for b in beta],
                    "chi2": chi2, "AIC": aic, "AICc": aicc,
                    "LOOCV_RMSE": loocv,
                    "pred": [float(v) for v in pred]})
    best = min(res, key=lambda r: r["AICc"])["AICc"]
    for r in res:
        r["dAICc"] = r["AICc"] - best
    return res


def fmt_models(res, title):
    lines = [f"**{title}**", "",
             "| model | k | fitted params | chi2 | AICc | dAICc | LOOCV RMSE |",
             "|---|---:|---|---:|---:|---:|---:|"]
    for r in sorted(res, key=lambda x: x["AICc"]):
        pars = ", ".join(f"{b:+.4g}" for b in r["beta"])
        lines.append(f"| `{r['model']}` | {r['k']} | {pars} | {r['chi2']:.3f} | "
                     f"{r['AICc']:.2f} | {r['dAICc']:.2f} | {r['LOOCV_RMSE']:.4f} |")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# markdown tables
# ---------------------------------------------------------------------------
def md_main_table(summaries):
    L = ["| dataset | n | q | parents | transitions | q*R1 | q*R2 | q*(R1+R2) | q*R_total | "
         "95% CI q*R_total | cancel_ratio | E[I] | E[D] | K_ADC |",
         "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|"]
    for s in summaries:
        L.append(
            "| {ds} | {n} | {q} | {p} | {t} | {r1:+.3f} | {r2:+.3f} | {rs:+.3f} | {rt:+.3f} | "
            "[{lo:+.3f}, {hi:+.3f}] | {cr:.4f} | {ei:.4f} | {ed:.4f} | {k:.4f} |".format(
                ds=s["dataset"], n=s["n"], q=s["q"], p=s["parents"], t=s["transitions"],
                r1=s["q_R1"], r2=s["q_R2"], rs=s["q_R1_plus_R2"], rt=s["q_R_total"],
                lo=s["q_R_total_lo"], hi=s["q_R_total_hi"], cr=s["cancel_ratio"],
                ei=s["E_I"], ed=s["E_D"], k=s["K_ADC"]))
    return "\n".join(L)


def md_bulk_table(summaries):
    L = ["| n | q | q*R1_bulk | q*(R1+R2)_bulk | q*R_total_bulk | "
         "95% CI q*R_total_bulk | cancel_ratio_bulk | q * mean subset-vs-bulk gap |",
         "|---:|---:|---:|---:|---:|---|---:|---:|"]
    for s in summaries:
        L.append(
            "| {n} | {q} | {r1:+.3f} | {rs:+.3f} | {rt:+.3f} | [{lo:+.3f}, {hi:+.3f}] | "
            "{cr:.4f} | {g:.3f} |".format(
                n=s["n"], q=s["q"], r1=s["q_R1_bulk"], rs=s["q_R1_plus_R2_bulk"],
                rt=s["q_R_total_bulk"], lo=s["q_R_total_bulk_lo"],
                hi=s["q_R_total_bulk_hi"], cr=s["cancel_ratio_bulk"],
                g=s["q"] * s["mean_subset_vs_bulk_gap"]))
    return "\n".join(L)


def md_validation(summaries):
    L = ["| dataset | n | max Fourier resid | max bulk-id err | max delta-I id err | "
         "max check-4 err | max abs g on S | max abs(sum w - 1) | amb. parents | "
         "amb. children | solver fails | mean t parent LP (s) | mean t child LP (s) |",
         "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for s in summaries:
        L.append(
            "| {ds} | {n} | {fr:.2e} | {b:.2e} | {d:.2e} | {c:.2e} | {g:.2e} | {sw:.2e} | "
            "{ap} | {ac} | {sf} | {tp:.2f} | {tc:.2f} |".format(
                ds=s["dataset"], n=s["n"], fr=s["max_fourier_resid"],
                b=s["max_bulk_identity_error"], d=s["max_delta_I_identity_error"],
                c=s["max_check4_error"], g=s["max_abs_g_on_S"], sw=s["max_sum_w_err"],
                ap=s["ambiguous_parents"], ac=s["ambiguous_children"],
                sf=s["solver_failures"], tp=s["mean_solve_time_parent"],
                tc=s["mean_solve_time_child"]))
    return "\n".join(L)


def md_audits(audits):
    if not audits:
        return "_No full-j audit parents in this run._"
    L = ["| n | parent | free j (F) | children used | q*R1 full | q*R1 subset | "
         "q*R2 full | q*R2 subset | q*R_total full | q*R_total subset | subset k |",
         "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for a in audits:
        L.append("| {n} | {p} | {F} | {c} | {a1:+.3f} | {b1:+.3f} | {a2:+.3f} | {b2:+.3f} | "
                 "{at:+.3f} | {bt:+.3f} | {k} |".format(
                     n=a["n"], p=a["parent_id"], F=a["free_j"], c=a["children_used"],
                     a1=a["q_R1_full"], b1=a["q_R1_subset"], a2=a["q_R2_full"],
                     b2=a["q_R2_subset"], at=a["q_R_total_full"],
                     bt=a["q_R_total_subset"], k=a["subset_size"]))
    return "\n".join(L)


def md_tops(tops):
    L = ["| dataset | n | parent | q*R_total | q*R1 | q*R2 | I | D | children |",
         "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for t in tops:
        L.append("| {ds} | {n} | {p} | {rt:+.3f} | {r1:+.3f} | {r2:+.3f} | {i:.4f} | "
                 "{d:.4f} | {c} |".format(
                     ds=t["dataset"], n=t["n"], p=t["parent_id"], rt=t["q_R_total"],
                     r1=t["q_R1"], r2=t["q_R2"], i=t["I"], d=t["D"], c=t["num_children"]))
    return "\n".join(L)


def trend_test(qs, ys, ses):
    """Weighted regression of Y on log q with KNOWN variances.

    This, not the AICc/LOOCV table, is the decision statistic: AICc with N=4 and
    k=2 carries a +12 small-sample penalty that mechanically favours the
    1-parameter model, while LOOCV on 4 points mechanically favours the more
    flexible one.  The slope's own significance does not depend on that choice.
    With known variances, SE(b) = 1/sqrt(Sxx) and delta-chi2 = t^2 is the
    likelihood-ratio statistic for b != 0 on 1 dof.
    """
    x = np.log(np.asarray(qs, float))
    y = np.asarray(ys, float)
    w = 1.0 / np.asarray(ses, float) ** 2
    Sw = w.sum()
    mx = (w * x).sum() / Sw
    my = (w * y).sum() / Sw
    Sxx = (w * (x - mx) ** 2).sum()
    Sxy = (w * (x - mx) * (y - my)).sum()
    b = Sxy / Sxx
    se_b = 1.0 / math.sqrt(Sxx)
    a = my - b * mx
    chi2_full = float((w * (y - (a + b * x)) ** 2).sum())
    c0 = (w * y).sum() / Sw
    chi2_const = float((w * (y - c0) ** 2).sum())
    t = b / se_b
    # two-sided p from the chi2(1) likelihood-ratio statistic
    p = math.erfc(abs(t) / math.sqrt(2.0))
    return {"slope_per_log_q": float(b), "se_slope": float(se_b), "t": float(t),
            "p_two_sided": float(p), "intercept": float(a),
            "chi2_constant": chi2_const, "dof_constant": len(y) - 1,
            "chi2_with_slope": chi2_full, "delta_chi2": chi2_const - chi2_full,
            "constant_value": float(c0)}


def md_trend(tr, title):
    return ("| {t} | {b:+.4f} | {se:.4f} | {tt:+.2f} | {p:.3f} | {c2:.3f} on {d} dof | "
            "{cv:+.4f} |".format(t=title, b=tr["slope_per_log_q"], se=tr["se_slope"],
                                 tt=tr["t"], p=tr["p_two_sided"],
                                 c2=tr["chi2_constant"], d=tr["dof_constant"],
                                 cv=tr["constant_value"]))


def collect():
    datasets = {}
    for path in sorted(HERE.glob("rba_parent_level*.csv")):
        name = path.stem.replace("rba_parent_level", "").lstrip("_") or "main"
        if name in ("smoke", "pilot4093", "n4093", "fj2053"):
            continue
        datasets[name] = load(path)

    summaries, audits, tops = [], [], []
    for label, rows in datasets.items():
        rows = [r for r in rows if r.get("ok")]
        for n in sorted({int(r["n"]) for r in rows}):
            sub = [r for r in rows if int(r["n"]) == n]
            main_rows = [r for r in sub if not r["full_j"]]
            fj_rows = [r for r in sub if r["full_j"]]
            if main_rows:
                s = summarize(main_rows, label)
                summaries.append(s)
                q = s["q"]
                for r in sorted(main_rows, key=lambda r: -abs(q * r["R_total"]))[:5]:
                    tops.append({"dataset": label, "n": n, "parent_id": int(r["parent_id"]),
                                 "q_R_total": q * r["R_total"], "q_R1": q * r["mean_R1"],
                                 "q_R2": q * r["mean_R2"], "I": r["I"], "D": r["D"],
                                 "num_children": int(r["num_children"])})
            for r in fj_rows:
                q = int(r["q"])
                def gg(k, r=r, q=q):
                    return (q * r[k]) if r.get(k) is not None else float("nan")
                audits.append({"dataset": label, "n": n, "parent_id": int(r["parent_id"]),
                               "free_j": int(r["F"]), "children_used": int(r["num_children"]),
                               "q_R1_full": q * r["mean_R1"], "q_R2_full": q * r["mean_R2"],
                               "q_R_total_full": q * r["R_total"],
                               "subset_size": int(r.get("audit_sub_size") or 0),
                               "q_R1_subset": gg("audit_sub_R1"),
                               "q_R2_subset": gg("audit_sub_R2"),
                               "q_R_total_subset": gg("audit_sub_R_total"),
                               "bulk_identity_error": r["bulk_identity_error"]})
    return summaries, audits, tops


def main():
    summaries, audits, tops = collect()
    if summaries:
        keys = sorted({k for s in summaries for k in s})
        with open(HERE / "rba_decomposition_results.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            for s in summaries:
                w.writerow(s)
    boot_rows = []
    for s in summaries:
        for stat in ("R1", "R2", "R1_plus_R2", "R_total", "R_total_bulk"):
            boot_rows.append({"dataset": s["dataset"], "n": s["n"], "q": s["q"],
                              "statistic": "q*mean(" + stat + ")", "point": s["q_" + stat],
                              "ci_lo": s["q_" + stat + "_lo"], "ci_hi": s["q_" + stat + "_hi"],
                              "se_parent_level": s["q_" + stat + "_se"],
                              "parents": s["parents"], "n_boot": NBOOT})
    if boot_rows:
        with open(HERE / "rba_decomposition_bootstrap.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(boot_rows[0].keys()))
            w.writeheader()
            for r in boot_rows:
                w.writerow(r)

    main_s = sorted([s for s in summaries if s["dataset"] == "main"], key=lambda s: s["n"])
    other_s = sorted([s for s in summaries if s["dataset"] != "main"], key=lambda s: s["n"])
    mc = {}
    trends = {}
    if len(main_s) >= 3:
        qs = [s["q"] for s in main_s]
        for key in ("R_total", "R1_plus_R2", "R_total_bulk", "R1", "R2"):
            ys = [s["q_" + key] for s in main_s]
            ses = [max((s["q_" + key + "_hi"] - s["q_" + key + "_lo"]) / 3.919928, 1e-12)
                   for s in main_s]
            trends[key] = trend_test(qs, ys, ses)
            if key in ("R_total", "R1_plus_R2", "R_total_bulk"):
                mc[key] = compare_models(qs, ys, ses)

    (HERE / "metrics").mkdir(exist_ok=True)
    with open(HERE / "metrics" / "rba_decomposition_summary.json", "w", encoding="utf-8") as f:
        json.dump({"summaries": summaries, "full_j_audits": audits, "top5_by_abs_qR": tops,
                   "model_comparison": mc, "trend_tests": trends,
                   "n_bootstrap": NBOOT}, f, indent=2)

    parts = ["<!-- AUTO-GENERATED by rba_decomposition_report.py -->", "",
             "## 2. Main table (primary: literal-spec subset estimator)", "",
             md_main_table(main_s), "",
             "### 2b. Variance-reduced variant (EXACT all-free-j mean for the g_j*A_j term)", "",
             md_bulk_table(main_s), "",
             "## 3. Numerical validation", "", md_validation(summaries), "",
             "## 4. Model comparison", "",
             "_Weighted least squares with KNOWN per-point variances (bootstrap SE, "
             "derived as CI width / 3.919928), so the noise scale is not itself estimated "
             "from 4 residuals. k counts regression coefficients only; "
             "AICc = chi2 + 2k + 2k(k+1)/(N-k-1) with N=4. LOOCV = leave-one-n-out, "
             "RMSE of the 4 held-out predictions._", ""]
    for key, title in (("R_total", "Y_q = q*E[R_q] (subset estimator)"),
                       ("R1_plus_R2", "Y_q = q*E[R1+R2] (subset estimator)"),
                       ("R_total_bulk", "Y_q = q*E[R_q] (bulk-exact estimator)")):
        if key in mc:
            parts += [fmt_models(mc[key], title), ""]
    if trends:
        parts += ["### 4b. Decision statistic -- weighted slope on log q (N=4 points)", "",
                  "| quantity | slope per unit log q | SE | t | p (two-sided) | "
                  "chi2 of the CONSTANT model | best constant |",
                  "|---|---:|---:|---:|---:|---|---:|"]
        for key, title in (("R_total", "q*E[R_q] (subset)"),
                           ("R_total_bulk", "q*E[R_q] (bulk-exact)"),
                           ("R1_plus_R2", "q*E[R1+R2] (subset)"),
                           ("R1", "q*E[R1]"), ("R2", "q*E[R2]")):
            if key in trends:
                parts.append(md_trend(trends[key], title))
        parts += [""]
    parts += ["## Sanity check 1 -- full-j audit (ALL free j vs a random subset, same parent)",
              "", md_audits(audits), "",
              "## Sanity check 3 -- top-5 parents by |q*R| per n (nothing discarded)", "",
              md_tops(tops), ""]
    if other_s:
        parts += ["## Sanity check 2 -- second-seed reproduction", "",
                  md_main_table(other_s), ""]
    (HERE / "rba_decomposition_tables.md").write_text("\n".join(parts), encoding="utf-8")
    print("\n".join(parts))


if __name__ == "__main__":
    main()
