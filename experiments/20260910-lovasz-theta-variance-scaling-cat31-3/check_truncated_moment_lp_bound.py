"""Point 44: truncated-moment LP bound on C_q using ALREADY-COMPUTED M_1..M_6 (point 38) and the
canonical Johnson eigenvalues gamma_l -- no new theta-solves needed. This is a genuine
falsification test for the entire "moment method" route (Priority C), not another diagnostic.

Classical truncated-moment-problem idea (Chebyshev-Markov-Krein / LP duality for positive
measures given moments -- NOT a new mathematical technique, cited as such, applied here to this
project's own spectral measure E_l on {gamma_1,...,gamma_L}): the spectral energies E_l>=0 form
a positive measure on the finite set {gamma_l}, and M_r=sum_l gamma_l^r E_l are its first s raw
moments (r=1..s). Given ONLY these s moments and positivity, the LP

    U_s := max sum_l E_l  s.t.  E_l>=0,  sum_l gamma_l^r E_l = M_r for r=1..s

gives the LARGEST C_q=sum_l E_l compatible with the observed moments -- an upper bound that is
provably TIGHT given only this information (the true spectrum is a feasible point, so
C_q<=U_s always; and U_s is the best possible bound derivable from moments 1..s alone). The LP
dual gives an explicit degree-s polynomial certificate P(gamma)=sum c_r*gamma^r with P>=1 on
every gamma_l, and U_s = sum c_r*M_r -- i.e. the dual solution IS the sharpest possible
moment-based inequality, found by the solver rather than guessed.

Key falsification use: R_s := U_s/C_q_actual. If R_6 stays large (or grows) with n, the first
six Johnson moments are PROVABLY INSUFFICIENT to pin down C_q at the needed scale -- no amount
of cleverer combining of THESE SAME SIX NUMBERS can ever do better than U_6, so the entire fixed-
moment-order Priority C route is closed by this result, not just this specific attempt at it.
If R_6 shrinks toward 1, the six moments are close to sufficient and a genuine analytic target
(the dual certificate's own polynomial) is directly visible.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"


def gamma_l_array(N: int, q: int) -> np.ndarray:
    L = min(q, N - q)
    ls = np.arange(1, L + 1)
    return ls * (N + 1 - ls) / (q * (N - q))


def solve_moment_lp(gammas: np.ndarray, moments: list[float], maximize: bool) -> dict:
    """max/min sum(E) s.t. E>=0, A@E = moments (A[r,l] = gamma_l^(r+1), r=0..s-1)."""
    s = len(moments)
    L = len(gammas)
    A_eq = np.vstack([gammas**r for r in range(1, s + 1)])
    b_eq = np.array(moments)
    c = -np.ones(L) if maximize else np.ones(L)
    res = linprog(
        c,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=[(0, None)] * L,
        method="highs",
    )
    if not res.success:
        return {"success": False, "message": res.message}
    value = -res.fun if maximize else res.fun
    active = [int(i) + 1 for i, e in enumerate(res.x) if e > 1e-9 * max(res.x.max(), 1e-30)]
    # dual: for equality constraints, linprog (highs) reports marginals in res.eqlin.marginals
    dual = None
    if hasattr(res, "eqlin") and res.eqlin is not None:
        dual = (
            (-np.array(res.eqlin.marginals)).tolist()
            if maximize
            else np.array(res.eqlin.marginals).tolist()
        )
    return {
        "success": True,
        "value": float(value),
        "active_levels": active,
        "n_active": len(active),
        "dual_coeffs": dual,
    }


def run_one(row: dict) -> dict:
    n, N, q = row["n"], row["N"], row["q"]
    C_q = row["C_q"]
    gammas = gamma_l_array(N, q)
    L = len(gammas)
    moments_all = [row[f"M{r}"] for r in range(1, 7)]

    per_s = {}
    for s in range(1, 7):
        moments = moments_all[:s]
        up = solve_moment_lp(gammas, moments, maximize=True)
        lo = solve_moment_lp(gammas, moments, maximize=False)
        R_s = up["value"] / C_q if up["success"] else float("nan")
        per_s[s] = {
            "U_s": up.get("value"),
            "L_s": lo.get("value"),
            "R_s": R_s,
            "active_levels_U": up.get("active_levels"),
            "n_active_U": up.get("n_active"),
            "dual_coeffs_U": up.get("dual_coeffs"),
        }
        print(
            f"  n={n:3d} s={s}: U_s={up.get('value'):.6f} L_s={lo.get('value'):.6f} "
            f"C_q={C_q:.6f} R_s={R_s:.4f} active={up.get('active_levels')}",
            flush=True,
        )

    return {
        "n": n,
        "N": N,
        "q": q,
        "L": L,
        "C_q": C_q,
        "gamma_1": float(gammas[0]),
        "gamma_L": float(gammas[-1]),
        "per_s": per_s,
    }


def run() -> list[dict]:
    with open(METRICS / "higher_moments_M1_M6.json", encoding="utf-8") as f:
        rows = json.load(f)["rows"]
    rows = sorted(rows, key=lambda r: r["n"])

    results = [run_one(r) for r in rows]

    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "truncated_moment_lp_bound.json", "w", encoding="utf-8") as f:
        json.dump({"rows": results}, f, indent=2)

    print("\n--- R_s matrix (U_s / C_q_actual) ---")
    header = "n".rjust(5) + "".join(f"R{s}".rjust(9) for s in range(1, 7))
    print(header)
    for r in results:
        line = str(r["n"]).rjust(5)
        for s in range(1, 7):
            line += f"{r['per_s'][s]['R_s']:9.4f}"
        print(line)

    return results


if __name__ == "__main__":
    run()
    print("\nDone.", flush=True)
