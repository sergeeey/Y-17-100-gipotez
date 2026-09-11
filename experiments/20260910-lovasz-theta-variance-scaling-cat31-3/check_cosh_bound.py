"""Verify the exact inequality Var(X_n) <= 2*(E[theta]/sqrt(n) - 1) against H-CAT31-3's
own already-collected sweep data. Derivation (independently re-derived, not trusted from
the pasted external text): by the Lovasz identity theta(G)*theta(Gbar)=n (already used in
this experiment's own substrate gate) and self-complementarity in distribution at p=0.5,
X_n = log(theta/sqrt(n)) satisfies X_n =d= -X_n exactly, so E[X_n]=0 and
E[e^{X_n}] = E[e^{-X_n}] = E[cosh(X_n)] = E[theta]/sqrt(n). Since cosh(x) >= 1+x^2/2 for all
real x, E[cosh(X_n)] >= 1 + Var(X_n)/2, giving the stated bound. No new compute needed --
pure recheck of stored metrics/run.json as a numerical sanity/positive-control check on
data already on disk.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
d = json.load(open(HERE / "metrics" / "run.json", encoding="utf-8"))

print(f"{'n':>6} {'V_n (measured)':>16} {'RHS=2(E/sqrt(n)-1)':>20} {'RHS-LHS':>10} {'holds?':>8}")
rows = []
for r in d["sweep"]:
    n = r["n"]
    V = r["var_log_ratio"]
    ratio = r["mean_theta_over_sqrt_n"]
    rhs = 2 * (ratio - 1)
    holds = rhs >= V
    rows.append({"n": n, "V_n": V, "rhs": rhs, "margin": rhs - V, "holds": holds})
    print(f"{n:6d} {V:16.6f} {rhs:20.6f} {rhs - V:10.6f} {'OK' if holds else 'VIOLATED':>8}")

out = HERE / "metrics" / "cosh_bound_check.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(rows, f, indent=2)
print(f"\nAll hold: {all(r['holds'] for r in rows)}")
print(f"Written: {out}")
