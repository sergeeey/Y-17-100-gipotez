"""Cheap falsification check (user's plan step 4): using ALREADY-COLLECTED exact data
(johnson_swap_energy.json, n=23,29,31,37 -- no new simulation), compute n^3*T_q at central
layers and as a probability-weighted aggregate, and check whether it stabilizes, grows slowly,
or grows as a power law. If it already grows like n^alpha for alpha>0 clearly, the proposed
sufficient lemma T_q=O(n^-3) in the bulk is likely false and should not be pursued analytically.
"""

import json
import math
from pathlib import Path

METRICS_DIR = Path(__file__).resolve().parent / "metrics"

with open(METRICS_DIR / "johnson_swap_energy.json", encoding="utf-8") as f:
    swap_data = json.load(f)


def comb(n, r):
    if r < 0 or r > n:
        return 0
    return math.comb(n, r)


results = []
for n_str, rows in swap_data.items():
    n = int(n_str)
    N = rows[0]["N"]
    valid_rows = [r for r in rows if not (isinstance(r["T_q"], float) and math.isnan(r["T_q"]))]

    # central layer(s): q closest to N/2
    center = N / 2
    valid_rows_sorted = sorted(valid_rows, key=lambda r: abs(r["q"] - center))
    central_q_row = valid_rows_sorted[0]
    Tq_central = central_q_row["T_q"]

    # probability-weighted aggregate T_bar = sum_q w_q T_q, w_q = C(N,q)/2^N
    total_weight = 0.0
    weighted_sum = 0.0
    for r in valid_rows:
        w = comb(N, r["q"]) / (2**N)
        total_weight += w
        weighted_sum += w * r["T_q"]
    T_bar = weighted_sum / total_weight if total_weight > 0 else float("nan")

    results.append(
        {
            "n": n,
            "N": N,
            "central_q": central_q_row["q"],
            "T_q_central": Tq_central,
            "n3_Tq_central": n**3 * Tq_central,
            "T_bar_weighted": T_bar,
            "n3_T_bar": n**3 * T_bar,
        }
    )

results.sort(key=lambda r: r["n"])

print(
    f"{'n':>4} {'N':>3} {'q*':>3} {'T_q(central)':>14} {'n^3*T_q':>12} "
    f"{'T_bar':>12} {'n^3*T_bar':>12}"
)
for r in results:
    print(
        f"{r['n']:>4} {r['N']:>3} {r['central_q']:>3} "
        f"{r['T_q_central']:>14.8f} {r['n3_Tq_central']:>12.4f} "
        f"{r['T_bar_weighted']:>12.8f} {r['n3_T_bar']:>12.4f}"
    )

# rough power-law fit alpha: n^3*T_q ~ n^alpha  =>  log(n3Tq) = alpha*log(n) + const
print()
if len(results) >= 2:
    import statistics

    xs = [math.log(r["n"]) for r in results]
    ys_central = [math.log(r["n3_Tq_central"]) for r in results]
    ys_bar = [math.log(r["n3_T_bar"]) for r in results]

    def slope(xs, ys):
        mx, my = statistics.mean(xs), statistics.mean(ys)
        num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        den = sum((x - mx) ** 2 for x in xs)
        return num / den if den != 0 else float("nan")

    alpha_central = slope(xs, ys_central)
    alpha_bar = slope(xs, ys_bar)
    print(f"Rough log-log slope alpha (n^3*T_q_central ~ n^alpha): {alpha_central:.4f}")
    print(f"Rough log-log slope alpha (n^3*T_bar ~ n^alpha):       {alpha_bar:.4f}")
    print(
        "(alpha near 0 => stabilizing/bounded; alpha>0 clearly => growing, "
        "lemma as stated likely false)"
    )

with open(METRICS_DIR / "n3_Tq_scaling_check.json", "w", encoding="utf-8") as f:
    json.dump({"results": results}, f, indent=2)
