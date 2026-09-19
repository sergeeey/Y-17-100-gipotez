"""Independent re-derivation of the headline slope (controls.md, 'Independent verification').

Different code path from analyze.py: variances from raw sums (no np.var), weights taken from the
bootstrap intervals stored in analysis.json, and the fit done by scipy.optimize.curve_fit with
absolute_sigma=False (residual-scaled covariance), instead of explicit normal equations.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy import stats
from scipy.optimize import curve_fit

METRICS = Path(__file__).resolve().parent / "metrics"


def main() -> None:
    analysis = json.loads((METRICS / "analysis.json").read_text(encoding="utf-8"))
    by_n: dict[int, list[float]] = {}
    for line in (METRICS / "thetas_main.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            rec = json.loads(line)
            by_n.setdefault(rec["n"], []).append(rec["theta"])

    ns, log_var, sig = [], [], []
    for row in analysis["rows"]:
        n = row["n"]
        xs = [math.log(t / math.sqrt(n)) for t in by_n[n]]
        m = sum(xs) / len(xs)
        var = sum((x - m) ** 2 for x in xs) / (len(xs) - 1)
        assert abs(var - row["var"]) < 1e-12 * max(1.0, abs(var)), (n, var, row["var"])
        ns.append(n)
        log_var.append(math.log(var))
        sig.append(row["se_log_var"])

    ln = np.log(np.array(ns, dtype=float))

    def line(x, a, b):
        return a * x + b

    popt, pcov = curve_fit(line, ln, np.array(log_var), sigma=np.array(sig), absolute_sigma=False)
    slope, se = float(popt[0]), float(np.sqrt(pcov[0, 0]))
    dof = len(ns) - 2
    t = float(stats.t.ppf(0.975, dof))
    ci = [slope - t * se, slope + t * se]
    primary = analysis["primary_fit"]
    result = {
        "slope_verify": slope,
        "slope_analyze": primary["slope"],
        "abs_diff_slope": abs(slope - primary["slope"]),
        "ci_verify": ci,
        "ci_analyze": primary["ci95"],
        "abs_diff_ci": max(abs(ci[0] - primary["ci95"][0]), abs(ci[1] - primary["ci95"][1])),
    }
    result["agree_1e-6"] = bool(result["abs_diff_slope"] < 1e-6 and result["abs_diff_ci"] < 1e-6)
    (METRICS / "verify.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
