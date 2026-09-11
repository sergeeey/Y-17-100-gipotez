"""Fourth check toward the O(1/n) upper bound, per direct user request to keep trying.

Two things done here, NEITHER of which is a new expensive experiment -- both reuse data and
facts already on disk:

1. A structural check of whether the paper's OTHER primal/dual LP formulations ('time domain':
   max sum(x_i) s.t. Fx>=0, x_0=1, x_k=0 for edges) offer an escape from the same obstruction
   found in decision.md points 6 and 8. Conclusion (reasoned, not computed): dropping x_i=0 is
   classical LP variable-unfixing sensitivity, which is STILL governed by a concave
   piecewise-linear value function in the freed variable -- the same "how far does the vertex
   move" question, just relabeled. The paper's 4 LPs are connected by an invertible linear map
   (Fourier transform) and LP strong duality, both of which preserve optimal values exactly but
   do NOT trivialize vertex-stability questions. No escape found; not a new attempt, a ruled-out
   one, honestly reported as such in decision.md.

2. A re-reading of THIS project's OWN already-collected single_generator_sensitivity.json
   (n=128,512,1536): computes n*(Efron-Stein bound) explicitly and checks whether it is
   trending toward a constant (which is exactly what the O(1/n) claim requires) -- this is
   EMPIRICAL evidence, not a proof, but it had not been stated in exactly these terms before.
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

data = json.load(open(METRICS / "single_generator_sensitivity.json", encoding="utf-8"))

print(f"{'n':>6} {'ES bound':>12} {'n*ES_bound':>12} {'measured V_n':>14} {'n*V_n':>10}")

main_sweep = json.load(open(METRICS / "run.json", encoding="utf-8"))
measured_var = {row["n"]: row["var_log_ratio"] for row in main_sweep["sweep"]}

rows = []
for row in data["rows"]:
    n = row["n"]
    es_bound = row["efron_stein_bound_on_var_X"]
    v_n = measured_var[n]
    rows.append(
        {
            "n": n,
            "es_bound": es_bound,
            "n_times_es_bound": n * es_bound,
            "measured_V_n": v_n,
            "n_times_measured_V_n": n * v_n,
        }
    )
    print(f"{n:6d} {es_bound:12.6f} {n * es_bound:12.4f} {v_n:14.6f} {n * v_n:10.4f}")

with open(METRICS / "own_data_upper_bound_signal.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, indent=2)

print(
    "\nIf n*(ES bound) is roughly CONSTANT across n, that is empirical (not proven) support "
    "for Sum_i E[(Delta_i X)^2] = O(1/n), i.e. the target Efron-Stein upper bound itself -- "
    "distinct from, and not implied by, any of the 3 failed proof attempts in points 6/8."
)
