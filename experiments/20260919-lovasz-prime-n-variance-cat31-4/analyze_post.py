"""POST-REGISTRATION exploratory analysis (not part of the locked verdict in claim.md).

Question asked only after the locked result (P-MINUS-ONE): are the prime and composite ensembles
consistent with ONE common slope, and what does a joint fit say about -1?
Uses H-CAT31-3's composite rows (metrics/run.json there) and this experiment's prime rows.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
COMPOSITE = HERE.parent / "20260910-lovasz-theta-variance-scaling-cat31-3" / "metrics" / "run.json"


def rows() -> tuple[list[dict], list[dict]]:
    comp = []
    for r in json.loads(COMPOSITE.read_text(encoding="utf-8"))["sweep"]:
        lo, hi = r["var_log_ratio_bootstrap_ci95"]
        v = r["var_log_ratio"]
        comp.append({"n": r["n"], "var": v, "se": (hi - lo) / (2 * 1.96 * v), "prime": 0})
    prime = []
    for r in json.loads((HERE / "metrics" / "analysis.json").read_text(encoding="utf-8"))["rows"]:
        prime.append({"n": r["n"], "var": r["var"], "se": r["se_log_var"], "prime": 1})
    return comp, prime


def wls(x_cols: list[np.ndarray], y: np.ndarray, se: np.ndarray) -> dict:
    X = np.vstack(x_cols).T
    w = 1.0 / se**2
    XtWX = X.T @ (w[:, None] * X)
    beta = np.linalg.solve(XtWX, X.T @ (w * y))
    resid = y - X @ beta
    dof = len(y) - X.shape[1]
    sigma2 = float(np.sum(w * resid**2)) / dof
    cov = sigma2 * np.linalg.inv(XtWX)
    t = float(stats.t.ppf(0.975, dof))
    se_b = np.sqrt(np.diag(cov))
    return {
        "beta": beta.tolist(),
        "se": se_b.tolist(),
        "ci95": [[float(b - t * s), float(b + t * s)] for b, s in zip(beta, se_b, strict=True)],
        "dof": dof,
        "sigma2_resid_scale": sigma2,
    }


def main() -> None:
    comp, prime = rows()
    allr = comp + prime
    ln = np.log(np.array([r["n"] for r in allr], dtype=float))
    y = np.log(np.array([r["var"] for r in allr]))
    se = np.array([r["se"] for r in allr])
    is_p = np.array([r["prime"] for r in allr], dtype=float)
    out = {
        "common_slope_and_prime_shift": wls([ln, np.ones_like(ln), is_p], y, se),
        "separate_slopes": wls([ln, np.ones_like(ln), is_p, is_p * ln], y, se),
        "common_slope_no_shift": wls([ln, np.ones_like(ln)], y, se),
        "note": (
            "beta order: slope, intercept, prime-level-shift[, prime-slope-difference]. "
            "Exploratory, post-registration; the locked verdict is in analysis.json."
        ),
    }
    (HERE / "metrics" / "analysis_post.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
